# =============================================================
# main.py — Orchestrator
# Ties all modules together: Monitor → Detect → Explain → Heal
# Run this file to see the full pipeline in action.
# =============================================================

import time
from monitor  import simulate_normal, simulate_anomaly
from detector import train_model, predict
from explainer import explain
from healer   import decide_and_heal

DEMO_DELAY = 1.0   # seconds between demo rounds

def run_demo():
    """
    Run a full demo of the self-healing pipeline with 5 scenarios:
      1. Normal state
      2. CPU spike
      3. Memory leak
      4. Disk full
      5. Combined failure
    """
    print("\n" + "★"*55)
    print("  Explainable AI-Based Self-Healing Cloud Application")
    print("★"*55)

    # Step 1: Train the model
    model = train_model(n_samples=200)
    print(f"\n  [✓] Model ready.\n")

    # Step 2: Define scenarios to demonstrate
    scenarios = [
        (simulate_normal,                        "SCENARIO 1: Normal System State"),
        (lambda: simulate_anomaly("cpu_spike"),  "SCENARIO 2: CPU Spike"),
        (lambda: simulate_anomaly("memory_leak"),"SCENARIO 3: Memory Leak"),
        (lambda: simulate_anomaly("disk_full"),  "SCENARIO 4: Disk Full"),
        (lambda: simulate_anomaly("combined"),   "SCENARIO 5: Combined Failure"),
    ]

    for generate_metrics, scenario_name in scenarios:
        time.sleep(DEMO_DELAY)

        print("\n" + "─"*55)
        print(f"  {scenario_name}")
        print("─"*55)

        # Step 3: Collect metrics
        metrics = generate_metrics()
        print(f"\n  Raw Metrics: {metrics}")

        # Step 4: AI Detection
        label, score, _ = predict(model, metrics)
        print(f"\n  AI Decision: {label}  (score={score})")

        # Step 5: XAI Explanation
        xai_report = explain(metrics, label, score)
        print(xai_report)

        # Step 6: Self-Healing
        decide_and_heal(metrics, label, xai_report)

    print("\n\n" + "★"*55)
    print("  Demo complete! Check 'recovery_log.txt' for all actions.")
    print("★"*55)


if __name__ == "__main__":
    run_demo()
