# Paper-Ready Tables

### Table 1: Dataset Configuration

| Parameter | Value |
|---|---|
| Base Telemetry Metrics | CPU, Memory, Disk, Network Sent, Network Receive |
| Temporal Representations | Current, Mean (5/10), Delta (5/10), Slope (5/10), Std (5/10) |
| Total Features | 45 |
| Prediction Horizon | 10 timesteps (simulated minutes) |
| Target Definition | Failure active now OR within the next 10 timesteps |
| Train/Validation/Test Split | 120 / 30 / 30 Sequences |
| Sequence Length | 60 timesteps |

### Table 2: Predictive Model Comparison

Mean ± standard deviation across 5 random seeds on the strictly isolated test sets.

| Model | Accuracy | Precision | Recall | F1 Score | FPR | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|---|
| majority_baseline | 0.4703 ± 0.0335 | 0.3795 ± 0.1925 | 0.8000 ± 0.4000 | 0.5141 ± 0.2589 | 0.8000 ± 0.4000 | N/A | N/A |
| threshold_baseline | 0.5524 ± 0.0470 | 0.9973 ± 0.0055 | 0.0856 ± 0.0311 | 0.1560 ± 0.0538 | 0.0003 ± 0.0006 | N/A | N/A |
| logistic_regression | 0.7156 ± 0.0127 | 0.7304 ± 0.0493 | 0.6605 ± 0.0499 | 0.6917 ± 0.0362 | 0.2317 ± 0.0328 | 0.8133 ± 0.0208 | 0.8397 ± 0.0274 |
| random_forest | 0.7376 ± 0.0237 | 0.8049 ± 0.0469 | 0.6195 ± 0.0571 | 0.6964 ± 0.0209 | 0.1548 ± 0.0698 | 0.8185 ± 0.0052 | 0.8467 ± 0.0166 |
| gradient_boosting | 0.7044 ± 0.0709 | 0.7471 ± 0.1373 | 0.7007 ± 0.1267 | 0.6989 ± 0.0303 | 0.2678 ± 0.2238 | 0.8257 ± 0.0133 | 0.8518 ± 0.0252 |

### Table 3: Per-Scenario Performance (Logistic Regression)

| Scenario | True Negatives | False Positives | False Negatives | True Positives | Total |
|---|---|---|---|---|---|
| disk_gradual_exhaustion | 12 | 9 | 47 | 178 | 246 |
| normal_stable | 132 | 73 | 0 | 0 | 205 |
| combined_gradual_failure | 56 | 27 | 40 | 123 | 246 |
| normal_variable | 164 | 0 | 0 | 0 | 164 |
| network_degradation | 36 | 27 | 13 | 47 | 123 |
| memory_gradual_leak | 4 | 0 | 13 | 24 | 41 |
| cpu_sudden_failure | 16 | 8 | 8 | 9 | 41 |
| cpu_gradual_failure | 41 | 13 | 52 | 58 | 164 |

### Table 4: Contamination Parameter Experiment (Phase 2B Isolation Forest)

*(Note: Values derived from Phase 2B validation. The selected parameter is not universally optimal, but calibrated for this specific synthetic distribution.)*

| Contamination | Recall | F1 Score | FPR |
|---|---|---|---|
| 0.05 | 0.1424 | 0.2493 | 0.0 |
| 0.10 | 0.2848 | 0.4433 | 0.0 |
| 0.15 | 0.4272 | 0.5986 | 0.0 |
| 0.20 | 0.5696 | 0.7258 | 0.0 |

### Table 5: Early-Warning Analysis (Logistic Regression)

An early warning is strictly defined as a prediction made *before* the `failure_start_index`.

| Metric | Value |
|---|---|
| Sequences with Valid Early Warning | 18 |
| Mean Warning Time | 18.06 timesteps |
| Median Warning Time | 16.0 timesteps |
| Warning Time Range | 4 - 33 timesteps |

### Table 6: Representative XAI Cases

| Scenario | Model Score | Likely Root Cause | Top 2 Contributing Features |
|---|---|---|---|
| disk_gradual_exhaustion | 0.5905 | Combined Failure | Memory 10-step average (-1.00), Memory 10-step variability (0.59) |
| combined_gradual_failure | 0.5372 | Combined Failure | Cpu 10-step variability (-0.42), Memory 10-step average (-0.37) |
| network_degradation | 0.5341 | Combined Failure | Memory 10-step variability (0.42), Cpu 10-step average (-0.25) |
| cpu_sudden_failure | 0.6855 | Memory Leak | Memory 10-step average (0.92), Network Recv 10-step average (-0.29) |

### Table 7: System Recovery Verification Examples (Phase 3E Integration)

Examples of simulated before/after verification states captured from the integrated API.

| Scenario | Pre-Healing Risk | Simulated Action | Post-Healing Risk | Verification Result |
|---|---|---|---|---|
| CPU Sudden Failure | HIGH (Score: 0.812) | Scale CPU / Restart | LOW (Score: 0.124) | RECOVERED |
| Memory Leak | CRITICAL (Score: 0.945) | Restart Service | LOW (Score: 0.089) | RECOVERED |
| Network Degradation | HIGH (Score: 0.760) | Alert Operator | MEDIUM (Score: 0.358) | INCONCLUSIVE |

