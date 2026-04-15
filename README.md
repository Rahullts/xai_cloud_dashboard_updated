# ⚡ Explainable AI-Based Self-Healing Cloud Application

> Autonomous cloud health monitoring with AI anomaly detection and human-readable explanations.

---

## 🔍 What This Project Does

This system monitors cloud application health metrics, detects failures using machine learning, **explains WHY a failure was detected**, and automatically triggers recovery actions — all without human intervention.

```
Monitor Metrics → AI Detection → XAI Explanation → Self-Healing Actions
     CPU/RAM          Isolation          Z-score +           Restart /
     Disk/Net         Forest             Rule Engine         Scale / Alert
```

---

## 🧠 Key Concepts

| Concept | What it means here |
|---|---|
| **Self-Healing** | System detects its own failures and recovers automatically |
| **Explainable AI** | Every AI decision comes with a human-readable reason |
| **Isolation Forest** | Unsupervised ML algorithm to detect metric outliers |
| **Feature Importance** | Ranks which metric caused the anomaly |

---

## 📁 Project Structure

```
xai_self_healing/
├── monitor.py        # Collect CPU, memory, disk, network metrics
├── detector.py       # Isolation Forest anomaly detection
├── explainer.py      # XAI: z-scores + rule-based explanations
├── healer.py         # Decision engine + self-healing actions
├── main.py           # Run all 5 demo scenarios
├── dashboard.py      # Optional Flask web dashboard
├── requirements.txt  # Python dependencies
└── recovery_log.txt  # Auto-generated action log
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/xai-self-healing-cloud.git
cd xai-self-healing-cloud

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the demo
python main.py

# 4. (Optional) Run the web dashboard
python dashboard.py
# Open http://localhost:5000
```

---

## 📊 Sample Output

```
SCENARIO 2: CPU Spike
──────────────────────────────────────
AI Decision: ANOMALY  (score=-0.1243)

XAI EXPLANATION REPORT
  CPU Usage (%)        93.7   (z=+6.9)  <<<
  Memory Usage (%)     44.2   (z=+0.2)
  Disk Usage (%)       33.1   (z=-0.2)

Feature Importance:
  #1 CPU Usage (%)     z=+6.9  ████████████████

Rule-Based Reasoning:
  ⚠ CPU at 93.7% — well above safe limit of 85%.
    Likely cause: runaway process or traffic surge.

DECISION ENGINE:
  🔄 Restarting service 'web-app-server'... ✅
  📈 Scaling out — adding 1 instance...    ✅
  📋 LOG: RESTART + SCALE_OUT recorded.
```

---

## 🛠 Tech Stack

- **Python 3.9+**
- **psutil** — system metrics collection
- **scikit-learn** — Isolation Forest ML model
- **numpy** — numerical computations
- **Flask** — optional web dashboard

---

## 🔮 Future Improvements

- [ ] SHAP values for rigorous feature attribution
- [ ] Real AWS CloudWatch / GCP Stackdriver integration
- [ ] LSTM-based predictive anomaly detection
- [ ] Reinforcement learning for adaptive healing
- [ ] Kubernetes operator for production deployment

---

## 📖 Related Concepts

- [Isolation Forest Paper (Liu et al., 2008)](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)
- [SHAP Explainability](https://github.com/slundberg/shap)
- [psutil Documentation](https://psutil.readthedocs.io)
- [Scikit-learn Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

## 👨‍💻 Author

**[Your Name]** — [Your College], [Department], [Year]

---

*Built as an academic mini-project demonstrating Explainable AI in cloud systems.*
