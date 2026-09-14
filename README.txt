================================================================================
FIRE MAGE HUD 3.3.5a — WEAKAURAS 4.0.0 SUITE COMPLETA (WotLK Build 12340)
================================================================================

GUIDA RAPIDA DI INSTALLAZIONE E AGGIORNAMENTO IN GIOCO:
--------------------------------------------------------------------------------
1. Apri il file IMPORT_STRING.txt e copia tutto il testo (Ctrl+A, poi Ctrl+C).
2. In World of Warcraft, apri WeakAuras digitando in chat:
   /wa
3. Clicca sul pulsante "Import" in alto a sinistra.
4. Incolla il testo con Ctrl+V.
5. Scegli la modalità di importazione:
   - "Update Auras" (o "Upgrade"): aggiorna l'HUD preservando le tue preferenze.
   - "Replace": se vuoi una reinstallazione pulita che ripristini le posizioni base.
6. Chiudi WeakAuras premendo Esc. L'HUD e' pronto all'uso!

--------------------------------------------------------------------------------
PANORAMICA DELLE FUNZIONALITA' E DEL LAYOUT:
--------------------------------------------------------------------------------

1. BARRA HOT STREAK DINAMICA (Sotto la Barra del Mana a y = -25):
   - 1° Critico Non-Periodico: illumina esattamente meta' barretta a sinistra
     (50%, 130x5px) di colore arancione vivo e RESTA PERSISTENTE nel tempo.
     I DoT periodici (Ignite, tick Living Bomb) non azzerano la serie.
   - 2° Critico Consecutivo (Hot Streak Proc): la meta' barretta sparisce e
     i due segmenti DIVENTANO UN'UNICA BARRA CONTINUA DA 264px a tutta larghezza!
     Attiva il Pixel Glow dorato/arancio e avvia il conto alla rovescia di 10s
     del buff con scorrimento orologio (radial swipe) in tempo reale.
   - Lancio di Pyroblast (o fine 10s): consuma l'effetto e azzera subito la barra.
   - Zero Testo: design puramente visivo, pulito e minimale.

2. BUFF A LUNGA DURATA NASCOSTI SE > 5 MINUTI (Molten Armor, Intellect, Focus Magic):
   - Invisibili > 5 min: per la massima pulizia dello schermo durante i boss fight.
   - Conto alla rovescia <= 5 min: compaiono con swipe orologio e timer colorato
     (giallo > 60s, rosso <= 60s) solo quando mancano 5 minuti o meno.
   - Allerta OFF: se il buff manca del tutto o e' scaduto, mostra l'icona grigia
     desaturata con avviso rosso "OFF".
   - Tracking Intelligente Focus Magic: riconosce l'alleato buffato in raid e,
     quando il mago riceve il proc da critico di 10s, estende la durata del buff
     a 30 minuti prevenendo falsi allarmi OFF senza dover ritarghettare l'alleato.

3. PANNELLO STATISTICHE IN TEMPO REALE (Sotto i 3 Buff a x = -180, y = -54):
   - SP: Spell Power Fuoco in tempo reale (include gear, proc, buff, pozioni).
   - Crit: Spell Crit Fuoco (include Molten Armor + glifo, talenti, stack di
     Combustion +10% a carica, e debuff boss +5% Scorch / +3% Totem).
   - Haste: Spell Haste con rating e moltiplicatori raid (Bloodlust, Totem, Moonkin).
   - Hit: Spell Hit con rating, talenti, Draenei e debuff boss (+3% Misery/Faerie Fire),
     con indicatore verde "(Cap)" al raggiungimento della soglia del 17%.

4. ENGINE UNIVERSALE PER TRINKET (SLOT 13 E 14) E MANTELLO (SLOT 15):
   - Database integrato con oltre 40 monili WotLK (DFO, Filatterio, CTS, ecc.).
   - Riconoscimento automatico On-Use e proc passivi con Internal Cooldown (ICD).
   - Pixel Glow dorato durante il proc attivo, seguito dallo swipe a orologio
     e conto alla rovescia del tempo prima del prossimo riproc.
   - Fallback euristico: stima automatica anche per monili non catalogati.

5. GEMMA DEL MANA CON BONUS 2 PEZZI T7 (x = +22, y = -54):
   - All'uso attiva il proc T7 (+225 SP per 15s) commutando l'icona sul simbolo
     di Mana Surge con Pixel Glow dorato e countdown decimale a sud (%.1fs).
   - Al termine del buff, torna alla gemma mostrando il cooldown di 2 minuti.
   - Cariche residue mostrate in alto a destra (%c, con "0" rosso se esaurite).

6. CLUSTER CENTRALE ERGONOMICO (Larghezza 264px):
   - Castbar (y = +8): icona spell a sinistra, nome spell, tempo residuo a destra.
   - GCD (y = -4): barra bianca sottile per il Global Cooldown.
   - Mana Bar (y = -15): percentuale con 2 decimali (es. 85.24%), rossa se <= 20%.
   - Hot Streak Bar (y = -25): 264x7px a scomparsa dinamica.

7. FILA UTILITY INFERIORE (y = -54, 6 icone 28x28 centrate sotto la barra):
   - Trinket 1 (x = -110) | Trinket 2 (x = -66) | Mantello (x = -22)
   - Mana Gem  (x =  +22) | Combustion (x = +66) | Copie   (x = +110)

8. PROCS & DEBUFF CON TIMER ROSSI IN SCADENZA (y = +52):
   - Timer in rosso vivo negli ultimi secondi: Scorch <= 5s, Hot Streak <= 3s,
     Living Bomb <= 3s prima del boom, Ignite <= 1.5s, Clearcasting <= 4s.

================================================================================
Repository GitHub: https://github.com/Glacyal/FireMageHUD-335 (Branch: main)
================================================================================
