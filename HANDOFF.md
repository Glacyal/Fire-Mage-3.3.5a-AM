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
| **Engine WA4 Specification** | **`internalVersion = 52`**, prototipi nativi `aura2` (con `matchesShowOn`), `unit` (`Cast`, `Power`, `Health`), `spell` e `item` (`Cooldown Progress`). |
| **Sistema di Rendering Testi** | `subRegions` WA4 native (`subbackground`, `subforeground`, `subtext` con font Expressway outline). Evita il fallback ai nomi delle aure. |
| **Formato Stringa WA** | `!WA:1!` (LibDeflate Little-Endian 6-bit + AceSerializer-3.0 Protocol Rev 1, versione 2000 per sub-gruppi nidificati) |
| **Struttura Interna** | **Tutti i 10 moduli sono rigorosamente raggruppati** sotto `Fire Mage HUD`. Eliminabile o spostabile in blocco con un solo clic. |
| **Controllo Versione** | Repository Git collegata a GitHub privato: [`Glacyal/FireMageHUD-335`](https://github.com/Glacyal/FireMageHUD-335) (branch `main`). |

---

## Causa Root dell'Inattività Precedente e Risoluzione

Dall'ispezione di `WTF\Account\...\SavedVariables\WeakAuras.lua` è emerso che:
1. **Mancanza di `internalVersion = 52`**: WeakAuras 4.0.0 ha un modulo di migrazione (`Modernize.lua`). In assenza di `internalVersion`, il client considerava l'aura preistorica (versione < 7) e sostituiva tutti i trigger con un trigger dummy `type = "aura", event = "Health"`, disattivando qualsiasi reattività.
2. **Mancanza di `subRegions`**: In WeakAuras 4, i testi non risiedono più nei campi top-level `displayTextLeft`/`text`, ma nell'array `subRegions`. Senza `subRegions`, WeakAuras mostrava il nome dell'aura (es. `"08 - Castbar"`, `"07 - Mana Bar"`).

**Risoluzione applicata**:
- Compilazione con `internalVersion = 52` su ogni componente.
- Triggers nativi conformi all'engine di WA 4.0.0 (`aura2`, `Cast`, `Power`, `Cooldown Progress`).
- Array `subRegions` strutturato con formattazione `%p`, `%n`, `%1.percentpower%`.

---

## Architettura dei Moduli

```text
Fire Mage HUD (root: group, internalVersion: 52)
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
├── 03 - Target (text: unit characteristics target, centrato a yOffset: -70)
│
├── 04 - Focus Magic (group: ala destra HUD, xOffset: +155, yOffset: 0, Focus Magic Monitor)
│   ├── Focus Magic - Active (icon: aura2 buff "Focus Magic", matchesShowOn: "showOnActive", cooldown timer %p)
│   └── Focus Magic - OFF (icon: aura2 buff "Focus Magic", matchesShowOn: "showOnMissing", desaturate: true)
│
├── 05 - Trinket 1 (icon: item Cooldown Progress slot 13, xOffset: -32, yOffset: -48)
├── 05 - Trinket 2 (icon: item Cooldown Progress slot 14, xOffset: 0, yOffset: -48)
├── 06 - Cloak (icon: item Cooldown Progress slot 15, xOffset: +32, yOffset: -48)
│
├── 07 - Mana Bar (aurabar: unit Power player, yOffset: -26, width: 240, height: 14)
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
Lo script legge i parametri e genera istantaneamente `IMPORT_STRING.txt`.

---

## Gestione Repository Git & GitHub

Il progetto è gestito con Git e sincronizzato su GitHub:
- **Repository Remota**: [`https://github.com/Glacyal/FireMageHUD-335`](https://github.com/Glacyal/FireMageHUD-335) (privata)
- **Branch principale**: `main`
- **Configurazione ignore**: `.gitignore` esclude `__pycache__`, file temporanei e directory di sistema.
- **Workflow modifiche**:
  1. Modifica moduli o parametri in `generate_import_string.py`.
  2. Esecuzione `python generate_import_string.py`.
  3. Verifica sincronizzazione di `README.txt`, `README.md` e `HANDOFF.md`.
  4. `git add .` e commit `git commit -m "..."`.
  5. Sincronizzazione con `git push`.
