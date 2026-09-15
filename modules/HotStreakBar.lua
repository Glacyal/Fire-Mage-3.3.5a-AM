-- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo: Barra Hot Streak (264x7px)
--- =========================================================================
--- Gestisce il monitoraggio in tempo reale del talento Hot Streak (Lancio Istantaneo)
--- posizionata immediatamente sotto la Barra del Mana (264x7px):
--- - 1° Critico non-periodico: illumina esattamente metà barretta (50%, 130px ambra vivo)
---   e RESTA PERSISTENTE nel tempo. I DoT (Ignite, tick Living Bomb) non azzerano la serie.
---   Si azzera solo su colpo diretto non-critico, uscita dal combat o morte.
--- - 2° Critico consecutivo (Proc Hot Streak): i due segmenti diventano un'UNICA BARRA
---   al 100% (264px) con Pixel Glow, che mostra il TIMING con il conto alla rovescia di 10s!
--- - Lancio di Pyroblast (o scadenza buff): consuma immediatamente l'effetto
---   e azzera istantaneamente la barra a 0.
--- =========================================================================

FireMageHUD_HotStreak = FireMageHUD_HotStreak or {
    streak = 0,
    hasBuff = false,
    duration = 10,
    expirationTime = 0,
    lastTimestamp = 0,
    lastSpellId = 0,
    lastDestGUID = "",
}

local HS = FireMageHUD_HotStreak

-- Tabella spell valide per Hot Streak (colpi diretti non-periodici)
local QUALIFYING_SPELLS = {
    -- Fireball (tutti i rank)
    [133] = true, [143] = true, [145] = true, [3140] = true, [8400] = true,
    [8401] = true, [8402] = true, [10148] = true, [10149] = true, [10150] = true,
    [10151] = true, [25306] = true, [27070] = true, [38692] = true, [42832] = true, [42833] = true,
    -- Fire Blast (tutti i rank)
    [2136] = true, [2137] = true, [2138] = true, [8412] = true, [8413] = true,
    [10197] = true, [10199] = true, [27078] = true, [27079] = true, [42872] = true, [42873] = true,
    -- Scorch (tutti i rank)
    [2948] = true, [8444] = true, [8445] = true, [8446] = true, [10205] = true,
    [10206] = true, [10207] = true, [27073] = true, [27074] = true, [42858] = true, [42859] = true,
    -- Frostfire Bolt (Rank 1 e 2)
    [44614] = true, [47610] = true,
    -- Living Bomb (Rank 1, 2 e 3)
    [44461] = true, [55361] = true, [55362] = true, [44457] = true, [55359] = true, [55360] = true,
}

local function IsQualifyingSpell(spellId, spellName)
    if spellId and QUALIFYING_SPELLS[spellId] then
        return true
    end
    if spellName then
        if string.find(spellName, "Fireball") or string.find(spellName, "Palla di Fuoco") or
           string.find(spellName, "Fire Blast") or string.find(spellName, "Deflagrazione") or
           string.find(spellName, "Scorch") or string.find(spellName, "Bruciatura") or
           string.find(spellName, "Frostfire") or string.find(spellName, "Fuocogelo") or
           string.find(spellName, "Living Bomb") or string.find(spellName, "Bomba Vivente") then
            return true
        end
    end
    return false
end

--- Sincronizza lo stato di Hot Streak con i buff correnti del giocatore.
local function SyncHotStreakBuff()
    local found = false
    for i = 1, 40 do
        local name, _, _, _, _, dur, expTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 48108 or name == "Hot Streak" or name == "Buona sorte" or string.find(name, "Hot Streak") then
            found = true
            HS.hasBuff = true
            HS.streak = 2
            HS.duration = (dur and dur > 0) and dur or 10
            HS.expirationTime = (expTime and expTime > 0) and expTime or (GetTime() + HS.duration)
            break
        end
    end
    if not found and HS.hasBuff then
        -- Il buff Hot Streak e' stato consumato o e' scaduto
        HS.hasBuff = false
        HS.streak = 0
        HS.expirationTime = 0
    end
end

local function NotifyWA()
    if WeakAuras and WeakAuras.ScanEvents then
        WeakAuras.ScanEvents("FMHUD_HS_UPDATE")
    end
end

--- Gestione eventi per la barra Hot Streak (CLEU, UNIT_AURA, SPELLCAST, REGEN)
---@param event string Nome evento WoW
---@param ... any Argomenti dell'evento
function FireMageHUD_HotStreak_OnEvent(event, ...)
    if event == "PLAYER_ENTERING_WORLD" then
        HS.streak = 0
        HS.hasBuff = false
        HS.expirationTime = 0
        SyncHotStreakBuff()
        NotifyWA()
    elseif event == "PLAYER_DEAD" or event == "PLAYER_UNGHOST" then
        HS.streak = 0
        HS.hasBuff = false
        HS.expirationTime = 0
        NotifyWA()
    elseif event == "PLAYER_REGEN_ENABLED" then
        if not HS.hasBuff and HS.streak > 0 then
            HS.streak = 0
            NotifyWA()
        end
    elseif event == "UNIT_AURA" then
        local unit = ...
        if unit == "player" then
            local oldBuff = HS.hasBuff
            SyncHotStreakBuff()
            if oldBuff ~= HS.hasBuff then
                NotifyWA()
            end
        end
    elseif event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spellName, _, _, spellId = ...
        if unit == "player" then
            -- Se viene lanciata Pyroblast, il buff Hot Streak viene consumato all'istante
            if spellId == 11366 or spellId == 12505 or spellId == 12522 or spellId == 12523 or
               spellId == 12524 or spellId == 12525 or spellId == 12526 or spellId == 33938 or
               spellId == 42890 or spellId == 42891 or (spellName and (string.find(spellName, "Pyro") or string.find(spellName, "Piro"))) then
                HS.hasBuff = false
                HS.streak = 0
                HS.expirationTime = 0
                NotifyWA()
            end
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local subEvent = select(2, ...)
        if subEvent == "SPELL_DAMAGE" then
            local sourceGUID = select(3, ...)
            local sourceName = select(4, ...)
            local sourceFlags = select(5, ...)
            local destGUID = select(6, ...)
            local destName = select(7, ...)
            local destFlags = select(8, ...)

            local isPlayer = (sourceGUID == UnitGUID("player")) or (sourceName and sourceName == UnitName("player"))
            if not isPlayer and sourceFlags and bit and bit.band then
                if bit.band(sourceFlags, 0x00000001) > 0 then
                    isPlayer = true
                end
            end

            -- Solo colpi eseguiti dal giocatore
            if isPlayer then
                local spellId = select(10, ...)
                local spellName = select(11, ...)
                if not IsQualifyingSpell(spellId, spellName) then
                    spellId = select(9, ...)
                    spellName = select(10, ...)
                end

                if IsQualifyingSpell(spellId, spellName) then
                    local timestamp = select(1, ...)
                    destGUID = select(6, ...) or destGUID or ""

                    if HS.lastTimestamp ~= timestamp or HS.lastSpellId ~= spellId or HS.lastDestGUID ~= destGUID then
                        HS.lastTimestamp = timestamp
                        HS.lastSpellId = spellId
                        HS.lastDestGUID = destGUID

                        local c18, c19, c20 = select(18, ...)
                        local isCrit = (c19 == true or c18 == true or c20 == true or c19 == 1 or c18 == 1)

                        if isCrit then
                            if not HS.hasBuff then
                                if HS.streak == 0 then
                                    -- 1° Critico: illumina metà barretta a 50%
                                    HS.streak = 1
                                    NotifyWA()
                                else
                                    -- 2° Critico: entra in Hot Streak
                                    HS.streak = 2
                                    HS.hasBuff = true
                                    HS.duration = 10.0
                                    HS.expirationTime = GetTime() + 10.0
                                    NotifyWA()
                                end
                            end
                        else
                            -- Colpo non-critico: azzera la serie se non c'e' gia' Hot Streak attivo
                            if not HS.hasBuff and HS.streak > 0 then
                                HS.streak = 0
                                NotifyWA()
                            end
                        end
                    end
                end
            end
        end
    end
end

-- Frame nativo WoW registrato per l'addon
local hsFrame = CreateFrame("Frame", "FireMageHUD_HotStreak_Frame")
hsFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
hsFrame:RegisterEvent("PLAYER_DEAD")
hsFrame:RegisterEvent("PLAYER_UNGHOST")
hsFrame:RegisterEvent("PLAYER_REGEN_ENABLED")
hsFrame:RegisterEvent("UNIT_AURA")
hsFrame:RegisterEvent("UNIT_SPELLCAST_SUCCEEDED")
hsFrame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
hsFrame:SetScript("OnEvent", function(self, event, ...)
    FireMageHUD_HotStreak_OnEvent(event, ...)
end)

--- Restituisce lo stato corrente della Barretta 1 (Sinistra, 1° Critico - 50%).
--- Visibile SOLO sul 1° critico, sparisce al proc della barra unica.
---@return boolean isVisible True se attiva al 50%
---@return number current Valore corrente (1)
---@return number max Valore massimo (1)
function FireMageHUD_HotStreak_Segment1()
    SyncHotStreakBuff()
    local isVisible = (HS.streak == 1 and not HS.hasBuff)
    return isVisible, 1, 1
end

--- Restituisce lo stato corrente della Barra Unificata di Proc (264px intera, 10s Timing).
---@return boolean isVisible True se Hot Streak proc e' attivo
---@return number remaining Secondi rimanenti prima della scadenza
---@return number duration Durata totale del buff (10.0s)
function FireMageHUD_HotStreak_ProcBar()
    SyncHotStreakBuff()
    if HS.hasBuff and HS.expirationTime and HS.expirationTime > GetTime() then
        local rem = math.max(0, HS.expirationTime - GetTime())
        return true, rem, HS.duration or 10.0
    end
    return false, 0, 10.0
end

-- Alias di retrocompatibilita'
FireMageHUD_HotStreak_Segment2 = FireMageHUD_HotStreak_ProcBar

