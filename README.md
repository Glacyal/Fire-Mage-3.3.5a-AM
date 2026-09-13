# Fire Mage HUD 3.3.5a — WeakAuras 4.0.0 Suite

Suite WeakAura modulare, professionale e completa per **Mago Fire Livello 80** per World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

> [!IMPORTANT]
> **TUTTI I MODULI SONO RIGOROSAMENTE RAGGRUPPATI E NATIVI!**  
> L'intero pacchetto è compilato per l'engine di WeakAuras 4.0.0 (`internalVersion = 52`):
> - La **Castbar** compare solo quando lanci magie e mostra icona, nome e tempo residuo.
> - **Molten Armor** mostra subito lo stato attivo (timer) o mancante (allarme rosso lampeggiante).
> - La **Mana Bar** mostra percentuale e valori numerici aggiornati in tempo reale.
> - **Hot Streak** si illumina al doppio critico e fa scattare l'Alert centrale a schermo.
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
Fire Mage HUD (Gruppo Master - Contiene TUTTI i componenti)
│
├── 01 - Procs (Dynamic Group orizzontale - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona + Timer + Glow Pixel all'attivazione)
│   ├── Living Bomb (Icona + Timer debuff sul Target)
│   ├── Ignite (Icona + Timer debuff sul Target)
│   ├── Combustion (Icona intelligente con Cooldown Progress)
│   └── Molten Fury (Icona attiva solo con Target HP <= 35%)
│
├── 02 - Molten Armor (Ala Sinistra HUD - Monitor Permanente)
│   ├── Molten Armor - Active (Icona attiva con timer dei minuti residui)
│   └── Molten Armor - OFF (Icona desaturata grigia con indicazione OFF)
│
├── 03 - Target (Aura Text: Nome Target, % HP e Valori salute - Centrato sotto HUD)
│
├── 04 - Focus Magic (Ala Destra HUD - Monitor Permanente, simmetrico a Molten Armor)
│   ├── Focus Magic - Active (Icona attiva con timer del proc crit o durata residua)
│   └── Focus Magic - OFF (Icona desaturata grigia con indicazione OFF se non applicato)
│
├── 05 - Trinket 1 (Icona Slot 13: Fila centrata sotto la Mana Bar)
├── 05 - Trinket 2 (Icona Slot 14: Fila centrata sotto la Mana Bar)
├── 06 - Cloak (Icona Slot 15: Fila centrata sotto la Mana Bar)
│
├── 07 - Mana Bar (Progress Bar: % e Valori correnti sotto il GCD)
├── 08 - Castbar (Progress Bar: Cast standard, Channeling, Icona spell e Tempo)
├── 09 - GCD (Barra sottile orizzontale tra Castbar e Mana Bar)
│
└── 10 - Alerts (Gruppo Alert Visivi ad alto impatto)
    └── Alert - Hot Streak ("HOT STREAK! / PYROBLAST READY!" al centro dello schermo)
```

---

## Verifica Immediata in Gioco

1. **Castbar**: Fuori dal cast la barra è invisibile. Lancia una *Fireball* o canalizza *Evocation*: la barra compare all'istante con icona, nome e conto alla rovescia.
2. **Molten Armor**: Clicca con il tasto destro sull'icona del buff di Molten Armor in alto a destra dello schermo di WoW per rimuoverla. L'indicatore a sinistra della HUD passa immediatamente allo stato rosso lampeggiante `OFF!`.
3. **Mana Bar**: Mostra percentuale e valori numerici aggiornati in tempo reale.
4. **Combattimento su Dummy**: Applica *Living Bomb* per vedere il countdown dei 12 secondi; fai critici fino al proc di *Hot Streak* per vederlo brillare e far scattare l'alert a schermo.

---

## Controllo Versione (Git)

Il progetto è versionato con Git ed è sincronizzato sulla repository remota privata di GitHub:
- **Repository Remota**: [Glacyal/FireMageHUD-335](https://github.com/Glacyal/FireMageHUD-335)
- **Branch**: `main`
- **File tracciati**: codice sorgente (`Core.lua`, `Config.lua`, `FireMageHUD.toc`, `modules/`), script compilatore (`generate_import_string.py`), stringa WeakAura (`IMPORT_STRING.txt`) e manuali (`README.*`, `HANDOFF.md`).
- **File ignorati**: cache Python (`__pycache__`), artefatti di sistema e directory IDE via [`.gitignore`](file:///d:/0Progetti/FireMageHUD-335/.gitignore).

### Comandi Rapidi per il Push
Per sincronizzare le future modifiche su GitHub:
```bash
git add .
git commit -m "descrizione della modifica"
git push
```
