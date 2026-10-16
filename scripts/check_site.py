"""Checks of the built site (E9), as Cloudflare Pages builds it.

Builds the site as a deploy of main, a second deploy of main, main with the
domain live and a preview, and checks:
- the address: feed ids the same across two deploys of main, previews on
  their branch alias, the domain only when it is live;
- E9.4: noindex (meta and header) on the provisional address and previews,
  none with the domain live, where only *.pages.dev keeps it; and no cookie
  nor analytics script anywhere (D383, D271);
- every image in a post links to itself, to open at full size;
- in English, an image of the interface still in Portuguese says so, in its
  alt text and in a caption under it (an image without text is listed in the
  page's extra.images_without_text; an English version has .en. in its name);
- no number written with a space between thousands ("5 000");
- the 404 page in both languages.

Run: python3 scripts/check_site.py (needs Zola on the PATH, or in ZOLA).
"""

import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOINDEX_META = '<meta name="robots" content="noindex">'

MAIN = {"CF_PAGES_URL": "https://abc123.projeto.pages.dev", "CF_PAGES_BRANCH": "main"}
MAIN_AGAIN = {"CF_PAGES_URL": "https://9f8e7d6c.projeto.pages.dev", "CF_PAGES_BRANCH": "main"}
LIVE = {**MAIN, "DOMAIN_LIVE": "1"}
PREVIEW = {"CF_PAGES_URL": "https://def456.projeto.pages.dev", "CF_PAGES_BRANCH": "e9/teste"}


def build(env, out):
    """`python build.py` with only these Cloudflare variables set."""
    clean = {k: v for k, v in os.environ.items()
             if not k.startswith("CF_PAGES") and k != "DOMAIN_LIVE"}
    done = subprocess.run([sys.executable, "build.py", "-o", str(out), "-f"],
                          cwd=ROOT, env={**clean, **env}, capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(f"check_site: build failed:\n{done.stdout}\n{done.stderr}")
    return out


def html_files(out):
    return sorted(out.rglob("*.html"))


def feed_ids(out):
    return re.findall(r"<id>(.*?)</id>", (out / "atom.xml").read_text(encoding="utf-8"))


def headers(out):
    path = out / "_headers"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check_address(main, main_again, live, preview, domain):
    problems = []
    ids, ids_again = feed_ids(main), feed_ids(main_again)
    if ids != ids_again:
        problems.append(f"address: the feed ids change between two deploys of main: {ids} != {ids_again}")
    for out, base, name in [(main, "https://projeto.pages.dev/", "main"),
                            (preview, "https://e9-teste.projeto.pages.dev/", "preview"),
                            (live, domain.rstrip("/") + "/", "main with the domain live")]:
        for value in feed_ids(out):
            if not value.startswith(base):
                problems.append(f"address: {name}: feed id {value} is not under {base}")
    return problems


def check_indexing(main, live, preview):
    problems = []
    for out, name in [(main, "main"), (preview, "preview")]:
        for page in html_files(out):
            if NOINDEX_META not in page.read_text(encoding="utf-8"):
                problems.append(f"E9.4: {name}: {page.relative_to(out)} has no noindex")
        if not re.search(r"^/\*\s*\n\s+X-Robots-Tag: noindex", headers(out), re.M):
            problems.append(f"E9.4: {name}: _headers does not send noindex for every page")
    for page in html_files(live):
        if NOINDEX_META in page.read_text(encoding="utf-8"):
            problems.append(f"E9.4: domain live: {page.relative_to(live)} has noindex")
    for out, name in [(main, "main"), (live, "domain live"), (preview, "preview")]:
        for page in html_files(out):
            if "<script" in page.read_text(encoding="utf-8").lower():
                problems.append(f"E9.4: {name}: {page.relative_to(out)} has a script")
        if "set-cookie" in headers(out).lower():
            problems.append(f"E9.4: {name}: _headers sets a cookie")
    live_headers = headers(live)
    if re.search(r"^/\*", live_headers, re.M):
        problems.append("E9.4: domain live: _headers sends noindex for every page")
    if not re.search(r"^https://:project\.pages\.dev/\*\s*\n\s+X-Robots-Tag: noindex",
                     live_headers, re.M):
        problems.append("E9.4: domain live: *.pages.dev is not kept out of search engines")
    return problems


def check_images(out):
    problems = []
    for page in html_files(out / "devlog") + html_files(out / "en" / "devlog"):
        text = page.read_text(encoding="utf-8")
        for src in re.findall(r'<img [^>]*src="([^"]+)"', text):
            linked = re.search(r'<a [^>]*href="[^"]*' + re.escape(Path(src).name)
                               + r'"[^>]*>\s*<img [^>]*src="' + re.escape(src) + '"', text)
            if not linked:
                problems.append(f"images: {page.relative_to(out)}: {src} does not open at full size")
    return problems


def check_image_language():
    problems = []
    for path in sorted((ROOT / "content").rglob("*.en.md")):
        text = path.read_text(encoding="utf-8")
        front = tomllib.loads(text.split("+++")[1]) if text.startswith("+++") else {}
        without_text = set(front.get("extra", {}).get("images_without_text", []))
        lines = text.splitlines()
        for number, line in enumerate(lines):
            for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)\s]+)\)", line):
                name = Path(src).name
                if ".en." in name or name in without_text:
                    continue
                caption = next((l for l in lines[number + 1:] if l.strip()), "")
                if "in Portuguese" not in alt or not (caption.startswith("*") and "in Portuguese" in caption):
                    problems.append(f"images: {path.relative_to(ROOT)}:{number + 1}: {name} is in "
                                    "Portuguese; say so in its alt text and in a caption under it")
    return problems


def check_numbers():
    problems = []
    for path in sorted((ROOT / "content").rglob("*.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\d[  ]\d{3}(?!\d)", line):
                problems.append(f"thousands: {path.relative_to(ROOT)}:{number}: a space between "
                                "thousands; use 5.000 in pt and 5,000 in en")
    return problems


def check_404(out):
    problems = []
    for path, lang, text in [(out / "404.html", 'lang="pt-BR"', "Página não encontrada"),
                             (out / "en" / "404.html", 'lang="en"', "Page not found")]:
        page = path.read_text(encoding="utf-8") if path.exists() else ""
        if lang not in page or text not in page:
            problems.append(f"404: {path.relative_to(out)} is not the {lang} page")
    return problems


def main():
    with open(ROOT / "identity.toml", "rb") as f:
        domain = tomllib.load(f)["site"]["url"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        main_out = build(MAIN, tmp / "main")
        main_again = build(MAIN_AGAIN, tmp / "main-again")
        live = build(LIVE, tmp / "live")
        preview = build(PREVIEW, tmp / "preview")
        problems = (check_address(main_out, main_again, live, preview, domain)
                    + check_indexing(main_out, live, preview)
                    + check_images(main_out)
                    + check_image_language()
                    + check_numbers()
                    + check_404(main_out))
        ids = feed_ids(main_out)
    for problem in problems:
        print(f"check_site: {problem}", file=sys.stderr)
    if problems:
        return 1
    print(f"check_site: address, E9.4, images, thousands and 404 pass; feed ids of main: {ids}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
