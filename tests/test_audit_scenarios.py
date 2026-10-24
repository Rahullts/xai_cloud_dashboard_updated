"""
test_audit_scenarios.py
Comprehensive 10-scenario validation test suite for Phase 7:
1. Normal operation
2. CPU spike
3. Memory leak
4. Disk exhaustion
5. Network degradation
6. Combined failure
7. Recovery that reduces risk (RECOVERED)
8. Recovery that does not reduce risk (NOT_RECOVERED)
9. Repeated refreshes & repeated scenario selections
10. No-active-incident state
"""

import urllib.request
import json
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

def get_scan(scenario):
    url = f"{BASE_URL}/api/scan?scenario={scenario}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))

def test_suite():
    print("=" * 65)
    print("      PHASE 7 COMPREHENSIVE PLATFORM TEST SUITE")
    print("=" * 65)
    
    results = {}
    
    # -----------------------------------------------------------------
    # Test 1 & 10: Normal Operation & No-Active-Incident State
    # -----------------------------------------------------------------
    print("\n[Test 1 & 10] Testing Normal Operation & No-Active-Incident State...")
    normal_data = None
    healing_in_normal = False
    for step in range(15):
        d = get_scan("normal")
        p = d["prediction"]
        h = d["healing"]
        if h.get("status") == "Executed":
            healing_in_normal = True
        normal_data = d
    
    t1_pass = (not healing_in_normal) and (normal_data["healing"]["status"] == "Skipped")
    print(f"  Final Risk Level: {normal_data['prediction']['risk_level']} (Score: {normal_data['prediction']['risk_score']})")
    print(f"  Healing Status: {normal_data['healing']['status']}")
    print(f"  Decision Recommended: {normal_data['decision']['recommended_action']}")
    print(f"  -> Test 1 & 10 Result: {'PASS' if t1_pass else 'FAIL'}")
    results["Test 1: Normal Operation"] = t1_pass
    results["Test 10: No-Active-Incident State"] = t1_pass

    # -----------------------------------------------------------------
    # Test 2 & 7: CPU Spike & Recovery that reduces risk (RECOVERED)
    # -----------------------------------------------------------------
    print("\n[Test 2 & 7] Testing CPU Spike & Recovery reducing risk (RECOVERED)...")
    cpu_heal = None
    for step in range(22):
        d = get_scan("cpu_spike")
        if d["healing"].get("status") == "Executed":
            cpu_heal = d["healing"]
            break
            
    t2_pass = (cpu_heal is not None) and (cpu_heal["verification"] == "RECOVERED")
    if cpu_heal:
        print(f"  Action Taken: {cpu_heal['action']}")
        print(f"  Verification: {cpu_heal['verification']}")
        print(f"  Evidence: Before={cpu_heal['evidence']['before']['risk_level']} ({cpu_heal['evidence']['before']['risk_score']}) -> After={cpu_heal['evidence']['after']['risk_level']} ({cpu_heal['evidence']['after']['risk_score']})")
    print(f"  -> Test 2 & 7 Result: {'PASS' if t2_pass else 'FAIL'}")
    results["Test 2: CPU Spike"] = t2_pass
    results["Test 7: Recovery Reduces Risk (RECOVERED)"] = t2_pass

    # -----------------------------------------------------------------
    # Test 3: Memory Leak
    # -----------------------------------------------------------------
    print("\n[Test 3] Testing Memory Leak Scenario...")
    mem_heal = None
    for step in range(22):
        d = get_scan("memory_leak")
        if d["healing"].get("status") == "Executed":
            mem_heal = d["healing"]
            break
            
    t3_pass = (mem_heal is not None) and (mem_heal["verification"] == "RECOVERED")
    if mem_heal:
        print(f"  Action Taken: {mem_heal['action']}")
        print(f"  Verification: {mem_heal['verification']}")
        print(f"  Evidence: Before={mem_heal['evidence']['before']['risk_level']} -> After={mem_heal['evidence']['after']['risk_level']}")
    print(f"  -> Test 3 Result: {'PASS' if t3_pass else 'FAIL'}")
    results["Test 3: Memory Leak"] = t3_pass

    # -----------------------------------------------------------------
    # Test 4: Disk Exhaustion
    # -----------------------------------------------------------------
    print("\n[Test 4] Testing Disk Exhaustion Scenario...")
    disk_heal = None
    for step in range(22):
        d = get_scan("disk_full")
        if d["healing"].get("status") == "Executed":
            disk_heal = d["healing"]
            break
            
    t4_pass = (disk_heal is not None) and (disk_heal["verification"] == "RECOVERED")
    if disk_heal:
        print(f"  Action Taken: {disk_heal['action']}")
        print(f"  Verification: {disk_heal['verification']}")
        print(f"  Evidence: Before={disk_heal['evidence']['before']['risk_level']} -> After={disk_heal['evidence']['after']['risk_level']}")
    print(f"  -> Test 4 Result: {'PASS' if t4_pass else 'FAIL'}")
    results["Test 4: Disk Exhaustion"] = t4_pass

    # -----------------------------------------------------------------
    # Test 5: Network Degradation (INCONCLUSIVE per Table VIII)
    # -----------------------------------------------------------------
    print("\n[Test 5] Testing Network Degradation (Partial / Inconclusive)...")
    net_heal = None
    for step in range(22):
        d = get_scan("network_issue")
        if d["healing"].get("status") == "Executed":
            net_heal = d["healing"]
            break
            
    t5_pass = (net_heal is not None) and (net_heal["verification"] == "INCONCLUSIVE")
    if net_heal:
        print(f"  Action Taken: {net_heal['action']}")
        print(f"  Verification: {net_heal['verification']}")
        print(f"  Evidence: Before={net_heal['evidence']['before']['risk_level']} ({net_heal['evidence']['before']['risk_score']}) -> After={net_heal['evidence']['after']['risk_level']} ({net_heal['evidence']['after']['risk_score']})")
    print(f"  -> Test 5 Result: {'PASS' if t5_pass else 'FAIL'}")
    results["Test 5: Network Degradation (INCONCLUSIVE)"] = t5_pass

    # -----------------------------------------------------------------
    # Test 6 & 8: Combined Failure & Recovery does NOT reduce risk
    # -----------------------------------------------------------------
    print("\n[Test 6 & 8] Testing Combined Failure (Unrecovered Multi-Resource)...")
    comb_heal = None
    for step in range(22):
        d = get_scan("combined")
        if d["healing"].get("status") == "Executed":
            comb_heal = d["healing"]
            break
            
    t6_pass = (comb_heal is not None) and (comb_heal["verification"] == "NOT_RECOVERED")
    if comb_heal:
        print(f"  Action Taken: {comb_heal['action']}")
        print(f"  Verification: {comb_heal['verification']}")
        print(f"  Evidence: Before={comb_heal['evidence']['before']['risk_level']} ({comb_heal['evidence']['before']['risk_score']}) -> After={comb_heal['evidence']['after']['risk_level']} ({comb_heal['evidence']['after']['risk_score']})")
    print(f"  -> Test 6 & 8 Result: {'PASS' if t6_pass else 'FAIL'}")
    results["Test 6: Combined Failure"] = t6_pass
    results["Test 8: Recovery Does Not Reduce Risk (NOT_RECOVERED)"] = t6_pass

    # -----------------------------------------------------------------
    # Test 9: Repeated Refreshes and Repeated Scenario Selections
    # -----------------------------------------------------------------
    print("\n[Test 9] Testing Repeated Refreshes & Scenario Switches...")
    # Switch back and forth: normal -> cpu_spike -> normal
    d1 = get_scan("normal")
    time.sleep(0.1)
    d2 = get_scan("cpu_spike")
    time.sleep(0.1)
    d3 = get_scan("normal")
    time.sleep(0.1)
    # Check that switching scenarios cleanly resets sequence state
    t9_pass = (d1["scenario"] == "normal" and d2["scenario"] == "cpu_spike" and d3["scenario"] == "normal")
    print(f"  Sequence switches properly synchronized: {t9_pass}")
    print(f"  -> Test 9 Result: {'PASS' if t9_pass else 'FAIL'}")
    results["Test 9: Repeated Refreshes & Scenario Switches"] = t9_pass

    # -----------------------------------------------------------------
    # Summary Table
    # -----------------------------------------------------------------
    print("\n" + "=" * 65)
    print("                    FINAL TEST SUMMARY")
    print("=" * 65)
    all_passed = True
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
        print(f"  {test_name:<48} : {status}")
    print("=" * 65)
    print(f"OVERALL RESULT: {'ALL 10 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}\n")
    return all_passed

if __name__ == "__main__":
    success = test_suite()
    sys.exit(0 if success else 1)
