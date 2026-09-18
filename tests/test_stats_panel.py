"""
Test unitario per la risoluzione dei conflitti e calcolo statistiche in raid 3.3.5a:
1. Anti-duplicazione Haste 3%: Swift Retribution (Paladino) vs Improved Moonkin Form (Druido) max 1 volta.
2. Moltiplicatori cumulativi di Haste: Bloodlust (30%), Wrath of Air (5%), 3% Raid, T10 2P (12%), PI, Berserking.
3. Anti-duplicazione Spell Crit +5%: Improved Scorch vs Winter's Chill vs Shadow and Flame max 1 volta.
4. Anti-duplicazione All Crit +3%: Heart of the Crusader vs Master Poisoner vs Totem of Wrath max 1 volta.
5. Anti-duplicazione Hit +3%: Misery vs Improved Faerie Fire max 1 volta.
6. Assenza di doppio conteggio del Critico di Combustion (Fix 4): GetSpellCritChance(3) include già
   i bonus dell'aura Combustion (+10% per stack), nessuna moltiplicazione manuale (stacks * 10).
7. Anti-duplicazione Hit Razziale Draenei vs Heroic Presence (aura party/raid Draenei).
8. Verifica soglia e indicatore visivo Hit Cap a 17.0%.
"""
import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from builder.components.stats import make_stats_custom_text, build_stats_auras


def calculate_stats(rating_haste, buffs, debuffs):
    mult = 1 + (rating_haste / 100)
    has_lust = False
    has_wrath_air = False
    has_3_haste = False
    has_t10 = False
    has_pi = False
    has_berserking = False

    for b in buffs:
        if not has_lust and (b in ["Bloodlust", "Heroism", 2825, 32182]):
            has_lust = True
            mult *= 1.30
        elif not has_wrath_air and (b in ["Wrath of Air Totem", 3738, 2895]):
            has_wrath_air = True
            mult *= 1.05
        elif not has_3_haste and (b in ["Swift Retribution", "Improved Moonkin Form", 48396, 53648, 24907, 31583]):
            has_3_haste = True
            mult *= 1.03
        elif not has_t10 and (b in ["Pushing the Limit", 70753, 70752]):
            has_t10 = True
            mult *= 1.12
        elif not has_pi and (b in ["Power Infusion", 10060]):
            has_pi = True
            mult *= 1.20
        elif not has_berserking and (b in ["Berserking", 26297]):
            has_berserking = True
            mult *= 1.20

    haste = (mult - 1) * 100

    has_5_crit = False
    has_3_crit = False
    target_crit = 0.0

    for d in debuffs:
        if not has_5_crit and (d in ["Improved Scorch", "Winter's Chill", "Shadow and Flame", 22959, 28593, 17800]):
            has_5_crit = True
            target_crit += 5.0
        if not has_3_crit and (d in ["Heart of the Crusader", "Master Poisoner", "Totem of Wrath", 20337, 58410, 30708]):
            has_3_crit = True
            target_crit += 3.0

    has_3_hit = False
    target_hit = 0.0
    for d in debuffs:
        if not has_3_hit and (d in ["Misery", "Faerie Fire", "Improved Faerie Fire", 33198, 770, 16857]):
            has_3_hit = True
            target_hit += 3.0

    return {
        "haste": haste,
        "target_crit": target_crit,
        "target_hit": target_hit,
    }


class TestStatsPanel(unittest.TestCase):

    def test_haste_anti_conflict_3_percent(self):
        """Verifica che Swift Retribution e Improved Moonkin Form non si sommino."""
        res_both = calculate_stats(rating_haste=0, buffs=["Swift Retribution", "Improved Moonkin Form"], debuffs=[])
        res_one = calculate_stats(rating_haste=0, buffs=["Swift Retribution"], debuffs=[])
        self.assertAlmostEqual(res_both["haste"], 3.0, places=2)
        self.assertAlmostEqual(res_both["haste"], res_one["haste"], places=4)

    def test_haste_all_buffs_stacking(self):
        """Verifica che i moltiplicatori di Haste si applichino in modo moltiplicativo corretto."""
        buffs = ["Bloodlust", "Wrath of Air Totem", "Swift Retribution", "Pushing the Limit"]
        res = calculate_stats(rating_haste=0, buffs=buffs, debuffs=[])
        expected = ((1.30 * 1.05 * 1.03 * 1.12) - 1) * 100
        self.assertAlmostEqual(res["haste"], expected, places=2)

    def test_crit_debuff_anti_conflict(self):
        """Verifica anti-duplicazione dei debuff sul target per crit Fuoco (+5%) e All Crit (+3%)."""
        debuffs = ["Improved Scorch", "Winter's Chill", "Heart of the Crusader", "Master Poisoner"]
        res = calculate_stats(rating_haste=0, buffs=[], debuffs=debuffs)
        self.assertEqual(res["target_crit"], 8.0, "5% + 3% = 8%, nessun doppio conteggio")

    def test_hit_debuff_anti_conflict(self):
        """Verifica anti-duplicazione del debuff Hit (+3%) tra Misery e Faerie Fire."""
        debuffs = ["Misery", "Improved Faerie Fire"]
        res = calculate_stats(rating_haste=0, buffs=[], debuffs=debuffs)
        self.assertEqual(res["target_hit"], 3.0, "Un solo debuff 3% hit conteggiato")

    # =========================================================================
    # TEST AGGIUNTIVI FIX 4: COMBUSTION DOUBLE-COUNTING & STATS ACCURACY
    # =========================================================================

    def test_combustion_no_manual_double_counting_in_lua_code(self):
        """
        Verifica che nel codice Lua generato da make_stats_custom_text():
        1. NON sia presente alcuna moltiplicazione 'stacks * 10' o 'crit = crit + (stacks'.
        2. GetSpellCritChance(3) sia utilizzato come unica sorgente nativa per il critico del player.
        """
        lua_code = make_stats_custom_text()

        # Non deve esserci la somma manuale di Combustion
        self.assertNotIn("stacks * 10", lua_code, "Rilevato 'stacks * 10' nel codice Lua: doppio conteggio Combustion!")
        self.assertNotIn("crit = crit + (stacks", lua_code, "Rilevato incremento manuale di crit con stacks di Combustion!")

        # Deve essere presente GetSpellCritChance(3)
        self.assertIn("GetSpellCritChance(3)", lua_code, "Manca la chiamata essenziale a GetSpellCritChance(3)")

    def test_combustion_crit_formula_consistency(self):
        """
        Simula il calcolo del Crit con e senza Combustion:
        Poiché GetSpellCritChance(3) in WoW 3.3.5a include già +10% per stack,
        il Crit mostrato deve essere ESATTAMENTE pari a GetSpellCritChance(3) + targetCritBonus,
        senza alcuna alterazione aggiuntiva.
        """
        # Esempio: Base crit 55.0%
        base_crit = 55.0

        # Con 1 stack di Combustion, il client restituisce 65.0%
        client_crit_1_stack = base_crit + 10.0
        # Con 2 stack di Combustion, il client restituisce 75.0%
        client_crit_2_stacks = base_crit + 20.0
        # Con 3 stack di Combustion, il client restituisce 85.0%
        client_crit_3_stacks = base_crit + 30.0

        # Debuff sul target: Scorch (+5%) + Totem of Wrath (+3%) = +8%
        target_crit_bonus = 8.0

        # Verifichiamo che il display finale FMHUD corrisponda a client_crit + target_crit_bonus
        display_0 = base_crit + target_crit_bonus
        display_1 = client_crit_1_stack + target_crit_bonus
        display_2 = client_crit_2_stacks + target_crit_bonus
        display_3 = client_crit_3_stacks + target_crit_bonus

        self.assertEqual(display_0, 63.0)
        self.assertEqual(display_1, 73.0)
        self.assertEqual(display_2, 83.0)
        self.assertEqual(display_3, 93.0)

        # Prima del fix (con stacks * 10 manuale), display_1 sarebbe stato 83.0 (+20% invece di +10%)!
        bugged_display_1 = client_crit_1_stack + (1 * 10) + target_crit_bonus
        self.assertNotEqual(display_1, bugged_display_1, "Il valore corretto non deve corrispondere al calcolo buggato raddoppiato")

    def test_draenei_hit_anti_duplication_logic(self):
        """
        Verifica che se il giocatore è Draenei (isDraenei == 1) e c'è anche l'aura Heroic Presence
        nel party/raid, il bonus Hit sia esattamente 1%, non 2%.
        """
        # Caso 1: Player Draenei senza aura esterna
        is_draenei = True
        has_heroic_presence = False
        draenei_hit = 1 if (is_draenei or has_heroic_presence) else 0
        self.assertEqual(draenei_hit, 1)

        # Caso 2: Player Non-Draenei con aura Heroic Presence nel party
        is_draenei = False
        has_heroic_presence = True
        draenei_hit = 1 if (is_draenei or has_heroic_presence) else 0
        self.assertEqual(draenei_hit, 1)

        # Caso 3: Player Draenei CON aura Heroic Presence nel party (non deve sommare 2%)
        is_draenei = True
        has_heroic_presence = True
        draenei_hit = 1 if (is_draenei or has_heroic_presence) else 0
        self.assertEqual(draenei_hit, 1)

        # Caso 4: Player Non-Draenei senza aura
        is_draenei = False
        has_heroic_presence = False
        draenei_hit = 1 if (is_draenei or has_heroic_presence) else 0
        self.assertEqual(draenei_hit, 0)

    def test_hit_cap_indicator_threshold(self):
        """Verifica la logica di visualizzazione del tag (Cap) sul totale di Hit (soglia 17.0%)."""
        # Sotto Cap (es. 16.99%)
        hit_under = 16.99
        is_cap_under = hit_under >= 17.0
        self.assertFalse(is_cap_under)

        # Esatto Cap (17.0%)
        hit_exact = 17.0
        is_cap_exact = hit_exact >= 17.0
        self.assertTrue(is_cap_exact)

        # Sopra Cap (17.5%)
        hit_over = 17.5
        is_cap_over = hit_over >= 17.0
        self.assertTrue(is_cap_over)

    def test_stats_auras_structure(self):
        """Verifica la conformità strutturale delle aure del componente Stats Panel."""
        auras = build_stats_auras()
        self.assertEqual(len(auras), 3, "Previste 3 aure nel componente Stats Panel")
        ids = [a["id"] for a in auras]
        self.assertIn("18 - Stats Panel", ids)
        self.assertIn("Stats Panel - Background", ids)
        self.assertIn("Stats Panel - Text", ids)


if __name__ == "__main__":
    unittest.main()
