from builder.core import serialize_string, serialize_value
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
    if not _G.FMHUD_TrinketDB then
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
    end

    local now = GetTime()
    _G.FMHUD_SlotCache = _G.FMHUD_SlotCache or {}
    if _G.FMHUD_SlotCache[slot] and _G.FMHUD_SlotCache[slot].time == now then
        local c = _G.FMHUD_SlotCache[slot]
        return c.state, c.rem, c.dur, c.icon
    end

    local function finish(st, r, d, ic)
        local c = _G.FMHUD_SlotCache[slot]
        if not c then
            c = {}
            _G.FMHUD_SlotCache[slot] = c
        end
        c.time = now
        c.state = st
        c.rem = r
        c.dur = d
        c.icon = ic
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
    """Genera la closure Lua per il testo descrittivo del monile/mantello (%c), con pixel glow su proc attivo e riposizionamento dinamico."""
    return f"""function()
    if not _G.FMHUD_CheckSlot_v5 then
        _G.FMHUD_CheckSlot = {SHARED_SLOT_CHECK_LUA}
        _G.FMHUD_CheckSlot_v5 = true
    end
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    if _G.FMHUD_UpdateUtilityRowPositions then
        _G.FMHUD_UpdateUtilityRowPositions()
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


SHARED_T8_INIT_LUA = """function()
    if _G.FMHUD_T8_InitDone then return end

    local ARMOR_SLOTS = { 1, 3, 5, 7, 10 }
    _G.FMHUD_ArmorSlots = ARMOR_SLOTS

    _G.FMHUD_T8_SetIDs = {
        -- 10-Man Valorous Kirin Tor
        [45367] = true, -- Head
        [45369] = true, -- Shoulder
        [45365] = true, -- Chest
        [45366] = true, -- Legs
        [45368] = true, -- Hands
        -- 25-Man Conqueror's Kirin Tor
        [45357] = true, -- Head
        [45359] = true, -- Shoulder
        [45355] = true, -- Chest
        [45356] = true, -- Legs
        [45358] = true, -- Hands
    }

    _G.FMHUD_T8_State = _G.FMHUD_T8_State or { lastStart = 0, lastEnd = 0, isProc = false }

    _G.FMHUD_CheckT8Equipped = function()
        local now = GetTime()
        local cache = _G.FMHUD_T8_EquipCache
        if cache and (now - cache.time < 0.2) then
            return cache.isEquipped
        end
        if not cache then
            cache = { time = 0, isEquipped = false }
            _G.FMHUD_T8_EquipCache = cache
        end

        -- 1. Controllo buff attivo Praxis (Spell ID 64868, "Praxis", "Prassi")
        for i = 1, 40 do
            local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
            if not name then break end
            if spellId == 64868 or name == "Praxis" or name == "Prassi" or name:find("T8 2P") then
                cache.time = now
                cache.isEquipped = true
                return true
            end
        end

        -- 2. Controllo Item ID noti Kirin Tor (10m e 25m)
        local count = 0
        local slots = _G.FMHUD_ArmorSlots
        if not slots then
            slots = { 1, 3, 5, 7, 10 }
            _G.FMHUD_ArmorSlots = slots
        end
        local setIDs = _G.FMHUD_T8_SetIDs
        for _, s in ipairs(slots) do
            local id = GetInventoryItemID("player", s)
            if id and setIDs and setIDs[id] then
                count = count + 1
            end
        end
        if count >= 2 then
            cache.time = now
            cache.isEquipped = true
            return true
        end

        -- 3. Scansione tooltip su pezzi equipaggiati per "Kirin Tor", "Praxis" o "Prassi"
        local ttCount = 0
        local tt = _G.FMHUD_ScanTT
        if not tt then
            tt = CreateFrame("GameTooltip", "FMHUD_ScanTT", nil, "GameTooltipTemplate")
            tt:SetOwner(WorldFrame, "ANCHOR_NONE")
            _G.FMHUD_ScanTT = tt
        end
        for _, s in ipairs(slots) do
            local id = GetInventoryItemID("player", s)
            if id then
                tt:ClearLines()
                tt:SetInventoryItem("player", s)
                for j = 1, tt:NumLines() do
                    local line = _G["FMHUD_ScanTTTextLeft"..j]
                    local text = line and line:GetText()
                    if text then
                        local lt = text:lower()
                        if lt:find("kirin tor") or lt:find("praxis") or lt:find("prassi") then
                            ttCount = ttCount + 1
                            break
                        end
                    end
                end
            end
        end
        if ttCount >= 2 then
            cache.time = now
            cache.isEquipped = true
            return true
        end

        cache.time = now
        cache.isEquipped = false
        return false
    end

    _G.FMHUD_CheckT8 = function()
        local isEquipped = _G.FMHUD_CheckT8Equipped()
        local defIcon = GetSpellTexture(64868) or "Interface\\\\Icons\\\\Spell_Arcane_StudentOfMagic"
        local icon = defIcon

        if not isEquipped then
            return "NONE", 0, 0, defIcon, false
        end

        local now = GetTime()
        local state = _G.FMHUD_T8_State

        -- 1. Controllo buff attivo Praxis (SpellID 64868, +350 SP per 15s)
        local foundBuff = false
        local remBuff = 0
        local durBuff = 15
        for i = 1, 40 do
            local name, _, bIcon, count, _, duration, expirationTime, _, _, _, spellId = UnitBuff("player", i)
            if not name then break end
            if spellId == 64868 or name == "Praxis" or name == "Prassi" or name:find("T8 2P") then
                foundBuff = true
                durBuff = (duration and duration > 0) and duration or 15
                remBuff = (expirationTime and expirationTime > 0) and (expirationTime - now) or durBuff
                if bIcon then icon = bIcon end
                break
            end
        end

        if foundBuff then
            if not state.isProc or (now - state.lastStart > durBuff + 2) then
                state.lastStart = now - (durBuff - remBuff)
                state.lastEnd = state.lastStart + 45
                state.isProc = true
            end
            return "ACTIVE", remBuff, durBuff, icon, true
        end

        if state.isProc then
            state.isProc = false
        end

        -- 2. ICD Stimato (45s totale = 15s proc + 30s ricarica)
        if state.lastStart > 0 then
            local elapsed = now - state.lastStart
            if elapsed < 45 then
                local remICD = 45 - elapsed
                return "ICD", remICD, 45, icon, true
            end
        end

        -- 3. Pronto
        return "READY", 0, 0, icon, true
    end

    -- Layout predefiniti statici per evitare allocazioni in combattimento
    _G.FMHUD_LayoutT8 = {
        ["05 - Trinket 1"]    = -114,
        ["05 - Trinket 2"]    = -76,
        ["06 - Cloak"]        = -38,
        ["06 - Tier 8"]       = 0,
        ["06 - Mana Gem"]     = 38,
        ["06 - Combustion"]   = 76,
        ["06 - Mirror Image"] = 114,
    }
    _G.FMHUD_LayoutStd = {
        ["05 - Trinket 1"]    = -110,
        ["05 - Trinket 2"]    = -66,
        ["06 - Cloak"]        = -22,
        ["06 - Mana Gem"]     = 22,
        ["06 - Combustion"]   = 66,
        ["06 - Mirror Image"] = 110,
    }

    local lastRowUpdate = 0
    _G.FMHUD_UpdateUtilityRowPositions = function(force)
        local now = GetTime()
        if not force and (now - lastRowUpdate < 0.15) then
            return
        end
        lastRowUpdate = now

        if not WeakAuras or not WeakAuras.regions then return end
        local groupObj = WeakAuras.regions["Fire Mage 3.3.5a AM"]
        local group = groupObj and (groupObj.region or (groupObj.GetPoint and groupObj))
        if not group then return end

        local hasT8 = _G.FMHUD_CheckT8Equipped and _G.FMHUD_CheckT8Equipped()
        local mode = hasT8 and "T8" or "STD"
        local layout = hasT8 and _G.FMHUD_LayoutT8 or _G.FMHUD_LayoutStd
        local targetW = 28

        local allFound = true
        for id, targetX in pairs(layout) do
            local regObj = WeakAuras.regions[id]
            local r = regObj and (regObj.region or (regObj.GetPoint and regObj))
            if r then
                local point, relTo, relPoint, curX, curY = r:GetPoint(1)
                if force or not curX or math.abs(curX - targetX) > 0.5 or (curY and math.abs(curY - (-45)) > 0.5) then
                    r:ClearAllPoints()
                    r:SetPoint("CENTER", group, "CENTER", targetX, -45)
                end
                if r.GetWidth and math.abs(r:GetWidth() - targetW) > 0.5 then
                    r:SetWidth(targetW)
                    r:SetHeight(targetW)
                end
                local data = WeakAuras.GetData and WeakAuras.GetData(id)
                if data and (data.xOffset ~= targetX or data.yOffset ~= -45) then
                    data.xOffset = targetX
                    data.yOffset = -45
                end
            else
                allFound = false
            end
        end

        if not hasT8 then
            local t8Obj = WeakAuras.regions["06 - Tier 8"]
            local t8r = t8Obj and (t8Obj.region or (t8Obj.GetPoint and t8Obj))
            if t8r and t8r.Hide then
                t8r:Hide()
            end
        else
            local t8Obj = WeakAuras.regions["06 - Tier 8"]
            local t8r = t8Obj and (t8Obj.region or (t8Obj.GetPoint and t8Obj))
            if t8r and t8r.Show then
                t8r:Show()
            end
        end

        if allFound then
            _G.FMHUD_LastLayoutMode = mode
        else
            _G.FMHUD_LastLayoutMode = nil
        end
    end

    if not _G.FMHUD_LayoutFrame then
        local f = CreateFrame("Frame", "FMHUD_LayoutFrame")
        f:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
        f:RegisterEvent("UNIT_INVENTORY_CHANGED")
        f:RegisterEvent("PLAYER_ENTERING_WORLD")
        f:RegisterEvent("ZONE_CHANGED_NEW_AREA")
        f:RegisterEvent("UNIT_AURA")
        f:SetScript("OnEvent", function(self, event, unit)
            if event == "UNIT_AURA" and unit ~= "player" then return end
            _G.FMHUD_T8_EquipCache = nil
            _G.FMHUD_LastLayoutMode = nil
            _G.FMHUD_UpdateUtilityRowPositions(true)
            if WeakAuras and WeakAuras.ScanEvents then
                WeakAuras.ScanEvents("FMHUD_T8_UPDATE")
            end
        end)
        _G.FMHUD_LayoutFrame = f
    end

    _G.FMHUD_T8_InitDone = true
end"""

SHARED_UTILITY_POS_LUA = """function(env, x6, x7)
    if not _G.FMHUD_T8_InitDone then
        if _G.FMHUD_InitT8 then _G.FMHUD_InitT8() end
    end
    if _G.FMHUD_UpdateUtilityRowPositions then
        _G.FMHUD_UpdateUtilityRowPositions()
    end
end"""

def make_t8_custom_text() -> str:
    """Genera la closure Lua per il testo descrittivo del Tier 8 2P (%c), con pixel glow su proc attivo e timer ICD."""
    return f"""function()
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    if _G.FMHUD_UpdateUtilityRowPositions then
        _G.FMHUD_UpdateUtilityRowPositions()
    end
    local state, rem, dur, icon, isEquipped = _G.FMHUD_CheckT8()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2, 0, 0, false, "FMHUD_T8_GLOW")
        end
        return string.format("|cFFFFFF00%.1fs|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, "FMHUD_T8_GLOW")
        end
        if state == "ICD" and rem > 0.1 then
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

def make_t8_custom_duration() -> str:
    """Genera la closure Lua per la durata e scadenza dello swipe di ricarica per il Tier 8 2P."""
    return f"""function()
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    local state, rem, dur, icon, isEquipped = _G.FMHUD_CheckT8()
    if (state == "ACTIVE" or state == "ICD") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""

def make_t8_custom_icon() -> str:
    """Genera la closure Lua per l'icona del Tier 8 2P (Praxis / Kirin Tor)."""
    return f"""function()
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    local state, rem, dur, icon, isEquipped = _G.FMHUD_CheckT8()
    return icon or GetSpellTexture(64868) or "Interface\\\\Icons\\\\Spell_Arcane_StudentOfMagic"
end"""

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
    """Genera il trigger Lua per Focus Magic attivo: visibile SOLO durante il proc di 10 secondi sul player."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc = _G.FMHUD_CheckFM(event, ...)
    return hasProc == true
end"""

def make_fm_untrigger() -> str:
    """Genera l'untrigger Lua per Focus Magic attivo: nascosto quando il proc di 10s sul player finisce."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc = _G.FMHUD_CheckFM(event, ...)
    return not hasProc
end"""

def make_fm_custom_duration() -> str:
    """Genera la durata e scadenza per lo swipe di Focus Magic per il proc da 10s."""
    return f"""function()
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive, procRem, procDur, procExp = _G.FMHUD_CheckFM()
    if hasProc then
        return procDur, procExp
    end
    return 0, 0
end"""

def make_fm_custom_text() -> str:
    """Genera il conto alla rovescia in secondi per il proc da 10s."""
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
    """Genera il trigger Lua per Focus Magic OFF: visibile SOLO se nessun alleato ha il buff e il player non ha il proc 10s."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive = _G.FMHUD_CheckFM(event, ...)
    return (not hasProc) and (not allyActive)
end"""

def make_fm_off_untrigger() -> str:
    """Disattiva lo stato OFF se il player ha il proc 10s oppure un alleato ha il buff attivo."""
    return f"""function(event, ...)
    _G.FMHUD_CheckFM = _G.FMHUD_CheckFM or {SHARED_FM_CHECK_LUA}
    local hasProc, allyActive = _G.FMHUD_CheckFM(event, ...)
    return hasProc or allyActive
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
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    if _G.FMHUD_UpdateUtilityRowPositions then
        _G.FMHUD_UpdateUtilityRowPositions()
    end
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
    local t10Pieces = _G.FMHUD_T10_4P_Pieces
    if not t10Pieces then
        t10Pieces = {
            [50069]=true,[51159]=true,[51284]=true,
            [50073]=true,[51155]=true,[51280]=true,
            [50070]=true,[51158]=true,[51283]=true,
            [50071]=true,[51157]=true,[51282]=true,
            [50072]=true,[51156]=true,[51281]=true,
        }
        _G.FMHUD_T10_4P_Pieces = t10Pieces
    end
    local slots = _G.FMHUD_ArmorSlots
    if not slots then
        slots = { 1, 3, 5, 7, 10 }
        _G.FMHUD_ArmorSlots = slots
    end
    local t10Count = 0
    for _, slot in ipairs(slots) do
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
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    if _G.FMHUD_UpdateUtilityRowPositions then
        _G.FMHUD_UpdateUtilityRowPositions()
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
    local baseIcon = (GetItemCount(33312) == 0 and GetItemCount(22044) > 0)
                     and "Interface\\\\Icons\\\\INV_Misc_Gem_Emerald_01"
                     or  "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
    local procIcon = nil

    -- 1. Controllo buff bonus 2 pezzi T7 Mago (+225 Spell Power per 15s dopo l'uso della gemma)
    for i = 1, 40 do
        local n, _, icon, _, _, dur, exp, _, _, _, spellId = UnitBuff("player", i)
        if not n then break end
        if spellId == 61062 or spellId == 37447 or
           n == "Mana Surge" or n == "Improved Mana Gems" or n == "Gemme di Mana Migliorate" or 
           n == "Gemme del Mana Migliorate" or n == "Gemma del Mana Migliorata" or n == "Ondata di Mana" then
            local rem = (exp and exp > now) and (exp - now) or 0
            if rem > 0.05 then
                isT7Active = true
                remT7 = rem
                durT7 = (dur and dur > 0) and dur or 15
                procIcon = icon or GetSpellTexture(61062) or "Interface\\\\Icons\\\\Spell_Arcane_ManaSurge" or "Interface\\\\Icons\\\\Spell_Holy_MagicalSentry"
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
    if not _G.FMHUD_CheckManaGem_v5 then
        _G.FMHUD_CheckManaGem = {SHARED_MANAGEM_CHECK_LUA}
        _G.FMHUD_CheckManaGem_v5 = true
    end
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    if _G.FMHUD_UpdateUtilityRowPositions then
        _G.FMHUD_UpdateUtilityRowPositions()
    end
    local state, rem, dur, icon = _G.FMHUD_CheckManaGem()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)

    -- Aggiornamento immediato texture dell'icona: Mana Surge SOLO durante proc T7 attivo, altrimenti SEMPRE Gemma standard
    if aura_env and aura_env.region then
        local defIcon = (GetItemCount(33312) == 0 and GetItemCount(22044) > 0)
                         and "Interface\\\\Icons\\\\INV_Misc_Gem_Emerald_01"
                         or  "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
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
    if not _G.FMHUD_CheckManaGem_v5 then
        _G.FMHUD_CheckManaGem = {SHARED_MANAGEM_CHECK_LUA}
        _G.FMHUD_CheckManaGem_v5 = true
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
    if not _G.FMHUD_CheckManaGem_v5 then
        _G.FMHUD_CheckManaGem = {SHARED_MANAGEM_CHECK_LUA}
        _G.FMHUD_CheckManaGem_v5 = true
    end
    local state, rem, dur, icon = _G.FMHUD_CheckManaGem()
    if state == "ACTIVE" and icon then
        return icon
    end
    local defIcon = (GetItemCount(33312) == 0 and GetItemCount(22044) > 0)
                     and "Interface\\\\Icons\\\\INV_Misc_Gem_Emerald_01"
                     or  "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
    return defIcon
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

        -- Combustion (+10% Fire crit per stack)
        if not hasCombustion and (spellId == 11129 or name == "Combustion" or name == "Combustione") then
            hasCombustion = true
            local stacks = (count and count > 0) and count or 1
            crit = crit + (stacks * 10)
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

SHARED_HOTSTREAK_CHECK_LUA = r"""function(event, ...)
    _G.FMHUD_HS = _G.FMHUD_HS or {
        streak = 0,
        lastEventKey = nil,
    }
    local hs = _G.FMHUD_HS

    local QUALIFYING_SPELLS = {
        [133]=true,[143]=true,[145]=true,[3140]=true,[8400]=true,[8401]=true,[8402]=true,[10148]=true,[10149]=true,[10150]=true,[10151]=true,[25306]=true,[27070]=true,[38692]=true,[42832]=true,[42833]=true, -- Fireball
        [2136]=true,[2137]=true,[2138]=true,[8412]=true,[8413]=true,[10197]=true,[10199]=true,[27078]=true,[27079]=true,[42872]=true,[42873]=true, -- Fire Blast
        [2948]=true,[8444]=true,[8445]=true,[8446]=true,[10205]=true,[10206]=true,[10207]=true,[27073]=true,[27074]=true,[42858]=true,[42859]=true, -- Scorch
        [44614]=true,[47610]=true, -- Frostfire Bolt
        [44461]=true,[55361]=true,[55362]=true,[44457]=true,[55359]=true,[55360]=true, -- Living Bomb
    }

    local function isQualifying(spellId, spellName)
        if spellId and QUALIFYING_SPELLS[spellId] then return true end
        if spellName then
            if string.find(spellName, "Fireball") or string.find(spellName, "Palla di Fuoco") or
               string.find(spellName, "Fire Blast") or string.find(spellName, "Deflagrazione") or
               string.find(spellName, "Scorch") or string.find(spellName, "Bruciatura") or
               string.find(spellName, "Frostfire") or string.find(spellName, "Fuocogelo") or
               string.find(spellName, "Living Bomb") or string.find(spellName, "Bomba Vivente") then
                return true
            end
        end
        return false
    end

    local function notifyWA()
        if WeakAuras and WeakAuras.ScanEvents then
            WeakAuras.ScanEvents("FMHUD_HS_UPDATE")
        end
    end

    local function handleEvent(ev, ...)
        if ev == "PLAYER_ENTERING_WORLD" or ev == "PLAYER_DEAD" or ev == "PLAYER_UNGHOST" then
            hs.streak = 0
            notifyWA()
        elseif ev == "COMBAT_LOG_EVENT_UNFILTERED" then
            local subEvent = select(2, ...)
            if subEvent == "SPELL_DAMAGE" then
                local sourceGUID = select(3, ...)
                local sourceName = select(4, ...)
                local sourceFlags = select(5, ...)

                local isPlayer = (sourceGUID == UnitGUID("player")) or (sourceName and sourceName == UnitName("player"))
                if not isPlayer and sourceFlags and bit and bit.band then
                    if bit.band(sourceFlags, 0x00000001) > 0 then
                        isPlayer = true
                    end
                end

                if isPlayer then
                    local spellId = select(9, ...)
                    local spellName = select(10, ...)
                    if not isQualifying(spellId, spellName) then
                        spellId = select(10, ...)
                        spellName = select(11, ...)
                    end

                    if isQualifying(spellId, spellName) then
                        local timestamp = select(1, ...)
                        local destGUID = select(6, ...) or ""
                        local eventKey = tostring(timestamp) .. "_" .. tostring(spellId) .. "_" .. tostring(destGUID)

                        if hs.lastEventKey ~= eventKey then
                            hs.lastEventKey = eventKey

                            local c18, c19, c20 = select(18, ...)
                            local isCrit = (c18 == true or c18 == 1 or c19 == true or c19 == 1 or c20 == true or c20 == 1)

                            if isCrit then
                                if hs.streak == 0 then
                                    hs.streak = 1
                                else
                                    hs.streak = 0
                                end
                            else
                                hs.streak = 0
                            end
                            notifyWA()
                        end
                    end
                end
            end
        end
    end

    _G.FMHUD_HandleHSEvent = handleEvent

    local f = _G.FMHUD_HSFrame
    if not f then
        f = CreateFrame("Frame", "FMHUD_HSFrame")
        _G.FMHUD_HSFrame = f
    end
    f:UnregisterAllEvents()
    f:RegisterEvent("PLAYER_ENTERING_WORLD")
    f:RegisterEvent("PLAYER_DEAD")
    f:RegisterEvent("PLAYER_UNGHOST")
    f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
    f:SetScript("OnEvent", function(self, ev, ...)
        if _G.FMHUD_HandleHSEvent then
            _G.FMHUD_HandleHSEvent(ev, ...)
        end
    end)

    if event then
        handleEvent(event, ...)
    end
    return hs
end"""

def make_hotstreak_bg_trigger() -> str:
    return """function(event, ...)
    _G.FMHUD_InitHotStreak = (""" + SHARED_HOTSTREAK_CHECK_LUA + """)
    _G.FMHUD_InitHotStreak(event, ...)
    return not UnitIsDeadOrGhost("player")
end"""

def make_hotstreak_bg_untrigger() -> str:
    return """function(event, ...)
    return UnitIsDeadOrGhost("player")
end"""

def make_hotstreak_seg1_trigger() -> str:
    return """function(event, ...)
    _G.FMHUD_InitHotStreak = (""" + SHARED_HOTSTREAK_CHECK_LUA + """)
    _G.FMHUD_InitHotStreak(event, ...)
    local hs = _G.FMHUD_HS
    return (hs and hs.streak == 1)
end"""

def make_hotstreak_seg1_untrigger() -> str:
    return """function(event, ...)
    local hs = _G.FMHUD_HS
    return not (hs and hs.streak == 1)
end"""

