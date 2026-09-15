"""
Test unitario per la logica anti-clutter di Focus Magic:
1. Senza buff: icona attiva NASCOSTA, icona OFF VISIBILE con avviso rosso.
2. Applicato su alleato (e vivo): TUTTO NASCOSTO (HUD 100% pulito).
3. Proc 10s attivo sul Mago: icona VISIBILE con countdown swipe 10s.
4. Fine proc 10s: torna automaticamente NASCOSTA se l'alleato ha ancora il buff.
5. Alleato morto o buff scaduto: compare immediatamente l'icona OFF.
"""
import unittest

def simulate_fm_logic(now, cast_time, has_self_proc, proc_rem, ally_dead=False):
    state_expires = cast_time + 1800 if (cast_time is not None and not ally_dead) else 0
    self_rem = proc_rem if has_self_proc else 0
    self_dur = 10
    self_exp = now + self_rem if has_self_proc else 0

    ally_active = (state_expires > now) and not ally_dead

    active_trigger = (self_rem > 0.05)
    off_trigger = (not active_trigger) and (not ally_active)

    if active_trigger and self_rem > 0:
        if self_rem <= 3:
            custom_text = f"|cFFFF4444{self_rem:.1f}s|r"
        else:
            custom_text = f"{int(self_rem)}s"
        duration = (self_dur, self_exp)
    else:
        custom_text = ""
        duration = (0, 0)

    return {
        "active_trigger": active_trigger,
        "off_trigger": off_trigger,
        "self_rem": self_rem,
        "ally_active": ally_active,
        "custom_text": custom_text,
        "duration": duration,
    }

class TestFocusMagic(unittest.TestCase):
    def test_unbuffed_shows_off_only(self):
        res = simulate_fm_logic(now=100, cast_time=None, has_self_proc=False, proc_rem=0)
        self.assertFalse(res["active_trigger"], "Active must be hidden when unbuffed")
        self.assertTrue(res["off_trigger"], "OFF must be shown when unbuffed")

    def test_applied_to_ally_hides_both(self):
        res = simulate_fm_logic(now=100, cast_time=0, has_self_proc=False, proc_rem=0)
        self.assertFalse(res["active_trigger"], "Active must be hidden when ally is buffed")
        self.assertFalse(res["off_trigger"], "OFF must be hidden when ally is buffed (clean HUD)")

    def test_proc_10s_shows_countdown(self):
        res = simulate_fm_logic(now=100, cast_time=0, has_self_proc=True, proc_rem=9.4)
        self.assertTrue(res["active_trigger"], "Active must show during 10s proc")
        self.assertFalse(res["off_trigger"], "OFF must be hidden during proc")
        self.assertEqual(res["custom_text"], "9s")

    def test_proc_ends_ally_alive_returns_to_hidden(self):
        res = simulate_fm_logic(now=110, cast_time=0, has_self_proc=False, proc_rem=0)
        self.assertFalse(res["active_trigger"], "Active must hide when proc ends")
        self.assertFalse(res["off_trigger"], "OFF must stay hidden while ally is still buffed")

    def test_ally_dies_returns_to_off(self):
        res = simulate_fm_logic(now=150, cast_time=0, has_self_proc=False, proc_rem=0, ally_dead=True)
        self.assertFalse(res["active_trigger"])
        self.assertTrue(res["off_trigger"], "OFF must show when ally dies")

if __name__ == "__main__":
    unittest.main()

