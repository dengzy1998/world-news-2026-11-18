#!/usr/bin/env python3
"""Render the front page of THE WORLD TODAY for 18 November 2026.

Draws a 1024x1024 newspaper front page with Pillow and saves it as
entry.png in this directory. Every drawing call is deterministic: no
randomness, no timestamps, no network.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (31, 42, 68)
GREY = (90, 86, 76)
PANEL = (255, 253, 246)
SEA = (46, 98, 140)
GOLD = (201, 162, 39)
GREEN = (34, 139, 34)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = os.path.join(FONT_DIR, "NotoSerif-Black.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, max_size, max_width, max_lines):
    """Largest font size (down from max_size) whose wrap fits max_lines."""
    for size in range(max_size, 15, -1):
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(path, 16)
    return fnt, wrap(draw, text, fnt, max_width)


def centre(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def draw_flag(draw, x, y, w, h, kind):
    """A small flag on a pole at (x, y), w x h, kind in CN/US/RU."""
    draw.line([(x + w // 2, y), (x + w // 2, y - 34)], fill=INK, width=3)
    if kind == "CN":
        draw.rectangle([x, y - 34, x + w, y - 34 + h], fill=(222, 41, 16))
        draw.text((x + 4, y - 34 + 2), "\u2605", font=font(SANS_BOLD, 12),
                  fill=(255, 222, 0))
    elif kind == "US":
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
            draw.rectangle([x, y - 34 + i * h // 7, x + w,
                            y - 34 + (i + 1) * h // 7], fill=col)
        draw.rectangle([x, y - 34, x + w // 2, y - 34 + 4 * h // 7],
                       fill=(60, 59, 110))
    else:  # RU
        for i, col in enumerate([(255, 255, 255), (0, 57, 166),
                                (213, 0, 50)]):
            draw.rectangle([x, y - 34 + i * h // 3, x + w,
                            y - 34 + (i + 1) * h // 3], fill=col)
    draw.rectangle([x, y - 34, x + w, y - 34 + h], outline=INK, width=1)


def draw_bridge(draw, x, y, w, h):
    """Kerch bridge with a broken span: deck, towers, sea, smoke."""
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=SEA)
    for i in range(3):
        sx = x + 20 + i * 52
        draw.arc([sx, y + h - 66, sx + 44, y + h - 22], 180, 360,
                 fill=(255, 255, 255), width=3)
    # towers
    for tx in (x + 62, x + w - 82):
        draw.rectangle([tx, y + 22, tx + 16, y + h - 46], fill=(70, 70, 70))
    # deck in two pieces with a gap in the middle
    draw.rectangle([x, y + 78, x + w // 2 - 26, y + 92], fill=(40, 40, 40))
    draw.rectangle([x + w // 2 + 26, y + 78, x + w, y + 92], fill=(40, 40, 40))
    # cables
    for cx in range(x + 10, x + w // 2 - 30, 26):
        draw.line([(cx, y + 78), (x + 70, y + 26)], fill=GREY, width=2)
    for cx in range(x + w // 2 + 34, x + w - 6, 26):
        draw.line([(cx, y + 78), (x + w - 74, y + 26)], fill=GREY, width=2)
    # smoke from the gap
    for i, r in enumerate((16, 12, 9)):
        cx = x + w // 2 + (i - 1) * 8
        cy = y + 58 - i * 12
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # red burst marker
    draw.ellipse([x + w // 2 - 10, y + 66, x + w // 2 + 10, y + 86],
                 fill=RED)


def draw_gulf(draw, x, y, w, h):
    """Gulf at night: tanker on a dark sea, flames, missile streak."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=SEA)
    for i in range(3):
        sx = x + 16 + i * 58
        draw.arc([sx, y + h - 58, sx + 46, y + h - 18], 180, 360,
                 fill=(255, 255, 255), width=3)
    # hull
    draw.polygon([(x + 12, y + 96), (x + w - 12, y + 96),
                  (x + w - 34, y + 128), (x + 34, y + 128)], fill=(32, 32, 40))
    draw.rectangle([x + 12, y + 88, x + w - 12, y + 96], fill=(178, 34, 34))
    # containers
    for i, col in enumerate([(201, 162, 39), (46, 98, 140), (201, 162, 39)]):
        draw.rectangle([x + 40 + i * 52, y + 58, x + 82 + i * 52, y + 88],
                       fill=col, outline=INK, width=1)
    # flames on deck
    for fx, fh in ((x + 56, 30), (x + 82, 40), (x + 108, 26)):
        draw.polygon([(fx - 12, y + 58), (fx, y + 58 - fh),
                      (fx + 12, y + 58)], fill=(255, 120, 0))
        draw.polygon([(fx - 7, y + 58), (fx, y + 58 - fh + 12),
                      (fx + 7, y + 58)], fill=(255, 210, 0))
    # missile streak top right with burst
    draw.line([(x + w - 90, y + 18), (x + w - 34, y + 44)], fill=GOLD, width=4)
    draw.ellipse([x + w - 44, y + 34, x + w - 14, y + 64], fill=(255, 120, 0))
    draw.ellipse([x + w - 36, y + 42, x + w - 22, y + 56], fill=(255, 210, 0))


def draw_summit(draw, x, y, w, h):
    """Three flags (China, US, Russia) behind a summit table."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d_table = y + h - 34
    draw.rectangle([x + 8, d_table, x + w - 8, d_table + 10], fill=(120, 72, 32))
    draw.rectangle([x + 8, d_table + 10, x + w - 8, d_table + 14],
                   fill=(90, 54, 24))
    for i, kind in enumerate(("CN", "US", "RU")):
        draw_flag(draw, x + 24 + i * 66, d_table, 46, 28, kind)
    # three chairs behind the table
    for cx in (x + 47, x + 113, x + 179):
        draw.rectangle([cx - 16, d_table - 2, cx + 16, d_table + 2],
                       fill=(70, 70, 70))


def draw_virus(draw, x, y, r, col):
    """Spiky virus circle."""
    for ang in range(0, 360, 30):
        import math
        rad = math.radians(ang)
        x1 = x + int(r * 0.9 * math.cos(rad))
        y1 = y + int(r * 0.9 * math.sin(rad))
        x2 = x + int(r * 1.35 * math.cos(rad))
        y2 = y + int(r * 1.35 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=col, width=3)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=col)


def draw_clinic(draw, x, y, w, h):
    """Clinic building with a red cross, plus measles virus circles."""
    draw.rectangle([x, y, x + w, y + h], fill=(235, 240, 244))
    # building
    draw.rectangle([x + 18, y + 52, x + w - 18, y + h - 8],
                   fill=(255, 255, 255), outline=INK, width=2)
    draw.rectangle([x + 18, y + 52, x + w - 18, y + 76], fill=NAVY)
    # red cross sign
    cx, cy = x + w // 2, y + 34
    draw.rectangle([cx - 5, cy - 12, cx + 5, cy + 12], fill=RED)
    draw.rectangle([cx - 12, cy - 5, cx + 12, cy + 5], fill=RED)
    # windows
    for i in range(3):
        draw.rectangle([x + 34 + i * 52, y + 92, x + 62 + i * 52, y + 116],
                       fill=(180, 205, 225), outline=INK, width=1)
    # door
    draw.rectangle([x + w // 2 - 16, y + h - 40, x + w // 2 + 16, y + h - 8],
                   fill=(60, 60, 60))
    # virus circles
    draw_virus(draw, x + 34, y + 26, 12, RED)
    draw_virus(draw, x + w - 34, y + 26, 9, RED)


def draw_chip(draw, x, y, w, h):
    """AI chip over a market chart: red fall, green rebound arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 36))
    # chart line: fall then rebound
    pts = [(x + 12, y + 30), (x + 60, y + 52), (x + 108, y + 44),
           (x + 156, y + 78), (x + 204, y + 62)]
    draw.line(pts, fill=(255, 80, 80), width=4, joint="curve")
    draw.polygon([(x + 204, y + 62), (x + 188, y + 58), (x + 200, y + 76)],
                 fill=GREEN)
    draw.line([(x + 150, y + 88), (x + 212, y + 88)], fill=GREEN, width=3)
    draw.polygon([(x + 212, y + 88), (x + 198, y + 82), (x + 198, y + 94)],
                 fill=GREEN)
    # chip
    cx, cy, s = x + w // 2 - 26, y + h - 62, 52
    for i in range(4):
        draw.line([(cx + 8 + i * 12, cy - 8), (cx + 8 + i * 12, cy)],
                  fill=GOLD, width=3)
        draw.line([(cx + 8 + i * 12, cy + s), (cx + 8 + i * 12, cy + s + 8)],
                  fill=GOLD, width=3)
    draw.rectangle([cx, cy, cx + s, cy + s], fill=(60, 90, 60),
                   outline=GOLD, width=2)
    draw.rectangle([cx + 14, cy + 14, cx + s - 14, cy + s - 14],
                   fill=(40, 60, 40), outline=GOLD, width=1)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer double border
    d.rectangle([22, 22, W - 22, H - 22], outline=INK, width=3)
    d.rectangle([30, 30, W - 30, H - 30], outline=INK, width=1)

    # kicker
    y = 48
    y = centre(d, y, "THE DAY IN ONE PICTURE", font(SANS_BOLD, 21), RED)
    # masthead
    y = 76
    centre(d, y, "THE WORLD TODAY", font(SERIF_BLACK, 88), INK)
    # rules + dateline
    d.rectangle([52, 168, W - 52, 174], fill=INK)
    d.rectangle([52, 180, W - 52, 182], fill=INK)
    centre(d, 190, "WEDNESDAY  \u00b7  18 NOVEMBER 2026",
           font(SERIF_BOLD, 27), INK)

    # ---- lead panel: Crimea bridge ----
    d.rectangle([36, 232, W - 36, 512], fill=PANEL, outline=INK, width=2)
    draw_bridge(d, 52, 242, 920, 104)
    fnt, lines = fit_lines(d, "UKRAINE KNOCKS OUT CRIMEA BRIDGE",
                           SERIF_BLACK, 44, 940, 2)
    ly = 360
    for line in lines:
        ly = centre(d, ly, line, fnt, INK)
        ly += 4
    fnt = font(SERIF, 21)
    sub = ("Road arch falls into the Kerch Strait, two days before "
           "the Trump\u2013Xi\u2013Putin summit.")
    centre(d, ly + 8, sub, fnt, INK)

    # ---- four columns ----
    cols = [
        ("GULF STRIKES ESCALATE",
         "US jets hit a missile site on Iran's Qeshm Island; Iran fires "
         "drones at Bahrain and Kuwait.", draw_gulf),
        ("TRUMP FLIES TO CHINA",
         "First-ever trilateral with Xi and Putin set for Thursday "
         "in Shenzhen.", draw_summit),
        ("US LOSES MEASLES-FREE STATUS",
         "More than 5,400 cases this year, the worst outbreak in "
         "over 30 years.", draw_clinic),
        ("NVIDIA BEATS, MARKETS FALL",
         "Shares jump 4% after hours on strong sales; the S&P 500 "
         "falls 1% ahead of results.", draw_chip),
    ]
    col_w, gap, top = 224, 18, 536
    for i, (head, cap, draw_fn) in enumerate(cols):
        x = 36 + i * (col_w + gap)
        d.rectangle([x, top, x + col_w, top + 3], fill=RED)
        draw_fn(d, x, top + 14, col_w, 138)
        fnt, lines = fit_lines(d, head, SERIF_BOLD, 24, col_w, 3)
        hy = top + 166
        for line in lines:
            d.text((x, hy), line, font=fnt, fill=INK)
            hy += fnt.size + 2
        fnt = font(SERIF, 17)
        for line in wrap(d, cap, fnt, col_w):
            d.text((x, hy + 6), line, font=fnt, fill=INK)
            hy += 23

    # ---- ticker ----
    d.rectangle([36, 912, W - 36, 964], fill=NAVY)
    tick = ("CYCLONE XAVIER, CAT 5, HITS COOK ISLANDS    \u2022    "
            "EBOLA CASES PASS 11,000 IN DR CONGO    \u2022    "
            "MAGNITUDE 6 QUAKE IN PAPUA NEW GUINEA")
    fnt = font(SANS_BOLD, 19)
    while d.textlength(tick, font=fnt) > 940 and fnt.size > 12:
        fnt = font(SANS_BOLD, fnt.size - 1)
    tw = d.textlength(tick, font=fnt)
    d.text(((W - tw) / 2, 930), tick, font=fnt, fill=(255, 255, 255))

    # footer
    centre(d, 972, "Wire reports  \u00b7  18 November 2026",
           font(SERIF, 14), GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print(f"saved {out} {img.size}")


if __name__ == "__main__":
    render()
