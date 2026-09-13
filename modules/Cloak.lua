-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 06: Mantello / Enchant (Slot 15)
-- =========================================================================
-- Monitora l'incantamento o l'effetto speciale del mantello (Slot 15):
-- - Proc di Sartoria: "Lightweave Embroidery" (Buff 55637 / 73849 - +295 SP per 15s, 45s ICD)
-- - Incantamenti On-Use di Ingegneria (Springy Arachnoweave, paracadute, ecc.)
-- Mostra: Nome, Icona, ACTIVE (durata), COOLDOWN (CD/ICD rimanente) o READY.
-- =========================================================================

local Cloak_ProcTimer = { lastProc = 0 }

function FireMageHUD_Cloak_Trigger(event, unit)
    return true -- Monitor permanente
end

function FireMageHUD_Cloak_CustomText()
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Cloak) or {}
    local buffID = cfg.BuffID or 55637       -- Default: Lightweave Embroidery
    local icd = cfg.InternalCD or 45         -- ICD stimato di 45 secondi
    local isOnUse = cfg.IsOnUse or false
    
    local itemID = GetInventoryItemID("player", 15)
    local itemName, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    itemName = itemName or "Mantello"

    -- 1. Controllo Buff Proc attivo
    if buffID and buffID > 0 then
        local buffName = GetSpellInfo(buffID)
        for i = 1, 40 do
            local name, _, icon, count, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if (buffName and name == buffName) or name == buffName then
                local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
                Cloak_ProcTimer.lastProc = GetTime()
                return string.format("%s\n|cFF00FF00ACTIVE %.1fs|r", itemName, rem)
            end
        end
    end

    -- 2. Controllo Cooldown On-Use da API (Ingegneria)
    local start, duration = GetInventoryItemCooldown("player", 15)
    if start and duration and start > 0 and duration > 1.5 then
        local rem = (start + duration) - GetTime()
        if rem > 0 then
            return string.format("%s\n|cFFFF9900CD %.1fs|r", itemName, rem)
        end
    end

    -- 3. Controllo ICD Software per Proc Passivo (Sartoria)
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

function FireMageHUD_Cloak_CustomIcon()
    local itemID = GetInventoryItemID("player", 15)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_Cape_19"
end

