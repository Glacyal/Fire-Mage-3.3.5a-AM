# Fire Mage HUD — configurazione diretta in `/wa`

Struttura creata:

```text
Fire Mage HUD (Gruppo Master - yOffset = -150)
├── 01 - Procs (Dynamic Group orizzontale)
│   ├── Hot Streak
│   ├── Living Bomb
│   ├── Ignite
│   ├── Combustion
│   └── Molten Fury
├── 02 - Molten Armor (Ala Sinistra, x = -155)
├── 04 - Focus Magic (Ala Destra, x = +155 - scompare se applicato ad un alleato)
├── 05 - Trinket 1 (Slot 13, x = -51, y = -48)
├── 05 - Trinket 2 (Slot 14, x = -17, y = -48)
├── 06 - Cloak (Slot 15, x = +17, y = -48)
├── 06 - Mana Gem (Item 33312 + cariche, x = +51, y = -48)
├── 07 - Mana Bar (Solo % a 2 decimali)
├── 08 - Castbar
├── 09 - GCD
└── 10 - Alerts (Hot Streak Alert)
```

Layout: proc sopra la castbar; castbar al centro (`y = 0`), mana sotto (`y = -26`); GCD compatto (`y = -13`); riga utility a 4 icone sotto il mana (`y = -48`); Molten Armor e Focus Magic alle ali (`x = -155` e `+155`); alert sopra i proc.
L'intera HUD è abbassata a `yOffset = -150` per non coprire il personaggio né interferire con i raid frames a sinistra o Omen3 a destra.

## Moduli nativi

- **Hot Streak**: Icona → Trigger Aura / Player / Buff / ID verificato; testo `%p` e Pixel Glow.
- **Living Bomb e Ignite**: Icona → Aura / Target / Debuff / ID verificato; testo `%p`.
- **Combustion**: Icona → Spell Cooldown / ID 11129; mostra cooldown progressivo.
- **Mana Bar**: Progress Bar → Status / Power / Player; mostra solo la percentuale `%1.percentpower%%` con 2 decimali.
- **Castbar**: Progress Bar → Status / Cast / Player; compare solo durante il cast con icona e tempo.
- **GCD**: Progress Bar → Spell Cooldown 61304; barra sottile di 4px.
- **Alert Hot Streak**: Aura Text → con testo ingrandito `HOT STREAK! / PYROBLAST READY!`.

## Molten Armor: monitor permanente
- `Molten Armor - Active`: Icona attiva con timer dei minuti residui.
- `Molten Armor - OFF`: Icona desaturata grigia con testo `OFF` se il buff non è attivo sul Mago.

## Focus Magic: monitor intelligente
- `Focus Magic - Active`: Icona attiva con timer del proc critico (%p, 10 secondi).
- `Focus Magic - OFF`: Icona desaturata grigia con testo `OFF` se **non è stato messo a nessuno**.
  Non appena viene applicato ad un qualsiasi alleato (in raid, party, o target), l'avviso OFF scompare immediatamente per tutti i 30 minuti tramite tracciamento automatico di combat log, spellcast e scansione roster.

## Utility: Trinket 1, Trinket 2, Cloak e Gemma del Mana
Fila orizzontale di 4 icone da 26x26 a `y = -48`:
- Slot 13 (Trinket 1): `x = -51`
- Slot 14 (Trinket 2): `x = -17`
- Slot 15 (Mantello con ricamo/ingegneria): `x = +17`
- Gemma del Mana (Mana Sapphire 33312 / Emerald 22044): `x = +51`
  Mostra il cooldown (%p) e in basso a destra le cariche rimanenti in borsa (%c).
