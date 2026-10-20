"""Checks of the built site (E9), as Cloudflare Pages builds it.

Builds the site as a deploy of main, a second deploy of main, main with the
domain live and a preview, and checks:
- the address: feed ids the same across two deploys of main, previews on
  their branch alias, the domain only when it is live;
- E9.4: noindex (meta and header) on the provisional address and previews,
  none with the domain live, where only *.pages.dev keeps it; and no cookie
  nor analytics script anywhere (D383, D271);
- every image in a post opens at full size in a new tab, and its link tells
  screen readers so, in the page's language, with no script;
- in English, an image of the interface still in Portuguese says so, in its
  alt text and in its caption (D388; an image with no text carries
  data-no-text, an English version has .en. in its name);
- no number written with a space between thousands ("5 000");
- the 404 page in both languages;
- each page has its own description, the status line only on the home page,
  and a "&" in a description is escaped once;
- the footer's profiles and contact address stay out of the pages while
  they have `show = false`, and show up with `show = true`;
- a thumbnail on an English page is no image with text in Portuguese (D388).

Run: python3 scripts/check_site.py (needs Zola on the PATH, or in ZOLA).
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from urllib.parse import urlparse

from check_brand import tracked_files

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


# What the hidden text of an image link says, per language of the page.
NEW_TAB = {"pt": "(abre em nova aba)", "en": "(opens in a new tab)"}


def figures(text):
    """Each image of a page: its link and img tags, the link's text and the
    caption right after it."""
    found = []
    for img in re.finditer(r"<img [^>]*>", text):
        before = text[:img.start()]
        opening = before.rfind("<a ")
        closing = text.find("</a>", img.end())
        link = text[opening:text.find(">", opening) + 1] if opening >= 0 and "</a>" not in before[opening:] else ""
        inside = text[img.end():closing] if link and closing >= 0 else ""
        after = text[closing + 4:closing + 600] if link and closing >= 0 else ""
        caption = re.match(r"\s*<figcaption class=\"caption\">(.*?)</figcaption>", after, re.S)
        found.append({"img": img.group(0), "link": link, "inside": inside,
                      "caption": caption.group(1) if caption else ""})
    return found


def attribute(tag, name):
    match = re.search(name + r'="([^"]*)"', tag)
    return match.group(1) if match else None


def check_images(out):
    """Every image of a post opens at full size in a new tab, says so to
    screen readers in the page's language, and needs no script."""
    problems = []
    for lang, pages in [("pt", html_files(out / "devlog")), ("en", html_files(out / "en" / "devlog"))]:
        for page in pages:
            for figure in figures(page.read_text(encoding="utf-8")):
                src = attribute(figure["img"], "src") or ""
                link = figure["link"]
                where = f"images: {page.relative_to(out)}: {Path(src).name}"
                if not link or not (attribute(link, "href") or "").endswith(Path(src).name):
                    problems.append(f"{where} does not open at full size")
                    continue
                if attribute(link, "target") != "_blank" or "noopener" not in (attribute(link, "rel") or ""):
                    problems.append(f"{where} does not open in a new tab (target and rel)")
                if NEW_TAB[lang] not in figure["inside"]:
                    problems.append(f"{where}: the link does not tell screen readers {NEW_TAB[lang]}")
    return problems


def check_image_language(out):
    """In English, an image of the interface still in Portuguese says so in
    its alt text and in its caption (D388). An English version has .en. in
    its name; an image with no text carries data-no-text."""
    problems = []
    for page in html_files(out / "en" / "devlog"):
        for figure in figures(page.read_text(encoding="utf-8")):
            img = figure["img"]
            name = Path(attribute(img, "src") or "").name
            if ".en." in name or "data-no-text" in img:
                continue
            if "in Portuguese" not in (attribute(img, "alt") or "") or "in Portuguese" not in figure["caption"]:
                problems.append(f"images: {page.relative_to(out)}: {name} is in Portuguese; say so "
                                "in its alt text and in its caption (D388)")
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


DESCRIPTION = re.compile(r'<meta name="description" content="([^"]*)">')


def statuses():
    """The status line of the home page, in each language (zola.toml)."""
    with open(ROOT / "zola.toml", "rb") as f:
        config = tomllib.load(f)
    return {"pt": config["translations"]["status"],
            "en": config["languages"]["en"]["translations"]["status"]}


def check_descriptions(out):
    """Each page describes itself, and only the home page by the status line.
    The 404 pages are left out: nobody links to them or shares them."""
    problems = []
    status = statuses()
    homes = {"index.html": status["pt"], "en/index.html": status["en"]}
    seen = {}
    for page in html_files(out):
        name = page.relative_to(out).as_posix()
        if name.endswith("404.html"):
            continue
        text = page.read_text(encoding="utf-8")
        if "&amp;amp;" in text:
            problems.append(f"description: {name}: a \"&\" escaped twice (&amp;amp;)")
        found = DESCRIPTION.findall(text)
        if len(found) != 1 or not found[0].strip():
            problems.append(f"description: {name} has {len(found)} descriptions, not one with text")
            continue
        description = found[0]
        if name in homes and description != homes[name]:
            problems.append(f"description: {name} is not the status line `{homes[name]}`")
        if name not in homes and description in status.values():
            problems.append(f"description: {name} uses the status line, which is only for the home page")
        if description in seen:
            problems.append(f"description: {name} has the same description as {seen[description]}")
        seen.setdefault(description, name)
    return problems


def footer_links():
    """Each link of data/footer.toml with its address filled in, as the
    footer of base.html fills it, and whether it shows."""
    with open(ROOT / "identity.toml", "rb") as f:
        identity = tomllib.load(f)
    with open(ROOT / "data" / "footer.toml", "rb") as f:
        footer = tomllib.load(f)
    handle, host = identity["brand"]["handle"], urlparse(identity["site"]["url"]).netloc
    return [(link["url"].replace("{handle}", handle).replace("{host}", host), link["show"])
            for link in footer["link"]]


def check_footer(out, all_shown=False):
    """A profile or the contact address with `show = false` is nowhere in the
    built site; one that shows is in the footer of both home pages."""
    problems = []
    pages = {page.relative_to(out).as_posix(): page.read_text(encoding="utf-8")
             for page in html_files(out)}
    for url, show in footer_links():
        if show or all_shown:
            for home in ["index.html", "en/index.html"]:
                if f'href="{url}"' not in pages.get(home, ""):
                    problems.append(f"footer: {home} does not link to {url}, which has show = true")
        else:
            problems.extend(f"footer: {name} shows {url}, which has show = false"
                            for name, text in pages.items() if url in text)
    return problems


THUMB = re.compile(r'<span class="thumb"[^>]*>')


def check_thumbnails(out):
    """A thumbnail on an English page is an English version (.en. in its
    name) or an image with no text (data-no-text, D388); a Portuguese page
    never shows the English version."""
    problems = []
    for page in html_files(out):
        name = page.relative_to(out).as_posix()
        english = name.startswith("en/")
        for tag in THUMB.findall(page.read_text(encoding="utf-8")):
            image = Path(re.search(r"url\('([^']*)'\)", tag).group(1)).name
            if english and ".en." not in image and "data-no-text" not in tag:
                problems.append(f"thumbnails: {name}: {image} has text in Portuguese; use the "
                                "English version or mark it with thumbnail_has_text = false (D388)")
            if not english and ".en." in image:
                problems.append(f"thumbnails: {name}: {image} is the English version")
    return problems


ROADMAP = re.compile(r'<ol class="roadmap">(.*?)</ol>\s*</section>', re.S)
ROADMAP_LINK = re.compile(r'<a class="(?:stage|delivery)-row" href="([^"]*)"')


def roadmap_posts():
    """The posts the roadmap links to: each stage and delivery with `post`."""
    with open(ROOT / "data" / "roadmap.toml", "rb") as f:
        roadmap = tomllib.load(f)
    posts = []
    for stage in roadmap["stage"]:
        posts += [stage["post"]] if "post" in stage else []
        posts += [d["post"] for d in stage.get("delivery", []) if "post" in d]
    return posts


def check_roadmap(out):
    """Every link of the roadmap, in Portuguese and in English, goes to a
    post that exists, in the page's language, and there is one link for
    each `post` of data/roadmap.toml."""
    problems = []
    expected = roadmap_posts()
    for page, prefix in [("devlog/index.html", "/devlog/"), ("en/devlog/index.html", "/en/devlog/")]:
        found = ROADMAP.search((out / page).read_text(encoding="utf-8"))
        if not found:
            problems.append(f"roadmap: {page} has no roadmap")
            continue
        links = [urlparse(href).path for href in ROADMAP_LINK.findall(found.group(1))]
        if [link.removeprefix(prefix).strip("/") for link in links] != expected:
            problems.append(f"roadmap: {page} links to {links}, and data/roadmap.toml has the "
                            f"posts {expected}")
        for link in links:
            if not link.startswith(prefix):
                problems.append(f"roadmap: {page} links to {link}, in the other language")
            if not (out / link.strip("/") / "index.html").is_file():
                problems.append(f"roadmap: {page} links to {link}, which is not a post")
    return problems


def check_variant(tmp):
    """A copy of the site with a "&" and quotes in the devlog's lead and every
    footer link shown: the "&" is escaped once in the description, and the
    links show up."""
    copy = tmp / "variant"
    for path in tracked_files(ROOT):
        target = copy / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / path, target)
    lead = copy / "content" / "devlog" / "_index.md"
    lead.write_text(lead.read_text(encoding="utf-8") + '\nTeste & "aspas".\n', encoding="utf-8")
    footer = copy / "data" / "footer.toml"
    footer.write_text(footer.read_text(encoding="utf-8").replace("show = false", "show = true"),
                      encoding="utf-8")
    out = tmp / "variant-out"
    built = subprocess.run([os.environ.get("ZOLA", "zola"), "build", "--base-url",
                            "https://variant.example", "-o", str(out), "-f"],
                           cwd=copy, capture_output=True, text=True)
    if built.returncode != 0:
        return [f"variant: the build failed:\n{built.stderr}"]
    problems = []
    devlog = (out / "devlog" / "index.html").read_text(encoding="utf-8")
    description = DESCRIPTION.findall(devlog)
    if not description or "Teste &amp; " not in description[0] or "aspas" not in description[0]:
        problems.append(f"description: a \"&\" and quotes in the devlog's lead do not come out as "
                        f"one escaped description: {description}")
    problems += [p for p in check_descriptions(out) if p.startswith("description: devlog/")]
    problems += check_footer(out, all_shown=True)
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
                    + check_image_language(main_out)
                    + check_numbers()
                    + check_404(main_out)
                    + check_descriptions(main_out)
                    + check_footer(main_out)
                    + check_thumbnails(main_out)
                    + check_roadmap(main_out)
                    + check_variant(tmp))
        ids = feed_ids(main_out)
    for problem in problems:
        print(f"check_site: {problem}", file=sys.stderr)
    if problems:
        return 1
    print("check_site: address, E9.4, images, thousands, 404, descriptions, footer, thumbnails "
          "and roadmap "
          f"pass; feed ids of main: {ids}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
