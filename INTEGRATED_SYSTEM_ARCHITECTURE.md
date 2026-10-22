# Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform (Phase 3E: Architecture)

## 1. Full Architecture
The system is built on a Flask backend providing a unified REST API (`/api/scan`), which is polled by a standalone HTML/JS frontend dashboard. 

## 2. Data Flow
`Live Simulated Telemetry (temporal_dataset)` → `Temporal Sliding Window Buffer` → `Feature Engineering (temporal_features)` → `Predictive Model (Logistic Regression)` → `XAI Attribution (xai_explainer)` → `Root-Cause Analysis (root_cause)` → `Decision Engine (decision_engine)` → `Simulated Healer (healer)` → `Dashboard Rendering`.

## 3. Temporal Feature Generation
The backend maintains a sliding window of exactly 10 telemetry states (the maximum window required). Once 10 states are buffered (warm-up phase), the system generates exact rolling averages, slopes, and standard deviations for the trailing edge of the window.

## 4. Predictive Model Selection
Logistic Regression was selected as the primary integrated model because it provides competitive predictive performance together with transparent feature-level coefficient attribution. 
While aggregate Phase 3C results showed Gradient Boosting had slightly higher F1/ROC-AUC, Logistic Regression guarantees completely deterministic, mathematically verifiable explanations locally via `scaled_value * coefficient`.
The model is strictly configured with `C=1.0`, `class_weight='balanced'`, `StandardScaler()`, and deterministic seed `42`.

## 4b. API Model Training
The prototype trains the deterministic model at startup using the same controlled training configuration (Train subset only: 120 sequences). A production implementation would persist a versioned trained model artifact and load it at runtime. It explicitly isolates and excludes Validation and Test data from this process.

## 5. XAI
Extracts mathematical feature attributions natively (`scaled feature value × model coefficient`) mapping precisely to the Logistic Regression model, preventing any disagreement between prediction and explanation.

## 6. Root-Cause Interpretation
Aggregates the positive XAI attributions by component groups (CPU, Memory, Disk, Network) to diagnose the most likely failure pattern causing the elevated model score.

## 7. Decision Engine
Maps the diagnosed likely failure to a precise recovery recommendation (e.g. `Memory Leak` → `Restart affected service / reclaim memory`), only enacting it when the predicted Risk Level reaches `HIGH` or `CRITICAL`.

## 8. Simulated Healing
Safely accepts the recommended action and simulates its execution by writing to the `recovery_log.txt` without destroying host resources or executing destructive shell commands.

## 9. Verification
Immediately following a simulated healing action, the temporal buffer is flushed. This organically simulates a post-recovery system state where metrics drop back down to safe baseline initialization values.

## 10. Dashboard/API Integration
The dashboard contains zero random number generators. It is fully stateless, merely rendering the highly structured JSON payloads provided by the `/api/scan` endpoint.

## 11. Safety Boundaries
The application is entirely sandboxed in simulation. Shell subprocesses are not used for scaling, restarts, or node deletion. 

## 12. Limitations
- **Controlled synthetic telemetry:** The dataset is artificially generated, limiting generalization to wild clouds.
- **Root-cause inference is not causal proof:** XAI points to correlated features, not mathematically proven mechanisms of action.
- **Sudden failures:** By design, un-signaled sudden CPU failures are extremely difficult to catch prior to the anomaly.
- **Simulated healing:** Simulating recovery does not prove that a production cluster would survive the same operation unharmed.
- **No production cloud deployment.** 

---
### Definitional Distinctions
- **Prediction:** "What is the model predicting?"
- **XAI:** "Which model inputs influenced the prediction?"
- **Root Cause:** "What failure category is most consistent with the evidence?"
- **Decision:** "What recovery action is recommended?"
- **Healing:** "What simulated recovery action was executed?"
- **Verification:** "Did the system observe evidence of recovery?"
