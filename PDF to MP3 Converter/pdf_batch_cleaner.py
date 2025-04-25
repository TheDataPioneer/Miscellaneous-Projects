import argparse, json, re, datetime
from pathlib import Path
from collections import Counter

from PyPDF2 import PdfReader
from spellchecker import SpellChecker

# -------------------------------------------------
# >>> CHANGE THIS to the directory that holds PDFs
PDF_FOLDER = Path("~path/to/files").expanduser()   # ← edit me
# -------------------------------------------------

# ---------- Helpers -----------------
def pdf_to_raw_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or '' for page in reader.pages]
    return '\n'.join(pages)

# Simple heuristics for common artefacts
HYPHEN_BREAK = re.compile(r"([A-Za-z])-\n([a-z])")  # broken words split by newline
MULTI_SPACE   = re.compile(r" {2,}")
LINE_END_HARD = re.compile(r"\s*\n\s+")             # merge single hard line-breaks

def clean_text(raw: str) -> tuple[str, dict]:
    fixes = Counter()

    txt = HYPHEN_BREAK.sub(lambda m: m.group(1) + m.group(2), raw)
    if txt != raw:
        fixes['hyphen_join'] += 1

    txt2 = MULTI_SPACE.sub(' ', txt)
    if txt2 != txt:
        fixes['multispace'] += 1

    txt3 = LINE_END_HARD.sub(' ', txt2)
    if txt3 != txt2:
        fixes['linebreak_merge'] += 1

    return txt3, dict(fixes)

def spellcheck(text: str, language='en') -> tuple[str, dict]:
    words = re.findall(r"[A-Za-z']+", text)
    sp = SpellChecker(language=language)
    miss = sp.unknown(words)

    corrections = {}
    for word in miss:
        suggestion = sp.correction(word)
        if suggestion and suggestion.lower() != word.lower():
            corrections[word] = suggestion

    # apply corrections (very simple global replace)
    for wrong, right in corrections.items():
        text = re.sub(rf"\b{re.escape(wrong)}\b", right, text)

    return text, corrections

# ---------- Main workflow ----------
def process_pdf(pdf_path: Path, lang='en') -> dict:
    raw = pdf_to_raw_text(pdf_path)
    cleaned, fix_stats = clean_text(raw)
    cleaned, corrections = spellcheck(cleaned, lang)

    txt_path = pdf_path.with_suffix('.txt')
    txt_path.write_text(cleaned, encoding='utf-8')

    return {
        'pdf': pdf_path.name,
        'chars_original': len(raw),
        'chars_cleaned': len(cleaned),
        'cleaning_fixes': fix_stats,
        'spelling_corrections': len(corrections),
        'corrections_detail': corrections
    }

def run(folder: Path, lang='en') -> Path:
    report = []
    for pdf in folder.glob('*.pdf'):
        try:
            report.append(process_pdf(pdf, lang))
            print(f"✓ Processed {pdf.name}")
        except Exception as e:
            print(f"✗ Failed {pdf.name}: {e}")
            report.append({'pdf': pdf.name, 'error': str(e)})

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = folder / f"batch_report_{ts}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"\nSummary JSON saved to {report_path}")
    return report_path

# ---------- CLI ----------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Batch-convert PDFs to cleaned TXT and spell-check them.')
    parser.add_argument('folder', nargs='?', default=PDF_FOLDER,
                        help='Folder containing PDFs (default = value of PDF_FOLDER var)')
    parser.add_argument('--lang', default='en',
                        help='Language for spell-check (default=en)')
    cli = parser.parse_args()
    run(Path(cli.folder).expanduser().resolve(), cli.lang)
