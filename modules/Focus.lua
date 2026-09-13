-- =========================================================================
-- Fire Mage HUD 3.3.5a — Modulo 04: Focus Monitor (Focus Magic & Focus Target)
-- =========================================================================
-- Monitora in tempo reale lo stato del Focus per il Mago Fire:
-- 1. Focus Magic Monitor (ala destra della HUD, simmetrico a Molten Armor):
--    - Se Focus Magic e' ATTIVO / PROC: icona a colori con swipe e timer %p.
--    - Se Focus Magic e' ASSENTE / OFF: icona desaturata grigia con testo "OFF".
-- 2. Living Bomb (Focus):
--    - Nel gruppo dinamico "01 - Procs", monitora la presenza di Living Bomb
--      sul bersaglio Focus: appare solo quando e' applicata con countdown %p e tag [F].
-- =========================================================================

local FOCUS_MAGIC_SPELL_ID = 54646 -- Buff 30 min / Spell
local FOCUS_MAGIC_PROC_ID  = 54648 -- Proc 10 sec (+3% spell crit)
local LIVING_BOMB_SPELL_ID = 55360 -- Debuff Living Bomb

-- =========================================================================
-- TRIGGER FOCUS MAGIC (Buff / Proc sul Giocatore)
-- =========================================================================
function FireMageHUD_FocusMagic_Trigger()
    -- Controlla se il giocatore ha il buff o il proc di Focus Magic
    local name, _, icon, count, debuffType, duration, expirationTime = UnitBuff("player", "Focus Magic")
    if name then
        return true, duration, expirationTime
    end
    return false
end

-- =========================================================================
-- TRIGGER LIVING BOMB ON FOCUS (Debuff sul bersaglio Focus)
-- =========================================================================
function FireMageHUD_LivingBomb_Focus_Trigger()
    if not UnitExists("focus") then return false end
    local name, _, icon, count, debuffType, duration, expirationTime, caster = UnitDebuff("focus", "Living Bomb")
    if name and caster == "player" then
        return true, duration, expirationTime
    end
    return false
end
