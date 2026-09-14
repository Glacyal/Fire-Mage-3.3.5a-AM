--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 01: Proc & Rotazione Fire Mage
--- =========================================================================
--- Gestisce le icone della riga orizzontale superiore (yOffset = +44):
--- 1. Hot Streak (Buff 48108, timer rosso <= 3s, pixel glow dorato).
--- 2. Clearcasting (Buff 12536, timer rosso <= 4s, pixel glow dorato).
--- 3. Living Bomb (Debuff 55360 sul target, timer rosso <= 3s per refresh senza clippare).
--- 4. Ignite (Debuff 12654 sul target, timer rosso <= 1.5s).
--- 5. Scorch / Improved Scorch (Debuff 22959 sul target, timer rosso <= 5s).
--- 6. Combustion (Stato a 3 fasi: READY, ACTIVE con stacks x%d, COOLDOWN).
--- 7. Molten Fury (Attivo quando il target scende a <= 35% HP).
--- =========================================================================

-- -------------------------------------------------------------------------
-- 1. HOT STREAK (Buff Giocatore)
-- -------------------------------------------------------------------------

--- Rileva la presenza del proc Hot Streak sul giocatore.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isProcActive
function FireMageHUD_HotStreak_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wanted = GetSpellInfo(48108) or "Hot Streak"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == "Hot Streak" then
            return true
        end
    end
    return false
end

--- Genera il conto alla rovescia (%c): rosso vivo <= 3s, bianco intero > 3s.
---@return string formattedTimer
function FireMageHUD_HotStreak_CustomText()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 48108 or name == "Hot Streak" or name == "Buona sorte" or string.find(name, "Hot Streak") or string.find(name, "Buona") then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 3 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end

-- -------------------------------------------------------------------------
-- 2. CLEARCASTING / CONCENTRAZIONE ARCANA (Buff Giocatore)
-- -------------------------------------------------------------------------

--- Genera il conto alla rovescia (%c): rosso vivo <= 4s, bianco intero > 4s.
---@return string formattedTimer
function FireMageHUD_Clearcasting_CustomText()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 12536 or name == "Clearcasting" or name == "Arcane Concentration" or name == "Lancio limpido" or name == "Concentrazione Arcana" or string.find(name, "Clearcasting") or string.find(name, "Limpido") or string.find(name, "Concentrat") then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 4 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end

-- -------------------------------------------------------------------------
-- 3. LIVING BOMB (Debuff Bersaglio)
-- -------------------------------------------------------------------------

--- Genera il conto alla rovescia (%c): rosso vivo <= 3s prima dell'esplosione finale.
---@return string formattedTimer
function FireMageHUD_LivingBomb_CustomText()
    if not UnitExists("target") then return "" end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, unitCaster, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if (unitCaster == "player" or not unitCaster) and (spellId == 55360 or spellId == 55359 or spellId == 44457 or name == "Living Bomb" or name == "Bomba Vivente" or string.find(name, "Living Bomb") or string.find(name, "Vivente")) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 3 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end

-- -------------------------------------------------------------------------
-- 4. IGNITE (Debuff Bersaglio)
-- -------------------------------------------------------------------------

--- Genera il conto alla rovescia (%c): rosso vivo <= 1.5s, bianco con 1 decimale > 1.5s.
---@return string formattedTimer
function FireMageHUD_Ignite_CustomText()
    if not UnitExists("target") then return "" end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, unitCaster, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if (unitCaster == "player" or not unitCaster) and (spellId == 12654 or name == "Ignite" or name == "Ignizione" or string.find(name, "Ignite") or string.find(name, "Igniz")) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 1.5 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.1fs", rem)
                end
            end
        end
    end
    return ""
end

-- -------------------------------------------------------------------------
-- 5. SCORCH / IMPROVED SCORCH (Debuff Bersaglio)
-- -------------------------------------------------------------------------

--- Rileva se il debuff di Scorch è presente sul bersaglio corrente.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isDebuffPresent
function FireMageHUD_Scorch_Trigger(event, unit)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") or not UnitCanAttack("player", "target") then
        return false
    end
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or spellId == 22959 then
            return true
        end
    end
    return false
end

--- Fornisce la durata e la scadenza per lo swipe di Scorch.
---@return number duration, number expiration
function FireMageHUD_Scorch_Duration()
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or spellId == 22959 then
            return duration or 30, expirationTime or 0
        end
    end
    return 0, 0
end

--- Genera il conto alla rovescia (%c): rosso vivo <= 5s, bianco intero > 5s.
---@return string formattedTimer
function FireMageHUD_Scorch_CustomText()
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or spellId == 22959 then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem <= 5.0 then
                return string.format("|cFFFF4444%.1fs|r", rem)
            else
                return string.format("%.0fs", rem)
            end
        end
    end
    return ""
end

-- -------------------------------------------------------------------------
-- 6. COMBUSTION (Cooldown & Buff Attivo con Stack)
-- -------------------------------------------------------------------------

--- Gestione a 3 stati di Combustion: READY, ACTIVE con stacks, COOLDOWN (%c).
---@return string statusDescription
function FireMageHUD_Combustion_CustomText()
    -- 1. Controllo buff attivo sul giocatore
    local buffName = GetSpellInfo(28682) or "Combustion"
    for i = 1, 40 do
        local name, _, _, count, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == buffName or name == "Combustion" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            return string.format("COMBUSTION\n|cFF00FF00ACTIVE (x%d)|r %.1fs", count or 1, rem)
        end
    end

    -- 2. Controllo tempo di ricarica
    local start, duration = GetSpellCooldown(11129)
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Combustion")
    end

    if start and duration and start > 0 and duration > 1.5 then
        local remCD = (start + duration) - GetTime()
        if remCD > 0 then
            return string.format("COMBUSTION\n|cFFFF9900CD %.1fs|r", remCD)
        end
    end

    -- 3. Pronto all'uso
    return "COMBUSTION\n|cFF00FF00READY|r"
end

-- -------------------------------------------------------------------------
-- 7. MOLTEN FURY (Talento Execute Bersaglio <= 35% HP)
-- -------------------------------------------------------------------------

--- Rileva quando il bersaglio scende a vita <= 35% per la fase di Execute.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isExecuteActive
function FireMageHUD_MoltenFury_Trigger(event, unit)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") or not UnitCanAttack("player", "target") then
        return false
    end
    local max = UnitHealthMax("target") or 1
    if max <= 0 then return false end
    local cur = UnitHealth("target") or 0
    return (cur / max) * 100 <= 35.0
end

--- Disattiva l'indicatore se il bersaglio supera il 35% o muore.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isExecuteInactive
function FireMageHUD_MoltenFury_Untrigger(event, unit)
    return not FireMageHUD_MoltenFury_Trigger(event, unit)
end

--- Testo indicatore Execute (%c).
---@return string
function FireMageHUD_MoltenFury_CustomText()
    return "|cFFFF5500MOLTEN FURY\nEXECUTE PHASE|r"
end
