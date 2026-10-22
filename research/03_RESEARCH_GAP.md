# Research Gap

## 1. What the Literature Shows

### Anomaly Detection
The dominant body of work in cloud anomaly detection addresses individual-component detection: Isolation Forest, autoencoders, LSTM-based log analysis (DeepLog [Ref01], LogAnomaly [Ref03]), and VAE-based metric monitoring (OmniAnomaly [Ref06], Donut [Ref07]). These approaches achieve high detection accuracy on specific telemetry types but operate largely as black boxes that flag anomalies without explaining the contributing factors. He et al. [Ref12] showed that classical ML methods already achieve competitive performance on certain log anomaly datasets, but neither classical nor deep learning detectors connect their outputs to remediation.

### AIOps and Intelligent Operations
The AIOps concept (Lin et al. [Ref02]; Bogatinovski et al. [Ref10]) describes an aspirational integration of anomaly detection, root cause analysis, and automated remediation within a single intelligent operations pipeline. Survey papers (Niu et al. [Ref18]; Islam et al. [Ref16]) confirm this integration as an open challenge. Most production AIOps tooling addresses components of the pipeline separately rather than as a unified workflow evaluated end-to-end.

### Explainability
LIME [Ref04] and SHAP [Ref05] are the dominant post-hoc explanation methods in the literature. They are widely applied in security and anomaly contexts (Guan et al. [Ref14]; Bogatinovski and Nedelkoski [Ref10]). However, these methods introduce approximation: LIME uses local surrogate models; SHAP uses Shapley value estimation. For logistic regression specifically, direct coefficient attribution is exact and requires no approximation, but its use in cloud operational settings is infrequently documented.

### Root Cause Analysis
RCA methods in the literature (CloudRanger [Ref08]; CauseInfer [Ref19]; Weng et al. [Ref15]) rely on causal graph construction from distributed traces, service dependencies, or performance metrics. These methods require instrumented infrastructure and graph construction at deployment time. Evidence-based heuristic RCA from XAI attributions — as implemented here — is lighter-weight and does not require trace data, but also makes no causal claims.

### Self-Healing and Remediation
Self-healing systems in the literature (Samir et al. [Ref14]; Zhang et al. [Ref20]) either use fuzzy logic or predefined script execution triggered by threshold events. Seer [Ref13] predicts QoS violations before they occur but does not include an XAI or RCA stage. PreFix [Ref16] predicts switch failures days in advance but is specific to networking hardware. None of the reviewed systems combine temporal prediction, model-based explanation, evidence-based category inference, rule-based decision logic, simulated recovery, and post-recovery model verification as a single evaluated workflow.

---

## 2. The Defensible Research Gap

The literature consistently addresses individual stages of the cloud management lifecycle — detection OR prediction OR explanation OR remediation — in isolation. Systems that approach end-to-end integration typically either:

(a) Lack explainability (e.g., DeepLog, OmniAnomaly predict but do not explain), or  
(b) Lack prediction capability (e.g., threshold-based self-healing systems act on current state, not temporal trajectory), or  
(c) Lack post-recovery verification (most remediation systems declare success without re-evaluating system state using the same model).

The gap is therefore:

**No surveyed work explicitly integrates: temporal rolling-feature prediction + deterministic model-coefficient attribution + evidence-based failure-category inference + autonomous decision logic + simulated recovery + post-recovery re-evaluation using the same predictive model into a single evaluated research prototype.**

This gap does not support the claim "no such system exists anywhere." It supports the more defensible claim: "To the best of our knowledge, a fully integrated pipeline connecting temporal prediction, linear coefficient attribution, category inference, decision logic, and post-recovery verification within a single cloud management prototype has not been demonstrated in the surveyed literature."

---

## 3. What We Do NOT Claim

- We do not claim this is the first system to combine anomaly detection with remediation.
- We do not claim LR with coefficient attribution is a new XAI method.
- We do not claim superiority over deep learning anomaly detectors (those systems address different problem settings).
- We do not claim the system operates on real production infrastructure.
- We do not claim causal root-cause detection.
