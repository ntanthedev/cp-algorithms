"""Translated copies must never replace the English snippets under test."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class ExtractSnippetsTest(unittest.TestCase):
    def test_english_is_the_only_source(self):
        script = Path(__file__).with_name("extract_snippets.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src"
            tests = root / "test"
            source.mkdir()
            tests.mkdir()
            (source / "example.md").write_text(
                "```{.cpp file=example}\nint answer = 42;\n```\n", encoding="utf-8"
            )
            (source / "example.vi.md").write_text(
                "# Bản dịch cũ\n```{.cpp file=example}\nint answer = -1;\n```\n",
                encoding="utf-8",
            )
            subprocess.run([sys.executable, str(script)], cwd=tests, check=True)
            self.assertEqual((tests / "example.h").read_text(), "int answer = 42;\n")


if __name__ == "__main__":
    unittest.main()
