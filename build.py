"""Builds the site with its address from identity.toml (D379).

Cloudflare Pages runs `python3 build.py` (Zola comes from ZOLA_VERSION), the
CI does the same, and locally `python build.py` works with Zola on the PATH
or in ZOLA. Extra arguments go to `zola build`.

The address:
- previews (any branch but main) use their own Cloudflare address;
- main uses its Cloudflare address too, until the domain is connected and
  DOMAIN_LIVE=1 is set in Pages; then the address from identity.toml;
- anywhere else, the address from identity.toml.
"""

import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def address(env, identity_url):
    """The base URL for this build."""
    deployment = env.get("CF_PAGES_URL")
    if not deployment:
        return identity_url
    if env.get("CF_PAGES_BRANCH") == "main" and env.get("DOMAIN_LIVE") == "1":
        return identity_url
    return deployment


def main():
    with open(ROOT / "identity.toml", "rb") as f:
        identity_url = tomllib.load(f)["site"]["url"]
    url = address(os.environ, identity_url)
    zola = os.environ.get("ZOLA", "zola")
    print(f"build.py: zola build --base-url {url}", flush=True)
    return subprocess.call([zola, "build", "--base-url", url, *sys.argv[1:]], cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
