# Final Validation Report: 7-Page IEEE Conference Paper

**Project:** Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform  
**Target PDF:** `01_PAPER_CURRENT/main_final.pdf`  
**LaTeX Source:** `01_PAPER_CURRENT/main.tex`  
**Bibliography:** `01_PAPER_CURRENT/references.bib`  
**Validation Date:** October 2026  
**Status:** **PASSED ALL CHECKS (100% Conformance)**

---

## 1. Compilation Verification

- **Engine:** pdfTeX (`latexonline.cc` / standard TeX Live toolchain)
- **Document Class:** `IEEEtran.cls` (Version 1.8b, conference mode)
- **Bibliography Processor:** `bibtex` with `IEEEtran.bst` (Version 1.14)
- **Exit Code:** `0` (Clean compilation, zero errors)
- **Deliverable Path:** `C:\Users\rahul\.gemini\antigravity\scratch\xai_cloud_dashboard_updated\01_PAPER_CURRENT\main_final.pdf`
- **Output Page Dimensions:** 612.0 pt $\times$ 792.0 pt (8.50 in $\times$ 11.00 in, Standard US Letter across all 7 pages)
- **Total Page Count:** **EXACTLY 7 PAGES** (Zero overflow onto Page 8)

---

## 2. Layout, Typography & Visual Inspection

High-resolution page proofs were rendered and verified:

| Page | Content Overview | Verification Outcome |
| :---: | :--- | :---: |
| **1** | Title, side-by-side author block (Rahul TS & Dr. S. Shirly), Abstract, Keywords, Section I (Introduction), Section II start | Title centered, dual author block formatted per IEEEtran standard without overlap, clean margins. |
| **2** | Section II (Related Work & Research Gaps, Subsections II-A–II-G), RQ1–RQ5, Contributions 1–5 | Two-column justified text, consistent headings, clean citation brackets [1]–[20]. |
| **3** | Section III (Architecture & Methodology), Fig. 1 (10-stage pipeline diagram), Equations (1) & (2), Table I (Action Mapping) | Fig. 1 clear vector graphic, equations properly centered and numbered, Table I cleanly formatted with booktabs. |
| **4** | Subsection III-E (Verification Protocol with simulation clarity), Section IV (Experimental Setup), Table II (Dataset Splits), Section V-A start | Table II crisp, positive label formulation clear, no margin overflow. |
| **5** | Section V-A/B, Table III (Isolation Forest vs Threshold), Table IV (5-seed models), Fig. 2 (Model comparison chart), Table V (Per-scenario metrics) | Tables III, IV, V fit column width perfectly, Fig. 2 clear vector chart with legible axis labels and legend. |
| **6** | Section V-D/E/F, Table VI (Lead-time statistics), Table VII (XAI case studies), Fig. 3 (Feature attribution chart), Table VIII (Verification table), Fig. 4 (Recovery flow diagram), Section VI (Discussion) | Fig. 3 and Fig. 4 sharp and readable, Table VIII formatted cleanly, Section VI discussion subsections styled cleanly. |
| **7** | Section VII (Limitations, items 1–7), Section VIII (Conclusion & Future Work), Acknowledgment block (Dr. S. Shirly), References [1]–[20] | Guide Dr. S. Shirly acknowledged, 20 references balanced across both columns, terminates precisely at bottom of Page 7. |

---

## 3. Automated Validation Suite Results

Validation executed via `research/validate_paper.py`:

```
============================================================
           IEEE PAPER AUTOMATED VALIDATION SUITE           
============================================================
[PASS] Page Count: 7 pages (Expected: 7)
[PASS] Paper Dimensions: 612.0 x 792.0 pt (US Letter) across all 7 pages
[PASS] Unresolved Citations ([?]): 0 found
[PASS] Unresolved References (??): 0 found
[PASS] Project Guide 'Dr. S. Shirly' found in author block & acknowledgment
[PASS] Author 'Rahul TS' & 'rahult23@karunya.edu.in' found in text
[PASS] Figure 1 referenced in body text (3 times)
[PASS] Figure 2 referenced in body text (3 times)
[PASS] Figure 3 referenced in body text (3 times)
[PASS] Figure 4 referenced in body text (3 times)
[PASS] Table I referenced in body text (2 times)
[PASS] Table II referenced in body text (2 times)
[PASS] Table III referenced in body text (5 times)
[PASS] Table IV referenced in body text (5 times)
[PASS] Table V referenced in body text (2 times)
[PASS] Table VI referenced in body text (2 times)
[PASS] Table VII referenced in body text (2 times)
[PASS] Table VIII referenced in body text (2 times)
------------------------------------------------------------
           QUANTITATIVE EMPIRICAL METRIC AUDIT             
------------------------------------------------------------
[PASS] Metric 'Total Sequences' matches artifact (180 == 180)
[PASS] Metric 'Total Supervised Rows' matches artifact (7380 == 7380)
[PASS] Metric 'Isolation Forest F1' matches artifact (0.760 == 0.760)
[PASS] Metric 'Temporal LR F1 Mean' matches artifact (0.692 == 0.692)
[PASS] Metric 'Temporal LR ROC-AUC Mean' matches artifact (0.813 == 0.813)
[PASS] Metric 'Mean Lead Time' matches artifact (18.06 == 18.06)
[PASS] Metric 'Pre-Healing Risk' matches artifact (0.884 == 0.884)
[PASS] Metric 'Post-Healing Risk' matches artifact (0.447 == 0.447)
[PASS] Metric 'Recovery Verdict' matches artifact (INCONCLUSIVE == INCONCLUSIVE)
============================================================
OVERALL RESULT: ALL CHECKS PASSED (100% Conformance)
============================================================
```

---

## 4. Guide Submission Checklist

- [x] **Author block correctly lists Rahul TS and Dr. S. Shirly with affiliations.**
- [x] **All sections I–VIII are present and properly titled.**
- [x] **Figures 1–4 and Tables I–VIII appear, properly sized, and are cited in text.**
- [x] **Equations (1) and (2) typeset correctly with zero margin bleed.**
- [x] **All numeric results match the project JSON files.**
- [x] **Key phrases indicating simulated actions are clearly labeled.**
- [x] **No unresolved citations or cross-references (`[?]` or `??`).**
- [x] **Total page count is EXACTLY 7 pages (US Letter, 10pt, IEEEtran).**
