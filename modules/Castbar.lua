-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 08: Castbar & Channeling
-- =========================================================================
-- Questo modulo gestisce la Castbar centrale per il Mago Fire.
-- Supporta sia i lanci standard (Cast) che le magie canalizzate (Channeling),
-- visualizzando icona, nome spell e tempo trascorso / rimanente (es. "1.63 / 2.00").
-- =========================================================================

-- =========================================================================
-- CUSTOM TRIGGER WEAKAURAS (Event-based)
-- =========================================================================
-- Eventi da inserire nel campo Events in /wa:
-- UNIT_SPELLCAST_START UNIT_SPELLCAST_STOP UNIT_SPELLCAST_FAILED UNIT_SPELLCAST_INTERRUPTED UNIT_SPELLCAST_DELAYED UNIT_SPELLCAST_CHANNEL_START UNIT_SPELLCAST_CHANNEL_UPDATE UNIT_SPELLCAST_CHANNEL_STOP PLAYER_ENTERING_WORLD

-- Custom Trigger Function:
function FireMageHUD_Castbar_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    
    local isCasting = UnitCastingInfo("player") ~= nil
    local isChanneling = UnitChannelInfo("player") ~= nil
    
    return isCasting or isChanneling
end

-- Custom Untrigger Function:
function FireMageHUD_Castbar_Untrigger(event, unit)
    if unit and unit ~= "player" then return false end
    return (UnitCastingInfo("player") == nil) and (UnitChannelInfo("player") == nil)
end

-- Custom Duration Function:
function FireMageHUD_Castbar_Duration()
    -- 1. Controllo Cast standard
    local spell, rank, displayName, icon, startTime, endTime = UnitCastingInfo("player")
    if spell and startTime and endTime then
        local duration = (endTime - startTime) / 1000
        local expiration = endTime / 1000
        return duration, expiration, true
    end

    -- 2. Controllo Channeling (es. Evocation, Blizzard)
    spell, rank, displayName, icon, startTime, endTime = UnitChannelInfo("player")
    if spell and startTime and endTime then
        local duration = (endTime - startTime) / 1000
        local expiration = endTime / 1000
        return duration, expiration, false -- false per inversione barra durante channeling
    end

    return 0, 0, true
end

-- Custom Name Info Function:
function FireMageHUD_Castbar_Name()
    local spell = UnitCastingInfo("player") or UnitChannelInfo("player")
    return spell or ""
end

-- Custom Icon Info Function:
function FireMageHUD_Castbar_Icon()
    local _, _, _, icon = UnitCastingInfo("player")
    if not icon then
        _, _, _, icon = UnitChannelInfo("player")
    end
    return icon or "Interface\\Icons\\Spell_Fire_Fireball02"
end

-- =========================================================================
-- TESTO PERSONALIZZATO (%c) PER TEMPO TRASCORSO / RIMANENTE
-- =========================================================================
-- Inserisci nel campo "Custom Function" per il testo secondario a destra (%c).
-- Esempio output: "1.63 / 2.00"

function FireMageHUD_Castbar_CustomTextTime()
    -- Cast Standard
    local spell, rank, displayName, icon, startTime, endTime = UnitCastingInfo("player")
    if spell and startTime and endTime then
        local now = GetTime() * 1000
        local total = (endTime - startTime) / 1000
        local elapsed = math.max(0, (now - startTime) / 1000)
        local remaining = math.max(0, (endTime - now) / 1000)
        return string.format("%.2f / %.2f", elapsed, total)
    end

    -- Channeling
    spell, rank, displayName, icon, startTime, endTime = UnitChannelInfo("player")
    if spell and startTime and endTime then
        local now = GetTime() * 1000
        local total = (endTime - startTime) / 1000
        local remaining = math.max(0, (endTime - now) / 1000)
        return string.format("%.2f / %.2f", remaining, total)
    end

    return ""
end

