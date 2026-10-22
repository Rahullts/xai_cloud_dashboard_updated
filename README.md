# Explainable-AI-Powered Self-Healing Cloud Applications

A research and demonstration project that combines synthetic cloud/system metrics, Isolation Forest problem detection, heuristic explanations, and simulated recovery recommendations.

> **Important scope note:** The current version is a local academic prototype. It does not connect to AWS/Azure/GCP, restart real services, kill processes, scale infrastructure, or clean real disks. Recovery actions are recommendations logged as simulation-only.

## Pipeline

```text
Metrics / synthetic scenarios
          ↓
Input validation and feature vector
          ↓
Isolation Forest (five metrics)
          ↓
Heuristic explanation + threshold rules
          ↓
Simulated recovery recommendations
```

## Current capabilities

- Collect CPU, memory, disk, and cumulative network-counter metrics with `psutil`.
- Generate reproducible synthetic normal, CPU-spike, memory-leak, disk-full, network-issue, and combined scenarios.
- Detect outliers using scikit-learn Isolation Forest.
- Show fixed-baseline deviation rankings and human-readable threshold rules.
- Serve a Flask dashboard whose selected scenario is passed to the server-side model endpoint.
- Return recovery recommendations explicitly marked as simulation-only.
- Test input validation, repeatability, explanation labeling, recovery planning, and Flask API behavior.

## Technology

- Python
- NumPy
- scikit-learn (Isolation Forest)
- psutil
- Flask
- unittest (standard library)

## Setup

Use Python 3.10+ where possible.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

Run the command-line demonstration:

```bash
python main.py
```

Run the dashboard:

```bash
python dashboard.py
```

Open http://127.0.0.1:5000. The dashboard calls `/api/scan?scenario=normal` and supports `normal`, `cpu`, `memory`, `disk`, `network`, and `combined`.

## Tests

Run from the repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite includes synthetic data reproducibility, scenario validation, feature ordering, invalid model inputs, seeded model reproducibility, heuristic explanation labeling, recovery recommendations, and Flask endpoint validation.

## Interpretation and research limitations

- The Isolation Forest is trained on generated synthetic samples. This is not evidence of real-world cloud reliability or generalization.
- Its `decision_function` score is higher for more normal observations and lower for more anomalous observations.
- Explanation rankings are based on fixed baseline deviations and hand-written thresholds. They are **not** SHAP/LIME values, causal explanations, or true Isolation Forest feature attributions.
- Network fields are cumulative MB counters since the host network counters were reset, not network throughput rates.
- Dashboard latency is a separate synthetic display field and is not included in the model's five input features.
- Do not report accuracy, precision, recall, F1, ROC-AUC, or PR-AUC without a separately generated held-out evaluation set and reproducible calculation code.

## Suggested next research milestones

1. Add a labeled, seeded train/validation/test generator and evaluate the model against a threshold baseline.
2. Report confusion matrix, precision, recall, F1, ROC-AUC, and PR-AUC where statistically appropriate.
3. Add temporal traces and evaluate early-warning lead time only when labels and event times are defined.
4. Add before/after recovery verification in simulation.
5. Consider provider integrations only after safe, permissioned action execution and rollback behavior are designed.

## References

- Liu, F. T., Ting, K. M., and Zhou, Z.-H. “Isolation Forest.” IEEE International Conference on Data Mining, 2008.
- [scikit-learn IsolationForest documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [psutil documentation](https://psutil.readthedocs.io/)
