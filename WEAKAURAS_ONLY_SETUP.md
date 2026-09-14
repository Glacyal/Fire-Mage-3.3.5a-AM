# Fire Mage 3.3.5a AM — Configurazione e Gestione WeakAuras (`/wa`)

## Struttura Attuale della Suite

```text
Fire Mage 3.3.5a AM (Gruppo Master - Scale = 1.2, yOffset = -190)
│
├── 01 - Procs (Dynamic Group orizzontale, y = +52 - centrato sopra la Castbar)
│   ├── Hot Streak (Icona 34x34 + Timer rosso <= 3s + Pixel Glow dorato)
│   ├── Clearcasting (Icona 34x34 + Timer rosso <= 4s + Pixel Glow dorato)
│   ├── Living Bomb (Icona 34x34 + Timer rosso <= 3s per refresh senza clippare)
│   ├── Ignite (Icona 34x34 + Timer rosso <= 1.5s)
│   ├── Scorch (Icona 34x34 + Timer rosso <= 5s)
│   └── Molten Fury (Icona 34x34 attiva con Target HP <= 35%)
│
├── Colonna Buff a Sinistra (3 icone 28x28 in riga orizzontale sopra Stats Panel a y = -14)
│   ├── 03 - Arcane Intellect (x = -210, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   ├── 02 - Molten Armor     (x = -180, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 04 - Focus Magic      (x = -150, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso se non assegnato)
│
├── 12 - Stats Panel (x = -180, y = -54, sotto i 3 buff - Box 88x48 con 4 righe stats real-time)
│   ├── SP:    Fire Spell Power (rosso, include proc/buff/gear in tempo reale)
│   ├── Crit:  Fire Spell Crit (arancione, include Molten Armor + glifo, talenti, Combustion, debuff boss: Scorch/Winter's Chill +5%, Heart of the Crusader/Master Poisoner +3%, supporto 3 cifre es. 110.99%)
│   ├── Haste: Spell Haste (viola, include rating + moltiplicatori Bloodlust/Totem/Moonkin, supporto 3 cifre es. 110.99%)
│   └── Hit:   Spell Hit (giallo, rating + Precision + Draenei + debuff boss: Misery/Faerie Fire +3%, indicatore verde (Cap) a >= 17%)
│
├── Cluster Centrale (Larghezza 264px, impilato verticalmente con Hot Streak Bar)
│   ├── 08 - Castbar         (y =  +8, w = 264, h = 20: Icona spell a sx, nome a sx, tempo a dx)
│   ├── 09 - GCD             (y =  -4, w = 264, h =  3: Barra bianca sottile)
│   ├── 07 - Mana Bar        (y = -15, w = 264, h = 14: % con 2 decimali, rossa se <= 20%)
│   └── 10 - Hot Streak Bar  (y = -25, w = 264, h =  7: Barretta dinamica pulita, no testo)
│       ├── Segmento 1 (sx: 130x5px, 50% 1° critico non-periodico persistente nel tempo)
│       └── Proc Bar   (barra unica: 264x5px, Hot Streak proc countdown 10s con Pixel Glow, reset su Pyroblast)
│
├── Fila Utility Inferiore Dinamica (y = -54, margine di 11.5px sotto la Hot Streak Bar)
│   │
│   ├── Modalità 6 Icone (< 2 Pezzi T8 Equipaggiati - Spaziatura 44px):
│   │   ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   │   ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   │   ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   │   ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer a sud %p + CD 2m + Cariche in alto a dx)
│   │   ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│   │   └── 06 - Mirror Image (x = +110: Glow attivo 30s + Swipe orologio CD 3m)
│   │
│   └── Modalità 7 Icone Ristrette (>= 2 Pezzi T8 Equipaggiati - Spaziatura 38px):
│       ├── 05 - Trinket 1    (x = -114: Glow attivo + Swipe orologio + Countdown ICD riproc)
│       ├── 05 - Trinket 2    (x =  -76: Glow attivo + Swipe orologio + Countdown ICD riproc)
│       ├── 06 - Cloak        (x =  -38: Glow attivo + Swipe orologio + Countdown ICD riproc)
│       ├── 06 - Tier 8       (x =    0: Praxis +350 SP per 15s con Glow dorato + Swipe ICD 30s)
│       ├── 06 - Mana Gem     (x =  +38: T7 2pc Glow dorato + Timer a sud %p + CD 2m + Cariche in alto a dx)
│       ├── 06 - Combustion   (x =  +76: Glow attivo + Stacks x%d + Swipe orologio CD)
│       └── 06 - Mirror Image (x = +114: Glow attivo 30s + Swipe orologio CD 3m)
│
└── 10 - Alerts (y = +105, sopra i Proc)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!")
```

---

## Modalità di Installazione e Aggiornamento

### Metodo A: Aggiornamento Diretto (Update / Upgrade) — Consigliato
1. Apri `IMPORT_STRING.txt` e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
   *(Nota: la stringa della versione precedente è conservata in `IMPORT_STRINGOLD.txt`)*
2. In gioco digita `/wa`, clicca su **Import** e incolla la stringa con `Ctrl+V`.
3. Nella finestra di dialogo di WeakAuras, seleziona **`Update Auras`** (o **`Upgrade`**).
   - WeakAuras aggiornerà tutti i moduli sul posto preservando la gerarchia e le tue personalizzazioni di posizione.
4. Chiudi WeakAuras (`Esc`).

### Metodo B: Reinstallazione Pulita (Reset Completo)
1. In `/wa`, clic destro sul gruppo precedente (`Fire Mage HUD` o `Fire Mage 3.3.5a AM`) $\rightarrow$ seleziona **`Delete children and group`**.
2. Clicca su **Import** $\rightarrow$ incolla con `Ctrl+V` $\rightarrow$ clicca su **`Import Group`**.
3. Chiudi con `Esc`.
