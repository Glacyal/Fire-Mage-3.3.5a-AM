# Fire Mage HUD 3.3.5a — WeakAuras 4.0.0 Suite

Suite WeakAura modulare, professionale e completa per **Mago Fire Livello 80** per World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

> [!IMPORTANT]
> **REGOLE CRUCIALI PER L'IMPORTAZIONE IN WEAKAURAS**:
> In WeakAuras, se importi un gruppo con lo stesso nome senza prima aver cancellato quello vecchio, WeakAuras **fonde (merge)** i moduli invece di sovrascriverli! Questo lasciava le vecchie aure (con le vecchie coordinate o il Target rimosso) visibili in contemporanea.
> **Procedura obbligatoria**: In `/wa`, fai clic destro su **`Fire Mage HUD`** $\rightarrow$ seleziona **`Delete children and group`** $\rightarrow$ solo DOPO incolla la nuova stringa da `IMPORT_STRING.txt`.

---

## Novità di Questo Aggiornamento

1. **Proc Trinket & Mantello con Rilevamento Attivo & Pixel Glow**:
   - I proc passivi dei trinket (DFO *Oggetto Estraneo Dislocato*, Filatterio *Phylactery of the Nameless Lich*, Scaglia *Charred Twilight Scale*, Bagliore *Flare of the Heavens*, Regno dei Morti *Reign of the Dead*, Clessidra, Dying Curse, Runa Abissale, ecc.) e l'incantamento Mantello di Sartoria (*Lightweave Embroidery*) **non mettono in cooldown lo slot di equipaggiamento**, ma applicano un **Buff temporaneo** sul Mago.
   - I moduli **`05 - Trinket 1`**, **`05 - Trinket 2`** e **`06 - Cloak`** ora integrano un trigger status personalizzato con riconoscimento automatico di tutti i trinket caster di WotLK 3.3.5a.
   - **All'attivazione del proc**: l'icona si illumina con un **Pixel Glow dorato animato**, mostra l'icona del proc, attiva lo swipe circolare e visualizza il conto alla rovescia in secondi esatti (`14.2s`).
   - **Quando il proc termina**: il glow si spegne all'istante e l'icona torna pulita mostrando l'oggetto equipaggiato. Se il trinket o il mantello è "On-Use" (es. paracadute ingegneria, trinket attivo), durante il cooldown mostra il countdown dei secondi residui.

2. **Geometria a Zero Sovrapposizioni (Zero-Overlap Layout)**:
   - **Castbar (`08 - Castbar`)**: larghezza 220px, altezza 20px, opzione `icon: False`. Il nome della spell è scritto all'interno a sinistra e il tempo rimanente a destra. Questo elimina definitivamente la collisione laterale con Molten Armor!
   - **Ali Laterali Pulite**:
     - **Molten Armor**: `x = -160, y = -7` (ben **33 pixel di spazio libero** dalla Castbar!).
     - **Focus Magic**: `x = +160, y = -7` (ben **33 pixel di spazio libero** dalla Castbar!).
   - **Cluster Centrale Verticale**:
     - **GCD Bar**: `y = -12`, altezza 3px, agganciata sotto la Castbar.
     - **Mana Bar**: `y = -23`, altezza 14px, testo rigorosamente solo percentuale con 2 decimali (`85.24%`).
   - **Fila Utility (`Trinket 1`, `Trinket 2`, `Cloak`, `Mana Gem`)**:
     - Posizionata a `y = -54` (**10 pixel di spazio libero** sotto la Mana Bar).
     - Icone 28x28 posizionate a `x = -60, -20, +20, +60` (**12 pixel di spazio libero** tra ogni icona).
   - **Gemma del Mana (`06 - Mana Gem`)**: Cooldown `%p` centrato; cariche residue `%c` ancorate in alto a destra (`INNER_TOPRIGHT`) per non scontrarsi mai.
   - **Riga Proc (`01 - Procs`)**: posizionata a `y = +44` (17 pixel sopra la Castbar).
   - **Alert Hot Streak (`10 - Alerts`)**: posizionato a `y = +105` (19 pixel sopra la riga dei proc).

---

## Come Aggiornare in Gioco (30 Secondi)

1. In gioco, digita `/wa`.
2. Fai clic destro su **`Fire Mage HUD`** e seleziona **`Delete children and group`**.
3. Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRING.txt)** e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
4. In `/wa`, clicca su **Import** in alto a sinistra.
5. Incolla la stringa con `Ctrl+V` nel riquadro.
6. Clicca su **Import Group**.
7. Chiudi WeakAuras (`Esc`). Pronto!

---

## Albero dei Moduli in WeakAuras (`/wa`)

```text
Fire Mage HUD (Gruppo Master - yOffset = -150, posizionato sopra le action bar)
│
├── 01 - Procs (Dynamic Group orizzontale, y = +44 - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona + Timer + Glow Pixel all'attivazione)
│   ├── Living Bomb (Icona + Timer debuff sul Target)
│   ├── Ignite (Icona + Timer debuff sul Target)
│   ├── Scorch (Icona Scorch/Improved Scorch + Timer %p + Avviso refresh <= 5s)
│   ├── Combustion (Icona intelligente con Cooldown Progress)
│   └── Molten Fury (Icona attiva solo con Target HP <= 35%)
│
├── 02 - Molten Armor (Ala Sinistra HUD - x = -160, y = -7, 33px di spazio dalla Castbar)
│   ├── Molten Armor - Active (Icona attiva con timer)
│   └── Molten Armor - OFF (Icona desaturata grigia con indicazione OFF se assente)
│
├── 04 - Focus Magic (Ala Destra HUD - x = +160, y = -7, 33px di spazio dalla Castbar)
│   ├── Focus Magic - Active (Icona attiva con timer del proc crit %p)
│   └── Focus Magic - OFF (Icona grigia OFF quando non assegnato a nessuno;
│                          SCOMPARE non appena applicato ad un alleato in raid/party)
│
├── 05 - Trinket 1 (Fila utility y = -54, x = -60: Glow + Timer sul Proc DFO/CTS/Flare o CD On-Use)
├── 05 - Trinket 2 (Fila utility y = -54, x = -20: Glow + Timer sul Proc Phylactery/Reign o CD On-Use)
├── 06 - Cloak (Fila utility y = -54, x = +20: Glow + Timer sul Proc Lightweave Sartoria o Paracadute)
├── 06 - Mana Gem (Fila utility y = -54, x = +60: Cooldown al centro + Cariche in alto a destra)
│
├── 07 - Mana Bar (Progress Bar y = -23: SOLO % con due cifre decimali, es. 85.24%)
├── 08 - Castbar (Progress Bar y = 0: Cast standard, Channeling, Testo spell a sx, Tempo a dx, no icona)
├── 09 - GCD (Barra sottile y = -12 tra Castbar e Mana Bar)
│
└── 10 - Alerts (Gruppo Alert Visivi ad alto impatto y = +105)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!" al centro dello schermo)
```

---

## Controllo Versione (Git)

Il progetto è versionato con Git ed è sincronizzato sulla repository remota privata di GitHub:
- **Repository Remota**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
