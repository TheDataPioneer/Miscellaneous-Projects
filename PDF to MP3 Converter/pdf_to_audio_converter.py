import argparse, json, re, datetime, asyncio
from pathlib import Path
from collections import Counter

from PyPDF2 import PdfReader
from spellchecker import SpellChecker
import edge_tts  # for natural-sounding voice

# ---------- Configurable Defaults ----------
PDF_FOLDER = Path("~path/to/files").expanduser()  # update this default path
DEFAULT_VOICE = "en-US-GuyNeural"
# ------------------------------------------

# ---------- Text Processing Utilities ----------
def pdf_to_raw_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or '' for page in reader.pages]
    return '\\n'.join(pages)

HYPHEN_BREAK = re.compile(r"([A-Za-z])-\\n([a-z])")
MULTI_SPACE   = re.compile(r" {2,}")
LINE_END_HARD = re.compile(r"\\s*\\n\\s+")

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
    for wrong, right in corrections.items():
        text = re.sub(rf"\\b{re.escape(wrong)}\\b", right, text)
    return text, corrections

# ---------- Main Workflow ----------
async def text_to_mp3(text_path: Path, voice: str):
    mp3_path = text_path.with_suffix('.mp3')
    text = text_path.read_text(encoding='utf-8')
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(mp3_path))
    print(f"🎧 Saved {mp3_path.name}")

async def process_pdf(pdf_path: Path, lang='en', voice=DEFAULT_VOICE) -> dict:
    raw = pdf_to_raw_text(pdf_path)
    cleaned, fix_stats = clean_text(raw)
    cleaned, corrections = spellcheck(cleaned, lang)

    txt_path = pdf_path.with_suffix('.txt')
    txt_path.write_text(cleaned, encoding='utf-8')

    await text_to_mp3(txt_path, voice)

    return {
        'pdf': pdf_path.name,
        'chars_original': len(raw),
        'chars_cleaned': len(cleaned),
        'cleaning_fixes': fix_stats,
        'spelling_corrections': len(corrections),
        'corrections_detail': corrections
    }

async def run(folder: Path, lang='en', voice=DEFAULT_VOICE):
    report = []
    for pdf in folder.glob('*.pdf'):
        try:
            result = await process_pdf(pdf, lang, voice)
            report.append(result)
            print(f"✓ Processed {pdf.name}")
        except Exception as e:
            print(f"✗ Failed {pdf.name}: {e}")
            report.append({'pdf': pdf.name, 'error': str(e)})
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = folder / f"batch_audio_report_{ts}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"\\n📄 Report saved to {report_path}")
    return report_path

# ---------- CLI ----------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PDF → Cleaned TXT + Natural Audio (MP3)')
    parser.add_argument('folder', nargs='?', default=PDF_FOLDER, help='Folder containing PDFs')
    parser.add_argument('--lang', default='en', help='Language for spell-check (default=en)')
    parser.add_argument('--voice', default=DEFAULT_VOICE, help='Microsoft Edge TTS voice name (e.g., en-US-GuyNeural)')
    args = parser.parse_args()

    asyncio.run(run(Path(args.folder).expanduser().resolve(), args.lang, args.voice))