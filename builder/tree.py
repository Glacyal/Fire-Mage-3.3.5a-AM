import copy
from builder.lua_scripts import *

FIRE_MAGE_LOAD = {
    "use_class": True,
    "class": { "single": "MAGE", "multi": { "MAGE": True } },
    "use_talent": True,
    "talent": { "single": 68, "multi": { 68: True } },
    "use_vehicle": False,
}

def build_wa_tree() -> dict:
    """Costruisce e restituisce l'albero gerarchico completo delle 28 aure per WeakAuras 4.0.0 (internalVersion 52)."""
    data = {
        "m": "d",
        "v": 2000,
        "w": "4.0.0",
        "d": {
            "id": "Fire Mage 3.3.5a AM",
            "uid": "FMHUD_ROOT",
            "regionType": "group",
            "internalVersion": 52,
            "scale": 1.2,
            "xOffset": 0,
            "yOffset": -190,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "groupIcon": "Interface\\Icons\\Spell_Fire_FlameBolt",
            "displayIcon": "Interface\\Icons\\Spell_Fire_FlameBolt",
            "icon": "Interface\\Icons\\Spell_Fire_FlameBolt",
            "controlledChildren": [
                "01 - Procs",
                "02 - Molten Armor",
                "03 - Arcane Intellect",
                "04 - Focus Magic",
                "05 - Trinket 1",
                "05 - Trinket 2",
                "06 - Cloak",
                "06 - Tier 8",
                "06 - Mana Gem",
                "06 - Combustion",
                "06 - Mirror Image",
                "07 - Mana Bar",
                "10 - Hot Streak Bar",
                "08 - Castbar",
                "10 - Alerts",
                "12 - Stats Panel"
            ],
            "load": copy.deepcopy(FIRE_MAGE_LOAD)
        },
        "c": [
            # =================================================================
            # 01 - PROCS (Dynamic Group)
            # =================================================================
            {
                "id": "01 - Procs",
                "uid": "FMHUD_PROCS_DG",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "dynamicgroup",
                "internalVersion": 52,
                "grow": "HORIZONTAL",
                "align": "CENTER",
                "space": 6,
                "xOffset": 0,
                "yOffset": 52,
                "controlledChildren": [
                    "Tier 10",
                    "Hot Streak",
                    "Clearcasting",
                    "Living Bomb",
                    "Ignite",
                    "Scorch",
                    "Molten Fury"
                ],
            },
            # Tier 10 (Pushing the Limit +12% Haste buff - Active on proc, left of Hot Streak)
            {
                "id": "Tier 10",
                "uid": "FMHUD_TIER10_PROC",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_ElementalDevastation",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 70753 or spellId == 70752 or name == "Pushing the Limit" or name == "Oltre il Limite" or string.find(name, "Limit") or string.find(name, "Limite") then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 3 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": [
                                "Pushing the Limit",
                                "70753",
                                "70752",
                                "Oltre il Limite"
                            ],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                    {
                        "type": "subglow",
                        "glow": True,
                        "glowType": "Pixel",
                        "glowLines": 8,
                        "glowFrequency": 0.25,
                        "glowLength": 10,
                        "glowThickness": 2,
                    }
                ],
            },
            # Hot Streak (Active on proc)
            {
                "id": "Hot Streak",
                "uid": "FMHUD_HOTSTREAK",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Ability_Mage_HotStreak",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 48108 or name == "Hot Streak" or name == "Buona sorte" or string.find(name, "Hot Streak") or string.find(name, "Buona") then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 3 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": [
                                "Hot Streak",
                                "48108",
                                "Buona sorte"
                            ],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                    {
                        "type": "subglow",
                        "glow": True,
                        "glowType": "Pixel",
                        "glowLines": 8,
                        "glowFrequency": 0.25,
                        "glowLength": 10,
                        "glowThickness": 2,
                    }
                ],
            },
            # Clearcasting / Arcane Concentration (Active on proc)
            {
                "id": "Clearcasting",
                "uid": "FMHUD_CLEARCASTING",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Shadow_ManaBurn",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 12536 or name == "Clearcasting" or name == "Arcane Concentration" or name == "Lancio limpido" or name == "Concentrazione Arcana" or string.find(name, "Clearcasting") or string.find(name, "Limpido") or string.find(name, "Concentrat") then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 4 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": [
                                "Clearcasting",
                                "Arcane Concentration",
                                "Lancio limpido",
                                "Concentrazione Arcana",
                                "12536"
                            ],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                    {
                        "type": "subglow",
                        "glow": True,
                        "glowType": "Pixel",
                        "glowLines": 8,
                        "glowFrequency": 0.25,
                        "glowLength": 10,
                        "glowThickness": 2,
                    }
                ],
            },
            # Living Bomb (Target Debuff)
            {
                "id": "Living Bomb",
                "uid": "FMHUD_LIVINGBOMB",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Ability_Mage_LivingBomb",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    if not UnitExists("target") then return "" end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, unitCaster, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if (unitCaster == "player" or not unitCaster) and (spellId == 55360 or spellId == 55359 or spellId == 44457 or name == "Living Bomb" or name == "Bomba Vivente" or string.find(name, "Living Bomb") or string.find(name, "Vivente")) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 3 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "target",
                            "auranames": [
                                "Living Bomb",
                                "55360",
                                "55359",
                                "44457",
                                "Bomba Vivente"
                            ],
                            "useName": True,
                            "debuffType": "HARMFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },
            # Ignite (Target Debuff)
            {
                "id": "Ignite",
                "uid": "FMHUD_IGNITE",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_Incinerate",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    if not UnitExists("target") then return "" end
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, unitCaster, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if (unitCaster == "player" or not unitCaster) and (spellId == 12654 or name == "Ignite" or name == "Ignizione" or string.find(name, "Ignite") or string.find(name, "Igniz")) then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 1.5 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.1fs", rem)
                end
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "target",
                            "auranames": [
                                "Ignite",
                                "12654",
                                "Ignizione"
                            ],
                            "useName": True,
                            "debuffType": "HARMFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },
            # Scorch / Improved Scorch (Target Debuff)
            {
                "id": "Scorch",
                "uid": "FMHUD_SCORCH",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_SoulBurn",
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    if not UnitExists("target") then return "" end
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 22959 or spellId == 12873 or spellId == 12872 or spellId == 17800 or name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or string.find(name, "Scorch") or string.find(name, "Bruciatura") then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 then
                if rem <= 5 then
                    return string.format("|cFFFF4444%.1fs|r", rem)
                else
                    return string.format("%.0fs", rem)
                end
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_ENTERING_WORLD",
                            "custom": """function(event, ...)
    if not UnitExists("target") then return false end
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 22959 or spellId == 12873 or spellId == 12872 or spellId == 17800 or name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or string.find(name, "Scorch") or string.find(name, "Bruciatura") then
            return true
        end
    end
    return false
end""",
                            "customDuration": """function()
    if not UnitExists("target") then return 0, 0 end
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 22959 or spellId == 12873 or spellId == 12872 or spellId == 17800 or name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or string.find(name, "Scorch") or string.find(name, "Bruciatura") then
            return duration or 30, expirationTime or (GetTime() + 30)
        end
    end
    return 0, 0
end""",
                            "customIcon": """function()
    if not UnitExists("target") then return "Interface\\\\Icons\\\\Spell_Fire_SoulBurn" end
    for i = 1, 40 do
        local name, _, icon, _, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 22959 or spellId == 12873 or spellId == 12872 or spellId == 17800 or name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or string.find(name, "Scorch") or string.find(name, "Bruciatura") then
            return icon or "Interface\\\\Icons\\\\Spell_Fire_SoulBurn"
        end
    end
    return "Interface\\\\Icons\\\\Spell_Fire_SoulBurn"
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    if not UnitExists("target") then return true end
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 22959 or spellId == 12873 or spellId == 12872 or spellId == 17800 or name == "Improved Scorch" or name == "Scorch" or name == "Shadow and Flame" or string.find(name, "Scorch") or string.find(name, "Bruciatura") then
            return false
        end
    end
    return true
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },
            # Molten Fury (Target <= 35% HP)
            {
                "id": "Molten Fury",
                "uid": "FMHUD_MOLTENFURY",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_MoltenBlood",
                "auto": True,
                "color": [1, 1, 1, 1],
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_HEALTH,UNIT_MAXHEALTH,PLAYER_TARGET_CHANGED,PLAYER_ENTERING_WORLD",
                            "custom": """function(event, ...)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") or not UnitCanAttack("player", "target") then
        return false
    end
    local maxHP = UnitHealthMax("target") or 0
    if maxHP <= 0 then return false end
    local curHP = UnitHealth("target") or 0
    return ((curHP / maxHP) * 100) <= 35.0
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    if not UnitExists("target") or UnitIsDeadOrGhost("target") or not UnitCanAttack("player", "target") then
        return true
    end
    local maxHP = UnitHealthMax("target") or 0
    if maxHP <= 0 then return true end
    local curHP = UnitHealth("target") or 0
    return ((curHP / maxHP) * 100) > 35.0
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("35%", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                    {
                        "type": "subglow",
                        "glow": True,
                        "glowType": "Pixel",
                        "glowLines": 8,
                        "glowFrequency": 0.25,
                        "glowLength": 10,
                        "glowThickness": 2,
                    }
                ],
            },

            # =================================================================
            # 02 - MOLTEN ARMOR (Wing: Left side column - Bottom Icon)
            # =================================================================
            {
                "id": "02 - Molten Armor",
                "uid": "FMHUD_MOLTENARMOR_GRP",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -190,
                "yOffset": 0,
                "controlledChildren": [
                    "Molten Armor - Active",
                    "Molten Armor - OFF"
                ],
            },
            # Molten Armor Active (Appears ONLY when <= 5 minutes! Otherwise HIDDEN)
            {
                "id": "Molten Armor - Active",
                "uid": "FMHUD_MA_ACTIVE",
                "parent": "02 - Molten Armor",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Ability_Mage_MoltenArmor",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 43046 or spellId == 43045 or spellId == 30482 or name == "Molten Armor" or name == "Armatura di Forgia" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("|cFFFFFF00%d:%02d|r", m, s)
            elseif rem > 0 then
                return string.format("|cFFFF4444%.0fs|r", rem)
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,PLAYER_ENTERING_WORLD,FRAME_UPDATE",
                            "custom": """function(event, ...)
    local now = GetTime()
    if event == "FRAME_UPDATE" and (now - (_G.FMHUD_LastMATime or 0)) < 0.25 then
        return _G.FMHUD_LastMAActive or false
    end
    _G.FMHUD_LastMATime = now
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 43046 or spellId == 43045 or spellId == 30482 or name == "Molten Armor" or name == "Armatura di Forgia" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or 0
            local active = rem > 0 and rem <= 300
            _G.FMHUD_LastMAActive = active
            return active
        end
    end
    _G.FMHUD_LastMAActive = false
    return false
end""",
                            "customDuration": """function()
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 43046 or spellId == 43045 or spellId == 30482 or name == "Molten Armor" or name == "Armatura di Forgia" then
            return duration or 1800, expirationTime
        end
    end
    return 0, 0
end""",
                            "customIcon": """function()
    return "Interface\\\\Icons\\\\Ability_Mage_MoltenArmor"
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    local now = GetTime()
    if event == "FRAME_UPDATE" and (now - (_G.FMHUD_LastMAUntrigTime or 0)) < 0.25 then
        return _G.FMHUD_LastMAUntrig or false
    end
    _G.FMHUD_LastMAUntrigTime = now
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 43046 or spellId == 43045 or spellId == 30482 or name == "Molten Armor" or name == "Armatura di Forgia" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or 0
            local untrig = not (rem > 0 and rem <= 300)
            _G.FMHUD_LastMAUntrig = untrig
            return untrig
        end
    end
    _G.FMHUD_LastMAUntrig = true
    return true
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },
            # Molten Armor OFF (Warning when missing)
            {
                "id": "Molten Armor - OFF",
                "uid": "FMHUD_MA_OFF",
                "parent": "02 - Molten Armor",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Ability_Mage_MoltenArmor",
                "auto": True,
                "desaturate": True,
                "color": [0.6, 0.6, 0.6, 0.8],
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": ["Molten Armor"],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnMissing",
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },

            # =================================================================
            # 03 - ARCANE INTELLECT (Left icon in 3-buff horizontal row above Stats)
            # =================================================================
            {
                "id": "03 - Arcane Intellect",
                "uid": "FMHUD_INTELLECT_GRP",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -220,
                "yOffset": 0,
                "controlledChildren": [
                    "Arcane Intellect - Active",
                    "Arcane Intellect - OFF"
                ],
            },
            # Arcane Intellect Active (Appears ONLY when <= 5 minutes! Otherwise HIDDEN)
            {
                "id": "Arcane Intellect - Active",
                "uid": "FMHUD_AI_ACTIVE",
                "parent": "03 - Arcane Intellect",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Holy_MagicalSentry",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": """function()
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 1459 or spellId == 1460 or spellId == 1461 or spellId == 10156 or spellId == 10157 or spellId == 27126 or spellId == 42995 or spellId == 23028 or spellId == 27127 or spellId == 43002 or spellId == 61024 or spellId == 61316 or spellId == 54034 or spellId == 57567 or name == "Arcane Intellect" or name == "Arcane Brilliance" or name == "Dalaran Intellect" or name == "Dalaran Brilliance" or name == "Fel Intelligence" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("|cFFFFFF00%d:%02d|r", m, s)
            elseif rem > 0 then
                return string.format("|cFFFF4444%.0fs|r", rem)
            end
        end
    end
    return ""
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,PLAYER_ENTERING_WORLD,FRAME_UPDATE",
                            "custom": """function(event, ...)
    local now = GetTime()
    if event == "FRAME_UPDATE" and (now - (_G.FMHUD_LastAITime or 0)) < 0.25 then
        return _G.FMHUD_LastAIActive or false
    end
    _G.FMHUD_LastAITime = now
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 1459 or spellId == 1460 or spellId == 1461 or spellId == 10156 or spellId == 10157 or spellId == 27126 or spellId == 42995 or spellId == 23028 or spellId == 27127 or spellId == 43002 or spellId == 61024 or spellId == 61316 or spellId == 54034 or spellId == 57567 or name == "Arcane Intellect" or name == "Arcane Brilliance" or name == "Dalaran Intellect" or name == "Dalaran Brilliance" or name == "Fel Intelligence" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or 0
            local active = rem > 0 and rem <= 300
            _G.FMHUD_LastAIActive = active
            return active
        end
    end
    _G.FMHUD_LastAIActive = false
    return false
end""",
                            "customDuration": """function()
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 1459 or spellId == 1460 or spellId == 1461 or spellId == 10156 or spellId == 10157 or spellId == 27126 or spellId == 42995 or spellId == 23028 or spellId == 27127 or spellId == 43002 or spellId == 61024 or spellId == 61316 or spellId == 54034 or spellId == 57567 or name == "Arcane Intellect" or name == "Arcane Brilliance" or name == "Dalaran Intellect" or name == "Dalaran Brilliance" or name == "Fel Intelligence" then
            return duration or 3600, expirationTime
        end
    end
    return 0, 0
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    local now = GetTime()
    if event == "FRAME_UPDATE" and (now - (_G.FMHUD_LastAIUntrigTime or 0)) < 0.25 then
        return _G.FMHUD_LastAIUntrig or false
    end
    _G.FMHUD_LastAIUntrigTime = now
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 1459 or spellId == 1460 or spellId == 1461 or spellId == 10156 or spellId == 10157 or spellId == 27126 or spellId == 42995 or spellId == 23028 or spellId == 27127 or spellId == 43002 or spellId == 61024 or spellId == 61316 or spellId == 54034 or spellId == 57567 or name == "Arcane Intellect" or name == "Arcane Brilliance" or name == "Dalaran Intellect" or name == "Dalaran Brilliance" or name == "Fel Intelligence" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or 0
            local untrig = not (rem > 0 and rem <= 300)
            _G.FMHUD_LastAIUntrig = untrig
            return untrig
        end
    end
    _G.FMHUD_LastAIUntrig = true
    return true
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },
            # Arcane Intellect OFF (Warning when missing on player)
            {
                "id": "Arcane Intellect - OFF",
                "uid": "FMHUD_AI_OFF",
                "parent": "03 - Arcane Intellect",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Holy_MagicalSentry",
                "auto": True,
                "desaturate": True,
                "color": [0.6, 0.6, 0.6, 0.8],
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": [
                                "Arcane Intellect",
                                "Arcane Brilliance",
                                "Dalaran Intellect",
                                "Dalaran Brilliance",
                                "Fel Intelligence"
                            ],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnMissing",
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },

            # =================================================================
            # 04 - FOCUS MAGIC (Right icon in 3-buff horizontal row above Stats)
            # =================================================================
            {
                "id": "04 - Focus Magic",
                "uid": "FMHUD_FOCUS_GRP",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -160,
                "yOffset": 0,
                "controlledChildren": [
                    "Focus Magic - Active",
                    "Focus Magic - OFF"
                ],
            },
            # Focus Magic Active (Appears ONLY when <= 5 minutes! Otherwise HIDDEN)
            {
                "id": "Focus Magic - Active",
                "uid": "FMHUD_FOCUS_ACTIVE",
                "parent": "04 - Focus Magic",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Arcane_StudentOfMagic",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_fm_custom_text(),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,PLAYER_ENTERING_WORLD",
                            "custom": make_fm_trigger(),
                            "customDuration": make_fm_custom_duration(),
                            "customIcon": """function()
    return "Interface\\\\Icons\\\\Spell_Arcane_StudentOfMagic"
end""",
                        },
                        "untrigger": {
                            "custom": make_fm_untrigger(),
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },
            # Focus Magic OFF (Warning when not cast on anyone or expired)
            {
                "id": "Focus Magic - OFF",
                "uid": "FMHUD_FOCUS_OFF",
                "parent": "04 - Focus Magic",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Arcane_StudentOfMagic",
                "desaturate": True,
                "color": [0.6, 0.6, 0.6, 0.8],
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "COMBAT_LOG_EVENT_UNFILTERED,UNIT_SPELLCAST_SUCCEEDED,UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_FOCUS_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,PLAYER_ENTERING_WORLD",
                            "custom": make_fm_off_trigger(),
                        },
                        "untrigger": {
                            "custom": make_fm_off_untrigger(),
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },

            # =================================================================
            # 05 - TRINKET 1 (Slot 13 - With Active Proc & ICD Reproc Countdown)
            # =================================================================
            {
                "id": "05 - Trinket 1",
                "uid": "FMHUD_TRINKET1",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -110,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_slot_custom_text(13),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,BAG_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,PLAYER_EQUIPMENT_CHANGED,UNIT_INVENTORY_CHANGED,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": make_slot_custom_duration(13),
                            "customIcon": make_slot_custom_icon(13, "Interface\\\\Icons\\\\INV_Misc_QuestionMark"),
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
                ],
            },

            # =================================================================
            # 05 - TRINKET 2 (Slot 14 - With Active Proc & ICD Reproc Countdown)
            # =================================================================
            {
                "id": "05 - Trinket 2",
                "uid": "FMHUD_TRINKET2",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -66,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_slot_custom_text(14),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,BAG_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,PLAYER_EQUIPMENT_CHANGED,UNIT_INVENTORY_CHANGED,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": make_slot_custom_duration(14),
                            "customIcon": make_slot_custom_icon(14, "Interface\\\\Icons\\\\INV_Misc_QuestionMark"),
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
                ],
            },

            # =================================================================
            # 06 - CLOAK (Slot 15 - With Active Proc & ICD Reproc Countdown)
            # =================================================================
            {
                "id": "06 - Cloak",
                "uid": "FMHUD_CLOAK",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -22,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_slot_custom_text(15),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,BAG_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,PLAYER_EQUIPMENT_CHANGED,UNIT_INVENTORY_CHANGED,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": make_slot_custom_duration(15),
                            "customIcon": make_slot_custom_icon(15, "Interface\\\\Icons\\\\INV_Misc_Cape_19"),
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
                ],
            },

            # =================================================================
            # 06 - TIER 8 (Center of Utility Row at x = 0, y = -54)
            # Active when >= 2 pieces of T8 equipped (Praxis: +350 SP, 45s ICD)
            # =================================================================
            {
                "id": "06 - Tier 8",
                "uid": "FMHUD_TIER8",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 0,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Arcane_StudentOfMagic",
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_t8_custom_text(),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "update",
                            "events": "PLAYER_EQUIPMENT_CHANGED,UNIT_INVENTORY_CHANGED,PLAYER_ENTERING_WORLD,ZONE_CHANGED_NEW_AREA,UNIT_AURA,FMHUD_T8_UPDATE",
                            "custom": f"""function(event, ...)
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    local state, rem, dur, icon, isEquipped = _G.FMHUD_CheckT8()
    return isEquipped
end""",
                            "customDuration": make_t8_custom_duration(),
                            "customIcon": make_t8_custom_icon(),
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    if not _G.FMHUD_T8_InitDone then return true end
    local state, rem, dur, icon, isEquipped = _G.FMHUD_CheckT8()
    return not isEquipped
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
                ],
            },

            # =================================================================
            # 06 - MANA GEM (Right of T8 - T7 Proc + CD + Charges)
            # =================================================================
            {
                "id": "06 - Mana Gem",
                "uid": "FMHUD_MANAGEM",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 22,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\INV_Misc_Gem_Sapphire_02",
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_managem_custom_text(),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "update",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": make_managem_custom_duration(),
                            "customIcon": make_managem_custom_icon(),
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext(
                        "%p",
                        justify="CENTER",
                        anchor_point="INNER_BOTTOM",
                        font_size=10,
                        y_offset=1,
                        extra_props={
                            "text_text_format_p_format": "timed",
                            "text_text_format_p_time_precision": 1,
                            "text_text_format_p_time_dynamic_threshold": 60,
                        }
                    ),
                    make_subtext(
                        "%c",
                        justify="RIGHT",
                        anchor_point="INNER_TOPRIGHT",
                        font_size=9,
                        extra_props={
                            "anchorXOffset": -1,
                            "anchorYOffset": -1,
                        }
                    ),
                ],
            },

            # =================================================================
            # 06 - COMBUSTION (Between Mana Gem and Mirror Image)
            # =================================================================
            {
                "id": "06 - Combustion",
                "uid": "FMHUD_COMBUSTION",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 66,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Fire_SealOfFire",
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_combustion_custom_text(),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,PLAYER_EQUIPMENT_CHANGED,UNIT_INVENTORY_CHANGED,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": make_combustion_custom_duration(),
                            "customIcon": """function()
    return "Interface\\\\Icons\\\\Spell_Fire_SealOfFire"
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
                ],
            },

            # =================================================================
            # 06 - MIRROR IMAGE (Rightmost icon in utility row)
            # =================================================================
            {
                "id": "06 - Mirror Image",
                "uid": "FMHUD_MIRRORIMAGE",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 110,
                "yOffset": -45,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\Spell_Magic_LesserInvisibilty",
                "cooldown": True,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "cooldownTextDisabled": True,
                "inverse": False,
                "customTextUpdate": "update",
                "customText": make_mirrorimage_custom_text(),
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "update",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": make_mirrorimage_custom_duration(),
                            "customIcon": make_mirrorimage_custom_icon(),
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
                ],
            },

            # =================================================================
            # 07 - MANA BAR (Aurabar)
            # =================================================================
            {
                "id": "07 - Mana Bar",
                "uid": "FMHUD_MANABAR",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 278,
                "height": 14,
                "xOffset": 0,
                "yOffset": -15,
                "barColor": [0.09, 0.55, 1.0, 1.0],
                "backgroundColor": [0.1, 0.1, 0.1, 0.8],
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "displayText_format_1.percentpower_format": "Number",
                "displayText_format_1.percentpower_decimal_precision": 2,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "unit",
                            "event": "Power",
                            "unit": "player",
                            "powertype": 0,
                            "use_powertype": True,
                            "use_unit": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "conditions": [
                    {
                        "check": {
                            "trigger": 1,
                            "op": "<=",
                            "variable": "percentpower",
                            "value": "20",
                        },
                        "changes": [
                            {
                                "property": "barColor",
                                "value": [1.0, 0.15, 0.15, 1.0],
                            }
                        ]
                    }
                ],
                "subRegions": [
                    { "type": "subbackground" },
                    { "type": "subforeground" },
                    make_subtext(
                        "%1.percentpower%%",
                        justify="CENTER",
                        anchor_point="CENTER",
                        font_size=10,
                        extra_props={
                            "text_text_format_1.percentpower_format": "Number",
                            "text_text_format_1.percentpower_decimal_precision": 2,
                        }
                    ),
                ],
            },

            # =================================================================
            # 10 - HOT STREAK BAR (Dual Segment Progress Bar, Clean - No Text)
            # =================================================================
            {
                "id": "10 - Hot Streak Bar",
                "uid": "FMHUD_HOTSTREAK_BAR_GRP",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": 0,
                "yOffset": -25,
                "anchorPoint": "CENTER",
                "selfPoint": "CENTER",
                "controlledChildren": [
                    "Hot Streak Bar - Background",
                    "Hot Streak Bar - Segment 1",
                    "Hot Streak Bar - Proc",
                ],
            },
            # Hot Streak Bar - Background Frame (264x7px)
            {
                "id": "Hot Streak Bar - Background",
                "uid": "FMHUD_HSBAR_BG",
                "parent": "10 - Hot Streak Bar",
                "regionType": "texture",
                "internalVersion": 52,
                "xOffset": 0,
                "yOffset": 0,
                "width": 278,
                "height": 7,
                "texture": "Interface\\Buttons\\WHITE8X8",
                "color": [0.05, 0.05, 0.05, 0.85],
                "selfPoint": "CENTER",
                "anchorPoint": "CENTER",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "PLAYER_ENTERING_WORLD,PLAYER_ALIVE,PLAYER_DEAD",
                            "custom": make_hotstreak_bg_trigger(),
                        },
                        "untrigger": {
                            "custom": make_hotstreak_bg_untrigger(),
                        }
                    },
                    "activeTriggerMode": -10,
                },
            },
            # Hot Streak Bar - Segment 1 (Left Half: 1° Crit, Metà Barretta 130x5px a -66, Illuminata a 50%, Persistente)
            {
                "id": "Hot Streak Bar - Segment 1",
                "uid": "FMHUD_HSBAR_SEG1",
                "parent": "10 - Hot Streak Bar",
                "regionType": "texture",
                "internalVersion": 52,
                "width": 137,
                "height": 5,
                "xOffset": -70.5,
                "yOffset": 0,
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "color": [1.0, 0.55, 0.0, 1.0],
                "selfPoint": "CENTER",
                "anchorPoint": "CENTER",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "FMHUD_HS_UPDATE,PLAYER_ENTERING_WORLD,PLAYER_DEAD,PLAYER_ALIVE",
                            "custom": make_hotstreak_seg1_trigger(),
                        },
                        "untrigger": {
                            "custom": make_hotstreak_seg1_untrigger(),
                        }
                    },
                    "activeTriggerMode": -10,
                },
            },
            # Hot Streak Bar - Proc (Barra Unificata 264x5px: Hot Streak 10s Countdown Swipe, Pixel Glow)
            {
                "id": "Hot Streak Bar - Proc",
                "uid": "FMHUD_HSBAR_SEG2",
                "parent": "10 - Hot Streak Bar",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 137,
                "height": 5,
                "xOffset": 70.5,
                "yOffset": 0,
                "barColor": [1.0, 0.35, 0.0, 1.0],
                "backgroundColor": [0.1, 0.1, 0.1, 0.8],
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": [
                                "Hot Streak",
                                "48108",
                                "Buona sorte"
                            ],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    { "type": "subforeground" },
                    {
                        "type": "subglow",
                        "glow": True,
                        "glowType": "Pixel",
                        "glowLines": 8,
                        "glowFrequency": 0.25,
                        "glowLength": 6,
                        "glowThickness": 2,
                        "glowColor": [1.0, 0.6, 0.0, 1.0],
                    }
                ],
            },

            # =================================================================
            # 08 - CASTBAR (Aurabar)
            # =================================================================
            {
                "id": "08 - Castbar",
                "uid": "FMHUD_CASTBAR",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 278,
                "height": 20,
                "xOffset": 0,
                "yOffset": 8,
                "barColor": [0.0, 0.77, 1.0, 1.0],
                "backgroundColor": [0.15, 0.15, 0.15, 0.8],
                "texture": "Blizzard",
                "icon": False,
                "icon_color": [1, 1, 1, 1],
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "unit",
                            "event": "Cast",
                            "unit": "player",
                            "use_unit": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    { "type": "subforeground" },
                    make_subtext(
                        "%p",
                        justify="RIGHT",
                        anchor_point="INNER_RIGHT",
                        font_size=11,
                        extra_props={
                            "anchorXOffset": -6,
                            "text_text_format_p_format": "timed",
                            "text_text_format_p_time_precision": 1,
                        }
                    ),
                    make_subtext("%n", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, extra_props={"anchorXOffset": 6}),
                ],
            },


            # =================================================================
            # 10 - ALERTS (Group)
            # =================================================================
            {
                "id": "10 - Alerts",
                "uid": "FMHUD_ALERTS_GRP",
                "parent": "Fire Mage 3.3.5a AM",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": 0,
                "yOffset": 105,
                "controlledChildren": [
                    "Alert - Hot Streak"
                ],
            },
            # Alert - Hot Streak
            {
                "id": "Alert - Hot Streak",
                "uid": "FMHUD_ALERT_HS",
                "parent": "10 - Alerts",
                "regionType": "text",
                "internalVersion": 52,
                "displayText": "|cFFFF5500HOT STREAK!|r\\n|cFFFFFF00PYROBLAST READY!|r",
                "fontSize": 20,
                "outline": "OUTLINE",
                "justify": "CENTER",
                "color": [1, 1, 1, 1],
                "selfPoint": "CENTER",
                "anchorPoint": "CENTER",
                "xOffset": 0,
                "yOffset": 0,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": ["Hot Streak"],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
            },

            # =================================================================
            # 12 - STATS PANEL (Under the 3 Buffs row, perfectly aligned)
            # =================================================================
            {
                "id": "12 - Stats Panel",
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
            # Stats Panel - Background Frame
            {
                "id": "Stats Panel - Background",
                "uid": "FMHUD_STATS_BG",
                "parent": "12 - Stats Panel",
                "regionType": "texture",
                "internalVersion": 52,
                "xOffset": 0,
                "yOffset": 0,
                "width": 88,
                "height": 48,
                "texture": "Interface\\Buttons\\WHITE8X8",
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
            # Stats Panel - Real-time Text (SP, Crit, Haste, Hit)
            {
                "id": "Stats Panel - Text",
                "uid": "FMHUD_STATS_TXT",
                "parent": "12 - Stats Panel",
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
                "font": "Expressway",
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
    }
    for item in data["c"]:
        item["load"] = copy.deepcopy(FIRE_MAGE_LOAD)
    return data

