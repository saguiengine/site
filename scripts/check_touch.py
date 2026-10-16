"""Touch targets of at least 32 x 32 px on a phone (rule 18 of D322).

Builds the site, serves it locally, opens the main pages 390 px wide in
headless Chrome and measures every link outside the running text of a page
(links inside the text of a post or a lead are exempt, as in WCAG 2.5.8).

Run: python3 scripts/check_touch.py (needs Zola, or ZOLA, and Chrome on
the PATH, or in CHROME).
"""

import functools
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN = 32
WIDTH = 390
PAGES = ["/", "/devlog/", "/en/", "/en/devlog/", "/licenca/"]

MEASURE = """<!doctype html><meta charset="utf-8"><body>
<script>
const pages = %s;
const results = [];
let left = pages.length;
for (const page of pages) {
  const frame = document.createElement('iframe');
  frame.style.width = '%dpx'; frame.style.height = '1600px'; frame.src = page;
  frame.onload = () => {
    const doc = frame.contentDocument;
    for (const a of doc.querySelectorAll('a')) {
      if (a.closest('.prose, .lead') || a.classList.contains('skip')) continue;
      const r = a.getBoundingClientRect();
      results.push({page, text: a.textContent.trim(), w: Math.round(r.width), h: Math.round(r.height)});
    }
    if (--left === 0) document.title = 'done:' + JSON.stringify(results);
  };
  document.body.appendChild(frame);
}
</script>"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def chrome():
    for name in [os.environ.get("CHROME"), "google-chrome", "chromium", "chrome",
                 r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if name and (shutil.which(name) or Path(name).exists()):
            return shutil.which(name) or name
    raise SystemExit("check_touch: Chrome not found (set CHROME)")


def main():
    zola = os.environ.get("ZOLA", "zola")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "public"
        handler = functools.partial(QuietHandler, directory=str(out))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        port = server.server_address[1]
        subprocess.run([zola, "build", "--base-url", f"http://127.0.0.1:{port}", "-o", str(out)],
                       cwd=ROOT, check=True, capture_output=True)
        (out / "measure.html").write_text(MEASURE % (json.dumps(PAGES), WIDTH), encoding="utf-8")
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            dom = subprocess.run(
                [chrome(), "--headless=new", "--disable-gpu", "--no-sandbox",
                 "--virtual-time-budget=10000", "--dump-dom",
                 f"http://127.0.0.1:{port}/measure.html"],
                capture_output=True, text=True, timeout=120).stdout
        finally:
            server.shutdown()
    start = dom.find("<title>done:")
    if start < 0:
        print("check_touch: the pages did not load in Chrome", file=sys.stderr)
        return 1
    import html
    results = json.loads(html.unescape(dom[start + len("<title>done:"):dom.find("</title>", start)]))
    small = [r for r in results if r["w"] < MIN or r["h"] < MIN]
    for r in small:
        print(f"check_touch: {r['page']} \"{r['text']}\" is {r['w']} x {r['h']} px "
              f"(at least {MIN} x {MIN})", file=sys.stderr)
    if small:
        return 1
    smallest = min(results, key=lambda r: min(r["w"], r["h"]))
    print(f"check_touch: {len(results)} links at {WIDTH} px, the smallest "
          f"\"{smallest['text']}\" {smallest['w']} x {smallest['h']} px")
    return 0


if __name__ == "__main__":
    sys.exit(main())
