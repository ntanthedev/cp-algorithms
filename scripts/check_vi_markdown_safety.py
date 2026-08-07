#!/usr/bin/env python3
"""Check Vietnamese-only Markdown patterns that are easy to render incorrectly."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src"
VI_PATTERN = "*.vi.md"
INDENTED_NOTE_RE = re.compile(r"^[ \t]+\*\*Ghi chú bản dịch:\*\*", re.MULTILINE)


def main() -> int:
    errors: list[str] = []

    for path in sorted(DOCS.rglob(VI_PATTERN)):
        text = path.read_text(encoding="utf-8")
        for match in INDENTED_NOTE_RE.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"{path.relative_to(ROOT)}:{line}: translation notes must start at "
                "column 1; place the note after the complete source list instead of "
                "indenting it between list items"
            )

    if errors:
        print("Vietnamese Markdown safety validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Vietnamese Markdown safety checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
