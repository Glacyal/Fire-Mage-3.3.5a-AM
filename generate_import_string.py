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
    local icon = GetSpellTexture(55342) or "Interface\\\\Icons\\\\Spell_Magic_LesserInvisibilty"
    
    -- 1. Check if Mirror Image buff is ACTIVE on player (e.g. T10 4pc proc 70753 or buff "Mirror Image")
    for i = 1, 40 do
        local name, _, buffIcon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if name == "Mirror Image" or name == "Immagine Speculare" or spellId == 70753 or spellId == 55342 then
            local rem = expirationTime and expirationTime > 0 and (expirationTime - now) or 0
            local dur = duration and duration > 0 and duration or 30
            return "ACTIVE", rem, dur, icon
        end
    end
    
    -- 2. Check spell cooldown
    local start, duration = GetSpellCooldown(55342)
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Mirror Image")
    end
    if not start or duration == 0 then
        start, duration = GetSpellCooldown("Immagine Speculare")
    end
    
    if start and duration and start > 0 and duration > 1.5 then
        local elapsed = now - start
        -- Mirror Images stay active for 30 seconds after cast!
        if elapsed >= 0 and elapsed < 30 then
            local remActive = 30 - elapsed
            return "ACTIVE", remActive, 30, icon
        else
            local remCD = (start + duration) - now
            if remCD > 0.1 then
                return "COOLDOWN", remCD, duration, icon
            end
        end
    end
    
    -- 3. READY
    return "READY", 0, 0, icon
end"""

def make_mirrorimage_custom_text() -> str:
    """Genera il testo descrittivo (%c) delle Copie (Mirror Image): durata attiva 30s con glow cyan o CD 3 min."""
    return f"""function()
    _G.FMHUD_CheckMirrorImage = _G.FMHUD_CheckMirrorImage or {SHARED_MIRRORIMAGE_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckMirrorImage()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{0.2, 0.8, 1.0, 1}}, 8, 0.25, 10, 2)
        end
        if rem > 0 then
            return string.format("|cFF33FFFF%.1fs|r", rem)
        end
        return "|cFF33FFFFON|r"
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
    """Genera la durata e scadenza per lo swipe di Mirror Image."""
    return f"""function()
    _G.FMHUD_CheckMirrorImage = _G.FMHUD_CheckMirrorImage or {SHARED_MIRRORIMAGE_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckMirrorImage()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_mirrorimage_custom_icon() -> str:
    """Restituisce la texture dell'icona di Mirror Image (Spell ID 55342)."""
    return """function()
    local icon = GetSpellTexture(55342) or "Interface\\\\Icons\\\\Spell_Magic_LesserInvisibilty"
    return icon
end"""

SHARED_MANAGEM_CHECK_LUA = """function()
    local now = GetTime()
    local isT7Active = false
    local remT7 = 0
    local durT7 = 15

    -- 1. Controllo buff bonus 2 pezzi T7 Mago (+225 Spell Power per 15s dopo l'uso della gemma)
    for i = 1, 40 do
        local n, _, icon, _, _, dur, exp, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if spellId == 61062 or spellId == 37445 or spellId == 37446 or n == "Improved Mana Gems" or n == "Gemme di Mana Migliorate" or n == "Gemme del Mana Migliorate" or n == "Gemma del Mana Migliorata" then
            if exp and exp > now then
                isT7Active = true
                remT7 = exp - now
                durT7 = (dur and dur > 0) and dur or 15
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
        return "ACTIVE", remT7, durT7
    elseif isCD then
        return "COOLDOWN", remCD, duration
    else
        return "READY", 0, 0
    end
end"""

def make_managem_custom_text() -> str:
    """Genera il testo descrittivo (%c) delle cariche della Gemma del Mana, gestendo il Pixel Glow durante il proc T7."""
    return f"""function()
    _G.FMHUD_CheckManaGem = _G.FMHUD_CheckManaGem or {SHARED_MANAGEM_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckManaGem()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)

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
    _G.FMHUD_CheckManaGem = _G.FMHUD_CheckManaGem or {SHARED_MANAGEM_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckManaGem()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_managem_custom_icon() -> str:
    """Restituisce la texture predefinita della Gemma del Mana (Mana Sapphire 33312)."""
    return """function()
    return "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
end"""

import copy

FIRE_MAGE_LOAD = {
    "use_class": True,
    "class": { "single": "MAGE", "multi": { "MAGE": True } },
    "use_talent": True,
    "talent": { "single": 68, "multi": { 68: True } },
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
                "08 - Castbar",
                "09 - GCD",
                "10 - Alerts"
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
                "yOffset": 44,
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
                "xOffset": -182,
                "yOffset": -18,
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
                "width": 32,
                "height": 32,
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
                "width": 32,
                "height": 32,
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
            # 03 - ARCANE INTELLECT (Wing: Left side column - Top Icon)
            # =================================================================
            {
                "id": "03 - Arcane Intellect",
                "uid": "FMHUD_INTELLECT_GRP",
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -182,
                "yOffset": 18,
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
                "width": 32,
                "height": 32,
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
            # 04 - FOCUS MAGIC (Wing: Left side column - Bottom Icon)
            # =================================================================
            {
                "id": "04 - Focus Magic",
                "uid": "FMHUD_FOCUS_GRP",
                "parent": "Fire Mage HUD",
                "regionType": "group",
                "internalVersion": 52,
                "xOffset": -182,
                "yOffset": -54,
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
                "width": 32,
                "height": 32,
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
                "width": 32,
                "height": 32,
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
                            "check": "event",
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,BAG_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,BAG_UPDATE,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
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
                            "check": "event",
                            "events": "UNIT_AURA,SPELL_UPDATE_COOLDOWN,ACTIONBAR_UPDATE_COOLDOWN,PLAYER_ENTERING_WORLD,COMBAT_LOG_EVENT_UNFILTERED",
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
                "yOffset": 0,
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
            }
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
