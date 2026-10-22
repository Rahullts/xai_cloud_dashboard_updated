# Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform (Phase 3D: XAI)

## 1. Purpose
The XAI Decision Layer translates raw model probability arrays into actionable, interpretable cloud management decisions. It explains *why* the model predicts an impending failure, attempts to categorize the underlying root cause based on evidence, and maps that evidence to a safe recovery recommendation.

## 2. Architecture
The pipeline is strictly sequential and avoids any ground-truth leakage:
`Predictive Model` → `Decision Score` → `XAI Attribution` → `Evidence Aggregation` → `Likely Root Cause` → `Risk Assessment` → `Recommended Recovery Action`.

## 3. Model Explained
The currently integrated model is the **Logistic Regression** model identified in Phase 3C as optimal (Seed 42). It balances F1 (0.7268) and ROC-AUC (0.8299) while providing fully stable coefficients for linear local feature attribution.

## 4. Explanation Method
The explanation method calculates exact local log-odds contributions:
`Contribution = scaled_feature_value × model_coefficient`

This deterministic method is highly efficient, avoiding the dependency complexity of KernelSHAP while producing mathematically sound attributions for linear models.

## 5. Feature Attribution & Grouping
The 45 temporal features are mapped into 4 resource groups:
- `CPU` (e.g. `cpu_percent_std_10` -> "Cpu 10-step variability")
- `Memory` (e.g. `memory_percent_slope_5` -> "Memory 5-step trend")
- `Disk` (e.g. `disk_percent_delta_10` -> "Disk 10-step delta")
- `Network` (e.g. `net_bytes_recv_rate_mean_10` -> "Network Recv 10-step average")

## 6. Root-Cause Reasoning
Positive feature contributions (features pushing the prediction toward `1 = Failure`) are aggregated by their resource groups. The layer calculates a normalized evidence score.
- If one group holds >45% of evidence and leads by >15%, the system diagnoses a specific component failure (e.g., `CPU Spike`).
- If multiple groups share >30% evidence each, it returns `Combined Failure`.
- Otherwise, it falls back to `Unknown / Mixed`.

## 7. Risk Classification
Prediction probabilities are bucketed into actionable risk tiers:
- `< 0.30`: LOW
- `0.30 - 0.59`: MEDIUM
- `0.60 - 0.84`: HIGH
- `≥ 0.85`: CRITICAL

## 8. Recovery Decision Mapping
Root causes map cleanly to automated actions:
- `CPU Spike` → Scale CPU / restart affected workload
- `Memory Leak` → Restart affected service / reclaim memory
- `Disk Exhaustion` → Clean temporary data / expand storage
- `Network Degradation` → Check/restart network service / reroute where applicable
- `Combined Failure` → Controlled recovery sequence + alert
- `Unknown / Mixed` → Alert operator and avoid unsafe autonomous action

## 9. Leakage Prevention
The explainer operates *strictly* on the 45 prediction features. Metadata fields (`failure_status`, `target_failure_within_10`, `failure_start_index`) are excluded, ensuring explanations represent pure inference based on simulated real-world telemetry arrays.

## 10. Test Methodology & Case Studies
A full suite of unit tests (`test_xai_layer.py`) verifies the mathematical bounds of the pipeline. Additionally, `xai_case_study.py` processes raw test-set rows through the live model, ensuring explanations accurately describe the model's inner mechanics without accessing test labels.

## 11. Limitations
The XAI layer identifies influential model features and aggregates them into evidence for a likely failure category. **It does not establish causal relationships.** The validation uses controlled synthetic telemetry rather than production cloud telemetry. Occasional misclassifications (e.g. diagnosing a CPU failure as a Memory Leak due to random correlated noise) accurately reflect the underlying model's confusion, proving the XAI is honestly reporting the model's logic.
