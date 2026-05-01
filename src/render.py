"""Render the daily ayah onto an iPhone 14 Pro wallpaper PNG.

Layout:
    +------------------------------------+   <- 1179 x 2556
    |        (safe top, clock area)      |
    |   +----- gold double border -----+ |
    |   |   Arabic (RTL, Amiri Bold)   | |
    |   |   ─── hairline divider ───   | |
    |   |   English (Cormorant)        | |
    |   |        Surah X · S:A         | |
    |   +------------------------------+ |
    |   (safe bottom, Face ID area)      |
    +------------------------------------+
"""
from __future__ import annotations

from typing import Iterable

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

from . import style
from .fetch import Ayah


# ---------- Background ----------

def _gradient_background() -> Image.Image:
    """Subtle vertical gradient between BG_TOP and BG_BOTTOM."""
    img = Image.new("RGB", (style.CANVAS_WIDTH, style.CANVAS_HEIGHT), style.BG_TOP)
    top = style.BG_TOP
    bot = style.BG_BOTTOM
    height = style.CANVAS_HEIGHT
    pixels = img.load()
    for y in range(height):
        t = y / (height - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(style.CANVAS_WIDTH):
            pixels[x, y] = (r, g, b)
    return img


# ---------- Text shaping ----------

def _shape_arabic(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


# ---------- Font loading ----------

def _font(path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


# ---------- Word wrapping ----------

def _measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    if not text:
        return (0, 0)
    bbox = draw.textbbox((0, 0), text, font=font)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])


def _wrap_to_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """Greedy word-wrap. Works for both Latin and (already-shaped) Arabic strings.

    For Arabic, pass the *unshaped* logical string here, then shape each line
    afterwards — that way we wrap on logical words but render each line shaped/RTL.
    """
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        w, _ = _measure(draw, candidate, font)
        if w <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _block_height(
    draw: ImageDraw.ImageDraw,
    lines: Iterable[str],
    font: ImageFont.FreeTypeFont,
    line_spacing: float,
) -> int:
    lines = list(lines)
    if not lines:
        return 0
    line_h = font.size  # nominal em height; line_spacing controls actual leading
    return int(line_h * line_spacing * len(lines))


# ---------- Auto-fit ----------

def _autofit_arabic(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path,
    max_width: int,
    max_height: int,
    size_max: int,
    size_min: int,
    line_spacing: float,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    """Find largest size where shaped+wrapped Arabic fits in (max_width, max_height).

    We wrap on the *logical* (unshaped) string, then return shaped lines for rendering.
    """
    for size in range(size_max, size_min - 1, -2):
        font = _font(font_path, size)
        # Use shaped full string for width measurement to be safe
        shaped_full = _shape_arabic(text)
        full_w, _ = _measure(draw, shaped_full, font)
        if full_w <= max_width:
            shaped_lines = [shaped_full]
        else:
            logical_lines = _wrap_to_width(draw, text, font, max_width)
            shaped_lines = [_shape_arabic(line) for line in logical_lines]
        h = _block_height(draw, shaped_lines, font, line_spacing)
        # Re-measure widest shaped line
        widest = max((_measure(draw, ln, font)[0] for ln in shaped_lines), default=0)
        if widest <= max_width and h <= max_height:
            return font, shaped_lines
    # Fall back to minimum size with whatever wrapping fits
    font = _font(font_path, size_min)
    shaped_full = _shape_arabic(text)
    full_w, _ = _measure(draw, shaped_full, font)
    if full_w <= max_width:
        return font, [shaped_full]
    logical_lines = _wrap_to_width(draw, text, font, max_width)
    return font, [_shape_arabic(line) for line in logical_lines]


def _autofit_latin(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path,
    max_width: int,
    max_height: int,
    size_max: int,
    size_min: int,
    line_spacing: float,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(size_max, size_min - 1, -2):
        font = _font(font_path, size)
        lines = _wrap_to_width(draw, text, font, max_width)
        widest = max((_measure(draw, ln, font)[0] for ln in lines), default=0)
        h = _block_height(draw, lines, font, line_spacing)
        if widest <= max_width and h <= max_height:
            return font, lines
    font = _font(font_path, size_min)
    return font, _wrap_to_width(draw, text, font, max_width)


# ---------- Drawing primitives ----------

def _draw_double_border(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Classic mushaf-style double rounded border in gold."""
    x0, y0, x1, y1 = box
    # Outer
    draw.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=style.BOX_RADIUS,
        outline=style.GOLD,
        width=style.BOX_STROKE_OUTER,
    )
    # Inner
    g = style.BOX_DOUBLE_GAP
    draw.rounded_rectangle(
        (x0 + g, y0 + g, x1 - g, y1 - g),
        radius=max(style.BOX_RADIUS - g, 4),
        outline=style.GOLD_DIM,
        width=style.BOX_STROKE_INNER,
    )


def _draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    font: ImageFont.FreeTypeFont,
    *,
    box_left: int,
    box_right: int,
    top_y: int,
    line_spacing: float,
    align: str,
    color: tuple[int, int, int],
) -> int:
    """Draw a list of pre-wrapped lines. Returns y position after the block."""
    line_h = int(font.size * line_spacing)
    y = top_y
    for line in lines:
        w, _ = _measure(draw, line, font)
        if align == "right":
            x = box_right - w
        elif align == "left":
            x = box_left
        else:  # center
            x = box_left + (box_right - box_left - w) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += line_h
    return y


# ---------- Public API ----------

def render(ayah: Ayah) -> Image.Image:
    img = _gradient_background()
    draw = ImageDraw.Draw(img)

    # Box geometry — vertically positioned within iOS safe area
    box_left = style.BOX_INSET_X
    box_right = style.CANVAS_WIDTH - style.BOX_INSET_X
    inner_top = style.SAFE_TOP
    inner_bottom = style.CANVAS_HEIGHT - style.SAFE_BOTTOM

    text_left = box_left + style.BOX_PADDING
    text_right = box_right - style.BOX_PADDING
    text_width = text_right - text_left
    text_area_height = (inner_bottom - inner_top) - 2 * style.BOX_PADDING

    # Reserve space for divider + reference footer
    reference = f"Surah {ayah.surah_name_en} \u00b7 {ayah.surah_num}:{ayah.ayah_num}"
    ref_font = _font(style.LATIN_FONT_REGULAR, style.REF_SIZE)
    ref_w, ref_h = _measure(draw, reference, ref_font)
    divider_block_h = style.DIVIDER_VPAD * 2 + 2
    reserved = divider_block_h + ref_h + 40  # 40 = gap above reference

    # Allocate ~55% of remaining height to Arabic, rest to English
    remaining = text_area_height - reserved
    arabic_max_h = int(remaining * 0.55)
    english_max_h = remaining - arabic_max_h

    arabic_font, arabic_lines = _autofit_arabic(
        draw, ayah.arabic, style.ARABIC_FONT,
        max_width=text_width,
        max_height=arabic_max_h,
        size_max=style.ARABIC_SIZE_MAX,
        size_min=style.ARABIC_SIZE_MIN,
        line_spacing=style.ARABIC_LINE_SPACING,
    )

    english_font, english_lines = _autofit_latin(
        draw, ayah.english, style.LATIN_FONT,
        max_width=text_width,
        max_height=english_max_h,
        size_max=style.LATIN_SIZE_MAX,
        size_min=style.LATIN_SIZE_MIN,
        line_spacing=style.LATIN_LINE_SPACING,
    )

    arabic_h = _block_height(draw, arabic_lines, arabic_font, style.ARABIC_LINE_SPACING)
    english_h = _block_height(draw, english_lines, english_font, style.LATIN_LINE_SPACING)
    content_h = arabic_h + divider_block_h + english_h + 40 + ref_h

    # Vertically center the actual content within the inner area
    content_top = inner_top + style.BOX_PADDING + max(0, (text_area_height - content_h) // 2)

    # --- Box (sized snugly around content with padding) ---
    box_y0 = content_top - style.BOX_PADDING
    box_y1 = content_top + content_h + style.BOX_PADDING
    # Clamp box to safe area
    box_y0 = max(box_y0, style.SAFE_TOP)
    box_y1 = min(box_y1, style.CANVAS_HEIGHT - style.SAFE_BOTTOM)
    _draw_double_border(draw, (box_left, box_y0, box_right, box_y1))

    # --- Arabic (right-aligned, RTL) ---
    y_after_arabic = _draw_lines(
        draw, arabic_lines, arabic_font,
        box_left=text_left, box_right=text_right,
        top_y=content_top,
        line_spacing=style.ARABIC_LINE_SPACING,
        align="right",
        color=style.GOLD,
    )

    # --- Divider ---
    div_y = y_after_arabic + style.DIVIDER_VPAD
    div_w = int(text_width * style.DIVIDER_WIDTH_RATIO)
    div_x0 = text_left + (text_width - div_w) // 2
    div_x1 = div_x0 + div_w
    draw.line((div_x0, div_y, div_x1, div_y), fill=style.GOLD, width=1)
    y_after_divider = div_y + style.DIVIDER_VPAD

    # --- English (centered) ---
    y_after_english = _draw_lines(
        draw, english_lines, english_font,
        box_left=text_left, box_right=text_right,
        top_y=y_after_divider,
        line_spacing=style.LATIN_LINE_SPACING,
        align="center",
        color=style.GOLD,
    )

    # --- Reference ---
    ref_y = y_after_english + 40
    ref_x = text_left + (text_width - ref_w) // 2
    draw.text((ref_x, ref_y), reference, font=ref_font, fill=style.GOLD)

    return img
