--- =========================================================================
--- Fire Mage 3.3.5a AM — Modulo 12: Real-time Stats Panel (SP, Crit, Haste, Hit)
--- =========================================================================
--- Monitoraggio in tempo reale delle 4 statistiche fondamentali del Mago Fuoco:
--- - SP: Spell Power specifico per la scuola Fuoco (GetSpellBonusDamage(3))
--- - Crit: Critico incantesimi Fuoco (GetSpellCritChance(3)) con Molten Armor e talenti
--- - Haste: Celerita incantesimi (UnitSpellHaste o rating + moltiplicatori raid)
--- - Hit: Precisione incantesimi (Rating + Talento Precision + Draenei + Target Debuff)
--- =========================================================================

-- Cache interna per evitare scansioni ridondanti di talenti a ogni frame
local statCache = {
    lastTalentCheck = 0,
    precisionHit    = 0,
    isDraenei       = (select(2, UnitRace("player")) == "Draenei") and 1 or 0,
}

--- Trigger di aggiornamento del pannello statistiche
---@param event string Nome evento WoW
---@return boolean isValid Sempre true per mantenere attivo il pannello
function FireMageHUD_Stats_Trigger(event, ...)
    return true
end

--- Calcola e restituisce la stringa formattata con le 4 statistiche
---@return string Testo formattato su 4 righe con codici colore
function FireMageHUD_Stats_CustomText()
    -- 1. SPELL POWER (Scuola 3 = Fuoco)
    local sp = GetSpellBonusDamage(3) or 0
    sp = math.floor(sp + 0.5)

    -- 2. SPELL CRIT (Scuola 3 = Fuoco)
    -- Include crit base, intelletto, Molten Armor (con spirito e glifo), talenti e buff
    local crit = GetSpellCritChance(3) or 0

    -- Combustion (+10% Crit per carica se attivo)
    for i = 1, 40 do
        local bname, _, _, count, _, _, _, _, _, _, bId = UnitBuff("player", i)
        if not bname then break end
        if bId == 11129 or bname == "Combustion" then
            local stacks = (count and count > 0) and count or 1
            crit = crit + (stacks * 10)
            break
        end
    end

    -- 3. SPELL HASTE
    local ratingBonus = GetCombatRatingBonus(20) or 0
    local mult = 1 + (ratingBonus / 100)

    local hasLust = false
    local hasWrathAir = false
    local has3Haste = false
    local hasT10 = false
    local hasPI = false
    local hasBerserking = false

    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end

        -- 1. Bloodlust / Heroism (+30% Haste)
        if not hasLust and (spellId == 2825 or spellId == 32182 or name == "Bloodlust" or name == "Heroism" or name == "Bramosia Sanguinaria" or name == "Eroismo") then
            hasLust = true
            mult = mult * 1.30
        -- 2. Wrath of Air Totem (+5% Spell Haste Shamano)
        elseif not hasWrathAir and (spellId == 3738 or spellId == 2895 or name == "Wrath of Air Totem" or name == "Totem dell'Aria Furiosa" or (name.find and name:find("Wrath of Air"))) then
            hasWrathAir = true
            mult = mult * 1.05
        -- 3. 3% Raid Haste: Swift Retribution (Paladino) vs Improved Moonkin Form (Druido) - MAX ONCE (Anti-conflitto)
        elseif not has3Haste and (spellId == 48396 or spellId == 53648 or spellId == 53379 or spellId == 24907 or spellId == 31583
            or name == "Swift Retribution" or name == "Ritorsione Rapida" 
            or name == "Improved Moonkin Form" or name == "Forma di Lunagufo Migliorata") then
            has3Haste = true
            mult = mult * 1.03
        -- 4. Tier 10 2-Piece Bonus: Pushing the Limit (+12% Spell Haste per 5s)
        elseif not hasT10 and (spellId == 70753 or spellId == 70752 or name == "Pushing the Limit" or name == "Oltre il Limite") then
            hasT10 = true
            mult = mult * 1.12
        -- 5. Power Infusion (+20% Spell Haste Sacerdote)
        elseif not hasPI and (spellId == 10060 or name == "Power Infusion" or name == "Infusione di Potere") then
            hasPI = true
            mult = mult * 1.20
        -- 6. Berserking (+20% Haste Razziale Troll)
        elseif not hasBerserking and (spellId == 26297 or name == "Berserking" or name == "Furia Berserker") then
            hasBerserking = true
            mult = mult * 1.20
        end
    end

    local haste = (mult - 1) * 100

    -- 4. SPELL HIT
    local hitRatingBonus = GetCombatRatingBonus(8) or 0

    -- Aggiornamento talenti con throttling (ogni 10 secondi)
    local now = GetTime()
    if (now - statCache.lastTalentCheck) > 10 then
        statCache.lastTalentCheck = now
        local prec = 0
        for i = 1, 35 do
            local name, _, _, _, currentRank = GetTalentInfo(1, i)
            if not name then break end
            if name == "Precision" or name:find("Precision") then
                prec = currentRank or 0
                break
            end
        end
        statCache.precisionHit = prec
    end

    -- Razziale o Buff Draenei (+1% Hit)
    local draeneiHit = statCache.isDraenei
    if draeneiHit == 0 then
        for i = 1, 40 do
            local bname, _, _, _, _, _, _, _, _, _, bId = UnitBuff("player", i)
            if not bname then break end
            if bname == "Heroic Presence" or bId == 28878 or bId == 6562 then
                draeneiHit = 1
                break
            end
        end
    end

    -- 5. DEBUFF SUL TARGET NEMICO (Crit & Hit sul boss)
    local targetCritBonus = 0
    local targetHitBonus = 0
    local cfg = FireMageHUD_Config and FireMageHUD_Config.Stats
    local checkTarget = (cfg == nil) or (cfg.IncludeTargetHit ~= false)
    if checkTarget and UnitExists("target") and not UnitIsDead("target") and UnitCanAttack("player", "target") then
        local has5Crit = false
        local has3Crit = false
        local has3Hit = false

        for i = 1, 40 do
            local dname, _, _, _, _, _, _, _, _, _, dId = UnitDebuff("target", i)
            if not dname then break end

            -- +5% Spell Crit: Improved Scorch (22959, 12873, 12872), Shadow and Flame (17800), Winter's Chill (28593)
            if not has5Crit then
                if dId == 22959 or dId == 12873 or dId == 12872 or dId == 17800 or dId == 28593
                   or dname == "Improved Scorch" or dname == "Scorch" or dname == "Shadow and Flame"
                   or dname == "Winter's Chill" or string.find(dname, "Scorch") or string.find(dname, "Bruciatura") then
                    has5Crit = true
                    targetCritBonus = targetCritBonus + 5.0
                end
            end

            -- +3% All Crit: Heart of the Crusader (20337, 20336, 20335), Master Poisoner (58410), Totem of Wrath (30708, 30706)
            if not has3Crit then
                if dId == 20337 or dId == 20336 or dId == 20335 or dId == 58410 or dId == 30708 or dId == 30706
                   or dname == "Heart of the Crusader" or dname == "Cuore del Crociato"
                   or dname == "Master Poisoner" or dname == "Mastro Velenifero"
                   or dname == "Totem of Wrath" or dname == "Totem dell'Ira" then
                    has3Crit = true
                    targetCritBonus = targetCritBonus + 3.0
                end
            end

            -- +3% Spell Hit: Misery (33198, 33197, 33196), Faerie Fire / Imp Faerie Fire (770, 16857)
            if not has3Hit then
                if dId == 33198 or dId == 33197 or dId == 33196 or dId == 770 or dId == 16857
                   or dname == "Misery" or dname == "Miseria"
                   or dname == "Faerie Fire" or dname == "Fuoco Fatato" or string.find(dname, "Faerie Fire") then
                    has3Hit = true
                    targetHitBonus = targetHitBonus + 3.0
                end
            end

            if has5Crit and has3Crit and has3Hit then
                break
            end
        end
    end

    crit = crit + targetCritBonus
    local totalHit = hitRatingBonus + statCache.precisionHit + draeneiHit + targetHitBonus

    local hitText
    if totalHit >= 17.0 then
        hitText = string.format("|cFFFFFF00Hit:|r |cFFFFFFFF%.2f%%|r |cFF55FF55(Cap)|r", totalHit)
    else
        hitText = string.format("|cFFFFFF00Hit:|r |cFFFFFFFF%.2f%%|r", totalHit)
    end

    return string.format(
        "|cFFFF2222SP:|r |cFFFFFFFF%d|r\n|cFFFF8800Crit:|r |cFFFFFFFF%.2f%%|r\n|cFFCC44FFHaste:|r |cFFFFFFFF%.2f%%|r\n%s",
        sp, crit, haste, hitText
    )
end

-- ============================================================================
-- FRAME STANDALONE (Per utilizzo come AddOn indipendente senza WeakAuras)
-- ============================================================================
local cfg = (FireMageHUD_Config and FireMageHUD_Config.Stats) or {}
local statsFrame = CreateFrame("Frame", "FireMageHUD_StatsFrame", UIParent)
statsFrame:SetSize(cfg.Width or 88, cfg.Height or 48)
statsFrame:SetPoint("CENTER", UIParent, "CENTER", cfg.XOffset or -180, cfg.YOffset or -54)
statsFrame:SetBackdrop({
    bgFile = "Interface\\Buttons\\WHITE8X8",
    edgeFile = nil,
    tile = false,
    tileSize = 0,
    edgeSize = 0,
    insets = { left = 0, right = 0, top = 0, bottom = 0 }
})
statsFrame:SetBackdropColor(0.05, 0.05, 0.05, 0.85)

local statsText = statsFrame:CreateFontString(nil, "OVERLAY")
statsText:SetFont("Fonts\\FRIZQT__.TTF", 10, "OUTLINE")
statsText:SetPoint("LEFT", statsFrame, "LEFT", 4, 0)
statsText:SetJustifyH("LEFT")

local lastUpdate = 0
statsFrame:SetScript("OnUpdate", function(self, elapsed)
    lastUpdate = lastUpdate + elapsed
    if lastUpdate >= 0.25 then
        lastUpdate = 0
        statsText:SetText(FireMageHUD_Stats_CustomText())
    end
end)

statsFrame:RegisterEvent("PLAYER_ENTERING_WORLD")
statsFrame:RegisterEvent("UNIT_AURA")
statsFrame:RegisterEvent("COMBAT_RATING_UPDATE")
statsFrame:RegisterEvent("PLAYER_DAMAGE_DONE_MODS")
statsFrame:RegisterEvent("PLAYER_TARGET_CHANGED")
statsFrame:RegisterEvent("UNIT_INVENTORY_CHANGED")
statsFrame:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
statsFrame:SetScript("OnEvent", function(self, event, ...)
    statsText:SetText(FireMageHUD_Stats_CustomText())
end)

