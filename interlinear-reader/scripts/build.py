#!/usr/bin/env python3
"""Build a click-to-reveal interlinear reader from a JSON data file.

Usage: python3 build.py data.json out.html

- Validates every token and every sentence translation before writing.
- If out.html already exists, the reading progress stored inside it is kept.
"""
import html
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "reader.html"
PROGRESS_RE = re.compile(r'(<script type="application/json" id="progress">)([\s\S]*?)(</script>)')
SENT_END = re.compile(r"[.?!]$")
NUMBERING = re.compile(r"^\d+\.$")
EMPTY_GLOSSES = {"", "–", "-", "—", "?"}


def tokens(text):
    for tok in text.split():
        i = tok.find("/")
        if i < 0:
            yield tok, None, None
        else:
            yield tok, tok[:i].replace("~", " "), tok[i + 1:].replace("_", " ")


def walk(data):
    """Yield (kind, key, payload) exactly like the template's render()."""
    seen = {}

    def key(kind, a, b):
        base = f"{kind}|{a}|{b}"
        seen[base] = seen.get(base, 0) + 1
        return f"{base}|{seen[base]}"

    for s in data["sections"]:
        for b in s["blocks"]:
            sents = b.get("sentences") if b["type"] == "p" else None
            si = 0
            for tok, src, gl in tokens(b["text"]):
                if src is None:
                    continue
                yield "w", key("w", src, gl), (src, gl)
                if sents and SENT_END.search(src) and not NUMBERING.match(src) and si < len(sents):
                    yield "s", key("s", sents[si], ""), sents[si]
                    si += 1


def validate(data):
    errors, warnings = [], []
    for s in data["sections"]:
        for b in s["blocks"]:
            where = f"[{s.get('label', '')}] {b['text'][:40]}…"
            if b["type"] not in ("h", "p"):
                errors.append(f"{where}: type must be 'h' or 'p'")
            for tok, src, gl in tokens(b["text"]):
                if src is None:
                    if re.search(r"\w", tok):
                        errors.append(f"{where}: token without gloss: {tok!r}")
                    continue
                if not src.strip():
                    errors.append(f"{where}: empty source in {tok!r}")
                if gl.strip() in EMPTY_GLOSSES:
                    warnings.append(f"{where}: meaningless gloss in {tok!r} – merge it into a chunk")
            if b["type"] == "p":
                ends = sum(1 for _, src, _ in tokens(b["text"])
                           if src and SENT_END.search(src) and not NUMBERING.match(src))
                n = len(b.get("sentences", []))
                if n != ends:
                    errors.append(f"{where}: {ends} sentence ends but {n} sentence translations")
    return errors, warnings


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    data_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    data = json.loads(data_path.read_text(encoding="utf-8"))

    errors, warnings = validate(data)
    for w in warnings:
        print("WARN ", w)
    if errors:
        for e in errors:
            print("ERROR", e)
        sys.exit(1)

    items = list(walk(data))
    word_keys = [k for kind, k, _ in items if kind == "w"]

    progress = {"words": [], "sents": []}
    # Optional one-time seed from an older position-based log: [[wordIndex, epochMillis], ...]
    for idx, t in (data.get("legacy") or {}).get("seed", []):
        progress["words"].append({"k": word_keys[idx], "t": t})
    if out_path.exists():
        m = PROGRESS_RE.search(out_path.read_text(encoding="utf-8"))
        if m:
            try:
                old = json.loads(m.group(2))
                for part in ("words", "sents"):
                    known = {e["k"] for e in progress[part]}
                    progress[part] += [e for e in old.get(part, []) if e["k"] not in known]
                if old.get("resetAt"):
                    progress["resetAt"] = old["resetAt"]
            except (json.JSONDecodeError, KeyError, TypeError):
                pass

    data_out = dict(data)
    if "legacy" in data_out:
        data_out["legacy"] = {k: v for k, v in data["legacy"].items() if k != "seed"}

    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("__LANG__", html.escape(data.get("lang", "es")), 1)
    page = page.replace("__TITLE__", html.escape(data["title"]), 1)
    page = page.replace("__PROGRESS__", json.dumps(progress, ensure_ascii=False).replace("<", "\\u003c"), 1)
    page = page.replace("__DATA__", json.dumps(data_out, ensure_ascii=False, indent=1).replace("</", "<\\/"), 1)
    out_path.write_text(page, encoding="utf-8")

    n_s = sum(1 for kind, _, _ in items if kind == "s")
    print(f"OK {out_path}: {len(word_keys)} words, {n_s} sentences, "
          f"{len(progress['words'])} words already revealed")


if __name__ == "__main__":
    main()
