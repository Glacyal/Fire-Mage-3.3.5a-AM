-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 04: Focus Magic Monitor
-- =========================================================================
-- Monitora in tempo reale lo stato di "Focus Magic" per il Mago:
-- - Posizionato sull'ala destra della HUD (xOffset = +155, yOffset = 0),
--   in perfetto equilibrio simmetrico con Molten Armor (xOffset = -155).
-- - Se Focus Magic e' ATTIVO / PROC sul giocatore:
--   mostra l'icona a colori con swipe di ricarica e conto alla rovescia (%p).
-- - Se Focus Magic NON E' APPLICATO a nessuno (né in raid/party né sul target/focus/player):
--   mostra l'icona desaturata grigia con indicazione sobria "OFF" come promemoria.
-- - Non appena Focus Magic viene APPLICATO ad un alleato in raid, party o target:
--   l'avviso "OFF" scompare completamente per mantenere la schermata pulita in raid!
-- =========================================================================

local FOCUS_MAGIC_BUFF = "Focus Magic"

-- =========================================================================
-- CONTROLLO GLOBALE APPLICAZIONE FOCUS MAGIC
-- =========================================================================
function FireMageHUD_HasFocusMagicApplied()
    -- 1. Controlla se il giocatore ha il buff o il proc attivo
    for i = 1, 40 do
        local n = UnitBuff("player", i)
        if not n then break end
        if n == FOCUS_MAGIC_BUFF then return true end
    end

    -- 2. Controlla sul bersaglio corrente (se amico)
    if UnitExists("target") and UnitIsFriend("player", "target") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("target", i)
            if not n then break end
            if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then return true end
        end
    end

    -- 3. Controlla sul focus (se amico)
    if UnitExists("focus") and UnitIsFriend("player", "focus") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("focus", i)
            if not n then break end
            if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then return true end
        end
    end

    -- 4. Controlla su tutti i membri del Raid (se in raid)
    local nr = GetNumRaidMembers()
    if nr and nr > 0 then
        for r = 1, nr do
            local u = "raid" .. r
            for i = 1, 40 do
                local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                if not n then break end
                if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then return true end
            end
        end
    else
        -- 5. Controlla sui membri del Party (se in gruppo)
        local np = GetNumPartyMembers()
        if np and np > 0 then
            for p = 1, np do
                local u = "party" .. p
                for i = 1, 40 do
                    local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                    if not n then break end
                    if n == FOCUS_MAGIC_BUFF and (c == "player" or not c) then return true end
                end
            end
        end
    end

    return false
end

-- =========================================================================
-- TRIGGER FOCUS MAGIC - OFF (Mostra icona grigia solo se NON applicato)
-- =========================================================================
function FireMageHUD_FocusMagic_OFF_Trigger()
    return not FireMageHUD_HasFocusMagicApplied()
end

function FireMageHUD_FocusMagic_OFF_Untrigger()
    return FireMageHUD_HasFocusMagicApplied()
end

-- =========================================================================
-- TRIGGER FOCUS MAGIC - ACTIVE (Mostra icona a colori se attivo su player)
-- =========================================================================
function FireMageHUD_FocusMagic_Active_Trigger()
    local name, _, icon, count, debuffType, duration, expirationTime = UnitBuff("player", FOCUS_MAGIC_BUFF)
    if name then
        return true, duration, expirationTime
    end
    return false
end
