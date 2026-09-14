--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 10: Avvisi a Schermo (Alerts)
--- =========================================================================
--- Gestisce avvisi visivi ad alto impatto posizionati a yOffset = +105:
--- 1. HOT STREAK! / PYROBLAST READY! (Avviso proc immediato al centro dello schermo).
--- 2. WARNING: NO MOLTEN ARMOR! (Avviso critico solo se in combattimento senza armatura).
--- =========================================================================

--- Rileva la presenza del proc Hot Streak per l'attivazione dell'alert a schermo.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isHotStreakActive
function FireMageHUD_Alert_HotStreak_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Alerts and FireMageHUD_Config.Alerts.HotStreak) or {}
    if cfg.Enabled == false then return false end

    local wanted = GetSpellInfo(48108) or "Hot Streak"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == "Hot Streak" then
            return true
        end
    end
    return false
end

--- Disattiva l'alert all'esaurimento o al consumo di Hot Streak (lancio Pyroblast).
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isHotStreakInactive
function FireMageHUD_Alert_HotStreak_Untrigger(event, unit)
    return not FireMageHUD_Alert_HotStreak_Trigger(event, unit)
end

--- Testo grande visualizzato a schermo per Hot Streak (%c).
---@return string
function FireMageHUD_Alert_HotStreak_CustomText()
    return "|cFFFF5500HOT STREAK!|r\n|cFFFFFF00PYROBLAST READY!|r"
end

--- Rileva se il giocatore è in combattimento senza Molten Armor attiva.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isCombatWithoutArmor
function FireMageHUD_Alert_MoltenArmorCombat_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    if not UnitAffectingCombat("player") then return false end

    local wanted = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == "Molten Armor" then
            return false
        end
    end
    return true
end

--- Disattiva l'avviso se il giocatore esce dal combattimento o applica Molten Armor.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isSafe
function FireMageHUD_Alert_MoltenArmorCombat_Untrigger(event, unit)
    return not FireMageHUD_Alert_MoltenArmorCombat_Trigger(event, unit)
end

--- Testo dell'avviso critico in combattimento (%c).
---@return string
function FireMageHUD_Alert_MoltenArmorCombat_CustomText()
    return "|cFFFF0000WARNING: NO MOLTEN ARMOR!|r"
end
