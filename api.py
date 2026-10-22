# =============================================================
# api.py -- Refactored for Phase 3E (Full System Integration)
# Serves the integrated temporal prediction + XAI pipeline
# =============================================================

import io
import sys
import traceback
import numpy as np
from flask import Blueprint, jsonify, request

from temporal_dataset import get_temporal_train_val_test_split, generate_sequence
from temporal_features import extract_features_dataset, METRICS, WINDOWS, _calculate_slope
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from decision_engine import get_risk_level, get_recommended_action, generate_explanation
from root_cause import determine_root_cause
from xai_explainer import get_feature_attributions
from healer import decide_and_heal

api_bp = Blueprint("api", __name__)

# --- Global Pipeline State ---
_model = None
_scaler = None
_fcols = None

_temporal_history = []
_scenario_state = {
    "scenario": None,
    "sequence": [],
    "index": 0
}

def init_api_model():
    """Train the Phase 3C Logistic Regression model on startup."""
    global _model, _scaler, _fcols
    if _model is not None:
        return
        
    print("[api] Training Phase 3C Logistic Regression model...")
    # Exact Phase 3C Seed 42 dataset size and seed
    raw_tr, raw_va, raw_te = get_temporal_train_val_test_split(n_train=120, n_val=30, n_test=30, random_seed=42)
    feat_tr = extract_features_dataset(raw_tr)
    
    META = {'sequence_id','timestep','timestamp','scenario','failure_status','target_failure_within_10','failure_start_index'}
    _fcols = [k for k in feat_tr[0].keys() if k not in META]
    
    Xtr = np.array([[r[c] for c in _fcols] for r in feat_tr])
    ytr = np.array([r['target_failure_within_10'] for r in feat_tr])
    
    _scaler = StandardScaler()
    Xtr_s = _scaler.fit_transform(Xtr)
    
    # Selected hyperparameters from Phase 3C Audit
    _model = LogisticRegression(C=1.0, max_iter=2000, random_state=42, class_weight='balanced')
    _model.fit(Xtr_s, ytr)
    print("[api] Model trained and ready.")

def extract_live_features(history):
    """Extract rolling features for the LIVE trailing row of the sliding window."""
    row_feat = {}
    current_row = history[-1]
    
    for metric in METRICS:
        row_feat[f"{metric}_current"] = current_row[metric]
        for w in WINDOWS:
            slice_history = [history[i][metric] for i in range(len(history) - w, len(history))]
            row_feat[f"{metric}_mean_{w}"] = round(float(np.mean(slice_history)), 4)
            row_feat[f"{metric}_delta_{w}"] = round(slice_history[-1] - slice_history[0], 4)
            row_feat[f"{metric}_slope_{w}"] = round(float(_calculate_slope(slice_history)), 4)
            row_feat[f"{metric}_std_{w}"] = round(float(np.std(slice_history)), 4)
            
    return row_feat

@api_bp.route("/api/scan", methods=["GET"])
def api_scan():
    """
    Main API endpoint for the dashboard.
    Steps forward through a temporal sequence and performs predictive XAI.
    """
    global _temporal_history
    init_api_model()

    scenario = request.args.get("scenario", "normal")

    # Map frontend dashboard scenarios to Phase 3A temporal scenarios
    scenario_map = {
        "normal": "normal_stable",
        "normal_stable": "normal_stable",
        "normal_variable": "normal_variable",
        "cpu_spike": "cpu_sudden_failure",
        "cpu": "cpu_sudden_failure",
        "cpu_sudden_failure": "cpu_sudden_failure",
        "cpu_gradual_failure": "cpu_gradual_failure",
        "memory_leak": "memory_gradual_leak",
        "memory": "memory_gradual_leak",
        "memory_gradual_leak": "memory_gradual_leak",
        "disk_full": "disk_gradual_exhaustion",
        "disk": "disk_gradual_exhaustion",
        "disk_gradual_exhaustion": "disk_gradual_exhaustion",
        "network_issue": "network_degradation",
        "network": "network_degradation",
        "network_degradation": "network_degradation",
        "combined": "combined_gradual_failure",
        "combined_gradual_failure": "combined_gradual_failure",
    }
    if scenario not in scenario_map:
        return jsonify({"error": f"Unsupported scenario: '{scenario}'."}), 400
    actual_scenario = scenario_map[scenario]
    
    try:
        # 1. Manage Sequence State
        if _scenario_state["scenario"] != actual_scenario or _scenario_state["index"] >= len(_scenario_state["sequence"]):
            print(f"[api] Resetting sequence to {actual_scenario}...")
            # Generate a 200-step sequence so the dashboard doesn't reset too frequently
            _scenario_state["sequence"] = generate_sequence(actual_scenario, f"live_{actual_scenario}", seq_len=200)
            _scenario_state["scenario"] = actual_scenario
            _scenario_state["index"] = 0
            _temporal_history.clear()
            
        current_telemetry = _scenario_state["sequence"][_scenario_state["index"]]
        _scenario_state["index"] += 1
        
        _temporal_history.append(current_telemetry)
        
        # Keep sliding window at exactly 10 (MAX_WINDOW = 10)
        if len(_temporal_history) > 10:
            _temporal_history.pop(0)
            
        # 2. Check Warm-up
        if len(_temporal_history) < 10:
            return jsonify({
                "scenario": scenario,
                "telemetry": current_telemetry,
                "prediction": {
                    "label": 0,
                    "risk_score": 0.0,
                    "risk_level": "WARMING_UP",
                    "status": "WARMING_UP"
                },
                "xai": {"top_features": []},
                "root_cause": {"category": "N/A", "evidence_score": 0.0, "supporting_features": []},
                "decision": {"recommended_action": "Wait for telemetry buffer to fill", "reason": "Insufficient temporal history"},
                "healing": {"status": "Skipped", "action": "None", "verification": "N/A"},
                "label": "NORMAL",
                "metrics": dict(current_telemetry, latency_ms=25.0),
                "score": 0.0,
                "explanation": "Warming up 10-step temporal buffer.",
                "actions": [],
                "recovery_mode": "simulation_only",
            })

        # 3. Extract Temporal Features
        live_features = extract_live_features(_temporal_history)
        
        # 4. Predict
        raw_vector = np.array([[live_features[c] for c in _fcols]])
        prob = float(_model.predict_proba(_scaler.transform(raw_vector))[0, 1])
        label = int(_model.predict(_scaler.transform(raw_vector))[0])
        
        risk_level = get_risk_level(prob)
        
        # 5. XAI Attribution
        attributions = get_feature_attributions(_model, _scaler, _fcols, live_features)
        
        # 6. Root Cause Decision
        root_cause, evidence_scores = determine_root_cause(attributions)
        recommended_action = get_recommended_action(root_cause)
        explanation = generate_explanation(prob, root_cause, attributions)
        
        # 7. Healing Simulation (If High Risk)
        healing_status = "Skipped"
        action_taken = "None"
        verification = "N/A"
        
        # Evidence objects for post-healing verify
        evidence_before = None
        evidence_after = None
        
        if risk_level in ["HIGH", "CRITICAL"]:
            evidence_before = {
                "risk_score": round(prob, 4),
                "risk_level": risk_level,
                "label": label
            }
            
            old_stdout = sys.stdout
            buffer = io.StringIO()
            try:
                sys.stdout = buffer
                decide_and_heal(recommended_action)
            finally:
                sys.stdout = old_stdout
            
            action_taken = recommended_action
            healing_status = "Executed"
            
            # --- POST-HEALING VERIFICATION SIMULATION ---
            # Generate a 10-step sequence of normal telemetry to represent the "recovered" state
            recovered_seq = generate_sequence("normal_stable", "post_healing_verify", seq_len=10)
            
            # Extract features on this recovered sequence
            post_features = extract_live_features(recovered_seq)
            
            # Predict post-healing risk
            raw_vector_post = np.array([[post_features[c] for c in _fcols]])
            prob_post = float(_model.predict_proba(_scaler.transform(raw_vector_post))[0, 1])
            label_post = int(_model.predict(_scaler.transform(raw_vector_post))[0])
            risk_level_post = get_risk_level(prob_post)
            
            evidence_after = {
                "risk_score": round(prob_post, 4),
                "risk_level": risk_level_post,
                "label": label_post
            }
            
            if risk_level_post == "LOW":
                verification = "RECOVERED"
            elif risk_level_post in ["HIGH", "CRITICAL"]:
                verification = "NOT_RECOVERED"
            else:
                verification = "INCONCLUSIVE"
            
            # Flush temporal history so the frontend organically falls into WARMING_UP
            # instead of instantly showing the old high-risk state on the next tick.
            _temporal_history.clear()

        # Format cleanly for the dashboard
        return jsonify({
            "scenario": scenario,
            "telemetry": current_telemetry,
            "prediction": {
                "label": label,
                "risk_score": round(prob, 4),
                "risk_level": risk_level,
                "status": "LIVE"
            },
            "xai": {
                "method": "Logistic Regression Linear Coefficient Attribution",
                "top_features": attributions[:5] # Send top 5
            },
            "root_cause": {
                "category": root_cause,
                "evidence_scores": evidence_scores,
                "explanation_text": explanation
            },
            "decision": {
                "recommended_action": recommended_action,
                "reason": "Risk thresholds exceeded for category" if risk_level in ["HIGH", "CRITICAL"] else "Monitoring normal variance"
            },
            "healing": {
                "status": healing_status,
                "action": action_taken,
                "verification": verification,
                "evidence": {
                    "before": evidence_before,
                    "after": evidence_after
                } if evidence_before else None
            },
            "label": "ANOMALY" if label == 1 else "NORMAL",
            "metrics": dict(current_telemetry, latency_ms=220.0 if "network" in scenario else 25.0),
            "score": round(prob, 4),
            "explanation": explanation,
            "actions": [{"action": recommended_action, "reason": "Model risk threshold exceeded"}] if risk_level in ["HIGH", "CRITICAL"] else [],
            "recovery_mode": "simulation_only"
        })
        
    except Exception as e:
        return jsonify({
            "error": "Backend exception",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500
