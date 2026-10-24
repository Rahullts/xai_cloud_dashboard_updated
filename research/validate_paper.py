import fitz  # PyMuPDF
import re
import os

from pathlib import Path

def validate_pdf(pdf_path=None, baseline_path=None):
    base_dir = Path(__file__).resolve().parent.parent
    if pdf_path is None:
        pdf_path = base_dir / "01_PAPER_CURRENT/main_final.pdf"
    else:
        pdf_path = Path(pdf_path)
        if not pdf_path.is_absolute():
            pdf_path = base_dir / pdf_path

    if baseline_path is None:
        baseline_path = base_dir / "01_PAPER_CURRENT/main_8page_baseline.pdf"
    else:
        baseline_path = Path(baseline_path)
        if not baseline_path.is_absolute():
            baseline_path = base_dir / baseline_path

    print(f"=== VALIDATING PDF: {pdf_path} ===")
    doc = fitz.open(str(pdf_path))
    base_doc = fitz.open(str(baseline_path))
    
    print(f"Final PDF Pages: {len(doc)}")
    print(f"Baseline PDF Pages: {len(base_doc)}")
    
    # Check page dimensions
    for i, page in enumerate(doc):
        rect = page.rect
        width_in = rect.width / 72.0
        height_in = rect.height / 72.0
        print(f"Page {i+1}: {rect.width:.1f} x {rect.height:.1f} pt ({width_in:.2f} x {height_in:.2f} in)")
        
    # Extract full text
    full_text = ""
    page_texts = []
    for i, page in enumerate(doc):
        t = page.get_text()
        page_texts.append(t)
        full_text += f"\n--- PAGE {i+1} ---\n" + t
        
    # 1. Check for unresolved LaTeX references (?? or [?])
    unresolved_cites = re.findall(r'\[\?+\]', full_text)
    unresolved_refs = re.findall(r'\?\?', full_text)
    print(f"\nUnresolved citations [?]: {unresolved_cites}")
    print(f"Unresolved cross-references ??: {unresolved_refs}")
    
    # 2. Check guide acknowledgment
    guide_found = "Shirly" in full_text
    print(f"\nGuide 'Shirly' found: {guide_found}")
    if guide_found:
        for line in full_text.splitlines():
            if "Shirly" in line:
                print(f"  Guide line: {line.strip()}")
                
    # 3. Check author details
    author_found = "Rahul TS" in full_text and "rahult23@karunya.edu.in" in full_text
    print(f"Author 'Rahul TS' & 'rahult23@karunya.edu.in' found: {author_found}")
    
    # 4. Check figures and tables in text
    print("\n--- Figure and Table References in Body Text ---")
    for fig_num in range(1, 5):
        cites_fig = len(re.findall(rf'Fig\.?\s*{fig_num}\b|Figure\s*{fig_num}\b', full_text, re.IGNORECASE))
        print(f"Fig. {fig_num} mentioned {cites_fig} times")
    for tab_roman in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]:
        cites_tab = len(re.findall(rf'Table\s*{tab_roman}\b|TABLE\s*{tab_roman}\b', full_text))
        print(f"Table {tab_roman} mentioned {cites_tab} times")
        
    # 5. Check empirical numbers
    print("\n--- Empirical Numbers Verification ---")
    metrics_to_check = [
        ("180 sequences", "180" in full_text),
        ("7,380 supervised rows", "7,380" in full_text or "7380" in full_text),
        ("Isolation Forest F1 0.760", "0.760" in full_text or "0.76" in full_text),
        ("Temporal LR mean F1 0.692", "0.692" in full_text),
        ("Temporal LR ROC-AUC 0.813", "0.813" in full_text),
        ("Early warning mean lead time 18.06", "18.06" in full_text),
        ("Pre-healing risk 0.884", "0.884" in full_text),
        ("Post-healing risk 0.447", "0.447" in full_text),
        ("Verdict INCONCLUSIVE", "INCONCLUSIVE" in full_text),
    ]
    for label, ok in metrics_to_check:
        print(f"  {label}: {'PASS' if ok else 'FAIL'}")
        
    # 6. Render high-res proofs to artifact directory
    artifact_dir = r"C:\Users\rahul\.gemini\antigravity\brain\e7e13116-7a4a-4bcc-ba31-f03cd597e129"
    print(f"\nRendering high-res page proofs to {artifact_dir}...")
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(artifact_dir, f"final_page_{i+1}_of_{len(doc)}.png")
        pix.save(img_path)
        print(f"  Rendered Page {i+1} -> {img_path}")
        
    print("\nValidation complete!")

if __name__ == "__main__":
    validate_pdf()
