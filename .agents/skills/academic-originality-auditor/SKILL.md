---
name: academic-originality-auditor
description: Audits scientific manuscripts and LaTeX source files for Turnitin, iThenticate, and IEEE CrossCheck similarity compliance, detects formulaic phrasing, verifies reference authenticity, and provides academic similarity reduction strategies.
---

# Academic Originality & Similarity Auditor

A specialized skill for auditing research papers, conference manuscripts, and dissertations against academic similarity, plagiarism detection, and reference integrity standards (Turnitin, iThenticate, IEEE CrossCheck, and Google Scholar).

---

## 1. Compliance Benchmarks

When reviewing academic manuscripts, adhere strictly to publication thresholds:

| Metric | Target Standard | Action Threshold |
| :--- | :--- | :--- |
| **Overall Similarity Index** | $\le 15\%$ | Flag and rephrase if $\ge 18\%$ |
| **Single-Source Similarity** | $< 1.5\%$ per source | Immediate rewrite if $\ge 2.0\%$ |
| **Verbatim Sentence Matches** | $0$ unquoted sentences | Prohibit 6+ word contiguous overlaps |
| **Citation Authenticity** | $100\%$ verified | Zero hallucinated DOIs or synthetic papers |
| **Self-Plagiarism / Salami Slicing** | Distinct contributions | Differentiate from prior student/mini reports |

---

## 2. Multi-Stage Originality Audit Protocol

### Stage 1: Lexical & N-Gram Overlap Scan
1. Extract plain text from `.tex`, `.md`, or `.pdf`.
2. Inspect Section II (Related Work), Section I (Introduction), and Section III (Methodology) for standard academic clichés or verbatim phrasing borrowed from source literature.
3. Identify contiguous 5-gram to 8-gram matches that mirror published abstracts or surveys.

### Stage 2: Reference & Citation Integrity Check
1. For each `\cite{...}` key in the text, locate its `@article` or `@inproceedings` entry in `references.bib`.
2. Verify:
   - Does the title match the official indexed publication?
   - Are the author names and order exact?
   - Is the publication year and venue genuine?
   - Is the DOI valid and resolvable?
3. Flag any synthetic citations, mismatched titles, or broken URLs.

### Stage 3: Formulaic & Template Detection
Scan for repetitive or robotic sentence scaffolds:
- *"In modern times, cloud computing has become increasingly important..."*
- *"X et al. proposed Y and achieved Z..."* (repeated across entire paragraphs)
- *"The rest of the paper is organized as follows..."*
Replace with active-voice contextual framing that directly emphasizes the research problem, empirical tension, and specific contributions.

### Stage 4: Non-Destructive Scientific Paraphrasing
When lowering similarity, adhere to the **Invariance Rule**:
- **NEVER** alter experimental numbers, metrics, thresholds, or seeds (e.g. F1 `0.692`, `45` features, `18.06` timesteps).
- **NEVER** alter author names, guide names, or institutional affiliations.
- **NEVER** rename mathematical symbols without updating corresponding equations and tables.
- **Transform syntax and perspective:** Shift passive cataloging into analytical comparison, invert clausal dependencies, and contextualize findings within the system's operational constraints.

---

## 3. Best Practices for IEEE Manuscript Preparation

1. **Section II (Related Work):** Group papers by conceptual methodology rather than summarizing one paper per sentence. Contrast tradeoffs instead of stating isolated results.
2. **Methodology:** Describe the mathematical formulations and state machines directly in the paper's own terminology.
3. **Acknowledgment:** Explicitly disclose language-refinement or formatting assistance in compliance with IEEE AI author policies while asserting that all scientific findings and code remain the author's original work.
