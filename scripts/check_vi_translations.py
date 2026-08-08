#!/usr/bin/env python3
"""Validate Vietnamese translations against their English source files.

The checker compares syntax-sensitive structures that translators should not
alter: source metadata, headings, code blocks, inline code, math delimiters,
link destinations, Jinja expressions, HTML structure, MkDocs tabs, and
admonitions. For translation files changed by the current commit/PR, every
LaTeX expression must also be preserved exactly with the same multiplicity.
Human-readable HTML attributes such as alt text may be translated.
"""

from __future__ import annotations

import collections
import re
import subprocess
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
FENCE_RE = re.compile(r"^\s*(```+|~~~+)([^\n]*)$")
LINK_TARGET_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
JINJA_RE = re.compile(r"(?:\{%.*?%\}|\{\{.*?\}\})", re.DOTALL)
HTML_TAG_RE = re.compile(
    r"</?[A-Za-z][A-Za-z0-9:-]*(?:\s+[^<>]*?)?\s*/?>"
)
TRANSLATABLE_HTML_ATTR_RE = re.compile(
    r"(\s(?:alt|title|aria-label)\s*=\s*)([\"'])(.*?)\2",
    re.IGNORECASE,
)
TAB_RE = re.compile(r"^(\s*)===\s+.+$", re.MULTILINE)
ADMONITION_RE = re.compile(r"^\s*(?:!!!|\?\?\?)\s+([\w-]+)", re.MULTILINE)
TRANSLATOR_NOTE_LINE_RE = re.compile(r"^\*\*Ghi chú bản dịch:\*\*.*$", re.MULTILINE)
BLOCK_MATH_DELIM_RE = re.compile(r"(?<!\\)\$\$")
MATH_RE = re.compile(
    r"(?:\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)(?<!\$)\$(?!\$).*?(?<!\\)\$(?!\$))",
    re.DOTALL,
)


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
        match = FENCE_RE.match(line)
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


def strip_fenced_blocks(text: str) -> str:
    """Remove fenced blocks before checking inline-only Markdown syntax."""
    output: list[str] = []
    current_marker: str | None = None

    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if current_marker is None:
            if match:
                current_marker = match.group(1)[0:3]
                output.append("")
            else:
                output.append(line)
            continue

        output.append("")
        if re.match(rf"^\s*{re.escape(current_marker)}+\s*$", line):
            current_marker = None

    return "\n".join(output)


def normalize_metadata(metadata: str) -> str:
    """Normalize insignificant trailing whitespace while keeping key order strict."""
    lines = [line.rstrip() for line in metadata.strip().splitlines()]
    return "\n".join(lines)


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


def format_counter(counter_value: collections.Counter[str]) -> str:
    """Format a small Counter deterministically for actionable validator errors."""
    if not counter_value:
        return "none"
    parts: list[str] = []
    for value, count in sorted(counter_value.items(), key=lambda item: repr(item[0])):
        suffix = f" x{count}" if count != 1 else ""
        parts.append(f"{value!r}{suffix}")
    return ", ".join(parts)


def counter_difference(expected: collections.Counter[str], actual: collections.Counter[str]) -> str:
    """Describe missing and unexpected values without changing validation semantics."""
    missing = expected - actual
    extra = actual - expected
    return f"missing: {format_counter(missing)}; extra: {format_counter(extra)}"


def token_line_number_map(pattern: re.Pattern[str], text: str) -> dict[str, list[int]]:
    """Index exact regex matches by token with 1-based line numbers in one scan."""
    locations: dict[str, list[int]] = collections.defaultdict(list)
    for match in pattern.finditer(text):
        locations[match.group(0)].append(text.count("\n", 0, match.start()) + 1)
    return dict(locations)


def math_mismatch_locations(source_text: str, translated_text: str, source_math: collections.Counter[str], translated_math: collections.Counter[str]) -> str:
    """Show locations for mismatched math tokens without changing validation semantics."""
    tokens = sorted(set((source_math - translated_math).keys()) | set((translated_math - source_math).keys()))
    source_locations = token_line_number_map(MATH_RE, source_text)
    translated_locations = token_line_number_map(MATH_RE, translated_text)
    parts: list[str] = []
    for token in tokens:
        parts.append(
            f"{token!r}: source lines {source_locations.get(token, [])}, "
            f"translation lines {translated_locations.get(token, [])}"
        )
    return "; ".join(parts)


def changed_translation_paths() -> set[Path]:
    """Return .vi.md files touched by the current PR/commit plus local changes.

    GitHub pull_request workflows check out a synthetic merge commit. With
    fetch-depth 2, diffing HEAD^1..HEAD yields every translation changed by the
    PR while avoiding legacy mismatches in untouched translations.
    """
    changed: set[Path] = set()
    commands = [
        ["git", "diff", "--name-only", "HEAD^1", "HEAD", "--", "src"],
        ["git", "diff", "--name-only", "HEAD", "--", "src"],
        ["git", "diff", "--cached", "--name-only", "--", "src"],
    ]
    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            if line.endswith(".vi.md"):
                changed.add((ROOT / line).resolve())
    return changed


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


def validate_pair(
    source: Document,
    translated: Document,
    errors: list[str],
    *,
    exact_math: bool,
) -> None:
    source_metadata = normalize_metadata(source.metadata)
    translated_source_metadata = normalize_metadata(
        strip_translation_metadata(translated.metadata)
    )
    if source_metadata != translated_source_metadata:
        add_error(
            errors,
            translated.path,
            "source front matter must match exactly, excluding the translation block",
        )

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

    source_without_fences = strip_fenced_blocks(source.body)
    translated_without_fences = strip_fenced_blocks(translated.body)
    source_inline = counter(INLINE_CODE_RE, source_without_fences)
    translated_inline = counter(INLINE_CODE_RE, translated_without_fences)
    if source_inline != translated_inline:
        add_error(
            errors,
            translated.path,
            f"inline code differs from source ({counter_difference(source_inline, translated_inline)})",
        )

    source_block_math_delimiters = len(BLOCK_MATH_DELIM_RE.findall(source.body))
    translated_block_math_delimiters = len(BLOCK_MATH_DELIM_RE.findall(translated.body))
    if source_block_math_delimiters != translated_block_math_delimiters:
        add_error(errors, translated.path, "number of $$ math delimiters differs from source")
    if source_block_math_delimiters % 2 != 0 or translated_block_math_delimiters % 2 != 0:
        add_error(errors, translated.path, "unbalanced $$ math delimiters")

    if exact_math:
        source_math_text = INLINE_CODE_RE.sub("", source_without_fences)
        translated_math_text = INLINE_CODE_RE.sub(
            "", TRANSLATOR_NOTE_LINE_RE.sub("", translated_without_fences)
        )
        source_math = collections.Counter(sequence(MATH_RE, source_math_text))
        translated_math = collections.Counter(sequence(MATH_RE, translated_math_text))
        if source_math != translated_math:
            add_error(
                errors,
                translated.path,
                "LaTeX expressions differ from source "
                f"({counter_difference(source_math, translated_math)}; "
                f"locations: {math_mismatch_locations(source_math_text, translated_math_text, source_math, translated_math)})",
            )

    source_targets = counter(LINK_TARGET_RE, source.body) + counter(REFERENCE_LINK_RE, source.body)
    translated_targets = counter(LINK_TARGET_RE, translated.body) + counter(
        REFERENCE_LINK_RE, translated.body
    )
    if source_targets != translated_targets:
        add_error(
            errors,
            translated.path,
            f"Markdown link/image destinations differ from source ({counter_difference(source_targets, translated_targets)})",
        )

    source_jinja = counter(JINJA_RE, source.body)
    translated_jinja = counter(JINJA_RE, translated.body)
    if source_jinja != translated_jinja:
        add_error(
            errors,
            translated.path,
            f"Jinja/MkDocs expressions differ from source ({counter_difference(source_jinja, translated_jinja)})",
        )

    source_html = html_structure(source_without_fences)
    translated_html = html_structure(translated_without_fences)
    if source_html != translated_html:
        add_error(
            errors,
            translated.path,
            f"HTML structure or non-translatable attributes differ ({counter_difference(source_html, translated_html)})",
        )

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

    exact_math_paths = changed_translation_paths()
    if exact_math_paths:
        paths = ", ".join(
            str(path.relative_to(ROOT)) for path in sorted(exact_math_paths)
        )
        print(f"Exact LaTeX validation enabled for changed translation(s): {paths}")

    for translated_path in translated_paths:
        translated = load_document(translated_path)
        source_path = validate_metadata(translated, errors)
        if source_path is None:
            continue
        source = load_document(source_path)
        validate_pair(
            source,
            translated,
            errors,
            exact_math=translated_path.resolve() in exact_math_paths,
        )

    if errors:
        print("Vietnamese translation validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(translated_paths)} Vietnamese translation file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())