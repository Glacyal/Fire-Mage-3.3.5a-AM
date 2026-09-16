# Fire Mage 3.3.5a AM — Handoff Tecnico

Manuale di riferimento tecnico per lo sviluppo, la manutenzione e l'estensione della suite **Fire Mage 3.3.5a AM** per World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Panoramica del Progetto

La suite è distribuita come **WeakAura autonoma** in formato compresso `!WA:1!` (serializzazione `AceSerializer-3.0` + compressione `LibDeflate`). Include un simulatore web interattivo per la visualizzazione immediata del layout ospitato su GitHub Pages e una suite completa di test deterministici in Python.

| Proprietà | Dettaglio |
| :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (WotLK Build 12340) |
| **Engine WeakAuras** | WeakAuras 2 / 3 Backport 3.3.5a (`internalVersion = 52`, header `!WA:1!`) |
| **File di Distribuzione** | [`IMPORT_STRING.txt`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/IMPORT_STRING.txt) |
| **Simulatore Web** | [`docs/index.html`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/docs/index.html) |
| **Live Demo Online** | [GitHub Pages Live Showcase](https://glacyal.github.io/FireMageHUD-335/) |
| **Controllo Versione** | Git su GitHub: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335) (branch: `main`) |

---

## 2. Struttura del Repository

```text
Fire Mage 3.3.5a AM/
├── IMPORT_STRING.txt                # Stringa WeakAuras pronta all'uso per il comando /wa
├── generate.py                      # Compilatore Python dell'albero WA
├── README.md                        # Documentazione utente, guida installazione e compatibilità
├── HANDOFF.md                       # Specifiche tecniche per sviluppatori e manutentori
├── GEMINI.md                        # Regole di progetto, comandi CP e MODELLO
│
├── builder/                         # Pacchetto Python modulare per la generazione dell'HUD
│   ├── tree.py                      # Assemblatore dell'albero gerarchico (28 nodi WeakAuras)
│   ├── core/                        # Moduli core di serializzazione e codifica
│   │   ├── constants.py             # Load conditions (Mage 68), texture, font Expressway
│   │   ├── serializer.py            # Serializzatore AceSerializer-3.0 puro (^1...^^)
│   │   ├── deflate.py               # Compressione Deflate RFC 1951 + LibDeflate Print Encoding
│   │   ├── encoder.py               # Generatore stringa finale (!WA:1!...)
│   │   └── helpers.py               # Generatori di subtext e helper grafici
│   └── components/                  # Moduli dedicati ai singoli componenti dell'HUD
│       ├── hot_streak.py            # Barra Hot Streak a doppio segmento decoppiato
│       ├── procs.py                 # Gruppo dinamico 01 - Procs (7 icone con Ignite)
│       ├── buffs.py                 # 02 - Molten Armor, 03 - Arcane Intellect, 04 - Focus Magic
│       ├── utility.py               # 06 - Utility Row (Combustion, DFO, CTS, Gemma, Copie, T8)
│       ├── bars.py                  # 08 - Castbar, 09 - Mana Bar, Global Cooldown (GCD)
│       ├── stats.py                 # 07 - Stats (SP, Crit, Haste, Hit con cap resolution)
│       └── alerts.py                # Allerte visive testuali a centro schermo (HOT STREAK! / PYROBLAST READY!)
│
├── docs/                            # Documentazione e anteprima interattiva per GitHub Pages
│   └── index.html                   # Simulatore interattivo HTML/CSS/JS (proporzioni 1:1)
│
└── tests/                           # Suite di test automatici e paralleli
    ├── run_parallel_tests.py        # Test runner parallelo multi-processore (ProcessPoolExecutor)
    ├── test_components_integrity.py # Verifica integrità strutturale moduli
    ├── test_hotstreak_decoupled.py  # Test logica Hot Streak persistente e decoppiata
    ├── test_html_simultaneous.py    # Stress test concorrenza simulatore web
    ├── test_showcase.py             # Audit 100% interattività e handler DOM
    ├── test_lua.py                  # Validazione sintassi codice Lua
    ├── test_tree_layout.py          # Verifica gerarchia e proporzioni albero WA
    ├── test_equip_switch.py         # Test switch dinamico 6 vs 7 icone
    ├── test_focus_magic.py          # Test stati e transizioni Focus Magic
    └── test_stats_panel.py          # Test calcolo statistiche e conflitti raid
```

---

## 3. Workflow di Sviluppo

Per apportare modifiche alla suite o estendere la logica:

1. **Modifica Componenti**:
   - Modifica i moduli Python in `builder/components/` o le librerie in `builder/core/`.
2. **Esecuzione Test Paralleli**:
   - Lancia la suite di test completa sfruttando tutti i core della CPU:
     ```bash
     python tests/run_parallel_tests.py
     ```
   - Oppure esegui i test mirati:
     ```bash
     python -m unittest tests/test_hotstreak_decoupled.py
     python tests/test_showcase.py
     ```
3. **Compilazione Stringa di Importazione**:
   - Ricompila la stringa WA eseguendo:
     ```bash
     python generate.py
     ```
   - Questo aggiornerà deterministicamente [`IMPORT_STRING.txt`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/IMPORT_STRING.txt).
4. **Verifica Simulatore Web**:
   - Se hai modificato il layout o aggiunto elementi visivi, aggiorna `docs/index.html` e lancia:
     ```bash
     python tests/test_showcase.py
     ```
5. **Commit & Push (`CP`)**:
   - Usa il comando utente `CP` per verificare, committare e sincronizzare il branch `main` su GitHub.

---

## 4. Specifiche Architetturali Chiave

### 4.1 Barra Hot Streak Decoppiata (`10 - Hot Streak Bar`)
- **Posizione**: Subito sotto la barra del Mana (`y = -25`, larghezza totale 278px, altezza 7px).
- **Architettura a Due Segmenti Decoppiati**:
  1. **Segment 1 (Metà Sinistra, 137x5px a x = -70.5)**:
     - Traccia lo stato binario `0` o `1` del 1° colpo critico andato a segno (*Fireball, Scorch, Fire Blast, Frostfire Bolt, esplosione Living Bomb*).
     - **Persistenza**: Non scade nel tempo e non decade uscendo dal combattimento.
     - **Reset**: Si azzera a `0` solo al 2° critico consecutivo (che innesca il proc) o se la spell qualificabile successiva non critta.
     - **Non azzerato da Pyroblast**: Il lancio di Pyroblast non resetta questo segmento, permettendo la gestione del *Rolling Hot Streak*.
  2. **Proc (Metà Destra, 137x5px a x = +70.5)**:
     - Traccia nativamente il buff `Hot Streak` (Spell ID 48108) con conto alla rovescia di 10 secondi, swipe circolare e Pixel Glow dorato.
     - È completamente svincolato dal segmento di sinistra: si spegne al consumo o scadenza del buff.

### 4.2 Gruppo Dinamico Procs (`01 - Procs`)
- **Posizione**: Sopra la Castbar a `y = 42`.
- **Icone Reattive (fino a 7 contemporanee)**:
  1. `Tier 10 (Pushing the Limit)`: +12% Haste per 5s con Pixel Glow dorato.
  2. `Hot Streak`: Icona proc con timer.
  3. `Clearcasting`: Proc mana free.
  4. `Living Bomb`: Debuff sul target con countdown swipe.
  5. `Ignite`: Debuff di 4s rolling sul target da spell critiche.
  6. `Improved Scorch`: Debuff +5% spell crit sul target.
  7. `Molten Fury`: Bersaglio con salute < 35% (+12% danno aumentato).
- **Combustion**: Collocata **esclusivamente** nella riga utility (`06 - Utility Row`), evitando duplicazioni nel gruppo procs.

### 4.3 Focus Magic Anti-Clutter (`04 - Focus Magic`)
- **Invisibile di base**: Se il buff è attivo su un alleato vivo, l'icona è nascosta per preservare la pulizia dello schermo.
- **Proc 10s Personale**: Quando l'alleato mette a segno un critico, compare con swipe e conto alla rovescia (+3% Crit per 10s).
- **Allerta OFF**: Se il buff non è assegnato a nessuno o se l'alleato muore, compare l'icona desaturata con avviso `OFF` rosso.

### 4.4 Switch Dinamico Tier 8 & Tier 10
- **Tier 10 2P**: Collocato dinamicamente in `01 - Procs` a sinistra di Hot Streak.
- **Tier 8 2P**: Gestito tramite riposizionamento globale nella riga utility in basso:
  - Con $\ge 2$ pezzi T8 equipaggiati: layout a **7 icone** (passo 38px, span 256px) con *Praxis* (+350 SP con ICD 45s) al centro esatto (`x = 0`).
  - Con $< 2$ pezzi T8 equipaggiati: layout standard a **6 icone** (passo 44px, span 248px) nascondendo *Praxis*.

### 4.5 Risoluzione Conflitti Statistiche di Raid
Il modulo `builder/components/stats.py` impedisce la duplicazione di buff raid della stessa categoria:
- **Haste 3%**: *Swift Retribution* (Paladino) e *Improved Moonkin Form* (Druido) conteggiati una sola volta.
- **Spell Crit 5%**: *Improved Scorch*, *Winter's Chill* e *Shadow and Flame* conteggiati una sola volta.
- **All Crit 3%**: *Heart of the Crusader*, *Master Poisoner* e *Totem of Wrath* conteggiati una sola volta.
- **Hit 3%**: *Misery* e *Improved Faerie Fire* conteggiati una sola volta.

---

## 5. Note di Compatibilità Addon & API

- **Client 3.3.5a**: Compatibilità nativa 100%. Gli script Lua impiegano `COMBAT_LOG_EVENT_UNFILTERED` con passaggio parametri tramite `...`, `UnitBuff` con return a 11 argomenti e `GetNumPartyMembers()`.
- **Client Moderni / Retail**: WeakAuras 5 su client moderni non è compatibile per via delle modifiche alle API Blizzard (`CombatLogGetCurrentEventInfo`, `C_UnitAuras`, rimozione di `GetNumPartyMembers`) e della diversa rotazione del Mago Fuoco.
