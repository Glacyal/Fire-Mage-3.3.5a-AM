# Fire Mage HUD (WoW 3.3.5a) — Handoff Tecnico

Suite WeakAura modulare, ad altissime prestazioni e ad architettura pura per **Mago Fuoco Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).

---

## 1. Architettura di Progetto & Specifiche Piattaforma

| Componente | Specifica / Implementazione | Note Tecniche |
| :--- | :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (*WotLK Build 12340*) | Compatibile con tutti i core emulatore (*TrinityCore, AzerothCore, Mangos*) |
| **Addon Target** | WeakAuras 4.0.0 (Backport WotLK 3.3.5a) | Engine nativo WA4, `internalVersion = 52` |
| **Modalità di Distribuzione** | **WeakAura 100% Pura** (`IMPORT_STRING.txt`) | Importabile con un solo clic. Nessun file esterno o addon obbligatorio |
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
3. **Timer Intelligenti con Allerta Rossa di Scadenza**:
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
  - In WeakAuras 3.3.5a, `COMBAT_LOG_EVENT_UNFILTERED` non viene processato in modo affidabile da trigger di tipo `custom_type: "status"`.
  - È stato inserito un frame invisibile dedicato nativo (`FMHUD_HSFrame`) che si registra direttamente agli eventi del motore di gioco (`COMBAT_LOG_EVENT_UNFILTERED`, `UNIT_AURA`, `UNIT_SPELLCAST_SUCCEEDED`, `PLAYER_REGEN_ENABLED`, `PLAYER_DEAD`, `PLAYER_UNGHOST`, `PLAYER_ENTERING_WORLD`).
  - Parsing multi-offset per garantire compatibilità con tutti i core emulatore (verifica argomenti 9/10 per la spell e argomenti 18/19/20 per il flag `critical` sia booleano `true` che intero `1`).
  - Filtro rigoroso su `SPELL_DAMAGE` diretto: i DoT periodici (*Ignite, tick di Living Bomb*) producono `SPELL_PERIODIC_DAMAGE` e vengono ignorati, preservando lo streak.
  - Al verificarsi di una variazione, il frame invia `WeakAuras.ScanEvents("FMHUD_HS_UPDATE")`.
- **1° Critico**: Illumina esattamente il 50% a sinistra (`width: 130px, xOffset: -66`) e **resta persistente nel tempo** in attesa del colpo successivo.
- **2° Critico Consecutivo (Hot Streak Proc)**:
  - Il segmento al 50% si nasconde e viene attivata la **Barra di Proc unificata a piena larghezza (264x5px a `xOffset: 0`)**!
  - Mostra il **Pixel Glow** dorato/arancione e avvia il conto alla rovescia swipe di 10 secondi del buff Hot Streak (48108).
- **Lancio Pyroblast (o fine 10s)**:
  - Al lancio di Pyroblast istantaneo (`UNIT_SPELLCAST_SUCCEEDED`), la barra si azzera all'istante tornando alla sola cornice di fondo scura.
- **Zero Testo**: Design puramente visuale, privo di testi sovrapposti.

---

### 3.2 Focus Magic Monitor (`04 - Focus Magic`) — Tracking Intelligente

Posizionato a `x = -150, y = -14` (in riga sopra il pannello statistiche).
- **Meccanica WotLK**: Lanciare Focus Magic applica un buff di 30 minuti all'alleato (`caster == "player"`), mentre il Mago riceve il proc da critico di 10s (Spell ID 54648) ogni volta che l'alleato mette a segno un colpo critico.
- **Back-Propagation del Proc**: Quando il Mago riceve il buff di 10s, il sistema riconosce matematicamente che l'alleato ha ancora Focus Magic attivo. La scadenza viene automaticamente mantenuta/estesa a 30 minuti senza clippare a 10s, prevenendo falsi allarmi "OFF" ed evitando la necessità di ritarghettare l'alleato.
- **Scansione Automatica**: Monitora continuamente `target`, `focus`, `party1..4`, `raid1..40`.

---

### 3.3 Gemma del Mana (`06 - Mana Gem`) — Proc Bonus T7 & Cooldown Dinamico

Posizionata a `x = +22, y = -54` nella fila utility (tra Mantello `x = -22` e Combustione `x = +66`).
- **Bonus Set Tier 7 (2 pezzi - "Mana Surge")**:
  - All'uso della gemma attiva il buff "Improved Mana Gems" / "Mana Surge" (+225 Spell Power per 15s, Spell ID 61062).
  - L'icona **commuta dinamicamente sul simbolo di Mana Surge** (`Spell_Arcane_ManaSurge`), accende il **Pixel Glow** dorato e mostra il conto alla rovescia del proc con 1 decimale (`%.1fs`).
- **Cooldown Oggetto (2 minuti)**:
  - Al termine del buff T7, l'icona ritorna allo Zaffiro del Mana (`INV_Misc_Gem_Sapphire_02`), spegne il glow e mostra lo swipe radiale e il timer del cooldown residuo della gemma.
- **Anti-Sovrapposizione Testi**:
  - Timer di scorrimento (`%p`): Ancorato in zona SUD (`INNER_BOTTOM`).
  - Cariche residue (`%c`): Ancorate in ALTO A DESTRA (`INNER_TOPRIGHT`). Mostra "0" rosso se la gemma è esaurita o assente.

---

### 3.4 Trinkets Slot 13 & 14 (`05 - Trinket 1` & `05 - Trinket 2`) — Engine ICD Universale

Posizionati a `x = -110` e `x = -66` a `y = -54`.
- **Database 40+ Trinket WotLK**: Include tutti i monili da caster (*Dislodged Foreign Object, Phylactery of the Nameless Lich, Charred Twilight Scale, Reign of the Dead, Flare of the Heavens, Muradin's Spyglass, Sundial of the Exiled, Nevermelting Ice Crystal*, ecc.).
- **Dual State (On-Use vs Proc Passivo con ICD)**:
  - Rileva gli oggetti On-Use interrogando `GetItemCooldown`.
  - Per i proc passivi, monitora l'applicazione del buff sul giocatore e traccia l'Internal Cooldown (ICD, es. 45s per DFO/CTS, 90s per Filatterio).
  - Mostra il **Pixel Glow** durante i secondi di proc attivo, commutando poi sullo swipe a orologio e countdown del tempo prima del riproc.
- **Fallback Euristico Universale**: Se equipaggi un trinket non presente nel database, il modulo scansiona automaticamente le parole chiave (*spellpower, haste, crit, spell damage*) e applica un tracciamento stimato con ICD predefinito di 45s.

---

### 3.5 Real-Time Stats Panel (`12 - Stats Panel`)

Posizionato a `x = -180, y = -54` (box compatto 88x48px con 4 righe di statistiche aggiornate in tempo reale):
1. **SP (Spell Power)**: `GetSpellBonusDamage(3)` per la scuola Fuoco. Include gear, incantamenti, proc attivi, gemme e pozioni.
2. **Crit (Spell Crit %)**: `GetSpellCritChance(3)` + Molten Armor (con spirito e glifo) + talenti Fire + stack di Combustion (+10% a carica) + debuff boss (+5% da *Improved Scorch/Winter's Chill*, +3% da *Heart of the Crusader/Master Poisoner*). Supporta visualizzazione a 3 cifre (es. `102.50%`).
3. **Haste (Spell Haste %)**: `UnitSpellHaste("player")` combinato con i moltiplicatori di raid attivi (*Bloodlust/Heroism +30%, Wrath of Air Totem +5%, Moonkin/Retri Aura +3%*).
4. **Hit (Spell Hit %)**: Combat rating + Talento Precision (+3%) + Razziale Draenei (+1%) + debuff boss (*Misery / Faerie Fire +3%*). Mostra l'indicatore verde **`(Cap)`** al raggiungimento del 17% (o 14% con debuff).

---

## 4. Architettura Completa dei Moduli (27 Displays WA4)

```text
Fire Mage HUD (root: group, internalVersion: 52, xOffset: 0, yOffset: -190, scale: 1.2, load: Mage + Living Bomb)
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
├── Fila Utility Inferiore (y = -54, margine di 11.5px sotto la Hot Streak Bar - 6 icone 28x28)
│   ├── 05 - Trinket 1    (x = -110: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 05 - Trinket 2    (x =  -66: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Cloak        (x =  -22: Glow attivo + Swipe orologio + Countdown ICD riproc)
│   ├── 06 - Mana Gem     (x =  +22: T7 2pc Glow dorato + Timer a sud %p + CD 2m + Cariche in alto a dx)
│   ├── 06 - Combustion   (x =  +66: Glow attivo + Stacks x%d + Swipe orologio CD)
│   └── 06 - Mirror Image (x = +110: Glow attivo 30s + Swipe orologio CD 3m)
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
5. Chiudi la finestra con `Esc`. Il tuo HUD è pronto all'uso!
