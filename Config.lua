--- =========================================================================
--- Fire Mage 3.3.5a AM — Configurazione Centrale
--- Compatibile con World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340)
--- Tabella SavedVariables opzionale per l'addon stand-alone FireMageHUD.
--- =========================================================================

---@class FireMageHUD_ConfigTable
---@field Debug boolean Abilita l'output di messaggi diagnostici in chat
---@field Mana table Parametri di soglia, colore e formattazione per la barra del Mana
---@field Spells table Mappatura ID magie, rank, debuff e durate per Fire Mage
---@field Trinket1 table Configurazione slot 13 (Trinket 1)
---@field Trinket2 table Configurazione slot 14 (Trinket 2)
---@field Cloak table Configurazione slot 15 (Ricamo o incantamento Mantello)
---@field Tier8 table Configurazione bonus 2P Tier 8 (Praxis: +350 SP, 45s ICD)
---@field Alerts table Impostazioni per avvisi a schermo (Hot Streak, Molten Armor)
---@field Target table Preferenze di visualizzazione dati target
---@field Focus table Preferenze di visualizzazione dati focus

FireMageHUD_Config = {
    -- Diagnostica: se true, stampa in chat eventi di proc, buff/debuff e cambi target
    Debug = false,

    -- ---------------------------------------------------------------------
    -- 1. SOGLIE E COLORI MANA
    -- ---------------------------------------------------------------------
    Mana = {
        Thresholds = {
            High     = 50,  -- > 50%: Mana regolare (Blu standard)
            Medium   = 30,  -- 30% - 50%: Livello intermedio (Giallo)
            Low      = 20,  -- 20% - 30%: Attenzione (Arancione)
            Critical = 20,  -- <= 20%: Critico (Rosso vivo)
        },
        Colors = {
            High     = { r = 0.00, g = 0.55, b = 1.00, a = 1.0 }, -- Blu Mana
            Medium   = { r = 1.00, g = 0.85, b = 0.10, a = 1.0 }, -- Giallo / Ambra
            Low      = { r = 1.00, g = 0.45, b = 0.00, a = 1.0 }, -- Arancione
            Critical = { r = 1.00, g = 0.15, b = 0.15, a = 1.0 }, -- Rosso Critico
        },
        Format = "SHORT", -- "SHORT" (es. 14.8k / 16.0k) oppure "FULL" (es. 14820 / 16000)
    },

    -- ---------------------------------------------------------------------
    -- 1B. BARRA HOT STREAK (Sotto Mana Bar a y = -25, 264x7px, no testo)
    -- Dinamica: 1° critico illumina metà barra a sx (50%), al 2° critico
    -- i due segmenti diventano un'unica barra continua da 264px con swipe 10s!
    -- ---------------------------------------------------------------------
    HotStreakBar = {
        Width = 264,
        Height = 7,
        HalfWidth = 130,     -- Metà barretta 50% sul 1° critico
        InnerHeight = 5,
        Colors = {
            FirstCrit  = { r = 1.00, g = 0.55, b = 0.00, a = 1.0 }, -- Ambra / Arancio vivo (1° critico persistente)
            ProcBar    = { r = 1.00, g = 0.35, b = 0.00, a = 1.0 }, -- Rosso fuoco / Arancio acceso (Proc 10s unificato)
            Glow       = { r = 1.00, g = 0.60, b = 0.00, a = 1.0 }, -- Pixel Glow dorato/arancio durante proc
            Background = { r = 0.05, g = 0.05, b = 0.05, a = 0.85 }, -- Sfondo scuro cornice
        },
    },

    -- ---------------------------------------------------------------------
    -- 2. SPELL ID E RIFERIMENTI FIRE MAGE (WotLK 3.3.5a)
    -- ---------------------------------------------------------------------
    Spells = {
        -- Armatura Ardente (Molten Armor)
        MoltenArmor = {
            Rank3 = 43046,
            Rank2 = 43045,
            Rank1 = 30482,
            Name  = "Molten Armor",
        },

        -- Proc Hot Streak (Lancio istantaneo di Pyroblast)
        HotStreak = {
            BuffID = 48108,
            Name   = "Hot Streak",
        },

        -- Pyroblast (Rank 12 max in WotLK)
        Pyroblast = {
            SpellID = 42891,
            Name    = "Pyroblast",
        },

        -- Bomba Vivente (Living Bomb Rank 3)
        LivingBomb = {
            SpellID     = 55360,
            DebuffID    = 55360,
            ExplosionID = 55362,
            Name        = "Living Bomb",
            Duration    = 12.0,
        },

        -- Ignizione (Ignite, debuff da colpi critici Fire)
        Ignite = {
            DebuffID = 12654,
            Name     = "Ignite",
            Duration = 4.0,
        },

        -- Scorch / Improved Scorch (+5% critico magico al bersaglio)
        Scorch = {
            DebuffID = 22959,
            Name     = "Improved Scorch",
            AltName  = "Scorch",
            Duration = 30.0,
        },

        -- Combustione (Combustion, talento Fire)
        Combustion = {
            SpellID  = 11129,
            BuffID   = 28682,
            Name     = "Combustion",
            Cooldown = 120,
        },

        -- Copie (Mirror Image / Proc 4P T10)
        MirrorImage = {
            SpellID     = 55342,
            Name        = "Mirror Image",
            AltName     = "Immagine Speculare",
            Cooldown    = 180,
            Duration    = 30.0,
            T10BuffID   = 70747,
            T10BuffName = "Quad Core",
        },

        -- Furia Incandescente (Molten Fury, talento execute <= 35% HP bersaglio)
        MoltenFury = {
            ThresholdPercent = 35.0,
            TalentTab        = 2,
            TalentIndex      = 20,
        },

        -- Fire Blast (usato anche per verifica fallback cooldown)
        FireBlast = {
            SpellID = 42873,
            Name    = "Fire Blast",
        },

        -- Frostfire Bolt
        FrostfireBolt = {
            SpellID = 47610,
            Name    = "Frostfire Bolt",
        },

        -- Fireball
        Fireball = {
            SpellID = 42833,
            Name    = "Fireball",
        },

        -- Magia di riferimento standard per il Global Cooldown (GCD)
        GCDReferenceSpell = 61304,
    },

    -- ---------------------------------------------------------------------
    -- 3. TRINKET (Slot 13 e 14)
    -- ---------------------------------------------------------------------
    Trinket1 = {
        Slot       = 13,
        Name       = "Trinket 1",
        ItemID     = 0,     -- Auto-rilevato da inventario; impostabile manualmente
        BuffID     = 0,     -- Auto-rilevato dal database trinket; impostabile per proc custom
        InternalCD = 45,    -- ICD stimato in secondi (es. 45s DFO/CTS, 90s Filatterio)
        IsOnUse    = false, -- true per oggetti On-Use, false per proc passivi
    },

    Trinket2 = {
        Slot       = 14,
        Name       = "Trinket 2",
        ItemID     = 0,
        BuffID     = 0,
        InternalCD = 45,
        IsOnUse    = false,
    },

    -- ---------------------------------------------------------------------
    -- 4. MANTELLO / RICAMO (Slot 15)
    -- ---------------------------------------------------------------------
    Cloak = {
        Slot       = 15,
        Name       = "Cloak Enchant",
        BuffID     = 55637, -- Predefinito: Ricamo della Tessitura della Luce (Sartoria: +295 SP per 15s)
        InternalCD = 45,    -- ICD stimato per il ricamo (45 secondi)
        IsOnUse    = false, -- true per paracadute o ingegneria attiva
    },

    -- ---------------------------------------------------------------------
    -- 5. AVVISI TESTUALI A SCHERMO
    -- ---------------------------------------------------------------------
    Alerts = {
        HotStreak = {
            Enabled  = true,
            Duration = 3.0,
            Text     = "HOT STREAK!\nPYROBLAST READY!",
            Sound    = "Interface\\AddOns\\WeakAuras\\PowerAurasMedia\\Sounds\\wilhelm.ogg",
        },
        MoltenArmorMissing = {
            Enabled      = true,
            OnlyInCombat = false,
            Text         = "MOLTEN ARMOR OFF\nWARNING",
        },
    },

    -- ---------------------------------------------------------------------
    -- 6. IMPOSTAZIONI BERSAGLIO E FOCUS
    -- ---------------------------------------------------------------------
    Target = {
        ShowHealthValues = true,
        ShowPercentage   = true,
        ShowDebuffs      = true,
    },

    Focus = {
        ShowHealthValues = true,
        ShowPercentage   = true,
        NoFocusText      = "NO FOCUS",
        DeadFocusText    = "FOCUS DEAD",
    },

    -- ---------------------------------------------------------------------
    -- 7. REAL-TIME STATS PANEL (Modulo 12: SP, Crit, Haste, Hit)
    -- ---------------------------------------------------------------------
    Stats = {
        Enabled          = true,
        IncludeTargetHit = true,  -- Se true, include il debuff +3% Hit sul target (Misery / Faerie Fire)
        XOffset          = -180,  -- Offset X relativo al centro dell'HUD
        YOffset          = -54,   -- Offset Y relativo al centro dell'HUD
        Width            = 88,
        Height           = 48,
    },

    -- ---------------------------------------------------------------------
    -- 8. GEMMA DEL MANA (Mana Gem & Bonus 2 Pezzi T7)
    -- ---------------------------------------------------------------------
    ManaGem = {
        T7BuffID     = 61062, -- Mana Surge (+225 Spell Power per 15s)
        CooldownItem = 33312, -- Mana Sapphire (2 min CD)
        ChargesMax   = 3,
    },

    -- ---------------------------------------------------------------------
    -- 9. TIER 8 2-PIECE BONUS (Praxis: +350 SP per 15s, 45s ICD)
    -- ---------------------------------------------------------------------
    Tier8 = {
        BuffID     = 64868, -- Praxis (+350 Spell Power per 15s)
        TriggerID  = 64867, -- Item - Mage T8 2P Bonus
        InternalCD = 45,    -- ICD stimato in secondi (15s attivo + 30s CD)
        Duration   = 15.0,  -- Durata buff attivo
        Icon       = "Interface\\Icons\\Spell_Arcane_StudentOfMagic",
        SetPieces  = {
            -- 10-Man (Kirin Tor Valoroso)
            [45367] = true, -- Elmo
            [45369] = true, -- Spalle
            [45365] = true, -- Torso
            [45366] = true, -- Gambe
            [45368] = true, -- Guanti
            -- 25-Man (Kirin Tor Conquistatore)
            [45357] = true, -- Elmo
            [45359] = true, -- Spalle
            [45355] = true, -- Torso
            [45356] = true, -- Gambe
            [45358] = true, -- Guanti
        },
    },

    -- ---------------------------------------------------------------------
    -- 10. TIER 10 2-PIECE BONUS / FROSTFORGED SAGE
    -- ---------------------------------------------------------------------
    Tier10 = {
        BuffID     = 70753, -- Pushing the Limit (+12% Haste per 5s) / Frostforged Sage
        AltBuffID  = 72416, -- Frostforged Sage (+285 SP, 10s durata, 60s ICD)
        Duration   = 5.0,   -- Durata buff base (5s T10 2P, 10s ring)
        InternalCD = 0,     -- 0s per T10 2P (60s se proc anello ICC)
        Icon       = "Interface\\Icons\\Spell_Frost_FrostWard",
        SetPieces  = {
            -- 251 Normal (Regalia del Mago del Sangue)
            [50278] = true, -- Elmo
            [50279] = true, -- Spalle
            [50275] = true, -- Torso
            [50277] = true, -- Gambe
            [50276] = true, -- Guanti
            -- 264 Santificato (Regalia Santificata del Mago del Sangue)
            [51283] = true, -- Elmo
            [51284] = true, -- Spalle
            [51280] = true, -- Torso
            [51282] = true, -- Gambe
            [51281] = true, -- Guanti
            -- 277 Eroico Santificato (Regalia Santificata del Mago del Sangue)
            [51303] = true, -- Elmo
            [51304] = true, -- Spalle
            [51300] = true, -- Torso
            [51302] = true, -- Gambe
            [51301] = true, -- Guanti
        },
    },
}
