# Explainable AI (XAI) Autonomous Cloud Operations Platform

An end-to-end, explainable autonomous cloud reliability platform that combines temporal sliding-window telemetry, machine learning failure-risk forecasting, exact linear feature attribution (XAI), root-cause evidence diagnosis, targeted recovery decision logic, and closed-loop post-healing verification.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20scikit--learn%20%7C%20Gunicorn-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Deployment](https://img.shields.io/badge/Deploy-Render%20Ready-brightgreen)
![Status](https://img.shields.io/badge/Release-Production%20Cloud%20Ready-brightgreen)

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
[Post-Healing Verification Loop] (Simulated recovery state, re-prediction: RECOVERED / NOT_RECOVERED / INCONCLUSIVE)
```

---

## 2. Key Modules & Implementation

| Component | Source File | Description |
|-----------|-------------|-------------|
| **Operations Dashboard** | `dashboard.py` | Dark-theme operations UI with real-time telemetry, 7-stage pipeline visualizer, XAI contribution waterfall, and post-healing verification log. |
| **Backend REST API** | `api.py` | REST endpoints (`/api/scan`, `/healthz`) managing scenario playback, 10-step buffer, model inference, XAI attribution, and verification loop. |
| **WSGI Entrypoint** | `wsgi.py` | Production WSGI entry point for Gunicorn with model pre-warming for zero-cold-start inference. |
| **Temporal Dataset** | `temporal_dataset.py` | 180 controlled 60-step sequences (120 Train, 30 Validation, 30 Test) across 8 failure/normal scenarios with strict temporal split isolation. |
| **Feature Extraction** | `temporal_features.py` | Generates 45 leakage-free rolling features (current, mean, delta, linear slope, standard deviation over 5 and 10 windows). |
| **XAI & Decision Layer** | `xai_explainer.py`, `root_cause.py`, `decision_engine.py` | Exact linear coefficient attributions, metric-level evidence aggregation, risk categorization, and targeted recovery selection. |
| **Remediation & Verification** | `healer.py` | Unified execution adapter supporting simulated remediation actions and post-healing state evaluation. |
| **Predictive Benchmark** | `predictive_evaluation.py`, `evaluate.py` | 5-seed comparative benchmarking (Logistic Regression vs Random Forest vs Gradient Boosting) evaluating lead times and detection metrics. |

---

## 3. Cloud Deployment Guide (Public HTTPS Hosting on Render)

The application is pre-configured for instant zero-configuration deployment on [Render](https://render.com/) (or Railway, Fly.io, Heroku) via GitHub integration.

### Method A: One-Click Render Blueprint (Recommended)

1. Fork or push this repository to your GitHub account: `https://github.com/Rahullts/xai_cloud_dashboard_updated`.
2. Log in to your [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** → **Blueprint**.
4. Connect your GitHub repository: `xai_cloud_dashboard_updated`.
5. Render will automatically detect [`render.yaml`](./render.yaml) and configure the build command, start command, health check, and environment variables.
6. Click **Apply**. Render will build the environment and provide your live public HTTPS link (e.g., `https://xai-cloud-platform.onrender.com`).

---

### Method B: Manual Web Service Setup on Render

If creating the web service manually without Blueprint:

1. In Render Dashboard, click **New +** → **Web Service**.
2. Select your repository: `xai_cloud_dashboard_updated` (branch: `feature/xai-final-year-upgrade` or `master`).
3. Fill in the service configuration:
   - **Name**: `xai-cloud-platform`
   - **Region**: Any (e.g., Oregon, USA or Frankfurt, EU)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
   - **Instance Type**: `Free`
4. Expand **Advanced** and configure:
   - **Health Check Path**: `/healthz`
   - **Auto-Deploy**: `Yes`
5. Click **Create Web Service**.

> [!NOTE]
> **Single-Worker Concurrency (`--workers 1 --threads 4`)**: The simulated cloud scenario buffer maintains in-memory temporal state across dashboard poll cycles. Running a single worker with multiple threads ensures thread-safe, synchronized playback for demo reviewers while supporting high-concurrency requests.

---

## 4. Environment Variables Reference

| Variable | Default Value | Required | Purpose |
| :--- | :---: | :---: | :--- |
| `PORT` | `5000` | No (Injected by Cloud) | Listening port for web server. Render automatically sets this (e.g. 10000). |
| `HOST` | `0.0.0.0` | No | Network interface binding. `0.0.0.0` allows external cloud routing. |
| `DEBUG` | `False` | No | Enables Flask debug mode and detailed tracebacks. Keep `False` in production. |
| `PYTHON_VERSION`| `3.11.9` | No | Pinned Python runtime version for container builds. |
| `MODEL_SAMPLES` | `200` | No | Sample size for initial prototype training runs. |

---

## 5. Local Development & Testing

### Running Locally

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

# Start the dashboard locally
python dashboard.py
```

Open `http://localhost:5000` in your web browser.

---

## 6. Reviewer Verification Checklist (Public Dashboard Audit)

Once deployed, conference reviewers and project supervisors can verify all 10 platform capabilities:

- [ ] **1. Public Availability**: Navigate to the Render HTTPS URL. Confirm HTTP 200 and page render.
- [ ] **2. Health Check**: Visit `/healthz` to confirm load balancer response: `{"status": "ok", "service": "xai-cloud-platform", "mode": "simulation"}`.
- [ ] **3. Normal Operation**: Select **Normal Stable** in Simulation Lab. Confirm telemetry stays within baseline, risk remains LOW/MEDIUM, and no recovery is triggered.
- [ ] **4. Buffer Warm-Up**: Observe the 10-step temporal buffer counter (`k / 10`) until 45 rolling features activate.
- [ ] **5. CPU Failure Detection**: Select **CPU Spike** or **CPU Gradual**. Verify predicted risk shifts to HIGH/CRITICAL before threshold breaches.
- [ ] **6. XAI Linear Attribution**: Inspect the **XAI Reasoning** waterfall chart. Verify exact coefficient contributions with clear positive/negative directions.
- [ ] **7. Root-Cause Category**: Confirm inferred root-cause reflects the dominant resource driver (e.g., `CPU Saturation` or `Memory Leak`).
- [ ] **8. Simulated Remediation**: Observe the decision engine dispatching mapped action (e.g., `Scale CPU / restart affected workload`).
- [ ] **9. Closed-Loop Verification**:
  - CPU / Memory / Disk: Re-evaluates post-healing telemetry and confirms **RECOVERED**.
  - Network Degradation: Conservatively outputs **INCONCLUSIVE** (honest scientific validation).
  - Combined Failure: Correctly outputs **NOT_RECOVERED** for unresolvable concurrent multi-faults.
- [ ] **10. Incident Timeline**: Review the chronological incident log at the bottom to verify timestamped state transitions.

---

## 7. Verification & Automated Test Suites

The repository contains automated unit, integration, and scenario audit test suites:

```bash
# Run the 10-scenario platform audit test suite
python tests/test_audit_scenarios.py

# Run Phase 3E full-pipeline integration and XAI layer tests
python test_phase3e_integration.py test_xai_layer.py

# Run temporal dataset generation & split integrity validations (12 checks)
python test_temporal_dataset.py

# Run temporal rolling feature validations (12 checks)
python test_temporal_features.py

# Run end-to-end dashboard server & API integration test
python test_api.py
```

---

## 8. Research Scope & Limitations

1. **Controlled Telemetry**: Telemetry is generated from parameterized operational profiles (stable, bursty, drift, and degradation models) rather than live production cloud providers.
2. **Simulation-Only Remediation**: Healing actions (service restarts, cache clears, scaling, disk compaction) are simulated and logged. No destructive actions are performed on host operating systems or cloud infrastructure.
3. **Linear Interpretability**: Logistic Regression was selected over complex ensemble models because its linear coefficients $w_i \cdot \tilde{x}_i$ yield exact, closed-form local attributions without relying on perturbation-based SHAP approximations.
4. **Non-Causal Evidence**: Root-cause categorization is based on metric-level attribution weighting. It provides transparent operational evidence of model focus, not formal counterfactual causal proof.
5. **Operational Caution in Verification**: Partial mitigations return `INCONCLUSIVE` rather than falsely asserting recovery, preventing hazardous false confidence in autonomous operations.

---

## 9. License & Authors

- **Primary Author**: Rahul TS (`rahult23@karunya.edu.in`)
- **Project Supervisor**: Dr. S. Shirly (`shirly@karunya.edu.in`)
- **Institution**: Department of Computer Science and Engineering, School of Computer Science and Technology, Karunya Institute of Technology and Science, Coimbatore, India
- **Repository**: [Rahullts/xai_cloud_dashboard_updated](https://github.com/Rahullts/xai_cloud_dashboard_updated)
