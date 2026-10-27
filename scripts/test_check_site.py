"""check_site.py: every devlog post is marked in the roadmap (D401).

Run: python3 -m unittest discover -s scripts -p "test_*.py"
"""

import tempfile
import unittest
from pathlib import Path

import check_site

ROADMAP = """
[[stage]]
pt = "Etapa 1: base"
en = "Stage 1: foundation"
state = "done"
post = "etapa-1"

[[stage]]
pt = "Etapa 2: peças e fases"
en = "Stage 2: pieces and levels"
state = "now"

[[stage.delivery]]
pt = "5 · o formato das fases"
en = "5 · the level format"
count = 1
state = "done"
post = "formato"

[[stage.delivery]]
pt = "9 · o editor abre o projeto"
en = "9 · the editor opens the project"
count = 1
state = "next"
"""


def post(extra):
    return f'+++\ntitle = "Um post"\ndate = 2026-10-20\n\n[extra]\n{extra}\n+++\n\nTexto.\n'


class PostsInRoadmap(unittest.TestCase):
    def check(self, posts):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data" / "roadmap.toml").write_text(ROADMAP, encoding="utf-8")
            for name, extra in posts.items():
                folder = root / "content" / "devlog" / name
                folder.mkdir(parents=True)
                (folder / "index.md").write_text(post(extra), encoding="utf-8")
            return check_site.check_posts_in_roadmap(root)

    def test_marked_posts_pass(self):
        self.assertEqual(self.check({
            "formato": 'delivery_stage = "2"\ndeliveries = [5]',
            "etapa-1": 'stage = "1"',
            "outro": 'thumbnail = "x.png"',
        }), [])

    def test_a_delivery_post_that_the_roadmap_does_not_mark_fails(self):
        problems = self.check({"editor": 'delivery_stage = "2"\ndeliveries = [9]'})
        self.assertEqual(len(problems), 1)
        self.assertIn("editor tells deliveries [9] of stage 2", problems[0])

    def test_a_milestone_post_of_a_stage_not_done_fails(self):
        problems = self.check({"etapa-2": 'stage = "2"'})
        self.assertEqual(len(problems), 1)
        self.assertIn("etapa-2 is the milestone post of stage 2", problems[0])


if __name__ == "__main__":
    unittest.main()
