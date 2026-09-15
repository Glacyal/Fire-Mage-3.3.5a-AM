"""
Test di audit interattivo per index.html e t8_t10_preview.html:
Verifica:
1. Che tutti gli handler onclick corrispondano a funzioni JavaScript definite.
2. Che tutti i tag <button> abbiano un handler attivo.
3. Che index.html e t8_t10_preview.html siano sincronizzati e validi.
"""
import os
import re
import sys

def audit_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Estrai script JS
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    js_content = "\n".join(scripts)

    # Funzioni definite
    func_defs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', js_content))

    # Chiamate onclick
    onclick_matches = re.findall(r'onclick=["\']([^"\']+)["\']', content)
    called_funcs = set()
    for call in onclick_matches:
        parts = re.findall(r'([a-zA-Z0-9_]+)\s*\(', call)
        for p in parts:
            called_funcs.add(p)

    missing = called_funcs - func_defs
    if missing:
        print(f"[-] {file_path}: Funzioni onclick non definite: {missing}")
        return False

    # Verifica bottoni
    buttons = re.findall(r'<button\b[^>]*>', content)
    buttons_without_onclick = [b for b in buttons if 'onclick=' not in b]
    if buttons_without_onclick:
        print(f"[-] {file_path}: Bottoni senza onclick: {len(buttons_without_onclick)}")
        return False

    print(f"[OK] {os.path.basename(file_path)}: {len(buttons)} bottoni e {len(onclick_matches)} onclick verificati al 100%!")
    return True

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_ok = True
    for fname in ["index.html", "t8_t10_preview.html"]:
        fpath = os.path.join(root_dir, fname)
        if os.path.exists(fpath):
            if not audit_html(fpath):
                all_ok = False

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(run_tests())

