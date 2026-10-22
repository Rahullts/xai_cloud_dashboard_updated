# =============================================================
# detector.py — AI Anomaly Detection Module
# Uses Isolation Forest (scikit-learn) to detect metric outliers.
# =============================================================

import numpy as np
from sklearn.ensemble import IsolationForest
from monitor import collect_samples

FEATURES = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "net_bytes_sent",
    "net_bytes_recv",
]


def metrics_to_vector(metrics: dict) -> list:
    """Validate and convert one metric dictionary into model feature order."""
    missing = [feature for feature in FEATURES if feature not in metrics]
    if missing:
        raise ValueError(f"Missing required metric(s): {', '.join(missing)}")

    vector = []
    for feature in FEATURES:
        value = metrics[feature]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Metric '{feature}' must be numeric.")
        if not np.isfinite(value):
            raise ValueError(f"Metric '{feature}' must be finite.")
        vector.append(float(value))
    return vector


def train_model(n_samples=200, random_state=42):
    """
    Train Isolation Forest on generated demonstration data.

    Important: generated scenarios are synthetic; model performance must be
    evaluated separately on held-out samples before making accuracy claims.
    """
    if not isinstance(n_samples, int) or n_samples < 20:
        raise ValueError("n_samples must be an integer >= 20.")

    print("[detector] Training Isolation Forest model...")
    samples = collect_samples(n=n_samples, inject_anomalies=True, seed=random_state)
    X = np.asarray([metrics_to_vector(sample) for sample in samples], dtype=float)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=random_state,
    )
    model.fit(X)
    print(f"[detector] Model trained on {n_samples} synthetic samples.")
    return model


def predict(model, metrics: dict):
    """
    Predict one metric snapshot.

    Returns (label, decision_score, feature_vector). In scikit-learn's
    decision_function, lower scores are more anomalous; zero is the boundary.
    """
    vector = metrics_to_vector(metrics)
    X = np.asarray([vector], dtype=float)
    raw_prediction = model.predict(X)[0]
    score = model.decision_function(X)[0]
    label = "ANOMALY" if raw_prediction == -1 else "NORMAL"
    return label, round(float(score), 4), vector


if __name__ == "__main__":
    from monitor import simulate_normal, simulate_anomaly

    model = train_model()
    for description, sample in [
        ("NORMAL", simulate_normal()),
        ("CPU spike", simulate_anomaly("cpu_spike")),
    ]:
        label, score, _ = predict(model, sample)
        print(f"{description}: {label} (decision_score={score})")
