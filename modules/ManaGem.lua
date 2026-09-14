--- =========================================================================
--- Fire Mage HUD 3.3.5a — Modulo 06: Mana Gem (Gemma del Mana)
--- =========================================================================
--- Monitora la Gemma del Mana (Mana Sapphire / Mana Emerald, x = +110, y = -54):
--- - Visualizza il cooldown residuo (2 min) con swipe circolare al centro dell'icona.
--- - Conta in tempo reale le cariche disponibili (3, 2, 1) mostrate in basso a destra.
--- - Se le cariche sono esaurite o la gemma non è in borsa, mostra uno "0" rosso
---   per avvisare immediatamente di ri-evocare la gemma prima del fight.
--- =========================================================================

local MANA_SAPPHIRE_ID = 33312 -- Rank 6 (Livello 80)
local MANA_EMERALD_ID  = 22044 -- Rank 5 (Livello 70)

--- Restituisce il conteggio delle cariche disponibili in borsa (%c).
---@return string cariche (es. "3", "2", "1", oppure "|cFFFF22220|r")
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

--- Recupera i parametri di cooldown dell'oggetto per la barra/icona WeakAuras.
---@return number startTime Inizio del cooldown
---@return number duration Durata totale (120 secondi)
---@return number enable 1 se abilitato
function FireMageHUD_ManaGem_GetCooldown()
    local startTime, duration, enable = GetItemCooldown(MANA_SAPPHIRE_ID)
    if not startTime or startTime == 0 then
        startTime, duration, enable = GetItemCooldown(MANA_EMERALD_ID)
    end
    return startTime or 0, duration or 0, enable or 1
end
