# Fire Mage 3.3.5a AM (WoW 3.3.5a) — Handoff Tecnico

Suite WeakAura modulare, ad altissime prestazioni e ad architettura pura per **Mago Fuoco Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).

---

## 1. Architettura di Progetto & Specifiche Piattaforma

| Componente | Specifica / Implementazione | Note Tecniche |
| :--- | :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (*WotLK Build 12340*) | Compatibile con tutti i core emulatore (*TrinityCore, AzerothCore, Mangos*) |
| **Addon Target** | WeakAuras 4.0.0 (Backport WotLK 3.3.5a) | Engine nativo WA4, `internalVersion = 52` |
| **Modalità di Distribuzione** | **WeakAura 100% Pura** (`IMPORT_STRING.txt`) | Importabile con un solo clic. Nessun file esterno o addon obbligatorio |
| **Backup Versione Precedente** | `IMPORT_STRINGOLD.txt` | Stringa di backup della versione prima dell'integrazione T8 |
| **Addon Companion Standalone** | `FireMageHUD.toc` + moduli in `modules/` | Opzionale per chi preferisce l'esecuzione diretta come addon Lua nativo |
| **Formato di Serializzazione** | `!WA:1!` (LibDeflate Little-Endian 6-bit) | Compressione LibDeflate + AceSerializer-3.0 Protocol Rev 1 |
| **Tipografia & Texture** | Font `Expressway` (Outline) & Blizzard StatusBars | SubRegions WA4 (`subbackground`, `subforeground`, `subtext`, `subglow`) |
| **Posizionamento Schermo** | Gruppo Master a `x = 0, y = -190`, Scala `1.2` | Posizionato nella tasca centrale sopra le barre; privo di collisioni |
| **Controllo Versione** | Git su GitHub: [`Glacyal/FireMageHUD-335`](https://github.com/Glacyal/FireMageHUD-335) | Branch principale: `main` |

---

## 2. Filosofia del Design Visivo & Anti-Cluttering

L'interfaccia è progettata secondo i principi di **massima ergonomia e pulizia visiva (Zero UI Clutter)**:

1. **Buff Nascosti se > 5 Minuti (*Molten Armor, Intellect, Focus Magic*)**:
   - I buff a lunga durata restano invisibili durante il combattimento fintanto che mancano più di 5 minuti.
   - Compaiono automaticamente con conto alla rovescia a orologio (*swipe radiale*) e timer colorato (*giallo > 60s, rosso $\le$ 60s*) solo quando scendono a $\le$ 5 minuti (300s).
   - Se assenti o scaduti, mostrano l'icona desaturata con avviso rosso **`OFF`**.
2. **Cluster Centrale Unificato (Larghezza 264px)**:
   - Castbar, GCD, Mana Bar e Hot Streak Bar condividono la medesima larghezza di 264px, perfettamente impilate l'una sull'altra.
3. **Fila Utility Dinamica Adattiva (6 vs 7 Icone)**:
   - Se si usano solo T7 o solo T10 (o $< 2$ pezzi T8), la riga è predisposta a 6 moduli simmetrici spaziati a 44px.
   - Con $\ge 2$ pezzi T8, viene inserito il modulo T8 al centro e gli altri si restringono dinamicamente a 38px, mantenendo la simmetria assoluta.
4. **Timer Intelligenti con Allerta Rossa di Scadenza**:
   - I procs e debuff dinamici (*Scorch $\le$ 5s, Hot Streak $\le$ 3s, Living Bomb $\le$ 3s prima dell'esplosione, Ignite $\le$ 1.5s*) commutano automaticamente il testo in rosso vivo a 1 decimale (`|cFFFF4444%.1fs|r`), avvertendo tempestivamente del momento ottimale per il refresh senza clippare i tick.

---

## 3. Dettagli di Implementazione dei Moduli

### 3.1 Barra Hot Streak (`10 - Hot Streak Bar`) — Redesign Dinamico a Barra Unica

Collocata a filo sotto la Barra del Mana a `yOffset = -25` (larghezza 264px, spessore 7px, metà spessore della mana bar).

```
Stato Iniziale:
[                       Cornice Scura 264x7px                       ]

1° Critico Diretto (Metà Barretta a Sinistra 50%, Persistente):
[█████████████████████|                                             ]  (130x5px Arancio Fuoco)

2° Critico / Hot Streak Proc (I due segmenti DIVENTANO UNICO a 264px!):
[███████████████████████████████████████████████████████████████████]  (Pixel Glow + Swipe 10s)

Lancio di Pyroblast (o scadenza 10s):
[                                                                   ]  (Reset istantaneo a 0)
```

- **Rilevazione 1° Critico (Fix CLEU WotLK 3.3.5a)**:
  - Frame invisibile dedicato nativo (`FMHUD_HSFrame`) registrato a `COMBAT_LOG_EVENT_UNFILTERED`, `UNIT_AURA`, `UNIT_SPELLCAST_SUCCEEDED`, ecc.
  - Parsing multi-offset compatibile con tutti i core emulatore.
  - Filtro rigoroso su `SPELL_DAMAGE` diretto: i DoT periodici (*Ignite, tick di Living Bomb*) producono `SPELL_PERIODIC_DAMAGE` e vengono ignorati, preservando lo streak.
- **1° Critico**: Illumina esattamente il 50% a sinistra (`width: 130px, xOffset: -66`) e **resta persistente nel tempo** in attesa del colpo successivo.
- **2° Critico Consecutivo (Hot Streak Proc)**:
  - Il segmento al 50% si nasconde e viene attivata la **Barra di Proc unificata a piena larghezza (264x5px a `xOffset: 0`)**!
  - Mostra il **Pixel Glow** dorato/arancione e avvia il conto alla rovescia swipe di 10 secondi del buff Hot Streak (48108).
- **Lancio Pyroblast (o fine 10s)**:
  - Al lancio di Pyroblast istantaneo (`UNIT_SPELLCAST_SUCCEEDED`), la barra si azzera all'istante tornando alla sola cornice di fondo scura.
- **Zero Testo**: Design puramente visuale, privo di testi sovrapposti.

---

### 3.2 Modulo Tier 8 2-Piece Bonus (`06 - Tier 8` — Praxis)

Posizionato a `x = 0, y = -54` al centro della riga utility:
- **Auto-Rilevamento Intelligente**:
  - Scansiona i 10 pezzi T8 Kirin Tor (10m: 45367, 45369, 45365, 45366, 45368; 25m: 45357, 45359, 45355, 45356, 45358).
- **Adattamento Dinamico del Layout**:
  - Funzione condivisa `_G.FMHUD_SetUtilityPos(env, x6, x7)` che aggiorna i punti delle icone utility senza ricaricare la UI.
  - Con $< 2$ pezzi T8: `06 - Tier 8` è nascosto, le altre 6 icone si posizionano su `[-110, -66, -22, +22, +66, +110]` (spaziatura 44px).
  - Con $\ge 2$ pezzi T8: `06 - Tier 8` appare a `x = 0`, le altre 6 icone si stringono su `[-114, -76, -38, +38, +76, +114]` (spaziatura 38px).
- **Tracciamento Proc & ICD**:
  - **Buff Attivo**: Praxis (Spell ID 64868, +350 SP per 15s) con **Pixel Glow** e timer decimale giallo `|cFFFFFF00%.1fs|r`.
  - **Internal Cooldown (ICD)**: 45 secondi complessivi (15s buff + 30s ricarica a orologio con timer residuo `%.0f`).
  - **Stato Pronto**: Icona desaturata o pulita pronta al prossimo proc.

---

### 3.3 Focus Magic Monitor (`04 - Focus Magic`) — Tracking Intelligente

Posizionato a `x = -150, y = -14` (in riga sopra il pannello statistiche).
- **Back-Propagation del Proc**: Quando il Mago riceve il buff di 10s dall'alleato, il sistema estende la durata del buff alleato a 30 minuti, prevenendo falsi allarmi "OFF" ed evitando la necessità di ritarghettare l'alleato.
- **Scansione Automatica**: Monitora continuamente `target`, `focus`, `party1..4`, `raid1..40`.

---

### 3.4 Gemma del Mana (`06 - Mana Gem`) — Proc Bonus T7 & Cooldown Dinamico

Posizionata nella fila utility a `y = -54`:
- **Bonus Set Tier 7 (2 pezzi - "Mana Surge")**:
  - All'uso attiva il buff "Mana Surge" (+225 Spell Power per 15s, Spell ID 61062).
  - L'icona **commuta dinamicamente sul simbolo di Mana Surge** (`Spell_Arcane_ManaSurge`), accende il **Pixel Glow** dorato e mostra il conto alla rovescia del proc (`%.1fs`).
- **Cooldown Oggetto (2 minuti)**:
  - Al termine del buff T7, l'icona ritorna allo Zaffiro del Mana (`INV_Misc_Gem_Sapphire_02`), spegne il glow e mostra lo swipe radiale e il cooldown residuo.
- **Cariche Residue**: Ancorate in ALTO A DESTRA (`INNER_TOPRIGHT`).

---

### 3.5 Trinkets Slot 13 & 14 (`05 - Trinket 1` & `05 - Trinket 2`) & Mantello (`06 - Cloak`)

Posizionati a `y = -54`:
- **Database 40+ Trinket WotLK**: Riconoscimento automatico On-Use e proc passivi con ICD (45s per DFO/CTS, 90s per Filatterio).
- **Pixel Glow & Swipe Radiale**: Glow durante il proc attivo, swipe a orologio durante l'ICD.

---

### 3.6 Real-Time Stats Panel (`12 - Stats Panel`)

Posizionato a `x = -180, y = -54` (box 88x48px con 4 righe real-time):
1. **SP**: `GetSpellBonusDamage(3)` per la scuola Fuoco (gear, buff, proc, pozioni).
2. **Crit**: `GetSpellCritChance(3)` + Molten Armor + talenti Fire + stack Combustion (+10% a carica) + debuff boss (+5% Scorch, +3% Totem).
3. **Haste**: `UnitSpellHaste("player")` + moltiplicatori raid (*Bloodlust, Totem, Moonkin*).
4. **Hit**: Rating + Precision (+3%) + Draenei (+1%) + debuff boss (+3% Misery/Faerie Fire) con indicatore verde **`(Cap)`** a $\ge 17\%$.

---

## 4. Architettura Completa dei Moduli (28 Displays WA4)

```text
Fire Mage 3.3.5a AM (root: group, internalVersion: 52, xOffset: 0, yOffset: -190, scale: 1.2, load: Mage + Living Bomb)
│
├── 01 - Procs (dynamicgroup: horizontal, center-aligned, space: 6px, yOffset: +52)
│   ├── Hot Streak (icon: aura2 buff "Hot Streak", matchesShowOn: "showOnActive", Pixel Glow dorato)
│   ├── Clearcasting (icon: aura2 buff "Clearcasting" / "Arcane Concentration" 12536, timer %p)
│   ├── Living Bomb (icon: aura2 debuff "Living Bomb" su target, allerta rossa <= 3s prima dell'esplosione)
│   ├── Ignite (icon: aura2 debuff "Ignite" su target, allerta rossa <= 1.5s)
│   ├── Scorch (icon: custom status debuff Scorch/Improved Scorch su target, allerta rossa <= 5s)
│   └── Molten Fury (icon: target health <= 35%, subtext "35%")
│
├── Colonna Buff a Sinistra (Riga Orizzontale a y = -14, sopra Stats Panel)
│   ├── 03 - Arcane Intellect (x = -210, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   ├── 02 - Molten Armor     (x = -180, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso)
│   └── 04 - Focus Magic      (x = -150, y = -14: Nascosta > 5m, Timer <= 5m, OFF rosso se non assegnato)
│
├── 12 - Stats Panel (x = -180, y = -54, sotto i 3 buff - Box 88x48 con 4 righe real-time)
│   ├── SP:    Fire Spell Power (rosso, include proc/buff/gear in tempo reale)
│   ├── Crit:  Fire Spell Crit (arancione, include Molten Armor, Combustion, debuff boss)
│   ├── Haste: Spell Haste (viola, include rating e moltiplicatori raid)
│   └── Hit:   Spell Hit (giallo, include talenti, razza e debuff con indicatore Cap a >= 17%)
│
├── Cluster Centrale (Larghezza 264px, impilato verticalmente)
│   ├── 08 - Castbar         (y =  +8, w = 264, h = 20: Icona a sx, nome spell a sx, tempo a dx)
│   ├── 09 - GCD             (y =  -4, w = 264, h =  3: Barra bianca sottile per spell 61304)
│   ├── 07 - Mana Bar        (y = -15, w = 264, h = 14: % con 2 decimali, rossa se <= 20%)
│   └── 10 - Hot Streak Bar  (y = -25, w = 264, h =  7: Barretta dinamica pulita, no testo)
│       ├── Hot Streak Bar - Background (texture: cornice scura 264x7px)
│       ├── Hot Streak Bar - Segment 1  (texture: 130x5px a sx, 50% 1° critico persistente)
│       └── Hot Streak Bar - Proc       (aurabar: 264x5px intera, countdown 10s con Pixel Glow)
│
├── Fila Utility Inferiore Dinamica (y = -54, margine di 11.5px sotto la Hot Streak Bar)
│   ├── MODALITÀ 6 ICONE (< 2 pezzi T8 equipaggiati - Spaziatura 44px):
│   │   ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD)
│   │   ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│   │   ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│   │   └── 06 - Mirror Image (x = +110: Glow attivo 30s + Swipe orologio CD 3m)
│   │
│   └── MODALITÀ 7 ICONE RISTRETTE (>= 2 pezzi T8 equipaggiati - Spaziatura 38px):
│       ├── 05 - Trinket 1    (x = -114: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 05 - Trinket 2    (x =  -76: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Cloak        (x =  -38: Glow attivo + Swipe orologio + Countdown ICD)
│       ├── 06 - Tier 8       (x =    0: Praxis +350 SP 15s con Glow + Swipe ICD 30s)
│       ├── 06 - Mana Gem     (x =  +38: T7 2pc Glow dorato + Timer %p + CD 2m + Cariche)
│       ├── 06 - Combustion   (x =  +76: Glow attivo + Stacks x%d + Swipe orologio CD)
│       └── 06 - Mirror Image (x = +114: Glow attivo 30s + Swipe orologio CD 3m)
│
└── 10 - Alerts (y = +105, sopra i Proc)
    └── Alert - Hot Streak (text: alert "HOT STREAK! / PYROBLAST READY!" font expressway)
```

---

## 5. Procedura di Rigenerazione & Validazione

Per compilare la stringa WeakAuras ed eseguire tutti i test di validazione sintattica e logica:

```bash
# 1. Rigenera la stringa compressa WA4 (!WA:1!) in IMPORT_STRING.txt
python generate_import_string.py

# 2. Esegui la suite di test sulla logica e sul simulatore Hot Streak
python scratch/test_hotstreak_logic.py

# 3. Esegui il validatore di sintassi Lua per tutti i moduli
python scratch/test_lua.py
```

---

## 6. Istruzioni di Importazione in-Game

1. Copia l'intero contenuto di **[`IMPORT_STRING.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRING.txt)** (`Ctrl+A`, `Ctrl+C`).
2. In World of Warcraft, digita `/wa` per aprire WeakAuras.
3. Clicca su **Import** in alto a sinistra e incolla la stringa (`Ctrl+V`).
4. Seleziona **`Update Auras`** (o **`Replace`** per una reinstallazione pulita).
5. Chiudi la finestra con `Esc`. Il tuo HUD **Fire Mage 3.3.5a AM** è pronto all'uso!
