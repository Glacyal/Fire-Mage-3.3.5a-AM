-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 10: Alert e Notifiche Visive
-- =========================================================================
-- Gestisce avvisi visivi e sonori ad alto impatto per i momenti chiave del combattimento:
-- 1. HOT STREAK! / PYROBLAST READY! (Proc attivo)
-- 2. MOLTEN ARMOR ASSENTE IN COMBATTIMENTO (Avviso critico)
-- =========================================================================

-- =========================================================================
-- 1. ALERT: HOT STREAK / PYROBLAST READY
-- =========================================================================
-- Tipo: Aura Text / Icon
-- Posizione consigliata: Centro schermo, subito sopra i proc
-- Eventi: UNIT_AURA PLAYER_ENTERING_WORLD

function FireMageHUD_Alert_HotStreak_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Alerts and FireMageHUD_Config.Alerts.HotStreak) or {}
    if cfg.Enabled == false then return false end

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

function FireMageHUD_Alert_HotStreak_Untrigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wantedName = GetSpellInfo(48108) or "Hot Streak"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Hot Streak" then
            return false
        end
    end
    return true
end

function FireMageHUD_Alert_HotStreak_CustomText()
    return "|cFFFF5500HOT STREAK!|r\n|cFFFFFF00PYROBLAST READY!|r"
end


-- =========================================================================
-- 2. ALERT: MOLTEN ARMOR MISSING IN COMBAT
-- =========================================================================
-- Compare solo se sei in combattimento e ti dimentichi di attivare Molten Armor
-- Eventi: PLAYER_REGEN_DISABLED PLAYER_REGEN_ENABLED UNIT_AURA PLAYER_ENTERING_WORLD

function FireMageHUD_Alert_MoltenArmorCombat_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    
    -- Controlla se siamo in combattimento
    if not UnitAffectingCombat("player") then
        return false
    end

    -- Controlla se Molten Armor è attiva
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return false -- È attiva
        end
    end

    return true -- IN COMBATTIMENTO SENZA MOLTEN ARMOR!
end

function FireMageHUD_Alert_MoltenArmorCombat_Untrigger(event, unit)
    if not UnitAffectingCombat("player") then return true end
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return true
        end
    end
    return false
end

function FireMageHUD_Alert_MoltenArmorCombat_CustomText()
    return "|cFFFF0000WARNING: NO MOLTEN ARMOR!|r"
end

