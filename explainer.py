# =============================================================
# explainer.py — Heuristic Explanation Module
# =============================================================

from detector import FEATURES

NORMAL_THRESHOLDS = {
    "cpu_percent": {"mean": 25.0, "std": 10.0, "high_danger": 85.0},
    "memory_percent": {"mean": 42.0, "std": 10.0, "high_danger": 85.0},
    "disk_percent": {"mean": 35.0, "std": 10.0, "high_danger": 85.0},
    "net_bytes_sent": {"mean": 5.0, "std": 3.0, "high_danger": 40.0},
    "net_bytes_recv": {"mean": 5.0, "std": 3.0, "high_danger": 40.0},
}
FEATURE_LABELS = {
    "cpu_percent": "CPU Usage (%)",
    "memory_percent": "Memory Usage (%)",
    "disk_percent": "Disk Usage (%)",
    "net_bytes_sent": "Network Sent (cumulative MB)",
    "net_bytes_recv": "Network Received (cumulative MB)",
}


def _validate_metrics(metrics):
    missing = [feature for feature in FEATURES if feature not in metrics]
    if missing:
        raise ValueError(f"Missing required metric(s): {', '.join(missing)}")


def compute_deviations(metrics: dict) -> dict:
    """Return heuristic z-score-like deviations from fixed demo baselines."""
    _validate_metrics(metrics)
    return {
        feature: round(
            (float(metrics[feature]) - NORMAL_THRESHOLDS[feature]["mean"])
            / NORMAL_THRESHOLDS[feature]["std"],
            2,
        )
        for feature in FEATURES
    }


def get_top_contributors(deviations: dict, top_n=3) -> list:
    """Rank metrics by absolute deviation; these are not model feature attributions."""
    if not isinstance(top_n, int) or top_n < 0:
        raise ValueError("top_n must be a non-negative integer.")
    return sorted(deviations.items(), key=lambda item: abs(item[1]), reverse=True)[:top_n]


def rule_based_explanation(metrics: dict) -> list:
    """Generate readable threshold explanations (heuristics, not causal claims)."""
    _validate_metrics(metrics)
    explanations = []
    if metrics["cpu_percent"] > 85:
        explanations.append(f"CPU usage is {metrics['cpu_percent']:.1f}% (demo threshold: 85%).")
    if metrics["memory_percent"] > 85:
        explanations.append(f"Memory usage is {metrics['memory_percent']:.1f}% (demo threshold: 85%).")
    if metrics["disk_percent"] > 85:
        explanations.append(f"Disk usage is {metrics['disk_percent']:.1f}% (demo threshold: 85%).")
    if metrics["net_bytes_sent"] > 40:
        explanations.append(f"Cumulative network sent is {metrics['net_bytes_sent']:.1f} MB (demo threshold: 40 MB).")
    if metrics["net_bytes_recv"] > 40:
        explanations.append(f"Cumulative network received is {metrics['net_bytes_recv']:.1f} MB (demo threshold: 40 MB).")
    if not explanations:
        explanations.append("No configured metric threshold was exceeded.")
    return explanations


def explain(metrics: dict, label: str, score: float) -> str:
    """
    Format a report. Feature rankings are fixed-baseline deviation heuristics,
    not SHAP/LIME or a causal explanation of the Isolation Forest prediction.
    """
    deviations = compute_deviations(metrics)
    contributors = get_top_contributors(deviations)
    lines = [
        "=" * 55,
        "HEURISTIC EXPLANATION REPORT",
        "Note: rankings use fixed demo baselines; they are not model attributions.",
        f"Detection result: {label}",
        f"Isolation Forest decision_function score: {score} (lower = more anomalous)",
        "",
        "--- Metric snapshot ---",
    ]
    for feature in FEATURES:
        value = float(metrics[feature])
        deviation = deviations[feature]
        flag = "  [large deviation]" if abs(deviation) > 2 else ""
        lines.append(
            f"{FEATURE_LABELS[feature]:<34} {value:8.2f} (z-like={deviation:+.2f}){flag}"
        )
    lines.extend(["", "--- Largest baseline deviations (heuristic) ---"])
    for rank, (feature, deviation) in enumerate(contributors, 1):
        lines.append(f"#{rank} {FEATURE_LABELS[feature]}: z-like={deviation:+.2f}")
    lines.extend(["", "--- Threshold rules ---"])
    lines.extend(rule_based_explanation(metrics))
    lines.append("=" * 55)
    return "\n".join(lines)


if __name__ == "__main__":
    from monitor import simulate_anomaly
    from detector import train_model, predict

    model = train_model()
    metrics = simulate_anomaly("cpu_spike")
    label, score, _ = predict(model, metrics)
    print(explain(metrics, label, score))
