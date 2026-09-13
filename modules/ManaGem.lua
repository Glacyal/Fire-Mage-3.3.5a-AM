-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 06: Mana Gem (Gemma del Mana)
-- =========================================================================
-- Monitora in tempo reale la Gemma del Mana (Mana Sapphire / Mana Emerald):
-- - Posizionato nella riga delle utility sotto la barra del Mana (x = +51, y = -48).
-- - Timer di Cooldown: visualizza il countdown (%p) e lo swipe circolare quando in ricarica (2 min).
-- - Cariche Rimanenti: visualizza in basso a destra il numero di cariche rimaste (3, 2, 1) tramite %c.
-- - Allarme Cariche Esaurite: se le cariche sono 0 o non hai gemme in borsa, mostra uno "0" rosso
--   per ricordarti immediatamente di evocare una nuova gemma!
-- =========================================================================

local MANA_SAPPHIRE_ID = 33312 -- Livello 80 (Rank 6)
local MANA_EMERALD_ID  = 22044 -- Livello 70 (Rank 5)

-- =========================================================================
-- CUSTOM TEXT FUNZIONE PER LE CARICHE (%c)
-- =========================================================================
function FireMageHUD_ManaGem_Charges_CustomText()
    local c = GetItemCount(MANA_SAPPHIRE_ID, nil, true) or 0
    if c == 0 then
        c = GetItemCount(MANA_EMERALD_ID, nil, true) or 0
    end
    if c > 0 then
        return tostring(c)
    end
    return "|cFFFF22220|r"
end

-- =========================================================================
-- CONTROLLO COOLDOWN GEMMA DEL MANA
-- =========================================================================
function FireMageHUD_ManaGem_GetCooldown()
    local startTime, duration, enable = GetItemCooldown(MANA_SAPPHIRE_ID)
    if not startTime or startTime == 0 then
        startTime, duration, enable = GetItemCooldown(MANA_EMERALD_ID)
    end
    return startTime or 0, duration or 0, enable or 1
end
