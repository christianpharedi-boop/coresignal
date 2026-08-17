#!/usr/bin/env python3
"""Reject CJK and other disallowed script characters in repository content."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

TEXT_EXTENSIONS = {
    ".py", ".md", ".mdx", ".txt", ".rst", ".tex", ".bib", ".cff",
    ".yaml", ".yml", ".json", ".toml", ".csv", ".ipynb", ".svg",
    ".xml", ".html", ".css", ".js", ".ts",
}
BINARY_EXTENSIONS = {".pdf", ".eps", ".png", ".jpg", ".jpeg", ".webp"}
IGNORED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "node_modules", "dist", "build",
}

DISALLOWED_RANGES = [
    (0x1100, 0x11FF, "Hangul Jamo"),
    (0x2E80, 0x2EFF, "CJK Radicals Supplement"),
    (0x2F00, 0x2FDF, "Kangxi Radicals"),
    (0x3000, 0x303F, "CJK Symbols and Punctuation"),
    (0x3040, 0x309F, "Hiragana"),
    (0x30A0, 0x30FF, "Katakana"),
    (0x3100, 0x312F, "Bopomofo"),
    (0x3130, 0x318F, "Hangul Compatibility Jamo"),
    (0x31A0, 0x31BF, "Bopomofo Extended"),
    (0x31C0, 0x31EF, "CJK Strokes"),
    (0x31F0, 0x31FF, "Katakana Phonetic Extensions"),
    (0x3200, 0x32FF, "Enclosed CJK Letters and Months"),
    (0x3300, 0x33FF, "CJK Compatibility"),
    (0x3400, 0x4DBF, "CJK Unified Ideographs Extension A"),
    (0x4E00, 0x9FFF, "CJK Unified Ideographs"),
    (0xA960, 0xA97F, "Hangul Jamo Extended-A"),
    (0xAC00, 0xD7AF, "Hangul Syllables"),
    (0xD7B0, 0xD7FF, "Hangul Jamo Extended-B"),
    (0xF900, 0xFAFF, "CJK Compatibility Ideographs"),
    (0xFE30, 0xFE4F, "CJK Compatibility Forms"),
    (0xFF00, 0xFFEF, "Halfwidth and Fullwidth Forms"),
    (0x20000, 0x2FA1F, "CJK Unified Ideographs Extensions"),
]

def blocked(ch: str):
    cp = ord(ch)
    for lo, hi, name in DISALLOWED_RANGES:
        if lo <= cp <= hi:
            return name
    return None

def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file() or any(part in IGNORED_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in TEXT_EXTENSIONS | BINARY_EXTENSIONS:
            yield p

def read_candidate(path: Path):
    if path.suffix.lower() == ".ipynb":
        return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None

def scan_text(path: Path, text: str):
    findings = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for col_no, ch in enumerate(line, 1):
            script = blocked(ch)
            if script:
                findings.append((path, line_no, col_no, ch, f"U+{ord(ch):04X}", script))
    return findings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    root = Path(parser.parse_args().root).resolve()

    findings = []
    scanned = 0
    skipped_binary = 0

    for path in iter_files(root):
        text = read_candidate(path)
        if text is None:
            skipped_binary += 1
            continue
        scanned += 1
        findings.extend(scan_text(path, text))

    if findings:
        print("ERROR: English-only character policy violation(s) detected.")
        for path, line, col, ch, codepoint, script in findings:
            print(f"{path.relative_to(root)}:{line}:{col}: {script} {codepoint} {ch!r}")
        return 1

    print(f"English-only character policy passed. Scanned textual files: {scanned}.")
    if skipped_binary:
        print(f"Note: {skipped_binary} binary file(s) were not decoded as text.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
