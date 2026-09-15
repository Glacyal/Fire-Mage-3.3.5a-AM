# Fire Mage 3.3.5a AM — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-4.0.0-blue.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![Class](https://img.shields.io/badge/Class-Mage%20(Fire)-red.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Glacyal/FireMageHUD-335)

Suite WeakAura modulare, professionale e ad altissime prestazioni studiata appositamente per **Mago Fuoco Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).

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
- **Molten Armor & Arcane Intellect**:
  - **Invisibili se > 5 Minuti**: Fintanto che hanno più di 5 minuti residui, restano completamente nascosti per la massima pulizia dello schermo durante i boss fight e in raid.
  - **Conto alla Rovescia a Orologio ($\le$ 5 Minuti)**: Appena scendono sotto i 5 minuti (300 secondi), appaiono automaticamente con animazione swipe circolare a orologio e conto alla rovescia (*giallo > 60s, rosso $\le$ 60s*) per preparare il rinnovo.
  - **Allerta OFF se Assenti/Scaduti**: Se un buff manca o scade, compare l'icona desaturata grigia con avviso rosso **`OFF`**.
- **Gestione Focus Magic (`04 - Focus Magic`)**:
  - **Nascosto se Applicato**: Fintanto che il Focus Magic è attivo sull'alleato assegnato (e vivo), l'icona rimane **completamente nascosta**, garantendo la massima pulizia visiva dello schermo.
  - **Proc Personale 10s (+3% Crit)**: Quando l'alleato mette a segno un critico e il Mago riceve il proc da 10 secondi (Spell ID 54648), l'icona compare all'istante mostrando il **conto alla rovescia dei 10 secondi** con swipe del cooldown.
  - **Ritorno a Nascosto**: Al termine dei 10 secondi, l'icona torna automaticamente **nascosta** se l'alleato ha ancora il buff attivo.
  - **Allerta OFF se Non Assegnato o Alleato Morto**: Se Focus Magic non è applicato su alcun giocatore, oppure se l'alleato assegnato muore in combattimento o il buff scade, compare immediatamente l'icona desaturata grigia con avviso rosso **`OFF`**.

### 3. Pannello Statistiche in Tempo Reale (`12 - Stats Panel`)
Collocato a sinistra sotto i tre buff (`x = -180, y = -54`), monitora in tempo reale le 4 statistiche fondamentali del Mago Fuoco con gestione rigorosa delle priorità e prevenzione dei conflitti/doppi conteggi:
- **SP (Spell Power)**: Danno magico scuola Fuoco (`GetSpellBonusDamage(3)`), comprensivo di gear, gemme, incantamenti, proc monili, pozioni, Flask, Demonic Pact (Warlock), Totem of Wrath / Flametongue (Shamano), bonus 2P T8 Praxis (+350 SP) e 2P T7 Mana Gem (+225 SP).
- **Crit (Spell Crit %)**: Probabilità di critico Fuoco con Molten Armor (+ glifo spirito), talenti (*Critical Mass, Pyromaniac*), proc Focus Magic (+3%), stack di Combustion (+10% per carica) e debuff boss non cumulabili tra loro:
  - Categoria +5% Spell Crit (max una sola volta): *Improved Scorch* (Mago Fuoco) vs *Winter's Chill* (Mago Gelo) vs *Shadow and Flame* (Stregone).
  - Categoria +3% All Crit (max una sola volta): *Heart of the Crusader* (Paladino) vs *Master Poisoner* (Ladro) vs *Totem of Wrath* (Shamano).
  - Supporta valori superiori a 100% (es. `102.50%`).
- **Haste (Spell Haste %)**: Celerità magica calcolata moltiplicando la percentuale da rating con tutti i moltiplicatori raid attivi:
  - *Bloodlust / Heroism*: `* 1.30` (+30% haste).
  - *Wrath of Air Totem*: `* 1.05` (+5% haste Shamano).
  - *Raid 3% Haste (Anti-conflitto)*: *Swift Retribution* (Paladino) vs *Improved Moonkin Form* (Druido) conteggiato **al massimo una sola volta** (`* 1.03`).
  - *Tier 10 2-Piece (Pushing the Limit)*: `* 1.12` (+12% spell haste per 5s su proc Hot Streak).
  - *Power Infusion*: `* 1.20` (+20% spell haste Sacerdote).
  - *Berserking*: `* 1.20` (+20% haste razziale Troll).
- **Hit (Spell Hit %)**: Indice di precisione magica con rating, talento Precision (+3%), razziale Draenei o aura *Heroic Presence* (+1%) e debuff boss non cumulabile (+3% *Misery* vs *Improved Faerie Fire*). Mostra l'indicatore verde **`(Cap)`** al raggiungimento della soglia del 17.00%.

### 4. Gestione Dinamica Tier 8 & Tier 10
- **Tier 10 2-Piece (Pushing the Limit - Spell ID 70753/70752)**:
  - Collocato nella **riga superiore dei procs (`01 - Procs`)**, compare dinamicamente **immediatamente a sinistra di Hot Streak** (34x34 px).
  - Al proc di Hot Streak, se equipaggiati $\ge 2$ pezzi T10, il buff *Pushing the Limit* (+12% Haste per 5s) si attiva con Pixel Glow dorato/arancione e timer swipe. Al termine scompare senza alterare la riga dei proc.
- **Tier 10 4-Piece (Quad Core - Spell ID 70747)**:
  - Integrato nell'icona **Mirror Image** (`06 - Mirror Image`): al cast delle Copie, mostra il buff +18% danni per 30s con glow e texture dedicata.
- **Tier 8 2-Piece (Praxis - Spell ID 64868)**:
  - Collocato al centro della **fila utility inferiore** a `x = 0, y = -54` (tra Mantello e Gemma di Mana).
  - Mostra il proc +350 Spell Power per 15s con Pixel Glow dorato e swipe dell'ICD stimato di 45s.
- **Le 2 Configurazioni della Fila Utility (`y = -54`, 28x28 px) in base al Gear**:
  - **Layout A: 7 Icone (Con $\ge 2$ pezzi T8 equipaggiati, passo 38px, span 256px)**:
    - `Trinket 1 (-114) | Trinket 2 (-76) | Mantello (-38) | T8 Praxis (0) | Gemma Mana (+38) | Combustion (+76) | Mirror Image (+114)`.
    - Attivo per: **Solo T8**, **T7 misto a T8**, **T8 misto a T10**.
  - **Layout B: 6 Icone Standard (< 2 pezzi T8 equipaggiati, passo 44px, span 248px)**:
    - `Trinket 1 (-110) | Trinket 2 (-66) | Mantello (-22) | Gemma Mana (+22) | Combustion (+66) | Mirror Image (+110)`.
    - Attivo per: **Solo T7**, **Solo T10**, o equipaggiamento generico senza bonus T8.
  - **Rilevamento Dinamico Istantaneo**: Cambio layout immediato ad ogni cambio di equipaggiamento (`PLAYER_EQUIPMENT_CHANGED`, Outfitter, ItemRack, Equipment Manager) a zero latenza.

### 5. Engine Universale per Monili & Mantello (Slot 13, 14 e 15)
- **Database con oltre 40 Monili WotLK**: Riconoscimento automatico di oggetti On-Use e proc passivi con Internal Cooldown (ICD, es. 45s per *Dislodged Foreign Object / Charred Twilight Scale*, 90s per *Phylactery of the Nameless Lich*).
- **Animazione a Orologio Blizzard (Radial Clock Swipe)**: Mostra il **Pixel Glow** dorato durante la durata attiva del buff, commutando poi sullo swipe a orologio e countdown del tempo residuo prima del prossimo riproc.
- **Fallback Euristico Intelligente**: Scansione automatica dei tooltip per stimare gli effetti dei monili non presenti a catalogo.

### 6. Gemma del Mana con Bonus 2 Pezzi T7 (`06 - Mana Gem`)
- **Commutazione Dinamica Icona**: All'uso della gemma con 2P T7 equipaggiato, attiva il bonus (+225 Spell Power per 15s) evidenziato dal Pixel Glow dorato e dal countdown decimale a sud (`%.1fs`).
- **Ritorno a Cooldown Oggetto**: Al termine del buff, torna all'icona della gemma e visualizza il cooldown dell'oggetto (2 min).
- **Conteggio Cariche**: Mostra le cariche residue in alto a destra (`%c`, con "0" rosso se esaurite o gemma mancante).

### 7. Cluster Centrale Ergonomico (Larghezza 264px)
- **Castbar con Icona Spell** (`264x20px`, `y = +8`): Icona spell a sinistra, nome spell a sinistra, tempo residuo a destra.
- **Barra GCD** (`264x3px`, `y = -4`): Barra bianca sottile per il Global Cooldown.
- **Barra del Mana Dinamica** (`264x14px`, `y = -15`): Visualizza la percentuale con 2 decimali (es. `85.24%`) e diventa rossa sotto il 20%.

### 8. Gruppo Procs & Debuff (`01 - Procs`)
- Posizionato orizzontalmente sopra la Castbar a `y = +52`.
- Include: **Tier 10** (*Pushing the Limit* a sinistra di Hot Streak), **Hot Streak**, **Clearcasting**, **Living Bomb** (refresh preventivo sotto 3s), **Ignite**, **Scorch**, **Molten Fury** ($\le 35\%$ HP).

---

## 📐 Layout e Struttura della Suite

```text
Fire Mage 3.3.5a AM (Gruppo Master - Scale: 1.2, xOffset: 0, yOffset: -190)
│
├── 01 - Procs (Dynamic Group orizzontale a y = +52 - centrato sopra la Castbar)
│   ├── Tier 10      (Icona 34x34 a sx di Hot Streak, Pushing the Limit / +12% Haste 5s con Pixel Glow)
│   ├── Hot Streak   (Icona 34x34 + Timer rosso <= 3s + Pixel Glow dorato)
│   ├── Clearcasting (Icona 34x34 + Timer rosso <= 4s + Pixel Glow dorato)
│   ├── Living Bomb  (Icona 34x34 debuff su target + Timer rosso <= 3s prima dell'esplosione)
│   ├── Ignite       (Icona 34x34 debuff su target + Timer rosso <= 1.5s)
│   ├── Scorch       (Icona 34x34 debuff Scorch/Improved Scorch su target + Timer rosso <= 5s)
│   └── Molten Fury  (Icona 34x34 attiva con salute target <= 35%)
│
├── Colonna Buff a Sinistra (3 icone 28x28 allineate sopra Stats Panel a y = -14)
│   ├── 03 - Arcane Intellect (x = -210, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   ├── 02 - Molten Armor     (x = -180, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 04 - Focus Magic      (x = -150, y = -14: Proc 10s con countdown e glow, alleato <= 5m timer, OFF rosso se assente)
│
├── 12 - Stats Panel (x = -180, y = -54, sotto i 3 buff - Box 88x48 con 4 righe real-time)
│   ├── SP:    Fire Spell Power (rosso, include proc/buff/gear/gemme in tempo reale)
│   ├── Crit:  Fire Spell Crit (arancione, Molten Armor + talenti + Combustion + debuff boss anti-conflitto)
│   ├── Haste: Spell Haste (viola, rating + Bloodlust/Totem/3% raid + T10 2P + PI + Berserking)
│   └── Hit:   Spell Hit (giallo, rating + Precision + Draenei + debuff boss con Cap a >= 17%)
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
│   ├── Scenario A: 7 Icone (Equipaggiati >= 2 pezzi T8 - 28x28px, passo 38px, span 256px):
│   │   ├── 05 - Trinket 1    (x = -114: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 05 - Trinket 2    (x =  -76: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Cloak        (x =  -38: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Tier 8       (x =    0: Praxis +350 SP 15s con Glow dorato + Swipe ICD)
│   │   ├── 06 - Mana Gem     (x =  +38: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│   │   ├── 06 - Combustion   (x =  +76: Glow attivo + Stacks x%d + Swipe orologio CD)
│   │   └── 06 - Mirror Image (x = +114: Glow attivo 30s + proc 4P T10 + Swipe CD 3m)
│   │
│   └── Scenario B: 6 Icone Standard (< 2 pezzi T8 - 28x28px, passo 44px, span 248px):
│       ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│       ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│       └── 06 - Mirror Image (x = +110: Glow attivo 30s + proc 4P T10 + Swipe CD 3m)
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

## 🛠️ Validazione e Test

La suite include test deterministici per la verifica di ogni singolo componente:

```bash
# Rigenera la stringa compressa WA4 (!WA:1!) in IMPORT_STRING.txt
python generate_import_string.py

# Valida la sintassi Lua di tutti i moduli dell'addon e delle auras embedded
python scratch/test_lua.py

# Verifica integrità albero WA, posizioni fila utility e simmetrie
python scratch/test_t8_t10_full.py

# Simula le 5 configurazioni di equipaggiamento (Solo T7, T7+T8, Solo T8, T8+T10, Solo T10)
python scratch/test_equip_switch.py

# Verifica la gestione di Focus Magic (proc 10s e buff alleato)
python scratch/test_focus_magic.py

# Verifica il calcolo delle statistiche e la risoluzione dei conflitti raid 3.3.5a
python scratch/test_stats_panel.py
```

---

## 📜 Repository & Licenza

- **Repository Ufficiale**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
- Distribuito sotto licenza **MIT**.
