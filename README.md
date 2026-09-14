# Fire Mage 3.3.5a AM — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-4.0.0-blue.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![Class](https://img.shields.io/badge/Class-Mage%20(Fire)-red.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Glacyal/FireMageHUD-335)

Suite WeakAura modulare, professionale e ad altissime prestazioni studiata appositamente per **Mago Fuoco Livello 80** per World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).

---

## 🌟 Caratteristiche Principali

### 1. Barra Dinamica Hot Streak (`10 - Hot Streak Bar`)
- **Metà Barretta al 1° Critico (50% a Sinistra)**:
  - Si illumina la metà barretta sinistra (`130x5px`, colore arancione fuoco vivo) al primo colpo critico non-periodico (*Fireball, Fire Blast, Scorch, Dardo di Fuocogelo, Esplosione finale di Living Bomb*) e **resta persistente nel tempo**.
  - I danni periodici da DoT (*Ignite, tick periodici di Living Bomb*) non intaccano la serie.
- **Barra Unica Continua al Proc (264px a Tutta Larghezza)**:
  - Al secondo critico consecutivo (o all'attivazione del buff Hot Streak 48108), la mezza barretta sparisce e **i segmenti si unificano in una singola barra continua da 264px** con **Pixel Glow** dorato/arancione e **conto alla rovescia swipe di 10 secondi**!
- **Consumo Istantaneo su Pyroblast**:
  - Al lancio di Pyroblast (o alla scadenza dei 10s), la barra si azzera istantaneamente tornando alla sola cornice scura di fondo.
- **Risoluzione Combat Log WotLK 3.3.5a**:
  - Frame nativo WoW registrato direttamente agli eventi C++, con parsing multi-offset compatibile con tutti i core emulatore (*TrinityCore, AzerothCore, Mangos*).
- **Zero Testo**: Design puramente visivo, pulito e minimale.

### 2. Filosofia "Zero Clutter" sui Buff Lunghi (*Molten Armor, Intellect, Focus Magic*)
- **Invisibili se > 5 Minuti**: Fintanto che i buff hanno più di 5 minuti residui, restano completamente nascosti per la massima pulizia dello schermo durante i boss fight e in raid.
- **Conto alla Rovescia a Orologio ($\le$ 5 Minuti)**: Appena scendono sotto i 5 minuti (300 secondi), appaiono automaticamente con animazione swipe circolare a orologio e conto alla rovescia (*giallo > 60s, rosso $\le$ 60s*) per preparare il rinnovo.
- **Allerta OFF se Assenti/Scaduti**: Se un buff manca o scade, compare l'icona desaturata grigia con avviso rosso **`OFF`**.
- **Tracking Intelligente Focus Magic**: Riconosce automaticamente il buff assegnato all'alleato scansionando il raid. Quando il Mago riceve il proc da critico di 10s dall'alleato, il sistema estende la durata del buff alleato a 30 minuti, prevenendo allarmi prematuri senza dover ritarghettare l'alleato.

### 3. Pannello Statistiche in Tempo Reale (`12 - Stats Panel`)
Collocato a sinistra sotto i tre buff (`x = -180, y = -54`), monitora in tempo reale le 4 statistiche fondamentali del Mago Fuoco:
- **SP (Spell Power)**: Danno magico per la scuola Fuoco, comprensivo di gear, proc, buff, gemme e pozioni.
- **Crit (Spell Crit %)**: Probabilità di colpo critico Fuoco con Molten Armor, talenti, stack di Combustion (+10% a carica) e debuff boss (+5% *Improved Scorch/Winter's Chill*, +3% *Heart of the Crusader/Master Poisoner*). Supporta valori superiori al 100% (es. `102.50%`).
- **Haste (Spell Haste %)**: Celerità magica in tempo reale con rating e moltiplicatori raid (*Bloodlust/Heroism +30%, Wrath of Air Totem +5%, Moonkin/Retri Aura +3%*).
- **Hit (Spell Hit %)**: Indice di precisione magica con rating, talento Precision (+3%), razziale Draenei (+1%) e debuff boss (*Misery / Faerie Fire +3%*). Mostra l'indicatore verde **`(Cap)`** al raggiungimento del 17% (o 14% con debuff).

### 4. Gestione Dinamica Tier 8 (Bonus 2 Pezzi `06 - Tier 8` — Praxis)
- **Auto-Rilevamento Intelligente Equipaggiamento**:
  - Scansiona automaticamente i 10 Item ID dei pezzi Tier 8 Kirin Tor (Elmo, Spalle, Torso, Guanti, Gambe in versione 10m e 25m) ad ogni cambio di equipaggiamento (`PLAYER_EQUIPMENT_CHANGED`).
- **Modalità 6 Icone (Solo T7 o Solo T10, oppure < 2 Pezzi T8)**:
  - L'icona T8 resta completamente nascosta.
  - La fila utility mantiene la spaziatura classica da 44px tra i centri (`x = [-110, -66, -22, +22, +66, +110]`), perfetta per chi gioca con bonus T7 o T10.
- **Modalità 7 Icone Ristrette ($\ge 2$ Pezzi T8 Equipaggiati)**:
  - Viene inserita l'icona del Tier 8 (`Spell_Arcane_StudentOfMagic`) al centro esatto della riga utility (`x = 0, y = -54`, tra Mantello e Gemma).
  - Gli altri moduli si stringono dinamicamente con spaziatura da 38px (`x = [-114, -76, -38, 0, +38, +76, +114]`), occupando una larghezza totale di 256px perfettamente simmetrica e allineata sotto la barra da 264px!
- **Meccanica Completa Proc & ICD**:
  - **Buff Attivo Praxis (Spell ID 64868)**: +350 Spell Power per 15s con **Pixel Glow** dorato e countdown decimale in giallo (`|cFFFFFF00%.1fs|r`).
  - **Cooldown ICD (45 secondi totali)**: Al termine dei 15s di buff, l'icona spegne il glow e avvia la ricarica radiale a orologio (*swipe*) con countdown numerico per i restanti 30 secondi prima del riproc.
  - **Pronto**: Ritorno immediato all'icona pulita pronta al nuovo proc.

### 5. Engine Universale per Monili & Mantello (Slot 13, 14 e 15)
- **Database con oltre 40 Monili WotLK**: Riconoscimento automatico di oggetti On-Use e proc passivi con Internal Cooldown (ICD, es. 45s per *Dislodged Foreign Object / Charred Twilight Scale*, 90s per *Phylactery of the Nameless Lich*).
- **Animazione a Orologio Blizzard (Radial Clock Swipe)**: Mostra il **Pixel Glow** dorato durante la durata attiva del buff, commutando poi sullo swipe a orologio e countdown del tempo residuo prima del prossimo riproc.
- **Fallback Euristico Intelligente**: Se equipaggi un trinket non presente nel database, il modulo scansiona automaticamente le descrizioni per stimare l'effetto e applicare un timer affidabile.

### 6. Gemma del Mana con Bonus 2 Pezzi T7 (`06 - Mana Gem`)
- **Commutazione Dinamica Icona**: All'uso della gemma, attiva il bonus 2 pezzi T7 (+225 Spell Power per 15s) commutando l'icona sul simbolo di **Mana Surge** (`Spell_Arcane_ManaSurge`), evidenziata dal Pixel Glow dorato e dal countdown decimale a sud (`%.1fs`).
- **Ritorno a Cooldown Oggetto**: Al termine del buff, torna all'icona della gemma e visualizza il cooldown dell'oggetto (2 min).
- **Conteggio Cariche**: Mostra le cariche residue in alto a destra (`%c`, con "0" rosso se esaurite o gemma mancante).

### 7. Cluster Centrale Ergonomico (Larghezza 264px)
- **Castbar con Icona Spell** (`264x20px`, `y = +8`): Icona della magia in lancio a sinistra, nome spell a sinistra, tempo residuo a destra, gradiente ciano Blizzard.
- **Barra GCD** (`264x3px`, `y = -4`): Barra bianca sottile per il Global Cooldown (spell 61304).
- **Barra del Mana Dinamica** (`264x14px`, `y = -15`): Visualizza solo la percentuale con 2 decimali (es. `85.24%`) e diventa automaticamente **Rossa** quando scende a $\le 20\%$.

### 8. Gruppo Procs & Debuff con Timer Rossi in Scadenza (`01 - Procs`)
- Posizionato orizzontalmente sopra la Castbar a `y = +52`.
- I timer commutano in **rosso vivo** con precisione decimale negli ultimi secondi di durata:
  - **Hot Streak**: Rosso sotto i 3s (`<= 3s`).
  - **Clearcasting**: Rosso sotto i 4s (`<= 4s`).
  - **Living Bomb**: Rosso sotto i 3s (`<= 3s`) prima dell'esplosione, per preparare il refresh immediato.
  - **Ignite**: Rosso sotto 1.5s (`<= 1.5s`).
  - **Scorch / Improved Scorch**: Rosso sotto i 5s (`<= 5s`).
  - **Molten Fury**: Icona attiva con Target HP $\le 35\%$.

---

## 📐 Layout e Coordinate dell'HUD

```text
Fire Mage 3.3.5a AM (Gruppo Master - Scale: 1.2, xOffset: 0, yOffset: -190)
│
├── 01 - Procs (Dynamic Group orizzontale a y = +52 - Auto-centrato sopra la Castbar)
│   ├── Hot Streak (Icona 34x34 + Timer rosso <= 3s + Pixel Glow dorato)
│   ├── Clearcasting (Icona 34x34 + Timer rosso <= 4s + Pixel Glow dorato)
│   ├── Living Bomb (Icona 34x34 debuff su target + Timer rosso <= 3s prima dell'esplosione)
│   ├── Ignite (Icona 34x34 debuff su target + Timer rosso <= 1.5s)
│   ├── Scorch (Icona 34x34 debuff Scorch/Improved Scorch su target + Timer rosso <= 5s)
│   └── Molten Fury (Icona 34x34 attiva con salute target <= 35%)
│
├── Colonna Buff a Sinistra (3 icone 28x28 allineate sopra Stats Panel a y = -14)
│   ├── 03 - Arcane Intellect (x = -210, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   ├── 02 - Molten Armor     (x = -180, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 04 - Focus Magic      (x = -150, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso se non assegnato)
│
├── 12 - Stats Panel (x = -180, y = -54, sotto i 3 buff - Box 88x48 con 4 righe real-time)
│   ├── SP:    Fire Spell Power (rosso vivo, include proc/buff/gear in tempo reale)
│   ├── Crit:  Fire Spell Crit (arancione, include Molten Armor, talenti, Combustion, debuff boss)
│   ├── Haste: Spell Haste (viola, include rating e moltiplicatori raid)
│   └── Hit:   Spell Hit (giallo, rating + talenti + Draenei + debuff boss con indicatore Cap a >= 17%)
│
├── Cluster Centrale (Larghezza 264px, impilato verticalmente)
│   ├── 08 - Castbar         (y =  +8, w = 264, h = 20: Icona a sx, nome spell a sx, tempo a dx)
│   ├── 09 - GCD             (y =  -4, w = 264, h =  3: Barra bianca sottile per GCD)
│   ├── 07 - Mana Bar        (y = -15, w = 264, h = 14: Solo % con 2 decimali, rossa se <= 20%)
│   └── 10 - Hot Streak Bar  (y = -25, w = 264, h =  7: Barretta dinamica pulita, no testo)
│       ├── Hot Streak Bar - Background (texture: cornice scura 264x7px)
│       ├── Hot Streak Bar - Segment 1  (texture: 130x5px a sx, 50% 1° critico persistente)
│       └── Hot Streak Bar - Proc       (aurabar: 264x5px unificata, countdown 10s con Pixel Glow)
│
├── Fila Utility Inferiore Dinamica (y = -54, margine di 11.5px sotto la Hot Streak Bar)
│   │
│   ├── MODALITÀ 6 ICONE (Solo T7 o Solo T10, oppure < 2 pezzi T8 - Spaziatura 44px):
│   │   ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│   │   ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│   │   └── 06 - Mirror Image (x = +110: Glow attivo 30s + Swipe orologio CD 3m)
│   │
│   └── MODALITÀ 7 ICONE RISTRETTE (con >= 2 pezzi T8 equipaggiati - Spaziatura 38px):
│       ├── 05 - Trinket 1    (x = -114: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 05 - Trinket 2    (x =  -76: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Cloak        (x =  -38: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Tier 8       (x =    0: Praxis +350 SP 15s con Glow + Swipe ICD 30s)
│       ├── 06 - Mana Gem     (x =  +38: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│       ├── 06 - Combustion   (x =  +76: Glow attivo + Stacks x%d + Swipe orologio CD)
│       └── 06 - Mirror Image (x = +114: Glow attivo 30s + Swipe orologio CD 3m)
│
└── 10 - Alerts (y = +105, sopra i Procs)
    └── Alert - Hot Streak (text: alert "HOT STREAK! / PYROBLAST READY!" font expressway)
```

---

## 🚀 Installazione & Aggiornamento in Gioco

### Opzione A: Aggiornamento Diretto (Update / Upgrade) — Consigliato
1. Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRING.txt)** e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
   *(Nota: la stringa precedente è archiviata come backup di sicurezza in [`IMPORT_STRINGOLD.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRINGOLD.txt))*
2. In World of Warcraft, apri WeakAuras digitando `/wa`.
3. Clicca su **Import** in alto a sinistra e incolla con `Ctrl+V`.
4. Seleziona **`Update Auras`** (o **`Upgrade`**).
5. Chiudi WeakAuras (`Esc`). L'HUD è aggiornato a **Fire Mage 3.3.5a AM**!

### Opzione B: Reinstallazione Pulita (Clean Reset)
Se provieni da una versione precedente e desideri ripristinare coordinate e layout originali:
1. In `/wa`, fai clic destro sul gruppo precedente (`Fire Mage HUD` o `Fire Mage 3.3.5a AM`) e seleziona **`Delete children and group`**.
2. Clicca su **Import** in alto a sinistra.
3. Incolla il testo da `IMPORT_STRING.txt` con `Ctrl+V`.
4. Clicca su **`Import Group`** (o **`Replace`**).
5. Chiudi WeakAuras (`Esc`). Fatto!

---

## 🛠️ Compilazione e Test

La suite include strumenti dedicati per la generazione della stringa e la validazione del codice:

```bash
# Rigenera la stringa compressa WA4 (!WA:1!) in IMPORT_STRING.txt
python generate_import_string.py

# Esegui la suite di test sulla logica e sul simulatore Hot Streak
python scratch/test_hotstreak_logic.py

# Valida la sintassi Lua di tutti i moduli dell'addon e delle auras
python scratch/test_lua.py
```

---

## 📜 Repository & Licenza

- **Repository Ufficiale**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
- Distribuito sotto licenza **MIT**.
