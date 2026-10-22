# Final Demonstration Script

**Title:** Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform
**Duration:** 5-7 Minutes

## 1. Introduction (1 min)
*Open the Dashboard in the browser.*
"Welcome to the demonstration of our autonomous self-healing cloud platform. What you see here is a real-time temporal monitoring dashboard. The system isn't just looking at current metrics; it maintains a rolling sliding window to predict failures before they happen."

## 2. Normal Operations (1 min)
*Ensure 'Normal (Stable)' is selected.*
"Currently, the system is in a normal state. Notice the 'System Healthy' banner. The Risk Score is near zero. Below, the XAI and Root Cause panels are quiet because the metrics are well within safe, stable bounds."

## 3. Triggering Gradual Failure (2 mins)
*Click the 'Memory Leak' or 'Combined Failure' button.*
"Let's simulate a Gradual Memory Leak. As the backend generates the synthetic data stream, watch the Memory metric slowly climb. Because our model calculates temporal features—like the 5-step trend and 10-step variability—it detects the degradation trajectory. Notice the Risk Score increasing, pushing the system into the MEDIUM, and then HIGH RISK state."

## 4. Explainable AI & Root Cause (1 min)
*Point to the XAI panel and Root Cause panel.*
"The system has predicted a failure. But why? Look at the XAI panel. It uses exact Logistic Regression coefficient attribution to show us the top mathematical drivers. You can see 'Memory 10-step trend' and 'Memory variability' pushing the score into the red. Because of this evidence, the Root Cause Engine has categorized this as a 'MEMORY LEAK'."

## 5. Autonomous Healing & Verification (1 min)
*Point to the log panel and watch the post-healing reset.*
"Because the risk hit a critical threshold, the Decision Engine mapped the 'Memory Leak' to an autonomous recovery action: 'Restart affected service / reclaim memory'. This was safely logged by the simulated healer. Notice the verification step: the system gathered post-healing telemetry, confirmed the risk dropped back to LOW, and verified the state as 'RECOVERED'. The buffer is now warming up again natively."

## 6. Limitations & Conclusion (1 min)
"While the system successfully predicts and explains gradual failures, sudden unpredictable spikes remain a limitation, which the model catches reactively rather than predictively. Additionally, this is a simulated environment—future work would involve wiring the healer directly to AWS CloudWatch and Lambda. Thank you."
