--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 08: Castbar & Channeling
--- =========================================================================
--- Gestisce la Castbar centrale (larghezza 264px, yOffset = 0):
--- - Rileva sia lanci standard (UnitCastingInfo) che incantesimi canalizzati (UnitChannelInfo).
--- - Visualizza icona spell sul bordo sinistro, nome magia e tempo rimanente con 1 decimale.
--- =========================================================================

--- Rileva se il giocatore sta eseguendo un cast o una canalizzazione attiva.
---@param event string Nome evento
---@param unit? string Unità di riferimento
---@return boolean isCastingOrChanneling
function FireMageHUD_Castbar_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    return (UnitCastingInfo("player") ~= nil) or (UnitChannelInfo("player") ~= nil)
end

--- Disattiva la visualizzazione della barra al termine o interruzione del cast.
---@param event string Nome evento
---@param unit? string Unità di riferimento
---@return boolean isIdle
function FireMageHUD_Castbar_Untrigger(event, unit)
    if unit and unit ~= "player" then return false end
    return (UnitCastingInfo("player") == nil) and (UnitChannelInfo("player") == nil)
end

--- Restituisce durata e scadenza per la barra progressiva WeakAuras.
---@return number duration Durata totale in secondi
---@return number expiration Scadenza in secondi (GetTime)
---@return boolean normalOrder Vero per cast (0->max), Falso per canalizzazioni (max->0)
function FireMageHUD_Castbar_Duration()
    -- 1. Cast standard
    local spell, _, _, _, startTime, endTime = UnitCastingInfo("player")
    if spell and startTime and endTime then
        local duration = (endTime - startTime) / 1000
        local expiration = endTime / 1000
        return duration, expiration, true
    end

    -- 2. Channeling (es. Evocation, Blizzard)
    spell, _, _, _, startTime, endTime = UnitChannelInfo("player")
    if spell and startTime and endTime then
        local duration = (endTime - startTime) / 1000
        local expiration = endTime / 1000
        return duration, expiration, false
    end

    return 0, 0, true
end

--- Restituisce il nome dell'incantesimo in esecuzione.
---@return string spellName
function FireMageHUD_Castbar_Name()
    local spell = UnitCastingInfo("player") or UnitChannelInfo("player")
    return spell or ""
end

--- Restituisce la texture dell'icona dell'incantesimo in corso.
---@return string iconPath
function FireMageHUD_Castbar_Icon()
    local _, _, _, icon = UnitCastingInfo("player")
    if not icon then
        _, _, _, icon = UnitChannelInfo("player")
    end
    return icon or "Interface\\Icons\\Spell_Fire_Fireball02"
end

--- Restituisce il tempo residuo formattato per il subtext a destra (%c).
---@return string formattedTime
function FireMageHUD_Castbar_CustomTextTime()
    local spell, _, _, _, startTime, endTime = UnitCastingInfo("player")
    if spell and startTime and endTime then
        local now = GetTime() * 1000
        local remaining = math.max(0, (endTime - now) / 1000)
        return string.format("%.1f", remaining)
    end

    spell, _, _, _, startTime, endTime = UnitChannelInfo("player")
    if spell and startTime and endTime then
        local now = GetTime() * 1000
        local remaining = math.max(0, (endTime - now) / 1000)
        return string.format("%.1f", remaining)
    end

    return ""
end
