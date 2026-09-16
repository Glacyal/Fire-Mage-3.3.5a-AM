"""
High-Performance Multi-Threaded & Multi-Core Test Runner per Fire Mage 3.3.5a AM.
Sfrutta appieno i core della CPU (multiprocessing / ProcessPoolExecutor) per eseguire
in parallelo tutti gli script di test della suite, riducendo i tempi di esecuzione e
garantendo la totale indipendenza dei processi.
"""

import os
import sys
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configura encoding stdout per terminali Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)

# Elenco dei file di test dedicati
TEST_SCRIPTS = [
    "test_all_utility_cases.py",
    "test_equip_switch.py",
    "test_focus_magic.py",
    "test_lua.py",
    "test_showcase.py",
    "test_stats_panel.py",
    "test_tree_layout.py",
    "test_html_simultaneous.py",
    "test_components_integrity.py",
    "test_hotstreak_decoupled.py",
]

def run_single_test_script(script_name):
    """Esegue un singolo script di test in un processo separato."""
    script_path = os.path.join(TEST_DIR, script_name)
    start_time = time.perf_counter()
    
    cmd = [sys.executable, script_path]
    result = subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    
    elapsed = time.perf_counter() - start_time
    return {
        "script": script_name,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "elapsed": elapsed,
    }

def main():
    cpu_count = os.cpu_count() or 4
    num_workers = min(cpu_count, len(TEST_SCRIPTS))
    
    print("=" * 70)
    print("FIRE MAGE 3.3.5a AM - PARALLEL TEST RUNNER (MULTI-CORE)")
    print(f"CPU Cores Rilevati: {cpu_count} | Worker Paralleli Allocati: {num_workers}")
    print("=" * 70)
    
    wall_start = time.perf_counter()
    results = []
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(run_single_test_script, script): script for script in TEST_SCRIPTS}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
    
    wall_time = time.perf_counter() - wall_start
    
    # Ordina i risultati per nome script per consistenza di visualizzazione
    results.sort(key=lambda x: x["script"])
    
    total_cpu_time = sum(r["elapsed"] for r in results)
    all_passed = True
    
    print("\n--- RISULTATI DEI TEST PARALLELI ---")
    for r in results:
        status_icon = "[OK] PASSED" if r["returncode"] == 0 else "[X] FAILED"
        if r["returncode"] != 0:
            all_passed = False
        print(f"{status_icon} {r['script']:<28} ({r['elapsed']:.3f}s)")
        if r["returncode"] != 0:
            print("   --- STDERR ---")
            print(r["stderr"])
            print("   --- STDOUT ---")
            print(r["stdout"])
    
    speedup = total_cpu_time / wall_time if wall_time > 0 else 1.0
    
    print("=" * 70)
    print(f"Tempo Totale Wall-Clock (Parallelo): {wall_time:.3f}s")
    print(f"Somma Tempi Singoli CPU:            {total_cpu_time:.3f}s")
    print(f"Fattore di Efficienza Multi-Core:    {speedup:.2f}x speedup")
    
    if all_passed:
        print("TUTTI I TEST SONO STATI SUPERATI CON SUCCESSO IN PARALLELO!")
        print("=" * 70)
        return 0
    else:
        print("ALCUNI TEST HANNO RESTITUITO ERRORI.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
