# Explainable AI (XAI) Autonomous Cloud Operations Platform

An end-to-end, explainable autonomous cloud reliability platform that combines temporal sliding-window telemetry, machine learning failure-risk forecasting, exact linear feature attribution (XAI), root-cause evidence diagnosis, targeted recovery decision logic, and closed-loop post-healing verification.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20scikit--learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Release-Phase%204A%20Final-brightgreen)

---

## 1. System Overview & Architecture

Modern cloud infrastructure requires proactive, transparent resilience. Traditional monitoring relies on static threshold alerts that fire only after failures manifest. This platform implements a forward-looking predictive operations loop:

```
[Synthetic Telemetry Stream]
             ↓
[10-Step Sliding-Window Buffer] (10 timesteps history)
             ↓
[45 Temporal Rolling Features] (Current, Means, Deltas, Slopes, Std Devs across 5 metrics)
             ↓
[Predictive Classifier] (StandardScaler + Logistic Regression C=1.0, balanced weights)
             ↓
[Deterministic XAI Attribution] (Exact linear feature contributions: w_i * x_tilde_i)
             ↓
[Root-Cause Evidence Aggregator] (CPU, Memory, Disk, Network attribution scores)
             ↓
[Autonomous Decision Engine] (Root-cause to targeted remediation mapping)
             ↓
[Simulated Remediation] (Simulation-mode healing execution)
             ↓
[Post-Healing Verification Loop] (Simulated recovery state, re-prediction: RECOVERED / NOT_RECOVERED)
```

---

## 2. Key Modules & Implementation

| Component | Source File | Description |
|-----------|-------------|-------------|
| **Operations Dashboard** | `dashboard.py` | Phase 4A dark-theme operations UI with real-time telemetry, 7-stage pipeline visualizer, XAI contribution waterfall, and post-healing verification log. |
| **Backend REST API** | `api.py` | REST endpoints (`/api/scan`, `/api/health`) managing scenario playback, 10-step buffer, model inference, XAI attribution, and verification loop. |
| **Temporal Dataset** | `temporal_dataset.py` | 180 controlled 60-step sequences (120 Train, 30 Validation, 30 Test) across 8 failure/normal scenarios with strict temporal split isolation. |
| **Feature Extraction** | `temporal_features.py` | Generates 45 leakage-free rolling features (current, mean, delta, linear slope, standard deviation over 5 and 10 windows). |
| **XAI & Decision Layer** | `xai_explainer.py`, `root_cause.py`, `decision_engine.py` | Exact linear coefficient attributions, metric-level evidence aggregation, risk categorization, and targeted recovery selection. |
| **Remediation & Verification** | `healer.py` | Unified execution adapter supporting automated remediation actions and post-healing state evaluation. |
| **Predictive Benchmark** | `predictive_evaluation.py`, `evaluate.py` | 5-seed comparative benchmarking (Logistic Regression vs Random Forest vs Gradient Boosting) evaluating lead times and detection metrics. |

---

## 3. Technology Stack

- **Python**: 3.10+
- **Machine Learning**: `scikit-learn` (LogisticRegression, StandardScaler, IsolationForest)
- **Scientific Computing**: `NumPy`, `SciPy`
- **System Metrics**: `psutil`
- **Web & API**: `Flask`
- **Testing**: `unittest`

---

## 4. Quick Start & Setup

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/Rahullts/xai_cloud_dashboard_updated.git
cd xai_cloud_dashboard_updated

# Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Phase 4A Operations Dashboard

```bash
python dashboard.py
```

Open `http://localhost:5000` in your web browser. You can select any scenario (`Normal Stable`, `Normal Variable`, `CPU Sudden Failure`, `CPU Gradual Failure`, `Memory Gradual Leak`, `Disk Gradual Exhaustion`, `Network Degradation`, `Combined Gradual Failure`) and observe real-time predictions, XAI feature contributions, and the autonomous healing verification loop.

### Running the CLI Pipeline

```bash
python main.py
```

---

## 5. Verification & Test Suites

The repository contains comprehensive unit, integration, and dataset validation test suites:

```bash
# 1. Run pipeline and API tests
python -m unittest discover tests -v

# 2. Run Phase 3E full-pipeline integration and XAI layer tests
python -m unittest test_phase3e_integration.py test_xai_layer.py -v

# 3. Run temporal dataset generation & split integrity validations (12 checks)
python test_temporal_dataset.py

# 4. Run temporal rolling feature validations & anti-triviality checks (12 checks)
python test_temporal_features.py

# 5. Run end-to-end dashboard server & API integration test
python test_api.py
```

All 35+ test validations pass deterministically.

---

## 6. Research Scope & Limitations

1. **Controlled Telemetry**: Telemetry is generated from parameterized operational profiles (stable, bursty, drift, and degradation models) rather than live production cloud providers.
2. **Simulation-Only Remediation**: Healing actions (service restarts, cache clears, scaling, disk compaction) are simulated and logged. No destructive actions are performed on host operating systems or cloud infrastructure.
3. **Linear Interpretability**: Logistic Regression was selected over complex ensemble models because its linear coefficients $w_i \cdot \tilde{x}_i$ yield exact, closed-form local attributions without relying on perturbation-based SHAP approximations.
4. **Non-Causal Evidence**: Root-cause categorization is based on metric-level attribution weighting. It provides transparent operational evidence of model focus, not formal counterfactual causal proof.

---

## 7. License & Authors

- **Author**: Rahul TS
- **Project**: Explainable-AI-Powered Self-Healing Cloud Applications
- **Repository**: [Rahullts/xai_cloud_dashboard_updated](https://github.com/Rahullts/xai_cloud_dashboard_updated)
