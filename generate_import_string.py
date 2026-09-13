"""
Generator for Fire Mage HUD WeakAuras (WoW 3.3.5a - WeakAuras 4.0.0 backport)
Built to exactly match the native WeakAuras 4.0.0 (internalVersion 52) engine specifications.
Includes:
- Full ICD (Internal Cooldown) tracking for Trinket 1, Trinket 2, and Cloak.
- Exact spell ID and case-insensitive matching for Dying Curse (60494), Sundial (60064), etc.
- Molten Armor timer only when <= 5 minutes (clean otherwise).
- Arcane Intellect / Arcane Brilliance monitor with <= 5 min timer and OFF warning.
- Scorch / Improved Scorch debuff tracking with remaining seconds and <= 5s refresh alert.
- Master scale increased by 20% (scale = 1.2).
- Ergonomic position just above action bars (yOffset = -190).
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

# Core Lua function for shared slot tracking with ICD
SHARED_SLOT_CHECK_LUA = """function(slot)
    _G.FMHUD_ICD = _G.FMHUD_ICD or {
        [13] = { lastStart = 0, lastEnd = 0, isProc = false },
        [14] = { lastStart = 0, lastEnd = 0, isProc = false },
        [15] = { lastStart = 0, lastEnd = 0, isProc = false },
    }
    _G.FMHUD_TrinketDB = _G.FMHUD_TrinketDB or {
        [40255] = { buff = "Dying Curse", altBuff = "Curse of the Eye", spellId = 60494, icd = 45, dur = 10 },
        [40682] = { buff = "Now is the time!", altBuff = "Now is the Time!", spellId = 60064, icd = 45, dur = 10 },
        [50348] = { buff = "Celestial Infusion", spellId = 71601, icd = 45, dur = 20 },
        [50345] = { buff = "Celestial Infusion", spellId = 71644, icd = 45, dur = 20 },
        [50360] = { buff = "Siphon of Aethas", spellId = 71605, icd = 90, dur = 20 },
        [50365] = { buff = "Siphon of Aethas", altBuff = "Aethas' Siphon", spellId = 71636, icd = 90, dur = 20 },
        [54572] = { buff = "Shared Twilight", spellId = 75473, icd = 45, dur = 15 },
        [54588] = { buff = "Shared Twilight", spellId = 75466, icd = 45, dur = 15 },
        [45518] = { buff = "Elusive Power", spellId = 64713, icd = 45, dur = 10 },
        [47271] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
        [47477] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
        [47182] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
        [47316] = { buff = "Motes of Flame", altBuff = "Pillar of Flame", icd = 2, dur = 0 },
        [47213] = { buff = "Deadly Precision", spellId = 67669, icd = 45, dur = 10 },
        [37660] = { buff = "Forged Ember", spellId = 60479, icd = 45, dur = 10 },
        [40432] = { buff = "Dragon Soul", spellId = 60486, icd = 0, dur = 10 },
        [37264] = { buff = "Sudden Velocity", spellId = 60492, icd = 45, dur = 10 },
        [44253] = { buff = "Greatness", spellId = 60233, icd = 45, dur = 15 },
        [44255] = { buff = "Greatness", spellId = 60235, icd = 45, dur = 15 },
        [42987] = { buff = "Greatness", spellId = 60234, icd = 45, dur = 15 },
        [44254] = { buff = "Greatness", spellId = 60233, icd = 45, dur = 15 },
        [50340] = { buff = "Gathering Tracker", icd = 0, dur = 10 },
        [50353] = { buff = "Gathering Tracker", icd = 0, dur = 10 },
        [45466] = { buff = "Velocity", spellId = 64707, icd = 120, dur = 20 },
        [48724] = { buff = "Chilled Heart", spellId = 67696, icd = 120, dur = 20 },
        [48722] = { buff = "Volatile Power", spellId = 67702, icd = 120, dur = 20 },
        [50259] = { buff = "Deadly Precision", spellId = 71563, icd = 180, dur = 20 },
        [37873] = { buff = "Soul Power", icd = 120, dur = 20 },
        [50339] = { buff = "Pure Energy", icd = 120, dur = 0 },
        [50346] = { buff = "Pure Energy", icd = 120, dur = 0 },
        [47215] = { buff = "Revitalized", icd = 45, dur = 0 },
        [45490] = { buff = "Pandora's Plea", icd = 45, dur = 10 },
        [40685] = { buff = "Living Flame", icd = 120, dur = 20 },
        [50357] = { buff = "Maghia's Misguided Quill", icd = 120, dur = 20 },
    }
    _G.FMHUD_CloakBuffs = _G.FMHUD_CloakBuffs or {
        ["Lightweave"] = true,
        ["Darkglow"] = true,
        ["Swordguard"] = true,
        ["Parachute"] = true,
        ["Flexweave"] = true,
        ["Springy Arachnoweave"] = true,
    }

    local now = GetTime()
    local itemID = GetInventoryItemID("player", slot)
    local entry = itemID and _G.FMHUD_TrinketDB[itemID]
    local icdState = _G.FMHUD_ICD[slot]
    local targetICD = (entry and entry.icd) or (slot == 15 and 45) or 45
    local defaultDur = (entry and entry.dur) or (slot == 15 and 15) or 10

    local foundBuff = false
    local remBuff = 0
    local durBuff = 0
    local buffIcon = nil

    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        local isMatch = false
        if slot == 15 then
            if name == "Lightweave" or spellId == 55637 or spellId == 73849 or _G.FMHUD_CloakBuffs[name] then
                isMatch = true
            end
        elseif entry then
            if (entry.spellId and spellId == entry.spellId)
               or (entry.altSpellId and spellId == entry.altSpellId)
               or (entry.buff and string.lower(name) == string.lower(entry.buff))
               or (entry.altBuff and string.lower(name) == string.lower(entry.altBuff)) then
                isMatch = true
            end
        else
            local otherSlot = (slot == 13) and 14 or 13
            local otherID = GetInventoryItemID("player", otherSlot)
            local otherEntry = otherID and _G.FMHUD_TrinketDB[otherID]
            if _G.FMHUD_CasterProcs and _G.FMHUD_CasterProcs[name] and (not otherEntry or (name ~= otherEntry.buff and name ~= otherEntry.altBuff)) then
                isMatch = true
            end
        end

        if isMatch then
            foundBuff = true
            durBuff = (duration and duration > 0) and duration or defaultDur
            remBuff = (expirationTime and expirationTime > 0) and (expirationTime - now) or durBuff
            buffIcon = icon
            break
        end
    end

    if foundBuff then
        if not icdState.isProc or (now - icdState.lastStart > durBuff + 2) then
            icdState.lastStart = now - (durBuff - remBuff)
            icdState.lastEnd = icdState.lastStart + durBuff
            icdState.isProc = true
        end
        return "ACTIVE", remBuff, durBuff, buffIcon
    end

    if icdState.isProc then
        icdState.isProc = false
        if icdState.lastEnd == 0 or icdState.lastEnd > now then
            icdState.lastEnd = now
        end
    end

    -- Check if ICD is active
    if icdState.lastStart > 0 and targetICD > 0 then
        local elapsed = now - icdState.lastStart
        if elapsed < targetICD then
            local remICD = targetICD - elapsed
            return "ICD", remICD, targetICD, nil
        end
    end

    -- Check standard On-Use item cooldown
    local start, duration = GetInventoryItemCooldown("player", slot)
    if start and duration and start > 0 and duration > 1.5 then
        local remCD = (start + duration) - now
        if remCD > 0 then
            return "COOLDOWN", remCD, duration, nil
        end
    end

    return "READY", 0, 0, nil
end"""

def make_slot_custom_text(slot):
    return f"""function()
    _G.FMHUD_CheckSlot = _G.FMHUD_CheckSlot or {SHARED_SLOT_CHECK_LUA}
    local state, rem, dur, icon = _G.FMHUD_CheckSlot({slot})
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2)
        end
        return string.format("|cFFFFFF00%.1fs|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
        if state == "ICD" or state == "COOLDOWN" then
            return string.format("%.0f", rem)
        end
        return ""
    end
end"""

def make_slot_custom_duration(slot):
    return f"""function()
    _G.FMHUD_CheckSlot = _G.FMHUD_CheckSlot or {SHARED_SLOT_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckSlot({slot})
    if state == "ACTIVE" or state == "ICD" or state == "COOLDOWN" then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_slot_custom_icon(slot, default_icon):
    return f"""function()
    _G.FMHUD_CheckSlot = _G.FMHUD_CheckSlot or {SHARED_SLOT_CHECK_LUA}
    local state, rem, dur, icon = _G.FMHUD_CheckSlot({slot})
    if state == "ACTIVE" and icon then
        return icon
    end
    return GetInventoryItemTexture("player", {slot}) or "{default_icon}"
end"""

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
            "scale": 1.2,
            "xOffset": 0,
            "yOffset": -190,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "controlledChildren": [
                "01 - Procs",
                "02 - Molten Armor",
                "03 - Arcane Intellect",
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
            # 02 - MOLTEN ARMOR (Wing: Left side column - Bottom Icon)
            # =================================================================
            {
                "id": "02 - Molten Armor",
                "uid": "FMHUD_MOLTENARMOR_GRP",
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -160,
                "yOffset": -16,
                "controlledChildren": [
                    "Molten Armor - Active",
                    "Molten Armor - OFF"
                ],
            },
            # Molten Armor Active (Timer only shown when <= 5 minutes!)
            {
                "id": "Molten Armor - Active",
                "uid": "FMHUD_MA_ACTIVE",
                "parent": "02 - Molten Armor",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 32,
                "height": 32,
                "displayIcon": "Interface\\Icons\\Spell_Fire_Incinerate",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldownSwipe": True,
                "customTextUpdate": "update",
                "customText": """function()
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == "Molten Armor" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("|cFFFFFF00%d:%02d|r", m, s)
            end
            return ""
        end
    end
    return ""
end""",
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
                "width": 32,
                "height": 32,
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
                    make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
                ],
            },

            # =================================================================
            # 03 - ARCANE INTELLECT (Wing: Left side column - Top Icon)
            # =================================================================
            {
                "id": "03 - Arcane Intellect",
                "uid": "FMHUD_INTELLECT_GRP",
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -160,
                "yOffset": 22,
                "controlledChildren": [
                    "Arcane Intellect - Active",
                    "Arcane Intellect - OFF"
                ],
            },
            # Arcane Intellect Active (Timer only shown when <= 5 minutes!)
            {
                "id": "Arcane Intellect - Active",
                "uid": "FMHUD_AI_ACTIVE",
                "parent": "03 - Arcane Intellect",
                "regionType": "icon",
                "internalVersion": 52,
                "width": 32,
                "height": 32,
                "displayIcon": "Interface\\Icons\\Spell_Holy_MagicalSentry",
                "auto": True,
                "color": [1, 1, 1, 1],
                "cooldownSwipe": True,
                "customTextUpdate": "update",
                "customText": """function()
    local b = {
        ["Arcane Intellect"] = true,
        ["Arcane Brilliance"] = true,
        ["Dalaran Intellect"] = true,
        ["Dalaran Brilliance"] = true,
        ["Fel Intelligence"] = true,
    }
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if b[name] then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("|cFFFFFF00%d:%02d|r", m, s)
            end
            return ""
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
                                "Arcane Intellect",
                                "Arcane Brilliance",
                                "Dalaran Intellect",
                                "Dalaran Brilliance",
                                "Fel Intelligence"
                            ],
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
                "width": 32,
                "height": 32,
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
            # 04 - FOCUS MAGIC (Wing: Right side column)
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
            # 05 - TRINKET 1 (Slot 13 - With Active Proc & ICD Reproc Countdown)
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
                "customText": make_slot_custom_text(13),
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
                "customText": make_slot_custom_text(14),
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
                "customText": make_slot_custom_text(15),
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
