"""Tests for the date-based ayah selector."""
from __future__ import annotations

import datetime as dt

from src import ayahs


def test_pick_is_deterministic():
    d = dt.date(2026, 5, 1)
    assert ayahs.pick_for_date(d) == ayahs.pick_for_date(d)


def test_pick_returns_listed_ayah():
    d = dt.date(2026, 5, 1)
    assert ayahs.pick_for_date(d) in ayahs.SIGNIFICANT_AYAHS


def test_pick_varies_across_dates():
    picks = {ayahs.pick_for_date(dt.date(2026, 1, 1) + dt.timedelta(days=i)) for i in range(60)}
    # Over 60 distinct dates we expect at least a few distinct ayahs.
    assert len(picks) > 5


def test_list_is_non_empty_and_in_range():
    assert len(ayahs.SIGNIFICANT_AYAHS) >= 100
    for surah, ayah in ayahs.SIGNIFICANT_AYAHS:
        assert 1 <= surah <= 114
        assert ayah >= 1
