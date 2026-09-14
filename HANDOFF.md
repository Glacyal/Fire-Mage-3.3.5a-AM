# Fire Mage HUD (WoW 3.3.5a) — Handoff Tecnico

## Scopo del Documento

Questo file descrive l'architettura tecnica, le invarianti, il formato di serializzazione/compressione per WeakAuras 4.0.0, i dettagli di implementazione dei singoli moduli e i criteri di manutenzione del progetto **Fire Mage HUD 3.3.5a**.
`README.txt` e `README.md` rappresentano i manuali operativi per l'utente finale; questo documento è destinato agli sviluppatori per manutenere, estendere e validare il codice della suite.

---

## Stato Corrente del Progetto

| Componente | Specifica / Stato |
| :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340) |
| **Addon Target** | WeakAuras 4.0.0 (Backport WotLK 3.3.5a) |
| **Modalità di Distribuzione** | **WeakAura 100% pura** importabile tramite stringa (`IMPORT_STRING.txt`). Nessun file richiesto in `Interface\AddOns`. |
| **Engine WA4 Specification** | **`internalVersion = 52`**, prototipi nativi `aura2` (con `matchesShowOn`), `unit` (`Cast`, `Power`), `spell` e `item` (`Cooldown Progress`), custom status trigger. |
| **Sistema di Rendering Testi** | `subRegions` WA4 native (`subbackground`, `subforeground`, `subtext` con font Expressway outline). |
| **Formato Stringa WA** | `!WA:1!` (LibDeflate Little-Endian 6-bit + AceSerializer-3.0 Protocol Rev 1, versione 2000 per sub-gruppi nidificati). |
| **Struttura Interna** | **Tutti i moduli sono rigorosamente raggruppati** sotto `Fire Mage HUD`. Eliminabile o riposizionabile in blocco con un solo clic. |
| **Posizionamento Schermo** | `Fire Mage HUD`: `xOffset = 0, yOffset = -150` (tasca centrale libera sopra le action bar, nessun conflitto con Raid Grid a sinistra né Omen3 a destra). |
| **Controllo Versione** | Repository Git collegata a GitHub privato: [`Glacyal/FireMageHUD-335`](https://github.com/Glacyal/FireMageHUD-335) (branch `main`). |

---

## Dettagli di Implementazione dei Moduli Critici

#### 1. Mana Bar (`07 - Mana Bar`)
- **Visualizzazione**: Esclusivamente la percentuale con 2 decimali (es. `85.24%`).
- **Subtext**: `"%1.percentpower%%"`.
- **Formattatore**: `text_text_format_1.percentpower_format = "Number"`, precisione `2`.
- **Offset**: Riposizionata a `yOffset = -15` (spostata di +8px per far spazio alla nuova Hot Streak Bar).
- I valori grezzi `| cur / max` sono stati rimossi per la massima pulizia visiva in combattimento.

### 2. Barra Hot Streak (`10 - Hot Streak Bar`) — NUOVA
- **Posizionamento**: Collocata a filo sotto la Mana Bar a `yOffset = -25` (spessore 7px, larghezza 264px, metà spessore della barra mana).
- **Comportamento Visivo Dinamico (Unificazione al Proc)**:
  - **1° Critico Diretto (Sinistra, 50% Larghezza)**: Si illumina la metà barretta sinistra (130x5px, arancio fuoco) al primo colpo critico diretto non-periodico (*Fireball, Fire Blast, Scorch, Living Bomb impatto/esplosione, Frostfire Bolt*) e **resta persistente nel tempo**. I danni periodici DoT (*Ignite, Living Bomb tick*) non intaccano la serie. Si azzera solo su colpo diretto non-critico di questi incantesimi o all'uscita dal combattimento.
  - **Hot Streak Proc (Barra Unica a Piena Larghezza 264px)**: Al secondo critico consecutivo (o all'ottenimento del buff Hot Streak 48108), i due segmenti **diventano un'unica barra continua da 264x5px** con Pixel Glow dorato/arancio e timing con conto alla rovescia swipe di 10 secondi!
  - **Consumo con Pyroblast**: Al lancio di Pyroblast (o scadenza dei 10 secondi), la barra si azzera istantaneamente tornando alla sola cornice scura di fondo.
  - **Zero Testo**: Design minimale e pulito, nessun testo o percentuale sulla barra (gestito separatamente dagli alert).

### 3. Focus Magic Monitor (`04 - Focus Magic`)
- In WoW 3.3.5a, lanciare Focus Magic su un alleato posiziona il buff di 30 min sull'alleato (`caster == "player"`), mentre il Mago riceve il buff di 10s solo quando l'alleato esegue un critico.
- **Focus Magic - Active**: Compare esclusivamente se la durata residua è $\le 5$ minuti (300s) con swipe circolare e conto alla rovescia (giallo $> 60$s, rosso $\le 60$s). Se $> 5$m resta completamente nascosta.
- **Focus Magic - OFF**: Mostra l'icona desaturata con scritta rossa "OFF" solo se il buff non è assegnato a nessun alleato o è scaduto.
  - Intercetta in tempo reale Combat Log e `UNIT_SPELLCAST_SUCCEEDED`.
  - Scansiona `player`, `target`, `focus`, `raid1..40`, `party1..4`.
  - **Fix Proc Giocatore**: Quando il Mago riceve il proc da critico di 10s (Spell ID 54648), questo costituisce conferma diretta del buff attivo sull'alleato. La scadenza viene mantenuta a 30 minuti senza essere troncata a 10s, prevenendo la comparsa dello stato "OFF" ed evitando la necessità di ritarghettare l'alleato.

### 4. Gemma del Mana (`06 - Mana Gem`)
- Collocata a `x = +22, y = -54` tra Mantello (`-22`) e Combustion (`+66`).
- **Bonus Set T7 (2 pezzi)**:
  - All'utilizzo della gemma, attiva il buff "Mana Surge" / "Improved Mana Gems" (+225 Spell Power per 15s).
  - **Commutazione Icona Dinamica**: Durante i 15s di proc, l'icona commuta dinamicamente sul simbolo di **Mana Surge** (`Spell_Arcane_ManaSurge`), evidenziata dal Pixel Glow dorato intorno al riquadro e countdown a 1 decimale (`%.1fs`) a sud.
- **Cooldown Oggetto (2 min)**:
  - Al termine del buff T7, l'icona torna allo Zaffiro del Mana (`INV_Misc_Gem_Sapphire_02`), interrompe il glow e commuta automaticamente lo swipe e il timer sul cooldown residuo della gemma (Item `33312` Mana Sapphire, `22044` Mana Emerald).
- **Layout Anti-Sovrapposizione**:
  - Timer di scorrimento (`%p`): Ancorato in zona SUD (`INNER_BOTTOM`, giallo durante il proc T7, bianco durante il cooldown).
  - Conteggio cariche (`%c`): Ancorato in ALTO A DESTRA (`INNER_TOPRIGHT`). Mostra uno `"0"` rosso se le cariche sono esaurite o la gemma non è presente in borsa.

### 5. Layout Orizzontale Utility (Sotto la Hot Streak Bar a `y = -54`)
- 6 icone da 28x28 perfettamente simmetriche centrate sotto la Hot Streak Bar (intervallo di 44px, margine superiore di 11.5px):
  - `05 - Trinket 1`: `x = -110` (Slot 13, supporto 40+ trinket WotLK, On-Use e ICD passivi, Pixel Glow su proc)
  - `05 - Trinket 2`: `x =  -66` (Slot 14, 100% simmetrico a Trinket 1 con database identico e fallback)
  - `06 - Cloak`:     `x =  -22` (Slot 15, Lightweave/Darkglow/Swordguard con countdown ICD e swipe)
  - `06 - Mana Gem`:  `x =  +22` (Tra Mantello e Combustion: T7 2pc Glow dorato, timer a sud, cariche in alto a dx)
  - `06 - Combustion`: `x =  +66` (Pixel Glow e stack `xN` quando attiva, swipe su CD)
  - `06 - Mirror Image`: `x = +110` (Copie: 30s attivo con Pixel Glow cyan e swipe, CD 3 min)

### 6. Ribilanciamento Layout Verticale Anti-Sovrapposizione
- `01 - Procs`: spostata da `y = +44` a **`y = +52`**
- `08 - Castbar`: spostata da `y = 0` a **`y = +8`**
- `09 - GCD`: spostata da `y = -12` a **`y = -4`**
- `07 - Mana Bar`: spostata da `y = -23` a **`y = -15`**
- `10 - Hot Streak Bar`: posizionata a **`y = -25`** (spessore 7px)
- Riga Utility (`y = -54`): invariata, ora gode di un margine perfetto di 11.5px dalla Hot Streak Bar.

---

## Architettura Completa dei Moduli

```text
Fire Mage HUD (root: group, internalVersion: 52, xOffset: 0, yOffset: -190, scale: 1.2)
├── 01 - Procs (dynamicgroup: horizontal, center-aligned, space: 6px, yOffset: +52)
│   ├── Hot Streak (icon: aura2 buff "Hot Streak", matchesShowOn: "showOnActive", subglow pixel)
│   ├── Clearcasting (icon: aura2 buff "Clearcasting" / "Arcane Concentration" 12536, subglow pixel, timer %p)
│   ├── Living Bomb (icon: aura2 debuff "Living Bomb", matchesShowOn: "showOnActive", ownOnly: true)
│   ├── Ignite (icon: aura2 debuff "Ignite", matchesShowOn: "showOnActive", ownOnly: true)
│   ├── Scorch (icon: custom status trigger debuff su target, countdown esatto, alert rosso <=5s)
│   └── Molten Fury (icon: target <= 35% HP attivo, subtext "35%")
│
├── 02 - Molten Armor (group: colonna sinistra HUD, xOffset: -180, yOffset: -14)
├── 03 - Arcane Intellect (group: colonna sinistra HUD, xOffset: -210, yOffset: -14)
├── 04 - Focus Magic (group: colonna sinistra HUD, xOffset: -150, yOffset: -14)
│
├── 05 - Trinket 1 (icon: Slot 13, On-Use CD + ICD passivi, swipe Blizzlike, golden glow, xOffset: -110, yOffset: -54)
├── 05 - Trinket 2 (icon: Slot 14, 100% simmetrico a Trinket 1, xOffset: -66, yOffset: -54)
├── 06 - Cloak (icon: Slot 15 ricamo mantello con ICD, xOffset: -22, yOffset: -54)
├── 06 - Mana Gem (icon: T7 2pc proc glow, timer sud, cariche in alto a dx, xOffset: +22, yOffset: -54)
├── 06 - Combustion (icon: Pixel Glow e stack quando attiva, swipe CD, xOffset: +66, yOffset: -54)
├── 06 - Mirror Image (icon: copie 30s con glow, swipe CD, xOffset: +110, yOffset: -54)
│
├── 07 - Mana Bar (aurabar: unit Power player, yOffset: -15, width: 264, height: 14, % con 2 decimali, rossa <= 20%)
├── 10 - Hot Streak Bar (group: yOffset: -25, width: 264, height: 7, 50% 1° critico -> barra unica 264px al proc)
│   ├── Hot Streak Bar - Background (texture: cornice 264x7px)
│   ├── Hot Streak Bar - Segment 1 (texture: 1° critico persistente, 130x5px, 50% sx, xOffset: -66)
│   └── Hot Streak Bar - Proc (aurabar: proc Hot Streak barra unica 264x5px, countdown 10s con Pixel Glow)
├── 08 - Castbar (aurabar: unit Cast player con icona a sinistra, yOffset: +8, width: 264, height: 20)
├── 09 - GCD (aurabar: spell Cooldown Progress 61304, yOffset: -4, width: 264, height: 3)
│
├── 10 - Alerts (group: yOffset: +105)
│   └── Alert - Hot Streak (text: aura2 buff "Hot Streak", large text expressway outline)
│
└── 12 - Stats Panel (group: xOffset: -180, yOffset: -54, SP, Crit %, Haste %, Hit % con Cap)
```

### 6. Smart Living Bomb Target Assistant (`11 - Smart Living Bomb Assistant`)
- **Posizionamento**: Collocato sul lato destro (`xOffset = +210, yOffset = 0`), modulo interattivo autonomo.
- **Struttura Aurabar**:
  - `Smart Living Bomb - Background`: Cornice semitrasparente 196x132.
  - `Smart Living Bomb - Header`: Intestazione con icona Living Bomb e titolo.
  - `Smart Living Bomb - Bar 1..5`: 5 Aurabar animate indipendenti impilate verticalmente (y: +28, +10, -8, -26, -44).
- **Indicatori di Stato [V] e [X]**:
  - `[V]` (Verde): Bersaglio con Living Bomb già attiva. La barra scorre visualizzando il countdown dei 12 secondi (`12.0s -> 0.0s`), con testo decimale a destra (rosso a `<= 3.0s` prima dell'esplosione).
  - `[X]` (Rosso): Bersaglio privo di Living Bomb. La barra mostra la percentuale di salute (HP %) e la priorità (Verde per Medi 40-70%, Ciano per Alti 70-100%, Rosso per Bassi 0-40%). Il target #1 consigliato è contrassegnato con `!`.
- **Interazione Cliccabile (Click-to-Target)**:
  - Ciascuna barra integra un `SecureActionButtonTemplate`. Fuori dal combat, il click esegue `/targetexact <name>`.
  - In combat, protetto da `if not InCombatLockdown()` per prevenire errori `ADDON_ACTION_BLOCKED`.
  - Mouseover tooltip con riepilogo salute, stato Living Bomb e guida rapida.
- **Rigorosamente Senza Automazione**: Nessun auto-targeting, nessun cast automatico. Assistente decisionale al 100% manuale.
- **Configurabilità In-Gioco**: Sliders interattivi nella scheda *Custom Options* di WeakAuras (`medMin`, `medMax`, `highMax`, `maxEntries`, `onlyInCombat`).

---


## Architettura Completa dei Moduli

```text
Fire Mage HUD (root: group, internalVersion: 52, xOffset: 0, yOffset: -190, scale: 1.2)
├── 01 - Procs (dynamicgroup: horizontal, center-aligned, space: 6px, yOffset: +44)
│   ├── Hot Streak (icon: aura2 buff "Hot Streak", matchesShowOn: "showOnActive", subglow pixel)
│   ├── Clearcasting (icon: aura2 buff "Clearcasting" / "Arcane Concentration" 12536, subglow pixel, timer %p)
│   ├── Living Bomb (icon: aura2 debuff "Living Bomb", matchesShowOn: "showOnActive", ownOnly: true)
│   ├── Ignite (icon: aura2 debuff "Ignite", matchesShowOn: "showOnActive", ownOnly: true)
│   ├── Scorch (icon: custom status trigger debuff su target, countdown esatto, alert rosso <=5s)
│   └── Molten Fury (icon: unit Health target <= 35%, subtext "35%")
│
├── 02 - Molten Armor (group: colonna sinistra HUD, xOffset: -182, yOffset: -18)
│   ├── Molten Armor - Active (icon: compare SOLO se <= 5 min con timer m:ss / ss, nascosto se > 5m)
│   └── Molten Armor - OFF (icon: aura2 buff missing, icona desaturata con avviso rosso "OFF")
│
├── 03 - Arcane Intellect (group: colonna sinistra HUD, xOffset: -182, yOffset: +18)
│   ├── Arcane Intellect - Active (icon: compare SOLO se <= 5 min con timer m:ss / ss, nascosto se > 5m)
│   └── Arcane Intellect - OFF (icon: aura2 buff missing, icona desaturata con avviso rosso "OFF")
│
├── 04 - Focus Magic (group: colonna sinistra HUD, xOffset: -182, yOffset: -54)
│   ├── Focus Magic - Active (icon: compare SOLO se <= 5 min con countdown scadenza se applicato)
│   └── Focus Magic - OFF (custom status trigger: scansione raid/party/target/focus, sparisce se applicato)
│
├── 05 - Trinket 1 (icon: Slot 13, On-Use CD + ICD passivi, swipe Blizzlike, golden glow, xOffset: -110, yOffset: -54)
├── 05 - Trinket 2 (icon: Slot 14, 100% simmetrico a Trinket 1, xOffset: -66, yOffset: -54)
├── 06 - Cloak (icon: Slot 15 ricamo mantello con ICD, xOffset: -22, yOffset: -54)
├── 06 - Mana Gem (icon: T7 2pc proc glow, timer sud, cariche in alto a dx, xOffset: +22, yOffset: -54)
├── 06 - Combustion (icon: Pixel Glow e stack quando attiva, swipe CD, xOffset: +66, yOffset: -54)
├── 06 - Mirror Image (icon: copie 30s con glow, swipe CD, xOffset: +110, yOffset: -54)
│
├── 07 - Mana Bar (aurabar: unit Power player, yOffset: -23, width: 264, height: 14, % con 2 decimali, rossa <= 20%)
├── 08 - Castbar (aurabar: unit Cast player con icona a sinistra, yOffset: 0, width: 264, height: 20)
├── 09 - GCD (aurabar: spell Cooldown Progress 61304, yOffset: -12, width: 264, height: 3)
│
├── 10 - Alerts (group: yOffset: +105)
│   └── Alert - Hot Streak (text: aura2 buff "Hot Streak", large text expressway outline)
│
└── 11 - Smart Living Bomb Assistant (group: xOffset: +210, yOffset: 0, tracker interattivo 196x132)
    ├── Smart Living Bomb - Background (texture: cornice semitrasparente 196x132)
    ├── Smart Living Bomb - Header (text: icona + titolo "SMART LIVING BOMB")
    ├── Smart Living Bomb - Bar 1 (aurabar: [V]/[X], countdown 12s o % HP, click-to-target)
    ├── Smart Living Bomb - Bar 2 (aurabar: [V]/[X], countdown 12s o % HP, click-to-target)
    ├── Smart Living Bomb - Bar 3 (aurabar: [V]/[X], countdown 12s o % HP, click-to-target)
    ├── Smart Living Bomb - Bar 4 (aurabar: [V]/[X], countdown 12s o % HP, click-to-target)
    └── Smart Living Bomb - Bar 5 (aurabar: [V]/[X], countdown 12s o % HP, click-to-target)
```

---

## Modalità di Aggiornamento per l'Utente
- **Metodo A (Update / Upgrade)**: In `/wa` -> Import -> Incolla -> clic su `Update Auras`. Sovrascrive direttamente le aure esistenti mantenendo le impostazioni.
- **Metodo B (Clean Reset)**: In `/wa` -> Clic destro su `Fire Mage HUD` -> `Delete children and group` -> Import -> `Import Group`.

---

## Come Rigenerare la Stringa WeakAuras

```bash
python generate_import_string.py
```
Lo script legge la gerarchia, esegue l'encoding LibDeflate 6-bit e scrive istantaneamente `IMPORT_STRING.txt`.
