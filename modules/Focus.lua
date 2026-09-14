--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 04: Focus Magic Monitor
--- =========================================================================
--- Monitora l'applicazione del buff Focus Magic (x = -182, y = -54):
--- - Durata > 5 minuti: Completamente NASCOSTA per pulizia visiva in combattimento.
--- - Durata <= 5 minuti: COMPARE automaticamente con countdown e swipe per il rinnovo.
--- - NON applicato / Scaduto / Bersaglio morto: Icona grigia con avviso rosso "OFF".
--- Riconosce l'applicazione tramite COMBAT_LOG, UNIT_SPELLCAST_SUCCEEDED e
--- scansione attiva delle unità amiche (target, focus, raid1..40, party1..4).
--- =========================================================================

local FOCUS_MAGIC_BUFF = "Focus Magic"
local FOCUS_MAGIC_SPELL_ID = 54646

--- Tabella di stato condivisa per memorizzare l'applicazione e la scadenza
FMHUD_State = FMHUD_State or {}

--- Gestisce gli eventi di Combat Log e Spellcast Succeeded per intercettare l'assegnazione.
---@param event string Nome evento
---@param ... any Argomenti dell'evento
function FireMageHUD_FocusMagic_OnEvent(event, ...)
    local now = GetTime()

    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and spell == FOCUS_MAGIC_BUFF then
            FMHUD_State.FMTarget = UnitName("target") or "Ally"
            FMHUD_State.FMExpires = now + 1800
            FMHUD_State.FMDur = 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        if sourceGUID == UnitGUID("player") and (spellName == FOCUS_MAGIC_BUFF or spellId == FOCUS_MAGIC_SPELL_ID) then
            if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                FMHUD_State.FMTarget = destName or "Ally"
                FMHUD_State.FMExpires = now + 1800
                FMHUD_State.FMDur = 1800
            elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                FMHUD_State.FMExpires = 0
                FMHUD_State.FMTarget = nil
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
        local n, _, _, _, _, dur, exp, c = UnitBuff(unit, i)
        if not n then break end
        if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then
            local now = GetTime()
            FMHUD_State.FMExpires = (exp and exp > 0) and exp or (now + 1800)
            FMHUD_State.FMDur = dur or 1800
            FMHUD_State.FMTarget = UnitName(unit)
            return true
        end
    end
    return false
end

--- Scansiona l'intero gruppo/raid, il target e il focus alla ricerca del buff applicato.
---@return boolean isApplied
function FireMageHUD_HasFocusMagicApplied()
    local now = GetTime()

    -- 1. Controllo cache da eventi recenti
    if FMHUD_State.FMExpires and FMHUD_State.FMExpires > now then
        return true
    end

    -- 2. Target e Focus amici
    if CheckUnitFocusMagic("target") or CheckUnitFocusMagic("focus") then
        return true
    end

    -- 3. Membri del Raid o Party
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
    local now = GetTime()
    local rem = (FMHUD_State.FMExpires and FMHUD_State.FMExpires > now) and (FMHUD_State.FMExpires - now) or 0
    return rem <= 0
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
