# Fire Mage HUD — configurazione diretta in `/wa`

Struttura da creare:

```text
Fire Mage HUD
├── 01 - Procs (Dynamic Group)
│   ├── Hot Streak
│   ├── Living Bomb - Target
│   ├── Ignite - Target
│   ├── Combustion
│   └── Molten Fury
├── 02 - Molten Armor
├── 03 - Target
├── 04 - Focus
├── 05 - Trinkets (Trinket 1, Trinket 2)
├── 06 - Cloak
├── 07 - Mana
├── 08 - Castbar
├── 09 - GCD
└── 10 - Alerts (Hot Streak Alert)
```

Layout: proc sopra la castbar; castbar al centro, mana sotto; GCD compatto accanto; target/focus e trinket ai lati; Molten Armor molto visibile a sinistra della zona centrale; alert sopra i proc.

## Moduli nativi

- **Hot Streak**: Icona → Trigger Aura / Player / Buff / ID verificato; testo `%p` e `%s`; Start Animation Zoom.
- **Living Bomb e Ignite**: Icona → Aura / Target / Debuff / ID verificato; testo `%p`.
- **Combustion**: Icona → Spell Cooldown / ID verificato; Conditions per READY e cooldown. Se vuoi il buff separato, aggiungi una seconda aura Aura/Player/Buff.
- **Mana**: Progress Bar → Status / Power o Mana / Player; Conditions >50, 30–50, <30, <15.
- **Castbar**: Progress Bar → Status / Cast / Player. Se il fork non gestisce il channel, crea una seconda barra Channel.
- **GCD**: Status → Global Cooldown. Non riusare il trigger Cast.
- **Alert Hot Streak**: aura distinta con lo stesso Buff Trigger di Hot Streak, testo `HOT STREAK!\nPYROBLAST READY!` e Start Animation; resta disattivabile in modo indipendente.

## Molten Armor: monitor permanente

Crea un gruppo statico con due aura figlie:

1. `Molten Armor - Active`: Aura / Player / Buff / ID Molten Armor; mostra icona, nome e `%p`.
2. `Molten Armor - OFF`: stesso trigger invertito con “Aura assente”; testo `MOLTEN ARMOR OFF\nWARNING`, icona desaturata e pulse rosso.

Se il fork non supporta il trigger invertito, usa questo Custom Trigger Event con eventi `UNIT_AURA PLAYER_ENTERING_WORLD`:

```lua
function(event, unit)
  local wanted = GetSpellInfo(0) -- SOSTITUIRE 0 con ID Molten Armor
  for i = 1, 40 do
    local name = UnitBuff("player", i)
    if not name then break end
    if name == wanted then return false end
  end
  return true
end
```

## Target, Focus e Molten Fury

Target/Focus sono aura Text con Custom Trigger Event. Eventi Target: `PLAYER_TARGET_CHANGED UNIT_HEALTH UNIT_MAXHEALTH`; per Focus sostituisci con `PLAYER_FOCUS_CHANGED` e `focus`.

```lua
function(event, unit)
  return true -- modulo permanente: il testo ricalcola sempre lo stato del target
end
```

Testo Target:

```lua
if not UnitExists("target") then return "NO TARGET" end
if UnitIsDeadOrGhost("target") then return "TARGET DEAD" end
local hp, max = UnitHealth("target"), UnitHealthMax("target")
return string.format("TARGET: %s\n%.1f%%  %d / %d", UnitName("target") or "?", max > 0 and hp * 100 / max or 0, hp, max)
```

Per Molten Fury, Custom Trigger Event con `PLAYER_TARGET_CHANGED UNIT_HEALTH UNIT_MAXHEALTH`:

```lua
function(event, unit)
  if not UnitExists("target") or UnitIsDeadOrGhost("target") then return false end
  local max = UnitHealthMax("target")
  return max > 0 and UnitHealth("target") * 100 / max <= 35
end
```

## Trinket 1, Trinket 2 e Cloak

Ogni slot è una Text/Icon aura separata. Custom Trigger Event: `PLAYER_ENTERING_WORLD PLAYER_EQUIPMENT_CHANGED UNIT_AURA SPELL_UPDATE_COOLDOWN`.

```lua
function(event, unit)
  return true -- il testo gestisce READY/ACTIVE/CD; il modulo resta sempre visibile
end
```

Testo custom (slot 13; sostituisci con 14 per Trinket 2, 15 per Cloak):

```lua
local slot, procID = 13, 0 -- SOSTITUIRE procID
local itemID = GetInventoryItemID("player", slot)
local name = itemID and GetItemInfo(itemID) or "Trinket 1"
local procName = GetSpellInfo(procID)
if procName then
  for i = 1, 40 do
    local buff, _, _, _, _, duration, expiration = UnitBuff("player", i)
    if not buff then break end
    if buff == procName then return string.format("%s\nACTIVE %.1fs", name, math.max(0, expiration - GetTime())) end
  end
end
local start, duration = GetInventoryItemCooldown("player", slot)
if start and duration and start > 0 and duration > 1.5 then
  return string.format("%s\nCD %.1fs", name, math.max(0, start + duration - GetTime()))
end
return name .. "\nREADY"
```

Per mantenere il countdown del testo aggiornato, nella tab Display abilita `Update Custom Text On` → `Every Frame` (se presente nel fork). Se non è presente, usa due aure native: una `Item Cooldown` per il CD e una `Aura/Player/Buff` per il proc; è l'alternativa più affidabile.

## Living Bomb MISSING e debug

Duplica Living Bomb, inverti il trigger “debuff assente”, usa testo `LIVING BOMB\nMISSING`: resta una scelta visuale modificabile in `/wa`.

Per errori: `/console scriptErrors 1`, poi `/reload` e riproduci il caso. Verifica tutti gli ID sul tuo server prima di inserirli.
