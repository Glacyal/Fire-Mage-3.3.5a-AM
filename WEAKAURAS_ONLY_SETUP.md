# Fire Mage HUD — Configurazione e Gestione WeakAuras (`/wa`)

## Struttura Attuale dell'HUD

```text
Fire Mage HUD (Gruppo Master - Scale = 1.2, yOffset = -190)
│
├── 01 - Procs (Dynamic Group orizzontale, y = +44 - centrato sopra la Castbar)
│   ├── Hot Streak (Icona 34x34 + Timer rosso <= 3s + Pixel Glow dorato)
│   ├── Clearcasting (Icona 34x34 + Timer rosso <= 4s + Pixel Glow dorato)
│   ├── Living Bomb (Icona 34x34 + Timer rosso <= 3s per refresh senza clippare)
│   ├── Ignite (Icona 34x34 + Timer rosso <= 1.5s)
│   ├── Scorch (Icona 34x34 + Timer rosso <= 5s)
│   └── Molten Fury (Icona 34x34 attiva con Target HP <= 35%)
│
├── Colonna Buff a Sinistra (x = -182, 34px dalla Castbar - 3 icone 32x32 impilate verticalmente)
│   ├── 03 - Arcane Intellect (y = +18: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   ├── 02 - Molten Armor     (y = -18: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 04 - Focus Magic      (y = -54: Nascosta > 5m, Timer <= 5m, OFF rosso se non assegnato)
│
├── Cluster Centrale (Allungato del +20% a larghezza 264px, impilato verticalmente)
│   ├── 08 - Castbar  (y =   0, w = 264, h = 20: Icona spell a sx, nome a sx, tempo a dx)
│   ├── 09 - GCD      (y = -12, w = 264, h =  3: Barra bianca sottile)
│   └── 07 - Mana Bar (y = -23, w = 264, h = 14: % con 2 decimali, rossa se <= 20%)
│
├── Fila Utility Inferiore (y = -54, 10px sotto la Mana Bar - 6 icone 28x28 centrate)
│   ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Combustion   (x =  +22: Glow attivo + Stacks x%d + Swipe orologio CD)
│   ├── 06 - Mirror Image (x =  +66: Glow attivo 30s + Swipe orologio CD 3m)
│   └── 06 - Mana Gem     (x = +110: Cooldown al centro + Cariche in basso a destra)
│
└── 10 - Alerts (y = +105, 24px sopra i Proc)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!")
```

---

## Modalità di Installazione e Aggiornamento

### Metodo A: Aggiornamento Diretto (Update / Upgrade) — Consigliato
1. Apri `IMPORT_STRING.txt` e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
2. In gioco digita `/wa`, clicca su **Import** e incolla la stringa con `Ctrl+V`.
3. Nella finestra di dialogo di WeakAuras, seleziona **`Update Auras`** (o **`Upgrade`**).
   - WeakAuras aggiornerà tutti i moduli sul posto preservando la gerarchia e le tue personalizzazioni di posizione.
4. Chiudi WeakAuras (`Esc`).

### Metodo B: Reinstallazione Pulita (Reset Completo)
1. In `/wa`, clic destro su **`Fire Mage HUD`** $\rightarrow$ seleziona **`Delete children and group`**.
2. Clicca su **Import** $\rightarrow$ incolla con `Ctrl+V` $\rightarrow$ clicca su **`Import Group`**.
3. Chiudi con `Esc`.
