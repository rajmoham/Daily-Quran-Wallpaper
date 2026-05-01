"""Visual style constants for the wallpaper renderer."""
from __future__ import annotations

from pathlib import Path

# --- Canvas (iPhone 14 Pro native resolution) ---
CANVAS_WIDTH = 1179
CANVAS_HEIGHT = 2556

# --- iOS safe areas (Lock Screen) ---
# Top reserved for clock / status; bottom reserved for Face ID indicator + flashlight/camera shortcuts.
SAFE_TOP = 360
SAFE_BOTTOM = 420
SAFE_SIDE = 80

# --- Colors ---
GOLD = (201, 169, 97)            # #C9A961 muted antique gold
GOLD_DIM = (140, 117, 65)        # darker gold for outer hairline of double border
BG_TOP = (14, 14, 16)            # #0E0E10
BG_BOTTOM = (26, 26, 31)         # #1A1A1F

# --- Box ---
BOX_INSET_X = SAFE_SIDE          # px from left/right edges
BOX_PADDING = 70                 # inner padding inside the gold box
BOX_RADIUS = 24
BOX_STROKE_OUTER = 2
BOX_STROKE_INNER = 1
BOX_DOUBLE_GAP = 10              # gap between outer and inner stroke

# --- Typography ---
FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
ARABIC_FONT = FONTS_DIR / "Amiri-Bold.ttf"
LATIN_FONT = FONTS_DIR / "CormorantGaramond-Italic.ttf"
LATIN_FONT_REGULAR = FONTS_DIR / "CormorantGaramond-Regular.ttf"

ARABIC_SIZE_MAX = 110
ARABIC_SIZE_MIN = 48
ARABIC_LINE_SPACING = 1.7

LATIN_SIZE_MAX = 56
LATIN_SIZE_MIN = 28
LATIN_LINE_SPACING = 1.35

REF_SIZE = 32                    # surah reference footer

# --- Layout proportions inside the box ---
DIVIDER_WIDTH_RATIO = 0.35       # hairline divider between Arabic and English (fraction of box width)
DIVIDER_VPAD = 50                # vertical padding around divider
