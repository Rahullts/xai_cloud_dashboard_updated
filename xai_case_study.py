import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from temporal_dataset import get_temporal_train_val_test_split
from temporal_features import extract_features_dataset
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from xai_explainer import get_feature_attributions
from root_cause import determine_root_cause
from decision_engine import get_risk_level, get_recommended_action, generate_explanation

def run_case_study():
    # 1. Recreate exact Phase 3C Seed 42 Model
    raw_tr, raw_va, raw_te = get_temporal_train_val_test_split(n_train=120, n_val=30, n_test=30, random_seed=42)
    feat_tr = extract_features_dataset(raw_tr)
    feat_te = extract_features_dataset(raw_te)
    
    META = {'sequence_id','timestep','timestamp','scenario','failure_status',
            'target_failure_within_10','failure_start_index'}
    fcols = [k for k in feat_tr[0].keys() if k not in META]
    
    Xtr = np.array([[r[c] for c in fcols] for r in feat_tr])
    ytr = np.array([r['target_failure_within_10'] for r in feat_tr])
    Xte = np.array([[r[c] for c in fcols] for r in feat_te])
    
    scaler = StandardScaler()
    Xtr_s = scaler.fit_transform(Xtr)
    
    # Phase 3C selected C=1.0 for Seed 42 Logistic Regression
    model = LogisticRegression(C=1.0, max_iter=2000, random_state=42, class_weight='balanced')
    model.fit(Xtr_s, ytr)
    
    # 2. Select representative examples from test set
    scenarios_to_find = [
        "cpu_gradual_failure",
        "memory_gradual_leak",
        "disk_gradual_exhaustion",
        "network_degradation",
        "combined_gradual_failure",
        "cpu_sudden_failure"
    ]
    
    case_study_results = []
    found_scenarios = set()
    
    for row in feat_te:
        sc = row['scenario']
        # We want rows that are pre-failure but have high probability of failure
        # to show the XAI layer working on predictive early-warnings.
        if sc in scenarios_to_find and sc not in found_scenarios:
            if row['target_failure_within_10'] == 1 and row['failure_status'] == 0:
                
                # Get Prediction Probability
                raw_vector = np.array([[row[c] for c in fcols]])
                prob = float(model.predict_proba(scaler.transform(raw_vector))[0, 1])
                
                if prob > 0.5:  # Only pick confident early warnings
                    # Run Pipeline
                    attributions = get_feature_attributions(model, scaler, fcols, row)
                    root_cause, evidence_scores = determine_root_cause(attributions)
                    action = get_recommended_action(root_cause)
                    explanation = generate_explanation(prob, root_cause, attributions)
                    
                    case_study_results.append({
                        "sequence_id": row["sequence_id"],
                        "timestep": row["timestep"],
                        "scenario": sc,
                        "model_score": round(prob, 4),
                        "likely_root_cause": root_cause,
                        "recommended_recovery_action": action,
                        "explanation_text": explanation,
                        "top_5_contributing_features": [
                            {
                                "feature": a["feature"],
                                "human_readable": a["human_readable_name"],
                                "contribution": round(a["contribution"], 4)
                            }
                            for a in attributions[:5]
                        ],
                        "evidence_scores": {k: round(v, 4) for k, v in evidence_scores.items()}
                    })
                    
                    found_scenarios.add(sc)
                    
    # Save results
    with open("results/xai_case_study_results.json", "w") as f:
        json.dump(case_study_results, f, indent=4)
        
    print(f"Generated case study for {len(case_study_results)} examples.")

if __name__ == "__main__":
    run_case_study()
