# Results and Discussion

## 1. Detection Results — Phase 2

Isolation Forest (IF) anomaly detection was evaluated against snapshot telemetry across all scenario types. A current-value threshold classifier (alarm if any metric exceeds 80%) served as the baseline.

### Key Findings

| Method | Precision | Recall | F1 | FPR |
|---|---|---|---|---|
| Threshold Baseline | 1.000 | 0.435 | 0.606 | 0.000 |
| Isolation Forest | 0.704 | 0.826 | 0.760 | 0.073 |

The threshold baseline achieves perfect precision but poor recall (0.435) because gradual failure scenarios accumulate resource usage slowly — no individual metric exceeds the 80% threshold until late in the failure sequence. The Isolation Forest achieves recall of 0.826 at the cost of a 7.3% false positive rate on normal telemetry. This trade-off is appropriate for a monitoring system where missing a real failure (false negative) is costlier than an occasional false alarm.

Per-scenario analysis shows network degradation and combined failures are detected with F1 of 0.823–1.00. Disk gradual exhaustion achieves only F1 0.700 at the snapshot level, reflecting that disk fill progresses slowly through value ranges where IF has not yet learned a clear anomaly boundary.

**Finding:** Snapshot-level anomaly detection alone cannot address gradual failures effectively. This motivates the temporal prediction layer.

---

## 2. Temporal Predictive Results — Phase 3

### 2.1 Model Comparison (5-Seed Evaluation)

Five models were evaluated across seeds {42, 123, 456, 789, 2026}. Results are mean ± standard deviation.

| Model | F1 | ROC-AUC | PR-AUC | Recall | Precision |
|---|---|---|---|---|---|
| Majority Baseline | 0.514 ± 0.259 | — | — | 0.800 ± 0.400 | 0.380 ± 0.193 |
| Threshold Baseline | 0.156 ± 0.054 | — | — | 0.086 ± 0.031 | 0.997 ± 0.006 |
| Logistic Regression | 0.692 ± 0.036 | 0.813 ± 0.021 | 0.840 ± 0.027 | 0.661 ± 0.050 | 0.730 ± 0.049 |
| Random Forest | 0.696 ± 0.021 | 0.819 ± 0.005 | 0.847 ± 0.017 | 0.620 ± 0.057 | 0.805 ± 0.047 |
| Gradient Boosting | 0.699 ± 0.030 | 0.826 ± 0.013 | 0.852 ± 0.025 | 0.701 ± 0.127 | 0.747 ± 0.137 |

All three ML classifiers substantially outperform both baselines. The threshold baseline — operating on current snapshot values — achieves recall of only 8.6% because gradual failure patterns do not trigger fixed thresholds early. This confirms the central hypothesis of RQ2: temporal features substantially improve early-warning capability.

The differences among LR, RF, and GB are small relative to within-seed variance. Gradient Boosting achieves the highest mean AUC (0.826) and F1 (0.699) but also the highest variance in recall (±0.127), suggesting sensitivity to the specific random seed used in tree construction. Logistic Regression shows the most consistent performance (F1 std ±0.036). At seed 42 specifically, LR achieves F1 0.727 and AUC 0.830 — marginally higher than RF (F1 0.718) and GB (F1 0.725) at that specific seed.

### 2.2 Model Selection Rationale

Logistic Regression is selected for integration not on performance grounds but on interpretability grounds: its coefficient-based attribution is mathematically exact and computationally inexpensive. Random Forest and Gradient Boosting would require SHAP or similar post-hoc approximation methods to produce feature attributions. This trade-off is documented as a design decision.

### 2.3 Per-Scenario Analysis

Gradual failure scenarios (memory leak F1 0.787, disk exhaustion F1 0.864, combined F1 0.786) achieve substantially higher F1 than abrupt scenarios (CPU sudden failure F1 0.529). This is expected: temporal rolling features — mean, slope, standard deviation — accumulate information over time and are most informative when the failure pattern evolves gradually. A sudden step-change failure produces limited temporal signal before onset.

The normal_stable scenario produces 73 false positives out of 205 rows (35.6% FPR at the row level), reflecting the model's sensitivity setting (class_weight='balanced'). This is consistent with the model's high recall on failure scenarios but implies that a deployed system would generate false alarms at this sensitivity level on stable infrastructure.

---

## 3. Early-Warning Analysis

The model issued at least one HIGH or CRITICAL prediction before the labelled failure onset in all 18 evaluated failure sequences (out of 30 test sequences; 12 were normal sequences with no failure region).

| Statistic | Value |
|---|---|
| Sequences with early warning | 18 / 18 (100%) |
| Mean lead time | 18.06 timesteps |
| Median lead time | 16.0 timesteps |
| Min lead time | 4 timesteps |
| Max lead time | 33 timesteps |

The minimum of 4 timesteps occurred on sudden-failure scenarios; the maximum of 33 timesteps on gradual disk exhaustion scenarios where the temporal trajectory began diverging from normal patterns well before any individual metric reached critical values. This demonstrates the practical value of temporal prediction over threshold monitoring for gradual failure scenarios.

---

## 4. XAI Attribution Analysis

The XAI case studies show that variability features (10-step standard deviation) and slope features (5-step and 10-step linear regression slope) dominate the top-5 contributions in most failure scenarios. This is interpretable: gradual failures increase both the variability and the slope of affected metrics' temporal trajectories before absolute values reach alarm levels.

Memory mean features show negative contributions in some cases (e.g., case test_1: Memory 10-step average contribution −0.999). This reflects a model behaviour that is operationally interpretable: the model has learned that high sustained memory utilisation alone, in the context of combined multi-resource patterns, reduces the probability of a specific failure label. The XAI attribution makes this visible and allows an operator to understand the prediction.

The evidence-score mapping to likely failure categories correctly identifies the dominant resource for gradual single-resource failures (memory leak → Memory; disk exhaustion → Disk) but produces "Combined Failure" for cases where attributions are distributed across multiple resource domains. This is honest behaviour: the model reports uncertainty across resources when evidence is evenly spread.

---

## 5. Post-Recovery Verification

For the network degradation scenario (most reliably reaching CRITICAL risk in repeated API calls):

- Pre-healing: CRITICAL (0.884)
- Simulated recovery action: "Controlled recovery sequence + alert"
- Post-healing (simulated normal telemetry): MEDIUM (0.447)
- Verdict: **INCONCLUSIVE**

The INCONCLUSIVE result is the correct and expected output. The post-healing synthetic telemetry produces a risk score of 0.447 — reduced from 0.884 but above the LOW threshold (≤0.25). The system correctly declines to claim RECOVERED when meaningful risk remains. This demonstrates that the three-class verification scheme adds genuine information over a binary RECOVERED/FAILED classification.

---

## 6. Summary of Findings by Research Question

| RQ | Answer |
|---|---|
| RQ1 | Isolation Forest achieves F1 0.76 on snapshot anomaly detection, with recall 0.826. Threshold monitoring achieves recall 0.435. |
| RQ2 | Temporal LR achieves recall 0.661 vs threshold recall 0.086, with mean early-warning lead time of 18 timesteps. Temporal features substantially improve early warning. |
| RQ3 | Coefficient attribution identifies variability and slope features as strongest predictors in gradual failure scenarios. Attributions are directional, exact, and interpretable. |
| RQ4 | Evidence scoring maps XAI attributions to likely failure categories with correct identification for single-resource gradual failures. Rule-based decision logic selects appropriate recovery actions. |
| RQ5 | Post-recovery verification using the same LR model provides a meaningful 3-class verdict (RECOVERED/NOT_RECOVERED/INCONCLUSIVE) that correctly conserves against premature success claims. |
