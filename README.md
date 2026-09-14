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

### 4. Gestione Dinamica Tier 8 & Tier 10 (Praxis & Frostforged Sage / Pushing the Limit)
- **Auto-Rilevamento Intelligente Equipaggiamento Multi-Stadio**:
  - Scansiona automaticamente i 10 Item ID dei pezzi Tier 8 Kirin Tor (10m/25m) e i 15 Item ID dei pezzi Tier 10 Bloodmage (251 Normal, 264 Sanctified, 277 Heroic), con fallback su scansione tooltip e controllo buff attivo.
- **Le 4 Configurazioni Dinamiche della Fila Utility (`y = -54`)**:
  - **Scenario A: T8 (2P) + T10 (2P) Equipaggiati Contemporaneamente [8 Icone Compattate]**:
    - Gli 8 componenti si compattano ergonomicamente a **26x26 px** con passo di **~33px** occupando esattamente 256px sotto la barra centrale da 264px.
    - Ordine: `Trinket 1 (-115) | Trinket 2 (-82) | Mantello (-49) | T8 Praxis (-16) | Gemma Mana (+16) | T10 Frostforged (+49) | Combustion (+82) | Mirror Image (+115)`.
    - Il **T8 Praxis** si posiziona a sinistra della Gemma; il **T10 Frostforged** si posiziona a destra della Gemma.
  - **Scenario B: Solo Tier 8 (2P) Equipaggiato [7 Icone]**:
    - Icone a **28x28 px**, passo **38px** (larghezza totale 256px).
    - Il T10 è completamente nascosto. Il T8 siede al centro esatto a `x = 0`, tra Mantello e Gemma.
    - Ordine: `Trinket 1 (-114) | Trinket 2 (-76) | Mantello (-38) | T8 Praxis (0) | Gemma Mana (+38) | Combustion (+76) | Mirror Image (+114)`.
  - **Scenario C: Solo Tier 10 (2P) Equipaggiato [7 Icone]**:
    - Icone a **28x28 px**, passo **38px** (larghezza totale 256px).
    - Il T8 è completamente nascosto. La Gemma di Mana siede al centro a `x = 0` e il T10 si trova immediatamente a destra a `x = +38`.
    - Ordine: `Trinket 1 (-114) | Trinket 2 (-76) | Mantello (-38) | Gemma Mana (0) | T10 Frostforged (+38) | Combustion (+76) | Mirror Image (+114)`.
  - **Scenario D: Né Tier 8 né Tier 10 Equipaggiati [6 Icone Standard]**:
    - Configurazione simmetrica classica per chi gioca con solo Tier 7 o equipaggiamento misto.
    - Icone a **28x28 px**, passo **44px** (larghezza totale 248px). Entrambi i moduli T8 e T10 restano nascosti.
    - Ordine: `Trinket 1 (-110) | Trinket 2 (-66) | Mantello (-22) | Gemma Mana (+22) | Combustion (+66) | Mirror Image (+110)`.
- **Meccanica Completa Proc & Glow**:
  - **Tier 8 (Praxis - Spell ID 64868)**: +350 Spell Power per 15s con Pixel Glow dorato (`|cFFFFFF00%.1fs|r`), seguito da ricarica ICD radiale di 30s.
  - **Tier 10 (Pushing the Limit - Spell ID 70753 / Frostforged Sage - Spell ID 72416)**: +12% Haste per 5s o +285 SP per 10s con Pixel Glow ciano/ghiaccio (`|cFFFFFF00%.1fs|r`) e swipe a orologio in tempo reale.

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
│   ├── SCENARIO A: 8 ICONE COMPATTATE (Entrambi T8 >= 2P e T10 >= 2P - 26x26px, passo ~33px):
│   │   ├── 05 - Trinket 1    (x = -115: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 05 - Trinket 2    (x =  -82: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Cloak        (x =  -49: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Tier 8       (x =  -16: Praxis +350 SP 15s con Glow dorato + Swipe ICD)
│   │   ├── 06 - Mana Gem     (x =  +16: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│   │   ├── 06 - Tier 10      (x =  +49: Frostforged Sage / Haste 12% con Glow ciano)
│   │   ├── 06 - Combustion   (x =  +82: Glow attivo + Stacks x%d + Swipe orologio CD)
│   │   └── 06 - Mirror Image (x = +115: Glow attivo 30s + Swipe orologio CD 3m)
│   │
│   ├── SCENARIO B: 7 ICONE T8 (Solo T8 >= 2P, T10 < 2P - 28x28px, passo 38px, T10 nascosto):
│   │   ├── 05 - Trinket 1    (x = -114) | 05 - Trinket 2 (x = -76) | 06 - Cloak (x = -38)
│   │   ├── 06 - Tier 8       (x =    0: Centrato tra Mantello e Gemma di Mana)
│   │   └── 06 - Mana Gem     (x =  +38) | 06 - Combustion (x = +76) | 06 - Mirror Image (x = +114)
│   │
│   ├── SCENARIO C: 7 ICONE T10 (Solo T10 >= 2P, T8 < 2P - 28x28px, passo 38px, T8 nascosto):
│   │   ├── 05 - Trinket 1    (x = -114) | 05 - Trinket 2 (x = -76) | 06 - Cloak (x = -38)
│   │   ├── 06 - Mana Gem     (x =    0: Centrata nella riga)
│   │   ├── 06 - Tier 10      (x =  +38: A destra della Gemma di Mana)
│   │   └── 06 - Combustion   (x =  +76) | 06 - Mirror Image (x = +114)
│   │
│   └── SCENARIO D: 6 ICONE STANDARD (Né T8 né T10 - 28x28px, passo 44px, T8 e T10 nascosti):
│       ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│       ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│       └── 06 - Mirror Image (x = +110: Glow attivo 30s + Swipe orologio CD 3m)
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
