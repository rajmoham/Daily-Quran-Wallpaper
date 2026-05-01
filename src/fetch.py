"""AlQuran.cloud client.

Fetches Arabic (Uthmani script) and Sahih International English translation for a
given (surah, ayah) reference.

API docs: https://alquran.cloud/api
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import requests

API_BASE = "https://api.alquran.cloud/v1"
ARABIC_EDITION = "quran-uthmani"
ENGLISH_EDITION = "en.sahih"

USER_AGENT = "quran-wallpaper/1.0 (+https://github.com/)"


class FetchError(RuntimeError):
    """Raised when the API cannot be reached or returns an unexpected payload."""


@dataclass(frozen=True)
class Ayah:
    surah_num: int
    ayah_num: int
    surah_name_en: str
    surah_name_ar: str
    arabic: str
    english: str

    @property
    def reference(self) -> str:
        return f"{self.surah_num}:{self.ayah_num}"


def _request(url: str, *, retries: int = 3, backoff: float = 1.5) -> dict[str, Any]:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
            resp.raise_for_status()
            payload = resp.json()
        except (requests.RequestException, ValueError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(backoff ** attempt)
            continue

        if payload.get("code") != 200 or "data" not in payload:
            raise FetchError(f"Unexpected payload from {url}: {payload!r}")
        return payload["data"]
    raise FetchError(f"Failed to fetch {url} after {retries} attempts: {last_err}")


def get_ayah(surah: int, ayah: int) -> Ayah:
    """Fetch a single ayah in both Arabic (Uthmani) and Sahih English translation."""
    ref = f"{surah}:{ayah}"
    arabic_data = _request(f"{API_BASE}/ayah/{ref}/{ARABIC_EDITION}")
    english_data = _request(f"{API_BASE}/ayah/{ref}/{ENGLISH_EDITION}")

    surah_block = arabic_data.get("surah") or {}
    return Ayah(
        surah_num=int(surah_block.get("number", surah)),
        ayah_num=int(arabic_data.get("numberInSurah", ayah)),
        surah_name_en=str(surah_block.get("englishName", "")),
        surah_name_ar=str(surah_block.get("name", "")),
        arabic=str(arabic_data.get("text", "")).strip(),
        english=str(english_data.get("text", "")).strip(),
    )
