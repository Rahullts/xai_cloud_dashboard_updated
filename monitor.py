# =============================================================
# monitor.py — System Monitoring and Scenario Simulation
# =============================================================

import random
import time

import psutil

METRIC_KEYS = (
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "net_bytes_sent",
    "net_bytes_recv",
)


def get_system_metrics(disk_path=None):
    """
    Collect a snapshot of real host metrics.

    Network values are cumulative MB since the network counters were reset,
    not throughput rates. disk_path defaults to the current working drive.
    """
    disk_percent = psutil.disk_usage(disk_path or ".").percent

    counters = psutil.net_io_counters()
    return {
        "cpu_percent": float(psutil.cpu_percent(interval=1)),
        "memory_percent": float(psutil.virtual_memory().percent),
        "disk_percent": float(disk_percent),
        "net_bytes_sent": float(counters.bytes_sent / 1_000_000),
        "net_bytes_recv": float(counters.bytes_recv / 1_000_000),
    }


def simulate_normal(rng=None):
    """Return one synthetic healthy-state metric snapshot."""
    rng = rng or random
    return {
        "cpu_percent": rng.uniform(10, 40),
        "memory_percent": rng.uniform(30, 55),
        "disk_percent": rng.uniform(20, 50),
        "net_bytes_sent": rng.uniform(1, 10),
        "net_bytes_recv": rng.uniform(1, 10),
    }


def simulate_anomaly(anomaly_type="cpu_spike", rng=None):
    """Return synthetic metrics for a supported failure scenario."""
    rng = rng or random
    if anomaly_type not in {"cpu_spike", "memory_leak", "disk_full", "combined", "network_issue"}:
        raise ValueError(
            "Unsupported scenario. Choose cpu_spike, memory_leak, disk_full, "
            "network_issue, or combined."
        )

    base = simulate_normal(rng)
    if anomaly_type == "cpu_spike":
        base["cpu_percent"] = rng.uniform(88, 99)
    elif anomaly_type == "memory_leak":
        base["memory_percent"] = rng.uniform(88, 98)
    elif anomaly_type == "disk_full":
        base["disk_percent"] = rng.uniform(90, 99)
    elif anomaly_type == "network_issue":
        base["net_bytes_sent"] = rng.uniform(45, 80)
        base["net_bytes_recv"] = rng.uniform(45, 80)
    elif anomaly_type == "combined":
        base["cpu_percent"] = rng.uniform(88, 99)
        base["memory_percent"] = rng.uniform(88, 98)
        base["disk_percent"] = rng.uniform(90, 99)
        base["net_bytes_sent"] = rng.uniform(45, 80)
        base["net_bytes_recv"] = rng.uniform(45, 80)
    return base


def collect_samples(n=50, inject_anomalies=True, seed=None):
    """Generate reproducible synthetic samples for development and tests."""
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer.")
    rng = random.Random(seed)
    samples = []
    scenario_types = ("cpu_spike", "memory_leak", "disk_full", "combined", "network_issue")
    for i in range(n):
        if inject_anomalies and i % 10 == 0:
            samples.append(simulate_anomaly(rng.choice(scenario_types), rng=rng))
        else:
            samples.append(simulate_normal(rng=rng))
    return samples


if __name__ == "__main__":
    print("=== Synthetic normal sample ===")
    print(simulate_normal())
    print("\n=== Synthetic CPU-spike sample ===")
    print(simulate_anomaly("cpu_spike"))
    print("\n=== Real host metrics ===")
    print(get_system_metrics())
