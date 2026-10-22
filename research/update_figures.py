import fitz

updates = [
    (
        "01_PAPER_CURRENT/figures/fig1_system_architecture.svg",
        "01_PAPER_CURRENT/figures/fig1_system_architecture.pdf",
        [("Eight-Stage Integrated Pipeline", "Ten-Stage Integrated Pipeline")]
    ),
    (
        "01_PAPER_CURRENT/figures/fig4_model_comparison.svg",
        "01_PAPER_CURRENT/figures/fig4_model_comparison.pdf",
        [("Figure 4 — Temporal Model Comparison", "Figure 2 — Temporal Model Comparison")]
    ),
    (
        "01_PAPER_CURRENT/figures/fig6_xai_contributions.svg",
        "01_PAPER_CURRENT/figures/fig6_xai_contributions.pdf",
        [("Figure 6 — XAI Coefficient Contributions (Case A: disk_gradual_exhaustion)", "Figure 3 — XAI Feature Contributions (Case A: Gradual Disk Exhaustion)")]
    ),
    (
        "01_PAPER_CURRENT/figures/fig7_verification.svg",
        "01_PAPER_CURRENT/figures/fig7_verification.pdf",
        [("Figure 7 — Recovery Verification", "Figure 4 — Recovery Verification")]
    ),
]

for svg_in, pdf_out, replacements in updates:
    with open(svg_in, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"Replaced '{old}' with '{new}' in {svg_in}")
        else:
            print(f"Warning: '{old}' not found in {svg_in}")
    with open(svg_in, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Convert to PDF via fitz
    svg_bytes = content.encode("utf-8")
    doc = fitz.open(stream=svg_bytes, filetype="svg")
    pdf_bytes = doc.convert_to_pdf()
    pdf_doc = fitz.open("pdf", pdf_bytes)
    pdf_doc.save(pdf_out)
    print(f"Saved updated vector PDF to {pdf_out}")
