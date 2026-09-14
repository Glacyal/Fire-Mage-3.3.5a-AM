--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 07: Mirror Image (Copie & Proc T10 4P)
--- =========================================================================
--- Monitora le Copie (Mirror Image, 55342, x = +110, y = -54):
--- Collocata all'estremita' destra della riga utility simmetricamente a Trinket 1.
--- 
--- Funzionalita' e layout:
--- 1. Bonus Set T10 (4 pezzi - "Quad Core"):
---    - All'uso di Mirror Image, il set 4P T10 attiva "Quad Core" (ID 70747 / +18% danni per 30s).
---    - Mostra il Pixel Glow dorato ({1, 0.85, 0.1, 1}) e il conto alla rovescia attivo
---      con 1 decimale in giallo (%c).
---    - Negli ultimi 3 secondi di proc (rem <= 3.0s), il timer diventa rosso vivo (|cFFFF2222)
---      per avvisare dell'imminente chiusura della finestra di burst DPS.
---    - Se non si possiede il 4P T10, mostra comunque la durata attiva base (30s) con glow ciano.
--- 2. Cooldown Abilita' (3 min):
---    - Al termine dei 30s di copie/proc, interrompe il glow e commuta automaticamente
---      lo swipe e il timer sul cooldown residuo di Mirror Image (m:ss o secondi interi).
--- 3. Stato Pronto:
---    - Quando fuori cooldown, l'icona e' pulita e pronta per il prossimo cast.
--- =========================================================================

local MIRROR_IMAGE_SPELL_ID = 55342

--- Spell ID e nomi noti per il buff del bonus 4 pezzi T10 Mago ("Quad Core")
local T10_4P_BUFF_SPELL_IDS = {
    [70747] = true, -- Quad Core (+18% damage, 30s)
    [70748] = true, -- Quad Core (trigger/effect)
    [70754] = true, -- Item - Mage T10 4P Bonus
    [70752] = true, -- Item - Mage T10 2P/4P variant
}

local T10_4P_BUFF_NAMES = {
    ["Quad Core"]                = true,
    ["Item - Mage T10 4P Bonus"] = true,
}

--- ID degli oggetti del set Tier 10 Mago (Sanctified / Bloodmage's Regalia)
local T10_PIECE_ITEM_IDS = {
    -- Elmo: 251, 264, 277
    [50069] = true, [51159] = true, [51284] = true,
    -- Spalle: 251, 264, 277
    [50073] = true, [51155] = true, [51280] = true,
    -- Veste: 251, 264, 277
    [50070] = true, [51158] = true, [51283] = true,
    -- Guanti: 251, 264, 277
    [50071] = true, [51157] = true, [51282] = true,
    -- Gambe: 251, 264, 277
    [50072] = true, [51156] = true, [51281] = true,
}

--- Verifica se il giocatore ha equipaggiato almeno 4 pezzi del Tier 10.
---@return boolean hasT10
function FireMageHUD_MirrorImage_HasT10()
    local count = 0
    for _, slot in ipairs({1, 3, 5, 7, 10}) do
        local id = GetInventoryItemID("player", slot)
        if id and T10_PIECE_ITEM_IDS[id] then
            count = count + 1
        end
    end
    return count >= 4
end

--- Determina lo stato operativo corrente di Mirror Image (ACTIVE, COOLDOWN, READY).
---@return string state "ACTIVE" (proc T10 o copie attive), "COOLDOWN", "READY"
---@return number rem Tempo residuo in secondi
---@return number dur Durata totale associata (30s attivo o 180s CD)
---@return string icon Texture dell'icona
---@return boolean isT10 true se e' attivo il proc T10 4P
function FireMageHUD_MirrorImage_CheckState()
    local now = GetTime()
    local baseIcon = GetSpellTexture(MIRROR_IMAGE_SPELL_ID) or "Interface\\Icons\\Spell_Magic_LesserInvisibilty"
    local quadCoreIcon = GetSpellTexture(70747) or "Interface\\Icons\\Spell_Nature_Invisibilty"
    local hasT10 = FireMageHUD_MirrorImage_HasT10()

    -- 1. Controllo buff T10 4P ("Quad Core") o Mirror Image attivo sul giocatore
    for i = 1, 40 do
        local name, _, buffIcon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if (spellId and T10_4P_BUFF_SPELL_IDS[spellId]) or T10_4P_BUFF_NAMES[name] then
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or 0
            local dur = (duration and duration > 0) and duration or 30
            local icon = buffIcon or quadCoreIcon
            return "ACTIVE", rem, dur, icon, true
        elseif name == "Mirror Image" or name == "Immagine Speculare" or spellId == MIRROR_IMAGE_SPELL_ID then
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or 0
            local dur = (duration and duration > 0) and duration or 30
            local icon = hasT10 and (buffIcon or quadCoreIcon) or baseIcon
            return "ACTIVE", rem, dur, icon, hasT10
        end
    end

    -- 2. Controllo tempo di ricarica dell'abilita'
    local start, duration = GetSpellCooldown(MIRROR_IMAGE_SPELL_ID)
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Mirror Image")
    end
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Immagine Speculare")
    end

    if start and duration and start > 0 and duration > 1.5 then
        local elapsed = now - start
        -- Le copie durano 30 secondi: entro i 30s siamo in stato ACTIVE
        if elapsed >= 0 and elapsed < 30 then
            local remActive = 30 - elapsed
            -- Se il buff T10 non e' presente sul giocatore, mostrare SEMPRE l'icona base delle copie
            return "ACTIVE", remActive, 30, baseIcon, false
        else
            local remCD = (start + duration) - now
            if remCD > 0.1 then
                return "COOLDOWN", remCD, duration, baseIcon, false
            end
        end
    end

    -- 3. Pronta all'uso
    return "READY", 0, 0, baseIcon, false
end

--- Calcola durata e scadenza per lo swipe circolare di Mirror Image.
---@return number duration Durata totale (30s proc o 180s CD)
---@return number expirationTime Timestamp GetTime() di scadenza
function FireMageHUD_MirrorImage_CustomDuration()
    local state, rem, dur = FireMageHUD_MirrorImage_CheckState()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end

--- Genera il testo descrittivo (%c) e gestisce il Pixel Glow su proc T10 o copie attive.
---@return string formattedText Conto alla rovescia o stringa vuota se pronta
function FireMageHUD_MirrorImage_CustomText()
    local state, rem, dur, icon, isT10 = FireMageHUD_MirrorImage_CheckState()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)

    -- Aggiornamento immediato texture: Quad Core SOLO su proc T10 attivo, altrimenti SEMPRE Copie standard
    if aura_env and aura_env.region then
        local defIcon = GetSpellTexture(MIRROR_IMAGE_SPELL_ID) or "Interface\\Icons\\Spell_Magic_LesserInvisibilty"
        local targetIcon = (state == "ACTIVE" and isT10 and icon) and icon or defIcon
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

    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            if isT10 then
                -- Glow dorato intenso per proc 4P T10 (+18% danni)
                LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2)
            else
                -- Glow ciano per copie base
                LCG.PixelGlow_Start(aura_env.region, {0.2, 0.8, 1.0, 1}, 8, 0.25, 10, 2)
            end
        end
        if rem > 0 then
            if isT10 then
                if rem <= 3.0 then
                    return string.format("|cFFFF2222%.1fs|r", rem)
                else
                    return string.format("|cFFFFFF00%.1fs|r", rem)
                end
            else
                return string.format("|cFF33FFFF%.1fs|r", rem)
            end
        end
        return isT10 and "|cFFFFFF00T10|r" or "|cFF33FFFFON|r"
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
        if state == "COOLDOWN" and rem > 0.1 then
            if rem >= 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("%d:%02d", m, s)
            else
                return string.format("%.0f", rem)
            end
        end
        return ""
    end
end

--- Restituisce la texture icona appropriata.
---@return string iconPath
function FireMageHUD_MirrorImage_CustomIcon()
    local state, rem, dur, icon, isT10 = FireMageHUD_MirrorImage_CheckState()
    if state == "ACTIVE" and isT10 then
        return icon
    end
    return GetSpellTexture(MIRROR_IMAGE_SPELL_ID) or "Interface\\Icons\\Spell_Magic_LesserInvisibilty"
end

--- Restituisce i parametri di cooldown base dell'abilità per compatibilità legacy.
---@return number startTime Inizio del cooldown
---@return number duration Durata totale (180 secondi)
---@return number enable 1 se abilitato
function FireMageHUD_MirrorImage_GetCooldown()
    local startTime, duration, enable = GetSpellCooldown(MIRROR_IMAGE_SPELL_ID)
    return startTime or 0, duration or 0, enable or 1
end

