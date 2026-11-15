#!/usr/bin/env python3
"""Fail CI when a Vietnamese translation is not synced with its source blob."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from check_vi_translations import (
    FRONT_MATTER_RE,
    SOURCE_COMMIT_RE,
    SOURCE_RE,
    STATUS_RE,
    VALID_STATUSES,
)

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src"


def git_blob_sha(path: Path) -> str:
    # Hash the working file with Git's clean filters (including CRLF -> LF).
    # Reading HEAD would incorrectly hide uncommitted source edits.
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "hash-object", f"--path={relative}", "--", relative],
        cwd=ROOT,
        text=True,
    ).strip()


def main() -> int:
    failures: list[str] = []
    for translated in sorted(DOCS.rglob("*.vi.md")):
        path = translated.relative_to(ROOT)
        front = FRONT_MATTER_RE.match(translated.read_text(encoding="utf-8"))
        metadata = front.group(1) if front else ""

        source_match = SOURCE_RE.search(metadata)
        commit_match = SOURCE_COMMIT_RE.search(metadata)
        status_match = STATUS_RE.search(metadata)
        if (
            not source_match or not commit_match or not status_match
            or status_match.group(1) not in VALID_STATUSES
        ):
            failures.append(f"{path} needs a source path, a 40-digit source blob SHA and a valid status.")
            continue

        relative = Path(source_match.group(1))
        if relative.is_absolute() or ".." in relative.parts:
            failures.append(f"{path} must name a source relative to src/.")
            continue
        source = DOCS / relative
        if not source.is_file():
            failures.append(f"{path} names a missing source: src/{relative}.")
            continue
        expected = commit_match.group(1)
        current = git_blob_sha(source)
        status = status_match.group(1)

        if current != expected and status != "stale":
            failures.append(
                f"{path} is out of date: "
                f"source blob is {current}, metadata records {expected}. "
                "Update the translation or set status: stale."
            )
        elif current == expected and status == "stale":
            failures.append(
                f"{path} is marked stale although its source blob matches."
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
