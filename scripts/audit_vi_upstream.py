#!/usr/bin/env python3
"""Read-only, pinned-ref inventory. Fetch refs before running; no network/writes.

Print JSON to stdout. Compare recorded source blobs, fork sources and upstream
sources separately. A matching blob proves freshness, not translation quality.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, encoding="utf-8", errors="strict"
    ).strip()


def tree(ref: str) -> dict[str, str]:
    entries = {}
    for line in git("ls-tree", "-r", ref, "--", "src").splitlines():
        info, path = line.split("\t", 1)
        _, kind, sha = info.split()
        if kind == "blob":
            entries[path] = sha
    return entries


def audit(translation_ref: str, upstream_ref: str) -> dict:
    local_sha = git("rev-parse", "--verify", f"{translation_ref}^{{commit}}")
    upstream_sha = git("rev-parse", "--verify", f"{upstream_ref}^{{commit}}")
    local, upstream = tree(local_sha), tree(upstream_sha)
    rows = []
    for path in sorted(p for p in local if p.endswith(".vi.md")):
        text = git("cat-file", "blob", local[path])
        front = re.match(r"\A---\s*\n(.*?)\n---", text, re.S)
        fields = dict(re.findall(
            r"^  (source|source_commit|status|last_synced):\s*(\S+)\s*$",
            front.group(1) if front else "", re.M,
        ))
        if set(fields) != {"source", "source_commit", "status", "last_synced"}:
            raise ValueError(f"Missing translation metadata: {path}")
        source = "src/" + fields["source"]
        if source not in local:
            raise ValueError(f"Missing fork source: {source}")
        recorded = fields["source_commit"]
        if not re.fullmatch(r"[0-9a-f]{40}", recorded):
            raise ValueError(f"Expected full source blob SHA: {path}")
        if git("cat-file", "-t", recorded) != "blob":
            raise ValueError(f"Recorded source is not a blob: {path}")
        target = upstream.get(source)
        delta = git("diff", "--numstat", recorded, target) if target else ""
        rows.append({
            "translation": path, "source": source,
            "status": fields["status"], "last_synced": fields["last_synced"],
            "recorded_blob": recorded, "fork_blob": local[source],
            "upstream_blob": target,
            "fork_matches_recorded": local[source] == recorded,
            "upstream_matches_recorded": target == recorded,
            "source_delta_numstat": delta,
        })
    # Scope is English Markdown under article directories, excluding root pages.
    article_dirs = {
        "algebra", "combinatorics", "data_structures", "dynamic_programming",
        "geometry", "graph", "linear_algebra", "num_methods", "others",
        "schedules", "sequences", "string", "game_theory",
    }
    translated = {r["source"] for r in rows}
    untranslated = sorted(p for p in upstream if p.endswith(".md")
                          and not p.endswith(".vi.md")
                          and p.split("/")[1] in article_dirs
                          and p not in translated)
    return {
        "translation_ref": translation_ref, "translation_commit": local_sha,
        "upstream_ref": upstream_ref, "upstream_commit": upstream_sha,
        "summary": {
            "translations": len(rows),
            "status_counts": dict(collections.Counter(r["status"] for r in rows)),
            "stale_against_fork": sum(not r["fork_matches_recorded"] for r in rows),
            "stale_against_upstream": sum(not r["upstream_matches_recorded"] for r in rows),
            "untranslated_article_files": len(untranslated),
        },
        "translations": rows, "untranslated": untranslated,
        "limits": "Committed refs only; fetch first. Does not assess meaning, review approval or working-tree edits.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--translation-ref", default="origin/master")
    parser.add_argument("--upstream-ref", default="upstream/main")
    args = parser.parse_args()
    try:
        report = audit(args.translation_ref, args.upstream_ref)
    except (subprocess.CalledProcessError, ValueError) as exc:
        parser.exit(2, f"Audit failed; verify refs, full history and metadata: {exc}\n")
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
