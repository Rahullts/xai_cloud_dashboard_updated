# =============================================================
# healer.py — Recovery Decision Engine (simulation only)
# =============================================================

from datetime import datetime, timezone
from pathlib import Path
import json

LOG_FILE = Path(__file__).with_name("recovery_log.jsonl")


def log_action(message: str, log_file=LOG_FILE):
    """Append a timestamped JSON record to the recovery audit log."""
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "simulation": True,
        "message": message,
    }
    with Path(log_file).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


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


def decide_and_heal(metrics: dict, label: str, explanation: str = "") -> list:
    """
    Backward-compatible orchestration entry point. Records proposed actions
    as simulated recommendations; it never claims that real recovery occurred.
    """
    actions = select_recovery_actions(metrics, label)
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
    from monitor import simulate_anomaly
    from detector import train_model, predict
    from explainer import explain

    model = train_model()
    metrics = simulate_anomaly("cpu_spike")
    label, score, _ = predict(model, metrics)
    report = explain(metrics, label, score)
    decide_and_heal(metrics, label, report)
