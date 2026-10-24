import fitz
from pathlib import Path

pdf_path = Path("C:/Users/rahul/.gemini/antigravity/scratch/xai_cloud_dashboard_updated/01_PAPER_CURRENT/main_final.pdf")
out_dir = Path("C:/Users/rahul/.gemini/antigravity/brain/e7e13116-7a4a-4bcc-ba31-f03cd597e129")

doc = fitz.open(pdf_path)
print(f"Opened {pdf_path.name}: {len(doc)} pages")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_file = out_dir / f"light_page_{i+1}_of_{len(doc)}.png"
    pix.save(out_file)
    print(f"Rendered Page {i+1}: {out_file.name} ({pix.width}x{pix.height})")
