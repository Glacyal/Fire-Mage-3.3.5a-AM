-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 04: Focus Magic Monitor
-- =========================================================================
-- Monitora in tempo reale lo stato di "Focus Magic" per il Mago:
-- - Posizionato sull'ala destra della HUD (xOffset = +155, yOffset = 0),
--   in perfetto equilibrio simmetrico con Molten Armor (xOffset = -155).
-- - Se Focus Magic e' ATTIVO / PROC:
--   mostra l'icona a colori con swipe di ricarica e conto alla rovescia (%p).
-- - Se Focus Magic NON E' APPLICATO / ASSENTE:
--   mostra l'icona desaturata grigia con indicazione sobria "OFF".
-- =========================================================================

local FOCUS_MAGIC_BUFF = "Focus Magic"

-- =========================================================================
-- TRIGGER FOCUS MAGIC (Buff / Proc sul Giocatore)
-- =========================================================================
function FireMageHUD_FocusMagic_Trigger()
    -- Controlla se il giocatore ha il buff o il proc di Focus Magic
    local name, _, icon, count, debuffType, duration, expirationTime = UnitBuff("player", FOCUS_MAGIC_BUFF)
    if name then
        return true, duration, expirationTime
    end
    return false
end
