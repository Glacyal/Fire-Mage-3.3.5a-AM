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

### 1. Mana Bar (`07 - Mana Bar`)
- **Visualizzazione**: Esclusivamente la percentuale con 2 decimali (es. `85.24%`).
- **Subtext**: `"%1.percentpower%%"`.
- **Formattatore**: `text_text_format_1.percentpower_format = "Number"`, precisione `2`.
- I valori grezzi `| cur / max` sono stati rimossi per la massima pulizia visiva in combattimento.

### 2. Focus Magic Monitor (`04 - Focus Magic`)
- In WoW 3.3.5a, lanciare Focus Magic su un alleato posiziona il buff di 30 min sull'alleato (`caster == "player"`), mentre il Mago riceve il buff di 10s solo quando l'alleato esegue un critico.
- **Focus Magic - Active**: Trigger nativo `aura2` su `unit = "player"`. Quando il Mago ottiene il buff/proc di 10s, compare l'icona attiva con lo swipe di ricarica e il countdown `%p`.
- **Focus Magic - OFF**: Custom Status Trigger registrato su eventi `UNIT_AURA, PLAYER_TARGET_CHANGED, PLAYER_FOCUS_CHANGED, RAID_ROSTER_UPDATE, PARTY_MEMBERS_CHANGED, PLAYER_ENTERING_WORLD`.
  - Scansiona: `player`, `target`, `focus`, `raid1..40`, `party1..4` cercando l'aura `"Focus Magic"` con `caster == "player"`.
  - Se il buff è presente su qualsiasi alleato o sul giocatore: l'untrigger si attiva e l'avviso grigio "OFF" **scompare completamente**.
  - Se il buff non è applicato a nessuno: il trigger si attiva e mostra l'icona grigia sobria `"OFF"`.

### 3. Gemma del Mana (`06 - Mana Gem`)
- Item: `33312` (Mana Sapphire - Livello 80) e `22044` (Mana Emerald).
- Trigger: `item` -> `Cooldown Progress (Item)` (`genericShowOn = "showAlways"`).
- Testo 1: `%p` per il countdown del cooldown (2 min).
- Testo 2: `%c` in basso a destra per le cariche residue in borsa (`GetItemCount(33312, nil, true)`). Se le cariche sono 0 o la gemma manca, compare uno `"0"` rosso di avvertimento.

### 4. Layout Orizzontale Utility (Sotto la Mana Bar a `y = -48`)
- 4 icone da 26x26 perfettamente simmetriche centrate a `x = 0`:
  - `05 - Trinket 1`: `x = -51` (Slot 13)
  - `05 - Trinket 2`: `x = -17` (Slot 14)
  - `06 - Cloak`: `x = +17` (Slot 15)
  - `06 - Mana Gem`: `x = +51` (Item 33312)

---

## Architettura Completa dei Moduli

```text
Fire Mage HUD (root: group, internalVersion: 52, xOffset: 0, yOffset: -150)
├── 01 - Procs (dynamicgroup: horizontal, center-aligned, space: 5px, yOffset: +36)
│   ├── Hot Streak (icon: aura2 buff "Hot Streak", matchesShowOn: "showOnActive", subglow pixel)
│   ├── Living Bomb (icon: aura2 debuff "Living Bomb", matchesShowOn: "showOnActive", ownOnly: true)
│   ├── Ignite (icon: aura2 debuff "Ignite", matchesShowOn: "showOnActive", ownOnly: true)
│   ├── Combustion (icon: spell Cooldown Progress 11129, genericShowOn: "showAlways")
│   └── Molten Fury (icon: unit Health target <= 35%, subtext "35%")
│
├── 02 - Molten Armor (group: ala sinistra HUD, xOffset: -155, yOffset: 0)
│   ├── Molten Armor - Active (icon: aura2 buff "Molten Armor", matchesShowOn: "showOnActive")
│   └── Molten Armor - OFF (icon: aura2 buff "Molten Armor", matchesShowOn: "showOnMissing", desaturate: true)
│
├── 04 - Focus Magic (group: ala destra HUD, xOffset: +155, yOffset: 0)
│   ├── Focus Magic - Active (icon: aura2 buff "Focus Magic", matchesShowOn: "showOnActive", timer %p)
│   └── Focus Magic - OFF (custom status trigger: scansione raid/party/target/focus, sparisce se applicato)
│
├── 05 - Trinket 1 (icon: item Cooldown Progress slot 13, xOffset: -51, yOffset: -48)
├── 05 - Trinket 2 (icon: item Cooldown Progress slot 14, xOffset: -17, yOffset: -48)
├── 06 - Cloak (icon: item Cooldown Progress slot 15, xOffset: +17, yOffset: -48)
├── 06 - Mana Gem (icon: item Cooldown Progress 33312 + cariche %c, xOffset: +51, yOffset: -48)
│
├── 07 - Mana Bar (aurabar: unit Power player, yOffset: -26, width: 240, height: 14, solo % a 2 decimali)
├── 08 - Castbar (aurabar: unit Cast player, yOffset: 0, width: 240, height: 22)
├── 09 - GCD (aurabar: spell Cooldown Progress 61304, yOffset: -13, width: 240, height: 4)
│
└── 10 - Alerts (group: yOffset: +85)
    └── Alert - Hot Streak (text: aura2 buff "Hot Streak", large text expressway outline)
```

---

## Come Rigenerare la Stringa WeakAuras

```bash
python generate_import_string.py
```
Lo script legge la gerarchia, esegue l'encoding LibDeflate 6-bit e scrive istantaneamente `IMPORT_STRING.txt`.
