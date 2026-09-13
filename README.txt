================================================================================
FIRE MAGE HUD 3.3.5a — WEAKAURAS 4.0.0 SUITE
Guida Operativa e Istruzioni per l'Utente
================================================================================

Questa suite e' una WeakAura completa, modulare e professionale per Mago Fire
Livello 80 su World of Warcraft 3.3.5a (Wrath of the Lich King - Build 12340).

NON E' NECESSARIO COPIARE ALCUN FILE IN Interface\AddOns.
L'intero pacchetto e' contenuto nella stringa di importazione IMPORT_STRING.txt
ed e' pronto all'uso al 100% dentro l'addon WeakAuras.

La suite e' compilata con i prototipi nativi di WeakAuras 4.0.0 (internalVersion 52):
- Ottimizzata specificamente per la visuale da Raid (Ulduar/ICC): posizionata
  nella tasca centrale libera sopra le action bar (yOffset = -150), senza alcuna
  interferenza con i raid frames a sinistra, Omen3 a destra o il modello 3D del pg.
- Mana Bar essenziale: mostra ESCLUSIVAMENTE la percentuale con 2 decimali (es. 85.24%).
- Focus Magic intelligente: scansione automatica di tutto il Raid (1-40), Party (1-4),
  Target e Focus. Se applicato ad un alleato, l'avviso "OFF" scompare completamente;
  quando il proc da critico si attiva sul Mago, mostra l'icona attiva con conto alla rovescia.
- Gemma del Mana (Mana Gem): monitora cooldown (2 min) e cariche residue (3, 2, 1);
  mostra uno "0" rosso di allarme quando esaurita per ricordarti di evocarla.
- TUTTI I MODULI SONO RIGOROSAMENTE RAGGRUPPATI dentro "Fire Mage HUD":
  puoi eliminare o spostare l'intera interfaccia in un colpo solo.

================================================================================
COME PULIRE E IMPORTARE LA WEAKAURA IN GIOCO (30 SECONDI)
================================================================================

1. In gioco, apri WeakAuras:
   /wa
2. Fai clic destro sul vecchio gruppo "Fire Mage HUD" e clicca
   "Delete children and group" per eliminare la vecchia versione.
3. Apri il file IMPORT_STRING.txt nella cartella di questo progetto.
4. Seleziona tutto il testo (Ctrl + A) e copialo (Ctrl + C).
5. In WoW, nella finestra di WeakAuras clicca sul pulsante "Import" in alto.
6. Clicca nella casella di testo e incolla la stringa con Ctrl + V.
7. Clicca sul pulsante rosso "Import Group".
8. Chiudi WeakAuras (tasto Esc o X in alto a destra).
9. Fatto! La suite "Fire Mage HUD" e' subito attiva e perfettamente funzionante.

================================================================================
STRUTTURA DEI MODULI IN WEAKAURAS (/wa)
================================================================================

Fire Mage HUD (Gruppo Master - yOffset = -150 sopra le barre delle azioni)
├── 01 - Procs (Dynamic Group orizzontale - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona + Timer + Glow all'attivazione)
│   ├── Living Bomb (Icona + Timer debuff sul Target)
│   ├── Ignite (Icona + Timer debuff sul Target)
│   ├── Combustion (Icona intelligente con Cooldown Progress)
│   └── Molten Fury (Icona attiva solo con Target HP <= 35%)
│
├── 02 - Molten Armor (Ala Sinistra HUD - Monitor Permanente x = -155)
│   ├── Molten Armor - Active (Icona attiva con timer dei minuti residui)
│   └── Molten Armor - OFF (Icona desaturata grigia con testo OFF se assente)
│
├── 04 - Focus Magic (Ala Destra HUD - Monitor Permanente x = +155)
│   ├── Focus Magic - Active (Icona attiva con timer %p quando il proc e' attivo)
│   └── Focus Magic - OFF (Icona grigia OFF se non assegnato a nessuno;
│                          SCOMPARE non appena applicato ad un alleato in raid/party)
│
├── 05 - Trinket 1 (Icona Slot 13: Fila centrata sotto la Mana Bar, x = -51)
├── 05 - Trinket 2 (Icona Slot 14: Fila centrata sotto la Mana Bar, x = -17)
├── 06 - Cloak (Icona Slot 15: Fila centrata sotto la Mana Bar, x = +17)
├── 06 - Mana Gem (Gemma del Mana: Cooldown %p + Cariche residue, x = +51)
│
├── 07 - Mana Bar (Progress Bar: SOLO % con due cifre decimali, es. 85.24%)
├── 08 - Castbar (Progress Bar: Cast standard, Channeling, Icona e Tempo)
├── 09 - GCD (Barra sottile orizzontale tra Castbar e Mana Bar)
│
└── 10 - Alerts (Alert Visivo Hot Streak sopra i proc con testo ingrandito)

================================================================================
COME PERSONALIZZARE GLI ELEMENTI IN GIOCO (/wa)
================================================================================

Ogni modulo e' completamente autonomo. Cliccando sul gruppo master o sulla singola aura:

- SPOSTARE L'INTERA HUD: Clicca su "Fire Mage HUD" e modifica yOffset (es. -140 o -160)
  oppure trascina l'ancora direttamente a schermo.
- RIDIMENSIONARE: Modifica Width (Larghezza) e Height (Altezza) del singolo modulo.
- FONT E TESTI: Scegli il font desiderato, dimensione caratteri e allineamento.
- COLORI: Modifica colore barra, colore sfondo e trasparenza (Alpha).
- NASCONDERE: Puoi disattivare singoli moduli cliccando sull'icona a forma di occhio.
- ELIMINARE TUTTO IN UN COLPO: Clic destro su "Fire Mage HUD" -> Delete children and group.

================================================================================
DIAGNOSTICA E VERIFICA IN COMBATTIMENTO E IN RAID
================================================================================

1. Focus Magic:
   - Se non lo hai lanciato su nessuno: vedi l'icona grigia "OFF" a destra.
   - Appena lo lanci su un alleato in raid o sul tuo target: l'icona "OFF" SCOMPARE subito.
   - Quando l'alleato fa un critico e ricevi il buff 10s: appare l'icona a colori con %p.
2. Gemma del Mana:
   - Mostra l'icona dello Zaffiro con il numero di cariche in basso a destra (3, 2, 1).
   - Se usi la gemma: parte lo swipe di cooldown circolare e il countdown di 2 minuti.
   - Se hai 0 cariche o non hai gemme: compare uno "0" rosso.
3. Mana Bar:
   - Mostra solo la percentuale con precisione al centesimo (es. 100.00% -> 94.15%).
4. Posizione a Schermo:
   - Perfettamente centrata nello spazio libero tra Grid (raid frames a sinistra)
     e Omen3 (threat meter a destra), appena sopra le action bar inferiori.
