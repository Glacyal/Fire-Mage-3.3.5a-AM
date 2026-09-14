--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 04: Focus Magic Monitor
--- =========================================================================
--- Monitora l'applicazione del buff Focus Magic (x = -182, y = -54):
--- - Durata > 5 minuti: Completamente NASCOSTA per pulizia visiva in combattimento.
--- - Durata <= 5 minuti: COMPARE automaticamente con countdown e swipe per il rinnovo.
--- - NON applicato / Scaduto / Bersaglio morto: Icona grigia con avviso rosso "OFF".
--- 
--- Riconoscimento intelligente dello stato attivo:
--- 1. Intercettazione eventi: UNIT_SPELLCAST_SUCCEEDED e COMBAT_LOG_EVENT_UNFILTERED.
--- 2. Scansione alleati: target, focus, raid1..40, party1..4.
--- 3. Proc critico sul mago (Spell ID 54648, 10s):
---    Se il mago riceve il proc da critico del compagno, questo costituisce la prova
---    matematica che il buff da 30 minuti è attivo sull'alleato. Lo stato non
---    commuta MAI su "OFF" e non richiede di ritarghettare manualmente l'alleato.
--- =========================================================================

local FOCUS_MAGIC_BUFF_EN = "Focus Magic"
local FOCUS_MAGIC_BUFF_IT = "Focalizzazione Magica"
local FOCUS_MAGIC_SPELL_ID = 54646 -- Buff 30 min applicato all'alleato
local FOCUS_MAGIC_PROC_ID  = 54648 -- Buff proc 10s attivo sul mago al critico dell'alleato

--- Tabella di stato condivisa per memorizzare l'applicazione e la scadenza
FMHUD_State = FMHUD_State or {}

--- Gestisce gli eventi di Combat Log e Spellcast Succeeded per intercettare l'assegnazione e i proc.
---@param event string Nome evento
---@param ... any Argomenti dell'evento
function FireMageHUD_FocusMagic_OnEvent(event, ...)
    local now = GetTime()

    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and (spell == FOCUS_MAGIC_BUFF_EN or spell == FOCUS_MAGIC_BUFF_IT) then
            FMHUD_State.FMTarget = UnitName("target") or "Ally"
            FMHUD_State.FMExpires = now + 1800
            FMHUD_State.FMDur = 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        local isFM = (spellName == FOCUS_MAGIC_BUFF_EN or spellName == FOCUS_MAGIC_BUFF_IT or spellId == FOCUS_MAGIC_SPELL_ID or spellId == FOCUS_MAGIC_PROC_ID)

        if isFM then
            -- 1. Assegnazione sull'alleato da parte del mago (spellId 54646, durata 30 minuti)
            if sourceGUID == UnitGUID("player") and spellId ~= FOCUS_MAGIC_PROC_ID then
                if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                    FMHUD_State.FMTarget = destName or "Ally"
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMDur = 1800
                elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                    FMHUD_State.FMExpires = 0
                    FMHUD_State.FMTarget = nil
                end
            -- 2. Attivazione proc critico sul mago (spellId 54648, 10s): conferma buff attivo sull'alleato!
            elseif destGUID == UnitGUID("player") and (subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH") then
                if not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMDur = 1800
                end
            end
        elseif subEvent == "UNIT_DIED" and FMHUD_State.FMTarget and destName == FMHUD_State.FMTarget then
            FMHUD_State.FMExpires = 0
            FMHUD_State.FMTarget = nil
        end
    end
end

--- Scansiona un'unità amica per verificare la presenza di Focus Magic lanciato dal player.
---@param unit string Unità da controllare (es. "target", "raid1")
---@return boolean isFound
local function CheckUnitFocusMagic(unit)
    if not UnitExists(unit) then return false end
    for i = 1, 40 do
        local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff(unit, i)
        if not n then break end
        if (n == FOCUS_MAGIC_BUFF_EN or n == FOCUS_MAGIC_BUFF_IT or spellId == FOCUS_MAGIC_SPELL_ID) and (c == "player" or not c) then
            local now = GetTime()
            FMHUD_State.FMExpires = (exp and exp > 0) and exp or (now + 1800)
            FMHUD_State.FMDur = dur or 1800
            FMHUD_State.FMTarget = UnitName(unit)
            return true
        end
    end
    return false
end

--- Verifica se il giocatore possiede attualmente il buff proc di 10 secondi (Spell ID 54648).
---@return boolean isProcActive
local function CheckPlayerProcActive()
    for i = 1, 40 do
        local n, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if spellId == FOCUS_MAGIC_PROC_ID or n == FOCUS_MAGIC_BUFF_EN or n == FOCUS_MAGIC_BUFF_IT then
            return true
        end
    end
    return false
end

--- Scansiona l'intero gruppo/raid, il target, il focus e il player alla ricerca del buff applicato.
---@return boolean isApplied
function FireMageHUD_HasFocusMagicApplied()
    local now = GetTime()

    -- 1. Controllo proc attivo di 10 secondi sul player (prova assoluta di buff attivo sull'alleato)
    if CheckPlayerProcActive() then
        if not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
            FMHUD_State.FMExpires = now + 1800
            FMHUD_State.FMDur = 1800
        end
        return true
    end

    -- 2. Controllo cache da eventi recenti ancora validi
    if FMHUD_State.FMExpires and FMHUD_State.FMExpires > now then
        return true
    end

    -- 3. Target e Focus amici
    if CheckUnitFocusMagic("target") or CheckUnitFocusMagic("focus") then
        return true
    end

    -- 4. Membri del Raid o Party
    local nr = GetNumRaidMembers()
    if nr and nr > 0 then
        for r = 1, nr do
            if CheckUnitFocusMagic("raid" .. r) then return true end
        end
    else
        local np = GetNumPartyMembers()
        if np and np > 0 then
            for p = 1, np do
                if CheckUnitFocusMagic("party" .. p) then return true end
            end
        end
    end

    return false
end

--- Trigger Active: visualizza l'icona SOLO se la durata residua è <= 5 minuti (300s).
---@param event string Nome evento
---@param ... any
---@return boolean shouldDisplay
function FireMageHUD_FocusMagic_Active_Trigger(event, ...)
    FireMageHUD_FocusMagic_OnEvent(event, ...)
    FireMageHUD_HasFocusMagicApplied()
    local now = GetTime()
    local rem = (FMHUD_State.FMExpires and FMHUD_State.FMExpires > now) and (FMHUD_State.FMExpires - now) or 0
    return rem > 0 and rem <= 300
end

--- Restituisce durata e scadenza per lo swipe di ricarica.
---@return number duration, number expiration
function FireMageHUD_FocusMagic_Active_Duration()
    local now = GetTime()
    local rem = (FMHUD_State.FMExpires and FMHUD_State.FMExpires > now) and (FMHUD_State.FMExpires - now) or 0
    if rem > 0 and rem <= 300 then
        return FMHUD_State.FMDur or 1800, FMHUD_State.FMExpires
    end
    return 0, 0
end

--- Testo countdown (%c) per Focus Magic attivo sotto i 5 minuti.
---@return string formattedTime
function FireMageHUD_FocusMagic_Active_CustomText()
    local now = GetTime()
    local rem = (FMHUD_State.FMExpires and FMHUD_State.FMExpires > now) and (FMHUD_State.FMExpires - now) or 0
    if rem > 60 and rem <= 300 then
        local m = math.floor(rem / 60)
        local s = math.floor(rem % 60)
        return string.format("|cFFFFFF00%d:%02d|r", m, s)
    elseif rem > 0 and rem <= 60 then
        return string.format("|cFFFF4444%.0fs|r", rem)
    end
    return ""
end

--- Trigger OFF: mostra l'icona desaturata con avviso "OFF" se il buff non è assegnato.
---@param event string Nome evento
---@param ... any
---@return boolean isMissing
function FireMageHUD_FocusMagic_OFF_Trigger(event, ...)
    FireMageHUD_FocusMagic_OnEvent(event, ...)
    if FireMageHUD_HasFocusMagicApplied() then
        return false
    end
    local now = GetTime()
    local rem = (FMHUD_State.FMExpires and FMHUD_State.FMExpires > now) and (FMHUD_State.FMExpires - now) or 0
    if rem <= 0 then
        if CheckPlayerProcActive() then
            return false
        end
        return true
    end
    return false
end

--- Disattiva lo stato OFF non appena il buff risulta applicato a un alleato.
---@param event string Nome evento
---@param ... any
---@return boolean isApplied
function FireMageHUD_FocusMagic_OFF_Untrigger(event, ...)
    return not FireMageHUD_FocusMagic_OFF_Trigger(event, ...)
end

--- Testo per lo stato OFF (%c).
---@return string
function FireMageHUD_FocusMagic_OFF_CustomText()
    return "|cFFFF2222OFF|r"
end
