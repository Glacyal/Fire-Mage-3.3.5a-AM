--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 11: Smart Living Bomb Target Assistant
--- =========================================================================
--- Tracker interattivo a barre di avanzamento (Aurabar) per l'applicazione
--- ottimale di Living Bomb su bersagli multipli.
--- Posizionato sul lato destro dell'HUD (xOffset = +250, yOffset = +40).
---
--- Caratteristiche:
--- 1. Auto-Hide Intelligente:
---    - Il modulo e completamente invisibile quando non ci sono nemici attaccabili
---      selezionati, in combat o con Living Bomb attiva. Zero ingombro a schermo!
--- 2. Nessuna Sovrapposizione:
---    - Coordinate ottimizzate (x = +250, y = +40) per garantire oltre 35px di
---      distacco dalla Mana Bar (termina a +132) e posizionamento sopra i tasti utility.
--- 3. Indicatori di Stato [V] e [X]:
---    - [V] (Verde): Bersaglio con Living Bomb gia attiva. La barra arancione fuoco
---      scorre visualizzando il countdown dei 12 secondi (12.0s -> 0.0s).
---    - [X] (Rosso): Bersaglio privo di Living Bomb. La barra mostra la percentuale
---      di vita (HP %) colorata in base alla fascia di priorita (Medi/Alti/Bassi).
--- 4. Interazione Cliccabile (Click-to-Target):
---    - Ciascuna barra e agganciata a un SecureActionButtonTemplate.
---    - Fuori dal combat, il click seleziona istantaneamente il bersaglio (/targetexact).
---    - In combat, protetto da InCombatLockdown() per azzerare rischi di blocco UI o taint.
--- =========================================================================

---@class SmartLivingBombSlot
---@field guid string GUID univoco dell'unità
---@field name string Nome del mob
---@field hpPct number Percentuale salute (0-100)
---@field unit string|nil Token unità (es. "target", "raid1target")
---@field hasLB boolean True se Living Bomb è attiva [V], false se assente [X]
---@field exp number Timestamp di scadenza di Living Bomb (GetTime() + rem)
---@field tier number Fascia di priorità per [X] (1 = Medi, 2 = Alti, 3 = Bassi)
---@field isTop boolean True per il bersaglio #1 consigliato

--- Tabella di stato globale del modulo Smart Living Bomb
_G.FMHUD_SmartLB = _G.FMHUD_SmartLB or {
    LB_Active  = {},    -- [guid] = { exp = timestamp, name = mobName, unit = u }
    LastUpdate = 0,     -- Timestamp ultimo calcolo per throttling
    Slots      = {},    -- Array di slot ordinati (da 1 a maxEntries)
}

--- Configurazione predefinita (sovrascrivibile via WeakAuras Custom Options o Config.lua)
_G.FMHUD_SmartLB_Config = _G.FMHUD_SmartLB_Config or {
    MedMin       = 40,   -- Soglia minima HP Medi (%)
    MedMax       = 70,   -- Soglia massima HP Medi (%)
    HighMax      = 100,  -- Soglia massima HP Alti (%)
    LowMin       = 0,    -- Soglia minima HP Bassi (%)
    MaxEntries   = 5,    -- Numero massimo di barre visualizzate
    OnlyInCombat = false -- Se true, nasconde il pannello fuori dal combat
}

--- Intercetta gli eventi del Combat Log per tracciare Living Bomb e la morte dei mob in tempo reale.
---@param ... any Argomenti dell'evento COMBAT_LOG_EVENT_UNFILTERED
function FireMageHUD_SmartLB_OnCombatLog(...)
    local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
    local lb = _G.FMHUD_SmartLB.LB_Active
    if not destGUID then return end

    -- Traccia applicazione e rinnovo di Living Bomb da parte del mago
    if sourceGUID == UnitGUID("player") then
        local isLB = (spellName == "Living Bomb" or spellName == "Bomba Vivente" or spellId == 44457 or spellId == 55359 or spellId == 55360)
        if isLB then
            if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" then
                lb[destGUID] = {
                    exp  = GetTime() + 12.0,
                    name = destName or "Enemy",
                    guid = destGUID,
                }
            elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                lb[destGUID] = nil
            end
        end
    end

    -- Pulizia istantanea alla morte del mob
    if subEvent == "UNIT_DIED" or subEvent == "PARTY_KILL" then
        lb[destGUID] = nil
    end
end

--- Calcola e restituisce i dati per un singolo slot della barra (da 1 a maxEntries).
--- Include throttling per azzerare l'impatto su CPU anche in raid da 25 giocatori.
---@param slotIndex number Indice slot richiesto (1..5)
---@param customConfig table|nil Tabella opzioni opzionale
---@return SmartLivingBombSlot|nil slotData Dati per lo slot specificato
function FireMageHUD_SmartLB_GetSlotData(slotIndex, customConfig)
    local now = GetTime()
    local state = _G.FMHUD_SmartLB

    -- Throttling di ricalcolo a ~0.08s (12 FPS)
    if (now - (state.LastUpdate or 0)) >= 0.08 or not state.Slots then
        state.LastUpdate = now

        -- Pulizia scadenze Living Bomb superate
        for guid, data in pairs(state.LB_Active) do
            local exp = (type(data) == "table") and data.exp or data
            if exp <= now then
                state.LB_Active[guid] = nil
            end
        end

        -- Risoluzione soglie di configurazione
        local cfg = customConfig or {}
        local globalCfg = _G.FireMageHUD_Config and _G.FireMageHUD_Config.SmartLivingBomb or _G.FMHUD_SmartLB_Config or {}
        local medMin     = cfg.medMin or globalCfg.MedMin or 40
        local medMax     = cfg.medMax or globalCfg.MedMax or 70
        local highMax    = cfg.highMax or globalCfg.HighMax or 100
        local maxEntries = cfg.maxEntries or globalCfg.MaxEntries or 5

        local seenGUIDs = {}
        local activeLB = {}   -- Lista [V] (Living Bomb attiva, barra timer 12s -> 0)
        local missingLB = {}  -- Lista [X] (Candidati privi di Living Bomb, barra HP)

        --- Analizza una singola unità raggiungibile
        ---@param u string Token unità
        local function inspectUnit(u)
            if not UnitExists(u) then return end
            if UnitIsDeadOrGhost(u) then return end
            if not UnitCanAttack("player", u) or UnitIsFriend("player", u) then return end

            local guid = UnitGUID(u)
            if not guid or seenGUIDs[guid] then return end
            seenGUIDs[guid] = true

            local hp = UnitHealth(u) or 0
            local maxHp = UnitHealthMax(u) or 1
            if hp <= 0 then return end

            local pct = (maxHp > 0) and math.floor((hp / maxHp) * 100) or 100
            if pct > 100 then pct = 100 end
            if pct < 0 then pct = 0 end

            local name = UnitName(u) or "Enemy"
            if name == "" then name = "Enemy" end

            local hasLB = false
            local lbExp = 0

            -- 1. Controllo debuff diretti sull'unità
            for i = 1, 40 do
                local debName, _, _, _, _, _, exp, caster, _, _, debSpellId = UnitDebuff(u, i)
                if not debName then break end
                if (debName == "Living Bomb" or debName == "Bomba Vivente" or debSpellId == 55360 or debSpellId == 55359 or debSpellId == 44457) and (caster == "player" or not caster) then
                    hasLB = true
                    lbExp = (exp and exp > 0) and exp or (now + 12.0)
                    state.LB_Active[guid] = { exp = lbExp, name = name, guid = guid, unit = u }
                    break
                end
            end

            -- 2. Controllo cache recente del Combat Log
            if not hasLB and state.LB_Active[guid] then
                local lbData = state.LB_Active[guid]
                local exp = (type(lbData) == "table") and lbData.exp or lbData
                if exp > now then
                    hasLB = true
                    lbExp = exp
                end
            end

            if hasLB then
                table.insert(activeLB, {
                    guid  = guid,
                    name  = name,
                    hpPct = pct,
                    unit  = u,
                    hasLB = true,
                    exp   = lbExp,
                    tier  = 1,
                    isTop = false,
                })
            else
                table.insert(missingLB, {
                    guid  = guid,
                    name  = name,
                    hpPct = pct,
                    unit  = u,
                    hasLB = false,
                    exp   = 0,
                    tier  = 1,
                    isTop = false,
                })
            end
        end

        -- 1. Scansione Unita Dirette del Giocatore
        inspectUnit("target")
        inspectUnit("focus")
        inspectUnit("mouseover")
        inspectUnit("targettarget")
        inspectUnit("focustarget")
        inspectUnit("boss1")
        inspectUnit("boss2")
        inspectUnit("boss3")
        inspectUnit("boss4")

        -- 2. Scansione Bersagli del Raid o Party
        local numRaid = GetNumRaidMembers()
        if numRaid and numRaid > 0 then
            local limit = math.min(numRaid, 40)
            for r = 1, limit do
                inspectUnit("raid" .. r .. "target")
            end
        else
            local numParty = GetNumPartyMembers()
            if numParty and numParty > 0 then
                for p = 1, numParty do
                    inspectUnit("party" .. p .. "target")
                end
            end
        end

        -- 3. Mobs con Living Bomb tracciati da Combat Log ma non attualmente targhettati
        for guid, lbData in pairs(state.LB_Active) do
            if not seenGUIDs[guid] then
                local exp = (type(lbData) == "table") and lbData.exp or lbData
                local name = (type(lbData) == "table") and lbData.name or "Enemy"
                if exp > now then
                    seenGUIDs[guid] = true
                    table.insert(activeLB, {
                        guid  = guid,
                        name  = name,
                        hpPct = 100,
                        unit  = nil,
                        hasLB = true,
                        exp   = exp,
                        tier  = 1,
                        isTop = false,
                    })
                end
            end
        end

        -- Ordinamento [V] (Living Bomb Attiva): chi scade prima in cima (timer a scorrimento 12s -> 0s)
        table.sort(activeLB, function(a, b) return a.exp < b.exp end)

        -- Partizione a tre fasce per i bersagli privi di Living Bomb [X]
        local tier1_Med  = {}
        local tier2_High = {}
        local tier3_Low  = {}

        for _, mob in ipairs(missingLB) do
            if mob.hpPct >= medMin and mob.hpPct <= medMax then
                mob.tier = 1
                table.insert(tier1_Med, mob)
            elseif mob.hpPct > medMax and mob.hpPct <= highMax then
                mob.tier = 2
                table.insert(tier2_High, mob)
            else
                mob.tier = 3
                table.insert(tier3_Low, mob)
            end
        end

        -- Ordinamento interno a ciascuna fascia
        table.sort(tier1_Med, function(a, b) return a.hpPct > b.hpPct end)
        table.sort(tier2_High, function(a, b) return a.hpPct < b.hpPct end)
        table.sort(tier3_Low, function(a, b) return a.hpPct > b.hpPct end)

        local sortedMissing = {}
        for _, m in ipairs(tier1_Med) do table.insert(sortedMissing, m) end
        for _, m in ipairs(tier2_High) do table.insert(sortedMissing, m) end
        for _, m in ipairs(tier3_Low) do table.insert(sortedMissing, m) end

        -- Contrassegna il bersaglio #1 consigliato per Living Bomb
        if #sortedMissing > 0 then
            sortedMissing[1].isTop = true
        end

        -- Composizione Slots: Prima [V] (Bombe attive), poi [X] (Candidati da dottare)
        local slots = {}
        for _, m in ipairs(activeLB) do
            if #slots < maxEntries then
                table.insert(slots, m)
            end
        end
        for _, m in ipairs(sortedMissing) do
            if #slots < maxEntries then
                table.insert(slots, m)
            end
        end

        state.Slots = slots
    end

    return state.Slots and state.Slots[slotIndex] or nil
end

--- Verifica se esistono dati attivi per mostrare il modulo (Auto-Hide).
---@param customConfig table|nil Tabella opzioni opzionale
---@return boolean hasData True se ci sono bersagli validi o bombe attive
function FireMageHUD_SmartLB_HasData(customConfig)
    if UnitInVehicle and UnitInVehicle("player") then return false end
    local d = FireMageHUD_SmartLB_GetSlotData(1, customConfig)
    return d ~= nil
end

--- Alias globali per WeakAuras
_G.FMHUD_SmartLB_GetSlotData = FireMageHUD_SmartLB_GetSlotData
_G.FMHUD_SmartLB_OnCombatLog = FireMageHUD_SmartLB_OnCombatLog
_G.FMHUD_SmartLB_HasData     = FireMageHUD_SmartLB_HasData
