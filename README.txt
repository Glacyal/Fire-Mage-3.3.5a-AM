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
- Reattivita' immediata al combattimento e alle magie (nessun lag o testo fittizio).
- La Castbar compare SOLO quando lanci magie e mostra icona, nome e tempo residuo.
- Molten Armor mostra subito lo stato attivo (timer) o mancante (allarme rosso).
- Mana Bar dinamica con percentuale e valori numerici correnti/massimi.
- Hot Streak si illumina al proc e scatena l'Alert centrale a schermo.
- TUTTI I MODULI SONO RIGOROSAMENTE RAGGRUPPATI dentro "Fire Mage HUD":
  puoi eliminare o spostare tutta la HUD in un colpo solo.

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

Fire Mage HUD (Gruppo Master - Contiene TUTTO il pacchetto)
├── 01 - Procs (Dynamic Group orizzontale - Auto-allineato sopra la Castbar)
│   ├── Hot Streak (Icona + Timer + Glow all'attivazione)
│   ├── Living Bomb (Icona + Timer debuff sul Target)
│   ├── Ignite (Icona + Timer debuff sul Target)
│   ├── Combustion (Icona intelligente con Cooldown Progress)
│   └── Molten Fury (Icona attiva solo con Target HP <= 35%)
│
├── 02 - Molten Armor (Gruppo dedicato - Monitor Permanente)
│   ├── Molten Armor - Active (Icona attiva con timer dei minuti residui)
│   └── Molten Armor - OFF (Icona desaturata + Bordo rosso + WARNING lampeggiante)
│
├── 03 - Target (Aura Text: Nome, % HP e Valori salute formattati)
├── 04 - Focus (Aura Text: Nome, % HP e Valori salute formattati)
│
├── 05 - Trinket 1 (Icona Slot 13: Cooldown Progress automatico)
├── 05 - Trinket 2 (Icona Slot 14: Cooldown Progress automatico)
├── 06 - Cloak (Icona Slot 15: Cooldown Progress automatico)
│
├── 07 - Mana Bar (Progress Bar: % e Valori correnti formattati)
├── 08 - Castbar (Progress Bar: Cast standard, Channeling, Icona e Tempo)
├── 09 - GCD (Barra sottile orizzontale: Monitor Global Cooldown)
│
└── 10 - Alerts (Alert Visivo Hot Streak al centro dello schermo con testo ingrandito)

================================================================================
COME PERSONALIZZARE GLI ELEMENTI IN GIOCO (/wa)
================================================================================

Ogni modulo e' completamente autonomo. Cliccando sulla singola aura in /wa puoi:

- SPOSTARE: Clicca e trascina con il mouse a video o cambia X Offset / Y Offset.
- RIDIMENSIONARE: Modifica Width (Larghezza) e Height (Altezza).
- FONT E TESTI: Scegli il font desiderato, dimensione caratteri e allineamento.
- COLORI: Modifica colore barra, colore sfondo e trasparenza (Alpha).
- NASCONDERE: Puoi disattivare singoli moduli (es. solo Focus o solo GCD)
  cliccando sull'icona a forma di occhio accanto al nome dell'aura.
- ELIMINARE TUTTO IN UN COLPO: Clic destro su "Fire Mage HUD" -> Delete.

================================================================================
DIAGNOSTICA E VERIFICA IN COMBATTIMENTO
================================================================================

1. Molten Armor:
   - Rimuovi il buff cliccando con il tasto destro sulla sua icona in alto a destra.
     -> Appare subito l'avviso rosso "OFF!" lampeggiante.
   - Rilancia Molten Armor -> Passa all'icona a colori con il conto alla rovescia.
2. Castbar:
   - Fuori dal cast la barra e' invisibile. Appena lanci Fireball o Frostfire Bolt
     la barra si accende con icona, nome e tempo.
3. Mana Bar:
   - Mostra la percentuale e il valore attuale/massimo aggiornati in tempo reale.
4. Manichino da allenamento (Dummy):
   - Living Bomb mostra il countdown dei 12s.
   - Hot Streak compare e si illumina al doppio critico, scatenando l'Alert a video.

================================================================================
CONTROLLO DI VERSIONE (GIT & GITHUB)
================================================================================

Il progetto e' versionato con Git e collegato al repository remoto privato:
https://github.com/Glacyal/FireMageHUD-335

File inclusi nel tracciamento:
- Codice sorgente: Config.lua, Core.lua, FireMageHUD.toc, cartella modules/
- Generatore WA: generate_import_string.py (AceSerializer + LibDeflate WA4)
- Stringa di importazione: IMPORT_STRING.txt
- Documentazione: README.txt, README.md, HANDOFF.md, WEAKAURAS_ONLY_SETUP.md
- Configurazione: .gitignore

Comandi rapidi Git:
  git status                  -> Verifica file modificati o non tracciati
  git log --oneline           -> Cronologia delle versioni e modifiche
  git push                    -> Carica i nuovi commit sul repository GitHub
================================================================================
