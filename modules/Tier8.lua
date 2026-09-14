--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo: Tier 8 2-Piece Bonus (Praxis)
--- =========================================================================
--- Monitora il bonus del set 2P Tier 8 (Kirin Tor):
--- - Spells: Praxis (ID 64868, +350 Spell Power per 15s, 45s ICD)
--- - Auto-rilevamento pezzi equipaggiati (Elmo, Spalle, Torso, Guanti, Gambe 10m/25m).
--- - Se >= 2 pezzi equipaggiati: attivo nel HUD (x = 0, y = -54 tra Mantello e Gemma).
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

local T8_ProcTimer = { lastProc = 0, lastEnd = 0, isProc = false }

--- Calcola il numero di pezzi Tier 8 equipaggiati dal mago.
---@return number count
function FireMageHUD_Tier8_GetEquippedCount()
    local count = 0
    local slots = { 1, 3, 5, 7, 10 }
    for _, slot in ipairs(slots) do
        local itemID = GetInventoryItemID("player", slot)
        if itemID and T8_SetIDs[itemID] then
            count = count + 1
        end
    end
    return count
end

--- Verifica se il bonus 2P Tier 8 e' attivo.
---@return boolean isActive
function FireMageHUD_Tier8_IsActive()
    return FireMageHUD_Tier8_GetEquippedCount() >= 2
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
    return "Interface\\Icons\\Spell_Arcane_StudentOfMagic"
end
