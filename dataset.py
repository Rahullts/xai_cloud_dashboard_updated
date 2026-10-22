# dataset.py
# Generates a reproducible dataset for ML evaluation.

import random
import time
import numpy as np
from sklearn.model_selection import train_test_split
from monitor import simulate_normal, simulate_anomaly

FEATURES = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "net_bytes_sent",
    "net_bytes_recv",
]

def generate_dataset(n_samples=1000, random_seed=42):
    """
    Generate a reproducible dataset.
    Normal = 0
    Anomaly/Failure = 1
    """
    random.seed(random_seed)
    dataset = []
    
    anomaly_types = ["cpu_spike", "memory_leak", "disk_full", "network_issue", "combined"]
    
    for i in range(n_samples):
        is_anomaly = random.random() < 0.2
        if is_anomaly:
            scenario = random.choice(anomaly_types)
            metrics = simulate_anomaly(scenario)
            label = 1
        else:
            scenario = "normal"
            metrics = simulate_normal()
            label = 0
            
        sample = {
            "id": i,
            "timestamp": int(time.time()) + i,
            "scenario": scenario,
            "label": label,
        }
        sample.update(metrics)
        dataset.append(sample)
        
    return dataset

def get_train_val_test_split(n_train=1200, n_val=400, n_test=400, random_seed=42):
    """
    Returns (X_train, X_val, X_test, y_train, y_val, y_test, train_data, val_data, test_data)
    Phase 2B.2: Generates train, validation, and test sets completely independently using
    different deterministic seeds to avoid near-duplicate distributions.
    """
    train_data = generate_dataset(n_samples=n_train, random_seed=random_seed)
    val_data = generate_dataset(n_samples=n_val, random_seed=random_seed + 1000)
    test_data = generate_dataset(n_samples=n_test, random_seed=random_seed + 2000)
    
    def extract(data):
        X = np.array([[d[f] for f in FEATURES] for d in data])
        y = np.array([d["label"] for d in data])
        return X, y

    X_train, y_train = extract(train_data)
    X_val, y_val = extract(val_data)
    X_test, y_test = extract(test_data)
    
    return X_train, X_val, X_test, y_train, y_val, y_test, train_data, val_data, test_data

def get_train_test_split(n_train=1600, n_test=400, random_seed=42):
    """
    Kept for backward compatibility if needed.
    """
    X_train, X_val, X_test, y_train, y_val, y_test, train_data, val_data, test_data = get_train_val_test_split(
        n_train, 0, n_test, random_seed
    )
    return X_train, X_test, y_train, y_test, train_data, test_data

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, m_train, m_test = get_train_test_split()
    print(f"Train size: {len(X_train)} (Anomalies: {sum(y_train)})")
    print(f"Test size: {len(X_test)} (Anomalies: {sum(y_test)})")
