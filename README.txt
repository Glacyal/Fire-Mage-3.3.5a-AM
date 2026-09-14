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
1. ENTRAMBI I TRINKET FUNZIONANTI (SLOT 13 E 14) & SWIPE AD OROLOGIO:
   - Risolto il proc mancato sul secondo trinket (Dying Curse + Sundial of the Exiled).
     I trinket sono tracciati in modo 100% indipendente con gestione case-insensitive
     e matching su Spell ID, Item ID e nomi buff 3.3.5a.
   - Caricamento stile orologio Blizzard nativo ("radial clock swipe") abilitato su tutti
     i cooldown, sia durante i procs attivi sia durante il countdown dell'ICD prima del riproc.
   - Fasi del tracciamento:
     * FASE 1 - PROC ATTIVO: Pixel Glow dorato animato, swipe a orologio e secondi residui (9.8s).
     * FASE 2 - ICD (RIPROC COUNTDOWN): Glow spento, swipe a orologio e secondi rimanenti (35, 34...).
     * FASE 3 - READY: Icona pulita, luminosa e pronta al prossimo proc.

2. COMBUSTION ATTIVA-ONLY CON NUMERO DI STACK CENTRATO:
   - L'icona compare SOLO quando Combustion e' attiva. Quando e' in CD o inattiva rimane nascosta.
   - Mostra il numero di cariche/stack rimanenti (3, 2, 1) grande (dim. 18) al centro dell'icona
     con Pixel Glow dorato animato. Si nasconde all'istante al consumo dell'ultima carica.

3. MOLTEN ARMOR E ARCANE INTELLECT NASCOSTI SE > 5 MINUTI:
   - Schermo pulito in raid: se Molten Armor o Intellect durano piu' di 5 minuti, le icone
     rimangono COMPLETAMENTE NASCOSTE.
   - Compaiono con countdown a orologio e minuti:secondi SOLO quando mancano <= 5 minuti.
   - Se il buff scade o manca del tutto, mostrano l'icona grigia con scritta rossa "OFF".

4. SCORCH / IMPROVED SCORCH:
   - Debuff monitorato nel gruppo procs con swipe a orologio e secondi residui (%p).
   - Colora l'icona in rosso quando mancano <= 5s per rinfrescarlo tempestivamente.

5. SCALA AUMENTATA DEL 20% E POSIZIONAMENTO SOPRA LE BARRE:
   - Master scale impostato a 1.2 (+20% di dimensione).
   - Posizionato a y = -190 (subito sopra le barre delle abilita' del giocatore).
================================================================================
