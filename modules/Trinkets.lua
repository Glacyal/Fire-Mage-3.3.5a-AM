-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 05: Trinket 1 e Trinket 2
-- =========================================================================
-- Gestisce in modo completamente separato ed indipendente:
-- - Trinket 1 (Slot 13)
-- - Trinket 2 (Slot 14)
-- Supporta sia Trinket "On-Use" (attivi) sia Trinket "Equip:" (proc passivi con ICD).
-- Riconosce automaticamente tutti i principali trinket da caster di WotLK 3.3.5a!
-- Mostra: Nome, Icona, ACTIVE (durata), COOLDOWN (CD rimanente) o READY.
-- =========================================================================

-- Tabella di riconoscimento automatico dei proc dei trinket WotLK 3.3.5a
local FMHUD_TrinketDB = {
    [50348] = { buff = "Celestial Infusion" }, -- DFO Normal
    [50345] = { buff = "Celestial Infusion" }, -- DFO Heroic
    [50360] = { buff = "Siphon of Aethas" }, -- Phylactery Normal
    [50365] = { buff = "Siphon of Aethas", altBuff = "Aethas' Siphon" }, -- Phylactery Heroic
    [54572] = { buff = "Shared Twilight" }, -- Charred Twilight Scale Normal
    [54588] = { buff = "Shared Twilight" }, -- Charred Twilight Scale Heroic
    [45518] = { buff = "Elusive Power" }, -- Flare of the Heavens
    [47271] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" }, -- Reign of the Dead
    [47477] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
    [47182] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" }, -- Reign of the Unliving
    [47316] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
    [40682] = { buff = "Now is the time!", altBuff = "Now is the Time!", spellId = 60064, icd = 45, dur = 10 }, -- Sundial of the Exiled
    [40255] = { buff = "Dying Curse", altBuff = "Curse of the Eye", spellId = 60494, icd = 45, dur = 10 }, -- The Dying Curse
    [47213] = { buff = "Deadly Precision" }, -- Abyssal Rune
    [37660] = { buff = "Forged Ember" }, -- Forge Ember
    [45308] = { buff = "Blessing of the Broodmother" },
    [40432] = { buff = "Dragon Soul" }, -- Illustration of the Dragon Soul
    [37264] = { buff = "Sudden Velocity" }, -- Embrace of the Spider
    [44253] = { buff = "Greatness" }, -- DMC Greatness
    [44255] = { buff = "Greatness" },
    [42987] = { buff = "Greatness" },
    [44254] = { buff = "Greatness" },
    [50340] = { buff = "Gathering Tracker" }, -- Muradin's Spyglass
    [50353] = { buff = "Gathering Tracker" },
    [45466] = { buff = "Velocity" }, -- Scale of Fates
    [48724] = { buff = "Chilled Heart" }, -- Shard of the Crystal Heart
    [48722] = { buff = "Volatile Power" }, -- Talisman of Resurgence
    [50259] = { buff = "Deadly Precision" }, -- Nevermelting Ice Crystal
    [37873] = { buff = "Soul Power" }, -- Mark of the War Prisoner
    [50339] = { buff = "Pure Energy" }, -- Sliver of Pure Ice Normal
    [50346] = { buff = "Pure Energy" }, -- Sliver of Pure Ice Heroic
    [47215] = { buff = "Revitalized" }, -- Tears of the Vanquished
    [45490] = { buff = "Pandora's Plea" },
    [40685] = { buff = "Living Flame" },
    [50357] = { buff = "Maghia's Misguided Quill" },
}

local FMHUD_CasterProcs = {
    ["Celestial Infusion"] = true,
    ["Siphon of Aethas"] = true,
    ["Aethas' Siphon"] = true,
    ["Shared Twilight"] = true,
    ["Twilight Flame"] = true,
    ["Elusive Power"] = true,
    ["Motes of Flame"] = true,
    ["Pillar of Flame"] = true,
    ["Now is the Time!"] = true,
    ["Now is the time!"] = true,
    ["Curse of the Eye"] = true,
    ["Dying Curse"] = true,
    ["Deadly Precision"] = true,
    ["Forged Ember"] = true,
    ["Blessing of the Broodmother"] = true,
    ["Dragon Soul"] = true,
    ["Sudden Velocity"] = true,
    ["Greatness"] = true,
    ["Gathering Tracker"] = true,
    ["Velocity"] = true,
    ["Chilled Heart"] = true,
    ["Volatile Power"] = true,
    ["Soul Power"] = true,
    ["Pure Energy"] = true,
    ["Revitalized"] = true,
    ["Pandora's Plea"] = true,
    ["Living Flame"] = true,
    ["Maghia's Misguided Quill"] = true,
    ["Peerless Destruction"] = true,
}

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

    -- 1. Controllo se il Buff del Proc passivo specifico o da DB è attivo sul player
    local buffName = targetBuffID and targetBuffID > 0 and GetSpellInfo(targetBuffID)
    local entry = itemID and FMHUD_TrinketDB[itemID]
    local dbBuff = entry and entry.buff
    local dbAltBuff = entry and entry.altBuff

    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        local isMatch = false
        if entry then
            if (entry.spellId and spellId == entry.spellId)
               or (entry.altSpellId and spellId == entry.altSpellId)
               or (entry.buff and string.lower(name) == string.lower(entry.buff))
               or (entry.altBuff and string.lower(name) == string.lower(entry.altBuff)) then
                isMatch = true
            end
        elseif buffName and (string.lower(name) == string.lower(buffName)) then
            isMatch = true
        end

        if isMatch then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            Trinket_ProcTimers[slot].lastProc = GetTime()
            local txt = string.format("%s\n|cFF00FF00ACTIVE %.1fs|r", itemName, rem)
            return "ACTIVE", txt, icon or itemTexture, rem
        end
    end

    -- Fallback: controllo se un buff da caster è attivo per questo slot
    local otherSlot = (slot == 13) and 14 or 13
    local otherID = GetInventoryItemID("player", otherSlot)
    local otherEntry = otherID and FMHUD_TrinketDB[otherID]
    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            Trinket_ProcTimers[slot].lastProc = GetTime()
            local txt = string.format("%s\n|cFF00FF00ACTIVE %.1fs|r", itemName, rem)
            return "ACTIVE", txt, icon or itemTexture, rem
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
    local icd = targetICD or 45
    if icd and icd > 0 and not isOnUse and Trinket_ProcTimers[slot].lastProc > 0 then
        local elapsed = GetTime() - Trinket_ProcTimers[slot].lastProc
        if elapsed < icd then
            local remICD = icd - elapsed
            local txt = string.format("%s\n|cFFFF9900ICD %.1fs|r", itemName, remICD)
            return "COOLDOWN", txt, itemTexture, remICD
        end
    end

    -- 4. Oggetto pronto all'uso / pronto al proc
    local txt = string.format("%s\n|cFF00FF00READY|r", itemName)
    return "READY", txt, itemTexture, 0
end

-- =========================================================================
-- TRINKET 1 (SLOT 13) — CODICE PER WEAKAURAS / ADDON
-- =========================================================================
function FireMageHUD_Trinket1_Trigger(event, unit)
    return true
end

function FireMageHUD_Trinket1_CustomText()
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Trinket1) or {}
    local buffID = cfg.BuffID or 0
    local icd = cfg.InternalCD or 45
    local isOnUse = cfg.IsOnUse or false
    local _, text = FireMageHUD_GetTrinketStatus(13, buffID, icd, isOnUse)
    return text
end

function FireMageHUD_Trinket1_CustomIcon()
    local itemID = GetInventoryItemID("player", 13)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"
end

-- =========================================================================
-- TRINKET 2 (SLOT 14) — CODICE PER WEAKAURAS / ADDON
-- =========================================================================
function FireMageHUD_Trinket2_Trigger(event, unit)
    return true
end

function FireMageHUD_Trinket2_CustomText()
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
