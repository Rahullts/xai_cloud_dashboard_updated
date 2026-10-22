import io
import os
import subprocess
import tarfile
from pathlib import Path
import pypdf

def compile_latex(source_dir="01_PAPER_CURRENT", tex_name="main.tex", output_pdf="01_PAPER_CURRENT/main_compiled.pdf"):
    source_path = Path(source_dir)
    print(f"Creating archive from {source_path} targeting {tex_name}...")
    
    tar_name = "temp_paper_payload.tar.gz"
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
        "-o", output_pdf
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(tar_name):
        os.remove(tar_name)
        
    try:
        reader = pypdf.PdfReader(output_pdf)
        num_pages = len(reader.pages)
        print(f"COMPILATION SUCCESS! Output PDF: {output_pdf} ({num_pages} pages)")
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            first = txt.splitlines()[0] if txt else "[EMPTY]"
            last = txt.splitlines()[-1] if txt else "[EMPTY]"
            print(f"  Page {i+1}: chars={len(txt)} | '{first[:40]}' ... '{last[:40]}'")
        return num_pages
    except Exception as e:
        print("COMPILATION FAILED or returned non-PDF:")
        with open(output_pdf, "rb") as f:
            print(f.read().decode("utf-8", errors="ignore")[:1000])
        return None

if __name__ == "__main__":
    compile_latex()
