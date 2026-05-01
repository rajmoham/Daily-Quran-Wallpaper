"""Download the Arabic + Latin fonts the renderer needs.

Run once after cloning:

    python scripts/download_fonts.py

The fonts are downloaded from the official Google Fonts GitHub repositories.
Both are licensed under the SIL Open Font License 1.1.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = REPO_ROOT / "assets" / "fonts"

FONT_URLS: dict[str, str] = {
    # Amiri — classic Naskh-style Arabic typeface (served via Google Fonts repo)
    "Amiri-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Bold.ttf",
    # Cormorant Garamond — elegant serif, pairs well with Amiri (variable fonts)
    "CormorantGaramond-Italic.ttf":
        "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf",
    "CormorantGaramond-Regular.ttf":
        "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
}


def download(name: str, url: str) -> None:
    dest = FONTS_DIR / name
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[fonts] {name} already present, skipping")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[fonts] downloading {name} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "quran-wallpaper/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp, open(dest, "wb") as fh:
        fh.write(resp.read())
    print(f"[fonts] saved {dest}")


def main() -> int:
    for name, url in FONT_URLS.items():
        try:
            download(name, url)
        except Exception as exc:  # noqa: BLE001
            print(f"[fonts] FAILED to download {name} from {url}: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
