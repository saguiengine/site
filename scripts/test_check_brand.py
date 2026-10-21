"""check_brand.py: the post about the name is the only text that may write
the brand (approved on 21/10/2026).

Run: python3 -m unittest discover -s scripts -p "test_*.py"
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_brand  # noqa: E402

IDENTITY = {"brand": {"engine_name": "Marmota"}, "site": {"url": "https://marmota.example"}}
POST = "content/devlog/o-nome-e-a-marca"


class NamePost(unittest.TestCase):
    """The exception covers the post's two files and nothing else."""

    def written(self, files):
        """What check_written finds in a repository with these files."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            for path in files:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text("Marmota\n", encoding="utf-8")
            return check_written_paths(check_brand.check_written(IDENTITY, root))

    def test_the_posts_two_files_may_write_the_brand(self):
        self.assertEqual(self.written([f"{POST}/index.md", f"{POST}/index.en.md"]), set())

    def test_another_post_with_the_same_file_name_may_not(self):
        other = ["content/devlog/etapa-0/index.md", "content/devlog/etapa-0/index.en.md"]
        self.assertEqual(self.written([f"{POST}/index.md", *other]), set(other))

    def test_another_file_beside_the_post_may_not(self):
        beside = f"{POST}/outro.md"
        self.assertEqual(self.written([f"{POST}/index.md", beside]), {beside})

    def test_a_template_may_not(self):
        self.assertEqual(self.written(["templates/base.html"]), {"templates/base.html"})

    def test_the_e9_2_copy_leaves_out_only_the_post(self):
        paths = [f"{POST}/index.md", f"{POST}/index.en.md", f"{POST}/nome-cena.png",
                 "content/devlog/etapa-0/index.md", "identity.toml"]
        self.assertEqual(check_brand.e9_2_files(paths),
                         [f"{POST}/nome-cena.png", "content/devlog/etapa-0/index.md",
                          "identity.toml"])


def check_written_paths(findings):
    """The files of check_written's findings ("path:line: contains ...")."""
    return {finding.split(":", 1)[0] for finding in findings}


if __name__ == "__main__":
    unittest.main()
