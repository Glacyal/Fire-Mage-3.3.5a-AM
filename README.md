# Fire Mage 3.3.5a AM — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/Fire-Mage-3.3.5a-AM)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-4.0.0-blue.svg)](https://github.com/Glacyal/Fire-Mage-3.3.5a-AM)
[![Class](https://img.shields.io/badge/Class-Mage%20(Fire)-red.svg)](https://github.com/Glacyal/Fire-Mage-3.3.5a-AM)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Glacyal/Fire-Mage-3.3.5a-AM)
[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg)](https://glacyal.github.io/Fire-Mage-3.3.5a-AM/)

Suite WeakAuras completa, ingegnerizzata a livello enterprise, modulare ed ergonomica per **Mago Fuoco Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).  
Progettata per garantire prestazioni estreme in raid, latenza Lua minima, tracciamento chirurgico dei proc e un'interfaccia "Zero-Clutter" focalizzata sull'ottimizzazione del DPS.

---

## 🌐 Anteprima Online (Live Simulator)

Visualizza e interagisci con l'HUD direttamente dal browser senza installare nulla:  
👉 **[Apri il Simulatore Web su GitHub Pages](https://glacyal.github.io/Fire-Mage-3.3.5a-AM/)**  
*(Disponibile anche in locale nel file [`docs/index.html`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/docs/index.html))*

---

## 🌟 Caratteristiche Principali

### 1. Barra Hot Streak a Doppio Segmento Decoppiato (Rolling Streak)
La barra centrale (278px totali a `y = -25`) è suddivisa in **due metà completamente indipendenti**:
- **Mezza Barra Sinistra (Segment 1 — 137px a x = -70.5)**:
  - **Stato Binario (0 o 1 critico)**: Si accende in arancione brillante al primo critico diretto (*Fireball, Scorch, Fire Blast, Frostfire Bolt, esplosione di Living Bomb*).
  - **Persistente nel Tempo e Fuori dal Combat**: Non decade mai, nemmeno uscendo dal combattimento, finché non si lancia un altro colpo diretto.
  - **Reset Mirato**: Si azzera a `0` solo quando avviene il 2° critico consecutivo (che fa accendere il proc a destra) oppure se il colpo andato a segno è un non-critico.
  - **NON si azzera lanciando la Pyroblast!**: Questo consente il tracciamento fluido del critico successivo anche mentre il buff di Hot Streak è attivo (*Rolling Hot Streak*).
- **Mezza Barra Destra (Proc — 137px a x = +70.5)**:
  - Tracciamento nativo del buff **Hot Streak** (Spell ID 48108) con **conto alla rovescia di 10 secondi**, swipe radiale e **Pixel Glow dorato**.
  - Si spegne solo quando il buff viene consumato (lancio della Pyroblast istantanea) o alla scadenza naturale. Se il buff scade o viene rimosso, l'eventuale critico registrato sulla barra di sinistra rimane intatto!

### 2. Gruppo Dinamico Procs (`01 - Procs`)
Posizionato sopra la Castbar (`y = 42`), il gruppo dinamico orizzontale accoglie fino a 7 icone (34x34px) con contrazione automatica dello spazio:
1. **Tier 10 2P (*Pushing the Limit*)**: +12% Haste per 5s con Pixel Glow dorato su proc di Hot Streak.
2. **Hot Streak**: Icona del proc con timer e swipe.
3. **Clearcasting**: Lancio a costo zero di mana con timer e swipe.
4. **Living Bomb**: Monitoraggio del debuff sul bersaglio con conto alla rovescia e swipe per il refresh ottimale.
5. **Ignite**: Debuff di 4 secondi rolling generato sul bersaglio dai colpi critici.
6. **Improved Scorch**: Monitoraggio del debuff +5% crit magico sul bersaglio.
7. **Molten Fury**: Icona attiva in fase di Execute (bersaglio con HP < 35%, +12% danno aumentato).

### 3. Filosofia "Zero Clutter" (Schermo Pulito)
- **Molten Armor & Arcane Intellect**: Completamente **nascosti durante il combattimento** se hanno più di 5 minuti residui. Mostrano lo swipe radiale solo negli ultimi 5 minuti e l'allerta rossa **`OFF`** se scaduti o assenti.
- **Focus Magic Intelligente**: Nascosto fintanto che è attivo su un alleato vivo. Si attiva all'istante con swipe e countdown solo durante il **proc personale di 10 secondi (+3% Crit)**, per poi tornare nascosto. Segnala **`OFF`** se non assegnato o se il compagno muore.

### 4. Pannello Statistiche in Tempo Reale (`07 - Stats`)
Monitora costantemente le 4 statistiche chiave del Mago Fuoco, risolvendo automaticamente i conflitti tra buff di raid non cumulabili:
- **SP (Spell Power)**: Valore effettivo aggiornato con equipaggiamento, gemme, flask, buff raid e bonus 2P T8 (*Praxis*).
- **Crit %**: Include Molten Armor, talenti, Combustion e debuff boss (+5% Scorch/Winter's Chill e +3% Crusader/Poisoner) senza doppi conteggi.
- **Haste %**: Include rating ed è moltiplicato con Bloodlust (+30%), Totem (+5%), 3% raid, 2P T10 (+12%), Power Infusion e Berserking.
- **Hit %**: Precisione con talenti (*Precision*), Draenei (*Heroic Presence*) e debuff boss (+3% *Misery* / *Improved Faerie Fire*), con indicatore verde **`(Cap)`** al 17% (o 14% con debuff).

### 5. Riga Utility Adattiva Universale & Ingegneria (`06 - Utility Row`, da 3 a 9 Icone)
La riga inferiore (`y = -45`) si adatta in tempo reale con **riposizionamento e centratura dinamica universale** in base all'equipaggiamento effettivo:
- **Monili (`05 - Trinket 1` e `05 - Trinket 2`)**: Compaiono **solo se gli slot 13 e 14 sono equipaggiati** (nascosti se vuoti), con tracciamento di oltre 35 monili WotLK, timer ICD, swipe radiale e Pixel Glow dorato su proc attivo.
- **Mantello con Proc (`06 - Cloak`)**: Compare **solo se il mantello possiede un incanto di potenziamento** (*Ricamo di Luce Intessuta* +295 SP, *Bagliore Oscuro*, *Spadatesta*, *Ragnatela Flessibile*). Se non incantato o privo di proc, non compare.
- **Tier 8 2P (*Praxis*) (`06 - Tier 8`)**: Compare **solo con $\ge 2$ pezzi T8 Kirin Tor equipaggiati**, tracciando il proc +350 SP e l'ICD di 45s.
- **Guanti Ingegneria (`06 - Gloves`)**: Posizionati **immediatamente a sinistra della Gemma del Mana**. Compaiono **solo se il mago ha Ingegneria con *Acceleratori Ipersonici*** (Hyperspeed Accelerators: +340 Haste per 12s, 60s CD).
- **Gemma del Mana (`06 - Mana Gem`)**: Tracciamento delle cariche effettive in borsa (`3`, `2`, `1` o `0` in rosso se assente, senza prefisso `x`), icona nativa dinamica (Zaffiro/Smeraldo), cooldown di 2 minuti e bonus 2P T7 (+225 SP per 15s con Pixel Glow).
- **Combustion (`06 - Combustion`)**: Traccia stato ON, cooldown (2 minuti) e stack critici residui (+10% crit a carica) con icona nativa dell'incantesimo.
- **Mirror Image (`06 - Mirror Image`)**: Durata delle copie (30s), cooldown (3 min) e bonus 4P T10 (*Quad Core*, +18% danno).
- **Stivali (`06 - Boots`)**: Posizionati **immediatamente a destra delle Copie (Mirror Image)**. Compaiono **solo se gli stivali hanno un incanto che conferisce velocità di movimento** (*Acceleratori a Nitro* / Nitro Boosts per Ingegneria con indicatore dei Nitro attivi a 5s con Pixel Glow, countdown di cooldown a 180s e swipe, oppure incanti passivi come *Vitalità Tuskarr* / Tuskarr's Vitality, *Rapidità Felina*, *Velocità Superiore*, ecc.). Se non incantati con velocità o con slot vuoto, non compaiono.
- **Auto-Centratura Matematica**: L'ordine delle icone è:  
  `[Trinket 1] -> [Trinket 2] -> [Mantello] -> [Tier 8] -> [Guanti] -> [Gemma] -> [Combustione] -> [Copie] -> [Stivali]`  
  Qualsiasi combinazione di icone attive (da 3 a 9) viene ricalcolata e centrata simmetricamente attorno all'asse $X = 0$, confinandosi perfettamente entro la larghezza della barra superiore (264px).

### 6. Castbar & Mana Bar Integrate
- **08 - Castbar**: Barra di lancio (larghezza 210px) con icona della spell attiva, nome incantesimo, tempo residuo al decimo di secondo e indicatore visivo di latenza.
- **09 - Mana Bar**: Barra orizzontale con visualizzazione della percentuale numerica e allerta colorata sotto il 20% di mana.

---

## ⚙️ Architettura del Software Modulare (`builder/`)

Il codice sorgente è interamente modularizzato secondo i principi di **Ingegneria del Software**, separando la logica di serializzazione e compressione da ciascun componente dell'interfaccia:

```text
Fire Mage 3.3.5a AM/
├── builder/
│   ├── core/                        # Engine di Serializzazione e Compressione
│   │   ├── constants.py             # Costanti globali, load conditions (Mage 68), texture
│   │   ├── serializer.py            # Protocollo AceSerializer-3.0 puro (^1...^^)
│   │   ├── deflate.py               # Compressione Deflate RFC 1951 + LibDeflate print encoding
│   │   ├── encoder.py               # Generatore stringa WeakAuras (!WA:1!)
│   │   └── helpers.py               # Costruttori di sottotesti, formattazione e utility
│   ├── components/                  # Moduli Funzionali dell'HUD
│   │   ├── hot_streak.py            # Barra Hot Streak a 2 segmenti decoppiati & combat log
│   │   ├── procs.py                 # Gruppo dinamico 01 - Procs (7 icone reattive)
│   │   ├── buffs.py                 # Molten Armor, Arcane Intellect, Focus Magic
│   │   ├── utility.py               # Combustion, Monili, Mantello, T8, Guanti, Gemma, Copie, Stivali
│   │   ├── bars.py                  # Castbar, Mana Bar, Global Cooldown (GCD)
│   │   ├── stats.py                 # Pannello 4 Statistiche (SP, Crit, Haste, Hit)
│   │   └── alerts.py                # Allerte visive testuali a centro schermo (HOT STREAK! / PYROBLAST READY!)
│   └── tree.py                      # Assemblatore dell'albero gerarchico (37 aure WeakAuras)
├── docs/
│   └── index.html                   # Simulatore Web Interattivo (GitHub Pages 1:1)
├── tests/                           # Suite di test paralleli deterministici
│   ├── run_parallel_tests.py        # Runner parallelo multi-processore
│   ├── test_all_utility_cases.py    # Verifica esaustiva 64 combinazioni riga utility
│   ├── test_components_integrity.py # Verifica integrità strutturale moduli (37 aure)
│   ├── test_equip_switch.py         # Test transizioni e centratura universale da 3 a 9 icone
│   ├── test_hotstreak_decoupled.py  # Test logica Hot Streak persistente e decoppiata
│   ├── test_html_simultaneous.py    # Stress test concorrenza simulatore web
│   ├── test_lua.py                  # Validazione sintattica blocchi Lua embedded
│   ├── test_showcase.py             # Audit 100% interattività e handler DOM
│   ├── test_stats_panel.py          # Verifica formule e moltiplicatori pannello statistiche
│   └── test_tree_layout.py          # Geometrie layout e albero WA
├── generate.py                      # Compilatore Python della stringa finale
└── IMPORT_STRING.txt                # Stringa WeakAuras generata pronta all'uso
```

---

## 🚀 Installazione in Gioco (3 Passaggi)

1. **Copia la Stringa**: Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/IMPORT_STRING.txt)** e copia tutto il testo (`Ctrl+A`, poi `Ctrl+C`).
2. **Apri WeakAuras**: In World of Warcraft, digita `/wa` nella chat di gioco.
3. **Importa**: Clicca su **Import** (o Importa) in alto a sinistra, incolla il testo con `Ctrl+V` e conferma cliccando su **Import** (o Aggiorna se sovrascrivi una versione precedente).

---

## 📌 Compatibilità Addon & Client

| Client / Piattaforma | Versione WeakAuras | Compatibilità | Note |
| :--- | :--- | :---: | :--- |
| **WotLK 3.3.5a (Build 12340)** | **WeakAuras 4.0.0** | ✅ **100% Nativa** | Sviluppata e validata su WeakAuras 4.0.0 (`internalVersion: 52`). Tutti i test sono stati eseguiti su questa versione di WeakAuras. Importazione istantanea (<38 KB). |
| **WotLK Classic / Cata Classic** | WeakAuras 5.x (Blizzard) | ⚠️ **Parziale** | Struttura importabile, ma richiede adattamento delle funzioni Lua del Combat Log (`CombatLogGetCurrentEventInfo`). |
| **Retail (The War Within)** | WeakAuras 5.x | ❌ **Non Compatibile** | Meccaniche e incantesimi del Mago completamente differenti (*Heating Up* nativo, rotazione diversa). |

---

## 🧪 Validazione & Test Suite

Il progetto include una suite di 10 test automatici deterministici eseguibili in parallelo per sfruttare al massimo tutti i core della CPU:

```bash
# Esegui l'intera suite di test in parallelo (Multi-Core ProcessPoolExecutor)
python tests/run_parallel_tests.py

# In alternativa, esegui i test standard via unittest
python -m unittest discover tests

# Per ricompilare la stringa di importazione dopo qualsiasi modifica al builder:
python generate.py
```

---

## 📄 Licenza

Distribuito sotto licenza **MIT**. Consulta il file per ulteriori dettagli.  
Repository: [Glacyal/Fire-Mage-3.3.5a-AM](https://github.com/Glacyal/Fire-Mage-3.3.5a-AM)
