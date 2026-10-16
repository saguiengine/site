"""build.py: the base address of each build (E9).

A deployment's own address (CF_PAGES_URL) changes on every deploy; links,
feed ids and old bookmarks need the project's fixed address on main and the
branch's alias on previews.

Run: python3 -m unittest discover -s scripts -p "test_*.py"
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import build  # noqa: E402

DOMAIN = "https://domain.example"


def cloudflare(deployment, branch, **more):
    return {"CF_PAGES_URL": deployment, "CF_PAGES_BRANCH": branch, **more}


class Address(unittest.TestCase):
    def test_outside_cloudflare_the_address_of_identity_toml(self):
        self.assertEqual(build.address({}, DOMAIN), DOMAIN)

    def test_main_uses_the_projects_fixed_address(self):
        env = cloudflare("https://abc123.projeto.pages.dev", "main")
        self.assertEqual(build.address(env, DOMAIN), "https://projeto.pages.dev")

    def test_two_deploys_of_main_give_the_same_address(self):
        first = build.address(cloudflare("https://abc123.projeto.pages.dev", "main"), DOMAIN)
        second = build.address(cloudflare("https://9f8e7d6c.projeto.pages.dev", "main"), DOMAIN)
        self.assertEqual(first, second)

    def test_main_with_the_domain_live_uses_the_domain(self):
        env = cloudflare("https://abc123.projeto.pages.dev", "main", DOMAIN_LIVE="1")
        self.assertEqual(build.address(env, DOMAIN), DOMAIN)

    def test_a_preview_uses_its_branch_alias(self):
        env = cloudflare("https://def456.projeto.pages.dev", "e9/Post_etapa-0")
        self.assertEqual(build.address(env, DOMAIN), "https://e9-post-etapa-0.projeto.pages.dev")

    def test_a_preview_ignores_domain_live(self):
        env = cloudflare("https://def456.projeto.pages.dev", "fix/api", DOMAIN_LIVE="1")
        self.assertEqual(build.address(env, DOMAIN), "https://fix-api.projeto.pages.dev")


class Indexing(unittest.TestCase):
    """E9.4 (D383): only the live domain is indexed."""

    def test_only_main_with_the_domain_live_is_indexed(self):
        self.assertFalse(build.indexed(
            cloudflare("https://abc123.projeto.pages.dev", "main"), DOMAIN))
        self.assertFalse(build.indexed(
            cloudflare("https://def456.projeto.pages.dev", "x"), DOMAIN))
        self.assertFalse(build.indexed(
            cloudflare("https://def456.projeto.pages.dev", "x", DOMAIN_LIVE="1"), DOMAIN))
        self.assertTrue(build.indexed(
            cloudflare("https://abc123.projeto.pages.dev", "main", DOMAIN_LIVE="1"), DOMAIN))

    def test_headers_keep_pages_dev_out_once_the_domain_is_live(self):
        self.assertIn("/*\n  X-Robots-Tag: noindex", build.headers(False))
        live = build.headers(True)
        self.assertIn("https://:project.pages.dev/*\n  X-Robots-Tag: noindex", live)
        self.assertNotIn("\n/*", live)


if __name__ == "__main__":
    unittest.main()
