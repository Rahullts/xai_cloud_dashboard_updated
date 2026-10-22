import fitz
from pathlib import Path

pdf_path = "01_PAPER_CURRENT/main_compiled.pdf"
doc = fitz.open(pdf_path)
print(f"Total pages in {pdf_path}: {len(doc)}")

artifact_dir = Path(r"C:\Users\rahul\.gemini\antigravity\brain\e7e13116-7a4a-4bcc-ba31-f03cd597e129")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_png = artifact_dir / f"page_{i+1}_of_{len(doc)}.png"
    pix.save(str(out_png))
    print(f"Saved {out_png.name} ({pix.width}x{pix.height})")

print("Rendering complete!")
