
# Final pdf_batch_cleaner.py
# 
# Features:
# - Folder variable for PDF location
# - Cleaned text extraction
# - 4 Spell check engines: pyspellchecker, JamSpell, SymSpell, BERT
# - Auto JamSpell model downloader (en.bin)
# - Per-PDF and total execution timing
# - Whitelist support
# - Metadata in final report

import argparse, datetime, json, re, sys, time, urllib.request
from collections import Counter
from pathlib import Path
from difflib import SequenceMatcher
from PyPDF2 import PdfReader

# --------------------------------------------------------------------#
PDF_DIR = Path("~path/to/files").expanduser()  # Change to your PDF folder
JAMSPELL_MODEL = Path("en.bin")
JAMSPELL_URL = "https://github.com/bakwc/JamSpell-models/raw/master/en.bin"
# --------------------------------------------------------------------#

# Try optional spell checker back-ends
try:
    from spellchecker import SpellChecker as _PySpell
except ImportError:
    _PySpell = None

try:
    import jamspell
except ImportError:
    jamspell = None

try:
    from symspellpy import SymSpell, Verbosity
except ImportError:
    SymSpell = None

try:
    from transformers import pipeline
except ImportError:
    pipeline = None

# Whitelist & Config
SIM_THRESHOLD = 0.85
WHITELIST: set[str] = {

    # --- Domains, platforms, protocols ---
    "http", "https", "www", "amazonaws", "vimeo", "youtube", "zoom",
    "ebook", "pdf", "mp3", "mp4", "json", "cli", "api",

    # --- Spell-check library names ---
    "jamspell", "symspell", "bertspell", "pyspellchecker",

    # --- Metaphysical platforms & concepts ---
    "imm", "uom", "uos", "sedona", "metaphysics", "metaphysical", "metaphysician",
    "consciousness", "higher-consciousness", "god-mind", "universal-mind", "affirmative",

    # --- Common errors from reports ---
    "chakra", "chakras", "yantra", "mantra", "meditators", "beingness", "unmanifest",

    # --- Religious and esoteric terms ---
    "kundalini", "samadhi", "aum", "om", "esp", "thought-forms",
    "self-realization", "self-hypnosis", "autosuggestion", "biofeedback",
    "auric", "pranic", "kirlian", "holistic", "oneness", "light-body",

    # --- Ceremony and UoS-specific context terms ---
    "minister", "ministry", "ordination", "baptism", "eulogy",
    "consecration", "reverend", "rite", "celebration", "unity", "divine",

    # --- Curriculum/degree structure ---
    "bmsc", "mmsc", "phd", "psyphd", "mba", "mba.m", "d.phil", "study-guide", "study-modules",

    # --- Spiritual & metaphysical figures (canonical lowercase) ---
    "masters", "yogananda", "vivekananda", "paramahansa", "jung", "freud", "einstein",
    "gibran", "chevreul", "quimby", "silva", "blavatsky", "baker", "eddy", "fillmore",
    "mystics", "swami", "deepak", "chopra", "maharishi", "ike", "erhard",

    # --- Capitalized forms (title casing) ---
    "IMM", "UOM", "UOS", "Sedona", "Metaphysics", "Metaphysical", "Metaphysician",
    "Consciousness", "Higher-Consciousness", "God-Mind", "Universal-Mind", "Affirmative",
    "Self-Realization", "Self-Hypnosis", "Autosuggestion", "Visualization", "Christ",
    "Christ-Consciousness", "Thought-Forms", "Light-Body", "Oneness",

    # --- Roman numerals ---
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",

    # --- Technical and misc terms (capitalized) ---
    "PDF", "JSON", "CLI", "API", "Vimeo", "YouTube", "eBook",

    # --- Educational acronyms and punctuation variants ---
    "e.g.", "i.e.", "etc.", "vs.", "PhD", "MBA", "PsyD",

    # --- Location and university affiliations ---
    "Arizona", "California", "Los", "Angeles", "University", "of", "Milwaukee",

    # --- Expanded ceremonial phrasing from UoS documents ---
    "Ceremony", "Minister", "Unity", "Harmony", "Divine", "Life", "Universe",

}

# Download JamSpell model if missing
def ensure_jamspell_model():
    if not JAMSPELL_MODEL.exists():
        print("[INFO] Downloading JamSpell model...")
        urllib.request.urlretrieve(JAMSPELL_URL, str(JAMSPELL_MODEL))

# PDF text extraction
def pdf_to_raw_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    return '\\n'.join(page.extract_text() or '' for page in reader.pages)

# Cleaning rules
HYPHEN_BREAK = re.compile(r"([A-Za-z])-?\\n([a-z])")
MULTI_SPACE   = re.compile(r" {2,}")
LINE_END_HARD = re.compile(r"\\s*\\n\\s*")

def clean_text(raw: str) -> tuple[str, dict]:
    fixes = Counter()
    txt = HYPHEN_BREAK.sub(lambda m: m.group(1) + m.group(2), raw)
    if txt != raw: fixes['hyphen_join'] += 1
    txt2 = MULTI_SPACE.sub(' ', txt)
    if txt2 != txt: fixes['multispace'] += 1
    txt3 = LINE_END_HARD.sub(' ', txt2)
    if txt3 != txt2: fixes['linebreak_merge'] += 1
    return txt3, dict(fixes)

# Spell Engine
class SpellEngine:
    def __init__(self, backend: str = 'pyspell', lang: str = 'en'):
        self.backend = backend.lower()
        self.lang = lang

        if self.backend == 'pyspell' and _PySpell:
            self.engine = _PySpell(language=lang)
        elif self.backend == 'jamspell' and jamspell:
            ensure_jamspell_model()
            self.engine = jamspell.TSpellCorrector()
            self.engine.LoadLangModel(str(JAMSPELL_MODEL))
        elif self.backend == 'symspell' and SymSpell:
            self.engine = SymSpell(max_dictionary_edit_distance=2)
            self.engine.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)
        elif self.backend == 'bert' and pipeline:
            self.engine = pipeline('fill-mask', model='bert-base-uncased')
        else:
            print(f"[WARN] Missing backend '{backend}', defaulting to pyspell.")
            self.backend = 'pyspell'
            self.engine = _PySpell(language=lang) if _PySpell else None

    def _similar(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def correct(self, text: str) -> tuple[str, dict]:
        if self.backend == 'pyspell':
            return self._correct_pyspell(text)
        elif self.backend == 'jamspell':
            return self._correct_jamspell(text)
        elif self.backend == 'symspell':
            return self._correct_symspell(text)
        elif self.backend == 'bert':
            return self._correct_bert(text)
        return text, {}

    def _correct_pyspell(self, text):
        words = re.findall(r"[A-Za-z']+", text)
        sp = self.engine
        miss = sp.unknown(words)
        changes = {}
        for w in miss:
            if w.lower() in WHITELIST: 
                continue
            sugg = sp.correction(w)
            if sugg and self._similar(w, sugg) >= SIM_THRESHOLD:
                changes[w] = sugg
        for w, s in changes.items():
            text = re.sub(rf"\\b{re.escape(w)}\\b", s, text)
        return text, changes

    def _correct_jamspell(self, text):
        sentences = text.split('. ')
        new_sent, changes = [], {}
        for sent in sentences:
            fixed = self.engine.FixFragment(sent)
            new_sent.append(fixed)
            for a, b in zip(sent.split(), fixed.split()):
                if a != b and a.lower() not in WHITELIST:
                    changes[a] = b
        return '. '.join(new_sent), changes

    def _correct_symspell(self, text):
        changes = {}
        for t in text.split():
            if t.lower() in WHITELIST or not t.isalpha(): 
                continue
            suggs = self.engine.lookup(t, Verbosity.CLOSEST, max_edit_distance=2)
            if suggs:
                best = suggs[0].term
                if best != t and self._similar(t, best) >= SIM_THRESHOLD:
                    changes[t] = best
        for w, s in changes.items():
            text = re.sub(rf"\\b{re.escape(w)}\\b", s, text)
        return text, changes

    def _correct_bert(self, text):
        tokens, changes = text.split(), {}
        for i, tok in enumerate(tokens):
            if tok.lower() in WHITELIST or not tok.isalpha(): 
                continue
            masked = tokens[:i] + ['[MASK]'] + tokens[i+1:]
            pred = self.engine(" ".join(masked[i-4:i+5]))[0]['token_str'].strip()
            if pred.lower() != tok.lower() and self._similar(tok, pred) >= SIM_THRESHOLD:
                changes[tok] = pred
                tokens[i] = pred
        return " ".join(tokens), changes

# PDF processor
def process_pdf(pdf_path: Path, engine: SpellEngine) -> dict:
    start = time.time()
    raw = pdf_to_raw_text(pdf_path)
    cleaned, fix_stats = clean_text(raw)
    cleaned, corrections = engine.correct(cleaned)
    out_path = pdf_path.with_suffix('.txt')
    out_path.write_text(cleaned, encoding='utf-8')
    elapsed = time.time() - start
    return {
        'pdf': pdf_path.name,
        'chars_original': len(raw),
        'chars_cleaned': len(cleaned),
        'cleaning_fixes': fix_stats,
        'spelling_corrections': len(corrections),
        'corrections_detail': corrections,
        'elapsed_seconds': round(elapsed, 2)
    }

# Main run
def run(folder: Path, lang='en', backend='pyspell'):
    print(f"[INFO] Using spell checker: {backend}")
    engine = SpellEngine(backend, lang)
    report, total_start = [], time.time()

    for pdf in folder.glob("*.pdf"):
        try:
            result = process_pdf(pdf, engine)
            print(f"✓ {pdf.name} ({result['spelling_corrections']} corrections, {result['elapsed_seconds']}s)")
            report.append(result)
        except Exception as e:
            print(f"✗ {pdf.name}: {e}")
            report.append({'pdf': pdf.name, 'error': str(e)})

    total_time = round(time.time() - total_start, 2)
    metadata = {
        'spell_checker': backend,
        'language': lang,
        'whitelist_size': len(WHITELIST),
        'total_elapsed_seconds': total_time,
        'report_generated': datetime.datetime.now().isoformat()
    }
    report.insert(0, metadata)

    out_path = folder / f"batch_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"[DONE] Report saved to: {out_path}")
    return out_path

# CLI
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--folder', default=str(PDF_DIR))
    p.add_argument('--lang', default='en')
    p.add_argument('--spell', default='pyspell', choices=['pyspell', 'jamspell', 'symspell', 'bert'])
    args = p.parse_args()

    run(Path(args.folder).expanduser().resolve(), lang=args.lang, backend=args.spell)