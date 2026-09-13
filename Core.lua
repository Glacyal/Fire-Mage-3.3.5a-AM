-- =========================================================================
-- Fire Mage HUD 3.3.5a — Core Library & Utilities
-- Compatibile con World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340)
-- =========================================================================

FireMageHUD_Core = FireMageHUD_Core or {}

local Core = FireMageHUD_Core
local Config = FireMageHUD_Config or {}

-- Tabella interna per il tracciamento degli Internal Cooldown (ICD) software
Core.ICD_Tracker = Core.ICD_Tracker or {
    Trinket1 = { lastProc = 0, icd = 45 },
    Trinket2 = { lastProc = 0, icd = 45 },
    Cloak    = { lastProc = 0, icd = 45 },
}

-- =========================================================================
-- FUNZIONI DIAGNOSTICHE E LOGGING
-- =========================================================================

function Core:Log(formatStr, ...)
    local cfg = FireMageHUD_Config or Config
    if cfg and cfg.Debug then
        local msg = string.format(formatStr, ...)
        DEFAULT_CHAT_FRAME:AddMessage("|cFFFF6600[FireMageHUD]|r " .. msg)
    end
end

-- =========================================================================
-- FORMATTAZIONE NUMERI E TEMPO
-- =========================================================================

function Core:FormatNumber(value, mode)
    if not value or value < 0 then return "0" end
    mode = mode or (Config.Mana and Config.Mana.Format) or "SHORT"

    if mode == "SHORT" then
        if value >= 1000000 then
            return string.format("%.1fM", value / 1000000)
        elseif value >= 1000 then
            return string.format("%.1fk", value / 1000)
        else
            return string.format("%d", value)
        end
    else
        return string.format("%d", value)
    end
end

function Core:FormatTime(seconds)
    if not seconds or seconds <= 0 then return "0.0s" end
    if seconds >= 60 then
        local m = math.floor(seconds / 60)
        local s = math.floor(seconds % 60)
        return string.format("%dm %02ds", m, s)
    elseif seconds >= 10 then
        return string.format("%ds", math.floor(seconds))
    else
        return string.format("%.1fs", seconds)
    end
end

-- =========================================================================
-- WRAPPER SICURI API AURE E BUFF / DEBUFF (3.3.5a)
-- =========================================================================

-- Cerca un Buff su un'unità per SpellID o Nome (scansione 1..40)
function Core:FindBuff(unit, spellIdentifier)
    if not UnitExists(unit) then return nil end
    local targetName = type(spellIdentifier) == "number" and GetSpellInfo(spellIdentifier) or spellIdentifier

    for i = 1, 40 do
        local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitBuff(unit, i)
        if not name then break end
        if (targetName and name == targetName) or (type(spellIdentifier) == "number" and spellId == spellIdentifier) then
            return name, rank, icon, count, duration, expirationTime, unitCaster, spellId
        end
    end
    return nil
end

-- Cerca un Debuff su un'unità per SpellID o Nome (scansione 1..40)
function Core:FindDebuff(unit, spellIdentifier)
    if not UnitExists(unit) then return nil end
    local targetName = type(spellIdentifier) == "number" and GetSpellInfo(spellIdentifier) or spellIdentifier

    for i = 1, 40 do
        local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitDebuff(unit, i)
        if not name then break end
        if (targetName and name == targetName) or (type(spellIdentifier) == "number" and spellId == spellIdentifier) then
            return name, rank, icon, count, duration, expirationTime, unitCaster, spellId
        end
    end
    return nil
end

-- =========================================================================
-- MOLTEN ARMOR MONITOR PERMANENTE
-- =========================================================================

function Core:CheckMoltenArmor()
    local spells = (Config.Spells and Config.Spells.MoltenArmor) or { 43046, 43045, 30482 }
    local nameFallback = (Config.Spells and Config.Spells.MoltenArmor and Config.Spells.MoltenArmor.Name) or "Molten Armor"

    -- Prova con i rank ID
    if type(spells) == "table" then
        for _, id in pairs(spells) do
            if type(id) == "number" then
                local name, rank, icon, count, duration, expirationTime = Core:FindBuff("player", id)
                if name then
                    local rem = expirationTime and (expirationTime > 0) and math.max(0, expirationTime - GetTime()) or 0
                    return true, name, icon, rem
                end
            end
        end
    end

    -- Prova per nome
    local name, rank, icon, count, duration, expirationTime = Core:FindBuff("player", nameFallback)
    if name then
        local rem = expirationTime and (expirationTime > 0) and math.max(0, expirationTime - GetTime()) or 0
        return true, name, icon, rem
    end

    return false, nameFallback, "Interface\\Icons\\Spell_Fire_Incinerate", 0
end

-- =========================================================================
-- MOLTEN FURY STATUS (Talento <= 35% HP Target)
-- =========================================================================

function Core:CheckMoltenFury()
    if not UnitExists("target") or UnitIsDeadOrGhost("target") then
        return false, 0
    end
    local maxHp = UnitHealthMax("target")
    if not maxHp or maxHp <= 0 then return false, 0 end
    local curHp = UnitHealth("target")
    local pct = (curHp / maxHp) * 100
    local threshold = (Config.Spells and Config.Spells.MoltenFury and Config.Spells.MoltenFury.ThresholdPercent) or 35.0

    return (pct <= threshold), pct
end

-- =========================================================================
-- TARGET & FOCUS HEALTH & STATUS
-- =========================================================================

function Core:GetUnitHealthData(unit)
    if not UnitExists(unit) then
        return false, "NO " .. string.upper(unit), 0, 0, 0, false
    end
    local isDead = UnitIsDeadOrGhost(unit)
    local name = UnitName(unit) or "Unknown"
    local cur = UnitHealth(unit) or 0
    local max = UnitHealthMax(unit) or 1
    local pct = max > 0 and (cur * 100 / max) or 0

    return true, name, cur, max, pct, isDead
end

-- =========================================================================
-- CASTBAR & CHANNELING STATUS (3.3.5a)
-- =========================================================================

function Core:GetCastOrChannelInfo(unit)
    unit = unit or "player"
    
    -- Controllo Cast standard
    local spell, rank, displayName, icon, startTime, endTime, isTradeSkill, castID, notInterruptible = UnitCastingInfo(unit)
    if spell then
        local now = GetTime() * 1000
        local startSec = startTime / 1000
        local endSec = endTime / 1000
        local duration = endSec - startSec
        local elapsed = (now - startTime) / 1000
        local remaining = (endTime - now) / 1000
        return "CAST", spell, icon, elapsed, remaining, duration, notInterruptible
    end

    -- Controllo Channeling (es. Evocation, Blizzard)
    spell, rank, displayName, icon, startTime, endTime, isTradeSkill, notInterruptible = UnitChannelInfo(unit)
    if spell then
        local now = GetTime() * 1000
        local startSec = startTime / 1000
        local endSec = endTime / 1000
        local duration = endSec - startSec
        local remaining = (endTime - now) / 1000
        local elapsed = duration - remaining
        return "CHANNEL", spell, icon, elapsed, remaining, duration, notInterruptible
    end

    return "NONE", nil, nil, 0, 0, 0, false
end

-- =========================================================================
-- GLOBAL COOLDOWN (GCD)
-- =========================================================================

function Core:GetGCD()
    local gcdSpell = (Config.Spells and Config.Spells.GCDReferenceSpell) or 61304
    local start, duration = GetSpellCooldown(gcdSpell)
    
    -- Fallback su Fire Blast se la reference spell non è disponibile
    if not start or duration == 0 or duration > 1.5 then
        local fbSpell = (Config.Spells and Config.Spells.FireBlast and Config.Spells.FireBlast.SpellID) or 42873
        start, duration = GetSpellCooldown(fbSpell)
    end

    if start and duration and start > 0 and duration > 0 and duration <= 1.5 then
        local remaining = (start + duration) - GetTime()
        return true, start, duration, math.max(0, remaining)
    end

    return false, 0, 0, 0
end

-- =========================================================================
-- TRINKET & CLOAK TRACKER (On-Use vs Proc Buff + ICD)
-- =========================================================================

function Core:GetEquipSlotStatus(slot, buffID, customICD, isOnUse)
    local itemID = GetInventoryItemID("player", slot)
    local itemName, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    itemName = itemName or ("Slot " .. slot)

    -- 1. Controllo Buff Proc attivo (se specificato)
    if buffID and buffID > 0 then
        local bName, bRank, bIcon, bCount, bDur, bExp = Core:FindBuff("player", buffID)
        if bName then
            local rem = bExp and (bExp > 0) and math.max(0, bExp - GetTime()) or 0
            -- Aggiorna l'ultimo momento di proc per il calcolo dell'ICD
            if slot == 13 then Core.ICD_Tracker.Trinket1.lastProc = GetTime() end
            if slot == 14 then Core.ICD_Tracker.Trinket2.lastProc = GetTime() end
            if slot == 15 then Core.ICD_Tracker.Cloak.lastProc = GetTime() end
            return "ACTIVE", itemName, bIcon or itemTexture, rem, bDur or 15, bCount
        end
    end

    -- 2. Controllo Cooldown On-Use da API
    local start, duration, enable = GetInventoryItemCooldown("player", slot)
    if start and duration and start > 0 and duration > 1.5 then
        local rem = (start + duration) - GetTime()
        if rem > 0 then
            return "COOLDOWN", itemName, itemTexture, rem, duration, 0
        end
    end

    -- 3. Controllo ICD Software per Proc Passivi
    local lastProcInfo = (slot == 13 and Core.ICD_Tracker.Trinket1)
                      or (slot == 14 and Core.ICD_Tracker.Trinket2)
                      or (slot == 15 and Core.ICD_Tracker.Cloak)
    
    if lastProcInfo and lastProcInfo.lastProc > 0 and customICD and customICD > 0 and not isOnUse then
        local elapsedSinceProc = GetTime() - lastProcInfo.lastProc
        if elapsedSinceProc < customICD then
            local remICD = customICD - elapsedSinceProc
            return "COOLDOWN", itemName, itemTexture, remICD, customICD, 0
        end
    end

    -- 4. Oggetto pronto
    return "READY", itemName, itemTexture, 0, 0, 0
end

