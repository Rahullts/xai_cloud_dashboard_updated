# Paper-Ready Figure Plan

Recommend figures based ONLY on existing evidence.

### Figure 1: Overall system architecture
*Requires regeneration from validated experiment outputs.*
**Description**: Block diagram showing the data flow: Telemetry -> Temporal Sliding Buffer -> Feature Extraction -> Logistic Regression Prediction -> Coefficient-based XAI -> Root-Cause Mapping -> Simulated Healer -> Post-Healing Verification.

### Figure 2: Temporal feature engineering pipeline
*Requires regeneration from validated experiment outputs.*
**Description**: Visual representation of the 10-timestep sliding window capturing 5 base metrics and expanding them into 45 temporal representations (current, means, deltas, slopes, standard deviations).

### Figure 3: Model comparison
*Requires regeneration from validated experiment outputs.*
**Description**: Bar chart grouping F1 and ROC-AUC scores for Majority Baseline, Threshold Baseline, Logistic Regression, Random Forest, and Gradient Boosting across the 5 independent seeds.

### Figure 4: Contamination vs performance
*Requires regeneration from validated experiment outputs.*
**Description**: Line plot showing F1 Score and Recall increasing as contamination increases from 0.05 to 0.20 in the Isolation Forest validation phase.

### Figure 5: Scenario-level predictive performance
*Requires regeneration from validated experiment outputs.*
**Description**: Stacked bar chart showing True Negatives, False Positives, False Negatives, and True Positives broken down by the 6 synthetic failure scenarios.

### Figure 6: Example XAI contribution visualization
*Requires regeneration from validated experiment outputs.*
**Description**: Horizontal bar chart visualizing the top 5 positive and negative contributing features for a selected sequence, directly matching the coefficient * scaled value output from `xai_case_study_results.json`.

### Figure 7: End-to-end self-healing workflow
*Requires regeneration from validated experiment outputs.*
**Description**: Sequence diagram showing the system transitioning from NORMAL -> HIGH RISK -> Action Execution -> Post-Healing Window -> RECOVERED/INCONCLUSIVE state.
