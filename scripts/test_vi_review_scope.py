"""Regression: exact-math scope covers a whole multi-commit PR and new files."""
import subprocess
import tempfile
import unittest
from pathlib import Path

import check_vi_translations as checker


class ReviewScopeTests(unittest.TestCase):
    def test_multiple_commits_and_untracked_translation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(
                    ["git", "-C", str(root), *args], text=True,
                    stderr=subprocess.DEVNULL,
                ).strip()

            def commit():
                git("add", ".")
                git("-c", "user.name=Test", "-c", "user.email=test@example.com",
                    "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")

            git("init", "-q")
            (root / "src").mkdir()
            (root / "src/source.md").write_text("# Example\n", encoding="utf-8")
            commit()
            base = git("rev-parse", "HEAD")
            for name in ("first", "second"):
                (root / f"src/{name}.vi.md").write_text("# Draft\n", encoding="utf-8")
                commit()
            (root / "src/untracked.vi.md").write_text("# Draft\n", encoding="utf-8")
            previous_root = checker.ROOT
            try:
                checker.ROOT = root
                self.assertEqual(checker.changed_translation_paths(base), {
                    (root / f"src/{name}.vi.md").resolve()
                    for name in ("first", "second", "untracked")
                })
                with self.assertRaises(ValueError):
                    checker.changed_translation_paths("refs/heads/missing")
            finally:
                checker.ROOT = previous_root


if __name__ == "__main__":
    unittest.main()
