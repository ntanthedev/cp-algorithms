#!/usr/bin/env python3
"""Validate Vietnamese translations against their English source files.

The checker compares syntax-sensitive structures that translators should not
alter: source metadata, headings, code blocks, inline code, math delimiters,
link destinations, Jinja expressions, HTML structure, MkDocs tabs, and
admonitions. Human-readable HTML attributes such as alt text may be translated.
"""

from __future__ import annotations

import collections
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src"
VI_PATTERN = "*.vi.md"
VALID_STATUSES = {
    "draft",
    "technical-reviewed",
    "language-reviewed",
    "ready",
    "stale",
}

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SOURCE_RE = re.compile(r"^\s{2}source:\s*(\S+)\s*$", re.MULTILINE)
SOURCE_COMMIT_RE = re.compile(r"^\s{2}source_commit:\s*([0-9a-f]{7,40})\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^\s{2}status:\s*([a-z-]+)\s*$", re.MULTILINE)
LAST_SYNCED_RE = re.compile(r"^\s{2}last_synced:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
LINK_TARGET_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
JINJA_RE = re.compile(r"(?:\{%.*?%\}|\{\{.*?\}\})", re.DOTALL)
HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")
TRANSLATABLE_HTML_ATTR_RE = re.compile(
    r"(\s(?:alt|title|aria-label)\s*=\s*)([\"'])(.*?)\2",
    re.IGNORECASE,
)
TAB_RE = re.compile(r"^(\s*)===\s+.+$", re.MULTILINE)
ADMONITION_RE = re.compile(r"^\s*(?:!!!|\?\?\?)\s+([\w-]+)", re.MULTILINE)


@dataclass
class Document:
    path: Path
    text: str
    body: str
    metadata: str


def load_document(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if match:
        return Document(path, text, text[match.end() :], match.group(1))
    return Document(path, text, text, "")


def extract_fenced_blocks(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines()
    signatures: list[str] = []
    bodies: list[str] = []
    current_marker: str | None = None
    current_signature = ""
    current_lines: list[str] = []

    for line in lines:
        match = re.match(r"^\s*(```+|~~~+)([^\n]*)$", line)
        if current_marker is None:
            if match:
                current_marker = match.group(1)[0:3]
                current_signature = match.group(2).strip()
                current_lines = []
            continue

        if re.match(rf"^\s*{re.escape(current_marker)}+\s*$", line):
            signatures.append(current_signature)
            bodies.append("\n".join(current_lines).rstrip())
            current_marker = None
            current_signature = ""
            current_lines = []
        else:
            current_lines.append(line)

    if current_marker is not None:
        raise ValueError("unclosed fenced code block")
    return signatures, bodies


def strip_translation_metadata(metadata: str) -> str:
    """Remove the top-level translation block while preserving source metadata."""
    lines = metadata.splitlines()
    kept: list[str] = []
    skipping = False

    for line in lines:
        if not skipping and re.fullmatch(r"translation:\s*", line):
            skipping = True
            continue
        if skipping:
            if line.startswith((" ", "\t")) or not line.strip():
                continue
            skipping = False
        kept.append(line.rstrip())

    while kept and not kept[-1]:
        kept.pop()
    return "\n".join(kept).strip()


def normalize_html_tag(tag: str) -> str:
    """Allow translation of human-readable attributes, but preserve structure."""
    return TRANSLATABLE_HTML_ATTR_RE.sub(
        lambda match: (
            f"{match.group(1)}{match.group(2)}"
            f"<translated>{match.group(2)}"
        ),
        tag,
    )


def html_structure(text: str) -> collections.Counter[str]:
    return collections.Counter(normalize_html_tag(tag) for tag in HTML_TAG_RE.findall(text))


def counter(pattern: re.Pattern[str], text: str) -> collections.Counter[str]:
    return collections.Counter(pattern.findall(text))


def sequence(pattern: re.Pattern[str], text: str) -> list[str]:
    return pattern.findall(text)


def add_error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def validate_metadata(doc: Document, errors: list[str]) -> Path | None:
    if not doc.metadata:
        add_error(errors, doc.path, "missing YAML front matter")
        return None
    if "translation:" not in doc.metadata:
        add_error(errors, doc.path, "missing translation metadata")
        return None

    source_match = SOURCE_RE.search(doc.metadata)
    commit_match = SOURCE_COMMIT_RE.search(doc.metadata)
    status_match = STATUS_RE.search(doc.metadata)
    synced_match = LAST_SYNCED_RE.search(doc.metadata)

    if not source_match:
        add_error(errors, doc.path, "missing translation.source")
        return None
    if not commit_match:
        add_error(errors, doc.path, "missing or invalid translation.source_commit")
    if not status_match:
        add_error(errors, doc.path, "missing translation.status")
    elif status_match.group(1) not in VALID_STATUSES:
        add_error(errors, doc.path, f"invalid translation.status: {status_match.group(1)}")
    if not synced_match:
        add_error(errors, doc.path, "missing or invalid translation.last_synced")

    source_rel = Path(source_match.group(1))
    if source_rel.is_absolute() or ".." in source_rel.parts:
        add_error(errors, doc.path, "translation.source must be relative to src/")
        return None
    source_path = DOCS / source_rel
    if not source_path.is_file():
        add_error(errors, doc.path, f"source file does not exist: src/{source_rel}")
        return None
    return source_path


def validate_pair(source: Document, translated: Document, errors: list[str]) -> None:
    source_metadata = source.metadata.strip()
    translated_source_metadata = strip_translation_metadata(translated.metadata)
    if source_metadata != translated_source_metadata:
        add_error(errors, translated.path, "source front matter differs from translation")

    source_headings = sequence(HEADING_RE, source.body)
    translated_headings = sequence(HEADING_RE, translated.body)
    if source_headings != translated_headings:
        add_error(errors, translated.path, "heading-level sequence differs from source")

    try:
        source_languages, source_blocks = extract_fenced_blocks(source.body)
        translated_languages, translated_blocks = extract_fenced_blocks(translated.body)
    except ValueError as exc:
        add_error(errors, translated.path, str(exc))
        return

    if source_languages != translated_languages:
        add_error(errors, translated.path, "code-fence languages/order differ from source")
    if source_blocks != translated_blocks:
        add_error(errors, translated.path, "content inside fenced code blocks differs from source")

    if counter(INLINE_CODE_RE, source.body) != counter(INLINE_CODE_RE, translated.body):
        add_error(errors, translated.path, "inline code differs from source")

    if source.body.count("$$") != translated.body.count("$$"):
        add_error(errors, translated.path, "number of $$ math delimiters differs from source")
    if source.body.count("$$") % 2 != 0 or translated.body.count("$$") % 2 != 0:
        add_error(errors, translated.path, "unbalanced $$ math delimiters")

    source_targets = counter(LINK_TARGET_RE, source.body) + counter(REFERENCE_LINK_RE, source.body)
    translated_targets = counter(LINK_TARGET_RE, translated.body) + counter(
        REFERENCE_LINK_RE, translated.body
    )
    if source_targets != translated_targets:
        add_error(errors, translated.path, "Markdown link/image destinations differ from source")

    if counter(JINJA_RE, source.body) != counter(JINJA_RE, translated.body):
        add_error(errors, translated.path, "Jinja/MkDocs expressions differ from source")

    if html_structure(source.body) != html_structure(translated.body):
        add_error(errors, translated.path, "HTML structure or non-translatable attributes differ")

    if sequence(TAB_RE, source.body) != sequence(TAB_RE, translated.body):
        add_error(errors, translated.path, "MkDocs tab sequence or indentation differs from source")

    if sequence(ADMONITION_RE, source.body) != sequence(ADMONITION_RE, translated.body):
        add_error(errors, translated.path, "MkDocs admonition sequence differs from source")


def main() -> int:
    errors: list[str] = []
    translated_paths = sorted(DOCS.rglob(VI_PATTERN))
    if not translated_paths:
        print("No Vietnamese translation files found.")
        return 0

    for translated_path in translated_paths:
        translated = load_document(translated_path)
        source_path = validate_metadata(translated, errors)
        if source_path is None:
            continue
        source = load_document(source_path)
        validate_pair(source, translated, errors)

    if errors:
        print("Vietnamese translation validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(translated_paths)} Vietnamese translation file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
