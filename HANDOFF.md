# Fire Mage 3.3.5a AM — Handoff Tecnico

Manuale di riferimento tecnico per lo sviluppo, la manutenzione e l'estensione della suite **Fire Mage 3.3.5a AM** per World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Panoramica del Progetto

La suite è distribuita principalmente come **WeakAura 100% autonoma** in formato compresso `!WA:1!`, senza dipendenze da addon esterni. Include inoltre un simulatore web interattivo per la visualizzazione immediata del layout e una suite completa di test deterministici in Python.

| Proprietà | Dettaglio |
| :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (WotLK Build 12340) |
| **Engine WeakAuras** | WeakAuras 4.0.0 (Backport 3.3.5a, `internalVersion = 52`) |
| **File di Distribuzione** | [`IMPORT_STRING.txt`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/IMPORT_STRING.txt) |
| **Simulatore Web** | [`index.html`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/index.html) |
| **Controllo Versione** | Git su GitHub: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335) (branch: `main`) |

---

## 2. Struttura del Repository

```text
Fire Mage 3.3.5a AM/
├── IMPORT_STRING.txt         # Stringa WeakAuras pronta all'uso per il comando /wa
├── generate_import_string.py # Compilatore Python dell'albero WA (AceSerializer + LibDeflate)
├── index.html                # Simulatore interattivo HTML/CSS/JS (proporzioni 1:1)
├── t8_t10_preview.html       # Copia di sincronizzazione dello showcase
│
├── modules/                  # Moduli Lua con la logica dei singoli componenti
│   ├── Alerts.lua            # Allerte visive e sonore (es. Hot Streak / Pyroblast pronto)
│   ├── Castbar.lua           # Barra di lancio con icona, nome spell e tempo residuo
│   ├── Cloak.lua             # Monitoraggio incantamento mantello e timer ICD
│   ├── Focus.lua             # Logica anti-clutter per Focus Magic e proc 10s
│   ├── GCD.lua               # Barretta sottile del Global Cooldown
│   ├── HotStreakBar.lua      # Barra dinamica unificata (1° critico persistente + proc)
│   ├── Intellect.lua         # Monitoraggio Arcane Intellect (nascosto se > 5m)
│   ├── Mana.lua              # Barra del Mana in percentuale con allerta sotto il 20%
│   ├── ManaGem.lua           # Gemma del mana con cariche, cooldown e bonus 2P T7
│   ├── MirrorImage.lua       # Copie con tracciamento durata e bonus 4P T10
│   ├── MoltenArmor.lua       # Monitoraggio Molten Armor (nascosto se > 5m)
│   ├── Procs.lua             # Gruppo orizzontale procs sopra la Castbar
│   ├── Stats.lua             # Pannello 4 statistiche (SP, Crit, Haste, Hit)
│   ├── Tier8.lua             # Bonus 2P T8 Praxis (+350 SP per 15s con timer ICD)
│   ├── Tier10.lua            # Bonus 2P T10 Pushing the Limit (+12% Haste per 5s)
│   └── Trinkets.lua          # Engine universale monili con ICD (DFO, CTS, ecc.)
│
├── tests/                    # Suite di test automatici in Python
│   ├── test_lua.py           # Validazione della sintassi Lua (moduli e codice embedded)
│   ├── test_tree_layout.py   # Verifica albero WA, gerarchia e proporzioni geometriche
│   ├── test_equip_switch.py  # Test del passaggio dinamico a 6 vs 7 icone
│   ├── test_focus_magic.py   # Test degli stati e delle transizioni di Focus Magic
│   ├── test_stats_panel.py   # Test del calcolo statistiche e risoluzione conflitti raid
│   └── test_showcase.py      # Audit dell'interattività e dei pulsanti del simulatore web
│
├── Config.lua                # Configurazione per eventuale addon standalone
├── Core.lua                  # Libreria di utility per addon standalone
├── FireMageHUD.toc           # Manifest per eventuale addon standalone
└── README.md                 # Documentazione utente e guida di installazione
```

---

## 3. Workflow di Sviluppo

Per apportare modifiche alla suite o aggiornare la logica di gioco:

1. **Modifica Codice**:
   - Modifica la logica nei file della cartella `modules/` o direttamente nei template di `generate_import_string.py`.
2. **Esecuzione dei Test**:
   - Lancia la suite di test sfruttando il multi-threading del processore per la massima velocità, oppure lancia script specifici in base alle modifiche fatte:
     ```bash
     python tests/run_parallel_tests.py
     # Oppure singolarmente:
     python tests/test_html_simultaneous.py
     python tests/test_showcase.py
     python tests/test_lua.py
     ```
3. **Rigenerazione della Stringa**:
   - Ricompila la stringa WA eseguendo:
     ```bash
     python generate_import_string.py
     ```
   - Il comando aggiornerà [`IMPORT_STRING.txt`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/IMPORT_STRING.txt) in modo deterministico.
4. **Verifica sul Simulatore**:
   - Se hai modificato il layout o aggiunto elementi visivi, aggiorna e verifica `index.html` e lancia:
     ```bash
     python tests/test_showcase.py
     ```
5. **Commit & Push**:
   - Usa il flusso Git standard o il comando `CP` per sincronizzare il repository remoto.

---

## 4. Specifiche Architetturali Chiave

### 4.1 Barra Hot Streak (`10 - Hot Streak Bar`)
- **Posizione**: Subito sotto la barra del Mana (`y = -25`, larghezza 264px, altezza 7px).
- **Stato 1° Critico**: Attiva la metà sinistra da 130px in arancione vivo. I DoT periodici (*Ignite, tick di Living Bomb*) non interferiscono. La barra **resta attiva indefinitamente** fino al colpo successivo.
- **Stato Proc (Hot Streak)**: Si unifica in una singola barra continua da 264px con Pixel Glow dorato e countdown swipe di 10 secondi.
- **Reset**: Si azzera istantaneamente al lancio di *Pyroblast!* o alla scadenza naturale.

### 4.2 Focus Magic (`04 - Focus Magic`)
- **Invisibile di base**: Se il buff è applicato su un alleato vivo, l'icona è completamente nascosta per preservare la pulizia dell'interfaccia.
- **Proc 10s**: Quando l'alleato mette a segno un critico, l'icona compare con il countdown dei 10 secondi.
- **Allerta OFF**: Se il buff non è attivo su nessuno o se l'alleato muore, compare l'icona desaturata con avviso `OFF` rosso.

### 4.3 Gestione Dinamica Tier 8 & Tier 10
- **Tier 10 2P**: Collocato nel gruppo dinamico `01 - Procs`, compare a sinistra di Hot Streak all'attivazione del buff (+12% Haste).
- **Tier 8 2P**: Gestito tramite la funzione globale `_G.FMHUD_UpdateUtilityRowPositions`.
  - **$\ge 2$ pezzi T8 equipaggiati**: attiva il **Layout a 7 icone** (passo 38px, span 256px) con T8 al centro esatto (`x = 0`).
  - **$< 2$ pezzi T8 equipaggiati**: attiva il **Layout Standard a 6 icone** (passo 44px, span 248px) nascondendo T8.

### 4.4 Risoluzione Conflitti Statistiche di Raid
Il pannello statistiche previene la duplicazione dei buff raid appartenenti alla stessa categoria:
- **Haste 3%**: *Swift Retribution* (Paladino) e *Improved Moonkin Form* (Druido) sono conteggiati una sola volta.
- **Spell Crit 5%**: *Improved Scorch*, *Winter's Chill* e *Shadow and Flame* sono conteggiati una sola volta.
- **All Crit 3%**: *Heart of the Crusader*, *Master Poisoner* e *Totem of Wrath* sono conteggiati una sola volta.
- **Hit 3%**: *Misery* e *Improved Faerie Fire* sono conteggiati una sola volta.

### 4.5 Ottimizzazione Estrema (Zero-Allocation e Concorrenza)
- **Zero-Allocation**: La WA alloca strutture di supporto (es. `_G.FMHUD_ArmorSlots`) una volta sola globalmente, limitando al massimo la creazione di garbage e sventando gli spike di latenza della Garbage Collection di Lua 5.1.
- **Throttling CPU**: Le logiche con eventi ad alta frequenza (come i loop del pannello stat o della corazza) adottano un throttle manuale (es. limitato a `0.25s` o 4Hz). I trigger non essenziali sono stati epurati dall'evento passivo `FRAME_UPDATE`.
- **Client Agnostici**: La suite riconosce i buff tramite **Spell ID** anziché nome, garantendo il supporto nativo a tutte le lingue dei client (En, It, Ru, ecc).

---

## 5. Linee Guida per Contributi Futuri

- **Compatibilità Lua 5.1**: Non utilizzare sintassi o funzioni introdotte in versioni successive di Lua (es. operatori bitwise nativi di Lua 5.3; usare `bit.band` se necessario).
- **Auto-sufficienza delle Auras**: Ciascun blocco di codice inserito in `generate_import_string.py` deve poter funzionare in autonomia all'interno dell'ambiente protetto di WeakAuras.
- **Determinismo**: La stringa esportata deve essere sempre riproducibile eseguendo `generate_import_string.py`.
