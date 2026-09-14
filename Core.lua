--- =========================================================================
--- Fire Mage 3.3.5a AM — Core Library & Utilities
--- Compatibile con World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340)
--- Fornisce funzioni sicure di scansione aure, formattazione, castbar e ICD.
--- =========================================================================

FireMageHUD_Core = FireMageHUD_Core or {}

local Core = FireMageHUD_Core
local Config = FireMageHUD_Config or {}

--- Tabella per il tracciamento interno degli Internal Cooldown (ICD) passivi
Core.ICD_Tracker = Core.ICD_Tracker or {
    Trinket1 = { lastProc = 0, icd = 45 },
    Trinket2 = { lastProc = 0, icd = 45 },
    Cloak    = { lastProc = 0, icd = 45 },
}

-- -------------------------------------------------------------------------
-- LOGGING E DIAGNOSTICA
-- -------------------------------------------------------------------------

--- Stampa messaggi diagnostici in chat se la modalità Debug è attiva in Config.
---@param formatStr string Stringa di formattazione compatibile con string.format
---@param ... any Parametri opzionali per la formattazione
function Core:Log(formatStr, ...)
    local cfg = FireMageHUD_Config or Config
    if cfg and cfg.Debug then
        local msg = string.format(formatStr, ...)
        DEFAULT_CHAT_FRAME:AddMessage("|cFFFF6600[FireMageHUD]|r " .. msg)
    end
end

-- -------------------------------------------------------------------------
-- FORMATTAZIONE NUMERI E TEMPI
-- -------------------------------------------------------------------------

--- Formatta un valore numerico in formato compatto (k, M) o esteso.
---@param value number Il numero da formattare
---@param mode? string "SHORT" (es. 14.8k) o "FULL" (es. 14820)
---@return string Valore formattato
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

--- Formatta i secondi rimanenti in una stringa leggibile (m:ss, secondi interi o decimali).
---@param seconds number Secondi da formattare
---@return string Tempo formattato
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

-- -------------------------------------------------------------------------
-- WRAPPER SICURI API AURE (BUFF / DEBUFF)
-- -------------------------------------------------------------------------

--- Scansiona i buff di un'unità per SpellID o per nome (slot 1..40).
---@param unit string Identificatore unità (es. "player", "target")
---@param spellIdentifier number|string Spell ID numerico o nome testuale
---@return string|nil name, string|nil rank, string|nil icon, number|nil count, number|nil duration, number|nil expirationTime, string|nil unitCaster, number|nil spellId
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

--- Scansiona i debuff di un'unità per SpellID o per nome (slot 1..40).
---@param unit string Identificatore unità (es. "target")
---@param spellIdentifier number|string Spell ID numerico o nome testuale
---@return string|nil name, string|nil rank, string|nil icon, number|nil count, number|nil duration, number|nil expirationTime, string|nil unitCaster, number|nil spellId
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

-- -------------------------------------------------------------------------
-- STATO MOLTEN ARMOR E MOLTEN FURY
-- -------------------------------------------------------------------------

--- Controlla la presenza e la durata residua di Molten Armor sul giocatore.
---@return boolean isPresent, string name, string icon, number remainingSeconds
function Core:CheckMoltenArmor()
    local spells = (Config.Spells and Config.Spells.MoltenArmor) or { 43046, 43045, 30482 }
    local nameFallback = (Config.Spells and Config.Spells.MoltenArmor and Config.Spells.MoltenArmor.Name) or "Molten Armor"

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

    local name, rank, icon, count, duration, expirationTime = Core:FindBuff("player", nameFallback)
    if name then
        local rem = expirationTime and (expirationTime > 0) and math.max(0, expirationTime - GetTime()) or 0
        return true, name, icon, rem
    end

    return false, nameFallback, "Interface\\Icons\\Spell_Fire_Incinerate", 0
end

--- Verifica se il bersaglio si trova nella fase di Execute (vita <= 35% per Molten Fury).
---@return boolean isExecuteActive, number currentHpPercent
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

-- -------------------------------------------------------------------------
-- STATO VITA TARGET E FOCUS
-- -------------------------------------------------------------------------

--- Restituisce i dati di salute correnti e massimi per un'unità.
---@param unit string Identificatore unità (es. "target", "focus")
---@return boolean exists, string name, number currentHp, number maxHp, number percent, boolean isDead
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

-- -------------------------------------------------------------------------
-- CASTBAR E CANALIZZAZIONE (3.3.5a)
-- -------------------------------------------------------------------------

--- Recupera i dettagli del cast o della canalizzazione in corso per un'unità.
---@param unit? string Identificatore unità (predefinito: "player")
---@return string castType "CAST", "CHANNEL" oppure "NONE"
---@return string|nil spellName Nome della magia
---@return string|nil icon Texture icona
---@return number elapsed Tempo trascorso in secondi
---@return number remaining Tempo rimanente in secondi
---@return number duration Durata complessiva in secondi
---@return boolean notInterruptible Vero se il lancio è protetto da interruzioni
function Core:GetCastOrChannelInfo(unit)
    unit = unit or "player"
    
    local spell, rank, displayName, icon, startTime, endTime, isTradeSkill, castID, notInterruptible = UnitCastingInfo(unit)
    if spell then
        local now = GetTime() * 1000
        local duration = (endTime - startTime) / 1000
        local elapsed = (now - startTime) / 1000
        local remaining = (endTime - now) / 1000
        return "CAST", spell, icon, elapsed, remaining, duration, notInterruptible
    end

    spell, rank, displayName, icon, startTime, endTime, isTradeSkill, notInterruptible = UnitChannelInfo(unit)
    if spell then
        local now = GetTime() * 1000
        local duration = (endTime - startTime) / 1000
        local remaining = (endTime - now) / 1000
        local elapsed = duration - remaining
        return "CHANNEL", spell, icon, elapsed, remaining, duration, notInterruptible
    end

    return "NONE", nil, nil, 0, 0, 0, false
end

-- -------------------------------------------------------------------------
-- GLOBAL COOLDOWN (GCD)
-- -------------------------------------------------------------------------

--- Calcola lo stato del Global Cooldown via spell 61304 o fallback su Fire Blast.
---@return boolean isActive, number startTime, number duration, number remaining
function Core:GetGCD()
    local gcdSpell = (Config.Spells and Config.Spells.GCDReferenceSpell) or 61304
    local start, duration = GetSpellCooldown(gcdSpell)
    
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

-- -------------------------------------------------------------------------
-- TRACCIAMENTO TRINKET E MANTELLO (On-Use vs Proc Passivo + ICD)
-- -------------------------------------------------------------------------

--- Determina lo stato operativo di uno slot di equipaggiamento (13, 14 o 15).
---@param slot number Numero slot (13, 14 o 15)
---@param buffID? number ID buff opzionale per il monitoraggio proc
---@param customICD? number Secondi di Internal Cooldown per proc passivi
---@param isOnUse? boolean Vero se l'oggetto è ad attivazione manuale
---@return string state "ACTIVE", "COOLDOWN", oppure "READY"
---@return string name Nome dell'oggetto o slot
---@return string icon Texture icona
---@return number remaining Tempo rimanente
---@return number duration Durata totale
---@return number count Cariche o stack
function Core:GetEquipSlotStatus(slot, buffID, customICD, isOnUse)
    local itemID = GetInventoryItemID("player", slot)
    local itemName, _, _, _, _, _, _, _, _, itemTexture = itemID and GetItemInfo(itemID) or nil
    itemName = itemName or ("Slot " .. slot)

    -- 1. Buff proc attivo
    if buffID and buffID > 0 then
        local bName, bRank, bIcon, bCount, bDur, bExp = Core:FindBuff("player", buffID)
        if bName then
            local rem = bExp and (bExp > 0) and math.max(0, bExp - GetTime()) or 0
            if slot == 13 then Core.ICD_Tracker.Trinket1.lastProc = GetTime() end
            if slot == 14 then Core.ICD_Tracker.Trinket2.lastProc = GetTime() end
            if slot == 15 then Core.ICD_Tracker.Cloak.lastProc = GetTime() end
            return "ACTIVE", itemName, bIcon or itemTexture, rem, bDur or 15, bCount
        end
    end

    -- 2. Cooldown nativo Blizzard On-Use
    local start, duration, enable = GetInventoryItemCooldown("player", slot)
    if start and duration and start > 0 and duration > 1.5 then
        local rem = (start + duration) - GetTime()
        if rem > 0 then
            return "COOLDOWN", itemName, itemTexture, rem, duration, 0
        end
    end

    -- 3. ICD stimato per proc passivi
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
