# =============================================================
# explainer.py — Explainability Module (XAI)
# Shows WHY an anomaly was detected using:
#   1. Feature deviation analysis (how far from normal baseline)
#   2. Rule-based human-readable explanation
#   3. Feature importance score for each metric
# =============================================================

import numpy as np
from detector import FEATURES

# ── Normal baseline thresholds (learned from typical usage) ──
NORMAL_THRESHOLDS = {
    "cpu_percent":    {"mean": 25.0, "std": 10.0, "high_danger": 85.0},
    "memory_percent": {"mean": 42.0, "std": 10.0, "high_danger": 85.0},
    "disk_percent":   {"mean": 35.0, "std": 10.0, "high_danger": 85.0},
    "net_bytes_sent": {"mean":  5.0, "std":  3.0, "high_danger": 50.0},
    "net_bytes_recv": {"mean":  5.0, "std":  3.0, "high_danger": 50.0},
}

# ── Friendly names for display ────────────────────────────────
FEATURE_LABELS = {
    "cpu_percent":    "CPU Usage (%)",
    "memory_percent": "Memory Usage (%)",
    "disk_percent":   "Disk Usage (%)",
    "net_bytes_sent": "Network Sent (MB)",
    "net_bytes_recv": "Network Received (MB)",
}


def compute_deviations(metrics: dict) -> dict:
    """
    Compute how many standard deviations each metric is from its normal mean.
    A deviation > 2 is suspicious; > 3 is critical.
    """
    deviations = {}
    for feature in FEATURES:
        value  = metrics[feature]
        mean   = NORMAL_THRESHOLDS[feature]["mean"]
        std    = NORMAL_THRESHOLDS[feature]["std"]
        # z-score: how many stds above/below normal
        z = (value - mean) / std if std > 0 else 0
        deviations[feature] = round(z, 2)
    return deviations


def get_top_contributors(deviations: dict, top_n=3) -> list:
    """
    Return the top-N features contributing most to the anomaly,
    sorted by absolute deviation (highest first).
    """
    sorted_features = sorted(
        deviations.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )
    return sorted_features[:top_n]


def rule_based_explanation(metrics: dict) -> list:
    """
    Apply simple threshold rules to generate human-readable explanations.
    Returns a list of explanation strings.
    """
    explanations = []

    if metrics["cpu_percent"] > 85:
        explanations.append(
            f"  ⚠ CPU at {metrics['cpu_percent']:.1f}% — well above safe limit of 85%. "
            f"Likely cause: runaway process or traffic surge."
        )

    if metrics["memory_percent"] > 85:
        explanations.append(
            f"  ⚠ Memory at {metrics['memory_percent']:.1f}% — possible memory leak. "
            f"Application may crash if usage reaches 100%."
        )

    if metrics["disk_percent"] > 85:
        explanations.append(
            f"  ⚠ Disk at {metrics['disk_percent']:.1f}% — storage critically low. "
            f"Log rotation or file cleanup recommended."
        )

    if metrics["net_bytes_sent"] > 40:
        explanations.append(
            f"  ⚠ Network sent {metrics['net_bytes_sent']:.1f} MB — unusually high. "
            f"Possible data exfiltration or runaway upload."
        )

    if not explanations:
        explanations.append("  ✓ All individual metrics within acceptable thresholds.")

    return explanations


def explain(metrics: dict, label: str, score: float) -> str:
    """
    Main XAI function — generates a full human-readable explanation.
    
    Parameters:
      metrics : dict of current system metrics
      label   : "NORMAL" or "ANOMALY" from detector
      score   : anomaly score from Isolation Forest
    
    Returns:
      A formatted explanation string.
    """
    deviations      = compute_deviations(metrics)
    top_contributors = get_top_contributors(deviations, top_n=3)
    rules           = rule_based_explanation(metrics)

    lines = []
    lines.append("=" * 55)
    lines.append(f"  XAI EXPLANATION REPORT")
    lines.append("=" * 55)
    lines.append(f"  Detection result : {label}")
    lines.append(f"  Anomaly score    : {score}  (lower = more anomalous)")
    lines.append("")
    lines.append("  --- Metric Snapshot ---")
    for feature in FEATURES:
        val = metrics[feature]
        dev = deviations[feature]
        flag = "  <<<" if abs(dev) > 2 else ""
        lines.append(
            f"  {FEATURE_LABELS[feature]:<25} {val:6.1f}   (z={dev:+.1f}){flag}"
        )

    lines.append("")
    lines.append("  --- Feature Importance (by deviation) ---")
    for i, (feature, z) in enumerate(top_contributors, 1):
        bar = "█" * min(int(abs(z) * 2), 20)
        lines.append(
            f"  #{i} {FEATURE_LABELS[feature]:<25} z={z:+.1f}  {bar}"
        )

    lines.append("")
    lines.append("  --- Rule-Based Reasoning ---")
    for r in rules:
        lines.append(r)

    lines.append("=" * 55)
    return "\n".join(lines)


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    from monitor import simulate_normal, simulate_anomaly
    from detector import train_model, predict

    model = train_model()

    print("\n[TEST 1] Normal system state:")
    m = simulate_normal()
    label, score, _ = predict(model, m)
    print(explain(m, label, score))

    print("\n[TEST 2] CPU spike anomaly:")
    m = simulate_anomaly("cpu_spike")
    label, score, _ = predict(model, m)
    print(explain(m, label, score))

    print("\n[TEST 3] Memory leak anomaly:")
    m = simulate_anomaly("memory_leak")
    label, score, _ = predict(model, m)
    print(explain(m, label, score))
