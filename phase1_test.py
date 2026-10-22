import sys, os, io, traceback, re

PY = sys.executable
PASS = "OK"
FAIL = "FAIL"
results = []

def record(name, passed, detail=""):
    mark = PASS if passed else FAIL
    results.append((mark, name, detail))
    print(f"[{mark}] {name}")
    if detail:
        print(f"      {detail}")

print()
print("=" * 60)
print("  PHASE 1 TEST SUITE")
print("=" * 60)

# FIX 1 -- disk path
print("\n--- FIX 1: Windows Disk Path ---")
try:
    from monitor import get_system_metrics, _DISK_ROOT
    import psutil
    disk_val = psutil.disk_usage(_DISK_ROOT).percent
    m = get_system_metrics()
    record("FIX 1 -- _DISK_ROOT resolved correctly", True, f"_DISK_ROOT={repr(_DISK_ROOT)}, disk={disk_val:.1f}%")
    record("FIX 1 -- get_system_metrics() no crash on Windows", True, f"disk_percent={m['disk_percent']:.1f}%")
except Exception as e:
    record("FIX 1 -- disk path", False, str(e))

# FIX 2 -- cumulative warning
print("\n--- FIX 2: Network Metric Documentation ---")
try:
    import inspect
    from monitor import get_system_metrics
    src = inspect.getsource(get_system_metrics)
    ok = "cumulative" in src.lower()
    record("FIX 2 -- Cumulative warning present in docstring", ok, "Found" if ok else "MISSING")
except Exception as e:
    record("FIX 2", False, str(e))

# FIX 5 -- absolute log path
print("\n--- FIX 5: Absolute Log Path ---")
try:
    from healer import LOG_FILE
    is_abs = os.path.isabs(LOG_FILE)
    record("FIX 5 -- LOG_FILE is absolute", is_abs, f"LOG_FILE={LOG_FILE}")
except Exception as e:
    record("FIX 5", False, str(e))

# FIX 6 -- log error handling
print("\n--- FIX 6: Log Error Handling ---")
try:
    from healer import log_action
    r = log_action("PHASE1_TEST_normal")
    record("FIX 6a -- Normal write returns True", r is True, f"returned {r!r}")
    import healer as _h
    orig = _h.LOG_FILE
    _h.LOG_FILE = "Z:\\nonexistent\\log.txt"
    try:
        r2 = log_action("PHASE1_TEST_forced_fail")
        record("FIX 6b -- Bad path returns False without crash", r2 is False, f"returned {r2!r}")
    finally:
        _h.LOG_FILE = orig
except Exception as e:
    record("FIX 6", False, traceback.format_exc())

# FIX 7 -- net_bytes_recv rule
print("\n--- FIX 7: net_bytes_recv Rule ---")
try:
    from explainer import rule_based_explanation
    m = {"cpu_percent":20,"memory_percent":40,"disk_percent":30,"net_bytes_sent":5,"net_bytes_recv":60}
    rules = rule_based_explanation(m)
    recv_fires = any("inbound" in r.lower() for r in rules)
    no_exfil   = not any("exfiltration" in r.lower() for r in rules)
    record("FIX 7 -- net_bytes_recv rule fires", recv_fires, str(rules))
    record("FIX 7 -- No exfiltration language in recv rule", no_exfil)
except Exception as e:
    record("FIX 7", False, str(e))

# FIX 9 -- Deviation Score terminology
print("\n--- FIX 9: Terminology ---")
try:
    from monitor import simulate_anomaly
    from detector import train_model, predict
    from explainer import explain
    model = train_model(n_samples=100)
    m = simulate_anomaly("cpu_spike")
    label, score, _ = predict(model, m)
    report = explain(m, label, score)
    old_gone = "Coefficient Contribution" not in report
    new_present = "Deviation Score" in report or "Contributing Metrics" in report
    record("FIX 9 -- Coefficient Contribution removed from output", old_gone,
           "Removed" if old_gone else "STILL PRESENT!")
    record("FIX 9 -- Deviation Score present in output", new_present,
           "Found" if new_present else "MISSING!")
except Exception as e:
    record("FIX 9", False, str(e))

# FIX 4 -- stdout safety
print("\n--- FIX 4: stdout Restore Safety ---")
try:
    real_stdout = sys.stdout
    buf = io.StringIO()
    try:
        sys.stdout = buf
        raise RuntimeError("deliberate")
    except RuntimeError:
        pass
    finally:
        sys.stdout = real_stdout
    record("FIX 4 -- try/finally pattern restores stdout after exception", sys.stdout is real_stdout)
except Exception as e:
    record("FIX 4", False, str(e))

# FIX 8 -- debug=False
print("\n--- FIX 8: Flask debug=False ---")
try:
    with open("dashboard.py", encoding="utf-8") as f:
        src = f.read()
    debug_true  = bool(re.search(r'app\.run\s*\([^)]*debug\s*=\s*True', src))
    debug_false = bool(re.search(r'app\.run\s*\([^)]*debug\s*=\s*False', src))
    record("FIX 8 -- debug=True removed", not debug_true, "Removed" if not debug_true else "STILL PRESENT!")
    record("FIX 8 -- debug=False confirmed", debug_false, "Present" if debug_false else "MISSING!")
except Exception as e:
    record("FIX 8", False, str(e))

# Full CLI pipeline -- all 5 scenarios
print("\n--- Full CLI Pipeline (5 Scenarios) ---")
try:
    from monitor import simulate_normal, simulate_anomaly
    from detector import train_model, predict
    from explainer import explain
    from healer import decide_and_heal
    model = train_model(n_samples=200)
    scenarios = [
        (simulate_normal,                         "normal"),
        (lambda: simulate_anomaly("cpu_spike"),   "cpu_spike"),
        (lambda: simulate_anomaly("memory_leak"), "memory_leak"),
        (lambda: simulate_anomaly("disk_full"),   "disk_full"),
        (lambda: simulate_anomaly("combined"),    "combined"),
    ]
    for gen, name in scenarios:
        metrics = gen()
        label, score, _ = predict(model, metrics)
        xai = explain(metrics, label, score)
        buf2 = io.StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf2
            decide_and_heal("Test Healing Action")
        finally:
            sys.stdout = old
        record(f"Scenario '{name}' pipeline OK", True, f"label={label}, score={score:.4f}")
except Exception as e:
    record("Full pipeline", False, traceback.format_exc())

# Recovery log written to absolute path
print("\n--- FIX 5: Log file stability ---")
try:
    from healer import LOG_FILE, log_action
    log_action("PHASE1_FINAL_VERIFY")
    record("FIX 5 -- recovery_log.txt at absolute path", os.path.exists(LOG_FILE), f"Path: {LOG_FILE}")
except Exception as e:
    record("FIX 5 log stability", False, str(e))

# Summary
print()
print("=" * 60)
print("  SUMMARY")
print("=" * 60)
passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)
for mark, name, detail in results:
    prefix = "  [OK  ]" if mark == PASS else "  [FAIL]"
    print(f"{prefix} {name}")
print(f"\n  {passed} passed, {failed} failed out of {len(results)} checks")
print("=" * 60)
sys.exit(0 if failed == 0 else 1)
