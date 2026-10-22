import numpy as np
import random
from datetime import datetime, timedelta

# Default configuration
DEFAULT_SEQ_LEN = 60
DEFAULT_INTERVAL_MINUTES = 1

SCENARIOS = [
    "normal_stable",
    "normal_variable",
    "cpu_gradual_failure",
    "cpu_sudden_failure",
    "memory_gradual_leak",
    "disk_gradual_exhaustion",
    "network_degradation",
    "combined_gradual_failure"
]

def _clip(val, min_v, max_v):
    return max(min_v, min(val, max_v))

def _generate_base_noise(seq_len):
    """Generate baseline normal system metrics."""
    return {
        "cpu": [max(5, min(random.gauss(30, 10), 80)) for _ in range(seq_len)],
        "mem": [max(20, min(random.gauss(40, 10), 75)) for _ in range(seq_len)],
        "disk": [random.uniform(20, 60) for _ in range(seq_len)], # disk usually static but we'll add slight jitter later
        "net_s": [abs(random.gauss(5, 5)) for _ in range(seq_len)],
        "net_r": [abs(random.gauss(8, 6)) for _ in range(seq_len)]
    }

def generate_sequence(scenario, seq_id, seq_len=DEFAULT_SEQ_LEN, start_time=None):
    if start_time is None:
        start_time = datetime(2026, 1, 1)
        
    timestamps = [start_time + timedelta(minutes=DEFAULT_INTERVAL_MINUTES * i) for i in range(seq_len)]
    
    # Initialize base metrics
    base = _generate_base_noise(seq_len)
    cpu = base["cpu"]
    mem = base["mem"]
    
    # Disk usually grows very slowly or stays flat, so we use a random walk
    disk = [random.uniform(20, 60)]
    for _ in range(1, seq_len):
        disk.append(_clip(disk[-1] + random.gauss(0, 0.5), 0, 100))
        
    net_s = base["net_s"]
    net_r = base["net_r"]
    
    failure_start_index = None
    failure_status = [0] * seq_len
    
    if scenario == "normal_stable":
        pass # keep base noise
        
    elif scenario == "normal_variable":
        # More legitimate variation but still healthy
        for i in range(seq_len):
            cpu[i] = _clip(cpu[i] + random.gauss(0, 15), 5, 85)
            mem[i] = _clip(mem[i] + random.gauss(0, 15), 20, 85)
            net_s[i] = _clip(net_s[i] + random.gauss(0, 10), 0, 50)
            
    elif scenario == "cpu_gradual_failure":
        failure_start_index = random.randint(int(seq_len * 0.4), int(seq_len * 0.7))
        for i in range(failure_start_index, seq_len):
            failure_status[i] = 1
            # gradually increase trend
            trend = ((i - failure_start_index) / (seq_len - failure_start_index)) * 60
            cpu[i] = _clip(cpu[i] + trend + random.gauss(0, 5), 5, 100)
            
    elif scenario == "cpu_sudden_failure":
        failure_start_index = random.randint(int(seq_len * 0.5), int(seq_len * 0.8))
        for i in range(failure_start_index, seq_len):
            failure_status[i] = 1
            cpu[i] = _clip(random.gauss(90, 5), 85, 100)
            
    elif scenario == "memory_gradual_leak":
        failure_start_index = random.randint(int(seq_len * 0.3), int(seq_len * 0.6))
        for i in range(failure_start_index, seq_len):
            failure_status[i] = 1
            trend = ((i - failure_start_index) / (seq_len - failure_start_index)) * 50
            mem[i] = _clip(mem[i] + trend + random.gauss(0, 3), 20, 100)
            
    elif scenario == "disk_gradual_exhaustion":
        failure_start_index = random.randint(int(seq_len * 0.2), int(seq_len * 0.5))
        for i in range(failure_start_index, seq_len):
            failure_status[i] = 1
            trend = ((i - failure_start_index) / (seq_len - failure_start_index)) * 40
            disk[i] = _clip(disk[i] + trend + random.gauss(0, 1), 0, 100)
            
    elif scenario == "network_degradation":
        failure_start_index = random.randint(int(seq_len * 0.4), int(seq_len * 0.7))
        for i in range(failure_start_index, seq_len):
            failure_status[i] = 1
            trend = ((i - failure_start_index) / (seq_len - failure_start_index)) * 50
            net_s[i] = _clip(net_s[i] + trend + random.gauss(0, 10), 0, 100)
            net_r[i] = _clip(net_r[i] + trend + random.gauss(0, 10), 0, 100)
            
    elif scenario == "combined_gradual_failure":
        failure_start_index = random.randint(int(seq_len * 0.4), int(seq_len * 0.7))
        for i in range(failure_start_index, seq_len):
            failure_status[i] = 1
            trend = ((i - failure_start_index) / (seq_len - failure_start_index)) * 40
            cpu[i] = _clip(cpu[i] + trend + random.gauss(0, 5), 5, 95)
            mem[i] = _clip(mem[i] + trend + random.gauss(0, 5), 20, 95)
            disk[i] = _clip(disk[i] + trend * 0.5 + random.gauss(0, 2), 20, 95)

    data = []
    for i in range(seq_len):
        data.append({
            "sequence_id": seq_id,
            "timestep": i,
            "timestamp": timestamps[i].isoformat(),
            "cpu_percent": round(cpu[i], 4),
            "memory_percent": round(mem[i], 4),
            "disk_percent": round(disk[i], 4),
            "net_bytes_sent_rate": round(net_s[i], 4),
            "net_bytes_recv_rate": round(net_r[i], 4),
            "scenario": scenario,
            "failure_status": failure_status[i],
            "failure_start_index": failure_start_index
        })
    
    return data

def generate_dataset_split(n_sequences, random_seed, seq_len=DEFAULT_SEQ_LEN, id_prefix="seq"):
    """
    Generate a complete dataset split consisting of multiple independent sequences.
    Returns a list of dictionary rows.
    """
    random.seed(random_seed)
    
    dataset = []
    for i in range(n_sequences):
        scenario = random.choice(SCENARIOS)
        seq_id = f"{id_prefix}_{i}"
        
        # Give each sequence a realistically progressing start time
        start_time = datetime(2026, 1, 1) + timedelta(minutes=i * seq_len)
        
        seq_data = generate_sequence(scenario, seq_id, seq_len, start_time)
        dataset.extend(seq_data)
        
    return dataset

def get_temporal_train_val_test_split(n_train=100, n_val=25, n_test=25, seq_len=DEFAULT_SEQ_LEN, random_seed=42):
    """
    Creates completely independent sequences for Train, Validation, and Test.
    No sequence ID overlaps. No individual timesteps are randomly split.
    """
    df_train = generate_dataset_split(n_train, random_seed, seq_len, id_prefix="train")
    df_val = generate_dataset_split(n_val, random_seed + 1000, seq_len, id_prefix="val")
    df_test = generate_dataset_split(n_test, random_seed + 2000, seq_len, id_prefix="test")
    
    return df_train, df_val, df_test

if __name__ == "__main__":
    df_train, df_val, df_test = get_temporal_train_val_test_split()
    train_ids = set(r['sequence_id'] for r in df_train)
    val_ids = set(r['sequence_id'] for r in df_val)
    test_ids = set(r['sequence_id'] for r in df_test)
    print(f"Train sequences: {len(train_ids)} | Shape: {len(df_train)} rows")
    print(f"Val sequences: {len(val_ids)} | Shape: {len(df_val)} rows")
    print(f"Test sequences: {len(test_ids)} | Shape: {len(df_test)} rows")
    
    # Save examples to csv for inspection if needed using standard python
    import csv, os
    os.makedirs("results", exist_ok=True)
    if df_test:
        keys = df_test[0].keys()
        with open("results/temporal_test_sample.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(df_test)
