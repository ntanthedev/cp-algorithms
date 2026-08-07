#!/usr/bin/env python3
"""Validate local image references in the rendered Vietnamese site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "public"
VI_SITE = SITE / "vi"


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        values = dict(attrs)
        src = values.get("src")
        if src:
            self.sources.append(src)


def is_external_or_embedded(src: str) -> bool:
    parsed = urlsplit(src)
    return bool(
        parsed.scheme
        or parsed.netloc
        or src.startswith(("//", "data:", "#"))
    )


def resolve_local_asset(page: Path, src: str) -> Path:
    parsed = urlsplit(src)
    asset_path = Path(unquote(parsed.path))
    if parsed.path.startswith("/"):
        return SITE / parsed.path.lstrip("/")
    return (page.parent / asset_path).resolve()


def main() -> int:
    if not VI_SITE.is_dir():
        print("Rendered Vietnamese site not found; run mkdocs build first.")
        return 1

    errors: list[str] = []
    checked = 0

    for page in sorted(VI_SITE.rglob("*.html")):
        parser = ImageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for src in parser.sources:
            if is_external_or_embedded(src):
                continue
            checked += 1
            target = resolve_local_asset(page, src)
            try:
                target.relative_to(SITE.resolve())
            except ValueError:
                errors.append(
                    f"{page.relative_to(SITE)}: image escapes site root: {src}"
                )
                continue
            if not target.is_file():
                errors.append(
                    f"{page.relative_to(SITE)}: missing local image {src} "
                    f"(resolved to {target.relative_to(SITE.resolve())})"
                )

    if errors:
        print("Rendered Vietnamese image validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {checked} local image reference(s) under public/vi/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
