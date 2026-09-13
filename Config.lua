-- =========================================================================
-- Fire Mage HUD 3.3.5a — Tabella di Configurazione Centrale
-- Compatibile con World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340)
-- =========================================================================

FireMageHUD_Config = {
    -- Modalità Debug: quando impostata su true stampa informazioni diagnostiche in chat
    -- relative a proc, buff, debuff, cast e target/focus rilevati.
    Debug = false,

    -- =====================================================================
    -- 1. SOGLIE E COLORI MANA
    -- =====================================================================
    Mana = {
        Thresholds = {
            High = 50,      -- > 50%: Mana normale (default: Blu)
            Medium = 30,    -- 30% - 50%: Attenzione (default: Giallo)
            Low = 15,       -- 15% - 30%: Basso (default: Arancione)
            Critical = 15,  -- < 15%: Critico (default: Rosso lampeggiante)
        },
        Colors = {
            High     = { r = 0.00, g = 0.55, b = 1.00, a = 1.0 }, -- Blu Mana
            Medium   = { r = 1.00, g = 0.85, b = 0.10, a = 1.0 }, -- Giallo / Ambra
            Low      = { r = 1.00, g = 0.45, b = 0.00, a = 1.0 }, -- Arancione
            Critical = { r = 1.00, g = 0.10, b = 0.10, a = 1.0 }, -- Rosso Critico
        },
        Format = "SHORT", -- "SHORT" (es. 14.8k / 16.0k) oppure "FULL" (es. 14820 / 16000)
    },

    -- =====================================================================
    -- 2. SPELL ID E PROC FIRE MAGE (3.3.5a)
    -- =====================================================================
    Spells = {
        -- Molten Armor (Rank 3: 43046, Rank 2: 43045, Rank 1: 30482)
        MoltenArmor = {
            Rank3 = 43046,
            Rank2 = 43045,
            Rank1 = 30482,
            Name = "Molten Armor", -- fallback per ricerca per nome
        },

        -- Hot Streak proc (rende il prossimo Pyroblast istantaneo)
        HotStreak = {
            BuffID = 48108,
            Name = "Hot Streak",
        },

        -- Pyroblast
        Pyroblast = {
            SpellID = 42891, -- Rank 12 (WotLK max rank)
            Name = "Pyroblast",
        },

        -- Living Bomb (Rank 3)
        LivingBomb = {
            SpellID = 55360,
            DebuffID = 55360,
            ExplosionID = 55362,
            Name = "Living Bomb",
            Duration = 12.0,
        },

        -- Ignite (Debuff applicato dai critici Fire)
        Ignite = {
            DebuffID = 12654,
            Name = "Ignite",
            Duration = 4.0,
        },

        -- Combustion (Talento Fire: Cooldown 2 min)
        Combustion = {
            SpellID = 11129,
            BuffID = 28682, -- Buff attivo con cariche critiche
            Name = "Combustion",
            Cooldown = 120,
        },

        -- Molten Fury (Talento passivo: danno aumentato su bersagli <= 35% HP)
        MoltenFury = {
            ThresholdPercent = 35.0,
            TalentTab = 2, -- Fire tree
            TalentIndex = 20, -- Molten Fury
        },

        -- Fire Blast (utilizzato anche per fallback controllo GCD)
        FireBlast = {
            SpellID = 42873, -- Rank 9
            Name = "Fire Blast",
        },

        -- Frostfire Bolt
        FrostfireBolt = {
            SpellID = 47610, -- Rank 2
            Name = "Frostfire Bolt",
        },

        -- Fireball
        Fireball = {
            SpellID = 42833, -- Rank 16
            Name = "Fireball",
        },

        -- Global Cooldown spell di riferimento standard 3.3.5a
        GCDReferenceSpell = 61304,
    },

    -- =====================================================================
    -- 3. TRINKETS (Slot 13 e 14)
    -- =====================================================================
    -- Predisposto per modificare facilmente gli ID senza riscrivere la logica
    Trinket1 = {
        Slot = 13,
        Name = "Trinket 1",
        ItemID = 0,         -- Sostituire con l'Item ID del tuo Trinket 1 (es. 50348 per DFO, 54588 per CTS)
        BuffID = 0,         -- Sostituire con il Buff ID del proc passivo se applicabile (es. 71601 per DFO)
        InternalCD = 45,    -- Durata stimata dell'ICD in secondi per i proc passivi (es. 45 o 90s)
        IsOnUse = false,    -- true se il trinket è 'Usa:' (On-Use), false se è un proc passivo 'Equipaggia:'
    },

    Trinket2 = {
        Slot = 14,
        Name = "Trinket 2",
        ItemID = 0,         -- Sostituire con l'Item ID del tuo Trinket 2 (es. 50365 per Phylactery)
        BuffID = 0,         -- Sostituire con il Buff ID del proc passivo (es. 71605 per Phylactery)
        InternalCD = 45,    -- ICD stimato (es. 90 per Phylactery, 45 per CTS/DFO)
        IsOnUse = false,
    },

    -- =====================================================================
    -- 4. CLOAK / ENCHANT (Slot 15)
    -- =====================================================================
    Cloak = {
        Slot = 15,
        Name = "Cloak Enchant",
        BuffID = 55637,     -- Default: Lightweave Embroidery (Sartoria: 295 Spell Power per 15s)
        InternalCD = 45,    -- ICD stimato per Lightweave Embroidery (45 secondi)
        IsOnUse = false,    -- true per enchant di Ingegneria 'Usa:' (es. paracadute/springy), false per proc passivi
    },

    -- =====================================================================
    -- 5. ALERTS E ANIMAZIONI
    -- =====================================================================
    Alerts = {
        HotStreak = {
            Enabled = true,
            Duration = 3.0,     -- Durata visibilità alert
            Text = "HOT STREAK!\nPYROBLAST READY!",
            Sound = "Interface\\AddOns\\WeakAuras\\PowerAurasMedia\\Sounds\\wilhelm.ogg", -- Opzionale
        },
        MoltenArmorMissing = {
            Enabled = true,
            OnlyInCombat = false, -- se true allerta solo in combattimento, se false sempre
            Text = "MOLTEN ARMOR OFF\nWARNING",
        },
    },

    -- =====================================================================
    -- 6. IMPOSTAZIONI TARGET E FOCUS
    -- =====================================================================
    Target = {
        ShowHealthValues = true, -- Mostra valore numerico HP
        ShowPercentage = true,   -- Mostra percentuale HP
        ShowDebuffs = true,      -- Mostra Living Bomb / Ignite sul target
    },

    Focus = {
        ShowHealthValues = true,
        ShowPercentage = true,
        NoFocusText = "NO FOCUS",
        DeadFocusText = "FOCUS DEAD",
    },
}

