"""Smoke test for the renderer using a fixed payload (no network)."""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("PIL")
pytest.importorskip("arabic_reshaper")
pytest.importorskip("bidi")

from src import render, style
from src.fetch import Ayah


def _fonts_present() -> bool:
    return style.ARABIC_FONT.exists() and style.LATIN_FONT.exists() and style.LATIN_FONT_REGULAR.exists()


@pytest.mark.skipif(not _fonts_present(), reason="Fonts not downloaded; run scripts/download_fonts.py")
def test_render_produces_correct_dimensions(tmp_path: Path):
    sample = Ayah(
        surah_num=2,
        ayah_num=255,
        surah_name_en="Al-Baqarah",
        surah_name_ar="البقرة",
        arabic=(
            "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ "
            "لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ"
        ),
        english=(
            "Allah - there is no deity except Him, the Ever-Living, the Sustainer of existence. "
            "Neither drowsiness overtakes Him nor sleep. To Him belongs whatever is in the heavens and whatever is on the earth."
        ),
    )
    img = render.render(sample)
    assert img.size == (style.CANVAS_WIDTH, style.CANVAS_HEIGHT)

    out = tmp_path / "wallpaper.png"
    img.save(out, format="PNG")
    assert out.exists() and out.stat().st_size > 0
