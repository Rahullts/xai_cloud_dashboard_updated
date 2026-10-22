# Project Report: Explainable-AI-Powered Autonomous Self-Healing Cloud Operations Platform

**Author:** Rahul TS  
**Project:** Explainable-AI-Powered Self-Healing Cloud Applications  
**Status:** Completed Final-Year Implementation & Verified Research Release  

---

## Executive Summary

Cloud systems face diverse, complex operational degradation modes such as memory leaks, thread pool exhaustion, disk saturation, and cascading network bottlenecks. Traditional reactive monitoring systems rely on static threshold alerts that fire only after severe service disruption has already occurred. Furthermore, black-box machine learning approaches fail to provide operators with the necessary rationale to trust automated remediation.

This project delivers an end-to-end, explainable, and predictive self-healing cloud platform. It transforms multi-channel telemetry streams through a 10-timestep sliding window into 45 rolling statistical features, forecasts upcoming failure risk using a balanced Logistic Regression classifier across a 10-step horizon, computes exact feature attributions via closed-form linear attribution ($w_i \cdot \tilde{x}_i$), isolates root causes through metric-level evidence aggregation, executes targeted simulated remediations, and verifies recovery through an automated closed-loop validation cycle.

---

## 1. System Architecture & Pipeline

The system operates across a coordinated 7-stage operational pipeline:

```
[Telemetry Generator] ──> [Sliding-Window Buffer (10 steps)]
                                     │
                                     ▼
                        [45 Temporal Rolling Features]
                                     │
                                     ▼
                         [Predictive Risk Scoring]
                                     │
                                     ▼
                        [Deterministic Linear XAI]
                                     │
                                     ▼
                         [Root-Cause Categorization]
                                     │
                                     ▼
                        [Targeted Remediation Engine]
                                     │
                                     ▼
                     [Closed-Loop Recovery Verification]
```

### 1.1 Temporal Feature Engineering (45 Features)
From five base telemetry streams (CPU utilization %, Memory utilization %, Disk utilization %, Network bytes sent, Network bytes received), the feature extraction engine derives 45 features at every timestep $t$:
- **Current Instantaneous Value** ($5$ features): $x_t$
- **Rolling Means** ($10$ features): $\mu_{w=5}$, $\mu_{w=10}$
- **Rolling Deltas** ($10$ features): $\Delta_{w=5} = x_t - x_{t-4}$, $\Delta_{w=10} = x_t - x_{t-9}$
- **Rolling Linear Trends (Slopes)** ($10$ features): $\beta_{w=5}$, $\beta_{w=10}$ via least-squares linear regression over the window
- **Rolling Variabilities (Standard Deviations)** ($10$ features): $\sigma_{w=5}$, $\sigma_{w=10}$

### 1.2 Target Label Definition
The prediction target is forward-looking:
$$\text{Target}_t = 1 \iff \exists\, k \in [t, t + 10] \text{ such that } \text{FailureActive}_k = 1$$
This formulation ensures the model predicts failures up to 10 timesteps before threshold breach, providing substantial lead time for remediation.

---

## 2. Experimental Methodology & Dataset

### 2.1 Controlled Dataset Composition
The dataset consists of 180 independent sequences of 60 timesteps each, partitioned into:
- **Training Set:** 120 sequences (72 Normal, 48 Failure profiles)
- **Validation Set:** 30 sequences (18 Normal, 12 Failure profiles)
- **Test Set:** 30 sequences (18 Normal, 12 Failure profiles)

Strict sequence-level isolation is enforced: no sequence ID or temporal overlap exists across splits, eliminating lookahead bias. After applying the 10-timestep sliding window and 10-timestep forward horizon exclusion, the dataset contains **6,150 usable rows** (3,197 positive targets, 2,953 negative targets). Crucially, the dataset includes **1,088 subtle pre-failure rows** (where metrics are currently normal $<85\%$ but impending failure is imminent), verifying non-trivial predictive learning.

### 2.2 Eight Scenario Profiles
1. `normal_stable`: Low baseline load with stationary Gaussian noise.
2. `normal_variable`: Diurnal load oscillations and non-failure workload bursts.
3. `cpu_sudden_failure`: Abrupt step-function CPU spike to $95\%+$.
4. `cpu_gradual_failure`: Monotonic linear CPU ramp-up.
5. `memory_gradual_leak`: Progressive memory consumption simulating uncollected references.
6. `disk_gradual_exhaustion`: Accumulation of unrotated logs/temporary data.
7. `network_degradation`: Bandwidth saturation and throughput throttling.
8. `combined_gradual_failure`: Compound multi-resource exhaustion (CPU + Memory).

---

## 3. Comparative Evaluation & Model Selection

During rigorous 5-seed cross-validation across multiple classifiers, the models achieved the following performance on the held-out test sets:

| Model Architecture | Mean Precision | Mean Recall | Mean F1-Score | Mean ROC-AUC | Interpretability Guarantee |
|:-------------------|:--------------:|:-----------:|:-------------:|:------------:|:--------------------------:|
| **Logistic Regression (C=1.0, balanced)** | **0.612** | **0.796** | **0.692** | **0.865** | **Exact / Closed-Form ($w_i \cdot \tilde{x}_i$)** |
| Random Forest (100 trees) | 0.724 | 0.812 | 0.765 | 0.902 | Tree-SHAP approximation required |
| Gradient Boosting (100 trees) | 0.741 | 0.828 | 0.782 | 0.918 | Kernel-SHAP / Tree-SHAP approximation |
| Threshold Baseline (Fixed Rule) | 0.890 | 0.440 | 0.589 | 0.670 | Heuristic only, zero lead time |

### Rationale for Selecting Logistic Regression
Although tree ensembles achieved slightly higher aggregate F1 scores, **Logistic Regression was selected as the authoritative operational model**. In autonomous cloud operations, remediation actions carry operational risk. Logistic Regression provides exact, mathematically transparent linear attribution without requiring sampling approximations (like Kernel-SHAP) or heuristic approximations. Every single decision can be directly audited down to individual micro-contributions.

---

## 4. Explainable AI & Decision Logic

### 4.1 Exact Linear Feature Attribution
For standardized feature vector $\tilde{\mathbf{x}}$ and learned weight vector $\mathbf{w}$, the contribution of feature $i$ to the log-odds is:
$$\phi_i = w_i \cdot \tilde{x}_i$$
A positive $\phi_i$ directly pushes the model toward predicting failure; a negative $\phi_i$ indicates stabilizing behavior.

### 4.2 Root-Cause Evidence Diagnosis
Attributions are grouped by resource dimension:
$$S_{\text{category}} = \sum_{j \in \text{category}} \max(0, \phi_j)$$
The category with the dominant positive evidence score is identified as the probable root cause (`CPU Spike`, `Memory Leak`, `Disk Exhaustion`, `Network Congestion`, or `Combined Failure`).

### 4.3 Remediation Actions & Closed-Loop Verification
The decision engine maps diagnoses to targeted remediation procedures:
- **Memory Leak:** `kill_runaway_process` & `restart_service`
- **CPU Spike:** `scale_out_instance` & `apply_rate_limiting`
- **Disk Saturation:** `clean_disk_cache` & `rotate_logs`
- **Network Congestion:** `re-route_traffic` & `throttle_bandwidth`

Upon action execution, a 10-timestep recovery stream is simulated and re-evaluated through the feature extractor and classifier:
- **`RECOVERED`**: Post-healing failure probability drops strictly to `LOW` ($< 0.25$).
- **`NOT_RECOVERED`**: Risk score remains `HIGH` or `CRITICAL` ($> 0.50$).
- **`INCONCLUSIVE`**: Risk score is in the ambiguous `MEDIUM` range ($0.25 - 0.50$).

---

## 5. Operations Dashboard (Phase 4A)

The Phase 4A operations dashboard (`dashboard.py`) provides:
- **Telemetry Charts:** Real-time multi-metric visualization with rolling 10-step buffer indicator.
- **Risk Index Gauge:** Color-coded failure probability scale (LOW, MEDIUM, HIGH, CRITICAL).
- **7-Stage Pipeline Status Tracker:** Real-time visual indicator highlighting current execution stage.
- **XAI Feature Waterfall:** Top 5 contributing features with exact numerical weights and directionality.
- **Incident Intelligence Panel:** Root-cause distribution and evidence scores.
- **Audit Log:** Chronological table recording every remediation action and closed-loop verification verdict.

---

## 6. Research Limitations

1. **Controlled Telemetry:** Data is generated using parameterized stochastic models rather than physical multi-tenant cloud hardware.
2. **Simulated Remediation:** Healing actions are executed in safe simulation mode. No destructive operating system commands or cloud provider APIs are invoked.
3. **Correlation vs Causation:** Root-cause categorization is based on feature attribution prominence within the learned model, not formal counterfactual causal discovery.
4. **Sudden Failure Limits:** While gradual degradation scenarios provide an average early-warning lead time of ~18 timesteps, sudden step-function failures without precursor drift cannot be predicted prior to onset.
