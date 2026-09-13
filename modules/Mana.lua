-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 07: Mana Bar
-- =========================================================================
-- Questo file contiene il codice per la Progress Bar del Mana in WeakAuras.
-- È progettato per essere autonomo e modificabile direttamente in /wa.
-- =========================================================================

-- =========================================================================
-- OPZIONE A: Trigger Nativo WeakAuras (Consigliato per la barra grafica)
-- =========================================================================
-- Tipo: Status
-- Status: Power (o Mana)
-- Unit: Player
-- Power Type: Mana

-- =========================================================================
-- OPZIONE B: Custom Trigger (Event-based per massima compatibilità 3.3.5a)
-- =========================================================================
-- Eventi: UNIT_POWER_UPDATE UNIT_MAXPOWER UNIT_MANA UNIT_MAXMANA PLAYER_ENTERING_WORLD

-- Custom Trigger Function:
function FireMageHUD_Mana_Trigger(event, unit)
    if event == "UNIT_POWER_UPDATE" or event == "UNIT_MANA" or event == "UNIT_MAXMANA" or event == "UNIT_MAXPOWER" then
        if unit ~= "player" then return false end
    end
    return true
end

-- Custom Duration Function:
function FireMageHUD_Mana_Duration()
    local cur = UnitPower("player", 0) or UnitMana("player") or 0
    local max = UnitPowerMax("player", 0) or UnitManaMax("player") or 1
    return cur, max, true
end

-- =========================================================================
-- TESTO PERSONALIZZATO (%c) PER WEAKAURAS
-- =========================================================================
-- Inserisci questo codice nel campo "Custom Function" del testo della barra (%c).
-- Mostra: Solo la Percentuale con due decimali (es. "85.24%")

function FireMageHUD_Mana_CustomText()
    local cur = UnitPower("player", 0) or UnitMana("player") or 0
    local max = UnitPowerMax("player", 0) or UnitManaMax("player") or 1
    if max <= 0 then max = 1 end
    local pct = (cur / max) * 100

    return string.format("%.2f%%", pct)
end

-- =========================================================================
-- CONDIZIONI DI COLORE DINAMICHE (Configurabili in /wa > Tab 'Conditions')
-- =========================================================================
-- Condition 1: If Power(%) <= 15  --> Color = Rosso Critico (#FF1A1A) + Animazione Glow/Flash
-- Condition 2: If Power(%) <= 30  --> Color = Arancione (#FF7300)
-- Condition 3: If Power(%) <= 50  --> Color = Giallo (#FFD700)
-- Condition 4: If Power(%) > 50   --> Color = Blu Mana (#0088FF)

