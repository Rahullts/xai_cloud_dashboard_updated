import warnings
import pypdf

warnings.filterwarnings("ignore")

def inspect_pdf(pdf_path="01_PAPER_CURRENT/main_compiled.pdf"):
    reader = pypdf.PdfReader(pdf_path)
    print(f"=== {pdf_path}: {len(reader.pages)} PAGES ===")
    for i, page in enumerate(reader.pages):
        txt = page.extract_text()
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        landmarks = []
        for l in lines:
            if any(l.startswith(prefix) for prefix in ["I. ", "II. ", "III. ", "IV. ", "V. ", "VI. ", "VII. ", "VIII. ", "ACKNOWLEDG", "REFERENCES", "Fig.", "TABLE "]):
                landmarks.append(l[:45])
        print(f"\n--- PAGE {i+1} ({len(lines)} lines, {len(txt)} chars) ---")
        print(f"  Start: {lines[0] if lines else '[EMPTY]'}")
        print(f"  Landmarks: {landmarks}")
        print(f"  End:   {lines[-1] if lines else '[EMPTY]'}")

if __name__ == "__main__":
    inspect_pdf()
