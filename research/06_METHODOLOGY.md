# Methodology

## 1. System Architecture Overview

The proposed system implements a pipeline of eight sequentially connected processing stages, each producing structured output consumed by the next stage. All stages are integrated in a single Flask application and are callable through the `/api/scan` endpoint.

```
Telemetry Source
       ↓
Stage 1: Anomaly Detection (Isolation Forest)
       ↓
Stage 2: Temporal Buffer (10-step sliding window)
       ↓
Stage 3: Temporal Feature Extraction (45 features)
       ↓
Stage 4: Failure Risk Prediction (Logistic Regression)
       ↓
Stage 5: XAI Attribution (Coefficient × Scaled Value)
       ↓
Stage 6: Likely Failure Category (Evidence Scoring)
       ↓
Stage 7: Autonomous Decision (Rule-Based Selection)
       ↓
Stage 8: Simulated Recovery + Post-Healing Verification
```

---

## 2. Telemetry Generation (Phase 1)

Telemetry is generated synthetically using six scenario profiles. Each scenario produces a 60-timestep sequence of five raw metrics:

| Metric | Description |
|---|---|
| cpu_percent | CPU utilisation (%) |
| memory_percent | Memory utilisation (%) |
| disk_percent | Disk utilisation (%) |
| net_bytes_sent_rate | Network transmit rate (MB/s) |
| net_bytes_recv_rate | Network receive rate (MB/s) |

### Scenarios
| Scenario Name | Type | Failure Pattern |
|---|---|---|
| normal_stable | Nominal | Steady low variance |
| normal_variable | Nominal | Higher natural variance |
| cpu_sudden_failure | Failure | Step-change CPU spike |
| cpu_gradual_failure | Failure | Gradual CPU ramp |
| memory_gradual_leak | Failure | Monotonic memory increase |
| disk_gradual_exhaustion | Failure | Gradual disk fill |
| network_degradation | Failure | Throughput and variability degradation |
| combined_gradual_failure | Failure | Multi-resource simultaneous degradation |

---

## 3. Anomaly Detection Layer (Phase 2)

Isolation Forest (IF) is trained on snapshot telemetry from the normal_stable scenario. Selected contamination parameter: 0.2. StandardScaler applied to raw features before fitting.

**Detection performance (snapshot-level):**
- Precision: 1.00, Recall: 0.83, F1: 0.76, ROC-AUC: N/A (unsupervised)
- False positive rate on normal data: 7.25%

The detection layer flags individual telemetry points as anomalous but cannot capture gradual-onset failure trajectories from a single snapshot.

---

## 4. Temporal Dataset Construction (Phase 3A)

A temporal dataset is constructed from 150 generated sequences (25 per scenario, each 60 timesteps long).

**Sliding window labelling:** For each timestep t in a sequence, a binary label is assigned. Label = 1 if the timestep falls within the labelled failure region OR within the 10 subsequent timesteps. Label = 0 otherwise. This creates early-warning sensitivity.

**Sequence-level splitting:**
- Training: 120 sequences → 4,920 supervised rows
- Validation: 30 sequences → 1,230 rows (Phase 3C audit: confirmed 30 val, 30 test)
- Test: 30 sequences → 1,230 rows
- Zero sequence overlap verified by audit (evaluation_audit.json)

---

## 5. Temporal Feature Engineering (Phase 3B)

From each 10-step trailing window, 45 features are extracted per timestep. For each of the 5 raw metrics, 9 features are computed:

| Feature Type | Windows |
|---|---|
| current | (single current value) |
| mean | 5-step, 10-step |
| delta | 5-step, 10-step |
| slope (linear regression) | 5-step, 10-step |
| std | 5-step, 10-step |

**Total:** 5 metrics × 9 features = **45 temporal features**

Features are constructed using strictly trailing observations. The feature extractor does not use future values. StandardScaler is fit only on training rows.

---

## 6. Predictive Model Comparison (Phase 3C)

Five models are evaluated across five random seeds {42, 123, 456, 789, 2026}:

1. Majority-class baseline
2. Current-value threshold baseline (>80% on any metric)
3. Logistic Regression (C=1.0, max_iter=2000, class_weight='balanced')
4. Random Forest (n_estimators=100, class_weight='balanced')
5. Gradient Boosting (n_estimators=100)

All supervised models use the same StandardScaler fit on training rows only. Evaluation metrics: accuracy, precision, recall, F1, ROC-AUC, PR-AUC.

---

## 7. Model Selection for Integration

Logistic Regression is selected for the integrated system because:
1. Its coefficient-based attribution is mathematically exact and deterministic.
2. It requires no post-hoc approximation method (e.g., SHAP) for explanation.
3. Its F1 and ROC-AUC are competitive with the other classifiers within their standard deviation ranges.

This selection is a deliberate interpretability trade-off, not a performance optimisation.

---

## 8. XAI Attribution Method

For each prediction, the contribution of each feature f_i is:

```
contribution_i = scaled_value_i × coefficient_i
```

Where:
- scaled_value_i = (raw_value_i - scaler_mean_i) / scaler_std_i
- coefficient_i = the learned LR coefficient for feature i

Positive contribution → feature increases predicted failure probability.
Negative contribution → feature decreases predicted failure probability.

The top 5 features by absolute contribution are reported.

This method is specific to logistic regression and does not generalise to non-linear models.

---

## 9. Likely Failure Category Inference

Evidence scores for four resource categories (CPU, Memory, Disk, Network) are computed by summing absolute XAI contributions of features belonging to each resource. The category with the highest summed evidence is reported as the "likely failure category." This is a heuristic mapping from model evidence to resource domain. It does not establish mechanical causality.

---

## 10. Autonomous Decision Logic

A lookup table maps likely-failure-category to a recommended simulated recovery action:

| Category | Recovery Action |
|---|---|
| CPU Spike | Terminate / throttle high-CPU processes |
| Memory Leak | Restart affected service / reclaim memory |
| Disk Exhaustion | Clear logs / archive data / expand storage |
| Network Degradation | Check/restart network service / reroute |
| Combined Failure | Controlled recovery sequence + alert |

---

## 11. Post-Healing Verification

When risk_level is HIGH or CRITICAL:
1. Evidence_before is recorded (risk_score, risk_level, label).
2. A 10-step synthetic normal_stable sequence is generated.
3. The same trained LR model predicts risk on this sequence.
4. Evidence_after is recorded.
5. Verification verdict:
   - RECOVERED: post-healing risk_level == LOW
   - NOT_RECOVERED: post-healing risk_level == HIGH or CRITICAL
   - INCONCLUSIVE: post-healing risk_level == MEDIUM

The temporal buffer is cleared after healing so the next real polling cycle enters the WARMING_UP state.
