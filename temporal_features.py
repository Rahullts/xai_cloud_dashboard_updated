import numpy as np

METRICS = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "net_bytes_sent_rate",
    "net_bytes_recv_rate"
]

PREDICTION_HORIZON = 10
WINDOWS = [5, 10]

def _calculate_slope(y_values):
    """
    Fits a simple linear regression: y = slope * x + intercept
    over the given window of values. x is [0, 1, ..., len(y)-1].
    Returns the slope.
    """
    n = len(y_values)
    if n < 2:
        return 0.0
    x = np.arange(n)
    # Slope formula: Cov(x, y) / Var(x)
    cov = np.cov(x, y_values)[0, 1]
    var = np.var(x, ddof=1)
    if var == 0:
        return 0.0
    return cov / var

def extract_features_from_sequence(sequence):
    """
    Given a list of dicts (a single sequence sorted by timestep),
    extracts rolling historical features and future targets.
    
    Warm-up: drops the first max(WINDOWS) - 1 rows.
    Censoring: drops the last PREDICTION_HORIZON rows.
    """
    seq_len = len(sequence)
    max_window = max(WINDOWS)
    
    features = []
    
    # We can only extract features if we have enough data for warm-up + horizon
    if seq_len <= max_window + PREDICTION_HORIZON:
        return []
        
    for t in range(max_window - 1, seq_len - PREDICTION_HORIZON):
        current_row = sequence[t]
        
        row_feat = {
            "sequence_id": current_row["sequence_id"],
            "timestep": current_row["timestep"],
            "timestamp": current_row["timestamp"],
            "scenario": current_row["scenario"],
            "failure_status": current_row["failure_status"], # Kept strictly as metadata
            # Target calculation
            # target = 1 if ANY of the next PREDICTION_HORIZON timesteps has failure_status == 1
            "target_failure_within_10": int(any(
                sequence[t + h]["failure_status"] == 1 
                for h in range(1, PREDICTION_HORIZON + 1)
            ))
        }
        
        for metric in METRICS:
            # Current value
            row_feat[f"{metric}_current"] = current_row[metric]
            
            for w in WINDOWS:
                # History slice [t - w + 1 : t + 1]
                history = [sequence[i][metric] for i in range(t - w + 1, t + 1)]
                
                row_feat[f"{metric}_mean_{w}"] = round(float(np.mean(history)), 4)
                row_feat[f"{metric}_delta_{w}"] = round(history[-1] - history[0], 4)
                row_feat[f"{metric}_slope_{w}"] = round(float(_calculate_slope(history)), 4)
                row_feat[f"{metric}_std_{w}"] = round(float(np.std(history)), 4)
                
        features.append(row_feat)
        
    return features

def extract_features_dataset(dataset):
    """
    Given a dataset (list of all sequence rows),
    groups by sequence_id and extracts features independently.
    Returns a flat list of feature dicts.
    """
    from collections import defaultdict
    seq_groups = defaultdict(list)
    for row in dataset:
        seq_groups[row["sequence_id"]].append(row)
        
    all_features = []
    for seq_id, seq in seq_groups.items():
        # Ensure it's sorted by timestep just in case
        seq.sort(key=lambda x: x["timestep"])
        seq_feats = extract_features_from_sequence(seq)
        all_features.extend(seq_feats)
        
    return all_features

if __name__ == "__main__":
    from temporal_dataset import get_temporal_train_val_test_split
    df_train, df_val, df_test = get_temporal_train_val_test_split()
    
    train_features = extract_features_dataset(df_train)
    print(f"Extracted {len(train_features)} feature rows from train set.")
    
    if train_features:
        print("\nExample feature row:")
        for k, v in train_features[0].items():
            print(f"  {k}: {v}")
