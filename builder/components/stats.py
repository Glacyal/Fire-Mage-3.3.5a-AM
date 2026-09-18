"""
Modulo Componente: 18 - Stats Panel
===================================
Gestisce il pannello delle statistiche in tempo reale (88x48px a x = -190, y = -45):
- Mostra 4 righe di statistiche dinamiche calcolate all'istante:
  1. Spell Power (Fuoco)
  2. Spell Crit (Fuoco, con talenti, Combustion integrato da GetSpellCritChance(3), e debuff sul target come Scorch +5% e Totem +3%)
  3. Spell Haste (con Bloodlust, Totem Wrath of Air +5%, Swift Retrib +3%, Tier 10 2P +12%, PI, Berserking)
  4. Spell Hit (con rating, Precisione talento, presenza Draenei e Miseria/Faerie Fire +3% sul target, con indicatore verde Cap a 17%)
"""
from builder.core.constants import TEXTURE_WHITE8X8, FONT_EXPRESSWAY


# =============================================================================
# LOGICA LUA CONDIVISA: CALCOLO STATISTICHE DINAMICHE IN TEMPO REALE
# =============================================================================
def make_stats_bg_trigger() -> str:
    """Trigger di stato per il background del pannello statistiche."""
    return """function(event, ...)
    return true
end"""


def make_stats_bg_untrigger() -> str:
    """Untrigger per il background del pannello statistiche."""
    return """function(event, ...)
    return false
end"""


def make_stats_trigger() -> str:
    """Trigger per il testo dinamico del pannello statistiche."""
    return """function(event, ...)
    return true
end"""


def make_stats_untrigger() -> str:
    """Untrigger per il testo dinamico del pannello statistiche."""
    return """function(event, ...)
    return false
end"""


def make_stats_custom_text() -> str:
    """
    Funzione Lua personalizzata che calcola e formatta in tempo reale:
    Spell Power, Crit Fuoco, Haste Totale e Hit con verifica Cap a 17%.
    """
    return """function()
    local now = GetTime()
    if _G.FMHUD_LastStatsText and (now - (_G.FMHUD_LastStatsTime or 0)) < 0.1 then
        return _G.FMHUD_LastStatsText
    end

    -- 1. SPELL POWER (Fire School = 3)
    local sp = GetSpellBonusDamage(3) or 0
    sp = math.floor(sp + 0.5)

    -- 2. SPELL CRIT (Fire School = 3)
    local crit = GetSpellCritChance(3) or 0

    -- 3. SPELL HASTE & HIT BUFFS (Scansione in singolo passaggio di UnitBuff)
    local ratingBonus = GetCombatRatingBonus(20) or 0
    local mult = 1 + (ratingBonus / 100)

    local hasCombustion = false
    local hasLust = false
    local hasWrathAir = false
    local has3Haste = false
    local hasT10 = false
    local hasPI = false
    local hasBerserking = false
    local hasHeroicPresence = false

    for i = 1, 40 do
        local name, _, _, count, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end

        -- Combustion (SpellID 11129): GetSpellCritChance(3) include già nativamente
        -- il bonus di critico del buff (+10% per stack) allo stesso modo di Molten Armor.
        -- Non va quindi sommato manualmente per evitare un doppio conteggio.
        if not hasCombustion and (spellId == 11129 or name == "Combustion" or name == "Combustione") then
            hasCombustion = true
        end

        -- Bloodlust / Heroism (+30% Haste)
        if not hasLust and (spellId == 2825 or spellId == 32182 or name == "Bloodlust" or name == "Heroism" or name == "Bramosia Sanguinaria" or name == "Eroismo") then
            hasLust = true
            mult = mult * 1.30
        -- Wrath of Air Totem (+5% Spell Haste Shamano)
        elseif not hasWrathAir and (spellId == 3738 or spellId == 2895 or name == "Wrath of Air Totem" or name == "Totem dell'Aria Furiosa" or name:find("Wrath of Air")) then
            hasWrathAir = true
            mult = mult * 1.05
        -- 3% Raid Haste: Swift Retribution (Paladino) vs Improved Moonkin Form (Druido) - MAX ONCE
        elseif not has3Haste and (spellId == 48396 or spellId == 53648 or spellId == 53379 or spellId == 24907 or spellId == 31583
            or name == "Swift Retribution" or name == "Ritorsione Rapida" 
            or name == "Improved Moonkin Form" or name == "Forma di Lunagufo Migliorata") then
            has3Haste = true
            mult = mult * 1.03
        -- Tier 10 2-Piece Bonus: Pushing the Limit (+12% Spell Haste per 5s)
        elseif not hasT10 and (spellId == 70753 or spellId == 70752 or name == "Pushing the Limit" or name == "Oltre il Limite") then
            hasT10 = true
            mult = mult * 1.12
        -- Power Infusion (+20% Spell Haste Sacerdote)
        elseif not hasPI and (spellId == 10060 or name == "Power Infusion" or name == "Infusione di Potere") then
            hasPI = true
            mult = mult * 1.20
        -- Berserking (+20% Haste Razziale Troll)
        elseif not hasBerserking and (spellId == 26297 or name == "Berserking" or name == "Furia Berserker") then
            hasBerserking = true
            mult = mult * 1.20
        end

        -- Heroic Presence (Draenei aura)
        if not hasHeroicPresence and (name == "Heroic Presence" or spellId == 28878 or spellId == 6562) then
            hasHeroicPresence = true
        end
    end

    local haste = (mult - 1) * 100

    -- 4. SPELL HIT
    local hitRatingBonus = GetCombatRatingBonus(8) or 0

    _G.FMHUD_StatCache = _G.FMHUD_StatCache or {
        lastTalentCheck = 0,
        precisionHit = 0,
        isDraenei = (select(2, UnitRace("player")) == "Draenei") and 1 or 0,
    }
    if (now - _G.FMHUD_StatCache.lastTalentCheck) > 10 then
        _G.FMHUD_StatCache.lastTalentCheck = now
        local prec = 0
        for i = 1, 35 do
            local name, _, _, _, currentRank = GetTalentInfo(1, i)
            if not name then break end
            if name == "Precision" or name:find("Precision") then
                prec = currentRank or 0
                break
            end
        end
        _G.FMHUD_StatCache.precisionHit = prec
    end

    local draeneiHit = (_G.FMHUD_StatCache.isDraenei == 1 or hasHeroicPresence) and 1 or 0

    -- 5. TARGET DEBUFFS (Crit & Hit on target / boss)
    local targetCritBonus = 0
    local targetHitBonus = 0
    if UnitExists("target") and not UnitIsDead("target") and UnitCanAttack("player", "target") then
        local has5Crit = false
        local has3Crit = false
        local has3Hit = false

        for i = 1, 40 do
            local dname, _, _, _, _, _, _, _, _, _, dId = UnitDebuff("target", i)
            if not dname then break end

            -- +5% Spell Crit: Improved Scorch, Shadow and Flame, Winter's Chill
            if not has5Crit then
                if dId == 22959 or dId == 12873 or dId == 12872 or dId == 17800 or dId == 28593
                   or dname == "Improved Scorch" or dname == "Scorch" or dname == "Shadow and Flame"
                   or dname == "Winter's Chill" or string.find(dname, "Scorch") or string.find(dname, "Bruciatura") then
                    has5Crit = true
                    targetCritBonus = targetCritBonus + 5.0
                end
            end

            -- +3% All Crit: Heart of the Crusader, Master Poisoner, Totem of Wrath
            if not has3Crit then
                if dId == 20337 or dId == 20336 or dId == 20335 or dId == 58410 or dId == 30708 or dId == 30706
                   or dname == "Heart of the Crusader" or dname == "Cuore del Crociato"
                   or dname == "Master Poisoner" or dname == "Mastro Velenifero"
                   or dname == "Totem of Wrath" or dname == "Totem dell'Ira" then
                    has3Crit = true
                    targetCritBonus = targetCritBonus + 3.0
                end
            end

            -- +3% Spell Hit: Misery, Faerie Fire / Improved Faerie Fire
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
    local totalHit = hitRatingBonus + _G.FMHUD_StatCache.precisionHit + draeneiHit + targetHitBonus

    local hitText
    if totalHit >= 17.0 then
        hitText = string.format("|cFFFFFF00Hit:|r |cFFFFFFFF%.2f%%|r |cFF55FF55(Cap)|r", totalHit)
    else
        hitText = string.format("|cFFFFFF00Hit:|r |cFFFFFFFF%.2f%%|r", totalHit)
    end

    local out = string.format(
        "|cFFFF2222SP:|r |cFFFFFFFF%d|r\\n|cFFFF8800Crit:|r |cFFFFFFFF%.2f%%|r\\n|cFFCC44FFHaste:|r |cFFFFFFFF%.2f%%|r\\n%s",
        sp, crit, haste, hitText
    )
    _G.FMHUD_LastStatsTime = now
    _G.FMHUD_LastStatsText = out
    return out
end"""


# =============================================================================
# BUILDER: AURE WEAKAURAS PER IL PANNELLO STATISTICHE
# =============================================================================
def build_stats_auras() -> list[dict]:
    """
    Costruisce e restituisce le 3 aure che compongono il componente Stats Panel:
    - 18 - Stats Panel (Group)
    - Stats Panel - Background (Texture 88x48px)
    - Stats Panel - Text (Text con le 4 righe formattate)
    """
    return [
        {
            "id": "18 - Stats Panel",
            "uid": "FMHUD_STATS_GRP",
            "parent": "Fire Mage 3.3.5a AM",
            "regionType": "group",
            "internalVersion": 52,
            "xOffset": -190,
            "yOffset": -45,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "controlledChildren": [
                "Stats Panel - Background",
                "Stats Panel - Text",
            ],
        },
        {
            "id": "Stats Panel - Background",
            "uid": "FMHUD_STATS_BG",
            "parent": "18 - Stats Panel",
            "regionType": "texture",
            "internalVersion": 52,
            "xOffset": 0,
            "yOffset": 0,
            "width": 88,
            "height": 48,
            "texture": TEXTURE_WHITE8X8,
            "color": [0.05, 0.05, 0.05, 0.85],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "PLAYER_ENTERING_WORLD",
                        "custom": make_stats_bg_trigger(),
                    },
                    "untrigger": {
                        "custom": make_stats_bg_untrigger()
                    }
                },
                "activeTriggerMode": -10,
            },
        },
        {
            "id": "Stats Panel - Text",
            "uid": "FMHUD_STATS_TXT",
            "parent": "18 - Stats Panel",
            "regionType": "text",
            "internalVersion": 52,
            "xOffset": 2,
            "yOffset": 0,
            "width": 84,
            "height": 46,
            "displayText": "%c",
            "customTextUpdate": "update",
            "customText": make_stats_custom_text(),
            "fontSize": 10,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "LEFT",
            "color": [1, 1, 1, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "UNIT_AURA,COMBAT_RATING_UPDATE,PLAYER_DAMAGE_DONE_MODS,PLAYER_ENTERING_WORLD,UNIT_INVENTORY_CHANGED,PLAYER_EQUIPMENT_CHANGED,PLAYER_TARGET_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,CHARACTER_POINTS_CHANGED",
                        "custom": make_stats_trigger(),
                    },
                    "untrigger": {
                        "custom": make_stats_untrigger()
                    }
                },
                "activeTriggerMode": -10,
            },
        },
    ]


# =============================================================================
# NOTA CORREZIONE CALCOLO STATISTICHE (FIX 4):
# - Correzione Doppio Conteggio Critico Combustion:
#   In World of Warcraft 3.3.5a, la funzione nativa GetSpellCritChance(3) include
#   già nella percentuale restituita tutti gli aura-mod attivi del giocatore per
#   la scuola Fuoco (come Molten Armor e Combustion). Sommare manualmente
#   (stacks * 10) causava un raddoppio fittizio dell'incremento di critico (+20%,
#   +40%, +60% invece di +10%, +20%, +30%). Con questa modifica, il valore mostrato
#   nel pannello FMHUD rimane perfettamente coerente con la scheda del personaggio.
# =============================================================================
