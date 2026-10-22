# Research Questions

## RQ1 — Anomaly Detection Under Multi-Scenario Telemetry
**How effectively can machine-learning-based anomaly detection identify cloud resource failures across diverse synthetic failure scenarios?**

The original Phase 2 system used Isolation Forest (contamination=0.2) evaluated against six controlled telemetry scenarios. This question is answered by the detection evaluation (evaluation_results.json, scenario_results.json).

## RQ2 — Temporal Feature Engineering for Early Warning
**Can temporal rolling features improve early-warning capability for gradual cloud resource failures compared with snapshot-level threshold monitoring?**

This question is answered by comparing the threshold baseline (which operates on current snapshots only) against the temporal predictive models. The early_warning_results.json records 18 early-warning events with a mean lead time of 18.06 steps.

## RQ3 — XAI for Operational Failure Attribution
**Can model-based coefficient attribution identify which temporal telemetry patterns most strongly influence a failure-risk prediction, and in what direction?**

This question is answered by the XAI case study (xai_case_study_results.json). The attribution method is deterministic LR coefficient × scaled feature value. Not SHAP/LIME.

## RQ4 — Connecting Prediction to Decision Logic
**Can a likely-failure-category classifier and rule-based decision engine translate temporal prediction outputs into appropriate autonomous recovery action selection?**

This question is answered by the integrated workflow demonstration. Evidence scores map XAI attributions to resource categories; decision rules select recovery actions.

## RQ5 — Post-Recovery Verification in an Integrated Workflow
**Can a post-recovery re-evaluation step using the same predictive model assess the effectiveness of a simulated healing action within an integrated cloud management workflow?**

This question is answered by the healing and verification layer in api.py. After a simulated recovery, a 10-step normal sequence is generated and re-evaluated by the same Logistic Regression model to produce RECOVERED / NOT_RECOVERED / INCONCLUSIVE verdicts.

---

## Boundary Conditions

**What this research does NOT answer:**
- Whether the system generalises to real production cloud infrastructure (it does not — telemetry is synthetic)
- Whether the likely-failure-category classifications establish mechanical causality (they do not)
- Whether the simulated recovery actions represent real orchestration (they do not)
- Whether Logistic Regression outperforms other models in aggregate (it does not — RF and GB have marginally higher mean AUC, but LR was selected for coefficient interpretability)
