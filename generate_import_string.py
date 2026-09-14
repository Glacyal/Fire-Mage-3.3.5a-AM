"""
Fire Mage HUD WeakAuras Suite Generator (WoW 3.3.5a - WeakAuras 4.0.0 Backport)
================================================================================
Generatore deterministico della stringa di importazione WeakAuras (!WA:1!) per la
suite Fire Mage Livello 80 in World of Warcraft 3.3.5a (Wrath of the Lich King).

Caratteristiche Architetturali:
- Engine Target: WeakAuras 4.0.0 (internalVersion 52) con supporto subRegions native.
- Formato di Codifica: AceSerializer-3.0 Protocol Rev 1 + Deflate compressione zlib
  + LibDeflate Little-Endian 6-bit Base64 encoding.
- Gerarchia Rigorosa: Tutti i 28 moduli sono nidificati sotto il gruppo master "Fire Mage HUD"
  per consentire spostamenti in blocco o disinstallazione pulita con un solo clic.
- Condizione di Caricamento: Classe Mago (Player Class: Mage) e talento Living Bomb (Fire),
  impostato su tutti i nodi foglia per conformità all'engine 3.3.5a.
- Tracciamento Cooldown Avanzato: ICD (Internal Cooldown) software per Trinket e Mantello,
  timer a orologio (cooldown swipe) e allerta rossa numerica (|cFFFF4444%.1fs|r) su tutti i proc.
- Layout Ergonomico: Barre centrali da 264px (+20%), colonna buff a sinistra (x = -182),
  fila utility a 6 icone simmetriche a y = -54.
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
    """Serializza una stringa nel formato AceSerializer-3.0 con sequenze di escape per caratteri di controllo."""
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

def serialize_value(v) -> str:
    """Serializza ricorsivamente valori Python (None, bool, int/float, str, dict, list) in formato AceSerializer."""
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

def ace_serialize(obj) -> str:
    """Incapsula un oggetto serializzato con l'header AceSerializer '^1' e il terminatore '^^'."""
    return '^1' + serialize_value(obj) + '^^'

def libdeflate_encode_for_print(data: bytes) -> str:
    """Codifica un buffer binario compresso secondo l'alfabeto personalizzato a 64 caratteri di LibDeflate."""
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

def generate_wa_string(data_table: dict) -> str:
    """Serializza, comprime con Deflate (livello 9) e codifica la tabella WeakAuras generando la stringa '!WA:1!'."""
    serialized = ace_serialize(data_table)
    comp_obj = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    compressed = comp_obj.compress(serialized.encode('latin1')) + comp_obj.flush()
    encoded = libdeflate_encode_for_print(compressed)
    return f"!WA:1!{encoded}"

def make_subtext(text: str, justify: str = "CENTER", anchor_point: str = "INNER_BOTTOM", font_size: int = 12, y_offset: int = 0, extra_props: dict = None) -> dict:
    """Genera la struttura per una subRegion di tipo subtext con font Expressway OUTLINE ad alta leggibilità."""
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
        [13] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
        [14] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
        [15] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
    }
    _G.FMHUD_TrinketDB = {
        -- The Dying Curse
        [40255] = { keywords = { "dyingcurse", "curseoftheeye", "thedyingcurse" }, spellIds = { [60494] = true, [60493] = true, [60492] = true, [60491] = true }, icd = 45, dur = 10 },
        -- Sundial of the Exiled
        [40682] = { keywords = { "nowisthetime", "sundial" }, spellIds = { [60064] = true, [60063] = true }, icd = 45, dur = 10 },
        -- Living Flame (On-Use)
        [40685] = { keywords = { "livingflame" }, spellIds = { [64701] = true, [60480] = true }, icd = 120, dur = 20, onUse = true },
        -- Mark of the War Prisoner (On-Use)
        [37873] = { keywords = { "soulpower" }, spellIds = { [60481] = true, [60480] = true }, icd = 120, dur = 20, onUse = true },
        -- Forge Ember
        [37660] = { keywords = { "forgedember", "forgeember" }, spellIds = { [60479] = true, [60478] = true }, icd = 45, dur = 10 },
        -- Embrace of the Spider
        [37264] = { keywords = { "suddenvelocity", "embraceofthespider" }, spellIds = { [60492] = true, [60491] = true }, icd = 45, dur = 10 },
        [39229] = { keywords = { "suddenvelocity", "embraceofthespider" }, spellIds = { [60492] = true, [60491] = true }, icd = 45, dur = 10 },
        -- Illustration of the Dragon Soul
        [40432] = { keywords = { "dragonsoul" }, spellIds = { [60486] = true, [60485] = true }, icd = 0, dur = 10 },
        -- Eye of the Broodmother
        [45308] = { keywords = { "broodmother", "blessingofthebroodmother" }, spellIds = { [65006] = true, [65004] = true, [65005] = true }, icd = 0, dur = 10 },
        -- DMC Greatness
        [44253] = { keywords = { "greatness" }, spellIds = { [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        [44255] = { keywords = { "greatness" }, spellIds = { [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        [42987] = { keywords = { "greatness" }, spellIds = { [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        [44254] = { keywords = { "greatness" }, spellIds = { [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        -- Scale of Fates (On-Use)
        [45466] = { keywords = { "velocity" }, spellIds = { [64707] = true, [64708] = true }, icd = 120, dur = 20, onUse = true },
        -- Flare of the Heavens
        [45518] = { keywords = { "elusivepower" }, spellIds = { [64713] = true, [64712] = true }, icd = 45, dur = 10 },
        -- Pandora's Plea
        [45490] = { keywords = { "pandorasplea", "pandora" }, spellIds = { [64741] = true, [64740] = true }, icd = 45, dur = 10 },
        -- Reign of the Dead / Unliving
        [47271] = { keywords = { "motesofflame", "pillarofflame" }, spellIds = { [67759] = true, [67760] = true }, icd = 2, dur = 0 },
        [47477] = { keywords = { "motesofflame", "pillarofflame" }, spellIds = { [67759] = true, [67760] = true }, icd = 2, dur = 0 },
        [47182] = { keywords = { "motesofflame", "pillarofflame" }, spellIds = { [67713] = true, [67714] = true }, icd = 2, dur = 0 },
        [47316] = { keywords = { "motesofflame", "pillarofflame" }, spellIds = { [67713] = true, [67714] = true }, icd = 2, dur = 0 },
        -- Abyssal Rune
        [47213] = { keywords = { "deadlyprecision" }, spellIds = { [67669] = true, [67668] = true }, icd = 45, dur = 10 },
        -- Talisman of Resurgence (On-Use)
        [48722] = { keywords = { "volatilepower" }, spellIds = { [67702] = true, [67701] = true }, icd = 120, dur = 20, onUse = true },
        -- Shard of the Crystal Heart (On-Use)
        [48724] = { keywords = { "chilledheart" }, spellIds = { [67696] = true, [67695] = true }, icd = 120, dur = 20, onUse = true },
        -- Dislodged Foreign Object
        [50348] = { keywords = { "celestialinfusion" }, spellIds = { [71601] = true, [71644] = true }, icd = 45, dur = 20 },
        [50345] = { keywords = { "celestialinfusion" }, spellIds = { [71601] = true, [71644] = true }, icd = 45, dur = 20 },
        -- Phylactery of the Nameless Lich
        [50360] = { keywords = { "siphonofaethas", "aethassiphon", "aethas" }, spellIds = { [71605] = true, [71636] = true }, icd = 90, dur = 20 },
        [50365] = { keywords = { "siphonofaethas", "aethassiphon", "aethas" }, spellIds = { [71605] = true, [71636] = true }, icd = 90, dur = 20 },
        -- Muradin's Spyglass
        [50340] = { keywords = { "gatheringtracker" }, spellIds = { [71570] = true, [71572] = true }, icd = 0, dur = 10 },
        [50353] = { keywords = { "gatheringtracker" }, spellIds = { [71570] = true, [71572] = true }, icd = 0, dur = 10 },
        -- Charred Twilight Scale
        [54572] = { keywords = { "sharedtwilight", "twilightflame" }, spellIds = { [75473] = true, [75466] = true }, icd = 45, dur = 15 },
        [54588] = { keywords = { "sharedtwilight", "twilightflame" }, spellIds = { [75473] = true, [75466] = true }, icd = 45, dur = 15 },
        -- Nevermelting Ice Crystal (On-Use)
        [50259] = { keywords = { "deadlyprecision" }, spellIds = { [71563] = true, [71562] = true }, icd = 180, dur = 20, onUse = true },
        -- Maghia's Misguided Quill (On-Use)
        [50357] = { keywords = { "maghiasmisguidedquill", "maghia", "elusivepower" }, spellIds = { [71584] = true }, icd = 120, dur = 20, onUse = true },
        -- Sliver of Pure Ice (On-Use)
        [50339] = { keywords = { "pureenergy" }, spellIds = { [71586] = true }, icd = 120, dur = 0, onUse = true },
        [50346] = { keywords = { "pureenergy" }, spellIds = { [71586] = true }, icd = 120, dur = 0, onUse = true },
        -- Tears of the Vanquished
        [47215] = { keywords = { "revitalized" }, spellIds = { [67700] = true }, icd = 45, dur = 0 },
        -- Jewelcrafting Figurines (On-Use)
        [42395] = { keywords = { "twilightserpent" }, spellIds = { [59757] = true }, icd = 120, dur = 20, onUse = true },
        [42413] = { keywords = { "sapphireowl" }, spellIds = { [59758] = true }, icd = 120, dur = 20, onUse = true },
        -- Cannoneer's
        [44013] = { keywords = { "fusillade" }, icd = 120, dur = 20, onUse = true },
        [44014] = { keywords = { "morale" }, icd = 120, dur = 20, onUse = true },
        -- DMC Death
        [42990] = { keywords = { "darkmooncarddeath" }, spellIds = { [60203] = true }, icd = 45, dur = 0 },
        -- Ashen Band
        [50398] = { keywords = { "peerlessdestruction" }, spellIds = { [73077] = true }, icd = 60, dur = 10 },
        [50400] = { keywords = { "peerlessdestruction" }, spellIds = { [73077] = true }, icd = 60, dur = 10 },
    }
    _G.FMHUD_AllCasterKeywords = {
        "dyingcurse", "curseoftheeye", "thedyingcurse", "nowisthetime", "sundial", "livingflame",
        "soulpower", "forgedember", "suddenvelocity", "dragonsoul", "broodmother",
        "blessingofthebroodmother", "greatness", "velocity", "elusivepower",
        "pandorasplea", "pandora", "motesofflame", "pillarofflame", "deadlyprecision",
        "volatilepower", "chilledheart", "celestialinfusion", "siphonofaethas",
        "aethassiphon", "aethas", "gatheringtracker", "sharedtwilight",
        "twilightflame", "twilightserpent", "sapphireowl", "pureenergy", "revitalized",
        "fusillade", "morale", "battlemaster", "medallion", "peerlessdestruction"
    }
    _G.FMHUD_CloakKeywords = { "lightweave", "darkglow", "swordguard", "parachute", "flexweave", "springyarachnoweave" }
    _G.FMHUD_CloakSpellIds = { [55637] = true, [73849] = true, [55775] = true, [55767] = true }

    local now = GetTime()
    _G.FMHUD_SlotCache = _G.FMHUD_SlotCache or {}
    if _G.FMHUD_SlotCache[slot] and _G.FMHUD_SlotCache[slot].time == now then
        local c = _G.FMHUD_SlotCache[slot]
        return c.state, c.rem, c.dur, c.icon
    end

    local function finish(st, r, d, ic)
        _G.FMHUD_SlotCache[slot] = { time = now, state = st, rem = r, dur = d, icon = ic }
        return st, r, d, ic
    end

    local itemID = nil
    if GetInventoryItemID then
        itemID = GetInventoryItemID("player", slot)
    end
    if not itemID then
        local link = GetInventoryItemLink("player", slot)
        if link then
            itemID = tonumber(link:match("item:(%d+)"))
        end
    end
    local icdState = _G.FMHUD_ICD[slot]
    if icdState.lastItemID and itemID and icdState.lastItemID ~= itemID then
        icdState.lastStart = 0
        icdState.lastEnd = 0
        icdState.isProc = false
    end
    if itemID then
        icdState.lastItemID = itemID
    end

    local entry = itemID and _G.FMHUD_TrinketDB[itemID]
    local targetICD = (entry and entry.icd) or ((slot == 15) and 45 or 45)
    local defaultDur = (entry and entry.dur) or ((slot == 15) and 15 or 10)

    -- Detect native On-Use cooldown
    local itemStart, itemDur = GetInventoryItemCooldown("player", slot)
    local isOnUseCooldown = false
    local remItemCD = 0
    if itemStart and itemDur and itemStart > 0 and itemDur > 1.5 then
        remItemCD = (itemStart + itemDur) - now
        if remItemCD > 0.1 then
            isOnUseCooldown = true
        end
    end

    -- Identify the OTHER trinket slot
    local otherSlot = (slot == 13) and 14 or ((slot == 14) and 13 or nil)
    local otherID = nil
    if otherSlot then
        if GetInventoryItemID then otherID = GetInventoryItemID("player", otherSlot) end
        if not otherID then
            local otherLink = GetInventoryItemLink("player", otherSlot)
            if otherLink then otherID = tonumber(otherLink:match("item:(%d+)")) end
        end
    end
    local otherEntry = otherID and _G.FMHUD_TrinketDB[otherID]

    local foundBuff = false
    local remBuff = 0
    local durBuff = 0
    local buffIcon = nil

    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        local isMatch = false
        local cName = string.lower(name):gsub("[%s%p%c]", "")

        if slot == 15 then
            if spellId and _G.FMHUD_CloakSpellIds[spellId] then
                isMatch = true
            else
                for _, kw in ipairs(_G.FMHUD_CloakKeywords) do
                    if cName:find(kw) then isMatch = true break end
                end
            end
        else
            -- 1. Direct match with this slot's known entry
            if entry then
                if spellId and entry.spellIds and entry.spellIds[spellId] then
                    isMatch = true
                elseif entry.keywords then
                    for _, kw in ipairs(entry.keywords) do
                        if cName:find(kw) then isMatch = true break end
                    end
                end
            end

            -- 2. Fallback matching if not matched directly
            if not isMatch then
                local isOther = false
                if otherEntry then
                    if spellId and otherEntry.spellIds and otherEntry.spellIds[spellId] then
                        isOther = true
                    elseif otherEntry.keywords then
                        for _, kw in ipairs(otherEntry.keywords) do
                            if cName:find(kw) then isOther = true break end
                        end
                    end
                end

                if not isOther then
                    for _, kw in ipairs(_G.FMHUD_AllCasterKeywords) do
                        if cName:find(kw) then isMatch = true break end
                    end
                end
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

    -- State 1: Active proc / buff on player
    if foundBuff then
        if not icdState.isProc or (now - icdState.lastStart > durBuff + 2) then
            icdState.lastStart = now - (durBuff - remBuff)
            icdState.lastEnd = icdState.lastStart + durBuff
            icdState.isProc = true
        end
        return finish("ACTIVE", remBuff, durBuff, buffIcon)
    end

    if icdState.isProc then
        icdState.isProc = false
        if icdState.lastEnd == 0 or icdState.lastEnd > now then
            icdState.lastEnd = now
        end
    end

    -- State 2: Native On-Use item cooldown (e.g. 120s / 180s)
    if isOnUseCooldown then
        return finish("COOLDOWN", remItemCD, itemDur, nil)
    end

    -- State 3: Internal Cooldown (ICD) before next reproc
    if icdState.lastStart > 0 and targetICD > 0 then
        local elapsed = now - icdState.lastStart
        if elapsed < targetICD then
            local remICD = targetICD - elapsed
            return finish("ICD", remICD, targetICD, nil)
        end
    end

    -- State 4: Ready
    return finish("READY", 0, 0, nil)
end"""

def make_slot_custom_text(slot: int) -> str:
    """Genera la closure Lua per il testo descrittivo del monile/mantello (%c), con pixel glow su proc attivo."""
    return f"""function()
    if not _G.FMHUD_CheckSlot_v5 then
        _G.FMHUD_CheckSlot = {SHARED_SLOT_CHECK_LUA}
        _G.FMHUD_CheckSlot_v5 = true
    end
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
        if (state == "ICD" or state == "COOLDOWN") and rem > 0.1 then
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
end"""

def make_slot_custom_duration(slot: int) -> str:
    """Genera la closure Lua per la durata e scadenza dello swipe di ricarica per lo slot indicato."""
    return f"""function()
    if not _G.FMHUD_CheckSlot_v5 then
        _G.FMHUD_CheckSlot = {SHARED_SLOT_CHECK_LUA}
        _G.FMHUD_CheckSlot_v5 = true
    end
    local state, rem, dur = _G.FMHUD_CheckSlot({slot})
    if (state == "ACTIVE" or state == "ICD" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_slot_custom_icon(slot: int, default_icon: str) -> str:
    """Genera la closure Lua per determinare dinamicamente l'icona dell'oggetto equipaggiato o del proc attivo."""
    return f"""function()
    if not _G.FMHUD_CheckSlot_v5 then
        _G.FMHUD_CheckSlot = {SHARED_SLOT_CHECK_LUA}
        _G.FMHUD_CheckSlot_v5 = true
    end
    local state, rem, dur, icon = _G.FMHUD_CheckSlot({slot})
    if state == "ACTIVE" and icon then
        return icon
    end
    return GetInventoryItemTexture("player", {slot}) or "{default_icon}"
end"""

SHARED_FM_CHECK_LUA = """function(event, ...)
    FMHUD_State = FMHUD_State or {}
    local now = GetTime()

    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and (spell == "Focus Magic" or spell == "Focalizzazione Magica") then
            FMHUD_State.FMTarget = UnitName("target") or "Ally"
            FMHUD_State.FMExpires = now + 1800
            FMHUD_State.FMDur = 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        local isFM = (spellName == "Focus Magic" or spellName == "Focalizzazione Magica" or spellId == 54646 or spellId == 54648)
        if isFM then
            -- Assegnazione sull'alleato da parte del mago (spellId 54646, buff 30 minuti)
            if sourceGUID == UnitGUID("player") and spellId ~= 54648 then
                if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                    FMHUD_State.FMTarget = destName or "Ally"
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMDur = 1800
                elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                    FMHUD_State.FMExpires = 0
                    FMHUD_State.FMTarget = nil
                end
            -- Attivazione proc critico sul mago (spellId 54648, 10s): conferma assoluta del buff attivo sull'alleato!
            elseif destGUID == UnitGUID("player") and (subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH") then
                if not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMDur = 1800
                end
            end
        elseif subEvent == "UNIT_DIED" and FMHUD_State.FMTarget and destName == FMHUD_State.FMTarget then
            FMHUD_State.FMExpires = 0
            FMHUD_State.FMTarget = nil
        end
    end

    local b1 = "Focus Magic"
    local b2 = "Focalizzazione Magica"
    local found = false

    -- 1. Controllo proc attivo di 10 secondi sul player (prova diretta che il buff sull'alleato è attivo)
    for i = 1, 40 do
        local n, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if spellId == 54648 or n == b1 or n == b2 then
            -- Mantiene viva la durata dell'alleato senza mai sovrascriverla con i 10 secondi del proc
            if not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                FMHUD_State.FMExpires = now + 1800
                FMHUD_State.FMDur = 1800
            end
            found = true
            break
        end
    end

    -- 2. Controllo bersaglio alleato (target)
    if not found and UnitExists("target") and UnitIsFriend("player", "target") then
        for i = 1, 40 do
            local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff("target", i)
            if not n then break end
            if (n == b1 or n == b2 or spellId == 54646) and (c == "player" or not c) then
                if exp and exp > 0 then
                    FMHUD_State.FMExpires = exp
                    FMHUD_State.FMDur = dur or 1800
                elseif not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMDur = 1800
                end
                FMHUD_State.FMTarget = UnitName("target")
                found = true
                break
            end
        end
    end

    -- 3. Controllo focus alleato
    if not found and UnitExists("focus") and UnitIsFriend("player", "focus") then
        for i = 1, 40 do
            local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff("focus", i)
            if not n then break end
            if (n == b1 or n == b2 or spellId == 54646) and (c == "player" or not c) then
                if exp and exp > 0 then
                    FMHUD_State.FMExpires = exp
                    FMHUD_State.FMDur = dur or 1800
                elseif not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                    FMHUD_State.FMExpires = now + 1800
                    FMHUD_State.FMDur = 1800
                end
                FMHUD_State.FMTarget = UnitName("focus")
                found = true
                break
            end
        end
    end

    -- 4. Scansione membri del Raid o del Party
    if not found then
        local nr = GetNumRaidMembers()
        if nr and nr > 0 then
            for r = 1, nr do
                local u = "raid"..r
                for i = 1, 40 do
                    local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff(u, i)
                    if not n then break end
                    if (n == b1 or n == b2 or spellId == 54646) and (c == "player" or not c) then
                        if exp and exp > 0 then
                            FMHUD_State.FMExpires = exp
                            FMHUD_State.FMDur = dur or 1800
                        elseif not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                            FMHUD_State.FMExpires = now + 1800
                            FMHUD_State.FMDur = 1800
                        end
                        FMHUD_State.FMTarget = UnitName(u)
                        found = true
                        break
                    end
                end
                if found then break end
            end
        else
            local np = GetNumPartyMembers()
            if np and np > 0 then
                for p = 1, np do
                    local u = "party"..p
                    for i = 1, 40 do
                        local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff(u, i)
                        if not n then break end
                        if (n == b1 or n == b2 or spellId == 54646) and (c == "player" or not c) then
                            if exp and exp > 0 then
                                FMHUD_State.FMExpires = exp
                                FMHUD_State.FMDur = dur or 1800
                            elseif not FMHUD_State.FMExpires or FMHUD_State.FMExpires <= now then
                                FMHUD_State.FMExpires = now + 1800
                                FMHUD_State.FMDur = 1800
                            end
                            FMHUD_State.FMTarget = UnitName(u)
                            found = true
                            break
                        end
                    end
                    if found then break end
                end
            end
        end
    end

    local rem = (FMHUD_State.FMExpires and FMHUD_State.FMExpires > now) and (FMHUD_State.FMExpires - now) or 0
    local dur = FMHUD_State.FMDur or 1800
    local exp = FMHUD_State.FMExpires or 0
    return rem, dur, exp
end"""

def make_fm_trigger() -> str:
    """Genera il trigger Lua per Focus Magic attivo con durata residua <= 5 minuti (300s)."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local rem, dur, exp = _G.FMHUD_CheckFM(event, ...)
    if rem > 0 and rem <= 300 then
        return true
    end
    return false
end"""

def make_fm_untrigger() -> str:
    """Genera l'untrigger Lua per nascondere Focus Magic se > 5m o scaduto."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local rem, dur, exp = _G.FMHUD_CheckFM(event, ...)
    if rem > 0 and rem <= 300 then
        return false
    end
    return true
end"""

def make_fm_custom_duration() -> str:
    """Genera la closure Lua per la durata e scadenza dello swipe circolare di Focus Magic."""
    return f"""function()
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local rem, dur, exp = _G.FMHUD_CheckFM()
    if rem > 0 and rem <= 300 then
        return dur, exp
    end
    return 0, 0
end"""

def make_fm_custom_text() -> str:
    """Genera il conto alla rovescia (%c) per Focus Magic attivo: m:ss in giallo (> 60s), secondi in rosso (<= 60s)."""
    return f"""function()
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local rem = _G.FMHUD_CheckFM()
    if rem > 60 then
        local m = math.floor(rem / 60)
        local s = math.floor(rem % 60)
        return string.format("|cFFFFFF00%d:%02d|r", m, s)
    elseif rem > 0 then
        return string.format("|cFFFF4444%.0fs|r", rem)
    end
    return ""
end"""

def make_fm_off_trigger() -> str:
    """Genera il trigger Lua per lo stato OFF di Focus Magic se il buff non è assegnato ad alcun alleato."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local rem = _G.FMHUD_CheckFM(event, ...)
    if rem <= 0 then
        -- Verifica di sicurezza: se il proc da 10s è attivo sul player, non mostrare mai OFF
        for i = 1, 40 do
            local n, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
            if not n then break end
            if spellId == 54648 or n == "Focus Magic" or n == "Focalizzazione Magica" then
                return false
            end
        end
        return true
    end
    return false
end"""

def make_fm_off_untrigger() -> str:
    """Disattiva lo stato OFF non appena Focus Magic risulta attivo su un alleato."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local rem = _G.FMHUD_CheckFM(event, ...)
    if rem <= 0 then
        for i = 1, 40 do
            local n, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
            if not n then break end
            if spellId == 54648 or n == "Focus Magic" or n == "Focalizzazione Magica" then
                return true
            end
        end
        return false
    end
    return true
end"""

SHARED_COMBUSTION_CHECK_LUA = """function()
    local now = GetTime()
    
    -- 1. Check if Combustion buff is ACTIVE on player
    for i = 1, 40 do
        local name, _, icon, count, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == "Combustion" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or 0
            local dur = duration and duration > 0 and duration or 0
            return "ACTIVE", rem, dur, count or 1, icon or "Interface\\\\Icons\\\\Spell_Fire_SealOfFire"
        end
    end
    
    -- 2. Check if Combustion spell is on COOLDOWN (Spell ID 11129)
    local start, duration = GetSpellCooldown(11129)
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Combustion")
    end
    if start and duration and start > 0 and duration > 1.5 then
        local remCD = (start + duration) - now
        if remCD > 0.1 then
            return "COOLDOWN", remCD, duration, 0, "Interface\\\\Icons\\\\Spell_Fire_SealOfFire"
        end
    end
    
    -- 3. READY
    return "READY", 0, 0, 0, "Interface\\\\Icons\\\\Spell_Fire_SealOfFire"
end"""

def make_combustion_custom_text() -> str:
    """Genera il testo descrittivo (%c) di Combustion con conteggio cariche critiche e pixel glow dorato."""
    return f"""function()
    _G.FMHUD_CheckCombustion = _G.FMHUD_CheckCombustion or {SHARED_COMBUSTION_CHECK_LUA}
    local state, rem, dur, count = _G.FMHUD_CheckCombustion()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2)
        end
        if count and count > 0 then
            return string.format("|cFFFFFF00x%d|r", count)
        elseif rem > 0 then
            return string.format("|cFFFFFF00%.1fs|r", rem)
        end
        return "|cFFFFFF00ON|r"
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
end"""

def make_combustion_custom_duration() -> str:
    """Genera la durata e scadenza per lo swipe di Combustion (CD o buff attivo)."""
    return f"""function()
    _G.FMHUD_CheckCombustion = _G.FMHUD_CheckCombustion or {SHARED_COMBUSTION_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckCombustion()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

SHARED_MIRRORIMAGE_CHECK_LUA = """function()
    local now = GetTime()
    local baseIcon = GetSpellTexture(55342) or "Interface\\\\Icons\\\\Spell_Magic_LesserInvisibilty"
    local quadCoreIcon = GetSpellTexture(70747) or "Interface\\\\Icons\\\\Spell_Nature_Invisibilty"
    
    -- 1. Controllo pezzi T10 equipaggiati (Elmo 50069/51159/51284, Spalle 50073/51155/51280, Veste 50070/51158/51283, Guanti 50071/51157/51282, Gambe 50072/51156/51281)
    local hasT10_4P = false
    local t10Pieces = {
        [50069]=true,[51159]=true,[51284]=true,
        [50073]=true,[51155]=true,[51280]=true,
        [50070]=true,[51158]=true,[51283]=true,
        [50071]=true,[51157]=true,[51282]=true,
        [50072]=true,[51156]=true,[51281]=true,
    }
    local t10Count = 0
    for _, slot in ipairs({1, 3, 5, 7, 10}) do
        local id = GetInventoryItemID("player", slot)
        if id and t10Pieces[id] then
            t10Count = t10Count + 1
        end
    end
    if t10Count >= 4 then
        hasT10_4P = true
    end

    -- 2. Controllo buff T10 4P ("Quad Core", Spell ID 70747 / +18% danni) o buff Mirror Image attivo
    for i = 1, 40 do
        local name, _, buffIcon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 70747 or spellId == 70748 or spellId == 70754 or spellId == 70752 or 
           name == "Quad Core" or name == "Item - Mage T10 4P Bonus" then
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or 0
            local dur = (duration and duration > 0) and duration or 30
            local icon = buffIcon or quadCoreIcon
            return "ACTIVE", rem, dur, icon, true
        elseif name == "Mirror Image" or name == "Immagine Speculare" or spellId == 55342 then
            local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or 0
            local dur = (duration and duration > 0) and duration or 30
            local icon = hasT10_4P and (buffIcon or quadCoreIcon) or baseIcon
            return "ACTIVE", rem, dur, icon, hasT10_4P
        end
    end
    
    -- 3. Controllo cooldown dell'abilita' Copie (55342)
    local start, duration = GetSpellCooldown(55342)
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Mirror Image")
    end
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Immagine Speculare")
    end
    
    if start and duration and start > 0 and duration > 1.5 then
        local elapsed = now - start
        -- Le copie durano 30 secondi dal cast: se entro i 30s, siamo in fase ATTIVA delle copie
        if elapsed >= 0 and elapsed < 30 then
            local remActive = 30 - elapsed
            -- Se il buff T10 non e' presente in UnitBuff, mostrare SEMPRE l'icona base delle copie
            return "ACTIVE", remActive, 30, baseIcon, false
        else
            local remCD = (start + duration) - now
            if remCD > 0.1 then
                return "COOLDOWN", remCD, duration, baseIcon, false
            end
        end
    end
    
    -- 4. PRONTO
    return "READY", 0, 0, baseIcon, false
end"""

def make_mirrorimage_custom_text() -> str:
    """Genera il testo descrittivo (%c) delle Copie (Mirror Image): durata attiva 30s con proc T10 (+18% danni) o CD 3 min."""
    return f"""function()
    if not _G.FMHUD_CheckMirrorImage_v4 then
        _G.FMHUD_CheckMirrorImage = {SHARED_MIRRORIMAGE_CHECK_LUA}
        _G.FMHUD_CheckMirrorImage_v4 = true
    end
    local state, rem, dur, icon, isT10 = _G.FMHUD_CheckMirrorImage()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)

    -- Aggiornamento immediato texture: Quad Core SOLO durante proc T10 attivo, altrimenti SEMPRE Copie standard
    if aura_env and aura_env.region then
        local defIcon = GetSpellTexture(55342) or "Interface\\\\Icons\\\\Spell_Magic_LesserInvisibilty"
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
                LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2)
            else
                LCG.PixelGlow_Start(aura_env.region, {{0.2, 0.8, 1.0, 1}}, 8, 0.25, 10, 2)
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
end"""

def make_mirrorimage_custom_duration() -> str:
    """Genera la durata e scadenza per lo swipe di Mirror Image / proc T10."""
    return f"""function()
    if not _G.FMHUD_CheckMirrorImage_v4 then
        _G.FMHUD_CheckMirrorImage = {SHARED_MIRRORIMAGE_CHECK_LUA}
        _G.FMHUD_CheckMirrorImage_v4 = true
    end
    local state, rem, dur = _G.FMHUD_CheckMirrorImage()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_mirrorimage_custom_icon() -> str:
    """Restituisce dinamicamente l'icona Quad Core (Spell_Nature_Invisibilty) durante il proc T10, altrimenti Mirror Image."""
    return f"""function()
    if not _G.FMHUD_CheckMirrorImage_v4 then
        _G.FMHUD_CheckMirrorImage = {SHARED_MIRRORIMAGE_CHECK_LUA}
        _G.FMHUD_CheckMirrorImage_v4 = true
    end
    local state, rem, dur, icon, isT10 = _G.FMHUD_CheckMirrorImage()
    if state == "ACTIVE" and isT10 and icon then
        return icon
    end
    return GetSpellTexture(55342) or "Interface\\\\Icons\\\\Spell_Magic_LesserInvisibilty"
end"""

SHARED_MANAGEM_CHECK_LUA = """function()
    local now = GetTime()
    local isT7Active = false
    local remT7 = 0
    local durT7 = 15
    local baseIcon = "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
    local procIcon = nil

    -- 1. Controllo buff bonus 2 pezzi T7 Mago (+225 Spell Power per 15s dopo l'uso della gemma)
    for i = 1, 40 do
        local n, _, icon, _, _, dur, exp, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if spellId == 61062 or spellId == 37445 or spellId == 37446 or spellId == 37447 or spellId == 54043 or
           n == "Mana Surge" or n == "Improved Mana Gems" or n == "Gemme di Mana Migliorate" or 
           n == "Gemme del Mana Migliorate" or n == "Gemma del Mana Migliorata" or n == "Ondata di Mana" then
            local rem = (exp and exp > now) and (exp - now) or 0
            if exp == 0 or exp == nil then
                rem = (dur and dur > 0) and dur or 15
            end
            if rem > 0.05 or exp == 0 or exp == nil then
                isT7Active = true
                remT7 = rem
                durT7 = (dur and dur > 0) and dur or 15
                procIcon = icon or GetSpellTexture(61062) or GetSpellTexture(37447) or "Interface\\\\Icons\\\\Spell_Arcane_ManaSurge" or "Interface\\\\Icons\\\\Spell_Holy_MagicalSentry"
                break
            end
        end
    end

    -- 2. Controllo cooldown oggetto Gemma del Mana (Mana Sapphire 33312, Mana Emerald 22044)
    local start, duration = GetItemCooldown(33312)
    if not start or duration == 0 then
        start, duration = GetItemCooldown(22044)
    end
    local isCD = false
    local remCD = 0
    if start and duration and duration > 1.5 and (start + duration) > now then
        remCD = (start + duration) - now
        if remCD > 0.1 then
            isCD = true
        end
    end

    if isT7Active then
        local activeIcon = procIcon or GetSpellTexture(61062) or "Interface\\\\Icons\\\\Spell_Arcane_ManaSurge" or "Interface\\\\Icons\\\\Spell_Holy_MagicalSentry"
        return "ACTIVE", remT7, durT7, activeIcon
    elseif isCD then
        return "COOLDOWN", remCD, duration, baseIcon
    else
        return "READY", 0, 0, baseIcon
    end
end"""

def make_managem_custom_text() -> str:
    """Genera il testo descrittivo (%c) delle cariche della Gemma del Mana, gestendo il Pixel Glow durante il proc T7 e icon swap."""
    return f"""function()
    if not _G.FMHUD_CheckManaGem_v4 then
        _G.FMHUD_CheckManaGem = {SHARED_MANAGEM_CHECK_LUA}
        _G.FMHUD_CheckManaGem_v4 = true
    end
    local state, rem, dur, icon = _G.FMHUD_CheckManaGem()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)

    -- Aggiornamento immediato texture dell'icona: Mana Surge SOLO durante proc T7 attivo, altrimenti SEMPRE Gemma standard
    if aura_env and aura_env.region then
        local defIcon = "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
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

    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2)
        end
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region)
        end
    end

    -- Imposta il colore del timer a sud (%p): Giallo durante il proc T7, Bianco durante il cooldown
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

    -- Conteggio cariche disponibili in borsa per la subRegion in alto a destra (%c)
    local c = GetItemCount(33312, nil, true) or 0
    if c == 0 then
        c = GetItemCount(22044, nil, true) or 0
    end
    if c > 0 then
        return tostring(c)
    end
    return "|cFFFF22220|r"
end"""

def make_managem_custom_duration() -> str:
    """Genera la durata e scadenza per lo swipe di ricarica della Gemma del Mana (durata T7 o CD oggetto)."""
    return f"""function()
    if not _G.FMHUD_CheckManaGem_v4 then
        _G.FMHUD_CheckManaGem = {SHARED_MANAGEM_CHECK_LUA}
        _G.FMHUD_CheckManaGem_v4 = true
    end
    local state, rem, dur, icon = _G.FMHUD_CheckManaGem()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_managem_custom_icon() -> str:
    """Restituisce dinamicamente la texture del proc T7 (Mana Surge) durante il buff attivo, altrimenti Mana Sapphire."""
    return f"""function()
    if not _G.FMHUD_CheckManaGem_v4 then
        _G.FMHUD_CheckManaGem = {SHARED_MANAGEM_CHECK_LUA}
        _G.FMHUD_CheckManaGem_v4 = true
    end
    local state, rem, dur, icon = _G.FMHUD_CheckManaGem()
    if state == "ACTIVE" and icon then
        return icon
    end
    return "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
end"""

SHARED_SMART_LB_CHECK_LUA = """function()
    _G.FMHUD_SmartLB = _G.FMHUD_SmartLB or {
        LB_Active  = {},
        LastUpdate = 0,
        Slots      = {},
    }

    if not _G.FMHUD_SmartLB_OnCombatLog then
        _G.FMHUD_SmartLB_OnCombatLog = function(...)
            local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
            local lb = _G.FMHUD_SmartLB.LB_Active
            if not destGUID then return end

            if sourceGUID == UnitGUID("player") then
                local isLB = (spellName == "Living Bomb" or spellName == "Bomba Vivente" or spellId == 44457 or spellId == 55359 or spellId == 55360)
                if isLB then
                    if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" then
                        lb[destGUID] = { exp = GetTime() + 12.0, name = destName or "Enemy", guid = destGUID }
                    elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                        lb[destGUID] = nil
                    end
                end
            end

            if subEvent == "UNIT_DIED" or subEvent == "PARTY_KILL" then
                lb[destGUID] = nil
            end
        end
    end

    if not _G.FMHUD_SmartLB_GetSlotData then
        _G.FMHUD_SmartLB_GetSlotData = function(slotIndex, customConfig)
            local now = GetTime()
            local state = _G.FMHUD_SmartLB

            if (now - (state.LastUpdate or 0)) >= 0.08 or not state.Slots then
                state.LastUpdate = now

                for guid, data in pairs(state.LB_Active) do
                    local exp = (type(data) == "table") and data.exp or data
                    if exp <= now then state.LB_Active[guid] = nil end
                end

                local cfg = customConfig or {}
                local globalCfg = _G.FireMageHUD_Config and _G.FireMageHUD_Config.SmartLivingBomb or _G.FMHUD_SmartLB_Config or {}
                local medMin     = cfg.medMin or globalCfg.MedMin or 40
                local medMax     = cfg.medMax or globalCfg.MedMax or 70
                local highMax    = cfg.highMax or globalCfg.HighMax or 100
                local maxEntries = cfg.maxEntries or globalCfg.MaxEntries or 5

                local seenGUIDs = {}
                local activeLB = {}
                local missingLB = {}

                local function inspectUnit(u)
                    if not UnitExists(u) then return end
                    if UnitIsDeadOrGhost(u) then return end
                    if not UnitCanAttack("player", u) or UnitIsFriend("player", u) then return end

                    local guid = UnitGUID(u)
                    if not guid or seenGUIDs[guid] then return end
                    seenGUIDs[guid] = true

                    local hp = UnitHealth(u) or 0
                    local maxHp = UnitHealthMax(u) or 1
                    if hp <= 0 then return end

                    local pct = (maxHp > 0) and math.floor((hp / maxHp) * 100) or 100
                    if pct > 100 then pct = 100 end
                    if pct < 0 then pct = 0 end

                    local name = UnitName(u) or "Enemy"
                    if name == "" then name = "Enemy" end

                    local hasLB = false
                    local lbExp = 0
                    for i = 1, 40 do
                        local debName, _, _, _, _, _, exp, caster, _, _, debSpellId = UnitDebuff(u, i)
                        if not debName then break end
                        if (debName == "Living Bomb" or debName == "Bomba Vivente" or debSpellId == 55360 or debSpellId == 55359 or debSpellId == 44457) and (caster == "player" or not caster) then
                            hasLB = true
                            lbExp = (exp and exp > 0) and exp or (now + 12.0)
                            state.LB_Active[guid] = { exp = lbExp, name = name, guid = guid, unit = u }
                            break
                        end
                    end

                    if not hasLB and state.LB_Active[guid] then
                        local lbData = state.LB_Active[guid]
                        local exp = (type(lbData) == "table") and lbData.exp or lbData
                        if exp > now then
                            hasLB = true
                            lbExp = exp
                        end
                    end

                    if hasLB then
                        table.insert(activeLB, { guid = guid, name = name, hpPct = pct, unit = u, hasLB = true, exp = lbExp, tier = 1, isTop = false })
                    else
                        table.insert(missingLB, { guid = guid, name = name, hpPct = pct, unit = u, hasLB = false, exp = 0, tier = 1, isTop = false })
                    end
                end

                inspectUnit("target")
                inspectUnit("focus")
                inspectUnit("mouseover")
                inspectUnit("targettarget")
                inspectUnit("focustarget")
                inspectUnit("boss1")
                inspectUnit("boss2")
                inspectUnit("boss3")
                inspectUnit("boss4")

                local numRaid = GetNumRaidMembers()
                if numRaid and numRaid > 0 then
                    local limit = math.min(numRaid, 40)
                    for r = 1, limit do inspectUnit("raid" .. r .. "target") end
                else
                    local numParty = GetNumPartyMembers()
                    if numParty and numParty > 0 then
                        for p = 1, numParty do inspectUnit("party" .. p .. "target") end
                    end
                end

                for guid, lbData in pairs(state.LB_Active) do
                    if not seenGUIDs[guid] then
                        local exp = (type(lbData) == "table") and lbData.exp or lbData
                        local name = (type(lbData) == "table") and lbData.name or "Enemy"
                        if exp > now then
                            seenGUIDs[guid] = true
                            table.insert(activeLB, { guid = guid, name = name, hpPct = 100, unit = nil, hasLB = true, exp = exp, tier = 1, isTop = false })
                        end
                    end
                end

                table.sort(activeLB, function(a, b) return a.exp < b.exp end)

                local tier1_Med = {}
                local tier2_High = {}
                local tier3_Low = {}
                for _, mob in ipairs(missingLB) do
                    if mob.hpPct >= medMin and mob.hpPct <= medMax then
                        mob.tier = 1
                        table.insert(tier1_Med, mob)
                    elseif mob.hpPct > medMax and mob.hpPct <= highMax then
                        mob.tier = 2
                        table.insert(tier2_High, mob)
                    else
                        mob.tier = 3
                        table.insert(tier3_Low, mob)
                    end
                end

                table.sort(tier1_Med, function(a, b) return a.hpPct > b.hpPct end)
                table.sort(tier2_High, function(a, b) return a.hpPct < b.hpPct end)
                table.sort(tier3_Low, function(a, b) return a.hpPct > b.hpPct end)

                local sortedMissing = {}
                for _, m in ipairs(tier1_Med) do table.insert(sortedMissing, m) end
                for _, m in ipairs(tier2_High) do table.insert(sortedMissing, m) end
                for _, m in ipairs(tier3_Low) do table.insert(sortedMissing, m) end

                if #sortedMissing > 0 then
                    sortedMissing[1].isTop = true
                end

                local slots = {}
                for _, m in ipairs(activeLB) do
                    if #slots < maxEntries then table.insert(slots, m) end
                end
                for _, m in ipairs(sortedMissing) do
                    if #slots < maxEntries then table.insert(slots, m) end
                end
                state.Slots = slots
            end

            return state.Slots and state.Slots[slotIndex] or nil
        end
    end

    if not _G.FMHUD_SmartLB_HasData then
        _G.FMHUD_SmartLB_HasData = function(customConfig)
            if UnitInVehicle and UnitInVehicle("player") then return false end
            if not _G.FMHUD_SmartLB_GetSlotData then return false end
            local d = _G.FMHUD_SmartLB_GetSlotData(1, customConfig)
            return d ~= nil
        end
    end
end"""

def make_smart_lb_bg_trigger() -> str:
    """Mostra lo sfondo e l'intestazione SOLO quando esistono bersagli validi o bombe attive e il player non e in un veicolo."""
    return f"""function(event, ...)
    if UnitInVehicle and UnitInVehicle("player") then return false end

    if not _G.FMHUD_SmartLB_Init then
        local init = {SHARED_SMART_LB_CHECK_LUA}
        init()
        _G.FMHUD_SmartLB_Init = true
    end
    if event == "COMBAT_LOG_EVENT_UNFILTERED" then
        if _G.FMHUD_SmartLB_OnCombatLog then
            _G.FMHUD_SmartLB_OnCombatLog(...)
        end
    end

    local cfg = aura_env and aura_env.config or {{}}
    if cfg.onlyInCombat and not UnitAffectingCombat("player") then
        return false
    end

    if _G.FMHUD_SmartLB_HasData then
        return _G.FMHUD_SmartLB_HasData(cfg)
    end
    return false
end"""

def make_smart_lb_bg_untrigger() -> str:
    """Nasconde lo sfondo e l'intestazione se non ci sono bersagli o bombe attive o se si entra in un veicolo."""
    return """function(event, ...)
    if UnitInVehicle and UnitInVehicle("player") then return true end

    local cfg = aura_env and aura_env.config or {}
    if cfg.onlyInCombat and not UnitAffectingCombat("player") then
        return true
    end
    if _G.FMHUD_SmartLB_HasData then
        return not _G.FMHUD_SmartLB_HasData(cfg)
    end
    return true
end"""

def make_smart_lb_trigger(slot_index: int) -> str:
    """Genera il trigger per il singolo slot aurabar dello Smart Living Bomb Assistant."""
    return f"""function(event, ...)
    if UnitInVehicle and UnitInVehicle("player") then return false end

    if not _G.FMHUD_SmartLB_Init then
        local init = {SHARED_SMART_LB_CHECK_LUA}
        init()
        _G.FMHUD_SmartLB_Init = true
    end
    if event == "COMBAT_LOG_EVENT_UNFILTERED" then
        if _G.FMHUD_SmartLB_OnCombatLog then
            _G.FMHUD_SmartLB_OnCombatLog(...)
        end
    end

    local cfg = aura_env and aura_env.config
    local data = _G.FMHUD_SmartLB_GetSlotData and _G.FMHUD_SmartLB_GetSlotData({slot_index}, cfg)

    if aura_env and aura_env.region and not InCombatLockdown() then
        if not aura_env.targetBtn then
            local btn = CreateFrame("Button", "FMHUD_SmartLB_Btn_{slot_index}", aura_env.region, "SecureActionButtonTemplate")
            btn:SetAllPoints(aura_env.region)
            btn:RegisterForClicks("AnyUp")
            btn:EnableMouse(true)
            aura_env.region:EnableMouse(true)
            aura_env.targetBtn = btn
        end
        if data and data.name then
            pcall(function()
                aura_env.targetBtn:SetAttribute("type", "macro")
                aura_env.targetBtn:SetAttribute("macrotext", "/targetexact " .. data.name)
                aura_env.targetBtn:Show()
            end)
        else
            pcall(function()
                aura_env.targetBtn:Hide()
            end)
        end
    end

    if aura_env and aura_env.region and data then
        local r, g, b = 1.0, 0.45, 0.1
        if not data.hasLB then
            if data.tier == 1 then
                r, g, b = 0.2, 0.85, 0.2
            elseif data.tier == 2 then
                r, g, b = 0.2, 0.7, 1.0
            else
                r, g, b = 0.85, 0.2, 0.2
            end
        end
        if aura_env.region.Color then
            aura_env.region:Color(r, g, b, 1.0)
        elseif aura_env.region.SetColor then
            aura_env.region:SetColor(r, g, b, 1.0)
        elseif aura_env.region.bar and aura_env.region.bar.SetStatusBarColor then
            aura_env.region.bar:SetStatusBarColor(r, g, b, 1.0)
        end
    end

    if not data then return false end
    if cfg and cfg.onlyInCombat and not UnitAffectingCombat("player") then
        return false
    end
    return true
end"""

def make_smart_lb_untrigger(slot_index: int) -> str:
    """Genera l'untrigger per nascondere la barra se lo slot e vuoto o il player e in un veicolo."""
    return f"""function(event, ...)
    if UnitInVehicle and UnitInVehicle("player") then return true end

    local cfg = aura_env and aura_env.config
    local data = _G.FMHUD_SmartLB_GetSlotData and _G.FMHUD_SmartLB_GetSlotData({slot_index}, cfg)
    if not data then return true end
    if cfg and cfg.onlyInCombat and not UnitAffectingCombat("player") then
        return true
    end
    return false
end"""

def make_smart_lb_duration(slot_index: int) -> str:
    """Genera la durata dinamica per la barra (12s countdown per [V], statico % HP per [X])."""
    return f"""function()
    local data = _G.FMHUD_SmartLB_GetSlotData and _G.FMHUD_SmartLB_GetSlotData({slot_index})
    if not data then return 0, 0 end
    if data.hasLB then
        local rem = (data.exp or 0) - GetTime()
        if rem > 0 then
            return 12.0, data.exp
        end
        return 0, 0
    else
        return (data.hpPct or 0), 100, true
    end
end"""

def make_smart_lb_custom_text(slot_index: int) -> str:
    """Genera il testo per il lato sinistro della barra (%c): [V]/[X] NomeMob * e aggiorna il fontstring a destra."""
    return f"""function()
    local data = _G.FMHUD_SmartLB_GetSlotData and _G.FMHUD_SmartLB_GetSlotData({slot_index})
    if not data then return "" end

    local status = data.hasLB and "|cFF55FF55[V]|r" or "|cFFFF4444[X]|r"
    local name = data.name or "Enemy"
    if #name > 10 then
        name = string.sub(name, 1, 9) .. ".."
    end
    local cur = (data.unit and UnitIsUnit(data.unit, "target")) and " |cFFFFFF00*|r" or ""

    if aura_env and aura_env.region and aura_env.region.subRegions then
        local rightSub = aura_env.region.subRegions[4]
        if not rightSub or not rightSub.text then
            for i = 1, #aura_env.region.subRegions do
                local sr = aura_env.region.subRegions[i]
                if sr and sr.text and i ~= 3 then
                    rightSub = sr
                    break
                end
            end
        end
        if rightSub and rightSub.text and rightSub.text.SetText then
            if data.hasLB then
                local rem = (data.exp or 0) - GetTime()
                if rem > 0 then
                    rightSub.text:SetFormattedText("%.1fs", rem)
                    rightSub.text:SetTextColor(1, 0.9, 0.2, 1)
                else
                    rightSub.text:SetText("0.0s")
                end
            else
                rightSub.text:SetFormattedText("%d%%", data.hpPct or 0)
                rightSub.text:SetTextColor(0.85, 0.85, 0.85, 1)
            end
        end
    end

    return string.format("%s %s%s", status, name, cur)
end"""

def make_stats_bg_trigger() -> str:
    return """function(event, ...)
    return true
end"""

def make_stats_bg_untrigger() -> str:
    return """function(event, ...)
    return false
end"""

def make_stats_trigger() -> str:
    return """function(event, ...)
    return true
end"""

def make_stats_untrigger() -> str:
    return """function(event, ...)
    return false
end"""

def make_stats_custom_text() -> str:
    return """function()
    -- 1. SPELL POWER (Fire School = 3)
    local sp = GetSpellBonusDamage(3) or 0
    sp = math.floor(sp + 0.5)

    -- 2. SPELL CRIT (Fire School = 3)
    -- Includes base crit, int contribution, Molten Armor (with spirit & glyph), talents, and buffs
    local crit = GetSpellCritChance(3) or 0

    -- Combustion stacks (+10% Fire crit per stack if active)
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
    local haste = 0
    if UnitSpellHaste then
        haste = UnitSpellHaste("player") or 0
    end
    if not haste or haste == 0 then
        local ratingBonus = GetCombatRatingBonus(20) or 0
        local mult = 1 + (ratingBonus / 100)
        for i = 1, 40 do
            local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
            if not name then break end
            if spellId == 2825 or spellId == 32182 or name == "Bloodlust" or name == "Heroism" then
                mult = mult * 1.30
            elseif spellId == 3738 or name == "Wrath of Air Totem" then
                mult = mult * 1.05
            elseif spellId == 48396 or spellId == 31583 or name == "Swift Retribution" or name == "Improved Moonkin Form" then
                mult = mult * 1.03
            end
        end
        haste = (mult - 1) * 100
    end

    -- 4. SPELL HIT
    local hitRatingBonus = GetCombatRatingBonus(8) or 0

    _G.FMHUD_StatCache = _G.FMHUD_StatCache or {
        lastTalentCheck = 0,
        precisionHit = 0,
        isDraenei = (select(2, UnitRace("player")) == "Draenei") and 1 or 0,
    }
    local now = GetTime()
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

    local draeneiHit = _G.FMHUD_StatCache.isDraenei
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

    return string.format(
        "|cFFFF2222SP:|r |cFFFFFFFF%d|r\\n|cFFFF8800Crit:|r |cFFFFFFFF%.2f%%|r\\n|cFFCC44FFHaste:|r |cFFFFFFFF%.2f%%|r\\n%s",
        sp, crit, haste, hitText
    )
end"""

SHARED_HOTSTREAK_CHECK_LUA = r"""function(event, ...)
    _G.FMHUD_HS = _G.FMHUD_HS or {
        streak = 0,
        hasBuff = false,
        duration = 10,
        expirationTime = 0,
    }
    local hs = _G.FMHUD_HS

    local function syncBuff()
        local found = false
        for i = 1, 40 do
            local name, _, _, _, _, dur, expTime, _, _, _, spellId = UnitBuff("player", i)
            if not name then break end
            if spellId == 48108 or name == "Hot Streak" or name == "Buona sorte" then
                found = true
                hs.hasBuff = true
                hs.streak = 2
                hs.duration = (dur and dur > 0) and dur or 10
                hs.expirationTime = expTime or (GetTime() + hs.duration)
                break
            end
        end
        if not found and hs.hasBuff then
            hs.hasBuff = false
            hs.streak = 0
            hs.expirationTime = 0
        end
    end

    if event == "PLAYER_ENTERING_WORLD" then
        hs.streak = 0
        hs.hasBuff = false
        hs.expirationTime = 0
        syncBuff()
    elseif event == "PLAYER_REGEN_ENABLED" then
        if not hs.hasBuff then
            hs.streak = 0
        end
    elseif event == "UNIT_AURA" then
        local unit = ...
        if unit == "player" then
            syncBuff()
        end
    elseif event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spellName, _, _, spellId = ...
        if unit == "player" then
            if spellId == 11366 or spellId == 12505 or spellId == 12522 or spellId == 12523 or
               spellId == 12524 or spellId == 12525 or spellId == 12526 or spellId == 33938 or
               spellId == 42890 or spellId == 42891 or spellName == "Pyroblast" or spellName == "Pirocombustione" then
                hs.hasBuff = false
                hs.streak = 0
                hs.expirationTime = 0
            end
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local timestamp, subEvent, sourceGUID, sourceName, sourceFlags,
              destGUID, destName, destFlags,
              spellId, spellName, spellSchool,
              amount, overkill, school, resisted, blocked, absorbed, critical = ...

        if sourceGUID == UnitGUID("player") and subEvent == "SPELL_DAMAGE" then
            -- Solo SPELL_DAMAGE diretto (non periodico). I DoT (SPELL_PERIODIC_DAMAGE) non azzerano!
            local isEligible = false
            if spellId then
                if spellId == 133 or spellId == 143 or spellId == 145 or spellId == 3140 or spellId == 8400 or
                   spellId == 8401 or spellId == 8402 or spellId == 10148 or spellId == 10149 or spellId == 10150 or
                   spellId == 10151 or spellId == 25306 or spellId == 27070 or spellId == 38692 or spellId == 42832 or
                   spellId == 42833 or -- Fireball
                   spellId == 2136 or spellId == 2137 or spellId == 2138 or spellId == 8412 or spellId == 8413 or
                   spellId == 10197 or spellId == 10199 or spellId == 27078 or spellId == 27079 or spellId == 42872 or
                   spellId == 42873 or -- Fire Blast
                   spellId == 2948 or spellId == 8444 or spellId == 8445 or spellId == 8446 or spellId == 10205 or
                   spellId == 10206 or spellId == 10207 or spellId == 27073 or spellId == 27074 or spellId == 42858 or
                   spellId == 42859 or -- Scorch
                   spellId == 44614 or spellId == 47610 or -- Frostfire Bolt
                   spellId == 44461 or spellId == 55361 or spellId == 55362 then -- Living Bomb Explosion
                    isEligible = true
                end
            end
            if not isEligible and spellName then
                if spellName == "Fireball" or spellName == "Palla di Fuoco" or
                   spellName == "Fire Blast" or spellName == "Deflagrazione di Fuoco" or
                   spellName == "Scorch" or spellName == "Bruciatura" or
                   spellName == "Frostfire Bolt" or spellName == "Dardo di Fuocogelo" then
                    isEligible = true
                end
            end

            if isEligible then
                if critical == true then
                    if not hs.hasBuff then
                        if hs.streak == 0 then
                            hs.streak = 1 -- 1° critico persistente!
                        else
                            hs.streak = 2
                        end
                    end
                else
                    -- Colpo non-critico diretto: azzera la serie
                    if not hs.hasBuff then
                        hs.streak = 0
                    end
                end
            end
        end
    end
    syncBuff()
    return hs
end"""

def make_hotstreak_bg_trigger() -> str:
    return """function(event, ...)
    return not UnitIsDeadOrGhost("player")
end"""

def make_hotstreak_bg_untrigger() -> str:
    return """function(event, ...)
    return UnitIsDeadOrGhost("player")
end"""

def make_hotstreak_seg1_trigger() -> str:
    return """function(event, ...)
    _G.FMHUD_UpdateHotStreakState = _G.FMHUD_UpdateHotStreakState or (""" + SHARED_HOTSTREAK_CHECK_LUA + """)
    local hs = _G.FMHUD_UpdateHotStreakState(event, ...)
    return (hs.streak >= 1 or hs.hasBuff)
end"""

def make_hotstreak_seg1_untrigger() -> str:
    return """function(event, ...)
    _G.FMHUD_UpdateHotStreakState = _G.FMHUD_UpdateHotStreakState or (""" + SHARED_HOTSTREAK_CHECK_LUA + """)
    local hs = _G.FMHUD_UpdateHotStreakState(event, ...)
    return not (hs.streak >= 1 or hs.hasBuff)
end"""

def make_hotstreak_seg1_duration() -> str:
    return """function()
    return 1, 1, true
end"""

def make_hotstreak_seg2_trigger() -> str:
    return """function(event, ...)
    _G.FMHUD_UpdateHotStreakState = _G.FMHUD_UpdateHotStreakState or (""" + SHARED_HOTSTREAK_CHECK_LUA + """)
    local hs = _G.FMHUD_UpdateHotStreakState(event, ...)
    return hs.hasBuff and hs.expirationTime and (hs.expirationTime > GetTime())
end"""

def make_hotstreak_seg2_untrigger() -> str:
    return """function(event, ...)
    _G.FMHUD_UpdateHotStreakState = _G.FMHUD_UpdateHotStreakState or (""" + SHARED_HOTSTREAK_CHECK_LUA + """)
    local hs = _G.FMHUD_UpdateHotStreakState(event, ...)
    return not (hs.hasBuff and hs.expirationTime and (hs.expirationTime > GetTime()))
end"""

def make_hotstreak_seg2_duration() -> str:
    return """function()
    local hs = _G.FMHUD_HS
    if hs and hs.hasBuff and hs.expirationTime and hs.expirationTime > 0 then
        return hs.duration or 10.0, hs.expirationTime
    end
    return 0, 0
end"""

import copy

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
                "06 - Combustion",
                "06 - Mirror Image",
                "07 - Mana Bar",
                "10 - Hot Streak Bar",
                "08 - Castbar",
                "09 - GCD",
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
                "parent": "Fire Mage HUD",
                "regionType": "dynamicgroup",
                "internalVersion": 52,
                "grow": "HORIZONTAL",
                "align": "CENTER",
                "space": 6,
                "xOffset": 0,
                "yOffset": 52,
                "controlledChildren": [
                    "Hot Streak",
                    "Clearcasting",
                    "Living Bomb",
                    "Ignite",
                    "Scorch",
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
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -180,
                "yOffset": -14,
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
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == "Molten Armor" then
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
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == "Molten Armor" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                return true
            end
            return false
        end
    end
    return false
end""",
                            "customDuration": """function()
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == "Molten Armor" then
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
    for i = 1, 40 do
        local name, _, _, _, _, duration, expirationTime = UnitBuff("player", i)
        if not name then break end
        if name == "Molten Armor" then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - GetTime()) or 0
            if rem > 0 and rem <= 300 then
                return false
            end
            return true
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
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -210,
                "yOffset": -14,
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
    local b = {
        ["Arcane Intellect"] = true,
        ["Arcane Brilliance"] = true,
        ["Dalaran Intellect"] = true,
        ["Dalaran Brilliance"] = true,
        ["Fel Intelligence"] = true,
    }
    for i = 1, 40 do
        local name, _, _, _, _, _, expirationTime = UnitBuff("player", i)
        if not name then break end
        if b[name] then
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
                return true
            end
            return false
        end
    end
    return false
end""",
                            "customDuration": """function()
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
            return duration or 3600, expirationTime
        end
    end
    return 0, 0
end""",
                        },
                        "untrigger": {
                            "custom": """function(event, ...)
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
                return false
            end
            return true
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
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -150,
                "yOffset": -14,
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
                            "events": "COMBAT_LOG_EVENT_UNFILTERED,UNIT_SPELLCAST_SUCCEEDED,UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_FOCUS_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,PLAYER_ENTERING_WORLD,FRAME_UPDATE",
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
                            "events": "COMBAT_LOG_EVENT_UNFILTERED,UNIT_SPELLCAST_SUCCEEDED,UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_FOCUS_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,PLAYER_ENTERING_WORLD,FRAME_UPDATE",
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
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -110,
                "yOffset": -54,
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
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -66,
                "yOffset": -54,
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
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": -22,
                "yOffset": -54,
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
            # 06 - MANA GEM (Between Cloak and Combustion - T7 Proc + CD + Charges)
            # =================================================================
            {
                "id": "06 - Mana Gem",
                "uid": "FMHUD_MANAGEM",
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 22,
                "yOffset": -54,
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
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 66,
                "yOffset": -54,
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
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
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
                "parent": "Fire Mage HUD",
                "regionType": "icon",
                "internalVersion": 52,
                "xOffset": 110,
                "yOffset": -54,
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
                "parent": "Fire Mage HUD",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 264,
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
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": 0,
                "yOffset": -25,
                "anchorPoint": "CENTER",
                "selfPoint": "CENTER",
                "controlledChildren": [
                    "Hot Streak Bar - Background",
                    "Hot Streak Bar - Segment 1",
                    "Hot Streak Bar - Segment 2",
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
                "width": 264,
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
                            "events": "PLAYER_ENTERING_WORLD,PLAYER_ALIVE",
                            "custom": make_hotstreak_bg_trigger(),
                        },
                        "untrigger": {
                            "custom": make_hotstreak_bg_untrigger(),
                        }
                    },
                    "activeTriggerMode": -10,
                },
            },
            # Hot Streak Bar - Segment 1 (Left Half: 1° Crit, Persistent, No Text)
            {
                "id": "Hot Streak Bar - Segment 1",
                "uid": "FMHUD_HSBAR_SEG1",
                "parent": "10 - Hot Streak Bar",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 130,
                "height": 5,
                "xOffset": -66,
                "yOffset": 0,
                "barColor": [1.0, 0.55, 0.0, 1.0],
                "backgroundColor": [0.1, 0.1, 0.1, 0.8],
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "COMBAT_LOG_EVENT_UNFILTERED,UNIT_AURA,UNIT_SPELLCAST_SUCCEEDED,PLAYER_REGEN_ENABLED,PLAYER_ENTERING_WORLD,FRAME_UPDATE",
                            "custom": make_hotstreak_seg1_trigger(),
                            "customDuration": make_hotstreak_seg1_duration(),
                        },
                        "untrigger": {
                            "custom": make_hotstreak_seg1_untrigger(),
                        }
                    },
                    "activeTriggerMode": -10,
                },
                "subRegions": [
                    { "type": "subbackground" },
                    { "type": "subforeground" },
                ],
            },
            # Hot Streak Bar - Segment 2 (Right Half: 2° Crit Hot Streak Proc 10s Countdown, No Text)
            {
                "id": "Hot Streak Bar - Segment 2",
                "uid": "FMHUD_HSBAR_SEG2",
                "parent": "10 - Hot Streak Bar",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 130,
                "height": 5,
                "xOffset": 66,
                "yOffset": 0,
                "barColor": [1.0, 0.35, 0.0, 1.0],
                "backgroundColor": [0.1, 0.1, 0.1, 0.8],
                "texture": "Interface\\TargetingFrame\\UI-StatusBar",
                "triggers": {
                    1: {
                        "trigger": {
                            "type": "custom",
                            "custom_type": "status",
                            "check": "event",
                            "events": "COMBAT_LOG_EVENT_UNFILTERED,UNIT_AURA,UNIT_SPELLCAST_SUCCEEDED,PLAYER_REGEN_ENABLED,PLAYER_ENTERING_WORLD,FRAME_UPDATE",
                            "custom": make_hotstreak_seg2_trigger(),
                            "customDuration": make_hotstreak_seg2_duration(),
                        },
                        "untrigger": {
                            "custom": make_hotstreak_seg2_untrigger(),
                        }
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
                "parent": "Fire Mage HUD",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 264,
                "height": 20,
                "xOffset": 0,
                "yOffset": 8,
                "barColor": [0.0, 0.77, 1.0, 1.0],
                "backgroundColor": [0.15, 0.15, 0.15, 0.8],
                "texture": "Blizzard",
                "icon": True,
                "icon_side": "LEFT",
                "iconSource": -1,
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
            # 09 - GCD (Aurabar)
            # =================================================================
            {
                "id": "09 - GCD",
                "uid": "FMHUD_GCD",
                "parent": "Fire Mage HUD",
                "regionType": "aurabar",
                "internalVersion": 52,
                "width": 264,
                "height": 3,
                "xOffset": 0,
                "yOffset": -4,
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
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -180,
                "yOffset": -54,
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
                            "events": "UNIT_AURA,COMBAT_RATING_UPDATE,PLAYER_DAMAGE_DONE_MODS,PLAYER_ENTERING_WORLD,UNIT_INVENTORY_CHANGED,PLAYER_EQUIPMENT_CHANGED,PLAYER_TARGET_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,CHARACTER_POINTS_CHANGED,FRAME_UPDATE",
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

if __name__ == "__main__":
    wa_tree = build_wa_tree()
    wa_string = generate_wa_string(wa_tree)
    with open("IMPORT_STRING.txt", "w", encoding="utf-8") as f:
        f.write(wa_string)
    print(f"Generated !WA:1! String successfully! Length: {len(wa_string)}")
