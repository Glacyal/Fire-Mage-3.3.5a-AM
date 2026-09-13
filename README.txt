================================================================================
FIRE MAGE HUD 3.3.5a — WEAKAURAS 4.0.0 SUITE COMPLETA (WotLK Build 12340)
================================================================================

ISTRUZIONI DI AGGIORNAMENTO IN GIOCO (MOLTO IMPORTANTE):
--------------------------------------------------------------------------------
1. In gioco, apri WeakAuras digitando:
   /wa
2. Clicca con il tasto destro su "Fire Mage HUD" e seleziona:
   "Delete children and group"
   (IMPORTANTE: se non cancelli il vecchio gruppo, WeakAuras fonde i moduli
    mantenendo attive le vecchie icone e le vecchie posizioni che si sovrappongono!)
3. Apri il file IMPORT_STRING.txt e copia tutto il testo (Ctrl+A, poi Ctrl+C).
4. In WeakAuras, clicca su "Import" (in alto a sinistra).
5. Incolla il testo con Ctrl+V.
6. Clicca sul pulsante rosso "Import Group".
7. Chiudi WeakAuras con Esc. Fatto!

--------------------------------------------------------------------------------
NOVITA' PRINCIPALI:
--------------------------------------------------------------------------------
1. RILEVAMENTO ATTIVO PROC TRINKET & MANTELLO (PIXEL GLOW):
   - Trinket passivi da caster (DFO, Phylactery, CTS, Flare, Reign, Sundial, Dying Curse, ecc.)
     e l'incantamento Mantello di Sartoria (Lightweave Embroidery) ora vengono monitorati
     in tempo reale.
   - Quando il proc si attiva:
     * L'icona si accende con un vivace PIXEL GLOW dorato animato attorno al bordo!
     * Mostra lo swipe circolare e il countdown numerico dei secondi residui (es. 14.2s).
   - Quando il proc termina:
     * Il glow si spegne e l'icona torna a mostrare l'oggetto equipaggiato pulito.
   - Per gli oggetti On-Use (es. paracadute ingegneria, trinket attivi):
     * Mostra il cooldown rimanente durante il tempo di ricarica.

2. GEOMETRIA A ZERO SOVRAPPOSIZIONI (ZERO-OVERLAP LAYOUT):
   - Castbar (y = 0, largh. 220): Rimossa icona esterna a sinistra ("icon": False).
     Testo spell all'interno a sinistra, tempo a destra.
   - Ali laterali pulite:
     * Molten Armor a x = -160, y = -7 (ben 33 pixel di spazio libero dalla Castbar!).
     * Focus Magic a x = +160, y = -7 (ben 33 pixel di spazio libero dalla Castbar!).
   - Mana Bar (y = -23, largh. 220): Mostra esclusivamente la percentuale con 2 decimali (85.24%).
   - Fila Utility (y = -54):
     * 10 pixel di spazio libero sotto la barra del mana.
     * Icone 28x28 a x = -60, -20, +20, +60 (12 pixel di spazio libero tra ogni icona).
   - Gemma del Mana (x = +60, y = -54): Cooldown centrato, cariche residue in alto a destra.
   - Riga Proc (y = +44): 17 pixel di spazio libero sopra la castbar.
   - Alert Hot Streak (y = +105): 19 pixel di spazio libero sopra i proc.
================================================================================
