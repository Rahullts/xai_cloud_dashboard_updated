# =============================================================
# monitor.py — System Monitoring Module
# Collects CPU, Memory, Disk, Network metrics using psutil
# =============================================================

import psutil
import time
import random

def get_system_metrics():
    """
    Collect real-time system metrics.
    Returns a dictionary of current resource usage.
    """
    metrics = {
        "cpu_percent":    psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent":   psutil.disk_usage("/").percent,
        "net_bytes_sent": psutil.net_io_counters().bytes_sent / 1e6,   # MB
        "net_bytes_recv": psutil.net_io_counters().bytes_recv / 1e6,   # MB
    }
    return metrics


def simulate_normal():
    """
    Simulate a NORMAL system state.
    Returns metrics with low/moderate resource usage.
    """
    return {
        "cpu_percent":    random.uniform(10, 40),
        "memory_percent": random.uniform(30, 55),
        "disk_percent":   random.uniform(20, 50),
        "net_bytes_sent": random.uniform(1, 10),
        "net_bytes_recv": random.uniform(1, 10),
    }


def simulate_anomaly(anomaly_type="cpu_spike"):
    """
    Simulate a FAILURE / ANOMALY state.
    
    anomaly_type options:
      - "cpu_spike"    : Very high CPU usage
      - "memory_leak"  : Memory nearly full
      - "disk_full"    : Disk almost full
      - "combined"     : Multiple metrics spiked
    """
    base = simulate_normal()

    if anomaly_type == "cpu_spike":
        base["cpu_percent"] = random.uniform(88, 99)
    elif anomaly_type == "memory_leak":
        base["memory_percent"] = random.uniform(88, 98)
    elif anomaly_type == "disk_full":
        base["disk_percent"] = random.uniform(90, 99)
    elif anomaly_type == "combined":
        base["cpu_percent"]    = random.uniform(85, 99)
        base["memory_percent"] = random.uniform(82, 95)
        base["disk_percent"]   = random.uniform(80, 95)

    return base


def collect_samples(n=50, inject_anomalies=True):
    """
    Collect n metric samples (simulated).
    Injects a few anomalies for training/demo purposes.
    Returns a list of metric dicts.
    """
    samples = []
    for i in range(n):
        if inject_anomalies and i % 10 == 0:          # ~10% anomalies
            anomaly_type = random.choice(
                ["cpu_spike", "memory_leak", "disk_full", "combined"]
            )
            samples.append(simulate_anomaly(anomaly_type))
        else:
            samples.append(simulate_normal())
    return samples


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Normal sample ===")
    print(simulate_normal())

    print("\n=== Anomaly sample (CPU spike) ===")
    print(simulate_anomaly("cpu_spike"))

    print("\n=== Anomaly sample (combined) ===")
    print(simulate_anomaly("combined"))
