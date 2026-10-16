"""The brand lives only in identity.toml (D276, D379), and E9.2.

1. No brand value is written in the site's files: templates, content, data,
   styles and configuration read it from identity.toml. People's documents
   (README, credits, licenses) and binary files are exempt.
2. E9.2: a copy of the site with another brand in identity.toml, and no other
   file changed, builds pages in both languages that show the other brand
   and none of the real one. Text drawn inside images is out of reach.

Run from anywhere: `python3 scripts/check_brand.py`. Needs Zola on the PATH,
or in ZOLA.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# People's documents and files that are not the site's text.
EXEMPT = {"identity.toml", "README.md", "CREDITOS.md", "LICENSE",
          "LICENSE-CC-BY-4.0.txt", "LICENSE-CC0-1.0.txt"}
BINARY = {".ttf", ".otf", ".woff", ".woff2", ".png", ".jpg", ".jpeg", ".gif",
          ".webp", ".ico"}
# The text the built site serves; images are out of reach (D379).
OUTPUT_TEXT = {".html", ".xml", ".txt", ".css", ".js", ".json", ""}

# Another brand for E9.2, unlike any word of the site.
TEST_BRAND = {
    "engine_name": "Marmota",
    "language_name": "MarmotaScript",
    "script_extension": "marmota",
    "config_dir": "marmota",
    "config_dir_dev": "Marmota (dev)",
    "url_scheme": "marmota",
    "handle": "marmotaengine",
}
TEST_URL = "https://marmota.example"
TEST_SAYING = {"pronunciation": "mar-MOH-tah", "pt": "um bichinho de teste",
               "en": "a little test animal"}


def saying(identity):
    """How the name sounds and what it means, for the footer (D276), or
    None when identity.toml does not say."""
    site = identity.get("site", {})
    meaning = site.get("meaning", {})
    if "pronunciation" not in site or "pt" not in meaning or "en" not in meaning:
        return None
    return {"pronunciation": site["pronunciation"], "pt": meaning["pt"], "en": meaning["en"]}


def tokens(identity):
    """The brand's words: [brand] values of three letters or more, the
    site's host and how the name sounds and what it means, lowercase."""
    words = {v.lower() for v in identity["brand"].values()
             if isinstance(v, str) and len(v) >= 3}
    words.add(urlparse(identity["site"]["url"]).hostname.lower())
    words.update(v.lower() for v in (saying(identity) or {}).values())
    return sorted(words)


def tracked_files(root):
    listing = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, capture_output=True, check=True)
    return [p for p in listing.stdout.decode().split("\0") if p]


def find_brand(path, text, words):
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        lower = line.lower()
        for word in words:
            if word in lower:
                found.append(f"{path}:{number}: contains `{word}`")
                break
    return found


def check_written(identity):
    """Part 1: nothing spells the brand outside identity.toml."""
    words = tokens(identity)
    findings = []
    for path in tracked_files(ROOT):
        name = Path(path).name
        if name in EXEMPT or Path(path).suffix.lower() in BINARY:
            continue
        try:
            text = (ROOT / path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        findings.extend(find_brand(path, text, words))
    return findings


def test_identity_text(original):
    """identity.toml with the test brand: only the values change."""
    text = original
    with open(ROOT / "identity.toml", "rb") as f:
        identity = tomllib.load(f)
    for key, value in TEST_BRAND.items():
        old = identity["brand"][key]
        text = text.replace(f'{key} = "{old}"', f'{key} = "{value}"')
    text = text.replace(f'url = "{identity["site"]["url"]}"', f'url = "{TEST_URL}"')
    for key, value in (saying(identity) or {}).items():
        text = text.replace(f'"{value}"', f'"{TEST_SAYING[key]}"')
    return text


def check_e9_2(identity):
    """Part 2: another brand in identity.toml changes the whole site."""
    zola = os.environ.get("ZOLA", "zola")
    real = tokens(identity)
    problems = []
    if saying(identity) is None:
        problems.append("E9.2: identity.toml does not say how the name sounds and what it "
                        "means ([site] pronunciation and [site.meaning] pt and en, D276)")
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "site"
        for path in tracked_files(ROOT):
            target = copy / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, target)
        original = (ROOT / "identity.toml").read_text(encoding="utf-8")
        changed = test_identity_text(original)
        if changed == original:
            return ["E9.2: the test brand did not change identity.toml"]
        (copy / "identity.toml").write_text(changed, encoding="utf-8")

        # No other file changed.
        for path in tracked_files(ROOT):
            if path != "identity.toml" and (copy / path).read_bytes() != (ROOT / path).read_bytes():
                problems.append(f"E9.2: {path} changed")

        built = subprocess.run([zola, "build", "--base-url", TEST_URL], cwd=copy,
                               capture_output=True, text=True)
        if built.returncode != 0:
            return [f"E9.2: the build with the test brand failed:\n{built.stderr}"]

        public = copy / "public"
        for file in sorted(public.rglob("*")):
            if file.is_file() and file.suffix.lower() in OUTPUT_TEXT:
                text = file.read_text(encoding="utf-8", errors="replace")
                problems.extend("E9.2: " + f for f in
                                find_brand(file.relative_to(public).as_posix(), text, real))

        for page in ["index.html", "en/index.html", "devlog/index.html", "en/devlog/index.html"]:
            path = public / page
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            for name in (TEST_BRAND["engine_name"], TEST_BRAND["language_name"]):
                if page.endswith("devlog/index.html") and name == TEST_BRAND["language_name"]:
                    continue
                if name not in text:
                    problems.append(f"E9.2: {page} does not show `{name}`")
        for page, lang in [("index.html", "pt"), ("en/index.html", "en")]:
            path = public / page
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            phrase = (f"{TEST_BRAND['engine_name']} ({TEST_SAYING['pronunciation']}): "
                      f"{TEST_SAYING[lang]}")
            if phrase not in text:
                problems.append(f"E9.2: {page} does not show `{phrase}` in the footer")
    return problems


def main():
    with open(ROOT / "identity.toml", "rb") as f:
        identity = tomllib.load(f)
    written = check_written(identity)
    for finding in written:
        print(f"check_brand: {finding}", file=sys.stderr)
    if written:
        print("check_brand: read the brand from identity.toml: {{ <marca /> }} in "
              "content, load_data in templates (D276, D379)", file=sys.stderr)
    e9_2 = check_e9_2(identity)
    for problem in e9_2:
        print(f"check_brand: {problem}", file=sys.stderr)
    if written or e9_2:
        return 1
    print("check_brand: the brand is only in identity.toml, and another brand "
          "there changes the whole site (E9.2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
