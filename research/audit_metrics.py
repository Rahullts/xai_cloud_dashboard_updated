import json
import os

def run_audit():
    print("=== 1. DATASET COUNTS (results/evaluation_audit.json) ===")
    with open("results/evaluation_audit.json") as f:
        audit = json.load(f)
    print("Sequence counts:", audit.get("sequence_counts"))
    print("Row counts:", audit.get("row_counts"))
    print("Overlap checks:", audit.get("overlap_checks"))
    print("Scenario support total:", audit.get("scenario_support_total"))

    print("\n=== 2. ISOLATION FOREST SNAPSHOT (results/evaluation_results.json) ===")
    with open("results/evaluation_results.json") as f:
        er = json.load(f)
    print("Baseline:", er["baseline_metrics"])
    print("Isolation Forest:", er["isolation_forest_metrics"])

    print("\n=== 3. 5-SEED TEMPORAL PREDICTIVE (results/predictive_model_results.json) ===")
    with open("results/predictive_model_results.json") as f:
        pm = json.load(f)
    print("Seeds evaluated:", pm.get("seeds_evaluated"))
    for model, m in pm["model_summary_mean_std"].items():
        print(f"\nModel: {model}")
        print(f"  F1: {m.get('f1_score_mean', 0):.4f} +/- {m.get('f1_score_std', 0):.4f}")
        print(f"  ROC-AUC: {m.get('roc_auc_mean', 0):.4f} +/- {m.get('roc_auc_std', 0):.4f}")
        print(f"  PR-AUC: {m.get('pr_auc_mean', 0):.4f} +/- {m.get('pr_auc_std', 0):.4f}")
        print(f"  Precision: {m.get('precision_mean', 0):.4f} +/- {m.get('precision_std', 0):.4f}")
        print(f"  Recall: {m.get('recall_mean', 0):.4f} +/- {m.get('recall_std', 0):.4f}")

    print("\n=== 4. EARLY WARNING LEAD TIME (results/early_warning_results.json) ===")
    with open("results/early_warning_results.json") as f:
        ew = json.load(f)
    print(ew)

    print("\n=== 5. PER-SCENARIO LOGISTIC REGRESSION SEED 42 (results/predictive_scenario_results.json) ===")
    with open("results/predictive_scenario_results.json") as f:
        ps = json.load(f)
    for sc, v in ps.items():
        print(f"  {sc:25s} | Supp: {v['support']:3d} | P: {v['precision']:.3f} | R: {v['recall']:.3f} | F1: {v['f1_score']:.3f} | CM: {v['confusion_matrix']}")

    print("\n=== 6. XAI CASE STUDIES (results/xai_case_study_results.json) ===")
    with open("results/xai_case_study_results.json") as f:
        xai = json.load(f)
    for cs in xai:
        print(f"  {cs['sequence_id']}: scenario={cs['scenario']}, score={cs['model_score']:.4f}, likely={cs['likely_root_cause']}, rec_action={cs.get('recommended_action')}")
        for feat in cs.get("top_features", [])[:3]:
            print(f"      {feat['feature']}: contrib={feat['contribution']:.4f}, dir={feat['direction']}")

if __name__ == "__main__":
    run_audit()
