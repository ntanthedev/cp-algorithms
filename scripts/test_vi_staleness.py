"""Regression tests for Git blob normalization and source metadata validation."""
import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "staleness", Path(__file__).with_name("check_vi_staleness.py")
)
staleness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(staleness)


class StalenessHashTests(unittest.TestCase):
    def test_clean_filters_and_uncommitted_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "core.autocrlf", "true"], check=True)
            source = root / "source.md"
            source.write_bytes(b"# Example\r\nText.\r\n")
            subprocess.run(["git", "-C", str(root), "add", "source.md"], check=True)
            expected = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", ":source.md"], text=True
            ).strip()
            previous_root = staleness.ROOT
            try:
                staleness.ROOT = root
                self.assertEqual(staleness.git_blob_sha(source), expected)
                source.write_bytes(b"# Example\nText.\n")
                self.assertEqual(staleness.git_blob_sha(source), expected)
                source.write_bytes(b"# Example\r\nChanged meaning.\r\n")
                self.assertNotEqual(staleness.git_blob_sha(source), expected)
            finally:
                staleness.ROOT = previous_root

    def test_short_blob_fails_sync_instead_of_skipping_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "src"
            docs.mkdir()
            (docs / "source.md").write_text("# Source\n", encoding="utf-8")
            (docs / "source.vi.md").write_text(
                "---\ntranslation:\n  source: source.md\n"
                "  source_commit: abcdef0\n  status: draft\n---\n# Translation\n",
                encoding="utf-8",
            )
            output = io.StringIO()
            with patch.multiple(staleness, ROOT=root, DOCS=docs), contextlib.redirect_stdout(output):
                self.assertEqual(staleness.main(), 1)
            self.assertIn("40-digit source blob SHA", output.getvalue())


if __name__ == "__main__":
    unittest.main()
