"""Regression: CRLF checkouts must match Git blobs without hiding source edits."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
