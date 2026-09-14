--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 09: Global Cooldown (GCD)
--- =========================================================================
--- Monitora il Global Cooldown (larghezza 264px, altezza 3px, yOffset = -12).
--- Utilizza la spell di riferimento standard WotLK 61304 (con fallback su Fire Blast).
--- Limita rigidamente il controllo a durate <= 1.5 secondi per isolare il vero GCD.
--- =========================================================================

--- Verifica se il Global Cooldown è attualmente in corso.
---@param event string Nome evento WoW
---@param unit? string Unità di riferimento
---@return boolean isGCDActive
function FireMageHUD_GCD_Trigger(event, unit)
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    return (start and duration and start > 0 and duration > 0 and duration <= 1.5) or false
end

--- Segnala la conclusione del Global Cooldown.
---@param event string Nome evento WoW
---@param unit? string Unità di riferimento
---@return boolean isGCDInactive
function FireMageHUD_GCD_Untrigger(event, unit)
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    return (not start) or (duration == 0) or (duration > 1.5)
end

--- Fornisce durata e scadenza per la barra grafica di avanzamento del GCD.
---@return number duration Durata del GCD (base 1.5s ridotta da Haste)
---@return number expiration Scadenza in secondi
---@return boolean isStatic
function FireMageHUD_GCD_Duration()
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    if start and duration and start > 0 and duration > 0 and duration <= 1.5 then
        return duration, start + duration, true
    end
    return 0, 0, true
end

--- Restituisce il valore numerico dei decimi di secondo rimanenti di GCD (%c).
---@return string formattedSeconds
function FireMageHUD_GCD_CustomText()
    local start, duration = GetSpellCooldown(61304)
    if not start or duration == 0 or duration > 1.5 then
        start, duration = GetSpellCooldown(42873)
    end
    if start and duration and start > 0 and duration > 0 and duration <= 1.5 then
        local rem = math.max(0, (start + duration) - GetTime())
        return string.format("%.1fs", rem)
    end
    return ""
end
