# Fire Mage HUD 3.3.5a — WeakAuras 4.0.0 Suite

Suite WeakAura modulare, professionale e completa per **Mago Fire Livello 80** per World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

> [!IMPORTANT]
> **REGOLE CRUCIALI PER L'IMPORTAZIONE IN WEAKAURAS**:
> In WeakAuras, se importi un gruppo con lo stesso nome senza prima aver cancellato quello vecchio, WeakAuras **fonde (merge)** i moduli invece di sovrascriverli!
> **Procedura obbligatoria**: In `/wa`, fai clic destro su **`Fire Mage HUD`** $\rightarrow$ seleziona **`Delete children and group`** $\rightarrow$ solo DOPO incolla la nuova stringa da `IMPORT_STRING.txt`.

---

## Novità di Questo Aggiornamento

1. **Entrambi i Trinket Funzionanti (Slot 13 e 14) & Animazione a Orologio (Radial Clock Swipe)**:
   - **Supporto Totale per Entrambi i Trinket**: Risolto il mancato proc sul secondo trinket (es. *The Dying Curse* su Slot 13 e *Sundial of the Exiled* su Slot 14). Riconoscimento garantito al 100% indipendente da maiuscole/minuscole, punteggiatura o spell ID.
   - **Caricamento Stile Orologio Blizzard (Swipe Radiale)**: Abilitato nativamente (`cooldown: true`, `cooldownSwipe: true`) su tutti i moduli: sia durante la durata del proc attivo sia durante il countdown dell'ICD (Internal Cooldown), l'icona mostra l'animazione rotatoria a orologio oltre ai secondi rimanenti.
   - **Tracciamento Indipendente**: Slot 13, Slot 14 e Mantello (Slot 15) hanno timer e cooldown interni separati che non interferiscono tra loro anche in caso di procs simultanei.

2. **Combustion Attiva-Only con Numero di Stack all'Interno dell'Icona**:
   - **Visibile Solo se Attiva**: Quando Combustion è pronta o in cooldown, l'icona è **completamente nascosta** per non occupare spazio.
   - **Numero di Stack Centrato**: Non appena viene attivata, compare nel gruppo dinamico dei Proc mostrando al centro dell'icona il numero di cariche/stack rimanenti (`3`, `2`, `1`) a caratteri grandi (dimensione 18) con **Pixel Glow dorato animato**. Al consumo dell'ultima carica, scompare all'istante.

3. **Molten Armor e Arcane Intellect Nascosti se > 5 Minuti**:
   - **Nessun Ingombro Visivo**: Se Molten Armor o Intellect (*Arcane Intellect*, *Arcane Brilliance*, *Dalaran Brilliance*, ecc.) hanno più di 5 minuti di durata residua, le icone rimangono **completamente nascoste**.
   - **Comparsa Automatica <= 5 Minuti**: Appaiono solo quando mancano 5 minuti o meno alla scadenza, mostrando il timer preciso di countdown (`4:30`, `45s`) e l'animazione a orologio.
   - **Allerta OFF**: Se il buff scade o manca del tutto, compare l'icona desaturata con la scritta rossa **`OFF`**.

4. **Tracciamento Debuff Scorch / Improved Scorch**:
   - Integrato nel gruppo dinamico `01 - Procs` con icona, swipe circolare e secondi residui.
   - Allerta colorazione rossa quando il debuff scende sotto i 5 secondi.

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
│   ├── Combustion (Icona 34x34 attiva-only + Stacks centrati grandezza 18 + Glow dorato)
│   └── Molten Fury (Icona 34x34 attiva con Target HP <= 35%)
│
├── Ala Sinistra (Colonna Utility Personali - x = -160, 34px di spazio dalla Castbar)
│   ├── 03 - Arcane Intellect (y = +22, size 32x32: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 02 - Molten Armor     (y = -16, size 32x32: Nascosta > 5m, Timer <= 5m, OFF rosso)
│
├── Ala Destra (Colonna Supporto Raid - x = +160, 33px di spazio dalla Castbar)
│   └── 04 - Focus Magic      (y = -7, size 34x34: Timer attivo o OFF grigio se non assegnato)
│
├── Fila Utility Inferiore (y = -54, 10px sotto la Mana Bar)
│   ├── 05 - Trinket 1 (x = -60, size 28x28: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 05 - Trinket 2 (x = -20, size 28x28: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Cloak     (x = +20, size 28x28: Glow attivo + Swipe orologio + Countdown ICD riproc)
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
