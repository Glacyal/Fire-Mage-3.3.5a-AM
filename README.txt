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
1. PROC TRINKET & MANTELLO CON COUNTDOWN ICD (INTERNAL COOLDOWN):
   - Trinket (Dying Curse, Sundial of the Exiled, DFO, Phylactery, CTS, Flare, Reign, ecc.)
     e Mantello (Lightweave Embroidery) ora hanno un comportamento completo a 3 fasi:
     * FASE 1 - PROC ATTIVO: Pixel Glow dorato animato, swipe circolare e secondi residui (es. 9.8s).
     * FASE 2 - ICD (CONTO ALLA ROVESCIA RIPROC): Appena il proc scade, il glow si spegne e
       l'icona mostra i secondi rimanenti in bianco (35, 34, ...) prima che il proc possa riattivarsi!
     * FASE 3 - READY: Al termine dell'ICD l'icona torna pulita senza testi, pronta a riproccare.
   - Supporto nativo ai buff/spellId 3.3.5a di Dying Curse (60494) e Sundial (60064).

2. MOLTEN ARMOR INTELLIGENTE (TIMER SOLO SE SOTTO I 5 MINUTI):
   - Se Molten Armor ha piu' di 5 minuti residui, l'icona e' pulita senza numeri a schermo.
   - Se scende a 5 minuti o meno (<= 5m), compare il countdown in giallo (es. 4:52, 3:15).
   - Se manca del tutto, l'icona diventa grigia desaturata con scritta "OFF" in rosso.

3. NUOVO MODULO ARCANE INTELLECT / ARCANE BRILLIANCE:
   - Monitora la presenza di Arcane Intellect, Arcane Brilliance, Dalaran Intellect o Fel Intelligence.
   - Posizionato a sinistra sopra Molten Armor (x = -160, y = +22).
   - Stessa logica anti-clutter: pulito se > 5m, countdown se <= 5m, avviso rosso "OFF" se manca.

4. SCORCH / IMPROVED SCORCH:
   - Debuff monitorato nel gruppo procs con secondi residui (%p).
   - Colora l'icona in rosso quando mancano <= 5s per ricordarti di rinfrescarlo sul boss.

5. SCALA AUMENTATA DEL 20% E POSIZIONAMENTO SOPRA LE BARRE:
   - Master scale impostato a 1.2 (+20% di dimensione).
   - Posizionato a y = -190 (subito sopra le barre delle abilita' del giocatore).
================================================================================
