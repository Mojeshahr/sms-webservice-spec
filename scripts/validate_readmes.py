#!/usr/bin/env python3
"""Require a Persian first word on every README line containing Persian text.

Markdown/HTML formatting is ignored; prose, tables, diagrams and comments
are all checked. Purely Latin code and paths are unaffected.
"""

import html
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent


def visible_line(line):
    line = html.unescape(line)
    # An image's alt text is its accessible label, not its HTML attributes.
    line = re.sub(r'<img\b[^>]*\balt="([^"]*)"[^>]*>', r"\1", line)
    line = re.sub(r"<[^>]+>", "", line)
    line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
    return line


def persian_letter(char):
    return unicodedata.category(char).startswith("L") and "ARABIC" in unicodedata.name(char, "")


def check_readmes():
    errors = []
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name.lower().startswith("readme") and p.suffix.lower() == ".md" and ".git" not in p.parts)
    for path in files:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            text = visible_line(line)
            if not any(persian_letter(c) for c in text):
                continue
            first = next((c for c in text if c.isalnum()), "")
            if not persian_letter(first):
                errors.append(f"{path.relative_to(ROOT)}:{number}: Persian line must start with a Persian word: {line}")
    return files, errors


def main():
    files, errors = check_readmes()
    for error in errors:
        print(error)
    print(f"README Persian line starts: {len(files)} files, {len(errors)} violations")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
