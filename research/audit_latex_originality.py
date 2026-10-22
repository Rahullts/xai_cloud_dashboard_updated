import re
import sys
from pathlib import Path

tex_path = Path("01_PAPER_CURRENT/main.tex")
bib_path = Path("01_PAPER_CURRENT/references.bib")

tex = tex_path.read_text(encoding="utf-8")
bib = bib_path.read_text(encoding="utf-8")

print("=" * 60)
print("ACADEMIC ORIGINALITY & LATEX INTEGRITY AUDIT")
print("=" * 60)

# 1. Citations Audit
citations = set()
for m in re.finditer(r'\\cite\{([^}]+)\}', tex):
    for k in m.group(1).split(','):
        citations.add(k.strip())

bib_keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib))
missing = citations - bib_keys
unused = bib_keys - citations

print(f"\n[1] CITATION INTEGRITY:")
print(f"    - Unique in-text citations: {len(citations)}")
print(f"    - Bibliography entries in .bib: {len(bib_keys)}")
if missing:
    print(f"    - [CRITICAL] Missing citations in bib: {missing}")
else:
    print("    - [PASS] All in-text citations exist in references.bib")
if unused:
    print(f"    - [INFO] Unused references in bib: {unused}")
else:
    print("    - [PASS] Zero orphaned references in bibliography.")

# 2. Structural & LaTeX Syntax Check
open_braces = tex.count('{')
close_braces = tex.count('}')
print(f"\n[2] LATEX SYNTAX BALANCE:")
print(f"    - Open braces: {open_braces}, Close braces: {close_braces}")
if open_braces == close_braces:
    print("    - [PASS] Braces perfectly balanced.")
else:
    print(f"    - [CRITICAL] Brace mismatch: difference = {open_braces - close_braces}")

# 3. Cross-reference Audit
labels = set(re.findall(r'\\label\{([^}]+)\}', tex))
refs = set(re.findall(r'\\ref\{([^}]+)\}', tex))
unresolved_refs = refs - labels
print(f"\n[3] CROSS-REFERENCE RESOLUTION:")
print(f"    - Defined labels: {len(labels)}")
print(f"    - In-text references: {len(refs)}")
if unresolved_refs:
    print(f"    - [CRITICAL] Unresolved references: {unresolved_refs}")
else:
    print("    - [PASS] 100% of internal references match defined labels.")

# 4. High-Similarity & Repetitive Template Analysis
print(f"\n[4] SIMILARITY & TEMPLATE CLICHE SCAN:")
# Find sentences with "et al." patterns
et_al_sentences = [s.strip() for s in tex.split('.') if 'et al' in s]
print(f"    - 'et al.' sentences in paper: {len(et_al_sentences)}")
for i, s in enumerate(et_al_sentences[:5], 1):
    cleaned = re.sub(r'\s+', ' ', s).strip()
    print(f"      {i}. {cleaned[:80]}...")

# Scan for formulaic academic openers
cliches = [
    "increasingly depends on",
    "far exceeds what human operators",
    "The rest of the paper is organized",
    "Several observations merit discussion",
    "widely used in",
    "demonstrates strong detection capability",
]
found_cliches = []
for c in cliches:
    count = len(re.findall(re.escape(c), tex, re.IGNORECASE))
    if count > 0:
        found_cliches.append((c, count))

if found_cliches:
    print(f"    - [FLAG] Formulaic phrasing instances detected:")
    for c, cnt in found_cliches:
        print(f"      * \"{c}\" (count: {cnt})")
else:
    print("    - [PASS] No standard formulaic openers detected.")

print("\n" + "=" * 60)
print("AUDIT EXECUTION COMPLETE")
print("=" * 60)
