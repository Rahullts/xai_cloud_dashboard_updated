# =============================================================
# detector.py — AI Anomaly Detection Module
# Uses Isolation Forest (scikit-learn) to detect outliers
# =============================================================

import numpy as np
from sklearn.ensemble import IsolationForest
from monitor import collect_samples

# ── Feature names (must match order in metrics dict) ──────────
FEATURES = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "net_bytes_sent",
    "net_bytes_recv",
]


def metrics_to_vector(metrics: dict) -> list:
    """Convert a metrics dict to a feature vector (list)."""
    return [metrics[f] for f in FEATURES]


def train_model(n_samples=200):
    """
    Train an Isolation Forest on simulated normal + anomalous data.
    
    IsolationForest:
      - Randomly isolates data points using decision trees
      - Anomalies are isolated in fewer steps → shorter path length
      - contamination=0.1 means ~10% of data is expected to be anomalous
    
    Returns: trained IsolationForest model
    """
    print("[detector] Training Isolation Forest model...")
    samples = collect_samples(n=n_samples, inject_anomalies=True)
    X = np.array([metrics_to_vector(s) for s in samples])

    model = IsolationForest(
        n_estimators=100,        # number of trees
        contamination=0.1,       # expected fraction of anomalies
        random_state=42,
    )
    model.fit(X)
    print(f"[detector] Model trained on {n_samples} samples.")
    return model


def predict(model, metrics: dict):
    """
    Predict whether a metrics snapshot is normal or anomalous.
    
    Returns:
      - label    : "NORMAL" or "ANOMALY"
      - score    : anomaly score (more negative = more anomalous)
      - vector   : the feature vector used
    """
    vector = metrics_to_vector(metrics)
    X = np.array([vector])

    raw_prediction = model.predict(X)[0]   # 1 = normal, -1 = anomaly
    score = model.decision_function(X)[0]  # higher = more normal

    label = "ANOMALY" if raw_prediction == -1 else "NORMAL"
    return label, round(score, 4), vector


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    from monitor import simulate_normal, simulate_anomaly

    model = train_model()

    print("\n--- Testing NORMAL sample ---")
    normal = simulate_normal()
    label, score, vec = predict(model, normal)
    print(f"Metrics : {normal}")
    print(f"Result  : {label}  (score={score})")

    print("\n--- Testing ANOMALY sample (CPU spike) ---")
    anomaly = simulate_anomaly("cpu_spike")
    label, score, vec = predict(model, anomaly)
    print(f"Metrics : {anomaly}")
    print(f"Result  : {label}  (score={score})")
