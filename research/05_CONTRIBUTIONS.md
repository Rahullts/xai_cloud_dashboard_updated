# Verified Contributions

These contributions are directly substantiated by the implementation and experimental evidence in this project. No contribution is stated unless it is backed by actual working code, actual results, or actual architectural decisions that can be demonstrated.

---

## C1 — End-to-End Integrated Workflow Prototype
The system implements a continuous pipeline: telemetry ingestion → anomaly detection → temporal feature extraction → multi-model failure prediction → XAI attribution → likely-failure-category inference → autonomous decision logic → simulated recovery → post-recovery verification. Each stage is implemented and callable through the Flask API. This integration is the primary architectural contribution; it is not merely a proposal.

## C2 — Temporal Feature Engineering Layer
A leak-free temporal feature set of 45 features is constructed from a 10-step sliding window over five raw telemetry metrics. Features include per-metric current value, rolling mean, delta, slope, and standard deviation over windows of 5 and 10 steps. The feature extraction is strictly applied to the trailing window of prior observations, preventing any future-value leakage.

## C3 — Comparative Predictive Evaluation
Three supervised classifiers (Logistic Regression, Random Forest, Gradient Boosting) are evaluated against two baselines (majority-class and current-value threshold) across five random seeds. The evaluation uses strict sequence-level splitting (120 train / 30 validation / 30 test sequences, confirmed zero overlap by the audit). All comparison numbers are drawn from predictive_model_results.json.

**Key comparative numbers (5-seed mean ± std):**
- Majority baseline F1: 0.514 ± 0.259
- Threshold baseline F1: 0.156 ± 0.054
- Logistic Regression F1: 0.692 ± 0.036, ROC-AUC: 0.813 ± 0.021
- Random Forest F1: 0.696 ± 0.021, ROC-AUC: 0.819 ± 0.005
- Gradient Boosting F1: 0.699 ± 0.030, ROC-AUC: 0.826 ± 0.013

*All three ML models substantially outperform both baselines. Differences among the three ML models are modest.*

## C4 — Model Selection Rationale for Interpretability
Logistic Regression is selected for the integrated prototype not because it achieves the highest aggregate F1 or AUC — it does not — but because its coefficient-based attribution is mathematically exact, deterministic, and directly interpretable without approximation methods. This is explicitly documented as a design decision rather than a performance claim.

## C5 — Deterministic XAI Attribution Layer
The system computes failure-risk attributions as (scaled feature value × LR coefficient) for each of the 45 features. This is deterministic and exact. The approach distinguishes positively contributing features (increasing failure probability) from negatively contributing features (decreasing failure probability). This is not SHAP and is not LIME; it is direct linear attribution applicable only to logistic regression.

## C6 — Early-Warning Capability
Among 18 evaluated failure-sequence test cases, the model issued at least one HIGH or CRITICAL prediction before the labelled failure onset in all qualifying cases. Mean lead time was 18.06 timesteps (median 16.0, min 4, max 33). This represents an improvement over the threshold-based baseline, which detected only 8.6% of failure events at recall. (Source: early_warning_results.json)

## C7 — Post-Recovery Verification Mechanism
After a simulated recovery action, the system generates a 10-step synthetic normal telemetry sequence and evaluates it using the same trained Logistic Regression model. The resulting risk level is compared against the pre-healing risk to produce a RECOVERED / NOT_RECOVERED / INCONCLUSIVE verdict. This prevents falsely claiming recovery without any evidence.

---

## What This Work Does NOT Claim

- It does not claim Logistic Regression is the best model for cloud failure prediction in general.
- It does not claim the likely-failure-category classification establishes mechanical causal proof.
- It does not claim real-world deployment or production cloud healing.
- It does not claim the synthetic telemetry accurately simulates all real infrastructure failure patterns.
- It does not claim the XAI attributions are human-validated or field-tested root-cause explanations.
