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
1. COMBUSTION A SINISTRA DI MANA GEM (STILE TRINKET/MANTELLO):
   - Posizionata nella fila inferiore subito a sinistra di Mana Gem (x = +36, y = -54).
   - Comportamento a 3 stati coerente con Trinket e Mantello:
     * PRONTA: Icona visibile a colori pieni, pronta al cast, senza scritte.
     * ATTIVA: Pixel Glow dorato animato, contatore stack x%d al centro.
     * IN COOLDOWN: Animazione a orologio (radial clock swipe Blizzard) con conto alla rovescia (m:ss o secondi).
     * RITORNO PRONTA: Lo swipe si completa, il glow si spegne e l'icona torna pulita.

2. TUTTI I BUFF NASCOSTI SE > 5 MINUTI (MOLTEN ARMOR, INTELLECT, FOCUS MAGIC):
   - Schermo pulito in raid: se Molten Armor, Arcane Intellect o Focus Magic durano piu' di 5 minuti,
     rimangono COMPLETAMENTE NASCOSTI.
   - Compaiono con countdown a orologio e minuti:secondi (m:ss o %.0fs) SOLO quando mancano <= 5 minuti (300 sec).
   - Se il buff scade o manca del tutto (o Focus Magic non e' stato assegnato a nessuno),
     mostrano l'icona desaturata grigia con avviso rosso "OFF".

3. ENTRAMBI I TRINKET FUNZIONANTI (SLOT 13 E 14) & MANTELLO (SLOT 15):
   - Tracciamento affidabile su entrambi i trinket con riconoscimento automatico proc, ICD (tempo prima del riproc)
     e animazione swipe stile orologio radiale Blizzard.
   - Pixel Glow dorato animato durante il proc attivo.

4. SCORCH / IMPROVED SCORCH:
   - Debuff monitorato nel gruppo procs con swipe a orologio e secondi residui (%p).
   - Allerta con colore rosso quando mancano <= 5s per rinfrescarlo tempestivamente.

5. SCALA AUMENTATA DEL 20% E POSIZIONAMENTO:
   - Master scale impostato a 1.2 (+20% di dimensione).
   - Posizionato a y = -190 (subito sopra le barre delle abilita' del giocatore).
================================================================================
