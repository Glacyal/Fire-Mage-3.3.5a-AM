--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo: Tier 10 2-Piece Bonus (Frostforged Sage / Pushing the Limit)
--- =========================================================================
--- Monitora il bonus del set 2P Tier 10 (Regalia del Mago del Sangue / Bloodmage)
--- e l'effetto proc Frostforged Sage (Spell ID 70753 / 72416):
--- - Spells: Pushing the Limit (ID 70753, +12% Haste per 5s) / Frostforged Sage (ID 72416, +285 SP)
--- - Auto-rilevamento multi-stadio: buff attivo, 15 Item ID noti (251/264/277) e scansione tooltip.
--- - Se >= 2 pezzi equipaggiati: inserito a destra della Gemma di Mana (tra Gemma e Combustion).
---   * In combinazione T8 + T10 (8 componenti): compattato a 26px a x = +49, y = -54.
---   * Con solo T10 (7 componenti): posizionato a 28px a x = +38, y = -54.
--- - Se < 2 pezzi equipaggiati: nascosto dinamicamente, lasciando spazio agli altri elementi.
--- =========================================================================

local T10_SetIDs = {
    -- 251 Normal (Bloodmage's Regalia)
    [50278] = true, -- Head
    [50279] = true, -- Shoulders
    [50275] = true, -- Chest
    [50277] = true, -- Legs
    [50276] = true, -- Hands
    -- 264 Sanctified (Sanctified Bloodmage's Regalia)
    [51283] = true, -- Head
    [51284] = true, -- Shoulders
    [51280] = true, -- Chest
    [51282] = true, -- Legs
    [51281] = true, -- Hands
    -- 277 Heroic Sanctified (Sanctified Bloodmage's Regalia)
    [51303] = true, -- Head
    [51304] = true, -- Shoulders
    [51300] = true, -- Chest
    [51302] = true, -- Legs
    [51301] = true, -- Hands
}

local T10_ProcTimer = { lastProc = 0, lastEnd = 0, isProc = false, lastSeen = 0, isRingProc = false }
local T10_EquipCache = { time = 0, isEquipped = false }

--- Verifica se il bonus 2P Tier 10 e' attivo sul mago con rilevamento multi-stadio.
---@return boolean isActive
function FireMageHUD_Tier10_IsActive()
    local now = GetTime()
    if (now - T10_EquipCache.time < 0.3) then
        return T10_EquipCache.isEquipped
    end

    -- 1. Controllo buff attivo Pushing the Limit / Frostforged Sage (70753 / 72416)
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 70753 or spellId == 72416 or name == "Frostforged Sage" or name == "Saggio della Forgia del Gelo" or name == "Pushing the Limit" or name == "Oltre il Limite" or (name.find and name:find("T10 2P")) then
            T10_ProcTimer.lastSeen = now
            T10_EquipCache = { time = now, isEquipped = true }
            return true
        end
    end

    -- 2. Controllo Item ID hardcoded dei set T10 (251, 264, 277)
    local count = 0
    local slots = { 1, 3, 5, 7, 10 }
    for _, slot in ipairs(slots) do
        local itemID = GetInventoryItemID("player", slot)
        if itemID and T10_SetIDs[itemID] then
            count = count + 1
        end
    end
    if count >= 2 then
        T10_EquipCache = { time = now, isEquipped = true }
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
    for _, slot in ipairs(slots) do
        local itemID = GetInventoryItemID("player", slot)
        if itemID then
            tt:ClearLines()
            tt:SetInventoryItem("player", slot)
            for j = 1, tt:NumLines() do
                local line = _G["FMHUD_AddonScanTTTextLeft"..j]
                local text = line and line:GetText()
                if text then
                    local lt = text:lower()
                    if lt:find("bloodmage") or lt:find("mago del sangue") or lt:find("pushing the limit") or lt:find("oltre il limite") or lt:find("frostforged") then
                        ttCount = ttCount + 1
                        break
                    end
                end
            end
        end
    end
    if ttCount >= 2 then
        T10_EquipCache = { time = now, isEquipped = true }
        return true
    end

    -- 4. Buff visto di recente (ultimi 60s)
    if T10_ProcTimer.lastSeen > 0 and (now - T10_ProcTimer.lastSeen < 60) then
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
    local altBuffID = cfg.AltBuffID or 72416
    local dur = cfg.Duration or 5.0

    local now = GetTime()

    -- 1. Controllo buff attivo
    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or spellId == altBuffID or name == "Frostforged Sage" or name == "Saggio della Forgia del Gelo" or name == "Pushing the Limit" or name == "Oltre il Limite" or (name.find and name:find("T10 2P")) then
            local isRing = (spellId == altBuffID or name == "Frostforged Sage" or name == "Saggio della Forgia del Gelo")
            local actualDur = (duration and duration > 0) and duration or (isRing and 10.0 or dur)
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or actualDur
            T10_ProcTimer.lastProc = now - (actualDur - rem)
            T10_ProcTimer.isProc = true
            T10_ProcTimer.lastSeen = now
            T10_ProcTimer.isRingProc = isRing
            return string.format("|cFFFFFF00%.1fs|r", rem)
        end
    end

    if T10_ProcTimer.isProc then
        T10_ProcTimer.isProc = false
    end

    -- 2. ICD per proc anello se applicabile (60s)
    if T10_ProcTimer.isRingProc and T10_ProcTimer.lastProc > 0 then
        local elapsed = now - T10_ProcTimer.lastProc
        if elapsed < 60 then
            local remICD = 60 - elapsed
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

--- Durata e scadenza dello swipe di ricarica per il Tier 10.
---@return number duration, number expirationTime
function FireMageHUD_Tier10_CustomDuration()
    if not FireMageHUD_Tier10_IsActive() then
        return 0, 0
    end

    local cfg = (FireMageHUD_Config and FireMageHUD_Config.Tier10) or {}
    local buffID = cfg.BuffID or 70753
    local altBuffID = cfg.AltBuffID or 72416
    local dur = cfg.Duration or 5.0

    local now = GetTime()

    -- Buff attivo
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == buffID or spellId == altBuffID or name == "Frostforged Sage" or name == "Saggio della Forgia del Gelo" or name == "Pushing the Limit" or name == "Oltre il Limite" or (name.find and name:find("T10 2P")) then
            local isRing = (spellId == altBuffID or name == "Frostforged Sage" or name == "Saggio della Forgia del Gelo")
            local actualDur = (duration and duration > 0) and duration or (isRing and 10.0 or dur)
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or actualDur
            return actualDur, now + rem
        end
    end

    -- Cooldown ICD (solo per ring proc)
    if T10_ProcTimer.isRingProc and T10_ProcTimer.lastProc > 0 then
        local elapsed = now - T10_ProcTimer.lastProc
        if elapsed < 60 then
            return 60, T10_ProcTimer.lastProc + 60
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
        if spellId == buffID or spellId == 72416 or name == "Frostforged Sage" or name == "Pushing the Limit" then
            if icon then return icon end
        end
    end
    return GetSpellTexture(buffID) or "Interface\\Icons\\Spell_Frost_FrostWard"
end
