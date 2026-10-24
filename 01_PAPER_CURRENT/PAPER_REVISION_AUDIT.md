# IEEE Paper Revision & Scientific Quality Audit Report

**Manuscript Title:** Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform  
**Target Venue:** IEEE Conference Format (`IEEEtran.cls` v1.8b, `conference` mode)  
**Authors:**  
1. **Rahul TS** (Author)  
   Department of Computer Science and Engineering, School of Computer Science and Technology, Karunya Institute of Technology and Science, Coimbatore, Tamil Nadu, India (`rahult23@karunya.edu.in`)  
2. **Dr. S. Shirly** (Project Guide / Supervisor)  
   Department of Computer Science and Engineering, School of Computer Science and Technology, Karunya Institute of Technology and Science, Coimbatore, Tamil Nadu, India  
**Workspace:** `xai_cloud_dashboard_updated/01_PAPER_CURRENT`  
**Compiled Deliverable:** `main_final.pdf` (**Exactly 7 pages**, US Letter, 612 x 792 pt)  
**Audit Date:** October 2026  
**Status:** **APPROVED & FULLY VERIFIED (100% Conformance)**

---

## 1. Executive Summary

This document provides a comprehensive audit of all corrections, enhancements, structural reconciliations, academic English edits, and formatting validations performed on the research paper. 

Through systematic audit and remediation:
- The paper has been strictly formatted using the official IEEE conference template (`IEEEtran.cls` v1.8b) at **exactly 7 pages** with zero overflow onto Page 8.
- The project guide **Dr. S. Shirly** is correctly positioned in the Page 1 author block alongside Rahul TS and prominently acknowledged in the Page 7 Acknowledgment section.
- Rahul TS's affiliation and email address (`rahult23@karunya.edu.in`) are preserved exactly.
- Complete academic English, grammatical, and typographical refinement was applied across all sections.
- The threshold-baseline discrepancy between Table III ($F_1 = 0.606$) and Table IV ($F_1 = 0.156$) is rigorously clarified: Table III assesses instantaneous acute failure detection, whereas Table IV evaluates 10-step advance predictive early warning.
- Mathematical notations for feature attribution ($c_i = z_i \cdot w_i$) and evidence aggregation ($E_r = \sum_{i \in \mathcal{F}_r} |c_i|$) are formalized.
- All 9 quantitative claims were programmatically verified against raw experimental JSON data.
- The compiled 7-page PDF (`main_final.pdf`) has zero unresolved citations (`[?]`), zero broken references (`??`), and zero margin violations.

---

## 2. Structural & Template Conformance

| Aspect | Requirement | Implemented Status | Verification Result |
| :--- | :--- | :--- | :---: |
| **Document Class** | Official IEEE Conference | `\documentclass[conference]{IEEEtran}` | **CONFIRMED** |
| **Page Geometry** | IEEE Standard US Letter | 8.5" $\times$ 11" (612.0 $\times$ 792.0 pt), standard margins | **PASS** |
| **Author Block** | Side-by-side multi-author | Rahul TS & Dr. S. Shirly side-by-side (`\author{...\and...}`) | **CONFIRMED** |
| **Project Guide** | Dr. S. Shirly | Present on Page 1 (author block) and Page 7 (acknowledgment) | **CONFIRMED** |
| **Total Page Count** | **Exactly 7 Pages** | 7 pages (ends cleanly on Page 7; 0 lines on Page 8) | **PERFECT** |
| **Bibliography Style** | Official IEEE Style | `IEEEtran.bst` v1.14 with 20 balanced references | **CONFIRMED** |
| **Figure & Tables** | 4 Figures, 8 Tables | Numbered sequentially, referenced in body text | **CONFIRMED** |

---

## 3. Section-by-Section Academic & Technical Revisions

### Abstract & Keywords
- **Content:** Outlines the 10-stage autonomous cloud management platform, unsupervised Isolation Forest baseline ($F_1 = 0.760$), temporal Logistic Regression early warning ($F_1 = 0.692 \pm 0.036$, ROC-AUC $0.813 \pm 0.021$, mean lead time 18.06 timesteps), deterministic XAI coefficient attribution, and conservative `INCONCLUSIVE` post-healing verification verdict.
- **Keywords:** Standard IEEE terms: *Cloud monitoring, anomaly detection, temporal feature engineering, explainable AI, coefficient attribution, AIOps, self-healing, failure prediction, autonomous remediation.*

### Section I: Introduction
- Motivation for AIOps and proactive fault prediction over reactive threshold monitoring.
- Clear statement of the 5 main contributions.

### Section II: Related Work and Research Gap
- Subsections II-A to II-E covering anomaly detection, AIOps surveys, XAI methods, root cause analysis, and self-healing.
- Research questions RQ1–RQ5 and explicit identification of the operational integration gap.

### Section III: System Architecture and Methodology
- 10-stage end-to-end pipeline: Ingestion, Anomaly Detection, Temporal Buffer, Feature Extraction (45 features), Failure Risk Prediction, XAI Attribution, Likely Failure Category, Autonomous Decision Engine, Simulated Recovery, and Post-Recovery Verification.
- Mathematical rigor: Equation (1) $c_i = z_i \cdot w_i$ and Equation (2) $E_r = \sum_{i \in \mathcal{F}_r} |c_i|$.
- Simulation transparency: Clearly indicates that remediation is simulated string dispatch in a controlled simulation environment rather than live cloud API execution.

### Section IV: Experimental Setup
- 180 sequences across 8 scenario profiles: 120 train (4,920 rows), 30 val (1,230 rows), 30 test (1,230 rows) totaling 7,380 supervised rows.
- 10-step forward prediction horizon strictly excluding current observation at timestep $t$ to eliminate leakage.

### Section V: Experimental Results and Analysis
- Table III: Isolation Forest snapshot anomaly detection ($F_1 = 0.760$ vs. threshold baseline $0.606$).
- Table IV & Fig. 2: 5-seed temporal model comparison (Logistic Regression $F_1 = 0.692 \pm 0.036$, ROC-AUC $0.813 \pm 0.021$; Random Forest $0.696$; Gradient Boosting $0.699$).
- Table V: Per-scenario breakdown for 8 profiles.
- Table VI: Early warning lead time statistics (mean 18.06 timesteps, median 16.0, min 4, max 33).
- Table VII & Fig. 3: XAI attribution case studies and feature contribution chart.
- Table VIII & Fig. 4: Post-recovery verification flow (pre-heal risk 0.884 CRITICAL $\to$ post-heal risk 0.447 MEDIUM $\to$ `INCONCLUSIVE`).

### Section VI: Discussion
- 4 thematic subsections addressing temporal vs. threshold detection, model selection trade-offs, XAI diagnostic clarity, and verification honesty.

### Section VII: System Limitations and Threats to Validity
- 7 explicitly acknowledged limitations: synthetic telemetry, simulated remediation, sudden failure bounds, non-causal heuristic attribution, synthetic post-healing data, startup model fitting, and lack of production multi-tenant trace validation.

### Section VIII: Conclusion and Future Work
- Concise summary of contributions and future research directions (production trace benchmarking, orchestration API integration, deep sequence comparisons).

### Acknowledgment & References
- Expresses sincere gratitude to project guide **Dr. S. Shirly**, Assistant Professor, Department of Computer Science and Engineering, Karunya Institute of Technology and Science.
- Mandatory IEEE AI-tool assistance disclosure included.
- References [1]–[20] formatted via `IEEEtran.bst` and cleanly balanced across Page 7 columns.

---

## 4. Empirical Consistency Verification

| Metric | Source JSON File | JSON Value | Paper Value | Status |
| :--- | :--- | :---: | :---: | :---: |
| Total Sequences | `results/temporal_dataset_summary.json` | 180 | 180 | **MATCH** |
| Supervised Rows | `results/temporal_dataset_summary.json` | 7,380 | 7,380 | **MATCH** |
| Isolation Forest F1 | `results/phase2_anomaly_detection.json` | 0.7601 | 0.760 | **MATCH** |
| Temporal LR F1 (Mean) | `results/predictive_evaluation_summary.json` | 0.6917 | 0.692 | **MATCH** |
| Temporal LR ROC-AUC (Mean) | `results/predictive_evaluation_summary.json` | 0.8133 | 0.813 | **MATCH** |
| Mean Lead Time | `results/lead_time_statistics.json` | 18.0556 | 18.06 timesteps | **MATCH** |
| Pre-Healing Risk | `results/post_healing_evaluation_test_6.json` | 0.8837 (Critical) | 0.884 (CRITICAL) | **MATCH** |
| Post-Healing Risk | `results/post_healing_evaluation_test_6.json` | 0.4471 (Medium) | 0.447 (MEDIUM) | **MATCH** |
| Recovery Verdict | `results/post_healing_evaluation_test_6.json` | INCONCLUSIVE | INCONCLUSIVE | **MATCH** |

---

## 5. Guide Checklist & Approval Verdict

- [x] **Author block correctly lists Rahul TS and Dr. S. Shirly with affiliations.**
- [x] **All sections I–VIII are present and properly titled.**
- [x] **Figures 1–4 and Tables I–VIII appear, properly sized, and are cited in text.**
- [x] **Equations (1) and (2) typeset correctly with zero margin bleed.**
- [x] **All numeric results match the project JSON files.**
- [x] **Key phrases indicating simulated actions are clearly labeled.**
- [x] **No unresolved citations or cross-references (`[?]` or `??`).**
- [x] **Total page count is EXACTLY 7 pages (US Letter, 10pt, IEEEtran).**

**Readiness Verdict:** The manuscript is 100% review-ready and compliant with IEEE submission standards.
