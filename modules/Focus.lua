-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 04: Focus Status & Health
-- =========================================================================
-- Monitora in tempo reale il Focus del Mago:
-- - Se non esiste Focus: mostra chiaramente "NO FOCUS"
-- - Se il Focus esiste: mostra "FOCUS: Nome", HP % e HP correnti/massimi
-- - Se il Focus muore: mostra "FOCUS DEAD"
-- - Aggiornamento istantaneo al cambio focus o al variare della vita
-- =========================================================================

-- =========================================================================
-- CUSTOM TRIGGER WEAKAURAS (Event-based)
-- =========================================================================
-- Eventi: PLAYER_FOCUS_CHANGED UNIT_HEALTH UNIT_MAXHEALTH PLAYER_ENTERING_WORLD

function FireMageHUD_Focus_Trigger(event, unit)
    if event == "UNIT_HEALTH" or event == "UNIT_MAXHEALTH" then
        if unit ~= "focus" then return false end
    end
    -- Rimane sempre attivo come monitor permanente del Focus
    return true
end

function FireMageHUD_Focus_Untrigger(event, unit)
    return false
end

-- Custom Duration / Progress Function (se usato come Progress Bar):
function FireMageHUD_Focus_Duration()
    if not UnitExists("focus") then return 0, 1, true end
    local cur = UnitHealth("focus") or 0
    local max = UnitHealthMax("focus") or 1
    return cur, max, true
end

-- =========================================================================
-- TESTO PERSONALIZZATO (%c) PER IL FOCUS
-- =========================================================================
-- Inserisci nel campo "Custom Function" per il testo in WeakAuras (%c).

function FireMageHUD_Focus_CustomText()
    if not UnitExists("focus") then
        return "|cFF777777NO FOCUS|r"
    end

    local name = UnitName("focus") or "Focus"

    if UnitIsDeadOrGhost("focus") then
        return string.format("FOCUS: %s\n|cFFFF2222FOCUS DEAD|r", name)
    end

    local cur = UnitHealth("focus") or 0
    local max = UnitHealthMax("focus") or 1
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

    return string.format("FOCUS: %s\n%.1f%%  (%s / %s)", name, pct, formatNum(cur), formatNum(max))
end

