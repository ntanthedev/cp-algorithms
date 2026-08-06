#!/usr/bin/env python3
"""Fail CI when a Vietnamese translation is not synced with its source blob."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src"
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SOURCE_RE = re.compile(r"^\s{2}source:\s*(\S+)\s*$", re.MULTILINE)
SOURCE_COMMIT_RE = re.compile(r"^\s{2}source_commit:\s*([0-9a-f]{40})\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^\s{2}status:\s*([a-z-]+)\s*$", re.MULTILINE)


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    failures: list[str] = []
    for translated in sorted(DOCS.rglob("*.vi.md")):
        text = translated.read_text(encoding="utf-8")
        front = FRONT_MATTER_RE.match(text)
        if not front:
            continue
        metadata = front.group(1)
        source_match = SOURCE_RE.search(metadata)
        commit_match = SOURCE_COMMIT_RE.search(metadata)
        status_match = STATUS_RE.search(metadata)
        if not source_match or not commit_match or not status_match:
            continue

        source = DOCS / source_match.group(1)
        if not source.is_file():
            continue
        expected = commit_match.group(1)
        current = git_blob_sha(source)
        status = status_match.group(1)

        if current != expected and status != "stale":
            failures.append(
                f"{translated.relative_to(ROOT)} is out of date: "
                f"source blob is {current}, metadata records {expected}. "
                "Update the translation or set status: stale."
            )
        elif current == expected and status == "stale":
            failures.append(
                f"{translated.relative_to(ROOT)} is marked stale although its source blob matches."
            )

    if failures:
        print("Translation synchronization check failed:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("All Vietnamese translation source hashes are synchronized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
