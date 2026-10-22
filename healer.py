# =============================================================
# healer.py — Phase 3E / 4A Simulated Healer & Recovery Engine
# Safely simulates recovery mapped from Root-Cause & Decision Engine
# =============================================================

import datetime
import json
import os
from pathlib import Path

LOG_FILE = Path(__file__).with_name("recovery_log.txt")


def log_action(message: str) -> bool:
    """Safely append a timestamped message to the recovery log."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(f"  [LOG] {entry}")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        return True
    except OSError:
        print("  [WARNING] LOG WRITE FAILED -- entry was NOT saved to disk.")
        return False


def select_recovery_actions(metrics: dict, label: str, thresholds=None) -> list:
    """
    Select proposed recovery actions without executing them.
    These are recommendations for a demo only. This project does not connect
    to a cloud provider or restart/kill/scale/clean any real resource.
    """
    thresholds = thresholds or {
        "cpu_percent": 85.0,
        "memory_percent": 85.0,
        "disk_percent": 85.0,
        "net_bytes_sent": 40.0,
        "net_bytes_recv": 40.0,
    }
    if label not in {"NORMAL", "ANOMALY"}:
        raise ValueError("label must be NORMAL or ANOMALY")
    required = set(thresholds)
    missing = required.difference(metrics)
    if missing:
        raise ValueError(f"Missing required metric(s): {', '.join(sorted(missing))}")

    if label == "NORMAL":
        return []

    actions = []
    if metrics["cpu_percent"] > thresholds["cpu_percent"]:
        actions.extend([
            {"action": "restart_service", "reason": "CPU usage exceeded threshold"},
            {"action": "scale_out", "reason": "CPU usage exceeded threshold"},
        ])
    if metrics["memory_percent"] > thresholds["memory_percent"]:
        actions.extend([
            {"action": "inspect_memory_pressure", "reason": "Memory usage exceeded threshold"},
            {"action": "restart_worker", "reason": "Memory usage exceeded threshold"},
        ])
    if metrics["disk_percent"] > thresholds["disk_percent"]:
        actions.append({"action": "review_disk_cleanup", "reason": "Disk usage exceeded threshold"})
    if (
        metrics["net_bytes_sent"] > thresholds["net_bytes_sent"]
        or metrics["net_bytes_recv"] > thresholds["net_bytes_recv"]
    ):
        actions.append({"action": "notify_operator", "reason": "Network volume exceeded threshold"})
    if not actions:
        actions.append({
            "action": "manual_review",
            "reason": "Model flagged a problem but no action rule matched",
        })
    return actions


def decide_and_heal(action_or_metrics, label: str = None, explanation: str = ""):
    """
    Executes the recommended recovery action safely in simulation.
    Supports both Phase 3E/4A string action commands and backward-compatible metric dicts.
    """
    if isinstance(action_or_metrics, str):
        recommended_action = action_or_metrics
        print("\n" + "=" * 55)
        print("  HEALING SIMULATION -- Executing Action")
        print("=" * 55)
        print(f"  [ACTION] {recommended_action}")

        if "Scale CPU" in recommended_action:
            log_action("SCALE_OUT: Simulated adding compute instances.")
        elif "Restart affected service" in recommended_action:
            log_action("RESTART: Simulated service restart to clear memory/state.")
        elif "Clean temporary data" in recommended_action:
            log_action("DISK_CLEAN: Simulated freeing disk space.")
        elif "Check/restart network service" in recommended_action:
            log_action("NETWORK_RESET: Simulated network service reboot.")
        elif "Controlled recovery sequence" in recommended_action:
            log_action("COMBINED_RECOVERY: Simulated rolling restart and scale out.")
        else:
            log_action(f"ALERT_ONLY: Alerted operator for {recommended_action}. No autonomous destructive action taken.")

        print("  [DONE] Recovery simulation complete.")
        return "Executed"

    # Backward-compatible dict input
    metrics = action_or_metrics
    actions = select_recovery_actions(metrics, label or "ANOMALY")
    if not actions:
        message = "NORMAL: no recovery action proposed."
        print(message)
        log_action(message)
        return []

    print("RECOVERY PLAN (SIMULATION ONLY)")
    if explanation:
        print(explanation)
    for action in actions:
        message = f"PROPOSED {action['action']}: {action['reason']}"
        print(f"- {message}")
        log_action(message)
    log_action(f"PLAN_CREATED: {len(actions)} simulated action(s)")
    return actions


if __name__ == "__main__":
    decide_and_heal("Restart affected service / reclaim memory")
