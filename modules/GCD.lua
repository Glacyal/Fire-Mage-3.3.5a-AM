-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 09: Global Cooldown (GCD)
-- =========================================================================
-- Monitora il Global Cooldown (GCD) separatamente dal tempo di cast.
-- Utilizza la spell di riferimento standard di WotLK (ID 61304) o fallback
-- su abilità istantanee (Fire Blast / Frost Nova).
-- =========================================================================

-- =========================================================================
-- CUSTOM TRIGGER WEAKAURAS (Event-based Progress Bar)
-- =========================================================================
-- Eventi: SPELL_UPDATE_COOLDOWN PLAYER_ENTERING_WORLD

function FireMageHUD_GCD_Trigger(event, unit)
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        -- Fallback su Fire Blast (Spell ID 42873) o Frost Nova (Spell ID 122)
        start, duration = GetSpellCooldown(42873)
    end

    if start and duration and start > 0 and duration > 0 and duration <= 1.5 then
        return true
    end
    return false
end

function FireMageHUD_GCD_Untrigger(event, unit)
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    return (not start) or (duration == 0) or (duration > 1.5)
end

-- Custom Duration Function:
function FireMageHUD_GCD_Duration()
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    if start and duration and start > 0 and duration > 0 and duration <= 1.5 then
        return duration, start + duration, true
    end
    return 0, 0, true
end

-- Custom Text (%c opzionale per mostrare i decimi di GCD rimanente):
function FireMageHUD_GCD_CustomText()
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    if start and duration and start > 0 and duration > 0 and duration <= 1.5 then
        local rem = math.max(0, (start + duration) - GetTime())
        return string.format("%.1fs", rem)
    end
    return ""
end

