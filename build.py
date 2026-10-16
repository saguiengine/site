"""Builds the site with its address from identity.toml (D379).

Cloudflare Pages runs `python3 build.py` (Zola comes from ZOLA_VERSION), the
CI does the same, and locally `python build.py` works with Zola on the PATH
or in ZOLA. Extra arguments go to `zola build` (`-o DIR -f` builds into DIR).

The address never depends on the deployment, which changes on every deploy:
- main uses the project's fixed address (https://<project>.pages.dev), until
  the domain is connected and DOMAIN_LIVE=1 is set in Pages; then the
  address from identity.toml;
- previews (any other branch) use their branch's alias
  (https://<branch>.<project>.pages.dev), which follows the branch;
- outside Cloudflare, the address from identity.toml.

Search engines (D383): only the live domain is indexed. The provisional
address and the previews get noindex, in every page (base.html, when the
address is not the domain) and in the _headers this script writes.

After Zola, the English 404 page moves to en/404.html: Cloudflare Pages
serves the 404.html nearest to the missing path.
"""

import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent

# A DNS label holds at most 63 characters.
MAX_LABEL = 63


def project_host(deployment):
    """`<project>.pages.dev` from a deployment's `<hash>.<project>.pages.dev`."""
    host = urlparse(deployment).hostname or ""
    labels = host.split(".")
    if len(labels) >= 4 and labels[-2:] == ["pages", "dev"]:
        return ".".join(labels[1:])
    return host


def branch_alias(branch):
    """Cloudflare's alias of a branch: lowercase, with a hyphen for every
    character that is not a letter or a digit."""
    return re.sub(r"[^a-z0-9]", "-", branch.lower())


def address(env, identity_url):
    """The base URL for this build."""
    deployment = env.get("CF_PAGES_URL")
    if not deployment:
        return identity_url
    branch = env.get("CF_PAGES_BRANCH", "")
    if branch == "main":
        if env.get("DOMAIN_LIVE") == "1":
            return identity_url
        return f"https://{project_host(deployment)}"
    alias = branch_alias(branch)
    if not alias or len(alias) > MAX_LABEL:
        return deployment
    return f"https://{alias}.{project_host(deployment)}"


def indexed(env, identity_url):
    """D383: search engines index only the site at its own address."""
    return address(env, identity_url) == identity_url


def headers(is_indexed):
    """The _headers file of Cloudflare Pages (D383)."""
    if is_indexed:
        return ("# D383: the domain is indexed; its copy on *.pages.dev is not.\n"
                "https://:project.pages.dev/*\n"
                "  X-Robots-Tag: noindex\n")
    return ("# D383: the provisional address and the previews are not indexed.\n"
            "/*\n"
            "  X-Robots-Tag: noindex\n")


def output_dir(args):
    for i, arg in enumerate(args):
        if arg in ("-o", "--output-dir") and i + 1 < len(args):
            return ROOT / args[i + 1]
    return ROOT / "public"


def move_english_404(out):
    """en/404/index.html becomes en/404.html, out of the sitemap."""
    page = out / "en" / "404" / "index.html"
    if not page.exists():
        return
    shutil.move(page, out / "en" / "404.html")
    shutil.rmtree(out / "en" / "404")
    sitemap = out / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        text = re.sub(r"\s*<url>\s*<loc>[^<]*/en/404/</loc>.*?</url>", "", text, flags=re.S)
        sitemap.write_text(text, encoding="utf-8")


def main():
    with open(ROOT / "identity.toml", "rb") as f:
        identity_url = tomllib.load(f)["site"]["url"]
    url = address(os.environ, identity_url)
    args = sys.argv[1:]
    zola = os.environ.get("ZOLA", "zola")
    print(f"build.py: zola build --base-url {url}", flush=True)
    code = subprocess.call([zola, "build", "--base-url", url, *args], cwd=ROOT)
    if code != 0:
        return code
    out = output_dir(args)
    (out / "_headers").write_text(headers(indexed(os.environ, identity_url)), encoding="utf-8")
    move_english_404(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
