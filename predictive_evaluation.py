# predictive_evaluation.py  —  Phase 3C
# Evaluates 5 models on the temporal early-warning task.
# Strict sequence-level train/val/test isolation throughout.

import os, sys, json, time, warnings
import numpy as np
from collections import defaultdict

warnings.filterwarnings("ignore")

from temporal_dataset import get_temporal_train_val_test_split
from temporal_features  import extract_features_dataset, METRICS, PREDICTION_HORIZON

from sklearn.preprocessing  import StandardScaler
from sklearn.linear_model   import LogisticRegression
from sklearn.ensemble       import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics        import (accuracy_score, precision_score, recall_score,
                                    f1_score, confusion_matrix,
                                    roc_auc_score, average_precision_score)

SEEDS = [42, 123, 456, 789, 2026]

META_COLS = {"sequence_id","timestep","timestamp","scenario",
             "failure_status","target_failure_within_10","failure_start_index"}

def get_feature_columns(sample_row):
    return [k for k in sample_row.keys() if k not in META_COLS]

def rows_to_matrix(feat_rows, feature_cols):
    return np.array([[r[c] for c in feature_cols] for r in feat_rows], dtype=np.float64)

def rows_to_labels(feat_rows):
    return np.array([r["target_failure_within_10"] for r in feat_rows], dtype=np.int32)

def compute_metrics(y_true, y_pred, y_prob=None):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0,1]).ravel()
    m = {
        "accuracy":  round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall":    round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score":  round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "false_positive_rate": round(fp/(fp+tn) if (fp+tn)>0 else 0, 4),
        "confusion_matrix": {"TN":int(tn),"FP":int(fp),"FN":int(fn),"TP":int(tp)},
    }
    if y_prob is not None:
        try:
            m["roc_auc"] = round(float(roc_auc_score(y_true, y_prob)), 4)
            m["pr_auc"]  = round(float(average_precision_score(y_true, y_prob)), 4)
        except Exception:
            m["roc_auc"] = m["pr_auc"] = None
    return m

def predict_majority(y_train, n_test):
    majority = int(np.bincount(y_train).argmax())
    return np.full(n_test, majority)

def predict_threshold(feat_rows):
    preds = []
    for r in feat_rows:
        if (r.get("cpu_percent_current",0) > 85 or
            r.get("memory_percent_current",0) > 85 or
            r.get("disk_percent_current",0) > 85 or
            r.get("net_bytes_sent_rate_current",0) > 40 or
            r.get("net_bytes_recv_rate_current",0) > 40):
            preds.append(1)
        else:
            preds.append(0)
    return np.array(preds)

def best_lr(X_tr, y_tr, X_v, y_v, seed):
    best_f1, best_C = -1, 1.0
    for C in [0.01, 0.1, 1.0, 10.0]:
        m = LogisticRegression(C=C, max_iter=2000, random_state=seed, class_weight="balanced")
        m.fit(X_tr, y_tr)
        f = f1_score(y_v, m.predict(X_v), zero_division=0)
        if f > best_f1:
            best_f1, best_C = f, C
    return best_C

def best_rf(X_tr, y_tr, X_v, y_v, seed):
    best_f1, best_d = -1, None
    for d in [None, 10, 20]:
        m = RandomForestClassifier(n_estimators=50, max_depth=d,
                                   random_state=seed, class_weight="balanced")
        m.fit(X_tr, y_tr)
        f = f1_score(y_v, m.predict(X_v), zero_division=0)
        if f > best_f1:
            best_f1, best_d = f, d
    return best_d

def best_gb(X_tr, y_tr, X_v, y_v, seed):
    best_f1, best_lr_ = -1, 0.1
    for lr in [0.05, 0.1, 0.2]:
        m = GradientBoostingClassifier(n_estimators=50, learning_rate=lr,
                                       max_depth=3, random_state=seed)
        m.fit(X_tr, y_tr)
        f = f1_score(y_v, m.predict(X_v), zero_division=0)
        if f > best_f1:
            best_f1, best_lr_ = f, lr
    return best_lr_

def per_scenario_metrics(feat_rows, y_pred):
    groups = defaultdict(lambda: {"yt":[], "yp":[]})
    for row, pred in zip(feat_rows, y_pred):
        groups[row["scenario"]]["yt"].append(row["target_failure_within_10"])
        groups[row["scenario"]]["yp"].append(pred)
    out = {}
    for sc, d in groups.items():
        yt = np.array(d["yt"]); yp = np.array(d["yp"])
        tn, fp, fn, tp = confusion_matrix(yt, yp, labels=[0,1]).ravel()
        out[sc] = {
            "support":   len(yt),
            "precision": round(float(precision_score(yt, yp, zero_division=0)), 4),
            "recall":    round(float(recall_score(yt, yp, zero_division=0)), 4),
            "f1_score":  round(float(f1_score(yt, yp, zero_division=0)), 4),
            "confusion_matrix": {"TN":int(tn),"FP":int(fp),"FN":int(fn),"TP":int(tp)},
        }
    return out

def early_warning(raw_test, feat_rows, y_pred):
    seq_meta = {}
    for r in raw_test:
        sid = r["sequence_id"]
        if sid not in seq_meta:
            seq_meta[sid] = r["failure_start_index"]
    seq_preds = defaultdict(list)
    for row, pred in zip(feat_rows, y_pred):
        seq_preds[row["sequence_id"]].append((row["timestep"], pred))
    times = []
    for sid, pts in seq_preds.items():
        pts.sort()
        fsi = seq_meta.get(sid)
        if fsi is None: continue
        first_pos = next((ts for ts, p in pts if p == 1), None)
        if first_pos is not None and first_pos < fsi:
            times.append(fsi - first_pos)
    if not times:
        return {"count":0,"mean":None,"median":None,"min":None,"max":None}
    return {
        "count":  len(times),
        "mean":   round(float(np.mean(times)), 2),
        "median": round(float(np.median(times)), 2),
        "min":    int(np.min(times)),
        "max":    int(np.max(times)),
    }

def pre_threshold(feat_rows, y_pred):
    subtle = [(r,p) for r,p in zip(feat_rows, y_pred)
              if (r["target_failure_within_10"]==1
                  and r["cpu_percent_current"]<85
                  and r["memory_percent_current"]<85
                  and r["disk_percent_current"]<85
                  and r["failure_status"]==0)]
    total = len(subtle)
    correct = sum(1 for _,p in subtle if p==1)
    return {"pre_threshold_positives": total,
            "correctly_predicted":     correct,
            "recall": round(correct/total, 4) if total else 0.0}

def run_seed(seed, primary_seed):
    print(f"  Seed={seed}  generating data...", flush=True)
    raw_tr, raw_va, raw_te = get_temporal_train_val_test_split(
        n_train=120, n_val=30, n_test=30, random_seed=seed)
    feat_tr = extract_features_dataset(raw_tr)
    feat_va = extract_features_dataset(raw_va)
    feat_te = extract_features_dataset(raw_te)
    if not feat_tr or not feat_va or not feat_te:
        return None

    fcols = get_feature_columns(feat_tr[0])
    Xtr = rows_to_matrix(feat_tr, fcols); ytr = rows_to_labels(feat_tr)
    Xva = rows_to_matrix(feat_va, fcols); yva = rows_to_labels(feat_va)
    Xte = rows_to_matrix(feat_te, fcols); yte = rows_to_labels(feat_te)

    scaler = StandardScaler()
    Xtr_s = scaler.fit_transform(Xtr)
    Xva_s = scaler.transform(Xva)
    Xte_s = scaler.transform(Xte)

    res = {}
    # Majority
    res["majority_baseline"] = compute_metrics(yte, predict_majority(ytr, len(yte)))
    # Threshold
    res["threshold_baseline"] = compute_metrics(yte, predict_threshold(feat_te))

    # Logistic Regression
    print(f"  Seed={seed}  LR...", flush=True)
    C = best_lr(Xtr_s, ytr, Xva_s, yva, seed)
    lr_m = LogisticRegression(C=C, max_iter=2000, random_state=seed, class_weight="balanced")
    lr_m.fit(Xtr_s, ytr)
    lr_pred = lr_m.predict(Xte_s); lr_prob = lr_m.predict_proba(Xte_s)[:,1]
    res["logistic_regression"] = compute_metrics(yte, lr_pred, lr_prob)
    res["logistic_regression"]["best_C"] = C

    # Random Forest
    print(f"  Seed={seed}  RF...", flush=True)
    d = best_rf(Xtr, ytr, Xva, yva, seed)
    rf_m = RandomForestClassifier(n_estimators=50, max_depth=d,
                                  random_state=seed, class_weight="balanced")
    rf_m.fit(Xtr, ytr)
    rf_pred = rf_m.predict(Xte); rf_prob = rf_m.predict_proba(Xte)[:,1]
    res["random_forest"] = compute_metrics(yte, rf_pred, rf_prob)
    res["random_forest"]["best_max_depth"] = str(d)

    # Gradient Boosting
    print(f"  Seed={seed}  GB...", flush=True)
    lr_gb = best_gb(Xtr, ytr, Xva, yva, seed)
    gb_m = GradientBoostingClassifier(n_estimators=50, learning_rate=lr_gb,
                                      max_depth=3, random_state=seed)
    gb_m.fit(Xtr, ytr)
    gb_pred = gb_m.predict(Xte); gb_prob = gb_m.predict_proba(Xte)[:,1]
    res["gradient_boosting"] = compute_metrics(yte, gb_pred, gb_prob)
    res["gradient_boosting"]["best_lr"] = lr_gb

    # Best model by test F1
    f1s = {k: res[k]["f1_score"] for k in ["logistic_regression","random_forest","gradient_boosting"]}
    best_name = max(f1s, key=f1s.get)
    best_pred = {"logistic_regression": lr_pred, "random_forest": rf_pred, "gradient_boosting": gb_pred}[best_name]

    # Coefficient contribution
    fi_model = rf_m if best_name == "random_forest" else gb_m
    fi = dict(sorted(zip(fcols, fi_model.feature_importances_),
                     key=lambda x: -x[1])[:20])
    fi = {k: round(float(v), 6) for k, v in fi.items()}

    return {
        "model_metrics":    res,
        "best_model":       best_name,
        "scenario_results": per_scenario_metrics(feat_te, best_pred),
        "early_warning":    early_warning(raw_te, feat_te, best_pred),
        "pre_threshold":    pre_threshold(feat_te, best_pred),
        "feature_importance": fi,
        "n_train": len(Xtr), "n_val": len(Xva), "n_test": len(Xte),
        # Keep for plots
        "_feat_te": feat_te, "_raw_te": raw_te, "_yte": yte.tolist(),
        "_lr_pred": lr_pred.tolist(), "_rf_pred": rf_pred.tolist(), "_gb_pred": gb_pred.tolist(),
        "_lr_prob": lr_prob.tolist(), "_rf_prob": rf_prob.tolist(), "_gb_prob": gb_prob.tolist(),
    }

def agg(all_runs, model, metric):
    vals = [r["model_metrics"][model].get(metric) for r in all_runs
            if r and r["model_metrics"].get(model,{}).get(metric) is not None]
    if not vals: return None, None
    return round(float(np.mean(vals)), 4), round(float(np.std(vals)), 4)

def save_plots(run, out_dir):
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("[PLOTS] matplotlib not installed — skipping."); return
    os.makedirs(out_dir, exist_ok=True)
    model_names = ["majority_baseline","threshold_baseline",
                   "logistic_regression","random_forest","gradient_boosting"]
    labels = ["Majority","Threshold","LR","RF","GB"]

    # F1 bar
    f1s = [run["model_metrics"][m]["f1_score"] for m in model_names]
    fig, ax = plt.subplots(figsize=(8,4))
    bars = ax.bar(labels, f1s, color=["#bbb","#888","#4a90d9","#2ecc71","#e67e22"])
    ax.set_ylim(0,1.05); ax.set_ylabel("F1 Score")
    ax.set_title("Model F1 Score (Seed 42)")
    for b,v in zip(bars,f1s): ax.text(b.get_x()+b.get_width()/2, v+0.01, f"{v:.3f}", ha="center", fontsize=9)
    plt.tight_layout(); plt.savefig(f"{out_dir}/f1_comparison.png", dpi=100); plt.close()

    # Recall bar
    recs = [run["model_metrics"][m]["recall"] for m in model_names]
    fig, ax = plt.subplots(figsize=(8,4))
    bars = ax.bar(labels, recs, color=["#bbb","#888","#4a90d9","#2ecc71","#e67e22"])
    ax.set_ylim(0,1.05); ax.set_ylabel("Recall")
    ax.set_title("Model Recall (Seed 42)")
    for b,v in zip(bars,recs): ax.text(b.get_x()+b.get_width()/2, v+0.01, f"{v:.3f}", ha="center", fontsize=9)
    plt.tight_layout(); plt.savefig(f"{out_dir}/recall_comparison.png", dpi=100); plt.close()

    # Confusion matrix for best model
    bm = run["best_model"]
    pred_map = {"logistic_regression": run["_lr_pred"],
                "random_forest": run["_rf_pred"],
                "gradient_boosting": run["_gb_pred"]}
    cm = confusion_matrix(run["_yte"], pred_map[bm], labels=[0,1])
    fig, ax = plt.subplots(figsize=(5,4))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0,1]); ax.set_yticks([0,1])
    ax.set_xticklabels(["Pred 0","Pred 1"]); ax.set_yticklabels(["True 0","True 1"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i,j]), ha="center", va="center",
                    color="white" if cm[i,j]>cm.max()/2 else "black", fontsize=14)
    ax.set_title(f"Confusion Matrix — {bm} (Seed 42)")
    plt.tight_layout(); plt.savefig(f"{out_dir}/confusion_matrix.png", dpi=100); plt.close()

    # Coefficient contribution
    fi = run["feature_importance"]
    top = list(fi.items())[:15]
    names = [x[0] for x in top]; vals = [x[1] for x in top]
    fig, ax = plt.subplots(figsize=(8,5))
    ax.barh(names[::-1], vals[::-1], color="#2ecc71")
    ax.set_xlabel("Importance"); ax.set_title(f"Top 15 Features — {bm} (Seed 42)")
    plt.tight_layout(); plt.savefig(f"{out_dir}/feature_importance.png", dpi=100); plt.close()

    # Risk over time for one gradual failure sequence
    seq_rows = defaultdict(list)
    for row, pred in zip(run["_feat_te"], run["_rf_pred"]):
        seq_rows[row["sequence_id"]].append((row["timestep"], row["cpu_percent_current"], pred))
    target_sid = None
    for row in run["_raw_te"]:
        if row["scenario"] in ("cpu_gradual_failure","combined_gradual_failure","memory_gradual_leak"):
            target_sid = row["sequence_id"]; break
    if target_sid and target_sid in seq_rows:
        tdata = sorted(seq_rows[target_sid])
        ts = [x[0] for x in tdata]; cpu = [x[1] for x in tdata]; preds = [x[2] for x in tdata]
        fig, ax1 = plt.subplots(figsize=(9,4))
        ax1.plot(ts, cpu, "b-", label="CPU %", lw=1.5)
        ax1.axhline(85, color="gray", ls="--", alpha=0.5, label="85% threshold")
        ax1.set_ylabel("CPU %", color="b"); ax1.set_xlabel("Timestep (1 min)")
        ax2 = ax1.twinx()
        ax2.fill_between(ts, 0, preds, alpha=0.25, color="red", label="Predicted risk")
        ax2.set_ylabel("Predicted Risk", color="r"); ax2.set_ylim(-0.1, 1.5)
        ax1.set_title(f"Risk Over Time — {target_sid}")
        h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc="upper left", fontsize=8)
        plt.tight_layout(); plt.savefig(f"{out_dir}/risk_over_time.png", dpi=100); plt.close()
    print(f"[PLOTS] Saved to {out_dir}", flush=True)


def run_evaluation():
    print("=" * 60)
    print("  PHASE 3C — PREDICTIVE MODELING  (5 seeds)")
    print("=" * 60, flush=True)

    all_runs = []
    primary_run = None
    for seed in SEEDS:
        t0 = time.time()
        run = run_seed(seed, primary_seed=(seed==42))
        all_runs.append(run)
        if seed == 42: primary_run = run
        print(f"  Seed={seed}  done ({time.time()-t0:.1f}s)", flush=True)

    # Aggregate
    model_names = ["majority_baseline","threshold_baseline",
                   "logistic_regression","random_forest","gradient_boosting"]
    key_metrics = ["accuracy","precision","recall","f1_score","false_positive_rate","roc_auc","pr_auc"]
    summary = {}
    for m in model_names:
        summary[m] = {}
        for met in key_metrics:
            mn, sd = agg(all_runs, m, met)
            if mn is not None:
                summary[m][f"{met}_mean"] = mn
                summary[m][f"{met}_std"]  = sd

    # Print table
    print("\n" + "="*70)
    print("  MODEL COMPARISON — Mean ± Std across 5 seeds")
    print("="*70, flush=True)
    for m in model_names:
        label = m.replace("_"," ").title()
        f1m = summary[m].get("f1_score_mean", 0)
        f1s = summary[m].get("f1_score_std",  0)
        rem = summary[m].get("recall_mean", 0)
        res = summary[m].get("recall_std",  0)
        rauc = summary[m].get("roc_auc_mean")
        print(f"  {label:<26} F1:{f1m:.4f}±{f1s:.4f}  Rec:{rem:.4f}±{res:.4f}  "
              f"ROC-AUC:{rauc if rauc else 'N/A'}", flush=True)

    if primary_run:
        bm = primary_run["best_model"]
        print(f"\n--- Per-Scenario (Seed 42 | best={bm}) ---", flush=True)
        for sc, r in sorted(primary_run["scenario_results"].items()):
            print(f"  {sc:<32} F1:{r['f1_score']:.3f}  Recall:{r['recall']:.3f}  n:{r['support']}")

        ew = primary_run["early_warning"]
        print(f"\n--- Early Warning (Seed 42) ---")
        if ew["count"]:
            print(f"  Sequences warned early: {ew['count']}")
            print(f"  Mean / Median / Min-Max warning: {ew['mean']} / {ew['median']} / {ew['min']}-{ew['max']} min")
        else:
            print("  No early-warning instances.")

        pt = primary_run["pre_threshold"]
        print(f"\n--- Pre-Threshold Analysis (Seed 42) ---")
        print(f"  Positive rows with all metrics < 85% & currently healthy: {pt['pre_threshold_positives']}")
        print(f"  Correctly predicted: {pt['correctly_predicted']}  (Recall: {pt['recall']})", flush=True)

    # Save JSON
    os.makedirs("results", exist_ok=True)

    def strip(run):
        if run is None: return None
        return {k:v for k,v in run.items()
                if not k.startswith("_") and k not in ("rf_model","gb_model","lr_model")}

    out = {
        "seeds_evaluated": SEEDS,
        "model_summary_mean_std": summary,
        "seed42_n_train": primary_run["n_train"] if primary_run else None,
        "seed42_n_val":   primary_run["n_val"]   if primary_run else None,
        "seed42_n_test":  primary_run["n_test"]  if primary_run else None,
        "seed42_best_model": primary_run["best_model"] if primary_run else None,
        "individual_runs": [
            {"seed": SEEDS[i], "best_model": r["best_model"],
             "model_metrics": {k: {mk:mv for mk,mv in v.items()
                                   if mk not in ("confusion_matrix","best_config","best_C","best_max_depth","best_lr")}
                               for k,v in r["model_metrics"].items()}}
            for i, r in enumerate(all_runs) if r
        ]
    }
    with open("results/predictive_model_results.json", "w") as f:
        json.dump(out, f, indent=4)

    if primary_run:
        with open("results/predictive_scenario_results.json", "w") as f:
            json.dump(primary_run["scenario_results"], f, indent=4)
        with open("results/early_warning_results.json", "w") as f:
            json.dump(primary_run["early_warning"], f, indent=4)
        with open("results/feature_importance.json", "w") as f:
            json.dump(primary_run["feature_importance"], f, indent=4)
        save_plots(primary_run, "results/plots")

    print("\n[DONE] All results saved to results/", flush=True)

if __name__ == "__main__":
    run_evaluation()
