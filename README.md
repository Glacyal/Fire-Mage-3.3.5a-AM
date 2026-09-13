# Fire Mage HUD 3.3.5a — WeakAuras 4.0.0 Suite

Suite WeakAura modulare, professionale e completa per **Mago Fire Livello 80** per World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

> [!IMPORTANT]
> **REGOLE CRUCIALI PER L'IMPORTAZIONE IN WEAKAURAS**:
> In WeakAuras, se importi un gruppo con lo stesso nome senza prima aver cancellato quello vecchio, WeakAuras **fonde (merge)** i moduli invece di sovrascriverli!
> **Procedura obbligatoria**: In `/wa`, fai clic destro su **`Fire Mage HUD`** $\rightarrow$ seleziona **`Delete children and group`** $\rightarrow$ solo DOPO incolla la nuova stringa da `IMPORT_STRING.txt`.

---

## Novità di Questo Aggiornamento

1. **Trinket & Mantello con Tracking Completo dei Proc & ICD (Internal Cooldown)**:
   - **Proc Attivo**: Quando il trinket (es. *The Dying Curse*, *Sundial of the Exiled*, *DFO*, *Phylactery*, *Charred Twilight Scale*, ecc.) o l'incantamento del Mantello (*Lightweave Embroidery*) si attivano, l'icona si illumina con un **Pixel Glow dorato animato**, swipe circolare e timer in secondi (`9.7s`).
   - **Fase ICD (Conto alla rovescia prima del prossimo reproc)**: Non appena il proc termina, il glow si spegne e l'icona mostra un conto alla rovescia in bianco (`35`, `34`, ...) che indica esattamente i secondi mancanti prima che l'effetto possa riattivarsi (ICD di 45s).
   - **Pronto (Ready)**: Allo scadere dell'ICD l'icona torna pulita senza testi, pronta al prossimo proc.
   - **Riconoscimento Spell ID Nativo 3.3.5a**: Supporto per *The Dying Curse* (Spell ID 60494, buff "Dying Curse"), *Sundial of the Exiled* (Spell ID 60064, buff "Now is the time!"), e tutti i trinket da caster di WotLK.

2. **Molten Armor Intelligente (Soglia 5 Minuti)**:
   - Mostra il timer di countdown (es. `4:30`) **solo ed esclusivamente se mancano meno di 5 minuti alla scadenza**.
   - Con durata superiore a 5 minuti, l'icona rimane pulita ed elegante, senza numeri superflui.
   - Se il buff è assente, l'icona diventa desaturata con avviso rosso **`OFF`**.

3. **Nuovo Modulo Arcane Intellect / Arcane Brilliance**:
   - Monitora la presenza del buff di intelletto (*Arcane Intellect*, *Arcane Brilliance*, *Dalaran Intellect*, *Dalaran Brilliance*, *Fel Intelligence*).
   - Posizionato nell'ala sinistra sopra Molten Armor (`x = -160, y = +22`).
   - Stessa logica anti-clutter: icona pulita se > 5 min, timer giallo se $\le 5$ min, e scritta rossa **`OFF`** se manca.

4. **Tracciamento Debuff Scorch / Improved Scorch**:
   - Integrato nel gruppo dinamico `01 - Procs` con icona, swipe circolare e secondi residui.
   - Allerta colorazione rossa quando il debuff scende sotto i 5 secondi, per non perdere mai il +5% critico magico sul boss.

5. **Scala Aumentata del +20% e Posizionamento Perfetto**:
   - Master scale impostato a **`1.2`** (+20% di grandezza complessiva).
   - Coordinata verticale impostata a **`yOffset = -190`**, posizionando l'intero HUD subito sopra le barre delle abilità di gioco senza coprire il personaggio o il combattimento.

---

## Come Aggiornare in Gioco (30 Secondi)

1. In gioco, digita `/wa`.
2. Fai clic destro su **`Fire Mage HUD`** e seleziona **`Delete children and group`**.
3. Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRING.txt)** e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
4. In `/wa`, clicca su **Import** in alto a sinistra.
5. Incolla la stringa con `Ctrl+V` nel riquadro.
6. Clicca su **Import Group**.
7. Chiudi WeakAuras (`Esc`). Fatto!

---

## Struttura e Coordinate dell'HUD

```text
Fire Mage HUD (Gruppo Master - Scale = 1.2, yOffset = -190, posizionato sopra le barre)
│
├── 01 - Procs (Dynamic Group orizzontale, y = +44 - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona 34x34 + Timer + Glow Pixel dorato)
│   ├── Living Bomb (Icona 34x34 + Timer debuff sul Target)
│   ├── Ignite (Icona 34x34 + Timer debuff sul Target)
│   ├── Scorch (Icona 34x34 Scorch/Improved Scorch + Timer + Avviso <= 5s)
│   ├── Combustion (Icona 34x34 con Cooldown Progress)
│   └── Molten Fury (Icona 34x34 attiva con Target HP <= 35%)
│
├── Ala Sinistra (Colonna Utility Personali - x = -160, 34px di spazio dalla Castbar)
│   ├── 03 - Arcane Intellect (y = +22, size 32x32: Icona pulita > 5m, Timer <= 5m, OFF rosso)
│   └── 02 - Molten Armor     (y = -16, size 32x32: Icona pulita > 5m, Timer <= 5m, OFF rosso)
│
├── Ala Destra (Colonna Supporto Raid - x = +160, 33px di spazio dalla Castbar)
│   └── 04 - Focus Magic      (y = -7, size 34x34: Timer attivo o OFF grigio se non assegnato)
│
├── Fila Utility Inferiore (y = -54, 10px sotto la Mana Bar)
│   ├── 05 - Trinket 1 (x = -60, size 28x28: Glow attivo + Conto alla rovescia ICD riproc)
│   ├── 05 - Trinket 2 (x = -20, size 28x28: Glow attivo + Conto alla rovescia ICD riproc)
│   ├── 06 - Cloak     (x = +20, size 28x28: Glow attivo + Conto alla rovescia ICD riproc)
│   └── 06 - Mana Gem  (x = +60, size 28x28: Cooldown al centro + Cariche in alto a destra)
│
├── Cluster Centrale
│   ├── 08 - Castbar  (y =   0, w = 220, h = 20: Testo spell a sx, tempo a dx, no icona)
│   ├── 09 - GCD      (y = -12, w = 220, h =  3: Barra bianca sottile)
│   └── 07 - Mana Bar (y = -23, w = 220, h = 14: Solo % con 2 decimali, es. 85.24%)
│
└── 10 - Alerts (y = +105, 24px sopra i Proc)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!")
```

---

## Controllo Versione (Git)

Il progetto è versionato con Git ed è sincronizzato sulla repository remota privata di GitHub:
- **Repository Remota**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
