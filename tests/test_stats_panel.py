"""
Test unitario per la risoluzione dei conflitti e calcolo statistiche in raid 3.3.5a:
1. Anti-duplicazione Haste 3%: Swift Retribution (Paladino) vs Improved Moonkin Form (Druido) max 1 volta.
2. Moltiplicatori cumulativi di Haste: Bloodlust (30%), Wrath of Air (5%), 3% Raid, T10 2P (12%), PI, Berserking.
3. Anti-duplicazione Spell Crit +5%: Improved Scorch vs Winter's Chill vs Shadow and Flame max 1 volta.
4. Anti-duplicazione All Crit +3%: Heart of the Crusader vs Master Poisoner vs Totem of Wrath max 1 volta.
5. Anti-duplicazione Hit +3%: Misery vs Improved Faerie Fire max 1 volta.
"""
import unittest

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
        res_both = calculate_stats(rating_haste=0, buffs=["Swift Retribution", "Improved Moonkin Form"], debuffs=[])
        res_one = calculate_stats(rating_haste=0, buffs=["Swift Retribution"], debuffs=[])
        self.assertAlmostEqual(res_both["haste"], 3.0, places=2)
        self.assertAlmostEqual(res_both["haste"], res_one["haste"], places=4)

    def test_haste_all_buffs_stacking(self):
        buffs = ["Bloodlust", "Wrath of Air Totem", "Swift Retribution", "Pushing the Limit"]
        res = calculate_stats(rating_haste=0, buffs=buffs, debuffs=[])
        expected = ((1.30 * 1.05 * 1.03 * 1.12) - 1) * 100
        self.assertAlmostEqual(res["haste"], expected, places=2)

    def test_crit_debuff_anti_conflict(self):
        debuffs = ["Improved Scorch", "Winter's Chill", "Heart of the Crusader", "Master Poisoner"]
        res = calculate_stats(rating_haste=0, buffs=[], debuffs=debuffs)
        self.assertEqual(res["target_crit"], 8.0, "5% + 3% = 8%, nessun doppio conteggio")

    def test_hit_debuff_anti_conflict(self):
        debuffs = ["Misery", "Improved Faerie Fire"]
        res = calculate_stats(rating_haste=0, buffs=[], debuffs=debuffs)
        self.assertEqual(res["target_hit"], 3.0, "Un solo debuff 3% hit conteggiato")

if __name__ == "__main__":
    unittest.main()

