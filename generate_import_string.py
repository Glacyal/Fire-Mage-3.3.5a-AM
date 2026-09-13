"""
Generator for Fire Mage HUD WeakAuras (WoW 3.3.5a - WeakAuras 4.0.0 backport)
Built to exactly match the native WeakAuras 4.0.0 (internalVersion 52) engine specifications
found in the user's working SavedVariables/WeakAuras.lua!
"""
import zlib

true = True
false = False

CHARS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '(', ')'
]

def serialize_string(s: str) -> str:
    res = ['^S']
    for ch in s:
        n = ord(ch)
        if n == 30:
            res.append('~z')
        elif n <= 32:
            res.append('~' + chr(n + 64))
        elif n == 94:
            res.append('~}')
        elif n == 126:
            res.append('~|')
        elif n == 127:
            res.append('~{')
        else:
            res.append(ch)
    return ''.join(res)

def serialize_value(v):
    if v is None:
        return '^Z'
    elif isinstance(v, bool):
        return '^B' if v else '^b'
    elif isinstance(v, (int, float)):
        if isinstance(v, float) and v.is_integer():
            return f'^N{int(v)}'
        return f'^N{v}'
    elif isinstance(v, str):
        return serialize_string(v)
    elif isinstance(v, dict):
        res = ['^T']
        for k, val in v.items():
            res.append(serialize_value(k))
            res.append(serialize_value(val))
        res.append('^t')
        return ''.join(res)
    elif isinstance(v, list):
        res = ['^T']
        for i, val in enumerate(v, 1):
            res.append(serialize_value(i))
            res.append(serialize_value(val))
        res.append('^t')
        return ''.join(res)
    raise ValueError(f'Unsupported type: {type(v)}')

def ace_serialize(obj):
    return '^1' + serialize_value(obj) + '^^'

def libdeflate_encode_for_print(data: bytes) -> str:
    n = len(data)
    i = 0
    buffer = []
    while i <= n - 3:
        x1, x2, x3 = data[i], data[i+1], data[i+2]
        i += 3
        cache = x1 + (x2 << 8) + (x3 << 16)
        b1 = cache % 64
        cache = (cache - b1) // 64
        b2 = cache % 64
        cache = (cache - b2) // 64
        b3 = cache % 64
        b4 = (cache - b3) // 64
        buffer.append(CHARS[b1] + CHARS[b2] + CHARS[b3] + CHARS[b4])
    
    cache = 0
    cache_bitlen = 0
    while i < n:
        x = data[i]
        cache += x * (1 << cache_bitlen)
        cache_bitlen += 8
        i += 1
    
    while cache_bitlen > 0:
        bit6 = cache % 64
        buffer.append(CHARS[bit6])
        cache = (cache - bit6) // 64
        cache_bitlen -= 6
    
    return ''.join(buffer)

def generate_wa_string(data_table):
    serialized = ace_serialize(data_table)
    comp_obj = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    compressed = comp_obj.compress(serialized.encode('latin1')) + comp_obj.flush()
    encoded = libdeflate_encode_for_print(compressed)
    return f"!WA:1!{encoded}"

def make_subtext(text, justify="CENTER", anchor_point="INNER_BOTTOM", font_size=12, y_offset=0, extra_props=None):
    res = {
        "type": "subtext",
        "text_text": text,
        "text_justify": justify,
        "text_anchorPoint": anchor_point,
        "text_fontSize": font_size,
        "text_font": "Expressway",
        "text_fontType": "OUTLINE",
        "text_color": [1, 1, 1, 1],
        "text_visible": True,
        "text_selfPoint": "AUTO",
        "text_automaticWidth": "Auto",
        "text_fixedWidth": 64,
        "anchorYOffset": y_offset,
        "anchorXOffset": 0,
        "text_shadowXOffset": 1,
        "text_shadowYOffset": -1,
        "text_shadowColor": [0, 0, 0, 1],
    }
    if extra_props:
        res.update(extra_props)
    return res

def build_wa_tree():
    data = {
        "m": "d",
        "v": 2000,
        "w": "4.0.0",
        "d": {
            "id": "Fire Mage HUD",
            "uid": "FMHUD_ROOT",
            "regionType": "group",
            "internalVersion": 52,
            "scale": 1,
            "xOffset": 0,
            "yOffset": -150,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "controlledChildren": [
                "01 - Procs",
                "02 - Molten Armor",
                "04 - Focus Magic",
                "05 - Trinket 1",
                "05 - Trinket 2",
                "06 - Cloak",
                "06 - Mana Gem",
                "07 - Mana Bar",
                "08 - Castbar",
                "09 - GCD",
                "10 - Alerts"
            ],
            "load": {
                "use_class": True,
                "class": { "single": "MAGE", "multi": { "MAGE": True } }
            }
        },
        "c": [
            # =================================================================
            # 01 - PROCS (Dynamic Group)
            # =================================================================
            {
                "id": "01 - Procs",
                "uid": "FMHUD_PROCS_DG",
                "parent": "Fire Mage HUD",
                "regionType": "dynamicgroup",
                "internalVersion": 52,
                "grow": "HORIZONTAL",
                "align": "CENTER",
                "space": 6,
                "xOffset": 0,
                "yOffset": 44,
                "controlledChildren": [
                    "Hot Streak",
                    "Living Bomb",
                    "Ignite",
                    "Scorch",
                    "Combustion",
                    "Molten Fury"
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
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": ["Hot Streak"],
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
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
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
                "cooldownSwipe": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "target",
                            "auranames": ["Living Bomb"],
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
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
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
                "cooldownSwipe": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "target",
                            "auranames": ["Ignite"],
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
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
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
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "target",
                            "auranames": [
                                "Improved Scorch",
                                "Scorch",
                                "22959",
                                "Shadow and Flame"
                            ],
                            "auraspellids": [
                                22959,
                                12873,
                                12872,
                                11095,
                                17800
                            ],
                            "useName": True,
                            "debuffType": "HARMFUL",
                            "matchesShowOn": "showOnActive",
                            "ownOnly": False,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "conditions": [
                    {
                        "check": {
                            "trigger": 1,
                            "variable": "remaining",
                            "op": "<=",
                            "value": "5"
                        },
                        "changes": [
                            {
                                "property": "color",
                                "value": [1, 0.25, 0.25, 1]
                            }
                        ]
                    }
                ],
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },
            # Combustion (Cooldown & Active)
            {
                "id": "Combustion",
                "uid": "FMHUD_COMBUSTION",
                "parent": "01 - Procs",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_SealOfFire",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldownSwipe": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "spell",
                            "event": "Cooldown Progress (Spell)",
                            "spellName": 11129,
                            "realSpellName": "Combustion",
                            "use_spellName": True,
                            "genericShowOn": "showAlways",
                            "use_genericShowOn": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
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
                "color": [1, 0.4, 0, 1],
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "unit",
                            "event": "Health",
                            "unit": "target",
                            "use_unit": True,
                            "percenthealth": "35",
                            "use_percenthealth": True,
                            "health_operator": "<=",
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("35%", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },

            # =================================================================
            # 02 - MOLTEN ARMOR (Wing: Left side of central bars)
            # =================================================================
            {
                "id": "02 - Molten Armor",
                "uid": "FMHUD_MOLTENARMOR_GRP",
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -160,
                "yOffset": -7,
                "controlledChildren": [
                    "Molten Armor - Active",
                    "Molten Armor - OFF"
                ],
            },
            # Molten Armor Active
            {
                "id": "Molten Armor - Active",
                "uid": "FMHUD_MA_ACTIVE",
                "parent": "02 - Molten Armor",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_Incinerate",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldownSwipe": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": ["Molten Armor"],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },
            # Molten Armor OFF (Warning when missing)
            {
                "id": "Molten Armor - OFF",
                "uid": "FMHUD_MA_OFF",
                "parent": "02 - Molten Armor",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Fire_Incinerate",
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
                    make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },

            # =================================================================
            # 04 - FOCUS MAGIC (Wing: Right side of central bars)
            # =================================================================
            {
                "id": "04 - Focus Magic",
                "uid": "FMHUD_FOCUS_GRP",
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": 160,
                "yOffset": -7,
                "controlledChildren": [
                    "Focus Magic - Active",
                    "Focus Magic - OFF"
                ],
            },
            # Focus Magic Active (Remaining Time / Proc)
            {
                "id": "Focus Magic - Active",
                "uid": "FMHUD_FOCUS_ACTIVE",
                "parent": "04 - Focus Magic",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
                "displayIcon": "Interface\\Icons\\Spell_Arcane_StudentOfMagic",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldownSwipe": True,
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "aura2",
                            "unit": "player",
                            "auranames": ["Focus Magic"],
                            "useName": True,
                            "debuffType": "HELPFUL",
                            "matchesShowOn": "showOnActive",
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },
            # Focus Magic OFF (Gray Icon when not applied to anyone)
            {
                "id": "Focus Magic - OFF",
                "uid": "FMHUD_FOCUS_OFF",
                "parent": "04 - Focus Magic",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 34,
                "height": 34,
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
                            "custom": """function(event, ...)
    FMHUD_State = FMHUD_State or {}
    local now = GetTime()

    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and spell == "Focus Magic" then
            FMHUD_State.FMTarget = UnitName("target") or "Ally"
            FMHUD_State.FMExpires = now + 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        if sourceGUID == UnitGUID("player") and (spellName == "Focus Magic" or spellId == 54646) then
            if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                FMHUD_State.FMTarget = destName or "Ally"
                FMHUD_State.FMExpires = now + 1800
            elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                FMHUD_State.FMExpires = 0
                FMHUD_State.FMTarget = nil
            end
        elseif subEvent == "UNIT_DIED" and FMHUD_State.FMTarget and destName == FMHUD_State.FMTarget then
            FMHUD_State.FMExpires = 0
            FMHUD_State.FMTarget = nil
        end
    end

    if FMHUD_State.FMExpires and FMHUD_State.FMExpires > now then
        return false
    end

    local b = "Focus Magic"
    for i = 1, 40 do
        local n = UnitBuff("player", i)
        if not n then break end
        if n == b then return false end
    end

    if UnitExists("target") and UnitIsFriend("player", "target") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("target", i)
            if not n then break end
            if n == b and (c == "player" or not c) then
                FMHUD_State.FMExpires = now + 1800
                FMHUD_State.FMTarget = UnitName("target")
                return false
            end
        end
    end

    if UnitExists("focus") and UnitIsFriend("player", "focus") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("focus", i)
            if not n then break end
            if n == b and (c == "player" or not c) then
                FMHUD_State.FMExpires = now + 1800
                FMHUD_State.FMTarget = UnitName("focus")
                return false
            end
        end
    end

    local nr = GetNumRaidMembers()
    if nr and nr > 0 then
        for r = 1, nr do
            local u = "raid"..r
            for i = 1, 40 do
                local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                if not n then break end
                if n == b and (c == "player" or not c) then
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMTarget = UnitName(u)
                    return false
                end
            end
        end
    else
        local np = GetNumPartyMembers()
        if np and np > 0 then
            for p = 1, np do
                local u = "party"..p
                for i = 1, 40 do
                    local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                    if not n then break end
                    if n == b and (c == "player" or not c) then
                        FMHUD_State.FMExpires = now + 1800
                        FMHUD_State.FMTarget = UnitName(u)
                        return false
                    end
                end
            end
        end
    end

    return true
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
    local now = GetTime()
    if FMHUD_State and FMHUD_State.FMExpires and FMHUD_State.FMExpires > now then
        return true
    end

    local b = "Focus Magic"
    for i = 1, 40 do
        local n = UnitBuff("player", i)
        if not n then break end
        if n == b then return true end
    end

    if UnitExists("target") and UnitIsFriend("player", "target") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("target", i)
            if not n then break end
            if n == b and (c == "player" or not c) then return true end
        end
    end

    if UnitExists("focus") and UnitIsFriend("player", "focus") then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, c = UnitBuff("focus", i)
            if not n then break end
            if n == b and (c == "player" or not c) then return true end
        end
    end

    local nr = GetNumRaidMembers()
    if nr and nr > 0 then
        for r = 1, nr do
            local u = "raid"..r
            for i = 1, 40 do
                local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                if not n then break end
                if n == b and (c == "player" or not c) then return true end
            end
        end
    else
        local np = GetNumPartyMembers()
        if np and np > 0 then
            for p = 1, np do
                local u = "party"..p
                for i = 1, 40 do
                    local n, _, _, _, _, _, _, c = UnitBuff(u, i)
                    if not n then break end
                    if n == b and (c == "player" or not c) then return true end
                end
            end
        end
    end

    return false
end"""
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("|cFF888888OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11),
                ],
            },

            # =================================================================
            # 05 - TRINKET 1 (Slot 13 - Centered row under Mana Bar)
            # =================================================================
            {
                "id": "05 - Trinket 1",
                "uid": "FMHUD_TRINKET1",
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -60,
                "yOffset": -54,
                "width": 28,
                "height": 28,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "customTextUpdate": "update",
                "customText": """function()
    _G.FMHUD_TrinketDB = _G.FMHUD_TrinketDB or {
        [50348] = { buff = "Celestial Infusion" },
        [50345] = { buff = "Celestial Infusion" },
        [50360] = { buff = "Siphon of Aethas" },
        [50365] = { buff = "Siphon of Aethas", altBuff = "Aethas' Siphon" },
        [54572] = { buff = "Shared Twilight" },
        [54588] = { buff = "Shared Twilight" },
        [45518] = { buff = "Elusive Power" },
        [47271] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [47477] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [47182] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [47316] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [40682] = { buff = "Now is the Time!" },
        [40255] = { buff = "Curse of the Eye" },
        [47213] = { buff = "Deadly Precision" },
        [37660] = { buff = "Forged Ember" },
        [45308] = { buff = "Blessing of the Broodmother" },
        [40432] = { buff = "Dragon Soul" },
        [37264] = { buff = "Sudden Velocity" },
        [44253] = { buff = "Greatness" },
        [44255] = { buff = "Greatness" },
        [42987] = { buff = "Greatness" },
        [44254] = { buff = "Greatness" },
        [50340] = { buff = "Gathering Tracker" },
        [50353] = { buff = "Gathering Tracker" },
        [45466] = { buff = "Velocity" },
        [48724] = { buff = "Chilled Heart" },
        [48722] = { buff = "Volatile Power" },
        [50259] = { buff = "Deadly Precision" },
        [37873] = { buff = "Soul Power" },
        [50339] = { buff = "Pure Energy" },
        [50346] = { buff = "Pure Energy" },
        [47215] = { buff = "Revitalized" },
        [45490] = { buff = "Pandora's Plea" },
        [40685] = { buff = "Living Flame" },
        [50357] = { buff = "Maghia's Misguided Quill" },
    }
    _G.FMHUD_CasterProcs = _G.FMHUD_CasterProcs or {
        ["Celestial Infusion"] = true,
        ["Siphon of Aethas"] = true,
        ["Aethas' Siphon"] = true,
        ["Shared Twilight"] = true,
        ["Twilight Flame"] = true,
        ["Elusive Power"] = true,
        ["Motes of Flame"] = true,
        ["Pillar of Flame"] = true,
        ["Now is the Time!"] = true,
        ["Curse of the Eye"] = true,
        ["Deadly Precision"] = true,
        ["Forged Ember"] = true,
        ["Blessing of the Broodmother"] = true,
        ["Dragon Soul"] = true,
        ["Sudden Velocity"] = true,
        ["Greatness"] = true,
        ["Gathering Tracker"] = true,
        ["Velocity"] = true,
        ["Chilled Heart"] = true,
        ["Volatile Power"] = true,
        ["Soul Power"] = true,
        ["Pure Energy"] = true,
        ["Revitalized"] = true,
        ["Pandora's Plea"] = true,
        ["Living Flame"] = true,
        ["Maghia's Misguided Quill"] = true,
        ["Peerless Destruction"] = true,
    }

    local itemID = GetInventoryItemID("player", 13)
    local hasProc = false
    local rem = 0
    if itemID and _G.FMHUD_TrinketDB[itemID] then
        local entry = _G.FMHUD_TrinketDB[itemID]
        for i = 1, 40 do
            local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if name == entry.buff or (entry.altBuff and name == entry.altBuff) then
                if expirationTime and expirationTime > GetTime() then
                    hasProc = true
                    rem = expirationTime - GetTime()
                    break
                end
            end
        end
    end

    if not hasProc then
        local otherID = GetInventoryItemID("player", 14)
        local otherEntry = otherID and _G.FMHUD_TrinketDB[otherID]
        for i = 1, 40 do
            local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                if expirationTime and expirationTime > GetTime() then
                    hasProc = true
                    rem = expirationTime - GetTime()
                    break
                end
            end
        end
    end

    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if hasProc then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2)
        end
        return string.format("|cFFFFFF00%.1f|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
        local start, duration = GetInventoryItemCooldown("player", 13)
        if start and duration and start > 0 and duration > 1.5 then
            local remCD = (start + duration) - GetTime()
            if remCD > 0 then
                return string.format("%.0f", remCD)
            end
        end
        return ""
    end
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "PLAYER_EQUIPMENT_CHANGED,UNIT_AURA,SPELL_UPDATE_COOLDOWN,PLAYER_ENTERING_WORLD",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": """function()
    local itemID = GetInventoryItemID("player", 13)
    if _G.FMHUD_TrinketDB and itemID and _G.FMHUD_TrinketDB[itemID] then
        local entry = _G.FMHUD_TrinketDB[itemID]
        for i = 1, 40 do
            local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if name == entry.buff or (entry.altBuff and name == entry.altBuff) then
                if expirationTime and expirationTime > GetTime() then
                    return duration, expirationTime
                end
            end
        end
    end
    if _G.FMHUD_CasterProcs then
        local otherID = GetInventoryItemID("player", 14)
        local otherEntry = otherID and _G.FMHUD_TrinketDB and _G.FMHUD_TrinketDB[otherID]
        for i = 1, 40 do
            local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                if expirationTime and expirationTime > GetTime() then
                    return duration, expirationTime
                end
            end
        end
    end
    local start, duration = GetInventoryItemCooldown("player", 13)
    if start and duration and start > 0 and duration > 1.5 then
        return duration, start + duration
    end
    return 0, 0
end""",
                            "customIcon": """function()
    local itemID = GetInventoryItemID("player", 13)
    if _G.FMHUD_TrinketDB and itemID and _G.FMHUD_TrinketDB[itemID] then
        local entry = _G.FMHUD_TrinketDB[itemID]
        for i = 1, 40 do
            local name, _, icon, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if name == entry.buff or (entry.altBuff and name == entry.altBuff) then
                if expirationTime and expirationTime > GetTime() then
                    return icon
                end
            end
        end
    end
    if _G.FMHUD_CasterProcs then
        local otherID = GetInventoryItemID("player", 14)
        local otherEntry = otherID and _G.FMHUD_TrinketDB and _G.FMHUD_TrinketDB[otherID]
        for i = 1, 40 do
            local name, _, icon, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                if expirationTime and expirationTime > GetTime() then
                    return icon
                end
            end
        end
    end
    return GetInventoryItemTexture("player", 13) or "Interface\\\\Icons\\\\INV_Misc_QuestionMark"
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
            # 05 - TRINKET 2 (Slot 14 - Centered row under Mana Bar)
            # =================================================================
            {
                "id": "05 - Trinket 2",
                "uid": "FMHUD_TRINKET2",
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -20,
                "yOffset": -54,
                "width": 28,
                "height": 28,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "customTextUpdate": "update",
                "customText": """function()
    _G.FMHUD_TrinketDB = _G.FMHUD_TrinketDB or {
        [50348] = { buff = "Celestial Infusion" },
        [50345] = { buff = "Celestial Infusion" },
        [50360] = { buff = "Siphon of Aethas" },
        [50365] = { buff = "Siphon of Aethas", altBuff = "Aethas' Siphon" },
        [54572] = { buff = "Shared Twilight" },
        [54588] = { buff = "Shared Twilight" },
        [45518] = { buff = "Elusive Power" },
        [47271] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [47477] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [47182] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [47316] = { buff = "Motes of Flame", altBuff = "Pillar of Flame" },
        [40682] = { buff = "Now is the Time!" },
        [40255] = { buff = "Curse of the Eye" },
        [47213] = { buff = "Deadly Precision" },
        [37660] = { buff = "Forged Ember" },
        [45308] = { buff = "Blessing of the Broodmother" },
        [40432] = { buff = "Dragon Soul" },
        [37264] = { buff = "Sudden Velocity" },
        [44253] = { buff = "Greatness" },
        [44255] = { buff = "Greatness" },
        [42987] = { buff = "Greatness" },
        [44254] = { buff = "Greatness" },
        [50340] = { buff = "Gathering Tracker" },
        [50353] = { buff = "Gathering Tracker" },
        [45466] = { buff = "Velocity" },
        [48724] = { buff = "Chilled Heart" },
        [48722] = { buff = "Volatile Power" },
        [50259] = { buff = "Deadly Precision" },
        [37873] = { buff = "Soul Power" },
        [50339] = { buff = "Pure Energy" },
        [50346] = { buff = "Pure Energy" },
        [47215] = { buff = "Revitalized" },
        [45490] = { buff = "Pandora's Plea" },
        [40685] = { buff = "Living Flame" },
        [50357] = { buff = "Maghia's Misguided Quill" },
    }
    _G.FMHUD_CasterProcs = _G.FMHUD_CasterProcs or {
        ["Celestial Infusion"] = true,
        ["Siphon of Aethas"] = true,
        ["Aethas' Siphon"] = true,
        ["Shared Twilight"] = true,
        ["Twilight Flame"] = true,
        ["Elusive Power"] = true,
        ["Motes of Flame"] = true,
        ["Pillar of Flame"] = true,
        ["Now is the Time!"] = true,
        ["Curse of the Eye"] = true,
        ["Deadly Precision"] = true,
        ["Forged Ember"] = true,
        ["Blessing of the Broodmother"] = true,
        ["Dragon Soul"] = true,
        ["Sudden Velocity"] = true,
        ["Greatness"] = true,
        ["Gathering Tracker"] = true,
        ["Velocity"] = true,
        ["Chilled Heart"] = true,
        ["Volatile Power"] = true,
        ["Soul Power"] = true,
        ["Pure Energy"] = true,
        ["Revitalized"] = true,
        ["Pandora's Plea"] = true,
        ["Living Flame"] = true,
        ["Maghia's Misguided Quill"] = true,
        ["Peerless Destruction"] = true,
    }

    local itemID = GetInventoryItemID("player", 14)
    local hasProc = false
    local rem = 0
    if itemID and _G.FMHUD_TrinketDB[itemID] then
        local entry = _G.FMHUD_TrinketDB[itemID]
        for i = 1, 40 do
            local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if name == entry.buff or (entry.altBuff and name == entry.altBuff) then
                if expirationTime and expirationTime > GetTime() then
                    hasProc = true
                    rem = expirationTime - GetTime()
                    break
                end
            end
        end
    end

    if not hasProc then
        local otherID = GetInventoryItemID("player", 13)
        local otherEntry = otherID and _G.FMHUD_TrinketDB[otherID]
        for i = 1, 40 do
            local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                if expirationTime and expirationTime > GetTime() then
                    hasProc = true
                    rem = expirationTime - GetTime()
                    break
                end
            end
        end
    end

    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if hasProc then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2)
        end
        return string.format("|cFFFFFF00%.1f|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
        local start, duration = GetInventoryItemCooldown("player", 14)
        if start and duration and start > 0 and duration > 1.5 then
            local remCD = (start + duration) - GetTime()
            if remCD > 0 then
                return string.format("%.0f", remCD)
            end
        end
        return ""
    end
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "PLAYER_EQUIPMENT_CHANGED,UNIT_AURA,SPELL_UPDATE_COOLDOWN,PLAYER_ENTERING_WORLD",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": """function()
    local itemID = GetInventoryItemID("player", 14)
    if _G.FMHUD_TrinketDB and itemID and _G.FMHUD_TrinketDB[itemID] then
        local entry = _G.FMHUD_TrinketDB[itemID]
        for i = 1, 40 do
            local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if name == entry.buff or (entry.altBuff and name == entry.altBuff) then
                if expirationTime and expirationTime > GetTime() then
                    return duration, expirationTime
                end
            end
        end
    end
    if _G.FMHUD_CasterProcs then
        local otherID = GetInventoryItemID("player", 13)
        local otherEntry = otherID and _G.FMHUD_TrinketDB and _G.FMHUD_TrinketDB[otherID]
        for i = 1, 40 do
            local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                if expirationTime and expirationTime > GetTime() then
                    return duration, expirationTime
                end
            end
        end
    end
    local start, duration = GetInventoryItemCooldown("player", 14)
    if start and duration and start > 0 and duration > 1.5 then
        return duration, start + duration
    end
    return 0, 0
end""",
                            "customIcon": """function()
    local itemID = GetInventoryItemID("player", 14)
    if _G.FMHUD_TrinketDB and itemID and _G.FMHUD_TrinketDB[itemID] then
        local entry = _G.FMHUD_TrinketDB[itemID]
        for i = 1, 40 do
            local name, _, icon, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if name == entry.buff or (entry.altBuff and name == entry.altBuff) then
                if expirationTime and expirationTime > GetTime() then
                    return icon
                end
            end
        end
    end
    if _G.FMHUD_CasterProcs then
        local otherID = GetInventoryItemID("player", 13)
        local otherEntry = otherID and _G.FMHUD_TrinketDB and _G.FMHUD_TrinketDB[otherID]
        for i = 1, 40 do
            local name, _, icon, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                if expirationTime and expirationTime > GetTime() then
                    return icon
                end
            end
        end
    end
    return GetInventoryItemTexture("player", 14) or "Interface\\\\Icons\\\\INV_Misc_QuestionMark"
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
            # 06 - CLOAK (Slot 15 - Centered row under Mana Bar)
            # =================================================================
            {
                "id": "06 - Cloak",
                "uid": "FMHUD_CLOAK",
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 20,
                "yOffset": -54,
                "width": 28,
                "height": 28,
                "cooldownSwipe": True,
                "cooldownEdge": True,
                "customTextUpdate": "update",
                "customText": """function()
    _G.FMHUD_CloakBuffs = _G.FMHUD_CloakBuffs or {
        ["Lightweave"] = true,
        ["Darkglow"] = true,
        ["Swordguard"] = true,
        ["Parachute"] = true,
        ["Flexweave"] = true,
        ["Springy Arachnoweave"] = true,
    }

    local hasProc = false
    local rem = 0
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if _G.FMHUD_CloakBuffs[name] then
            if expirationTime and expirationTime > GetTime() then
                hasProc = true
                rem = expirationTime - GetTime()
                break
            end
        end
    end

    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if hasProc then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2)
        end
        return string.format("|cFFFFFF00%.1f|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
        local start, duration = GetInventoryItemCooldown("player", 15)
        if start and duration and start > 0 and duration > 1.5 then
            local remCD = (start + duration) - GetTime()
            if remCD > 0 then
                return string.format("%.0f", remCD)
            end
        end
        return ""
    end
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "PLAYER_EQUIPMENT_CHANGED,UNIT_AURA,SPELL_UPDATE_COOLDOWN,PLAYER_ENTERING_WORLD",
                            "custom": """function(event, ...)
    return true
end""",
                            "customDuration": """function()
    if _G.FMHUD_CloakBuffs then
        for i = 1, 40 do
            local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CloakBuffs[name] then
                if expirationTime and expirationTime > GetTime() then
                    return duration, expirationTime
                end
            end
        end
    end
    local start, duration = GetInventoryItemCooldown("player", 15)
    if start and duration and start > 0 and duration > 1.5 then
        return duration, start + duration
    end
    return 0, 0
end""",
                            "customIcon": """function()
    if _G.FMHUD_CloakBuffs then
        for i = 1, 40 do
            local name, _, icon, _, _, _, expirationTime = UnitBuff("player", i)
            if not name then break end
            if _G.FMHUD_CloakBuffs[name] then
                if expirationTime and expirationTime > GetTime() then
                    return icon
                end
            end
        end
    end
    return GetInventoryItemTexture("player", 15) or "Interface\\\\Icons\\\\INV_Misc_Cape_19"
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
            # 06 - MANA GEM (Item 33312 / 22044 - Centered row under Mana Bar)
            # =================================================================
            {
                "id": "06 - Mana Gem",
                "uid": "FMHUD_MANAGEM",
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 60,
                "yOffset": -54,
                "width": 28,
                "height": 28,
                "displayIcon": "Interface\\Icons\\INV_Misc_Gem_Sapphire_02",
                "cooldownSwipe": True,
                "customTextUpdate": "update",
                "customText": """function()
    local c = GetItemCount(33312, nil, true) or 0
    if c == 0 then
        c = GetItemCount(22044, nil, true) or 0
    end
    if c > 0 then
        return tostring(c)
    end
    return "|cFFFF22220|r"
end""",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "item",
                            "event": "Cooldown Progress (Item)",
                            "itemName": 33312,
                            "use_itemName": True,
                            "genericShowOn": "showAlways",
                            "use_genericShowOn": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=10),
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
            # 07 - MANA BAR (Aurabar)
            # =================================================================
            {
                "id": "07 - Mana Bar",
                "uid": "FMHUD_MANABAR",
                "parent": "Fire Mage HUD",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 220,
                "height": 14,
                "xOffset": 0,
                "yOffset": -23,
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
            # 08 - CASTBAR (Aurabar)
            # =================================================================
            {
                "id": "08 - Castbar",
                "uid": "FMHUD_CASTBAR",
                "parent": "Fire Mage HUD",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 220,
                "height": 20,
                "xOffset": 0,
                "yOffset": 0,
                "barColor": [1.0, 0.55, 0.0, 1.0],
                "backgroundColor": [0.15, 0.15, 0.15, 0.8],
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "icon": False,
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
                    make_subtext("%p", justify="RIGHT", anchor_point="INNER_RIGHT", font_size=11, extra_props={"anchorXOffset": -6}),
                    make_subtext("%n", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, extra_props={"anchorXOffset": 6}),
                ],
            },

            # =================================================================
            # 09 - GCD (Aurabar)
            # =================================================================
            {
                "id": "09 - GCD",
                "uid": "FMHUD_GCD",
                "parent": "Fire Mage HUD",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 220,
                "height": 3,
                "xOffset": 0,
                "yOffset": -12,
                "barColor": [1.0, 1.0, 1.0, 0.8],
                "backgroundColor": [0.0, 0.0, 0.0, 0.0],
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "spell",
                            "event": "Cooldown Progress (Spell)",
                            "spellName": 61304,
                            "use_spellName": True,
                            "genericShowOn": "showOnCooldown",
                            "use_genericShowOn": True,
                        },
                        "untrigger": {}
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    { "type": "subforeground" },
                ],
            },

            # =================================================================
            # 10 - ALERTS (Group)
            # =================================================================
            {
                "id": "10 - Alerts",
                "uid": "FMHUD_ALERTS_GRP",
                "parent": "Fire Mage HUD",
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
                "subRegions": [
                    make_subtext("|cFFFF5500HOT STREAK!|r\\n|cFFFFFF00PYROBLAST READY!|r", justify="CENTER", anchor_point="CENTER", font_size=20)
                ],
            }
        ]
    }
    return data

if __name__ == "__main__":
    wa_tree = build_wa_tree()
    wa_string = generate_wa_string(wa_tree)
    with open("IMPORT_STRING.txt", "w", encoding="utf-8") as f:
        f.write(wa_string)
    print(f"Generated !WA:1! String successfully! Length: {len(wa_string)}")
