--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 06: Mantello / Ricamo (Slot 15)
--- =========================================================================
--- Monitora l'incantamento o l'effetto speciale del mantello (x = -22, y = -54):
--- - Ricamo di Sartoria: Lightweave Embroidery (+295 SP per 15s, 45s ICD).
--- - Varianti: Darkglow (Mana), Swordguard (AP), paracadute di Ingegneria.
--- - Mostra durata attiva con timer verde, cooldown ICD/nativo con timer arancione, o READY.
--- =========================================================================

local Cloak_ProcTimer = { lastProc = 0 }

local CLOAK_BUFFS = {
    ["Lightweave"]           = true,
    ["Darkglow"]             = true,
    ["Swordguard"]           = true,
    ["Parachute"]            = true,
    ["Flexweave"]            = true,
    ["Springy Arachnoweave"] = true,
}

--- Genera il testo descrittivo dello stato del mantello (%c).
---@return string formattedStatus
function FireMageHUD_Cloak_CustomText()
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Cloak) or {}
    local buffID = cfg.BuffID
    local icd = cfg.InternalCD or 45
    local isOnUse = cfg.IsOnUse or false

    local itemID = GetInventoryItemID("player", 15)
    local itemName, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    itemName = itemName or "Mantello"

    -- 1. Controllo buff attivo
    local customBuffName = buffID and buffID > 0 and GetSpellInfo(buffID)
    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if (customBuffName and name == customBuffName)
           or name == "Lightweave"
           or spellId == 55637
           or spellId == 73849
           or CLOAK_BUFFS[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            Cloak_ProcTimer.lastProc = GetTime()
            return string.format("%s\n|cFF00FF00ACTIVE %.1fs|r", itemName, rem)
        end
    end

    -- 2. Cooldown On-Use nativo (Ingegneria)
    local start, duration = GetInventoryItemCooldown("player", 15)
    if start and duration and start > 0 and duration > 1.5 then
        local rem = (start + duration) - GetTime()
        if rem > 0 then
            return string.format("%s\n|cFFFF9900CD %.1fs|r", itemName, rem)
        end
    end

    -- 3. ICD stimato per proc passivi di Sartoria
    if icd and icd > 0 and not isOnUse and Cloak_ProcTimer.lastProc > 0 then
        local elapsed = GetTime() - Cloak_ProcTimer.lastProc
        if elapsed < icd then
            local remICD = icd - elapsed
            return string.format("%s\n|cFFFF9900ICD %.1fs|r", itemName, remICD)
        end
    end

    -- 4. Oggetto pronto
    return string.format("%s\n|cFF00FF00READY|r", itemName)
end

--- Texture dinamica dell'icona del mantello equipaggiato.
---@return string iconPath
function FireMageHUD_Cloak_CustomIcon()
    local itemID = GetInventoryItemID("player", 15)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_Cape_19"
end
