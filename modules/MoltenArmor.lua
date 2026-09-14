--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 02: Molten Armor (Monitor Colonna Sinistra)
--- =========================================================================
--- Regole di visualizzazione per Molten Armor (x = -180, y = -14, sopra Stats Panel):
--- 1. Durata > 5 minuti: Completamente NASCOSTA per pulizia visiva in combattimento.
--- 2. Durata <= 5 minuti: COMPARE automaticamente con conto alla rovescia (m:ss o ss)
---    e swipe orologio per consentire il re-buff tempestivo.
--- 3. Buff Assente / Scaduto: Mostra l'icona desaturata grigia con allarme rosso "OFF".
--- =========================================================================

local MOLTEN_ARMOR_NAME = "Molten Armor"
local MOLTEN_ARMOR_ID = 43046

--- Rileva la presenza di Molten Armor con durata residua <= 5 minuti (300 sec).
---@param event string Nome evento
---@param unit? string Unità
---@return boolean shouldDisplay
function FireMageHUD_MoltenArmorActive_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wanted = GetSpellInfo(MOLTEN_ARMOR_ID) or MOLTEN_ARMOR_NAME

    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == MOLTEN_ARMOR_NAME then
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
function FireMageHUD_MoltenArmorActive_Untrigger(event, unit)
    return not FireMageHUD_MoltenArmorActive_Trigger(event, unit)
end

--- Fornisce durata e scadenza per lo swipe circolare WeakAuras.
---@return number duration Durata di riferimento (30 min)
---@return number expiration Scadenza in secondi
---@return boolean isStatic
function FireMageHUD_MoltenArmorActive_Duration()
    local wanted = GetSpellInfo(MOLTEN_ARMOR_ID) or MOLTEN_ARMOR_NAME
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == MOLTEN_ARMOR_NAME then
            return duration or 1800, expirationTime or (GetTime() + 1800), true
        end
    end
    return 0, 0, true
end

--- Genera il testo personalizzato (%c) per lo stato attivo sotto i 5 minuti.
--- Mostra m:ss in giallo se > 60s, oppure secondi interi in rosso se <= 60s.
---@return string formattedTime
function FireMageHUD_MoltenArmorActive_CustomText()
    local wanted = GetSpellInfo(MOLTEN_ARMOR_ID) or MOLTEN_ARMOR_NAME
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == MOLTEN_ARMOR_NAME then
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

--- Attiva lo stato OFF (icona grigia desaturata) quando Molten Armor è assente.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isMissing
function FireMageHUD_MoltenArmorOFF_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wanted = GetSpellInfo(MOLTEN_ARMOR_ID) or MOLTEN_ARMOR_NAME

    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wanted or name == MOLTEN_ARMOR_NAME then
            return false
        end
    end
    return true
end

--- Disattiva lo stato OFF quando il buff viene riapplicato.
---@param event string Nome evento
---@param unit? string Unità
---@return boolean isPresent
function FireMageHUD_MoltenArmorOFF_Untrigger(event, unit)
    return not FireMageHUD_MoltenArmorOFF_Trigger(event, unit)
end

--- Testo di allerta per lo stato OFF (%c).
---@return string
function FireMageHUD_MoltenArmorOFF_CustomText()
    return "|cFFFF2222OFF|r"
end
