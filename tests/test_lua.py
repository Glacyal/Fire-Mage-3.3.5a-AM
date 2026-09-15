import os
import re
import sys

def strip_lua(code):
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'\[\[.*?\]\]', '""', code, flags=re.DOTALL)
    code = re.sub(r'"(\\.|[^"])*"', '""', code)
    code = re.sub(r"'(\\.|[^'])*'", "''", code)
    return code

def verify_lua(code, name):
    stripped = strip_lua(code)
    tokens = re.findall(r'\b(function|if|do|while|repeat|end|until)\b', stripped)
    depth = 0
    for t in tokens:
        if t in ('function', 'if', 'do', 'while', 'repeat'):
            depth += 1
        elif t in ('end', 'until'):
            depth -= 1
        if depth < 0:
            print(f"[-] Errore di sintassi in {name}: terminatore inatteso '{t}'")
            return False
    if depth != 0:
        print(f"[-] Errore di sintassi in {name}: blocchi non bilanciati (depth = {depth})")
        return False
    return True

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_passed = True

    # 1. Verifica file in modules/
    modules_dir = os.path.join(root_dir, "modules")
    if os.path.exists(modules_dir):
        for fname in sorted(os.listdir(modules_dir)):
            if fname.endswith(".lua"):
                fpath = os.path.join(modules_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                ok = verify_lua(content, f"modules/{fname}")
                if not ok:
                    all_passed = False
                else:
                    print(f"[OK] modules/{fname}")

    # 2. Verifica file di configurazione root se presenti
    for root_lua in ["Config.lua", "Core.lua"]:
        fpath = os.path.join(root_dir, root_lua)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            ok = verify_lua(content, root_lua)
            if not ok:
                all_passed = False
            else:
                print(f"[OK] {root_lua}")

    # 3. Verifica blocchi Lua embedded nella WeakAura
    sys.path.insert(0, root_dir)
    try:
        import generate_import_string
        tree = generate_import_string.build_wa_tree()
        for item in tree.get('c', []):
            for k in ['customText', 'custom']:
                if k in item and isinstance(item[k], str):
                    if not verify_lua(item[k], f"{item.get('id', '')} ({k})"):
                        all_passed = False
        print("[OK] Tutti i blocchi Lua embedded in WeakAuras")
    except Exception as e:
        print(f"[-] Errore durante l'import di generate_import_string: {e}")
        all_passed = False

    if all_passed:
        print("\n=== TUTTI I TEST LUA SONO PASSATI CON SUCCESSO! ===")
        return 0
    else:
        print("\n=== FALLIMENTO: RISCONTRATI ERRORI DI SINTASSI LUA! ===")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())

