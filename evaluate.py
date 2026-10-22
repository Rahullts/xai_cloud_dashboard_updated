# evaluate.py
import json
import os
import time
import numpy as np
import warnings
from dataset import get_train_val_test_split
from detector import train_model

warnings.filterwarnings("ignore")

def evaluate_predictions(y_true, y_pred):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1_score": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "false_positive_rate": round(fp / (fp + tn) if (fp + tn) > 0 else 0, 4),
        "confusion_matrix": {"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)}
    }

def baseline_predict(meta_list):
    preds = []
    for m in meta_list:
        if (m["cpu_percent"] > 85 or 
            m["memory_percent"] > 85 or 
            m["disk_percent"] > 85 or 
            m["net_bytes_sent"] > 40 or 
            m["net_bytes_recv"] > 40):
            preds.append(1)
        else:
            preds.append(0)
    return preds

def run_single_experiment(random_seed, verbose=False):
    X_train, X_val, X_test, y_train, y_val, y_test, meta_train, meta_val, meta_test = get_train_val_test_split(
        n_train=1200, n_val=400, n_test=400, random_seed=random_seed
    )
    
    contaminations = [0.05, 0.10, 0.15, 0.20]
    best_f1 = -1
    best_contam = None
    
    import sys
    class DummyWriter:
        def write(self, _): pass
        def flush(self): pass
    old_stdout = sys.stdout
    sys.stdout = DummyWriter()
    
    for c in contaminations:
        model = train_model(X_train=X_train, contamination=c)
        raw_preds = model.predict(X_val)
        val_preds = [1 if p == -1 else 0 for p in raw_preds]
        
        val_results = evaluate_predictions(y_val, val_preds)
        if val_results["f1_score"] > best_f1:
            best_f1 = val_results["f1_score"]
            best_contam = c
            
    final_model = train_model(X_train=X_train, contamination=best_contam)
    sys.stdout = old_stdout
    
    if verbose:
        print(f"  Selected optimal contamination on validation set: {best_contam} (Validation F1: {best_f1})")

    start_time = time.time()
    raw_preds = final_model.predict(X_test)
    test_preds = [1 if p == -1 else 0 for p in raw_preds]
    ml_time = time.time() - start_time
    
    ml_results = evaluate_predictions(y_test, test_preds)
    ml_results["detection_time_sec"] = round(ml_time, 4)
    ml_results["best_contamination"] = best_contam
    
    start_time = time.time()
    base_preds = baseline_predict(meta_test)
    base_time = time.time() - start_time
    base_results = evaluate_predictions(y_test, base_preds)
    base_results["detection_time_sec"] = round(base_time, 4)
    
    return ml_results, base_results, test_preds, meta_test, y_test

def run_evaluation():
    print("Running Phase 2B.2 Validation and Repeated Experiments...\n")
    
    seeds = [42, 123, 456, 789, 2026]
    repeated_ml_results = []
    repeated_base_results = []
    
    for seed in seeds:
        print(f"Running experiment for seed={seed}...")
        ml_res, base_res, test_preds, meta_test, y_test = run_single_experiment(seed, verbose=(seed==42))
        repeated_ml_results.append(ml_res)
        repeated_base_results.append(base_res)
        
        if seed == 42:
            scenarios = ["normal", "cpu_spike", "memory_leak", "disk_full", "network_issue", "combined"]
            scenario_eval = {}
            for sc in scenarios:
                idx = [i for i, m in enumerate(meta_test) if m.get("scenario", m.get("label_str", sc)) == sc]
                if not idx:
                    continue
                sc_y_true = [y_test[i] for i in idx]
                sc_y_pred = [test_preds[i] for i in idx]
                if sc_y_true:
                    sc_res = evaluate_predictions(sc_y_true, sc_y_pred)
                    sc_res["support"] = len(idx)
                    scenario_eval[sc] = sc_res
                
            os.makedirs("results", exist_ok=True)
            with open(os.path.join("results", "scenario_results.json"), "w") as f:
                json.dump(scenario_eval, f, indent=4)
                
            eval_output = {
                "dataset": {
                    "train_size": 1200,
                    "val_size": 400,
                    "test_size": 400,
                    "random_seed": 42
                },
                "model_configuration": {
                    "algorithm": "IsolationForest",
                    "preprocessing": "StandardScaler",
                    "best_contamination": ml_res["best_contamination"]
                },
                "baseline_metrics": base_res,
                "isolation_forest_metrics": ml_res
            }
            with open(os.path.join("results", "evaluation_results.json"), "w") as f:
                json.dump(eval_output, f, indent=4)

    def compute_stats(results_list):
        keys = ["accuracy", "precision", "recall", "f1_score", "false_positive_rate"]
        stats = {}
        for k in keys:
            vals = [r[k] for r in results_list]
            stats[f"{k}_mean"] = round(float(np.mean(vals)), 4)
            stats[f"{k}_std"] = round(float(np.std(vals)), 4)
        return stats
        
    rep_output = {
        "seeds_tested": seeds,
        "isolation_forest_stats": compute_stats(repeated_ml_results),
        "baseline_stats": compute_stats(repeated_base_results),
        "individual_runs": {
            str(seed): {"ml": ml_res, "base": base_res}
            for seed, ml_res, base_res in zip(seeds, repeated_ml_results, repeated_base_results)
        }
    }
    
    with open(os.path.join("results", "repeated_experiment_results.json"), "w") as f:
        json.dump(rep_output, f, indent=4)
        
    print("\n" + "="*50)
    print("  REPEATED EXPERIMENT RESULTS (5 SEEDS)")
    print("="*50)
    print("\n--- BASELINE (Mean ± Std) ---")
    for k, v in rep_output["baseline_stats"].items():
        if "_mean" in k:
            base_k = k.replace("_mean", "")
            std = rep_output["baseline_stats"][base_k + "_std"]
            print(f"  {base_k:<20}: {v:.4f} ± {std:.4f}")

    print("\n--- ISOLATION FOREST (Mean ± Std) ---")
    for k, v in rep_output["isolation_forest_stats"].items():
        if "_mean" in k:
            base_k = k.replace("_mean", "")
            std = rep_output["isolation_forest_stats"][base_k + "_std"]
            print(f"  {base_k:<20}: {v:.4f} ± {std:.4f}")
            
    print("\n[DONE] All experiments finished. Validation logic prevents data leakage.")

if __name__ == "__main__":
    run_evaluation()
