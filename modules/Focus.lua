-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 04: Focus Magic Monitor
-- =========================================================================
-- Monitora in tempo reale lo stato di "Focus Magic" per il Mago:
-- - Posizionato sull'ala destra della HUD (xOffset = +155, yOffset = 0),
--   in perfetto equilibrio simmetrico con Molten Armor (xOffset = -155).
-- - Se Focus Magic NON E' STATO MESSO A NESSUNO:
--   mostra l'icona desaturata grigia con indicazione sobria "OFF" come promemoria.
-- - Non appena Focus Magic viene APPLICATO ad un alleato (in raid, party, o target):
--   l'avviso "OFF" scompare immediatamente e rimane nascosto per tutti i 30 minuti!
-- - Riconosce automaticamente il cast via COMBAT_LOG e UNIT_SPELLCAST_SUCCEEDED,
--   quindi l'avviso OFF rimane nascosto anche se deselezioni il bersaglio o sei solo.
-- - Se l'alleato muore o il buff scade/viene rimosso: "OFF" ricompare per avvisarti.
-- - Se l'alleato esegue un critico e il Mago riceve il proc (10s, +3% crit):
--   si attiva l'icona colorata "Focus Magic - Active" con timer %p.
-- =========================================================================

local FOCUS_MAGIC_BUFF = "Focus Magic"
local FOCUS_MAGIC_SPELL_ID = 54646

-- Tabella di stato condivisa per memorizzare l'applicazione di Focus Magic
FMHUD_State = FMHUD_State or {}

-- =========================================================================
-- GESTIONE EVENTI (COMBAT LOG & SPELLCAST)
-- =========================================================================
function FireMageHUD_FocusMagic_OnEvent(event, ...)
    local now = GetTime()

    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and spell == FOCUS_MAGIC_BUFF then
            FMHUD_State.FMTarget = UnitName("target") or "Ally"
            FMHUD_State.FMExpires = now + 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        if sourceGUID == UnitGUID("player") and (spellName == FOCUS_MAGIC_BUFF or spellId == FOCUS_MAGIC_SPELL_ID) then
            if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                FMHUD_State.FMTarget = destName or "Ally"
                FMHUD_State.FMExpires = now + 1800
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

-- =========================================================================
-- CONTROLLO GLOBALE APPLICAZIONE FOCUS MAGIC
-- =========================================================================
function FireMageHUD_HasFocusMagicApplied()
    local now = GetTime()

    -- 1. Controllo timer da Combat Log / Spellcast Succeeded
    if FMHUD_State.FMExpires and FMHUD_State.FMExpires > now then
        return true
    end

    -- 2. Controllo se il giocatore ha il buff o il proc attivo
    for i = 1, 40 do
        local n = UnitBuff("player", i)
        if not n then break end
        if n == FOCUS_MAGIC_BUFF then return true end
    end

    -- 3. Controllo sul bersaglio corrente (se amico)
    if UnitExists("target") and UnitIsFriend("player", "target") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("target", i)
            if not n then break end
            if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then
                FMHUD_State.FMExpires = now + 1800
                FMHUD_State.FMTarget = UnitName("target")
                return true
            end
        end
    end

    -- 4. Controllo sul focus (se amico)
    if UnitExists("focus") and UnitIsFriend("player", "focus") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("focus", i)
            if not n then break end
            if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then
                FMHUD_State.FMExpires = now + 1800
                FMHUD_State.FMTarget = UnitName("focus")
                return true
            end
        end
    end

    -- 5. Controllo su tutti i membri del Raid
    local nr = GetNumRaidMembers()
    if nr and nr > 0 then
        for r = 1, nr do
            local u = "raid" .. r
            for i = 1, 40 do
                local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                if not n then break end
                if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMTarget = UnitName(u)
                    return true
                end
            end
        end
    else
        -- 6. Controllo sui membri del Party
        local np = GetNumPartyMembers()
        if np and np > 0 then
            for p = 1, np do
                local u = "party" .. p
                for i = 1, 40 do
                    local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                    if not n then break end
                    if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then
                        FMHUD_State.FMExpires = now + 1800
                        FMHUD_State.FMTarget = UnitName(u)
                        return true
                    end
                end
            end
        end
    end

    return false
end

-- =========================================================================
-- TRIGGER FOCUS MAGIC - OFF (Mostra icona grigia solo se NON applicato)
-- =========================================================================
function FireMageHUD_FocusMagic_OFF_Trigger(event, ...)
    FireMageHUD_FocusMagic_OnEvent(event, ...)
    return not FireMageHUD_HasFocusMagicApplied()
end

function FireMageHUD_FocusMagic_OFF_Untrigger(event, ...)
    return FireMageHUD_HasFocusMagicApplied()
end

-- =========================================================================
-- TRIGGER FOCUS MAGIC - ACTIVE (Mostra icona a colori se attivo su player)
-- =========================================================================
function FireMageHUD_FocusMagic_Active_Trigger()
    local name, _, icon, count, debuffType, duration, expirationTime = UnitBuff("player", FOCUS_MAGIC_BUFF)
    if name then
        return true, duration, expirationTime
    end
    return false
end
