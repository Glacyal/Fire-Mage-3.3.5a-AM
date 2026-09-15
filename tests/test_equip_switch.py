"""
Test unitario per la transizione dinamica della riga utility (6 vs 7 icone).
Simula il comportamento di _G.FMHUD_UpdateUtilityRowPositions al cambio di equipaggiamento:
- Solo T7 (6 icone)
- T7 + T8 (7 icone)
- Solo T8 (7 icone)
- T8 + T10 (7 icone)
- Solo T10 (6 icone)
"""
import unittest

T8_SET_IDS = {
    45367, 45369, 45365, 45366, 45368,
    45357, 45359, 45355, 45356, 45358
}

LAYOUT_T8 = {
    "Trinket 1": -114, "Trinket 2": -76, "Cloak": -38,
    "Tier 8": 0, "Mana Gem": 38, "Combustion": 76, "Mirror Image": 114
}

LAYOUT_STD = {
    "Trinket 1": -110, "Trinket 2": -66, "Cloak": -22,
    "Mana Gem": 22, "Combustion": 66, "Mirror Image": 110
}

def simulate_check_t8(equipped_items, active_buffs):
    if 64868 in active_buffs or "Praxis" in active_buffs:
        return True
    count = sum(1 for item in equipped_items if item in T8_SET_IDS)
    return count >= 2

def get_layout(has_t8):
    return LAYOUT_T8 if has_t8 else LAYOUT_STD

class TestDynamicEquipSwitch(unittest.TestCase):
    def test_scenarios(self):
        # Scenario 1: Solo T7 (0 pezzi T8) -> 6 icone
        t7_items = [39491, 39492, 40416, 40417]
        self.assertFalse(simulate_check_t8(t7_items, []))
        self.assertEqual(get_layout(False), LAYOUT_STD)
        self.assertEqual(len(get_layout(False)), 6)

        # Scenario 2: T7 misto a T8 (2 pezzi T8 + 2 pezzi T7) -> 7 icone
        t7_t8_items = [45357, 45359, 40416, 40417]
        self.assertTrue(simulate_check_t8(t7_t8_items, []))
        self.assertEqual(get_layout(True), LAYOUT_T8)
        self.assertEqual(len(get_layout(True)), 7)

        # Scenario 3: Solo T8 (4 pezzi T8) -> 7 icone
        solo_t8_items = [45357, 45359, 45355, 45356]
        self.assertTrue(simulate_check_t8(solo_t8_items, []))
        self.assertEqual(get_layout(True), LAYOUT_T8)

        # Scenario 4: T8 misto a T10 (2 pezzi T8 + 2 pezzi T10) -> 7 icone
        t8_t10_items = [45357, 45359, 51283, 51282]
        self.assertTrue(simulate_check_t8(t8_t10_items, []))
        self.assertEqual(get_layout(True), LAYOUT_T8)

        # Scenario 5: Solo T10 (4 pezzi T10, 0 pezzi T8) -> 6 icone
        solo_t10_items = [51284, 51280, 51283, 51282]
        self.assertFalse(simulate_check_t8(solo_t10_items, []))
        self.assertEqual(get_layout(False), LAYOUT_STD)
        self.assertEqual(len(get_layout(False)), 6)

    def test_dynamic_transitions(self):
        gear_states = [
            ([45357, 45359], True),   # Solo T8 -> 7 icone
            ([51284, 51280], False),  # Solo T10 -> 6 icone
            ([45367, 45369], True),   # T7+T8 -> 7 icone
            ([39491, 39492], False),  # Solo T7 -> 6 icone
            ([45357, 45358], True),   # T8+T10 -> 7 icone
            ([51284, 51283], False),  # Solo T10 -> 6 icone
        ]
        for gear, expected in gear_states:
            is_t8 = simulate_check_t8(gear, [])
            self.assertEqual(is_t8, expected)
            layout = get_layout(is_t8)
            self.assertEqual(len(layout), 7 if expected else 6)

if __name__ == "__main__":
    unittest.main()

