-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 05: Trinket 1 e Trinket 2
-- =========================================================================
-- Gestisce in modo completamente separato ed indipendente:
-- - Trinket 1 (Slot 13)
-- - Trinket 2 (Slot 14)
-- Supporta sia Trinket "On-Use" (attivi) sia Trinket "Equip:" (proc passivi con ICD).
-- Mostra: Nome, Icona, ACTIVE (durata), COOLDOWN (CD rimanente) o READY.
-- =========================================================================

-- Tabella locale per la registrazione dei proc passivi
local Trinket_ProcTimers = {
    [13] = { lastProc = 0 },
    [14] = { lastProc = 0 },
}

-- =========================================================================
-- FUNZIONE GENERICA DI MONITORAGGIO TRINKET
-- =========================================================================
function FireMageHUD_GetTrinketStatus(slot, targetBuffID, targetICD, isOnUse)
    local itemID = GetInventoryItemID("player", slot)
    local itemName, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    itemName = itemName or (slot == 13 and "Trinket 1" or "Trinket 2")
    itemTexture = itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"

    -- 1. Controllo se il Buff del Proc passivo è attivo sul player
    if targetBuffID and targetBuffID > 0 then
        local targetBuffName = GetSpellInfo(targetBuffID)
        for i = 1, 40 do
            local name, _, icon, count, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if (targetBuffName and name == targetBuffName) or name == targetBuffName then
                local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
                Trinket_ProcTimers[slot].lastProc = GetTime()
                local txt = string.format("%s\n|cFF00FF00ACTIVE %.1fs|r", itemName, rem)
                return "ACTIVE", txt, icon or itemTexture, rem
            end
        end
    end

    -- 2. Controllo Cooldown On-Use standard (API nativa)
    local start, duration = GetInventoryItemCooldown("player", slot)
    if start and duration and start > 0 and duration > 1.5 then
        local rem = (start + duration) - GetTime()
        if rem > 0 then
            local txt = string.format("%s\n|cFFFF9900CD %.1fs|r", itemName, rem)
            return "COOLDOWN", txt, itemTexture, rem
        end
    end

    -- 3. Controllo ICD Software per Proc Passivi
    if targetICD and targetICD > 0 and not isOnUse and Trinket_ProcTimers[slot].lastProc > 0 then
        local elapsed = GetTime() - Trinket_ProcTimers[slot].lastProc
        if elapsed < targetICD then
            local remICD = targetICD - elapsed
            local txt = string.format("%s\n|cFFFF9900ICD %.1fs|r", itemName, remICD)
            return "COOLDOWN", txt, itemTexture, remICD
        end
    end

    -- 4. Oggetto pronto all'uso / pronto al proc
    local txt = string.format("%s\n|cFF00FF00READY|r", itemName)
    return "READY", txt, itemTexture, 0
end

-- =========================================================================
-- TRINKET 1 (SLOT 13) — CODICE PER WEAKAURAS
-- =========================================================================
-- Eventi: PLAYER_ENTERING_WORLD PLAYER_EQUIPMENT_CHANGED UNIT_AURA SPELL_UPDATE_COOLDOWN

function FireMageHUD_Trinket1_Trigger(event, unit)
    return true -- Rimane sempre visibile
end

function FireMageHUD_Trinket1_CustomText()
    -- CONFIGURAZIONE TRINKET 1:
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Trinket1) or {}
    local buffID = cfg.BuffID or 0       -- Sostituisci con il Buff ID del proc
    local icd = cfg.InternalCD or 45     -- Sostituisci con l'ICD in secondi
    local isOnUse = cfg.IsOnUse or false -- true se On-Use, false se Proc
    
    local _, text = FireMageHUD_GetTrinketStatus(13, buffID, icd, isOnUse)
    return text
end

function FireMageHUD_Trinket1_CustomIcon()
    local itemID = GetInventoryItemID("player", 13)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"
end

-- =========================================================================
-- TRINKET 2 (SLOT 14) — CODICE PER WEAKAURAS
-- =========================================================================
-- Eventi: PLAYER_ENTERING_WORLD PLAYER_EQUIPMENT_CHANGED UNIT_AURA SPELL_UPDATE_COOLDOWN

function FireMageHUD_Trinket2_Trigger(event, unit)
    return true -- Rimane sempre visibile
end

function FireMageHUD_Trinket2_CustomText()
    -- CONFIGURAZIONE TRINKET 2:
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Trinket2) or {}
    local buffID = cfg.BuffID or 0
    local icd = cfg.InternalCD or 45
    local isOnUse = cfg.IsOnUse or false
    
    local _, text = FireMageHUD_GetTrinketStatus(14, buffID, icd, isOnUse)
    return text
end

function FireMageHUD_Trinket2_CustomIcon()
    local itemID = GetInventoryItemID("player", 14)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"
end

