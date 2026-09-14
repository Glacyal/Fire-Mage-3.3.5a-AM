--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 06: Mana Gem (Gemma del Mana)
--- =========================================================================
--- Monitora la Gemma del Mana (Mana Sapphire / Mana Emerald, x = +22, y = -54):
--- Collocata nella riga utility tra Mantello (x = -22) e Combustion (x = +66).
--- 
--- Funzionalità e layout:
--- 1. Bonus Set T7 (2 pezzi):
---    - All'uso della gemma, attiva il buff "Improved Mana Gems" (+225 SP per 15s).
---    - Mostra il Pixel Glow dorato intorno all'icona (come per i monili) e
---      il conto alla rovescia attivo con 1 decimale a sud (%p).
--- 2. Cooldown Oggetto (2 min):
---    - Al termine del buff T7, interrompe il glow e commuta automaticamente
---      lo swipe e il timer a sud sul cooldown residuo della gemma (m:ss o secondi).
--- 3. Posizionamento e Anti-Sovrapposizione:
---    - Timer di scorrimento (%p): Ancorato in zona SUD (INNER_BOTTOM).
---    - Conteggio cariche (%c): Ancorato in ALTO A DESTRA (INNER_TOPRIGHT).
---    - Se le cariche sono esaurite o la gemma manca dalla borsa, mostra "0" rosso.
--- =========================================================================

local MANA_SAPPHIRE_ID = 33312 -- Rank 6 (Livello 80)
local MANA_EMERALD_ID  = 22044 -- Rank 5 (Livello 70)

--- Nomi e Spell ID associati al bonus 2 pezzi T7 del Mago (+225 Spell Power)
local T7_MANAGEM_BUFFS = {
    ["Mana Surge"]                = true,
    ["Improved Mana Gems"]        = true,
    ["Gemme di Mana Migliorate"]  = true,
    ["Gemme del Mana Migliorate"] = true,
    ["Gemma del Mana Migliorata"] = true,
    ["Ondata di Mana"]            = true,
}

local T7_MANAGEM_SPELLS = {
    [61062] = true,
    [37445] = true,
    [37446] = true,
    [37447] = true,
    [54043] = true,
}

--- Determina lo stato operativo corrente della Gemma del Mana (ACTIVE, COOLDOWN, READY).
---@return string state "ACTIVE" (buff T7 attivo), "COOLDOWN" (ricarica oggetto), "READY" (pronta)
---@return number rem Tempo residuo in secondi
---@return number dur Durata totale associata
---@return string icon Percorso della texture appropriata (Mana Surge o Gemma)
function FireMageHUD_ManaGem_CheckState()
    local now = GetTime()
    local baseIcon = "Interface\\Icons\\INV_Misc_Gem_Sapphire_02"

    -- 1. Controllo buff bonus 2 pezzi T7 attivo sul giocatore
    for i = 1, 40 do
        local n, _, icon, _, _, dur, exp, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if (spellId and T7_MANAGEM_SPELLS[spellId]) or (n and T7_MANAGEM_BUFFS[n]) then
            local rem = (exp and exp > now) and (exp - now) or 0
            if exp == 0 or exp == nil then
                rem = (dur and dur > 0) and dur or 15
            end
            if rem > 0.05 or exp == 0 or exp == nil then
                local totalDur = (dur and dur > 0) and dur or 15
                local procIcon = icon or GetSpellTexture(61062) or GetSpellTexture(37447) or "Interface\\Icons\\Spell_Arcane_ManaSurge" or "Interface\\Icons\\Spell_Holy_MagicalSentry"
                return "ACTIVE", rem, totalDur, procIcon
            end
        end
    end

    -- 2. Controllo cooldown dell'oggetto (Zaffiro o Smeraldo)
    local start, duration = GetItemCooldown(MANA_SAPPHIRE_ID)
    if not start or duration == 0 then
        start, duration = GetItemCooldown(MANA_EMERALD_ID)
    end
    if start and duration and duration > 1.5 and (start + duration) > now then
        local remCD = (start + duration) - now
        if remCD > 0.1 then
            return "COOLDOWN", remCD, duration, baseIcon
        end
    end

    -- 3. Pronta all'uso
    return "READY", 0, 0, baseIcon
end

--- Restituisce la texture appropriata per l'icona: Mana Surge durante il proc T7, Gemma del Mana altrimenti.
---@return string texturePath Percorso texture Blizzard Interface
function FireMageHUD_ManaGem_CustomIcon()
    local state, rem, dur, icon = FireMageHUD_ManaGem_CheckState()
    if state == "ACTIVE" and icon then
        return icon
    end
    return "Interface\\Icons\\INV_Misc_Gem_Sapphire_02"
end

--- Calcola durata e scadenza per lo swipe circolare e il progress timer (%p).
---@return number duration Durata totale dell'effetto o del cooldown
---@return number expirationTime Timestamp GetTime() di scadenza
function FireMageHUD_ManaGem_CustomDuration()
    local state, rem, dur, icon = FireMageHUD_ManaGem_CheckState()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end

--- Gestisce il Pixel Glow del proc T7, colora il timer a sud e restituisce le cariche (%c).
---@return string chargesText Numero cariche disponibili in borsa (es. "3", "2", "1", "|cFFFF22220|r")
function FireMageHUD_ManaGem_CustomText()
    local state, rem, dur, icon = FireMageHUD_ManaGem_CheckState()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)

    -- Gestione Pixel Glow dorato sul riquadro durante il proc attivo
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2)
        end
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
    end

    -- Aggiornamento immediato texture dell'icona: Mana Surge SOLO durante proc T7 attivo, altrimenti SEMPRE Gemma standard
    if aura_env and aura_env.region then
        local defIcon = "Interface\\Icons\\INV_Misc_Gem_Sapphire_02"
        local targetIcon = (state == "ACTIVE" and icon) and icon or defIcon
        if aura_env.region.icon and aura_env.region.icon.SetTexture then
            aura_env.region.icon:SetTexture(targetIcon)
        end
        if aura_env.region.SetIcon then
            aura_env.region:SetIcon(targetIcon)
        end
        if aura_env.state then
            aura_env.state.icon = targetIcon
        end
    end

    -- Aggiornamento colore dinamico del timer a sud (%p): Giallo su proc, Bianco su cooldown
    if aura_env and aura_env.region and aura_env.region.subRegions then
        local timerSub = aura_env.region.subRegions[2]
        if timerSub and timerSub.text and timerSub.text.SetTextColor then
            if state == "ACTIVE" then
                timerSub.text:SetTextColor(1, 0.9, 0.1, 1)
            else
                timerSub.text:SetTextColor(1, 1, 1, 1)
            end
        end
    end

    -- Conteggio cariche per la subRegion in alto a destra (%c)
    local c = GetItemCount(MANA_SAPPHIRE_ID, nil, true) or 0
    if c == 0 then
        c = GetItemCount(MANA_EMERALD_ID, nil, true) or 0
    end
    if c > 0 then
        return tostring(c)
    end
    return "|cFFFF22220|r"
end

--- Restituisce i parametri di cooldown base dell'oggetto per compatibilità legacy.
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
