import zipfile
from pathlib import Path

base_dir = Path("C:/Users/rahul/.gemini/antigravity/scratch/xai_cloud_dashboard_updated")
source_dir = base_dir / "01_PAPER_CURRENT"
out_zip = base_dir / "OVERLEAF_PACKAGE.zip"

print(f"Creating Overleaf package: {out_zip}...")
with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
    # Add root LaTeX files
    for item in ["main.tex", "IEEEtran.cls", "IEEEtran.bst", "references.bib", "main_final.pdf"]:
        fpath = source_dir / item
        if fpath.exists():
            zf.write(fpath, arcname=item)
            print(f"  Added {item}")
            
    # Add figures folder
    fig_dir = source_dir / "figures"
    for fig in fig_dir.glob("*"):
        if fig.is_file():
            arcname = f"figures/{fig.name}"
            zf.write(fig, arcname=arcname)
            print(f"  Added {arcname}")

print(f"ZIP package successfully created! Size: {out_zip.stat().st_size} bytes")
