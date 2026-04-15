# =============================================================
# healer.py — Decision Engine + Self-Healing Module
# Maps anomaly type → recovery action → executes + logs it
# =============================================================

import datetime
import os

LOG_FILE = "recovery_log.txt"


def log_action(message: str):
    """Append a timestamped message to the recovery log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(f"  📋 LOG: {entry}")
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


# ── Individual recovery actions (simulated) ──────────────────

def restart_service(service_name="app-server"):
    """Simulate restarting a crashed or unresponsive service."""
    print(f"\n  🔄 ACTION: Restarting service '{service_name}'...")
    # In real cloud: subprocess.run(["systemctl", "restart", service_name])
    print(f"  ✅ Service '{service_name}' restarted successfully.")
    log_action(f"RESTART: Service '{service_name}' restarted due to anomaly.")


def scale_out_resources(additional_instances=1):
    """Simulate scaling out by adding more compute instances."""
    print(f"\n  📈 ACTION: Scaling out — adding {additional_instances} instance(s)...")
    # In real cloud: call AWS Auto Scaling / GCP MIG / Azure VMSS API
    print(f"  ✅ {additional_instances} additional instance(s) launched.")
    log_action(f"SCALE_OUT: Added {additional_instances} instance(s) to handle load.")


def clear_disk_cache():
    """Simulate freeing up disk space by clearing logs/cache."""
    print(f"\n  🗑️  ACTION: Clearing temporary files and log cache...")
    # In real system: os.remove() old logs, clear /tmp, etc.
    freed_mb = 512  # simulated freed space
    print(f"  ✅ Cleared {freed_mb} MB of temporary files.")
    log_action(f"DISK_CLEAN: Freed {freed_mb} MB of disk space.")


def kill_runaway_process():
    """Simulate killing a process consuming too many resources."""
    print(f"\n  ☠️  ACTION: Identifying and killing runaway process...")
    # In real system: find top-CPU process and os.kill(pid, signal.SIGTERM)
    print(f"  ✅ Runaway process terminated. Resources released.")
    log_action(f"KILL_PROC: Runaway process terminated to free resources.")


def send_alert(reason: str):
    """Simulate sending an alert to the ops team."""
    print(f"\n  📣 ACTION: Sending alert to operations team...")
    print(f"  ✅ Alert sent: '{reason}'")
    log_action(f"ALERT: Ops team notified — {reason}")


# ── Decision Engine ───────────────────────────────────────────

def decide_and_heal(metrics: dict, label: str, explanation: str):
    """
    Decision Engine:
      1. Checks which metrics are in critical range
      2. Selects the appropriate healing action(s)
      3. Executes and logs every action taken
    
    Parameters:
      metrics     : dict of current system metrics
      label       : "NORMAL" or "ANOMALY"
      explanation : XAI explanation string (for logging)
    """
    if label == "NORMAL":
        print("\n  ✅ System is NORMAL. No healing action required.")
        log_action("STATUS: System healthy. No action taken.")
        return

    print("\n" + "=" * 55)
    print("  DECISION ENGINE — Selecting Recovery Action")
    print("=" * 55)

    actions_taken = []

    # ── Rule 1: High CPU → restart service + scale out ────────
    if metrics["cpu_percent"] > 85:
        restart_service("web-app-server")
        scale_out_resources(additional_instances=1)
        actions_taken.append("restart_service + scale_out")

    # ── Rule 2: High Memory → kill process + restart ──────────
    if metrics["memory_percent"] > 85:
        kill_runaway_process()
        restart_service("memory-intensive-worker")
        actions_taken.append("kill_process + restart_service")

    # ── Rule 3: High Disk → clear cache ───────────────────────
    if metrics["disk_percent"] > 85:
        clear_disk_cache()
        actions_taken.append("clear_disk_cache")

    # ── Rule 4: High Network → alert ops ──────────────────────
    if metrics["net_bytes_sent"] > 40:
        send_alert("Unusual outbound network traffic detected.")
        actions_taken.append("send_alert")

    # ── If anomaly detected but no rule matched (borderline) ──
    if not actions_taken:
        send_alert("Anomaly detected by AI — no specific rule matched. Manual review advised.")
        actions_taken.append("send_alert (no rule match)")

    print(f"\n  ✅ Recovery complete. Actions taken: {', '.join(actions_taken)}")
    log_action(f"RECOVERY_DONE: Actions = {', '.join(actions_taken)}")


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    from monitor import simulate_anomaly
    from detector import train_model, predict
    from explainer import explain

    model = train_model()

    test_cases = [
        ("cpu_spike",   "CPU spike scenario"),
        ("memory_leak", "Memory leak scenario"),
        ("disk_full",   "Disk full scenario"),
        ("combined",    "Combined failure scenario"),
    ]

    for anomaly_type, description in test_cases:
        print(f"\n{'='*55}")
        print(f"  SCENARIO: {description}")
        print("="*55)
        metrics = simulate_anomaly(anomaly_type)
        label, score, _ = predict(model, metrics)
        xai_report = explain(metrics, label, score)
        print(xai_report)
        decide_and_heal(metrics, label, xai_report)
