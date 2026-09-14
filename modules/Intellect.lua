--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 03: Arcane Intellect / Brilliance
--- =========================================================================
--- Monitora la presenza del buff di Intelletto sul giocatore (x = -210, y = -14, sopra Stats Panel):
--- - Riconosce Arcane Intellect, Arcane Brilliance, Dalaran Brilliance e Fel Intelligence.
--- - Durata > 5 minuti: Completamente NASCOSTA per massima pulizia visiva.
--- - Durata <= 5 minuti: COMPARE con conto alla rovescia (m:ss giallo, ss rosso).
--- - Buff Assente / Scaduto: Mostra icona desaturata grigia con avviso rosso "OFF".
--- =========================================================================

local INTELLECT_BUFFS = {
    ["Arcane Intellect"]   = true,
    ["Arcane Brilliance"]  = true,
    ["Dalaran Intellect"]  = true,
    ["Dalaran Brilliance"] = true,
    ["Fel Intelligence"]   = true,
}

--- Rileva se un buff di Intelletto è attivo con durata residua <= 5 minuti (300s).
---@param event string Nome evento
---@param unit? string Unità
---@return boolean shouldDisplay
function FireMageHUD_IntellectActive_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if INTELLECT_BUFFS[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            return rem > 0 and rem <= 300
        end
    end
    return false
end

--- Disattiva lo stato Active se il buff è superiore a 5 minuti o rimosso.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean shouldHide
function FireMageHUD_IntellectActive_Untrigger(event, unit)
    return not FireMageHUD_IntellectActive_Trigger(event, unit)
end

--- Genera il testo del conto alla rovescia (%c) per durata <= 5 minuti.
---@return string formattedTime
function FireMageHUD_IntellectActive_CustomText()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if INTELLECT_BUFFS[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 60 and rem <= 300 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("|cFFFFFF00%d:%02d|r", m, s)
            elseif rem > 0 and rem <= 60 then
                return string.format("|cFFFF4444%.0fs|r", rem)
            end
            return ""
        end
    end
    return ""
end

--- Rileva l'assenza totale di qualsiasi variante del buff di Intelletto.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isMissing
function FireMageHUD_IntellectOFF_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if INTELLECT_BUFFS[name] then
            return false
        end
    end
    return true
end

--- Disattiva l'icona di allarme OFF al re-buff.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isPresent
function FireMageHUD_IntellectOFF_Untrigger(event, unit)
    return not FireMageHUD_IntellectOFF_Trigger(event, unit)
end

--- Testo di allerta per lo stato OFF (%c).
---@return string
function FireMageHUD_IntellectOFF_CustomText()
    return "|cFFFF2222OFF|r"
end
