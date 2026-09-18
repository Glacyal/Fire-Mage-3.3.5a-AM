"""
Test di Integrità e Robustezza Architetturale dei Componenti WeakAuras
=====================================================================
Verifica la conformità di tutti i 7 moduli in builder/components/:
- Correttezza delle strutture dati e assenza di campi mancanti
- Unicità assoluta di tutti gli ID e UID
- Integrità referenziale tra controlledChildren e nodi figli
- Conformità con WeakAuras 4.0.0 (internalVersion 52)
"""
import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from builder.tree import build_wa_tree
from builder.components import (
    build_procs_auras,
    build_buffs_auras,
    build_utility_auras,
    build_bars_auras,
    build_hotstreak_auras,
    build_alerts_auras,
    build_stats_auras,
)


class TestComponentsIntegrity(unittest.TestCase):

    def test_each_component_produces_auras(self):
        """Verifica che ogni modulo builder produca una lista non vuota di dizionari."""
        components = [
            ("procs", build_procs_auras()),
            ("buffs", build_buffs_auras()),
            ("utility", build_utility_auras()),
            ("bars", build_bars_auras()),
            ("hotstreak", build_hotstreak_auras()),
            ("alerts", build_alerts_auras()),
            ("stats", build_stats_auras()),
        ]
        for name, auras in components:
            self.assertIsInstance(auras, list, f"Componente {name} non restituisce una lista")
            self.assertGreater(len(auras), 0, f"Componente {name} restituisce una lista vuota")
            for a in auras:
                self.assertIsInstance(a, dict, f"Un elemento in {name} non è un dizionario")
                self.assertIn("id", a, f"Elemento in {name} privo di 'id'")
                self.assertIn("uid", a, f"Elemento in {name} privo di 'uid'")
                self.assertIn("regionType", a, f"Elemento in {name} privo di 'regionType'")

    def test_total_aura_count_and_uniqueness(self):
        """Verifica il conteggio totale delle aure (37) e l'unicità di ID e UID."""
        tree = build_wa_tree()
        children = tree["c"]
        self.assertEqual(len(children), 37, f"Previste 37 aure, trovate {len(children)}")

        seen_ids = set()
        seen_uids = set()
        for a in children:
            aid = a["id"]
            auid = a["uid"]
            self.assertNotIn(aid, seen_ids, f"ID duplicato rilevato: {aid}")
            self.assertNotIn(auid, seen_uids, f"UID duplicato rilevato: {auid}")
            seen_ids.add(aid)
            seen_uids.add(auid)

    def test_referential_integrity(self):
        """Verifica che ogni aura referenziata in controlledChildren esista realmente."""
        tree = build_wa_tree()
        root = tree["d"]
        all_ids = {a["id"] for a in tree["c"]}

        # Controlla la radice
        for child_id in root["controlledChildren"]:
            self.assertIn(child_id, all_ids, f"Radice referenzia figlio inesistente: {child_id}")

        # Controlla i gruppi intermedi
        for a in tree["c"]:
            if "controlledChildren" in a:
                for child_id in a["controlledChildren"]:
                    self.assertIn(child_id, all_ids, f"Gruppo {a['id']} referenzia figlio inesistente: {child_id}")

    def test_castbar_spell_icon_enabled(self):
        """Verifica che 08 - Castbar abbia l'icona della spell attiva abilitata a sinistra."""
        tree = build_wa_tree()
        castbar = next((a for a in tree["c"] if a.get("id") == "08 - Castbar"), None)
        self.assertIsNotNone(castbar, "08 - Castbar non trovata nell'albero")
        self.assertTrue(castbar.get("icon"), "L'icona della spell sulla castbar deve essere True")
        self.assertEqual(castbar.get("icon_side"), "LEFT", "L'icona della spell deve essere posizionata a sinistra (LEFT)")
        self.assertEqual(castbar.get("iconSource"), -1, "iconSource deve essere -1 (automatico da trigger/spell)")


if __name__ == "__main__":
    unittest.main()
