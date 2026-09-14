--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 05: Trinket 1 (Slot 13) e Trinket 2 (Slot 14)
--- =========================================================================
--- Gestisce in modo completamente separato ed indipendente:
--- - Trinket 1 (Slot 13, x = -110, y = -54)
--- - Trinket 2 (Slot 14, x =  -66, y = -54)
--- Supporta sia oggetti "On-Use" (attivi) sia proc passivi "Equipaggia:" con
--- tracciamento software dell'Internal Cooldown (ICD).
--- Riconosce automaticamente tutti i principali monili da caster di WotLK 3.3.5a.
--- Stati operativi: ACTIVE (durata proc), COOLDOWN (CD nativo o ICD), READY.
--- =========================================================================

--- Database dei monili da caster di WotLK con mapping proc, ICD e durate
local FMHUD_TrinketDB = {
    -- Dislodged Foreign Object (DFO)
    [50348] = { buff = "Celestial Infusion", icd = 45, dur = 20 },
    [50345] = { buff = "Celestial Infusion", icd = 45, dur = 20 },
    -- Phylactery of the Nameless Lich
    [50360] = { buff = "Siphon of Aethas", altBuff = "Aethas' Siphon", icd = 90, dur = 20 },
    [50365] = { buff = "Siphon of Aethas", altBuff = "Aethas' Siphon", icd = 90, dur = 20 },
    -- Charred Twilight Scale (CTS)
    [54572] = { buff = "Shared Twilight", altBuff = "Twilight Flame", icd = 45, dur = 15 },
    [54588] = { buff = "Shared Twilight", altBuff = "Twilight Flame", icd = 45, dur = 15 },
    -- Flare of the Heavens
    [45518] = { buff = "Elusive Power", icd = 45, dur = 10 },
    -- Reign of the Dead / Unliving
    [47271] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
    [47477] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
    [47182] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
    [47316] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
    -- Sundial of the Exiled
    [40682] = { buff = "Now is the time!", altBuff = "Now is the Time!", spellId = 60064, icd = 45, dur = 10 },
    -- The Dying Curse
    [40255] = { buff = "Dying Curse", altBuff = "Curse of the Eye", spellId = 60494, icd = 45, dur = 10 },
    -- Abyssal Rune
    [47213] = { buff = "Deadly Precision", icd = 45, dur = 10 },
    -- Forge Ember
    [37660] = { buff = "Forged Ember", icd = 45, dur = 10 },
    -- Eye of the Broodmother
    [45308] = { buff = "Blessing of the Broodmother", icd = 0, dur = 10 },
    -- Illustration of the Dragon Soul
    [40432] = { buff = "Dragon Soul", icd = 0, dur = 10 },
    -- Embrace of the Spider
    [37264] = { buff = "Sudden Velocity", icd = 45, dur = 10 },
    [39229] = { buff = "Sudden Velocity", icd = 45, dur = 10 },
    -- Darkmoon Card: Greatness (tutte le varianti)
    [44253] = { buff = "Greatness", icd = 45, dur = 15 },
    [44255] = { buff = "Greatness", icd = 45, dur = 15 },
    [42987] = { buff = "Greatness", icd = 45, dur = 15 },
    [44254] = { buff = "Greatness", icd = 45, dur = 15 },
    -- Muradin's Spyglass
    [50340] = { buff = "Gathering Tracker", icd = 0, dur = 10 },
    [50353] = { buff = "Gathering Tracker", icd = 0, dur = 10 },
    -- Scale of Fates (On-Use)
    [45466] = { buff = "Velocity", icd = 120, dur = 20, onUse = true },
    -- Shard of the Crystal Heart (On-Use)
    [48724] = { buff = "Chilled Heart", icd = 120, dur = 20, onUse = true },
    -- Talisman of Resurgence (On-Use)
    [48722] = { buff = "Volatile Power", icd = 120, dur = 20, onUse = true },
    -- Nevermelting Ice Crystal (On-Use)
    [50259] = { buff = "Deadly Precision", icd = 180, dur = 20, onUse = true },
    -- Mark of the War Prisoner (On-Use)
    [37873] = { buff = "Soul Power", icd = 120, dur = 20, onUse = true },
    -- Sliver of Pure Ice (On-Use)
    [50339] = { buff = "Pure Energy", icd = 120, dur = 0, onUse = true },
    [50346] = { buff = "Pure Energy", icd = 120, dur = 0, onUse = true },
    -- Tears of the Vanquished
    [47215] = { buff = "Revitalized", icd = 45, dur = 0 },
    -- Pandora's Plea
    [45490] = { buff = "Pandora's Plea", icd = 45, dur = 10 },
    -- Living Flame (On-Use)
    [40685] = { buff = "Living Flame", icd = 120, dur = 20, onUse = true },
    -- Maghia's Misguided Quill (On-Use)
    [50357] = { buff = "Maghia's Misguided Quill", icd = 120, dur = 20, onUse = true },
}

--- Lookup rapido per buff di proc generici da caster
local FMHUD_CasterProcs = {
    ["Celestial Infusion"]          = true,
    ["Siphon of Aethas"]            = true,
    ["Aethas' Siphon"]              = true,
    ["Shared Twilight"]             = true,
    ["Twilight Flame"]              = true,
    ["Elusive Power"]               = true,
    ["Motes of Flame"]              = true,
    ["Pillar of Flame"]             = true,
    ["Now is the Time!"]            = true,
    ["Now is the time!"]            = true,
    ["Curse of the Eye"]            = true,
    ["Dying Curse"]                 = true,
    ["Deadly Precision"]            = true,
    ["Forged Ember"]                = true,
    ["Blessing of the Broodmother"] = true,
    ["Dragon Soul"]                 = true,
    ["Sudden Velocity"]             = true,
    ["Greatness"]                   = true,
    ["Gathering Tracker"]           = true,
    ["Velocity"]                    = true,
    ["Chilled Heart"]               = true,
    ["Volatile Power"]              = true,
    ["Soul Power"]                  = true,
    ["Pure Energy"]                 = true,
    ["Revitalized"]                 = true,
    ["Pandora's Plea"]              = true,
    ["Living Flame"]                = true,
    ["Maghia's Misguided Quill"]    = true,
    ["Peerless Destruction"]        = true,
}

--- Timers di proc per il calcolo software dell'ICD
local Trinket_ProcTimers = {
    [13] = { lastProc = 0 },
    [14] = { lastProc = 0 },
}

--- Determina lo stato e la stringa descrittiva per uno slot trinket.
---@param slot number 13 oppure 14
---@param targetBuffID? number ID buff esplicito da Config
---@param targetICD? number Valore ICD in secondi
---@param isOnUse? boolean Se l'oggetto è on-use
---@return string state "ACTIVE", "COOLDOWN", oppure "READY"
---@return string text Testo formattato
---@return string icon Texture icona
---@return number remaining Tempo residuo
function FireMageHUD_GetTrinketStatus(slot, targetBuffID, targetICD, isOnUse)
    local itemID = GetInventoryItemID("player", slot)
    local itemName, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    itemName = itemName or (slot == 13 and "Trinket 1" or "Trinket 2")
    itemTexture = itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"

    -- 1. Controllo buff attivo dal database o dall'ID configurato
    local buffName = targetBuffID and targetBuffID > 0 and GetSpellInfo(targetBuffID)
    local entry = itemID and FMHUD_TrinketDB[itemID]

    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        local isMatch = false
        if entry then
            if (entry.spellId and spellId == entry.spellId)
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

    -- Fallback intelligente: intercetta proc caster non associati all'altro slot
    local otherSlot = (slot == 13) and 14 or 13
    local otherID = GetInventoryItemID("player", otherSlot)
    local otherEntry = otherID and FMHUD_TrinketDB[otherID]
    for i = 1, 40 do
        local name, _, icon, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            Trinket_ProcTimers[slot].lastProc = GetTime()
            local txt = string.format("%s\n|cFF00FF00ACTIVE %.1fs|r", itemName, rem)
            return "ACTIVE", txt, icon or itemTexture, rem
        end
    end

    -- 2. Cooldown nativo Blizzard On-Use
    local start, duration = GetInventoryItemCooldown("player", slot)
    if start and duration and start > 0 and duration > 1.5 then
        local rem = (start + duration) - GetTime()
        if rem > 0 then
            local txt = string.format("%s\n|cFFFF9900CD %.1fs|r", itemName, rem)
            return "COOLDOWN", txt, itemTexture, rem
        end
    end

    -- 3. ICD stimato per proc passivo
    local icd = targetICD or (entry and entry.icd) or 45
    if icd and icd > 0 and not isOnUse and Trinket_ProcTimers[slot].lastProc > 0 then
        local elapsed = GetTime() - Trinket_ProcTimers[slot].lastProc
        if elapsed < icd then
            local remICD = icd - elapsed
            local txt = string.format("%s\n|cFFFF9900ICD %.1fs|r", itemName, remICD)
            return "COOLDOWN", txt, itemTexture, remICD
        end
    end

    -- 4. Monile pronto
    local txt = string.format("%s\n|cFF00FF00READY|r", itemName)
    return "READY", txt, itemTexture, 0
end

--- Custom text (%c) per Trinket 1 (Slot 13).
---@return string
function FireMageHUD_Trinket1_CustomText()
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Trinket1) or {}
    local _, text = FireMageHUD_GetTrinketStatus(13, cfg.BuffID, cfg.InternalCD, cfg.IsOnUse)
    return text
end

--- Icona dinamica per Trinket 1 (Slot 13).
---@return string
function FireMageHUD_Trinket1_CustomIcon()
    local itemID = GetInventoryItemID("player", 13)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"
end

--- Custom text (%c) per Trinket 2 (Slot 14).
---@return string
function FireMageHUD_Trinket2_CustomText()
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Trinket2) or {}
    local _, text = FireMageHUD_GetTrinketStatus(14, cfg.BuffID, cfg.InternalCD, cfg.IsOnUse)
    return text
end

--- Icona dinamica per Trinket 2 (Slot 14).
---@return string
function FireMageHUD_Trinket2_CustomIcon()
    local itemID = GetInventoryItemID("player", 14)
    local _, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    return itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark"
end
