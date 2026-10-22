# Viva Defense Q&A

**1. Why this problem?**
Modern cloud environments are complex and dynamic; reactive threshold-based monitoring causes downtime. Predicting failures before they happen and understanding *why* the model predicted them enables autonomous proactive recovery.

**2. Why cloud self-healing?**
Manual intervention in cloud operations is slow and expensive. Autonomous self-healing minimizes service disruption and improves system reliability by responding to identified risks immediately.

**3. Why machine learning?**
Static thresholds cannot capture complex temporal degradation (like a slow memory leak combined with increasing network traffic). Machine learning learns these temporal relationships from historical data.

**4. Why Isolation Forest initially?**
In Phase 2, Isolation Forest was used as an unsupervised baseline to detect anomalies without requiring labeled failure data. It proved capable but lacked predictive look-ahead and explicit root-cause mapping.

**5. Why temporal modeling?**
Point-in-time metrics miss trends. Temporal modeling captures slopes, variances, and rolling averages, allowing the model to see a system gradually degrading over time rather than just reacting to the absolute current value.

**6. Why Logistic Regression for integration?**
While tree-based models like Gradient Boosting scored slightly higher, Logistic Regression offers exact, verifiable coefficient attribution. This guarantees the XAI explanation perfectly matches the model's internal mathematics.

**7. Why StandardScaler?**
Metrics operate on vastly different scales (e.g., percentages vs. MB/s). StandardScaler normalizes these to a mean of 0 and variance of 1, allowing the Logistic Regression coefficients to directly reflect coefficient contribution without being skewed by raw magnitude.

**8. Why 45 features?**
5 base metrics multiplied by 9 representations (current, rolling means, deltas, slopes, and standard deviations at 5 and 10 step windows) capture short-term and long-term behavioral trends efficiently.

**9. Why a 10-step horizon?**
10 timesteps (simulated minutes) provides a practical balance between giving the system enough time to enact a recovery action and remaining close enough to current telemetry to predict accurately.

**10. What is XAI?**
Explainable AI is the process of making the decision-making of a complex ML model transparent. In our system, it highlights exactly which temporal features contributed to the failure risk score.

**11. Why coefficient attribution?**
It is mathematically exact for linear models: `scaled_value * coefficient`. It avoids approximations, ensures deterministic output, and runs in micro-seconds, which is ideal for real-time dashboards.

**12. Why not SHAP?**
SHAP is computationally expensive, especially for live continuous telemetry streams, and relies on approximations for complex models. Coefficient attribution is native, exact, and extremely fast for Logistic Regression.

**13. What is root-cause inference?**
It groups the positive XAI attributions (e.g., `cpu_slope_5`, `cpu_mean_10`) into logical hardware categories to infer which subsystem (CPU, Memory, Disk, Network) is most likely driving the predicted failure.

**14. Is it causal?**
No. It is an evidence-based interpretation of model behavior. The model relies on correlations; the XAI highlights those correlated features. It does not prove mechanical causality in the underlying host.

**15. What is early warning?**
An early warning is a high-risk prediction made strictly before the `failure_start_index`meaning the model identified the risk before the failure actually occurred.

**16. How was leakage prevented?**
The dataset was split at the *sequence* level. An entire 60-timestep scenario sequence went into either Train, Val, or Test, ensuring no future information or overlapping behavior leaked into the training set.

**17. Why synthetic data?**
Public datasets with high-resolution, cleanly labeled, temporal failure sequences across 5 metrics are extremely scarce. Synthetic generation provided the controlled environment necessary to validate the predictive architecture cleanly.

**18. What happens with sudden failures?**
Sudden failures without preceding indicators (e.g., a process instantly locking 100% CPU) remain difficult to predict. The system detects them reactively once they occur, but cannot easily forecast them.

**19. What does simulated healing mean?**
The system identifies a recovery action (e.g., "Scale CPU") and safely logs its execution to a file instead of issuing real destructive API calls to a cloud provider.

**20. How is recovery verified?**
Post-healing, the system simulates a restored metric state, re-extracts temporal features, and re-predicts the risk. If the score explicitly drops to a LOW state, recovery is verified.

**21. What is the research contribution?**
The implementation and evaluation of an integrated platform combining temporal telemetry, failure-risk prediction, XAI, root-cause categorization, and simulated healing verification into a single unified system.

**22. What are the limitations?**
Limitations include reliance on synthetic data, lack of production cloud deployment, the fact that sudden failures evade prediction, and that XAI inferences are correlative rather than strictly causal.

**23. How would you deploy this on AWS/Azure/GCP?**
I would replace `monitor.py` with an AWS CloudWatch or Prometheus metrics ingestion pipeline, deploy the API on a managed container service (ECS/Cloud Run), and replace `healer.py` with Lambda functions hitting provider APIs.

**24. How would you improve it with real telemetry?**
I would fine-tune the feature engineering windows, switch to a more complex sequence model (like LSTM or Transformer) once interpretability wrappers were solved, and train on thousands of historical production incident logs.
