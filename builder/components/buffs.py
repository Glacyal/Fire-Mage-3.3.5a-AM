"""
Modulo Componente: 02 - Molten Armor, 03 - Arcane Intellect, 04 - Focus Magic
==============================================================================
Gestisce la colonna sinistra dei buff di classe (x = -190, -220, -160 a y = 0):
1. 02 - Molten Armor (Gruppo + Active [<= 5 min] + OFF [mancante])
2. 03 - Arcane Intellect (Gruppo + Active [<= 5 min] + OFF [mancante])
3. 04 - Focus Magic (Gruppo + Active [Proc 10s] + OFF [non assegnato a nessun alleato])
"""
from builder.core.helpers import make_subtext


# =============================================================================
# LOGICA LUA CONDIVISA: FOCUS MAGIC
# =============================================================================
SHARED_FM_CHECK_LUA = """function(event, ...)
    local state = _G.FMHUD_FMState
    if not state then
        state = { targetGUID = nil, targetName = nil, expires = 0 }
        _G.FMHUD_FMState = state
    end

    local now = GetTime()

    -- 1. Gestione Eventi Assegnazione, Rimozione e Morte
    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and (spell == "Focus Magic" or spell == "Focalizzazione Magica") then
            state.targetName = UnitName("target")
            state.targetGUID = UnitGUID("target")
            state.expires = now + 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        if sourceGUID == UnitGUID("player") and (spellId == 54646 or spellName == "Focus Magic" or spellName == "Focalizzazione Magica") then
            if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                state.targetName = destName
                state.targetGUID = destGUID
                state.expires = now + 1800
            elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                state.targetName = nil
                state.targetGUID = nil
                state.expires = 0
            end
        elseif subEvent == "UNIT_DIED" then
            if (state.targetGUID and destGUID == state.targetGUID) or (state.targetName and destName == state.targetName) then
                state.targetName = nil
                state.targetGUID = nil
                state.expires = 0
            end
        end
    end

    -- 2. Controllo se il player ha il proc di 10 secondi (Spell ID 54648, +3% Crit)
    local hasProc = false
    local procRem = 0
    local procDur = 10
    local procExp = 0
    for i = 1, 40 do
        local n, _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if spellId == 54648 or ((n == "Focus Magic" or n == "Focalizzazione Magica") and duration and duration <= 15) then
            hasProc = true
            procDur = (duration and duration > 0) and duration or 10
            procRem = (expirationTime and expirationTime > 0) and (expirationTime - now) or procDur
            procExp = (expirationTime and expirationTime > 0) and expirationTime or (now + procRem)
            break
        end
    end

    -- 3. Verifica se l'alleato registrato ha ancora il buff ed e vivo
    if state.expires and state.expires > now then
        if state.targetName and UnitExists(state.targetName) and UnitIsDead(state.targetName) then
            state.targetName = nil
            state.targetGUID = nil
            state.expires = 0
        else
            return hasProc, true, procRem, procDur, procExp
        end
    end

    -- 4. Scansione attiva su target, focus, raid o party (utile al login, reload o cambio zona)
    local allyActive = false
    if UnitExists("target") and UnitIsFriend("player", "target") and not UnitIsDead("target") then
        for i = 1, 40 do
            local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff("target", i)
            if not n then break end
            if (spellId == 54646 or n == "Focus Magic" or n == "Focalizzazione Magica") and (c == "player" or not c) then
                state.targetName = UnitName("target")
                state.targetGUID = UnitGUID("target")
                state.expires = (exp and exp > 0) and exp or (now + 1800)
                allyActive = true
                break
            end
        end
    end

    if not allyActive and UnitExists("focus") and UnitIsFriend("player", "focus") and not UnitIsDead("focus") then
        for i = 1, 40 do
            local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff("focus", i)
            if not n then break end
            if (spellId == 54646 or n == "Focus Magic" or n == "Focalizzazione Magica") and (c == "player" or not c) then
                state.targetName = UnitName("focus")
                state.targetGUID = UnitGUID("focus")
                state.expires = (exp and exp > 0) and exp or (now + 1800)
                allyActive = true
                break
            end
        end
    end

    if not allyActive then
        local nr = GetNumRaidMembers()
        if nr and nr > 0 then
            for r = 1, nr do
                local u = "raid"..r
                if not UnitIsDead(u) then
                    for i = 1, 40 do
                        local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff(u, i)
                        if not n then break end
                        if (spellId == 54646 or n == "Focus Magic" or n == "Focalizzazione Magica") and (c == "player" or not c) then
                            state.targetName = UnitName(u)
                            state.targetGUID = UnitGUID(u)
                            state.expires = (exp and exp > 0) and exp or (now + 1800)
                            allyActive = true
                            break
                        end
                    end
                    if allyActive then break end
                end
            end
        else
            local np = GetNumPartyMembers()
            if np and np > 0 then
                for p = 1, np do
                    local u = "party"..p
                    if not UnitIsDead(u) then
                        for i = 1, 40 do
                            local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff(u, i)
                            if not n then break end
                            if (spellId == 54646 or n == "Focus Magic" or n == "Focalizzazione Magica") and (c == "player" or not c) then
                                state.targetName = UnitName(u)
                                state.targetGUID = UnitGUID(u)
                                state.expires = (exp and exp > 0) and exp or (now + 1800)
                                allyActive = true
                                break
                            end
                        end
                        if allyActive then break end
                    end
                end
            end
        end
    end

    return hasProc, allyActive, procRem, procDur, procExp
end"""


def make_fm_trigger() -> str:
    """Trigger Lua per Focus Magic attivo (visibile solo durante il proc da 10s sul player)."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc = _G.FMHUD_CheckFM(event, ...)
    return hasProc == true
end"""


def make_fm_untrigger() -> str:
    """Untrigger Lua per Focus Magic attivo."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc = _G.FMHUD_CheckFM(event, ...)
    return not hasProc
end"""


def make_fm_custom_duration() -> str:
    """Durata e scadenza per lo swipe di ricarica di Focus Magic."""
    return f"""function()
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive, procRem, procDur, procExp = _G.FMHUD_CheckFM()
    if hasProc then
        return procDur, procExp
    end
    return 0, 0
end"""


def make_fm_custom_text() -> str:
    """Conto alla rovescia in secondi per il proc da 10s di Focus Magic."""
    return f"""function()
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive, procRem = _G.FMHUD_CheckFM()
    if hasProc and procRem > 0 then
        if procRem <= 3 then
            return string.format("|cFFFF4444%.1fs|r", procRem)
        else
            return string.format("%.0fs", procRem)
        end
    end
    return ""
end"""


def make_fm_off_trigger() -> str:
    """Trigger Lua per Focus Magic OFF (visibile se nessun alleato ha il buff e nessun proc attivo)."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive = _G.FMHUD_CheckFM(event, ...)
    return (not hasProc) and (not allyActive)
end"""


def make_fm_off_untrigger() -> str:
    """Untrigger Lua per Focus Magic OFF."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive = _G.FMHUD_CheckFM(event, ...)
    return hasProc or allyActive
end"""


# =============================================================================
# BUILDER: AURE WEAKAURAS PER LA COLONNA BUFF
# =============================================================================
def build_buffs_auras() -> list[dict]:
    """
    Costruisce e restituisce le 6 aure (3 gruppi da 2 nodi) per la colonna sinistra dei buff:
    - 02 - Molten Armor (Active + OFF)
    - 03 - Arcane Intellect (Active + OFF)
    - 04 - Focus Magic (Active + OFF)
    """
    return [
        # =====================================================================
        # 02 - MOLTEN ARMOR
        # =====================================================================
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },
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
                {"type": "subbackground"},
                make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },

        # =====================================================================
        # 03 - ARCANE INTELLECT
        # =====================================================================
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },
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
                {"type": "subbackground"},
                make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },

        # =====================================================================
        # 04 - FOCUS MAGIC
        # =====================================================================
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },
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
                {"type": "subbackground"},
                make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },
    ]
