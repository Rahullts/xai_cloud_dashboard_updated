import fitz
from pathlib import Path

fig_dir = Path("C:/Users/rahul/.gemini/antigravity/scratch/xai_cloud_dashboard_updated/01_PAPER_CURRENT/figures")
out_dir = Path("C:/Users/rahul/.gemini/antigravity/brain/e7e13116-7a4a-4bcc-ba31-f03cd597e129")

fig_names = [
    "fig1_system_architecture",
    "fig2_temporal_features",
    "fig4_model_comparison",
    "fig5_scenario_performance",
    "fig6_xai_contributions",
    "fig7_verification"
]

for name in fig_names:
    pdf_path = fig_dir / f"{name}.pdf"
    if pdf_path.exists():
        doc = fitz.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(dpi=300)
        out_png = out_dir / f"{name}_light.png"
        pix.save(out_png)
        print(f"Rendered {out_png.name} ({pix.width}x{pix.height})")
