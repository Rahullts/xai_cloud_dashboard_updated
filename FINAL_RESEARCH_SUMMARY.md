# Final Research Summary

## 1. Problem Statement
Modern cloud infrastructure experiences diverse failure modes (CPU spikes, memory leaks, disk exhaustion) that are traditionally monitored using static thresholds. This reactive approach often fails to identify failures until they reach a critical state, causing service degradation and delayed recovery operations.

## 2. Research Objective
To implement and evaluate an integrated platform that combines temporal cloud telemetry monitoring, machine-learning-based failure-risk prediction, interpretable feature-level explanation, evidence-based failure categorization, autonomous recovery decision logic, and simulated recovery verification within a unified system.

## 3. System Architecture
The system consists of a REST API backend utilizing a 10-timestep sliding window of system telemetry, connected to a deterministic Logistic Regression model. The pipeline extracts temporal features, generates predictions, interprets those predictions via linear coefficient attribution (XAI), maps the attributions to likely root causes, triggers simulated healing actions, and explicitly verifies post-healing recovery states. A stateless HTML/JS dashboard consumes these outputs.

## 4. Dataset Methodology
A controlled synthetic temporal cloud-monitoring dataset was generated representing 60-timestep sequences (simulated minutes). The dataset explicitly defines both gradual degradation scenarios (e.g., memory leak) and sudden failures (e.g., sudden CPU spike). The sequences are independently partitioned into 120 Training, 30 Validation, and 30 Test sequences to enforce strict temporal isolation without lookahead leakage.

## 5. Temporal Feature Engineering
Five base telemetry metrics (CPU, Memory, Disk, Network Sent, Network Receive) are transformed into 45 temporal features. For each base metric, 9 representations are computed dynamically over the sliding window: current value, 5-step and 10-step rolling means, deltas, slopes (linear trend), and standard deviations (variability).

## 6. Predictive Modeling
The primary integrated model is a Logistic Regression classifier (`C=1.0`, `class_weight='balanced'`) fitted on `StandardScaler` transformed features with a deterministic seed (`42`). The target label is a 10-step failure-risk prediction target (failure active now or within the following 10 timesteps).

## 7. Model Comparison
Gradient Boosting and Random Forest achieved slightly higher aggregate F1 and ROC-AUC scores during the 5-seed Phase 3C evaluation. However, Logistic Regression was selected as the integrated model because it provides competitive predictive performance together with perfectly transparent, local feature-level coefficient attribution.

## 8. XAI Methodology
The Explainable AI (XAI) layer calculates exactly how much each feature pushes the model toward or away from a failure prediction. It uses mathematically exact linear attribution: `scaled feature value × Logistic Regression coefficient`. 

## 9. Root-Cause Interpretation
Root-cause classification is an evidence-based interpretation of model behavior. The XAI contributions are aggregated across metric categories (e.g., all CPU-related features) to identify the highest positive influence driving the failure prediction. This does NOT establish a strict causal relationship, but rather the most likely category based on model evidence.

## 10. Self-Healing Decision Mechanism
Based on the identified root cause, the decision engine maps the category to a specific recovery action (e.g., Memory Leak -> "Restart affected service / reclaim memory"). High and Critical risk predictions autonomously trigger these simulated decisions.

## 11. Recovery Verification
Post-healing verification is natively simulated. Upon executing a healing action, the API simulates a restored normal telemetry sequence, re-extracts features, and executes a second prediction. The system verifies if the risk score strictly drops to LOW (RECOVERED), remains elevated (NOT_RECOVERED), or hovers at MEDIUM (INCONCLUSIVE).

## 12. Experimental Results
The system achieved an average F1-score of ~0.69 (Logistic Regression) across 5 independent seeds. Analysis confirmed that temporal historical features provide useful warning capability for gradual failure patterns, while sudden failures without preceding indicators remain difficult to predict. The model successfully identified early-warning signals for gradual failures an average of ~18 timesteps before absolute failure thresholds were breached.

## 13. Limitations
1. Controlled synthetic telemetry.
2. No production cloud deployment.
3. Synthetic distributions may not capture real-world cloud behavior.
4. Sudden failures are difficult to predict.
5. Root-cause classification is not causal proof.
6. Simulated healing is not production validation.
7. Model performance is dataset-dependent.
8. Logistic Regression was selected for interpretability despite Gradient Boosting having slightly stronger aggregate predictive metrics.
9. The current API prototype trains the deterministic model at startup.
10. The prediction target includes currently active failure as well as near-future failure.

## 14. Reproducibility
The methodology uses fixed random seeds, strict sequence-level train/validation/test separation, deterministic XAI attribution, and `StandardScaler` fitting strictly on training data. All historical JSON research results generated during the validation phases remain explicitly preserved.

## 15. Research Contribution
The contribution of this work is the implementation and evaluation of an integrated platform that combines temporal cloud telemetry monitoring, machine-learning-based failure-risk prediction, interpretable feature-level explanation, evidence-based failure categorization, autonomous recovery decision logic, and simulated recovery verification within a unified system.
