--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 07: Barra del Mana
--- =========================================================================
--- Gestisce il monitoraggio in tempo reale della percentuale di Mana del Mago.
--- - Mostra unicamente la percentuale con due cifre decimali (es. "85.24%").
--- - Transizione cromatica dinamica: Blu standard tra 20% e 100%, Rosso vivo <= 20%.
--- =========================================================================

--- Trigger per l'aggiornamento del mana su eventi di potenza o ingresso nel mondo.
---@param event string Nome evento WoW
---@param unit string Unità associata all'evento
---@return boolean isValid Vero se l'evento riguarda il giocatore
function FireMageHUD_Mana_Trigger(event, unit)
    if event == "UNIT_POWER_UPDATE" or event == "UNIT_MANA" or event == "UNIT_MAXMANA" or event == "UNIT_MAXPOWER" then
        if unit ~= "player" then return false end
    end
    return true
end

--- Calcola i valori correnti e massimi per la barra grafica di avanzamento.
---@return number currentMana Mana attuale
---@return number maxMana Mana massimo
---@return boolean isStatic Vero per barre di stato standard
function FireMageHUD_Mana_Duration()
    local cur = UnitPower("player", 0) or UnitMana("player") or 0
    local max = UnitPowerMax("player", 0) or UnitManaMax("player") or 1
    return cur, max, true
end

--- Genera il testo personalizzato (%c) formattato come percentuale con due decimali.
---@return string Testo percentuale (es. "85.24%")
function FireMageHUD_Mana_CustomText()
    local cur = UnitPower("player", 0) or UnitMana("player") or 0
    local max = UnitPowerMax("player", 0) or UnitManaMax("player") or 1
    if max <= 0 then max = 1 end
    local pct = (cur / max) * 100

    return string.format("%.2f%%", pct)
end
