"""
web_to_text.py - saves the web sources listed in sources.json and converts them to plain text.

The text copies are much smaller than the PDFs and HTML they come from, so they
are what gets read back later for references. PDF text keeps a marker line at
every page break so citations can still give a page number:

  === page 14 ===

Layout (all next to this script):

  sources.json    one entry per source: id, title, author, url, kind (pdf|html), raw, used_for, notes
  raw/            the original files, as downloaded
  text/<id>.txt   plain text, with a short header naming the source
  text/INDEX.txt  one line per source: id, pages, size, title, url

Usage:  python web_to_text.py                  (download missing sources, rebuild all text)
        python web_to_text.py --refresh        (re-download sources that are already saved)
        python web_to_text.py --only nrel_gfm_roadmap sel_linam_ugfi

To add a source, append an entry to sources.json and rerun. Some sites
(selinc.com) block scripted downloads. For those, open the URL in a browser,
save the page as raw/<raw>, and rerun; the script converts whatever is in raw/.
A download that fails or returns a bot-check page never overwrites a saved copy.
"""

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import pymupdf
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "sources.json"
RAW = HERE / "raw"
TEXT = HERE / "text"

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
BOT_CHECK_MARKERS = (b"_Incapsula_Resource", b"cf-browser-verification", b"challenge-platform")
HTML_DROP_TAGS = ["script", "style", "noscript", "svg", "nav", "footer", "header", "aside", "form", "iframe"]

# Typographic characters -> ASCII, applied after NFKC normalization (which already
# splits ligatures like "fi" and turns non-breaking spaces into spaces). Keyed by
# code point so this file stays pure ASCII.
ASCII_MAP = {
    0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',            # curly quotes
    0x2010: "-", 0x2011: "-", 0x2012: "-", 0x2013: "-", 0x2014: "-", 0x2212: "-",  # dashes, minus
    0x2022: "-", 0x25CF: "-", 0x25AA: "-", 0x25B8: "-",            # bullets
    0x2026: "...", 0x200B: "", 0xFEFF: "",                          # ellipsis, zero-width, BOM
    0x00B0: " deg", 0x00B1: "+/-", 0x2264: "<=", 0x2265: ">=", 0x00D7: "x",
    0x03BC: "u", 0x03A9: " ohm", 0x2192: "->", 0x00AE: "(R)", 0x00A9: "(C)",
}
PRIVATE_USE = re.compile(f"[{chr(0xE000)}-{chr(0xF8FF)}]")    # e.g. Wingdings bullets in slide decks


def warn(msg):
    print("[!] " + msg)


def ok(msg):
    print("[OK] " + msg)


def fail(msg):
    print("[X] " + msg)


def download(src, refresh):
    """Fetch src['url'] into raw/. Returns (saved_copy_exists, status message)."""
    dest = RAW / src["raw"]
    if dest.exists() and not refresh:
        return True, "already saved"
    req = urllib.request.Request(src["url"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read()
    except (urllib.error.URLError, TimeoutError) as e:
        return dest.exists(), f"download failed ({e})"
    if src["kind"] == "pdf" and not body.startswith(b"%PDF"):
        return dest.exists(), "download was not a PDF (likely a bot-check page)"
    if src["kind"] == "html" and any(m in body for m in BOT_CHECK_MARKERS):
        return dest.exists(), "site returned a bot-check page"
    dest.write_bytes(body)
    return True, "downloaded"


def pdf_text(path):
    with pymupdf.open(path) as doc:
        pages = [f"=== page {i} ===\n{page.get_text()}" for i, page in enumerate(doc, 1)]
        return "\n".join(pages), doc.page_count


def json_text_fields(node, found):
    """Collect every string stored under a "text" key, depth first."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "text" and isinstance(value, str):
                found.append(value.strip())
            else:
                json_text_fields(value, found)
    elif isinstance(node, list):
        for value in node:
            json_text_fields(value, found)
    return found


def html_text(path):
    soup = BeautifulSoup(path.read_bytes(), "lxml")
    # Sites built on frameworks like Next.js keep tab and panel content in a JSON
    # <script> block and only render it in the browser (selinc.com does this).
    embedded = []
    for tag in soup.find_all("script", type="application/json"):
        try:
            json_text_fields(json.loads(tag.string or ""), embedded)
        except json.JSONDecodeError:
            pass
    for tag in soup(HTML_DROP_TAGS):
        tag.decompose()
    root = soup.find("main") or soup.find("article") or soup.body or soup
    visible = root.get_text("\n")
    flat = " ".join(visible.split())
    extra = []
    for s in embedded:
        s = " ".join(s.split())
        if len(s) > 1 and s not in flat and s not in extra:
            extra.append(s)
    if extra:
        visible += "\n\n=== embedded page data (content the page renders with script) ===\n" + "\n".join(extra)
    return visible, None


def clean(text):
    text = unicodedata.normalize("NFKC", text).translate(ASCII_MAP)
    text = PRIVATE_USE.sub("-", text)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def header(src, raw, pages):
    retrieved = datetime.fromtimestamp(raw.stat().st_mtime).strftime("%Y-%m-%d")
    rows = [
        ("SOURCE", src["title"]),
        ("AUTHOR", src.get("author", "")),
        ("URL", src["url"]),
        ("RAW FILE", f"raw/{src['raw']}"),
        ("RETRIEVED", retrieved),
        ("PAGES", pages if pages is not None else "n/a (web page)"),
        ("USED FOR", src.get("used_for", "")),
    ]
    return "\n".join(f"{k}: {v}" for k, v in rows) + "\n" + "-" * 72 + "\n\n"


def write_index(sources):
    lines = ["# id | pages | text KB | title | url"]
    for src in sources:
        out = TEXT / f"{src['id']}.txt"
        if not out.exists():
            lines.append(f"{src['id']} | MISSING | - | {src['title']} | {src['url']}")
            continue
        pages = re.search(r"^PAGES: (.*)$", out.read_text(encoding="utf-8"), re.M).group(1)
        lines.append(f"{src['id']} | {pages} | {out.stat().st_size / 1024:.0f} | {src['title']} | {src['url']}")
    (TEXT / "INDEX.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Save the web sources in sources.json and convert them to text.")
    ap.add_argument("--refresh", action="store_true", help="re-download sources that are already saved")
    ap.add_argument("--only", nargs="+", metavar="ID", help="process only these source ids")
    args = ap.parse_args()

    sources = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids = [s["id"] for s in sources]
    if len(ids) != len(set(ids)):
        fail("duplicate id in sources.json")
        return 1
    unknown = set(args.only or []) - set(ids)
    if unknown:
        fail(f"unknown id(s): {', '.join(sorted(unknown))}")
        return 1

    RAW.mkdir(exist_ok=True)
    TEXT.mkdir(exist_ok=True)
    missing = 0
    for src in sources:
        if args.only and src["id"] not in args.only:
            continue
        have_raw, status = download(src, args.refresh)
        raw = RAW / src["raw"]
        if not have_raw:
            fail(f"{src['id']}: {status}. Save {src['url']} from a browser as raw/{src['raw']}, then rerun.")
            missing += 1
            continue
        if status not in ("downloaded", "already saved"):
            warn(f"{src['id']}: {status}; converting the copy already saved")
        body, pages = pdf_text(raw) if src["kind"] == "pdf" else html_text(raw)
        out = TEXT / f"{src['id']}.txt"
        out.write_text(header(src, raw, pages) + clean(body), encoding="utf-8")
        ok(f"{src['id']}: {status}, {raw.stat().st_size / 1024:.0f} KB raw -> "
           f"{out.stat().st_size / 1024:.0f} KB text")

    write_index(sources)
    print(f"\nindex: {TEXT / 'INDEX.txt'}")
    if missing:
        print(f"{missing} source(s) still need a manual save")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
