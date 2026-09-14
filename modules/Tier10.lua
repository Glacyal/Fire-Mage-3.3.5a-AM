--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo: Tier 10 2-Piece Bonus (Pushing the Limit)
--- =========================================================================
--- Monitora il bonus del set 2P Tier 10 (Regalia del Mago del Sangue / Bloodmage)
--- e l'effetto proc Pushing the Limit (Spell ID 70753 / 70752 / 70747):
--- - Spells: Pushing the Limit (ID 70753, +12% Spell Haste per 5s)
--- - Auto-rilevamento multi-stadio: buff attivo, 20 Item ID noti (251/264/277), scansione link/nomi e tooltip.
--- - Se >= 2 pezzi equipaggiati: inserito a destra della Gemma di Mana (tra Gemma e Combustion).
---   * In combinazione T8 + T10 (8 componenti): compattato a 26px a x = +49, y = -54.
---   * Con solo T10 (7 componenti): posizionato a 28px a x = +38, y = -54.
--- - Se < 2 pezzi equipaggiati: nascosto dinamicamente, lasciando spazio agli altri elementi.
--- =========================================================================

local T10_SetIDs = {
    -- 251 Normal (Bloodmage's Regalia)
    [50275] = true, -- Gloves
    [50276] = true, -- Hood / Hands
    [50277] = true, -- Leggings
    [50278] = true, -- Robe / Head
    [50279] = true, -- Shoulderpads
    -- 264 Sanctified (Sanctified Bloodmage's Regalia)
    [51155] = true, -- Robe
    [51156] = true, -- Gloves
    [51157] = true, -- Hood
    [51158] = true, -- Leggings
    [51159] = true, -- Shoulderpads
    -- 277 Heroic Sanctified (Sanctified Bloodmage's Regalia)
    [51280] = true, -- Gloves
    [51281] = true, -- Hood
    [51282] = true, -- Leggings
    [51283] = true, -- Robe
    [51284] = true, -- Shoulderpads
    -- Private server / alternate item IDs
    [51300] = true, [51301] = true, [51302] = true, [51303] = true, [51304] = true,
}

local T10_ProcTimer = { lastProc = 0, lastEnd = 0, isProc = false, lastSeen = 0 }
local T10_EquipCache = { time = 0, isEquipped = false }
local T10_EquippedPersistent = false

-- Frame per invalidare la cache all'effettivo cambio di equipaggiamento
local T10_EventFrame = CreateFrame("Frame")
T10_EventFrame:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
T10_EventFrame:RegisterEvent("UNIT_INVENTORY_CHANGED")
T10_EventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
T10_EventFrame:SetScript("OnEvent", function()
    T10_EquipCache.time = 0
    T10_EquipCache.isEquipped = false
    T10_EquippedPersistent = false
end)

--- Verifica se il bonus 2P Tier 10 e' attivo sul mago con rilevamento multi-stadio.
---@return boolean isActive
function FireMageHUD_Tier10_IsActive()
    local now = GetTime()
    if (now - T10_EquipCache.time < 0.3) then
        return T10_EquipCache.isEquipped
    end

    -- Check 0: Stato persistente gia' confermato
    if T10_EquippedPersistent then
        T10_EquipCache = { time = now, isEquipped = true }
        return true
    end

    -- 1. Controllo buff attivo Pushing the Limit / Oltre il Limite (70753 / 70752 / 70747)
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 70753 or spellId == 70752 or spellId == 70747 or name == "Pushing the Limit" or name == "Oltre il Limite" or (name.find and (name:find("Limit") or name:find("Limite"))) then
            T10_ProcTimer.lastSeen = now
            T10_EquippedPersistent = true
            T10_EquipCache = { time = now, isEquipped = true }
            return true
        end
    end

    -- 2. Controllo Item ID sui 5 slot armatura (1=Head, 3=Shoulder, 5=Chest, 7=Legs, 10=Hands)
    local count = 0
    local slots = { 1, 3, 5, 7, 10 }
    for _, slot in ipairs(slots) do
        local itemID = GetInventoryItemID("player", slot)
        if itemID and T10_SetIDs[itemID] then
            count = count + 1
        end
    end
    if count >= 2 then
        T10_EquippedPersistent = true
        T10_EquipCache = { time = now, isEquipped = true }
        return true
    end

    -- 3. Scansione stringa Item Link & Nome oggetto
    local nameCount = 0
    for _, slot in ipairs(slots) do
        local link = GetInventoryItemLink("player", slot)
        if link then
            local lk = link:lower()
            if lk:find("bloodmage") or lk:find("mago del sangue") or lk:find("blutmagier") or lk:find("sangriento") or lk:find("mage de sang") then
                nameCount = nameCount + 1
            else
                local itemName = GetItemInfo(link)
                if itemName then
                    local iname = itemName:lower()
                    if iname:find("bloodmage") or iname:find("mago del sangue") or iname:find("blutmagier") or iname:find("sangriento") or iname:find("mage de sang") then
                        nameCount = nameCount + 1
                    end
                end
            end
        end
    end
    if nameCount >= 2 then
        T10_EquippedPersistent = true
        T10_EquipCache = { time = now, isEquipped = true }
        return true
    end

    -- 4. Scansione GameTooltip per set bonus "(2) Set" o "12% haste / celerita'"
    local ttCount = 0
    local tt = _G.FMHUD_AddonScanTT
    if not tt then
        tt = CreateFrame("GameTooltip", "FMHUD_AddonScanTT", nil, "GameTooltipTemplate")
        _G.FMHUD_AddonScanTT = tt
    end
    for _, slot in ipairs(slots) do
        local link = GetInventoryItemLink("player", slot)
        if link then
            tt:SetOwner(UIParent, "ANCHOR_NONE")
            tt:ClearLines()
            tt:SetInventoryItem("player", slot)
            for j = 1, tt:NumLines() do
                local line = _G["FMHUD_AddonScanTTTextLeft"..j]
                local text = line and line:GetText()
                if text then
                    local lt = text:lower()
                    if lt:find("bloodmage") or lt:find("mago del sangue") or lt:find("pushing the limit") or lt:find("oltre il limite") or (lt:find("12%%") and (lt:find("haste") or lt:find("celerit") or lt:find("speed") or lt:find("tempo") or lt:find("lancio"))) then
                        ttCount = ttCount + 1
                        break
                    end
                end
            end
        end
    end
    if ttCount >= 2 then
        T10_EquippedPersistent = true
        T10_EquipCache = { time = now, isEquipped = true }
        return true
    end

    -- 5. Buff visto durante la sessione
    if T10_ProcTimer.lastSeen > 0 then
        T10_EquippedPersistent = true
        T10_EquipCache = { time = now, isEquipped = true }
        return true
    end

    T10_EquipCache = { time = now, isEquipped = false }
    return false
end

--- Genera il testo descrittivo dello stato del Tier 10 (%c).
---@return string formattedStatus
function FireMageHUD_Tier10_CustomText()
    if not FireMageHUD_Tier10_IsActive() then
        return ""
    end

    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Tier10) or {}
    local buffID = cfg.BuffID or 70753
    local dur = cfg.Duration or 5.0

    local now = GetTime()

    -- 1. Controllo buff attivo
    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or spellId == 70752 or spellId == 70747 or name == "Pushing the Limit" or name == "Oltre il Limite" or (name.find and (name:find("Limit") or name:find("Limite"))) then
            local actualDur = (duration and duration > 0) and duration or dur
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or actualDur
            T10_ProcTimer.lastProc = now - (actualDur - rem)
            T10_ProcTimer.isProc = true
            T10_ProcTimer.lastSeen = now
            T10_EquippedPersistent = true
            return string.format("|cFFFFFF00%.1fs|r", rem)
        end
    end

    if T10_ProcTimer.isProc then
        T10_ProcTimer.isProc = false
    end

    -- 2. Pronto (idle)
    return ""
end

--- Durata e scadenza dello swipe di ricarica per il Tier 10.
---@return number duration, number expirationTime
function FireMageHUD_Tier10_CustomDuration()
    if not FireMageHUD_Tier10_IsActive() then
        return 0, 0
    end

    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Tier10) or {}
    local buffID = cfg.BuffID or 70753
    local dur = cfg.Duration or 5.0

    local now = GetTime()

    -- Buff attivo
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or spellId == 70752 or spellId == 70747 or name == "Pushing the Limit" or name == "Oltre il Limite" or (name.find and (name:find("Limit") or name:find("Limite"))) then
            local actualDur = (duration and duration > 0) and duration or dur
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or actualDur
            return actualDur, now + rem
        end
    end

    return 0, 0
end

--- Icona dinamica per il Tier 10.
---@return string iconPath
function FireMageHUD_Tier10_CustomIcon()
    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Tier10) or {}
    local buffID = cfg.BuffID or 70753
    for i = 1, 40 do
        local name, _, icon, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or spellId == 70752 or spellId == 70747 or name == "Pushing the Limit" or name == "Oltre il Limite" then
            if icon then return icon end
        end
    end
    return GetSpellTexture(buffID) or "Interface\\Icons\\Spell_Fire_ElementalDevastation"
end
