"""
Test di Sincronizzazione Stringa di Importazione
================================================
Verifica che IMPORT_STRING.txt sia perfettamente sincronizzato e identico
all'output generato programmaticamente da builder.core e builder.tree.
"""
import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from builder.core import generate_wa_string
from builder.tree import build_wa_tree


class TestStringSync(unittest.TestCase):

    def test_import_string_matches_generator(self):
        """Verifica che IMPORT_STRING.txt corrisponda esattamente alla stringa generata."""
        import_path = os.path.join(ROOT_DIR, "IMPORT_STRING.txt")
        self.assertTrue(os.path.exists(import_path), "IMPORT_STRING.txt deve esistere")

        with open(import_path, "r", encoding="utf-8") as f:
            saved_string = f.read().strip()

        tree = build_wa_tree()
        generated_string = generate_wa_string(tree).strip()

        self.assertEqual(
            saved_string,
            generated_string,
            "IMPORT_STRING.txt non corrisponde all'output di generate.py! Esegui 'python generate.py'."
        )
        self.assertTrue(saved_string.startswith("!WA:1!"), "La stringa deve iniziare con !WA:1!")


if __name__ == "__main__":
    unittest.main()

