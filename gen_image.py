#!/usr/bin/env python3
"""Render entry.png: a 1024x1024 infographic summarising 22 Nov 2026 news.

Generation-time only: uses Pillow and local DejaVu fonts. The grader
never runs this file; main.py simply copies the finished entry.png.
Run:  python3 gen_image.py   (writes entry.png beside this script)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

W = H = 1024
MARGIN = 32
GAP = 16

BG = (13, 20, 36)
HEADER_BG = (20, 32, 54)
PANEL_BG = (24, 38, 62)
TEXT = (245, 247, 250)
MUTED = (178, 190, 208)
WHITE = (255, 255, 255)

STORIES = [
    (
        "AI SELL-OFF ROCKS MARKETS",
        "S&P 500 -3.7%, Nasdaq -5.28% on Fri 20 Nov; Nasdaq erased its "
        "2026 gains amid doubts over AI spending.",
        (239, 83, 80),
    ),
    (
        "TANKER HIT NEAR HORMUZ",
        "Tanker ablaze east of Hormuz, no casualties; IRGC says it "
        "downed a US drone as Trump weighs strikes, IDF on high alert.",
        (255, 167, 38),
    ),
    (
        "COP31 DEADLOCKED, NO DEAL YET",
        "Antalya climate talks ran into overtime, deadlocked - the "
        "latest draft drops all mention of fossil fuels.",
        (102, 187, 106),
    ),
    (
        "6.8-6.9 QUAKE SHAKES PERU",
        "Epicentre near Junin, felt in Lima; no damage or "
        "casualties reported.",
        (171, 71, 188),
    ),
    (
        "CANCER PILL: EARLY PROMISE",
        "Early trial: daraxonrasib shrank or cleared tumours in "
        "60.7% of 61 pancreatic-cancer patients. Promising.",
        (38, 198, 218),
    ),
    (
        "INDONESIA WILDFIRES INTENSIFY",
        "About 200M tonnes of carbon, 3rd-highest since 2003; "
        "8.9M hectares burned, worst El Nino season in 11 years.",
        (255, 112, 67),
    ),
]


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int):
    """Greedy word wrap measured with the real font metrics."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_panel(draw, x, y, w, h, index, headline, subtext, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL_BG)
    draw.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    # Number badge
    badge_r = 20
    cx, cy = x + 34, y + 42
    draw.ellipse([cx - badge_r, cy - badge_r, cx + badge_r, cy + badge_r],
                 fill=accent)
    num_font = font("DejaVuSans-Bold.ttf", 24)
    num = str(index)
    nw = draw.textlength(num, font=num_font)
    draw.text((cx - nw / 2, cy - 15), num, font=num_font, fill=(10, 14, 22))

    inner_x = x + 24
    inner_w = w - 48
    head_font = font("DejaVuSans-Bold.ttf", 27)
    body_font = font("DejaVuSans.ttf", 21)

    ty = y + 72
    for line in wrap(draw, headline, head_font, inner_w):
        draw.text((inner_x, ty), line, font=head_font, fill=WHITE)
        ty += 33
    ty += 8
    for line in wrap(draw, subtext, body_font, inner_w):
        draw.text((inner_x, ty), line, font=body_font, fill=MUTED)
        ty += 27


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rounded_rectangle([MARGIN, 24, W - MARGIN, 132], radius=14,
                           fill=HEADER_BG)
    date_font = font("DejaVuSans-Bold.ttf", 44)
    title_font = font("DejaVuSans-Bold.ttf", 24)
    draw.text((MARGIN + 24, 40), "22 NOVEMBER 2026", font=date_font,
              fill=WHITE)
    draw.text((MARGIN + 26, 94), "THE WORLD IN ONE IMAGE",
              font=title_font, fill=(255, 213, 79))

    # Panels: 2 columns x 3 rows
    top = 148
    bottom = 968
    cols, rows = 2, 3
    panel_w = (W - 2 * MARGIN - (cols - 1) * GAP) // cols
    panel_h = (bottom - top - (rows - 1) * GAP) // rows
    for i, (headline, subtext, accent) in enumerate(STORIES):
        col, row = i % cols, i // cols
        x = MARGIN + col * (panel_w + GAP)
        y = top + row * (panel_h + GAP)
        draw_panel(draw, x, y, panel_w, panel_h, i + 1,
                   headline, subtext, accent)

    # Footer
    foot_font = font("DejaVuSans.ttf", 18)
    footer = "Made for the make.fun bounty: news-image-20261122"
    fw = draw.textlength(footer, font=foot_font)
    draw.text(((W - fw) / 2, 982), footer, font=foot_font, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
