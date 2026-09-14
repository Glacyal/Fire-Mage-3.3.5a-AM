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
- **Focus Magic - Active**: Compare esclusivamente se la durata residua è $\le 5$ minuti (300s) con swipe circolare e conto alla rovescia (giallo $> 60$s, rosso $\le 60$s). Se $> 5$m resta completamente nascosta.
- **Focus Magic - OFF**: Mostra l'icona desaturata con scritta rossa "OFF" solo se il buff non è assegnato a nessun alleato o è scaduto.
  - Intercetta in tempo reale Combat Log e `UNIT_SPELLCAST_SUCCEEDED`.
  - Scansiona `player`, `target`, `focus`, `raid1..40`, `party1..4`.
  - **Fix Proc Giocatore**: Quando il Mago riceve il proc da critico di 10s (Spell ID 54648), questo costituisce conferma diretta del buff attivo sull'alleato. La scadenza viene mantenuta a 30 minuti senza essere troncata a 10s, prevenendo la comparsa dello stato "OFF" ed evitando la necessità di ritarghettare l'alleato.

### 3. Gemma del Mana (`06 - Mana Gem`)
- Collocata a `x = +22, y = -54` tra Mantello (`-22`) e Combustion (`+66`).
- **Bonus Set T7 (2 pezzi)**:
  - All'utilizzo della gemma, attiva il buff "Improved Mana Gems" / "Gemme di Mana Migliorate" (+225 Spell Power per 15s).
  - Mostra il Pixel Glow dorato intorno all'icona (come per i monili) e il countdown a 1 decimale (`%.1fs`).
- **Cooldown Oggetto (2 min)**:
  - Al termine del buff T7, interrompe il glow e commuta automaticamente lo swipe e il timer sul cooldown residuo della gemma (Item `33312` Mana Sapphire, `22044` Mana Emerald).
- **Layout Anti-Sovrapposizione**:
  - Timer di scorrimento (`%p`): Ancorato in zona SUD (`INNER_BOTTOM`, giallo durante il proc T7, bianco durante il cooldown).
  - Conteggio cariche (`%c`): Ancorato in ALTO A DESTRA (`INNER_TOPRIGHT`). Mostra uno `"0"` rosso se le cariche sono esaurite o la gemma non è presente in borsa.

### 4. Layout Orizzontale Utility (Sotto la Mana Bar a `y = -54`)
- 6 icone da 28x28 perfettamente simmetriche centrate sotto la Mana Bar (intervallo di 44px):
  - `05 - Trinket 1`: `x = -110` (Slot 13, supporto 40+ trinket WotLK, On-Use e ICD passivi, Pixel Glow su proc)
  - `05 - Trinket 2`: `x =  -66` (Slot 14, 100% simmetrico a Trinket 1 con database identico e fallback)
  - `06 - Cloak`:     `x =  -22` (Slot 15, Lightweave/Darkglow/Swordguard con countdown ICD e swipe)
  - `06 - Mana Gem`:  `x =  +22` (Tra Mantello e Combustion: T7 2pc Glow dorato, timer a sud, cariche in alto a dx)
  - `06 - Combustion`: `x =  +66` (Pixel Glow e stack `xN` quando attiva, swipe su CD)
  - `06 - Mirror Image`: `x = +110` (Copie: 30s attivo con Pixel Glow cyan e swipe, CD 3 min)

### 5. Regola di Caricamento Spec Fire (Load Conditions)
- Nel backport WeakAuras 4.0.0 per 3.3.5a (`WeakAuras.lua` riga 1263), il motore calcola `loadFunc` **esclusivamente sui nodi foglia** (`if data and not data.controlledChildren`). Impostare `load` solo sul gruppo genitore non impediva alle aure figlie prive di `load` di caricarsi.
- Inoltre, `use_exact_spellknown = True` è indispensabile per bypassare il fallback di `WeakAuras.IsSpellKnownForLoad` su `GetSpellInfo(name)`, che restituirebbe true anche per spell non apprese.
- Ora **tutti i 27 elementi** (gruppo radice, sub-gruppi e singole aure foglia) contengono rigorosamente `FIRE_MAGE_LOAD`:
  - `use_class = True` (`class = { single = "MAGE", multi = { MAGE = True } }`)
  - `use_spellknown = True` (`spellknown = 11129` - Combustion)
  - `use_exact_spellknown = True` (controllo C-API esatto su `IsSpellKnown`)

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
├── 06 - Combustion (icon: a sinistra di Mirror Image, stack quando attiva, swipe CD, xOffset: +22, yOffset: -54)
├── 06 - Mirror Image (icon: copie tra Combustion e Gemma, 30s attivo con glow, swipe CD, xOffset: +66, yOffset: -54)
├── 06 - Mana Gem (icon: cariche + swipe CD, xOffset: +110, yOffset: -54)
│
├── 07 - Mana Bar (aurabar: unit Power player, yOffset: -23, width: 264, height: 14, % con 2 decimali, rossa <= 20%)
├── 08 - Castbar (aurabar: unit Cast player con icona a sinistra, yOffset: 0, width: 264, height: 20)
├── 09 - GCD (aurabar: spell Cooldown Progress 61304, yOffset: -12, width: 264, height: 3)
│
└── 10 - Alerts (group: yOffset: +105)
    └── Alert - Hot Streak (text: aura2 buff "Hot Streak", large text expressway outline)
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
