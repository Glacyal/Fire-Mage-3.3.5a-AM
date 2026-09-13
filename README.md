# Fire Mage HUD 3.3.5a — WeakAuras 4.0.0 Suite

Suite WeakAura modulare, professionale e completa per **Mago Fire Livello 80** per World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

> [!IMPORTANT]
> **TUTTI I MODULI SONO RIGOROSAMENTE RAGGRUPPATI E NATIVI!**  
> L'intero pacchetto è compilato per l'engine di WeakAuras 4.0.0 (`internalVersion = 52`):
> - **Layout Ottimizzato per Raid**: posizionato nella tasca centrale pulita (`yOffset = -150`) sopra le action bar, lasciando liberi il modello 3D del personaggio, le meccaniche del boss, i raid frames a sinistra e l'Omen threat meter a destra.
> - **Mana Bar Essenziale**: mostra **esclusivamente** la percentuale con 2 decimali (es. `85.24%`).
> - **Focus Magic Intelligente**: monitora in tempo reale tutto il Raid (1-40), Party (1-4), Target e Focus. Quando Focus Magic è applicato ad un alleato, l'avviso grigio `OFF` **scompare** completamente. Se il proc da critico (+3% spell crit) si attiva sul Mago, mostra l'icona attiva con conto alla rovescia.
> - **Gemma del Mana (Mana Gem)**: integrata nella riga utility (`x = +51, y = -48`); monitora il cooldown di 2 minuti (`%p`) e le cariche rimanenti in borsa (`%c`, con `0` rosso se assente o terminata).
> - Se vuoi spostare o eliminare l'intera suite, basta fare clic destro su **`Fire Mage HUD`** $\rightarrow$ **`Delete children and group`**.

---

## Come Aggiornare in Gioco (30 Secondi)

1. In `/wa`, fai clic destro su **`Fire Mage HUD`** e seleziona **`Delete children and group`** per rimuovere la vecchia versione.
2. Apri il file **[`IMPORT_STRING.txt`](file:///d:/0Progetti/FireMageHUD-335/IMPORT_STRING.txt)** e copia tutto il contenuto (`Ctrl+A`, `Ctrl+C`).
3. Entra in gioco su WoW 3.3.5a e apri WeakAuras:
   ```text
   /wa
   ```
4. Clicca su **Import** in alto a sinistra.
5. Incolla la stringa con `Ctrl+V` nel campo di testo.
6. Clicca sul pulsante rosso **Import Group**.
7. Chiudi WeakAuras (`Esc` o la `X` in alto).
8. Fatto! La nuova suite sarà subito attiva e funzionante.

---

## Albero dei Moduli in WeakAuras (`/wa`)

```text
Fire Mage HUD (Gruppo Master - yOffset = -150, posizionato sopra le action bar)
│
├── 01 - Procs (Dynamic Group orizzontale - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona + Timer + Glow Pixel all'attivazione)
│   ├── Living Bomb (Icona + Timer debuff sul Target)
│   ├── Ignite (Icona + Timer debuff sul Target)
│   ├── Combustion (Icona intelligente con Cooldown Progress)
│   └── Molten Fury (Icona attiva solo con Target HP <= 35%)
│
├── 02 - Molten Armor (Ala Sinistra HUD - Monitor Permanente x = -155)
│   ├── Molten Armor - Active (Icona attiva con timer dei minuti residui)
│   └── Molten Armor - OFF (Icona desaturata grigia con indicazione OFF se assente)
│
├── 04 - Focus Magic (Ala Destra HUD - Monitor Permanente x = +155)
│   ├── Focus Magic - Active (Icona attiva con timer del proc crit %p)
│   └── Focus Magic - OFF (Icona grigia OFF quando non assegnato a nessuno;
│                          SCOMPARE non appena applicato ad un alleato in raid/party)
│
├── 05 - Trinket 1 (Icona Slot 13: Fila centrata sotto la Mana Bar, x = -51)
├── 05 - Trinket 2 (Icona Slot 14: Fila centrata sotto la Mana Bar, x = -17)
├── 06 - Cloak (Icona Slot 15: Fila centrata sotto la Mana Bar, x = +17)
├── 06 - Mana Gem (Gemma del Mana: Cooldown %p + Cariche residue, x = +51)
│
├── 07 - Mana Bar (Progress Bar: SOLO % con due cifre decimali, es. 85.24%)
├── 08 - Castbar (Progress Bar: Cast standard, Channeling, Icona spell e Tempo)
├── 09 - GCD (Barra sottile orizzontale tra Castbar e Mana Bar)
│
└── 10 - Alerts (Gruppo Alert Visivi ad alto impatto)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!" al centro dello schermo)
```

---

## Controllo Versione (Git)

Il progetto è versionato con Git ed è sincronizzato sulla repository remota privata di GitHub:
- **Repository Remota**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
- **File tracciati**: codice sorgente (`Core.lua`, `Config.lua`, `FireMageHUD.toc`, `modules/`), script compilatore (`generate_import_string.py`), stringa WeakAura (`IMPORT_STRING.txt`) e manuali (`README.*`, `HANDOFF.md`).
