-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 01: Proc & Rotazione Fire Mage
-- =========================================================================
-- Include i trigger e i testi personalizzati per:
-- 1. Hot Streak (Buff Player 48108)
-- 2. Living Bomb (Debuff Target 55360 - Active & Missing)
-- 3. Ignite (Debuff Target 12654 - Stacks & Duration)
-- 4. Combustion (Spell Cooldown 11129 & Active Buff 28682)
-- 5. Molten Fury (Talento passivo <= 35% HP Target)
-- =========================================================================

-- =========================================================================
-- 1. HOT STREAK (Buff Player)
-- =========================================================================
-- In WeakAuras puoi usare il Trigger Nativo:
-- Type: Aura | Unit: Player | Aura Type: Buff | Spell Name or ID: 48108
-- Display Text: %p (timer) e %s (stacks)
-- Animations > Start: Preset "Zoom" o "Flash"

-- Custom Trigger Event Alternativo:
-- Eventi: UNIT_AURA PLAYER_ENTERING_WORLD
function FireMageHUD_HotStreak_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wantedName = GetSpellInfo(48108) or "Hot Streak"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Hot Streak" then
            return true
        end
    end
    return false
end

-- =========================================================================
-- 2. LIVING BOMB (Debuff Target)
-- =========================================================================
-- In WeakAuras:
-- Type: Aura | Unit: Target | Aura Type: Debuff | Own Only: Spunta | Spell ID: 55360

-- Custom Trigger per indicatore "LIVING BOMB MISSING" (opzionale):
-- Mostra quando hai un target vivo in combattimento ma manca Living Bomb
-- Eventi: UNIT_AURA PLAYER_TARGET_CHANGED PLAYER_REGEN_DISABLED PLAYER_REGEN_ENABLED
function FireMageHUD_LivingBombMissing_Trigger(event, unit)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") or not UnitCanAttack("player", "target") then
        return false
    end
    local wantedName = GetSpellInfo(55360) or "Living Bomb"
    for i = 1, 40 do
        local name, _, _, _, _, _, _, caster = UnitDebuff("target", i)
        if not name then break end
        if (name == wantedName or name == "Living Bomb") and caster == "player" then
            return false -- Debuff presente
        end
    end
    return true -- Debuff mancante sul target valido
end

function FireMageHUD_LivingBombMissing_CustomText()
    return "LIVING BOMB\n|cFFFF2222MISSING|r"
end

-- =========================================================================
-- 3. IGNITE (Debuff Target)
-- =========================================================================
-- In WeakAuras:
-- Type: Aura | Unit: Target | Aura Type: Debuff | Spell ID: 12654
-- Display Text: %p (durata rimanente) | %s (stacks se esposti)

-- =========================================================================
-- 4. COMBUSTION (Cooldown & Active Buff)
-- =========================================================================
-- Gestione completa a 3 stati (READY, ACTIVE, COOLDOWN):
-- Eventi: SPELL_UPDATE_COOLDOWN UNIT_AURA PLAYER_ENTERING_WORLD

function FireMageHUD_Combustion_Trigger(event, unit)
    return true -- Il testo personalizzato gestisce i 3 stati
end

function FireMageHUD_Combustion_CustomText()
    -- 1. Controllo se il Buff di Combustion è attivo sul player
    local buffName = GetSpellInfo(28682) or "Combustion"
    for i = 1, 40 do
        local name, _, _, count, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == buffName or name == "Combustion" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            return string.format("COMBUSTION\n|cFF00FF00ACTIVE (x%d)|r %.1fs", count or 1, rem)
        end
    end

    -- 2. Controllo Cooldown della magia (Spell ID: 11129)
    local start, duration = GetSpellCooldown(11129)
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Combustion")
    end

    if start and duration and start > 0 and duration > 1.5 then
        local remCD = (start + duration) - GetTime()
        if remCD > 0 then
            return string.format("COMBUSTION\n|cFFFF9900CD %.1fs|r", remCD)
        end
    end

    -- 3. Pronto all'uso
    return "COMBUSTION\n|cFF00FF00READY|r"
end

-- =========================================================================
-- 5. MOLTEN FURY (Talento passivo <= 35% HP Target)
-- =========================================================================
-- Rileva quando il target scende sotto il 35% di vita per massimizzare il DPS
-- Eventi: PLAYER_TARGET_CHANGED UNIT_HEALTH UNIT_MAXHEALTH PLAYER_ENTERING_WORLD

function FireMageHUD_MoltenFury_Trigger(event, unit)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") or not UnitCanAttack("player", "target") then
        return false
    end
    local max = UnitHealthMax("target") or 1
    if max <= 0 then return false end
    local cur = UnitHealth("target") or 0
    local pct = (cur / max) * 100
    
    return pct <= 35.0
end

function FireMageHUD_MoltenFury_Untrigger(event, unit)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") then
        return true
    end
    local max = UnitHealthMax("target") or 1
    if max <= 0 then return true end
    local cur = UnitHealth("target") or 0
    return (cur / max) * 100 > 35.0
end

function FireMageHUD_MoltenFury_CustomText()
    return "|cFFFF5500MOLTEN FURY\nEXECUTE PHASE|r"
end

