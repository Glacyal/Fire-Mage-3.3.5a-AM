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

6. **Mirror Image (Copie)**:
   - Integrata nella fila utility tra Combustion e Mana Gem (`x = +54, y = -54`) con durata attiva 30s (glow dorato e countdown) e cooldown swipe di 3m.

7. **Condizione di Caricamento (Load Tab)**:
   - Configurato nativamente su **Player Class: Mage** e **Talent: Living Bomb** su tutto l'albero di auras e su ogni singolo elemento, garantendo che l'HUD si carichi esclusivamente per maghi con talento Bomba Vivente (Fire).

8. **Barre Centrali Allungate (+20%) e Buff Impilati a Sinistra**:
   - **Larghezza Barre a 264px**: Castbar, GCD e Mana Bar allungate del 20% (da 220px a 264px) e perfettamente impilate una sotto l'altra.
   - **Colonna Buff a Sinistra ("Uno sotto l'altro")**: *Arcane Intellect*, *Molten Armor* e *Focus Magic* sono posizionati verticalmente a sinistra (`x = -182`) mantenendo uno spazio pulito di 34px dalla barra.
   - **Fila Utility Adattata**: I 6 moduli (Trinket 1, Trinket 2, Mantello, Combustione, Copie, Gemma) sono distribuiti e centrati armoniosamente sotto la barra allungata.

9. **Castbar con Icona Spell e Mana Bar Dinamica (Rosso <= 20%)**:
   - **Castbar con Icona a Sinistra**: Visualizza l'icona della magia in corso di lancio (cast o channel come Blizzard/Evocation) sul bordo sinistro della barra, con nome spell a sinistra, tempo rimanente a destra (`5.5`) e gradiente azzurro/ciano Blizzard.
   - **Allerta Mana <= 20%**: La barra del mana diventa automaticamente **Rossa** quando scende a $\le 20\%$, mentre rimane del colore blu abituale tra il 20% e il 100%.

10. **Timer Procs con Allerta Rossa in Scadenza (Simile a Scorch)**:
    - Tutti i proc e debuff del gruppo `01 - Procs` ora condividono lo stesso comportamento di Scorch:
      - **Hot Streak**: Quando scende sotto i 3s (`<= 3s`), il timer diventa **rosso acceso** con decimali (`|cFFFF4444%.1fs|r`), altrimenti bianco intero (`%.0fs`).
      - **Clearcasting / Lancio Limpido**: Quando scende sotto i 4s (`<= 4s`), il timer diventa **rosso** con decimali, altrimenti bianco intero.
      - **Living Bomb**: Quando mancano 3s (`<= 3s`) all'esplosione, il conto alla rovescia diventa **rosso** con decimali per preparare il refresh immediato post-esplosione senza clippare.
      - **Ignite**: Quando scende sotto 1.5s (`<= 1.5s`), il timer diventa **rosso** con decimali per avvertire che sta per cadere il debuff.
11. **Smart Living Bomb Interactive Bar Tracker (Modulo 11 - Lato Destro)**:
    - **Indicatori [V] e [X]**:
      - `[V]` (Verde): Bersaglio con Living Bomb già attiva. La barra arancione a tema fuoco scorre continuamente indicando il conto alla rovescia continuo dei 12 secondi (`12.0s -> 0.0s`), con secondi decimali a destra (diventa rosso a `<= 3.0s` prima dell'esplosione).
      - `[X]` (Rosso): Bersaglio privo di Living Bomb. La barra visualizza graficamente la percentuale di salute (HP %) colorata in base alla fascia di priorità:
        - **Priorità 1 - HP Medi (40-70%)**: Verde brillante (Target ottimale per sfruttare i 12s e l'esplosione). Il #1 è contrassegnato con `!`.
        - **Priorità 2 - HP Alti (70-100%)**: Ciano/Azzurro.
        - **Priorità 3 - HP Bassi (0-40%)**: Rosso (Rischio morte anticipata).
    - **Click-to-Target Cliccabile**:
      - Ogni barra è agganciata a un `SecureActionButtonTemplate`. Fuori dal combat, cliccare su una barra seleziona istantaneamente il bersaglio esatto (`/targetexact`).
      - In combat, protetto da `InCombatLockdown()` per azzerare qualsiasi rischio di blocco UI o taint.
    - **Zero Automazione**: Nessun cast o cambio target forzato; supporto decisionale al 100% manuale.

---

## Modalità di Installazione e Aggiornamento in Gioco

In WeakAuras sono disponibili due modalità per installare o aggiornare l'HUD:

### Metodo A: Aggiornamento Diretto (Update / Upgrade) — Più Veloce
1. Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRING.txt)** e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
2. In World of Warcraft, apri WeakAuras digitando `/wa`.
3. Clicca su **Import** in alto a sinistra e incolla la stringa con `Ctrl+V`.
4. Nella schermata di importazione di WeakAuras, seleziona **`Update Auras`** (o **`Upgrade`**).
   - WeakAuras riconoscerà gli identificatori (UID) esistenti e aggiornerà direttamente l'HUD sul posto, mantenendo le tue posizioni a schermo!
5. Chiudi WeakAuras (`Esc`). Fatto!

### Metodo B: Reinstallazione Pulita (Reset Completo) — Consigliato se hai vecchie versioni o duplicati
Se provieni da una configurazione modificata o vuoi ripristinare coordinate e layout originali al 100%:
1. In `/wa`, fai clic destro su **`Fire Mage HUD`** e seleziona **`Delete children and group`**.
2. Clicca su **Import** in alto a sinistra.
3. Incolla la stringa da `IMPORT_STRING.txt` con `Ctrl+V`.
4. Clicca su **`Import Group`**.
5. Chiudi WeakAuras (`Esc`). Fatto!

---

## Struttura e Coordinate dell'HUD

```text
Fire Mage HUD (Gruppo Master - Scale = 1.2, yOffset = -190, posizionato sopra le barre)
│
├── 01 - Procs (Dynamic Group orizzontale, y = +52 - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona 34x34 + Timer rosso <= 3s + Glow Pixel dorato)
│   ├── Clearcasting (Icona 34x34 + Timer rosso <= 4s + Glow Pixel dorato)
│   ├── Living Bomb (Icona 34x34 + Timer rosso <= 3s per refresh post-boom)
│   ├── Ignite (Icona 34x34 + Timer rosso <= 1.5s)
│   ├── Scorch (Icona 34x34 Scorch/Improved Scorch + Timer rosso <= 5s)
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
│   ├── 08 - Castbar         (y =  +8, w = 264, h = 20: Testo spell a sx, tempo a dx, icona a sx)
│   ├── 09 - GCD             (y =  -4, w = 264, h =  3: Barra bianca sottile)
│   ├── 07 - Mana Bar        (y = -15, w = 264, h = 14: Solo % con 2 decimali, es. 85.24%)
│   └── 10 - Hot Streak Bar  (y = -25, w = 264, h =  7: Barretta dual-segment pulita, no testo)
│       ├── Segmento 1 (sx: 130x5px, 1° critico non-periodico persistente nel tempo)
│       └── Segmento 2 (dx: 130x5px, Hot Streak proc countdown 10s con glow, reset istantaneo su Pyroblast)
│
├── Fila Utility Inferiore (y = -54, margine di 11.5px sotto la Hot Streak Bar - 6 icone 28x28)
│   ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer a sud %p + CD 2m + Cariche in alto a dx)
│   ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│   └── 06 - Mirror Image (x = +110: Glow attivo 30s + Swipe orologio CD 3m)
│
└── 10 - Alerts (y = +105, sopra i Proc)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!")
```

---

## Controllo Versione (Git)

Il progetto è versionato con Git ed è sincronizzato sulla repository remota di GitHub:
- **Repository Remota**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
