================================================================================
FIRE MAGE 3.3.5a AM — WEAKAURAS 4.0.0 SUITE COMPLETA (WotLK Build 12340)
================================================================================

GUIDA RAPIDA DI INSTALLAZIONE E AGGIORNAMENTO IN GIOCO:
--------------------------------------------------------------------------------
1. Apri il file IMPORT_STRING.txt e copia tutto il testo (Ctrl+A, poi Ctrl+C).
   (Nota: la versione precedente e' salvata nel file IMPORT_STRINGOLD.txt).
2. In World of Warcraft, apri WeakAuras digitando in chat:
   /wa
3. Clicca sul pulsante "Import" in alto a sinistra.
4. Incolla il testo con Ctrl+V.
5. Scegli la modalita' di importazione:
   - "Update Auras" (o "Upgrade"): aggiorna la suite preservando le tue impostazioni.
   - "Replace": se vuoi una reinstallazione pulita che ripristini le posizioni base.
6. Chiudi WeakAuras premendo Esc. Fire Mage 3.3.5a AM e' pronto all'uso!

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

2. GESTIONE DINAMICA TIER 8 & TIER 10 (Praxis +350 SP & Frostforged Sage / Haste 12%):
   - Auto-Rilevamento Intelligente Multi-Stadio: controlla continuamente i pezzi
     T8 Kirin Tor (10m/25m) e T10 Bloodmage (251/264/277), con fallback su tooltip e buff.
   - Le 4 Modalita' Dinamiche:
     * Scenario A: Entrambi T8 (>= 2P) e T10 (>= 2P) equipaggiati contemporaneamente.
       Tutti gli 8 moduli compattati a 26x26 px con passo ~33px (totale 256px).
       T8 a x = -16, T10 a x = +16 (sempre a sinistra della Gemma), Gemma a x = +49.
     * Scenario B: Solo T8 (>= 2P), no T10 (< 2P).
       Icone a 28px con passo 38px (totale 256px). T10 nascosto, T8 al centro a x = 0.
     * Scenario C: Solo T10 (>= 2P), no T8 (< 2P).
       Icone a 28px con passo 38px (totale 256px). T8 nascosto, T10 al centro a x = 0
       (sempre a sinistra della Gemma), Gemma a destra a x = +38.
     * Scenario D: Ne' T8 ne' T10 (< 2P entrambi).
       Icone a 28px con passo 44px (totale 248px). Configurazione simmetrica classica a 6 icone.
   - Meccanica Proc & Glow:
     * T8 Praxis (64868): Pixel Glow dorato per 15s, poi ricarica ICD 30s a orologio.
     * T10 Frostforged/Limit (70753/72416): Pixel Glow ciano/ghiaccio per 5s/10s.

3. BUFF A LUNGA DURATA NASCOSTI SE > 5 MINUTI (Molten Armor, Intellect, Focus Magic):
   - Invisibili > 5 min: per la massima pulizia dello schermo durante i boss fight.
   - Conto alla rovescia <= 5 min: compaiono con swipe orologio e timer colorato
     (giallo > 60s, rosso <= 60s) solo quando mancano 5 minuti o meno.
   - Allerta OFF: se il buff manca del tutto o e' scaduto, mostra l'icona grigia
     desaturata con avviso rosso "OFF".
   - Tracking Intelligente Focus Magic: riconosce l'alleato buffato in raid e,
     quando il mago riceve il proc da critico di 10s, estende la durata del buff
     a 30 minuti prevenendo falsi allarmi OFF senza dover ritarghettare l'alleato.

4. PANNELLO STATISTICHE IN TEMPO REALE (Sotto i 3 Buff a x = -180, y = -54):
   - SP: Spell Power Fuoco in tempo reale (include gear, proc, buff, pozioni).
   - Crit: Spell Crit Fuoco (include Molten Armor + glifo, talenti, stack di
     Combustion +10% a carica, e debuff boss +5% Scorch / +3% Totem).
   - Haste: Spell Haste con rating e moltiplicatori raid (Bloodlust, Totem, Moonkin).
   - Hit: Spell Hit con rating, talenti, Draenei e debuff boss (+3% Misery/Faerie Fire),
     con indicatore verde "(Cap)" al raggiungimento della soglia del 17%.

5. ENGINE UNIVERSALE PER TRINKET (SLOT 13 E 14) E MANTELLO (SLOT 15):
   - Database integrato con oltre 40 monili WotLK (DFO, Filatterio, CTS, ecc.).
   - Riconoscimento automatico On-Use e proc passivi con Internal Cooldown (ICD).
   - Pixel Glow dorato durante il proc attivo, seguito dallo swipe a orologio
     e conto alla rovescia del tempo prima del prossimo riproc.
   - Fallback euristico: stima automatica anche per monili non catalogati.

6. GEMMA DEL MANA CON BONUS 2 PEZZI T7 (y = -54):
   - All'uso attiva il proc T7 (+225 SP per 15s) commutando l'icona sul simbolo
     di Mana Surge con Pixel Glow dorato e countdown decimale a sud (%.1fs).
   - Al termine del buff, torna alla gemma mostrando il cooldown di 2 minuti.
   - Cariche residue mostrate in alto a destra (%c, con "0" rosso se esaurite).

7. CLUSTER CENTRALE ERGONOMICO (Larghezza 264px):
   - Castbar (y = +8): icona spell a sinistra, nome spell, tempo residuo a destra.
   - GCD (y = -4): barra bianca sottile per il Global Cooldown.
   - Mana Bar (y = -15): percentuale con 2 decimali (es. 85.24%), rossa se <= 20%.
   - Hot Streak Bar (y = -25): 264x7px a scomparsa dinamica.

8. FILA UTILITY INFERIORE DINAMICA (y = -54):
   - Scenario A [8 Icone Compattate a 26px] (T8 >= 2P e T10 >= 2P):
     Trinket 1 (-115) | Trinket 2 (-82) | Mantello (-49) | T8 Praxis (-16) | T10 Pushing the Limit (+16) | Gemma (+49) | Combustione (+82) | Copie (+115)
   - Scenario B [7 Icone a 28px] (Solo T8 >= 2P, no T10):
     Trinket 1 (-114) | Trinket 2 (-76) | Mantello (-38) | Tier 8 (0) | Gemma (+38) | Combustione (+76) | Copie (+114)
   - Scenario C [7 Icone a 28px] (Solo T10 >= 2P, no T8):
     Trinket 1 (-114) | Trinket 2 (-76) | Mantello (-38) | T10 Pushing the Limit (0) | Gemma (+38) | Combustione (+76) | Copie (+114)
   - Scenario D [6 Icone Standard a 28px] (Ne' T8 ne' T10):
     Trinket 1 (-110) | Trinket 2 (-66) | Mantello (-22) | Gemma (+22) | Combustione (+66) | Copie (+110)

9. PROCS & DEBUFF CON TIMER ROSSI IN SCADENZA (y = +52):
   - Timer in rosso vivo negli ultimi secondi: Scorch <= 5s, Hot Streak <= 3s,
     Living Bomb <= 3s prima del boom, Ignite <= 1.5s, Clearcasting <= 4s.

================================================================================
Repository GitHub: https://github.com/Glacyal/FireMageHUD-335 (Branch: main)
================================================================================
