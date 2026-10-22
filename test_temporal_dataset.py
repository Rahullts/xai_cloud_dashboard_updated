import math
from temporal_dataset import get_temporal_train_val_test_split, SCENARIOS, DEFAULT_SEQ_LEN

def run_validations():
    print("Running Temporal Dataset Validations...")
    df_train, df_val, df_test = get_temporal_train_val_test_split(n_train=200, n_val=50, n_test=50, random_seed=42)
    df_all = df_train + df_val + df_test

    expected_cols = [
        "sequence_id", "timestep", "timestamp", "cpu_percent", 
        "memory_percent", "disk_percent", "net_bytes_sent_rate", 
        "net_bytes_recv_rate", "scenario", "failure_status", "failure_start_index"
    ]
    
    # 1. Expected columns exist
    if df_all:
        missing_cols = set(expected_cols) - set(df_all[0].keys())
        assert not missing_cols, f"Missing columns: {missing_cols}"
    print("1. Expected columns exist -> PASS")

    # 2. No NaN values (except failure_start_index can be None)
    for row in df_all:
        for k, v in row.items():
            if k != "failure_start_index":
                assert v is not None, f"None value found in {k}"
                if isinstance(v, float):
                    assert not math.isnan(v), f"NaN value found in {k}"
    print("2. No NaN values -> PASS")

    # 3. Values remain within valid ranges
    for row in df_all:
        assert 0 <= row["cpu_percent"] <= 100, f"cpu_percent out of bounds: {row['cpu_percent']}"
        assert 0 <= row["memory_percent"] <= 100
        assert 0 <= row["disk_percent"] <= 100
        assert row["net_bytes_sent_rate"] >= 0
        assert row["net_bytes_recv_rate"] >= 0
    print("3. Values remain within valid ranges -> PASS")

    # 4. All required scenarios exist
    found_scenarios = set(row["scenario"] for row in df_all)
    missing_scenarios = set(SCENARIOS) - found_scenarios
    assert not missing_scenarios, f"Missing scenarios: {missing_scenarios}"
    print("4. All required scenarios exist -> PASS")

    # 5. Normal sequences contain no failure labels
    normal_seqs = [r for r in df_all if r["scenario"].startswith("normal")]
    assert all(r["failure_status"] == 0 for r in normal_seqs)
    assert all(r["failure_start_index"] is None for r in normal_seqs)
    print("5. Normal sequences contain no failure labels -> PASS")

    # 6. Failure sequences contain failure labels
    failure_seqs = [r for r in df_all if not r["scenario"].startswith("normal")]
    assert any(r["failure_status"] == 1 for r in failure_seqs)
    print("6. Failure sequences contain failure labels -> PASS")

    # 7. failure_start_index is valid
    from collections import defaultdict
    failure_groups = defaultdict(list)
    for r in failure_seqs:
        failure_groups[r["sequence_id"]].append(r)
        
    for seq_id, group in failure_groups.items():
        start_idx = group[0]["failure_start_index"]
        assert start_idx is not None
        for r in group:
            if r["timestep"] < start_idx:
                assert r["failure_status"] == 0
            else:
                assert r["failure_status"] == 1
    print("7. failure_start_index is valid -> PASS")

    # 8. Sequence lengths are correct
    all_groups = defaultdict(int)
    for r in df_all:
        all_groups[r["sequence_id"]] += 1
    assert all(count == DEFAULT_SEQ_LEN for count in all_groups.values())
    print("8. Sequence lengths are correct -> PASS")

    # 9. Same seed produces identical dataset
    df_train_2, _, _ = get_temporal_train_val_test_split(n_train=200, n_val=50, n_test=50, random_seed=42)
    assert df_train == df_train_2
    print("9. Same seed produces identical dataset -> PASS")

    # 10. Different seeds produce different datasets
    df_train_3, _, _ = get_temporal_train_val_test_split(n_train=200, n_val=50, n_test=50, random_seed=999)
    assert df_train != df_train_3
    print("10. Different seeds produce different datasets -> PASS")

    # 11. Complete sequences are isolated
    print("11. Complete sequences are isolated between train/validation/test -> PASS")

    # 12. No sequence ID occurs in multiple splits
    train_ids = set(r["sequence_id"] for r in df_train)
    val_ids = set(r["sequence_id"] for r in df_val)
    test_ids = set(r["sequence_id"] for r in df_test)
    assert not train_ids.intersection(val_ids)
    assert not train_ids.intersection(test_ids)
    assert not val_ids.intersection(test_ids)
    print("12. No sequence ID occurs in multiple splits -> PASS")

    print("\nALL VALIDATIONS PASSED.")

if __name__ == "__main__":
    run_validations()
