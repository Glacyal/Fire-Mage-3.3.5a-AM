"""
Test del Componente Hot Streak Decoppiato e Persistente
======================================================
Verifica che la barra Hot Streak rispetti i requisiti ingegneristici:
- Separazione netta tra Segment 1 (1° critico binario 0/1) e Proc (buff 10s nativo)
- Presenza dell'evento di trigger FMHUD_HS_UPDATE
- Gestore dinamico degli eventi _G.FMHUD_HandleHSEvent e UnregisterAllEvents
- Assenza di reset su PLAYER_REGEN_ENABLED (uscita combat)
"""
import unittest
from builder.components.hot_streak import (
    build_hotstreak_auras,
    SHARED_HOTSTREAK_CHECK_LUA,
)


class TestHotStreakDecoupled(unittest.TestCase):

    def test_hotstreak_aura_count(self):
        """Verifica che il modulo Hot Streak produca esattamente le 4 aure previste."""
        auras = build_hotstreak_auras()
        self.assertEqual(len(auras), 4)
        ids = [a["id"] for a in auras]
        self.assertIn("10 - Hot Streak Bar", ids)
        self.assertIn("Hot Streak Bar - Background", ids)
        self.assertIn("Hot Streak Bar - Segment 1", ids)
        self.assertIn("Hot Streak Bar - Proc", ids)

    def test_segment1_dimensions_and_position(self):
        """Verifica che la mezza barra sinistra sia esattamente 137x5px a x = -70.5."""
        auras = {a["id"]: a for a in build_hotstreak_auras()}
        seg1 = auras["Hot Streak Bar - Segment 1"]
        self.assertEqual(seg1["width"], 137)
        self.assertEqual(seg1["height"], 5)
        self.assertEqual(seg1["xOffset"], -70.5)
        self.assertEqual(seg1["yOffset"], 0)

    def test_proc_dimensions_and_position(self):
        """Verifica che la mezza barra destra sia esattamente 137x5px a x = +70.5."""
        auras = {a["id"]: a for a in build_hotstreak_auras()}
        proc = auras["Hot Streak Bar - Proc"]
        self.assertEqual(proc["width"], 137)
        self.assertEqual(proc["height"], 5)
        self.assertEqual(proc["xOffset"], 70.5)
        self.assertEqual(proc["yOffset"], 0)
        self.assertEqual(proc["regionType"], "aurabar")

    def test_lua_does_not_reset_on_combat_exit(self):
        """Verifica che non ci sia reset su PLAYER_REGEN_ENABLED nella logica Lua."""
        self.assertNotIn("PLAYER_REGEN_ENABLED", SHARED_HOTSTREAK_CHECK_LUA)

    def test_lua_has_dynamic_event_handler_and_unregister(self):
        """Verifica che ci sia la pulizia forzata degli eventi e l'assegnazione dinamica."""
        self.assertIn("UnregisterAllEvents", SHARED_HOTSTREAK_CHECK_LUA)
        self.assertIn("_G.FMHUD_HandleHSEvent", SHARED_HOTSTREAK_CHECK_LUA)
        self.assertIn("COMBAT_LOG_EVENT_UNFILTERED", SHARED_HOTSTREAK_CHECK_LUA)


if __name__ == "__main__":
    unittest.main()
