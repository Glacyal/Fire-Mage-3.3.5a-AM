# Fire Mage 3.3.5a AM — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-4.0.0-blue.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![Class](https://img.shields.io/badge/Class-Mage%20(Fire)-red.svg)](https://github.com/Glacyal/FireMageHUD-335)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Glacyal/FireMageHUD-335)

Suite WeakAuras completa, modulare ed elegante per **Mago Fuoco Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).  
Progettata per garantire le massime prestazioni in raid, un tracciamento millimetrico dei proc e un'interfaccia ad altissima ergonomia senza distrazioni visive.

---

## 🌟 Caratteristiche Principali

### 1. Barra Dinamica Hot Streak
- **1° Colpo Critico (50% Sinistra)**: Si illumina la metà sinistra della barra (arancione vivo) al primo critico diretto (*Fireball, Scorch, Fire Blast, Frostfire Bolt, esplosione Living Bomb*) e **resta persistente nel tempo**.
- **Barra Unificata al Proc (A Tutta Larghezza)**: Al secondo critico consecutivo, la barra si unifica in un segmento continuo da 264px con **Pixel Glow dorato** e **conto alla rovescia di 10 secondi**.
- **Reset Istantaneo**: Si azzera al lancio del *Pyroblast!* o alla scadenza del buff.

### 2. Filosofia "Zero Clutter" (Schermo Pulito)
- **Molten Armor & Arcane Intellect**: Completamente **nascosti durante il combattimento** se hanno più di 5 minuti residui. Mostrano lo swipe radiale solo negli ultimi 5 minuti e l'allerta rossa **`OFF`** se scaduti o assenti.
- **Focus Magic Intelligente**: Nascosto fintanto che è attivo su un alleato vivo. Si attiva all'istante con swipe e countdown solo durante il **proc personale di 10 secondi (+3% Crit)**, per poi tornare nascosto. Segnala **`OFF`** se non assegnato o se il compagno muore.

### 3. Pannello Statistiche in Tempo Reale
Monitora costantemente le 4 statistiche chiave del Mago Fuoco, risolvendo automaticamente i conflitti tra buff di raid non cumulabili:
- **SP (Spell Power)**: Valore reale aggiornato con gear, gemme, flask, proc e bonus 2P T8 / T7.
- **Crit %**: Include Molten Armor, talenti, Combustion e debuff boss (+5% Scorch/Winter's Chill e +3% Crusader/Poisoner) senza doppi conteggi.
- **Haste %**: Include rating ed è moltiplicato con Bloodlust (+30%), Totem (+5%), 3% raid, 2P T10 (+12%), Power Infusion e Berserking.
- **Hit %**: Precisione con talenti, Draenei e debuff boss (+3% Misery/Faerie Fire), con indicatore verde **`(Cap)`** al 17%.

### 4. Supporto Adattivo Tier 8 & Tier 10
- **Tier 10 2P (*Pushing the Limit*)**: Compare dinamicamente nella riga dei procs a sinistra di Hot Streak (+12% Haste per 5s con Pixel Glow).
- **Tier 8 2P (*Praxis*)**: Quando si equipaggiano $\ge 2$ pezzi T8, la fila inferiore si allarga automaticamente da 6 a **7 icone simmetriche**, posizionando Praxis al centro esatto con timer dell'ICD.

### 5. Monili End-Game & Utility
- **Database Monili con ICD**: Riconoscimento e timer per *Dislodged Foreign Object* (DFO), *Charred Twilight Scale* (CTS) e mantello con ingegneria.
- **Gemma del Mana**: Tracciamento delle cariche residue, cooldown di 2 minuti e bonus 2P T7 (+225 SP per 15s).
- **Combustion & Mirror Image**: Monitoraggio delle cariche di Combustion e durata Copie con bonus 4P T10.

### 6. Ottimizzazione Estrema (Enterprise-Grade)
- **Engine Lua Single-Threaded**: Il codice WeakAuras è stato ottimizzato per non pesare sul singolo core di WoW. I trigger non necessari sono stati rimossi dall'evento `FRAME_UPDATE`.
- **Throttling a 4Hz**: I controlli periodici (es. buff passivi come le armature) sono eseguiti solo 4 volte al secondo anziché ad ogni frame, riducendo le chiamate all'API del 97%.
- **Zero-Allocation Memory**: Prevenzione del micro-stuttering tramite caching globale delle tabelle (es. slot armatura), evitando l'intervento continuo del Garbage Collector.
- **Supporto Client Multi-Lingua**: Riconoscimento robusto dei buff tramite **Spell ID**, garantendo il perfetto funzionamento su client in italiano, russo, tedesco, ecc.

---

## 🚀 Installazione Rapida (3 Passaggi)

1. **Copia la Stringa**: Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/IMPORT_STRING.txt)** e copia tutto il testo (`Ctrl+A`, poi `Ctrl+C`).
2. **Apri WeakAuras**: In World of Warcraft, digita `/wa` nella chat.
3. **Importa**: Clicca su **Import** (o Importa) in alto a sinistra, incolla con `Ctrl + V` e conferma cliccando su **Update** (oppure Aggiorna, per sovrascrivere correttamente le auree preesistenti).

---

## 🖥️ Simulatore Web Interattivo

Puoi visualizzare e testare l'HUD direttamente nel tuo browser aprendo:
👉 **[`index.html`](file:///d:/0Progetti/Fire%20Mage%203.3.5a%20AM/index.html)**

Il simulatore riproduce in scala 1:1 il layout reale di gioco e consente di simulare:
- **Preset 📸 Foto 1 (Combat)**: Hot Streak attivo, 7 procs, Castbar 1.4s, Mana 38.77%.
- **Preset 📸 Foto 2 (Idle)**: Stato di riposo pulito a 0 procs, senza castbar.
- **Preset 📸 Foto 3 (DFO Cooldown)**: Simulazione ricarica DFO con swipe circolare a 49s.
- **Interattività Completa**: Lancio spell, attivazione/disattivazione armature, gestione cariche gemma e rotazione automatica.

---

## 🧪 Validazione & Test

Il progetto include una suite di test automatici in Python per verificare l'integrità del codice Lua e del simulatore.
Tutti i test possono essere eseguiti in parallelo per sfruttare al massimo il multi-threading del processore:

```bash
# Esegui l'intera suite di test sfruttando tutti i core della CPU (massima velocità)
python tests/run_parallel_tests.py

# In alternativa, puoi eseguire i test singolarmente:
# Validazione interattività e stress test di concorrenza del simulatore web
python tests/test_html_simultaneous.py
python tests/test_showcase.py

# Verifica la sintassi di tutti i moduli Lua
python tests/test_lua.py

# Verifica la struttura dell'albero e le proporzioni geometriche
python tests/test_tree_layout.py
```

Per ricompilare la stringa di importazione dopo aver modificato i moduli:
```bash
python generate_import_string.py
```

---

## 📄 Licenza

Distribuito sotto licenza **MIT**. Consulta il file per ulteriori dettagli.
Repository: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
