-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 03: Target Status & Health
-- =========================================================================
-- Monitora in tempo reale il target selezionato:
-- - Nome del Target
-- - Percentuale HP
-- - Valore HP attuale / massimo formattato (es. 1.2M / 1.4M o 14800 / 17300)
-- - Stato bersaglio (morto / attivo)
-- =========================================================================

-- =========================================================================
-- CUSTOM TRIGGER WEAKAURAS (Event-based)
-- =========================================================================
-- Eventi: PLAYER_TARGET_CHANGED UNIT_HEALTH UNIT_MAXHEALTH PLAYER_ENTERING_WORLD

function FireMageHUD_Target_Trigger(event, unit)
    if event == "UNIT_HEALTH" or event == "UNIT_MAXHEALTH" then
        if unit ~= "target" then return false end
    end
    -- Triggera sempre se esiste un target, oppure lascia attivo il monitor
    return UnitExists("target")
end

function FireMageHUD_Target_Untrigger(event, unit)
    return not UnitExists("target")
end

-- Custom Duration / Progress Function:
function FireMageHUD_Target_Duration()
    if not UnitExists("target") then return 0, 1, true end
    local cur = UnitHealth("target") or 0
    local max = UnitHealthMax("target") or 1
    return cur, max, true
end

-- =========================================================================
-- TESTO PERSONALIZZATO (%c) PER IL TARGET
-- =========================================================================
-- Inserisci nel campo "Custom Function" per il testo in WeakAuras (%c).

function FireMageHUD_Target_CustomText()
    if not UnitExists("target") then
        return "|cFF888888NO TARGET|r"
    end

    if UnitIsDeadOrGhost("target") then
        local name = UnitName("target") or "Target"
        return string.format("%s\n|cFFFF2222DEAD|r", name)
    end

    local name = UnitName("target") or "Target"
    local cur = UnitHealth("target") or 0
    local max = UnitHealthMax("target") or 1
    if max <= 0 then max = 1 end
    local pct = (cur / max) * 100

    -- Formattazione cifre
    local formatNum = function(v)
        if v >= 1000000 then
            return string.format("%.1fM", v / 1000000)
        elseif v >= 1000 then
            return string.format("%.1fk", v / 1000)
        else
            return string.format("%d", v)
        end
    end

    return string.format("%s\n%.1f%%  (%s / %s)", name, pct, formatNum(cur), formatNum(max))
end

