"""
Modulo Componente: 05 - Trinkets & 06 - Utility Row
====================================================
Gestisce la fila orizzontale utility a y = -45 con riposizionamento dinamico
a 6 o 7 icone (se il Tier 8 è equipaggiato o meno):
1. 05 - Trinket 1 (Slot 13, ICD 45s/90s/120s o On-Use, Pixel Glow su proc)
2. 05 - Trinket 2 (Slot 14, ICD 45s/90s/120s o On-Use, Pixel Glow su proc)
3. 06 - Cloak (Slot 15, Ricamo Spadatesta / Luce Intessuta ICD 45s)
4. 06 - Tier 8 (Attivo solo con >= 2 pezzi T8 Kirin Tor, Praxis +350 SP, 45s ICD)
5. 06 - Mana Gem (Gemma del Mana, Cooldown + cariche in borsa + Proc T7 Mana Surge)
6. 06 - Combustion (Combustione, stato ON, stack critici rimanenti, cooldown)
7. 06 - Mirror Image (Copie, durata 30s + Bonus T10 4P Quad Core +18% danni)
"""
from builder.core.helpers import make_subtext


# =============================================================================
# LOGICA LUA CONDIVISA: TRINKETS E CLOAK ICD TRACKING
# =============================================================================
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
    """Testo descrittivo del monile/mantello (%c), con pixel glow su proc attivo e riposizionamento dinamico."""
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
    """Durata e scadenza dello swipe di ricarica per lo slot indicato."""
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
    """Restituisce dinamicamente l'icona dell'oggetto equipaggiato o del proc attivo."""
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


# =============================================================================
# LOGICA LUA CONDIVISA: TIER 8 2-PIECE BONUS & LAYOUT DINAMICO A 6/7 ICONE
# =============================================================================
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


def make_t8_custom_text() -> str:
    """Testo descrittivo del Tier 8 2P (%c), con pixel glow su proc attivo e timer ICD."""
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
    """Durata e scadenza dello swipe di ricarica per il Tier 8 2P."""
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
    """Icona del Tier 8 2P (Praxis / Kirin Tor)."""
    return f"""function()
    if not _G.FMHUD_T8_InitDone then
        _G.FMHUD_InitT8 = {SHARED_T8_INIT_LUA}
        _G.FMHUD_InitT8()
    end
    local state, rem, dur, icon, isEquipped = _G.FMHUD_CheckT8()
    return icon or GetSpellTexture(64868) or "Interface\\\\Icons\\\\Spell_Arcane_StudentOfMagic"
end"""


# =============================================================================
# LOGICA LUA CONDIVISA: COMBUSTION
# =============================================================================
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
    """Testo descrittivo (%c) di Combustion con conteggio cariche critiche e pixel glow dorato."""
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
    """Durata e scadenza per lo swipe di Combustion (CD o buff attivo)."""
    return f"""function()
    _G.FMHUD_CheckCombustion = _G.FMHUD_CheckCombustion or {SHARED_COMBUSTION_CHECK_LUA}
    local state, rem, dur = _G.FMHUD_CheckCombustion()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""


# =============================================================================
# LOGICA LUA CONDIVISA: MIRROR IMAGE & TIER 10 4P QUAD CORE
# =============================================================================
SHARED_MIRRORIMAGE_CHECK_LUA = """function()
    local now = GetTime()
    local baseIcon = GetSpellTexture(55342) or "Interface\\\\Icons\\\\Spell_Magic_LesserInvisibilty"
    local quadCoreIcon = GetSpellTexture(70747) or "Interface\\\\Icons\\\\Spell_Nature_Invisibilty"
    
    -- 1. Controllo pezzi T10 equipaggiati
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
        if elapsed >= 0 and elapsed < 30 then
            local remActive = 30 - elapsed
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
    """Testo descrittivo (%c) delle Copie (Mirror Image): durata attiva 30s con proc T10 (+18% danni) o CD 3 min."""
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
    """Durata e scadenza per lo swipe di Mirror Image / proc T10."""
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
    """Icona Quad Core (Spell_Nature_Invisibilty) durante il proc T10, altrimenti Mirror Image."""
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


# =============================================================================
# LOGICA LUA CONDIVISA: MANA GEM & PROC T7 MANA SURGE
# =============================================================================
SHARED_MANAGEM_CHECK_LUA = """function()
    local now = GetTime()
    local isT7Active = false
    local remT7 = 0
    local durT7 = 15
    local baseIcon = (GetItemCount(33312) == 0 and GetItemCount(22044) > 0)
                     and "Interface\\\\Icons\\\\INV_Misc_Gem_Emerald_01"
                     or  "Interface\\\\Icons\\\\INV_Misc_Gem_Sapphire_02"
    local procIcon = nil

    -- 1. Controllo buff bonus 2 pezzi T7 Mago (+225 Spell Power per 15s)
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

    -- 2. Controllo cooldown oggetto Gemma del Mana (33312 / 22044)
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
    """Testo descrittivo (%c) delle cariche della Gemma del Mana, con Pixel Glow durante proc T7."""
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
    """Durata e scadenza per lo swipe di ricarica della Gemma del Mana."""
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
    """Restituisce dinamicamente la texture del proc T7 (Mana Surge) o Gemma del Mana."""
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


# =============================================================================
# BUILDER: AURE WEAKAURAS PER LA FILA UTILITY
# =============================================================================
def build_utility_auras() -> list[dict]:
    """
    Costruisce e restituisce le 7 aure che compongono la fila utility inferiore:
    - 05 - Trinket 1 (Icon)
    - 05 - Trinket 2 (Icon)
    - 06 - Cloak (Icon)
    - 06 - Tier 8 (Icon)
    - 06 - Mana Gem (Icon)
    - 06 - Combustion (Icon)
    - 06 - Mirror Image (Icon)
    """
    return [
        # 05 - Trinket 1 (Slot 13)
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
                        "customIcon": make_slot_custom_icon(13, "Interface\\Icons\\INV_Misc_QuestionMark"),
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 05 - Trinket 2 (Slot 14)
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
                        "customIcon": make_slot_custom_icon(14, "Interface\\Icons\\INV_Misc_QuestionMark"),
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 06 - Cloak (Slot 15)
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
                        "customIcon": make_slot_custom_icon(15, "Interface\\Icons\\INV_Misc_Cape_19"),
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 06 - Tier 8
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 06 - Mana Gem
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
                {"type": "subbackground"},
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

        # 06 - Combustion
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
    return "Interface\\Icons\\Spell_Fire_SealOfFire"
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 06 - Mirror Image
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
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },
    ]
