# Explainable AI (XAI) Autonomous Cloud Operations Platform

An end-to-end, explainable autonomous cloud reliability platform that combines temporal sliding-window telemetry, machine learning failure-risk forecasting, exact linear feature attribution (XAI), root-cause evidence diagnosis, targeted recovery decision logic, and closed-loop post-healing verification.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20scikit--learn%20%7C%20Gunicorn-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Deployment Status](https://img.shields.io/badge/Render-Live%20%7C%20Online-brightgreen)
![Build](https://img.shields.io/badge/Release-Verified-brightgreen)

---

## 🌐 Live Public Demo (Conference & Reviewer Verification)

The interactive autonomous operations platform is deployed and publicly accessible via HTTPS on Render:

* **🚀 Live Dashboard:** [https://xai-cloud-platform.onrender.com](https://xai-cloud-platform.onrender.com)
* **🩺 Health-Check Endpoint:** [https://xai-cloud-platform.onrender.com/healthz](https://xai-cloud-platform.onrender.com/healthz)
* **📂 GitHub Repository:** [https://github.com/Rahullts/xai_cloud_dashboard_updated](https://github.com/Rahullts/xai_cloud_dashboard_updated)

> [!IMPORTANT]
> **Scientific & Operational Disclaimer:**  
> All telemetry is generated from controlled synthetic failure scenario benchmarks, and autonomous healing actions and post-recovery verifications are executed in simulation mode. This platform evaluates algorithmic decision-making, deterministic feature attribution, and closed-loop verification; it does not claim to execute destructive or physical remediation on production cloud infrastructure.

> [!NOTE]
> **Free Tier Cold-Start Notice:**  
> On Render's free tier, the container instance automatically spins down after 15 minutes of inactivity. If the service is idle, the initial visit may take 30–50 seconds to spin up and warm the in-memory ML model. Subsequent requests respond in ~300–500 ms.

---

## 🔍 How to Verify the Live Demo (Step-by-Step)

1. **Access the Live Platform:** Open [https://xai-cloud-platform.onrender.com](https://xai-cloud-platform.onrender.com). The UI displays a live, real-time dark-theme dashboard with the top badge indicating **"Simulation Lab · Synthetic Telemetry"**.
2. **Verify Load Balancer & Health Status:** Navigate to [https://xai-cloud-platform.onrender.com/healthz](https://xai-cloud-platform.onrender.com/healthz). You will receive an immediate HTTP 200 JSON response confirming model readiness:
   ```json
   {"mode": "simulation", "service": "xai-cloud-platform", "status": "ok", "version": "1.0.0"}
   ```
3. **Buffer Warm-Up Inspection:** Upon initial connection, observe the 10-step sliding-window buffer counter increment from `1 / 10` to `10 / 10` as baseline telemetry streams in.
4. **Interactive Simulation Scenarios (Simulation Lab):**
   - **Normal Stable:** Baseline operating metrics. Risk score remains LOW / MEDIUM; healing engine reports `Skipped`.
   - **CPU Spike:** Sudden compute surge drives predicted failure risk to `HIGH` / `CRITICAL` ($P > 0.60$). Triggers simulated CPU scaling (`RECOVERED`).
   - **Memory Leak:** Linear memory saturation triggers autonomous memory reclaim (`RECOVERED`).
   - **Disk Exhaustion:** Steady storage depletion triggers temporary data cleanup (`RECOVERED`).
   - **Network Degradation:** Injects synthetic packet jitter and latency ($>200\text{ ms}$). Closed-loop verification conservatively returns **`INCONCLUSIVE`** (honest verification of partial mitigation without false recovery claims).
   - **Combined Failure:** Multi-resource saturation returns **`NOT_RECOVERED`** (honest verification when a single action cannot resolve multi-fault anomalies).
5. **Inspect Explainable AI (XAI) Attribution:** Scroll to the **Why Did the Model Decide This?** waterfall chart to inspect deterministic linear coefficients ($w_i \cdot \tilde{x}_i$) identifying influential trend and variability features.
6. **Chronological Incident Timeline:** Review the audit log at the bottom to verify timestamped state transitions and before/after verification evidence.

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

The application is pre-configured for instant zero-configuration deployment on [Render](https://render.com/) via GitHub integration.

### Method A: One-Click Render Blueprint (Recommended)

1. Connect this repository to your Render account: `https://github.com/Rahullts/xai_cloud_dashboard_updated`.
2. In [Render Dashboard](https://dashboard.render.com/), select **New +** → **Blueprint**.
3. Render automatically parses [`render.yaml`](./render.yaml) to configure the build command, start command, health check, and environment variables.
4. Click **Apply**. Render builds and provisions the live HTTPS service at `https://xai-cloud-platform.onrender.com`.

---

### Method B: Manual Web Service Setup on Render

1. Click **New +** → **Web Service** in Render.
2. Select repository `Rahullts/xai_cloud_dashboard_updated` (branch: `master`).
3. Set the configuration:
   - **Name**: `xai-cloud-platform`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
   - **Instance Type**: `Free`
4. Expand **Advanced**:
   - **Health Check Path**: `/healthz`
   - **Auto-Deploy**: `Yes`
5. Click **Create Web Service**.

> [!NOTE]
> **Single-Worker Concurrency (`--workers 1 --threads 4`)**: The simulated cloud scenario buffer maintains in-memory temporal state across dashboard poll cycles. Running a single worker with multiple threads ensures thread-safe, synchronized playback for demo reviewers while supporting concurrent client visits.

---

## 4. Environment Variables Reference

| Variable | Default Value | Required | Purpose |
| :--- | :---: | :---: | :--- |
| `PORT` | `5000` | No (Injected by Cloud) | Listening port for web server. Render automatically injects this. |
| `HOST` | `0.0.0.0` | No | Network interface binding. `0.0.0.0` allows external cloud routing. |
| `DEBUG` | `False` | No | Controls Flask debug mode and stack-trace exposure. Kept `False` in production. |
| `PYTHON_VERSION`| `3.11.9` | No | Pinned Python runtime version for container builds. |
| `MODEL_SAMPLES` | `200` | No | Sample size parameter for prototype model fitting. |

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

## 6. Verification & Automated Test Suites

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

All 35+ test validations pass deterministically.

---

## 7. Research Scope & Limitations

1. **Controlled Telemetry**: Telemetry is generated from parameterized operational profiles (stable, bursty, drift, and degradation models) rather than live production cloud providers.
2. **Simulation-Only Remediation**: Healing actions (service restarts, cache clears, scaling, disk compaction) are simulated and logged. No destructive actions are performed on host operating systems or cloud infrastructure.
3. **Linear Interpretability**: Logistic Regression was selected over complex ensemble models because its linear coefficients $w_i \cdot \tilde{x}_i$ yield exact, closed-form local attributions without relying on perturbation-based SHAP approximations.
4. **Non-Causal Evidence**: Root-cause categorization is based on metric-level attribution weighting. It provides transparent operational evidence of model focus, not formal counterfactual causal proof.
5. **Operational Caution in Verification**: Partial mitigations return `INCONCLUSIVE` rather than falsely asserting recovery, preventing hazardous false confidence in autonomous operations.

---

## 8. License & Authors

- **Primary Author**: Rahul TS (`rahult23@karunya.edu.in`)
- **Project Supervisor**: Dr. S. Shirly (`shirly@karunya.edu.in`)
- **Institution**: Department of Computer Science and Engineering, School of Computer Science and Technology, Karunya Institute of Technology and Science, Coimbatore, India
- **Repository**: [Rahullts/xai_cloud_dashboard_updated](https://github.com/Rahullts/xai_cloud_dashboard_updated)
- **Live Deployment**: [https://xai-cloud-platform.onrender.com](https://xai-cloud-platform.onrender.com)
