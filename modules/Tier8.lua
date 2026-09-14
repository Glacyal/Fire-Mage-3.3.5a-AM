--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo: Tier 8 2-Piece Bonus (Praxis)
--- =========================================================================
--- Monitora il bonus del set 2P Tier 8 (Kirin Tor):
--- - Spells: Praxis (ID 64868, +350 Spell Power per 15s, 45s ICD)
--- - Auto-rilevamento multi-stadio: buff attivo, 10 Item ID noti e scansione tooltip.
--- - Se >= 2 pezzi equipaggiati (o buff Praxis attivo): inserito a x = 0, y = -54 tra Mantello e Gemma.
--- - Se < 2 pezzi equipaggiati: nascosto, HUD a 6 icone simmetriche.
--- =========================================================================

local T8_SetIDs = {
    -- 10-Man Valorous Kirin Tor
    [45367] = true, -- Head
    [45369] = true, -- Shoulder
    [45365] = true, -- Chest
    [45366] = true, -- Legs
    [45368] = true, -- Hands
    -- 25-Man Conqueror's Kirin Tor
    [45357] = true, -- Head
    [45359] = true, -- Shoulder
    [45355] = true, -- Chest
    [45356] = true, -- Legs
    [45358] = true, -- Hands
}

local ARMOR_SLOTS = { 1, 3, 5, 7, 10 }
local T8_ProcTimer = { lastProc = 0, lastEnd = 0, isProc = false, lastSeen = 0 }
local T8_EquipCache = { time = 0, isEquipped = false }
local T8_EquippedPersistent = false

-- Frame per invalidare la cache all'effettivo cambio di equipaggiamento
local T8_EventFrame = CreateFrame("Frame")
T8_EventFrame:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
T8_EventFrame:RegisterEvent("UNIT_INVENTORY_CHANGED")
T8_EventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
T8_EventFrame:SetScript("OnEvent", function()
    T8_EquipCache.time = 0
    T8_EquipCache.isEquipped = false
    T8_EquippedPersistent = false
end)

--- Verifica se il bonus 2P Tier 8 e' attivo sul mago con rilevamento multi-stadio.
---@return boolean isActive
function FireMageHUD_Tier8_IsActive()
    local now = GetTime()
    if (now - T8_EquipCache.time < 0.3) then
        return T8_EquipCache.isEquipped
    end

    -- Check 0: Stato persistente gia' confermato
    if T8_EquippedPersistent then
        T8_EquipCache.time = now
        T8_EquipCache.isEquipped = true
        return true
    end

    -- 1. Controllo buff attivo Praxis (64868 / "Praxis" / "Prassi")
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 64868 or name == "Praxis" or name == "Prassi" or (name.find and name:find("T8 2P")) then
            T8_ProcTimer.lastSeen = now
            T8_EquippedPersistent = true
            T8_EquipCache.time = now
            T8_EquipCache.isEquipped = true
            return true
        end
    end

    -- 2. Controllo Item ID hardcoded
    local count = 0
    for _, slot in ipairs(ARMOR_SLOTS) do
        local itemID = GetInventoryItemID("player", slot)
        if itemID and T8_SetIDs[itemID] then
            count = count + 1
        end
    end
    if count >= 2 then
        T8_EquippedPersistent = true
        T8_EquipCache.time = now
        T8_EquipCache.isEquipped = true
        return true
    end

    -- 3. Scansione tooltip su pezzi equipaggiati
    local ttCount = 0
    local tt = _G.FMHUD_AddonScanTT
    if not tt then
        tt = CreateFrame("GameTooltip", "FMHUD_AddonScanTT", nil, "GameTooltipTemplate")
        tt:SetOwner(WorldFrame, "ANCHOR_NONE")
        _G.FMHUD_AddonScanTT = tt
    end
    for _, slot in ipairs(ARMOR_SLOTS) do
        local itemID = GetInventoryItemID("player", slot)
        if itemID then
            tt:ClearLines()
            tt:SetInventoryItem("player", slot)
            for j = 1, tt:NumLines() do
                local line = _G["FMHUD_AddonScanTTTextLeft"..j]
                local text = line and line:GetText()
                if text then
                    local lt = text:lower()
                    if lt:find("kirin tor") or lt:find("praxis") or lt:find("prassi") then
                        ttCount = ttCount + 1
                        break
                    end
                end
            end
        end
    end
    if ttCount >= 2 then
        T8_EquippedPersistent = true
        T8_EquipCache.time = now
        T8_EquipCache.isEquipped = true
        return true
    end

    -- 4. Buff visto di recente (ultimi 60s) o durante sessione
    if T8_ProcTimer.lastSeen > 0 then
        T8_EquippedPersistent = true
        T8_EquipCache.time = now
        T8_EquipCache.isEquipped = true
        return true
    end

    T8_EquipCache.time = now
    T8_EquipCache.isEquipped = false
    return false
end

--- Genera il testo descrittivo dello stato del Tier 8 (%c).
---@return string formattedStatus
function FireMageHUD_Tier8_CustomText()
    if not FireMageHUD_Tier8_IsActive() then
        return ""
    end

    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Tier8) or {}
    local buffID = cfg.BuffID or 64868
    local icd = cfg.InternalCD or 45
    local dur = cfg.Duration or 15.0

    local now = GetTime()

    -- 1. Controllo buff attivo Praxis (+350 SP)
    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or name == "Praxis" or name == "Prassi" or (name.find and name:find("T8 2P")) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or dur
            T8_ProcTimer.lastProc = now - (dur - rem)
            T8_ProcTimer.isProc = true
            T8_ProcTimer.lastSeen = now
            return string.format("|cFFFFFF00%.1fs|r", rem)
        end
    end

    if T8_ProcTimer.isProc then
        T8_ProcTimer.isProc = false
    end

    -- 2. ICD Stimato (45s totale)
    if T8_ProcTimer.lastProc > 0 then
        local elapsed = now - T8_ProcTimer.lastProc
        if elapsed < icd then
            local remICD = icd - elapsed
            if remICD >= 60 then
                local m = math.floor(remICD / 60)
                local s = math.floor(remICD % 60)
                return string.format("%d:%02d", m, s)
            else
                return string.format("%.0f", remICD)
            end
        end
    end

    -- 3. Pronto
    return ""
end

--- Durata e scadenza dello swipe di ricarica per il Tier 8.
---@return number duration, number expirationTime
function FireMageHUD_Tier8_CustomDuration()
    if not FireMageHUD_Tier8_IsActive() then
        return 0, 0
    end

    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Tier8) or {}
    local buffID = cfg.BuffID or 64868
    local icd = cfg.InternalCD or 45
    local dur = cfg.Duration or 15.0

    local now = GetTime()

    -- Buff attivo
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or name == "Praxis" or name == "Prassi" or (name.find and name:find("T8 2P")) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or dur
            return dur, now + rem
        end
    end

    -- Cooldown ICD
    if T8_ProcTimer.lastProc > 0 then
        local elapsed = now - T8_ProcTimer.lastProc
        if elapsed < icd then
            return icd, T8_ProcTimer.lastProc + icd
        end
    end

    return 0, 0
end

--- Icona dinamica per il Tier 8.
---@return string iconPath
function FireMageHUD_Tier8_CustomIcon()
    return GetSpellTexture(64868) or "Interface\\Icons\\Spell_Arcane_StudentOfMagic"
end
