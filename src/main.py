"""CLI entry point: fetch today's ayah, render the wallpaper, save it to docs/."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from . import ayahs, fetch, render

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_PNG = DOCS_DIR / "wallpaper.png"
OUTPUT_JSON = DOCS_DIR / "wallpaper.json"


def _parse_ref(value: str) -> tuple[int, int]:
    try:
        s, a = value.split(":")
        return int(s), int(a)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError(
            f"--ayah expects 'surah:ayah' (e.g. 2:255), got {value!r}"
        ) from exc


def _parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"--date expects YYYY-MM-DD, got {value!r}"
        ) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate today's Quran wallpaper.")
    parser.add_argument(
        "--ayah",
        type=_parse_ref,
        help="Override the ayah selection, e.g. 2:255.",
    )
    parser.add_argument(
        "--date",
        type=_parse_date,
        help="Pick the ayah for a specific UTC date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Open the generated image in the default viewer.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUTPUT_PNG,
        help=f"Output PNG path (default: {OUTPUT_PNG}).",
    )
    args = parser.parse_args(argv)

    today = args.date or dt.datetime.utcnow().date()
    if args.ayah is not None:
        surah, ayah_num = args.ayah
    else:
        surah, ayah_num = ayahs.pick_for_date(today)

    print(f"[wallpaper] date={today.isoformat()} ayah={surah}:{ayah_num}", flush=True)

    ayah = fetch.get_ayah(surah, ayah_num)
    img = render.render(ayah)

    out_png: Path = args.out
    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png, format="PNG", optimize=True)
    print(f"[wallpaper] wrote {out_png} ({img.size[0]}x{img.size[1]})", flush=True)

    # Metadata sidecar (only when writing to the default location)
    if out_png == OUTPUT_PNG:
        meta = {
            "date": today.isoformat(),
            "surah": ayah.surah_num,
            "ayah": ayah.ayah_num,
            "reference": ayah.reference,
            "surah_name_en": ayah.surah_name_en,
            "surah_name_ar": ayah.surah_name_ar,
            "arabic": ayah.arabic,
            "english": ayah.english,
            "translation_edition": fetch.ENGLISH_EDITION,
            "arabic_edition": fetch.ARABIC_EDITION,
        }
        OUTPUT_JSON.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[wallpaper] wrote {OUTPUT_JSON}", flush=True)

    if args.preview:
        img.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())
