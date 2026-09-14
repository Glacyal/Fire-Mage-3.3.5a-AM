-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 03: Arcane Intellect / Arcane Brilliance
-- =========================================================================
-- Monitora la presenza di Intellect (Arcane Intellect, Arcane Brilliance,
-- Dalaran Intellect, Dalaran Brilliance, Fel Intelligence).
-- 1. Quando ATTIVA con durata > 5m: icona pulita, nessun testo timer.
-- 2. Quando ATTIVA con durata <= 5m: countdown m:ss in giallo (es. 4:59).
-- 3. Quando MANCANTE: icona desaturata con scritta "OFF" in rosso.
-- =========================================================================

local IntellectBuffs = {
    ["Arcane Intellect"] = true,
    ["Arcane Brilliance"] = true,
    ["Dalaran Intellect"] = true,
    ["Dalaran Brilliance"] = true,
    ["Fel Intelligence"] = true,
}

function FireMageHUD_IntellectActive_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if IntellectBuffs[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                return true
            end
            return false
        end
    end
    return false
end

function FireMageHUD_IntellectActive_Untrigger(event, unit)
    if unit and unit ~= "player" then return false end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if IntellectBuffs[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                return false
            end
            return true
        end
    end
    return true
end

function FireMageHUD_IntellectActive_CustomText()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if IntellectBuffs[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("|cFFFFFF00%d:%02d|r", m, s)
            end
            return "" -- Nessun testo quando il buff dura più di 5 minuti
        end
    end
    return ""
end

function FireMageHUD_IntellectOFF_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if IntellectBuffs[name] then
            return false -- Buff presente -> OFF è disattivato
        end
    end
    return true -- Buff assente -> Mostra OFF
end

function FireMageHUD_IntellectOFF_Untrigger(event, unit)
    return not FireMageHUD_IntellectOFF_Trigger(event, unit)
end

