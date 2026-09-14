# Fire Mage HUD 3.3.5a — WeakAuras 4.0.0 Suite

Suite WeakAura modulare, professionale e completa per **Mago Fire Livello 80** per World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

> [!IMPORTANT]
> **REGOLE CRUCIALI PER L'IMPORTAZIONE IN WEAKAURAS**:
> In WeakAuras, se importi un gruppo con lo stesso nome senza prima aver cancellato quello vecchio, WeakAuras **fonde (merge)** i moduli invece di sovrascriverli!
> **Procedura obbligatoria**: In `/wa`, fai clic destro su **`Fire Mage HUD`** $\rightarrow$ seleziona **`Delete children and group`** $\rightarrow$ solo DOPO incolla la nuova stringa da `IMPORT_STRING.txt`.

---

## Novità di Questo Aggiornamento

1. **Combustion nella Fila Utility a Sinistra della Mana Gem**:
   - **Posizione**: Collocata a sinistra di Mana Gem (`x = +36, y = -54`), perfettamente allineata nella fila inferiore.
   - **Comportamento identico a Trinket e Mantello**:
     - **READY**: Icona visibile a colori pieni, pronta al cast, senza scritte.
     - **ATTIVA**: Pixel Glow dorato animato brillante, contatore di cariche/stack all'interno dell'icona (`x%d`).
     - **IN COOLDOWN**: Animazione a orologio (radial clock swipe Blizzard) con conto alla rovescia del CD in tempo reale (`m:ss` o secondi).
     - **DI NUOVO PRONTA**: Lo swipe si completa, il glow si spegne e l'icona torna pulita.

2. **Tutti i Buff Nascosti se > 5 Minuti (Molten Armor, Intellect e Focus Magic)**:
   - **Invisibili > 5 min**: Quando Molten Armor, Arcane Intellect (*Arcane Brilliance*, *Dalaran Brilliance*, ecc.) o Focus Magic hanno più di 5 minuti residui, sono **completamente nascosti** per pulizia visiva totale durante i boss fight e in raid.
   - **Conto alla Rovescia <= 5 min**: Appena un buff scende sotto i 5 minuti (300 secondi), l'icona appare automaticamente con conto alla rovescia in giallo (`4:59`, `3:20`, `45s`) e animazione swipe a orologio per preparare il refresh.
   - **Allerta OFF se Mancante/Scaduto**: Se il buff non è attivo sul giocatore o è scaduto (o Focus Magic non è assegnato a nessuno), compare l'icona desaturata grigia con avviso rosso **`OFF`**.

3. **Entrambi i Trinket Funzionanti (Slot 13 e 14) & Mantello (Slot 15)**:
   - **Supporto Completo per Entrambi gli Slot**: Monitoraggio affidabile sia su Slot 13 che su Slot 14 con riconoscimento per ID e per nome buff, e slot Mantello (Slot 15).
   - **Caricamento Stile Orologio Blizzard (Swipe Radiale)**: Abilitato nativamente (`cooldownSwipe: true`) sia durante la durata del proc attivo sia durante il countdown dell'ICD (Internal Cooldown per il prossimo riproc).
   - **Pixel Glow Dorato**: Evidenziazione visiva immediata quando il proc si attiva.

4. **Tracciamento Debuff Scorch / Improved Scorch**:
   - Integrato nel gruppo dinamico `01 - Procs` con swipe circolare e secondi residui (con allerta rossa sotto i 5 secondi).

5. **Mana Bar e Scala Generale**:
   - Barra del Mana con visualizzazione percentuale fino alla seconda cifra decimale (es. `85.24%`).
   - Master scale **`1.2`** (+20% di grandezza) con coordinata `yOffset = -190` (sopra le action bar).

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
│   └── Molten Fury (Icona 34x34 attiva con Target HP <= 35%)
│
├── Ala Sinistra (Colonna Buff Personali - x = -160, 34px dalla Castbar)
│   ├── 03 - Arcane Intellect (y = +22, size 32x32: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 02 - Molten Armor     (y = -16, size 32x32: Nascosta > 5m, Timer <= 5m, OFF rosso)
│
├── Ala Destra (Colonna Buff Supporto - x = +160, 33px dalla Castbar)
│   └── 04 - Focus Magic      (y =  -7, size 34x34: Nascosta > 5m, Timer <= 5m, OFF rosso se non assegnato)
│
├── Fila Utility Inferiore (y = -54, 10px sotto la Mana Bar - 5 icone 28x28 centrate)
│   ├── 05 - Trinket 1    (x = -72: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 05 - Trinket 2    (x = -36: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Cloak        (x =   0: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Combustion   (x = +36: Glow attivo + Stacks x%d + Swipe orologio CD)
│   └── 06 - Mana Gem     (x = +72: Cooldown al centro + Cariche in alto a destra)
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

Il progetto è versionato con Git ed è sincronizzato sulla repository remota di GitHub:
- **Repository Remota**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
