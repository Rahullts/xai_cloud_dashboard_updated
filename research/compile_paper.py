import io
import os
import subprocess
import tarfile
from pathlib import Path
import pypdf

def compile_latex(source_dir=None, tex_name="main.tex", output_pdf=None):
    base_dir = Path(__file__).resolve().parent.parent
    if source_dir is None:
        source_path = base_dir / "01_PAPER_CURRENT"
    else:
        source_path = Path(source_dir)
        if not source_path.is_absolute():
            source_path = base_dir / source_path

    if output_pdf is None:
        out_path = source_path / "main_compiled.pdf"
    else:
        out_path = Path(output_pdf)
        if not out_path.is_absolute():
            out_path = base_dir / out_path

    print(f"Creating archive from {source_path} targeting {tex_name}...")
    
    tar_name = str(base_dir / "temp_paper_payload.tar.gz")
    with tarfile.open(tar_name, "w:gz") as tar:
        for f in source_path.glob("**/*"):
            if f.is_file():
                if f.name.endswith(".pdf") and f.parent.name != "figures":
                    continue # Skip output PDFs
                if f.name.endswith(".tar.gz"):
                    continue
                arcname = f.relative_to(source_path).as_posix()
                tar.add(f, arcname=arcname)
                
    tar_size = os.path.getsize(tar_name)
    print(f"Archive created: {tar_size} bytes. Uploading to compiler...")
    
    cmd = [
        "curl.exe", "-s",
        "-F", f"file=@{tar_name}",
        f"https://latexonline.cc/data?target={tex_name}",
        "-o", str(out_path)
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(tar_name):
        os.remove(tar_name)
        
    try:
        reader = pypdf.PdfReader(str(out_path))
        num_pages = len(reader.pages)
        print(f"COMPILATION SUCCESS! Output PDF: {out_path} ({num_pages} pages)")
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            first = txt.splitlines()[0] if txt else "[EMPTY]"
            last = txt.splitlines()[-1] if txt else "[EMPTY]"
            print(f"  Page {i+1}: chars={len(txt)} | '{first[:40]}' ... '{last[:40]}'")
        return num_pages
    except Exception as e:
        print("COMPILATION FAILED or returned non-PDF:", e)
        if os.path.exists(out_path):
            with open(out_path, "rb") as f:
                print(f.read().decode("utf-8", errors="ignore")[:1000])
        return None

if __name__ == "__main__":
    compile_latex()
