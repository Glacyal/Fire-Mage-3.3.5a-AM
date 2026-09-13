-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 02: Molten Armor (Monitor Permanente)
-- =========================================================================
-- Molten Armor è un buff fondamentale per il Mago Fire (critico + spirito).
-- Questo modulo rimane SEMPRE VISIBILE:
-- 1. Quando ATTIVA: mostra icona, nome "MOLTEN ARMOR" e durata residua (es. 12m 32s).
-- 2. Quando NON ATTIVA: mostra allerta visiva "MOLTEN ARMOR OFF / WARNING" con icona desaturata.
-- =========================================================================

-- =========================================================================
-- PARTE 1: AURA "Molten Armor - Active" (Icona o Testo)
-- =========================================================================
-- Tipo: Custom Event Trigger
-- Eventi: UNIT_AURA PLAYER_ENTERING_WORLD

function FireMageHUD_MoltenArmorActive_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    
    -- Scansione buff sul player per Molten Armor (Rank 1, 2, 3 o Nome)
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return true
        end
    end
    return false
end

function FireMageHUD_MoltenArmorActive_Untrigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return false
        end
    end
    return true
end

-- Custom Duration Function (Active):
function FireMageHUD_MoltenArmorActive_Duration()
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return duration or 1800, expirationTime or (GetTime() + 1800), true
        end
    end
    return 0, 0, true
end

-- Custom Text Function (%c per stato attivo):
function FireMageHUD_MoltenArmorActive_CustomText()
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem >= 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("MOLTEN ARMOR\n%dm %02ds", m, s)
            else
                return string.format("MOLTEN ARMOR\n%.1fs", rem)
            end
        end
    end
    return "MOLTEN ARMOR\nACTIVE"
end


-- =========================================================================
-- PARTE 2: AURA "Molten Armor - OFF" (Avviso Permanente Buff Mancante)
-- =========================================================================
-- Tipo: Custom Event Trigger
-- Eventi: UNIT_AURA PLAYER_ENTERING_WORLD PLAYER_REGEN_DISABLED PLAYER_REGEN_ENABLED

function FireMageHUD_MoltenArmorOFF_Trigger(event, unit)
    if unit and unit ~= "player" then return false end
    
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return false -- Buff presente -> NON triggerare lo stato OFF
        end
    end
    return true -- Buff ASSENTE -> TRIGGERA lo stato OFF
end

function FireMageHUD_MoltenArmorOFF_Untrigger(event, unit)
    if unit and unit ~= "player" then return false end
    local wantedName = GetSpellInfo(43046) or "Molten Armor"
    for i = 1, 40 do
        local name = UnitBuff("player", i)
        if not name then break end
        if name == wantedName or name == "Molten Armor" then
            return true -- Buff riapplicato -> Disattiva lo stato OFF
        end
    end
    return false
end

-- Custom Text Function (%c per stato OFF):
function FireMageHUD_MoltenArmorOFF_CustomText()
    return "|cFFFF2222MOLTEN ARMOR OFF\nWARNING!|r"
end

-- Nota: Per l'Aura OFF in /wa, imposta:
-- 1. Display > Desaturate Icon (Spunta attivata)
-- 2. Display > Color: Rosso chiaro o Bordo Rosso
-- 3. Animations > Main: Preset "Pulse" o "Flash" per massima visibilità in combattimento

