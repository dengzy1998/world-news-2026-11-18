"""Draw a newspaper front page summing up world news on 18 November 2026.

Everything on the page is drawn from scratch with Pillow primitives:
no photographs, no external images, no network access at run time.
The output is fully deterministic: running this module twice produces
byte-identical PNG files.
"""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

PAPER = (246, 241, 227)      # warm newsprint cream
INK = (18, 18, 18)           # near-black ink
RED = (178, 34, 34)          # headline accent red
BLUE = (31, 78, 121)         # deep news blue
SKY = (178, 210, 232)
SEA = (64, 116, 158)
SEA_DARK = (38, 84, 122)
GREEN = (34, 120, 62)
GOLD = (198, 148, 42)
GREY = (110, 110, 105)
LIGHT_GREY = (210, 205, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: _font("DejaVuSerif-Bold.ttf", s)     # noqa: E731
SANS_BOLD = lambda s: _font("DejaVuSans-Bold.ttf", s)       # noqa: E731
SANS = lambda s: _font("DejaVuSans.ttf", s)                 # noqa: E731
SERIF = lambda s: _font("DejaVuSerif.ttf", s)               # noqa: E731


def wrap(draw, text, font, max_width):
    """Split text into lines that fit inside max_width pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def centred(draw, cx, y, text, font, fill=INK):
    """Draw text centred horizontally on cx at height y."""
    width = draw.textlength(text, font=font)
    draw.text((cx - width / 2, y), text, font=font, fill=fill)
    return y + font.size


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel_frame(draw, box, fill=(255, 255, 255)):
    """A bordered panel box; returns the inner rectangle."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=INK, width=2)
    return (x0 + 2, y0 + 2, x1 - 2, y1 - 2)


def tag(draw, x, y, text, fill=RED):
    """Small white-on-colour section label; returns the y below it."""
    font = SANS_BOLD(15)
    w = draw.textlength(text, font=font) + 14
    draw.rectangle([x, y, x + w, y + 21], fill=fill)
    draw.text((x + 7, y + 2), text, font=font, fill=(255, 255, 255))
    return y + 21


# ---------------------------------------------------------------------------
# Illustrations. Each draws one small scene inside the given box.
# All coordinates are relative to the box, so every picture is simple
# geometry: rectangles, ellipses, polygons, arcs and lines.
# ---------------------------------------------------------------------------


def draw_bridge(draw, box):
    """The Kerch Bridge: a road deck broken in the middle, arch in the sea."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y0 + int(h * 0.58)], fill=SKY)
    draw.rectangle([x0, y0 + int(h * 0.58), x1, y1], fill=SEA)
    # sun
    draw.ellipse([x0 + w - 66, y0 + 12, x0 + w - 26, y0 + 52],
                 fill=(240, 200, 90))
    # far shore
    draw.polygon([(x0, y0 + int(h * 0.58)), (x0 + w, y0 + int(h * 0.58)),
                  (x0 + w, y0 + int(h * 0.5)), (x0, y0 + int(h * 0.52))],
                 fill=(120, 140, 110))
    deck_y = y0 + int(h * 0.42)
    # pillars
    for px in (0.10, 0.30, 0.72, 0.90):
        px0 = x0 + int(w * px)
        draw.rectangle([px0, deck_y, px0 + 8, y0 + h], fill=(90, 90, 88))
    # deck: left span, gap, right span
    gap0 = x0 + int(w * 0.44)
    gap1 = x0 + int(w * 0.62)
    draw.rectangle([x0, deck_y, gap0, deck_y + 10], fill=(52, 52, 50))
    draw.rectangle([gap1, deck_y, x1, deck_y + 10], fill=(52, 52, 50))
    # standing arch over the left span
    draw.arc([x0 + int(w * 0.12), deck_y - 46, x0 + int(w * 0.40),
              deck_y + 26], start=180, end=360, fill=RED, width=6)
    # fallen arch, tilted, half sunk in the strait
    draw.arc([gap0 - 6, deck_y + 2, gap1 + 34, deck_y + 64],
             start=200, end=340, fill=RED, width=6)
    draw.line([(gap0 + 4, deck_y + 10), (gap0 + 40, deck_y + 52)],
              fill=RED, width=5)
    # broken deck edge
    draw.polygon([(gap0, deck_y + 10), (gap0 + 14, deck_y + 10),
                  (gap0 + 6, deck_y + 30)], fill=(52, 52, 50))
    draw.polygon([(gap1, deck_y + 10), (gap1 - 12, deck_y + 10),
                  (gap1 - 4, deck_y + 28)], fill=(52, 52, 50))
    # smoke from the gap
    for cx, cy, r in ((0.50, 0.30, 13), (0.55, 0.22, 17), (0.47, 0.18, 11)):
        draw.ellipse([x0 + int(w * cx) - r, y0 + int(h * cy) - r,
                      x0 + int(w * cx) + r, y0 + int(h * cy) + r],
                     fill=(150, 150, 148))
    # waves around the wreck
    for wy in (0.72, 0.82, 0.92):
        yy = y0 + int(h * wy)
        for kx in range(0, 7):
            kx0 = x0 + int(w * (0.06 + kx * 0.14))
            draw.arc([kx0, yy, kx0 + 26, yy + 10], start=180, end=360,
                     fill=(220, 230, 238), width=2)


def draw_gulf(draw, box):
    """Qeshm Island in the Strait of Hormuz: a blast, a jet, a radar dish."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(24, 38, 58))
    # stars
    for sx, sy in ((0.12, 0.15), (0.30, 0.08), (0.55, 0.18), (0.82, 0.10),
                   (0.92, 0.30), (0.07, 0.42)):
        draw.ellipse([x0 + int(w * sx), y0 + int(h * sy),
                      x0 + int(w * sx) + 3, y0 + int(h * sy) + 3],
                     fill=(255, 255, 255))
    # sea
    draw.rectangle([x0, y0 + int(h * 0.62), x1, y1], fill=SEA_DARK)
    # island silhouette
    draw.polygon([(x0 + int(w * 0.18), y0 + int(h * 0.62)),
                  (x0 + int(w * 0.38), y0 + int(h * 0.44)),
                  (x0 + int(w * 0.62), y0 + int(h * 0.48)),
                  (x0 + int(w * 0.82), y0 + int(h * 0.62))],
                 fill=(74, 92, 66))
    # explosion starburst over the island
    ex, ey = x0 + int(w * 0.50), y0 + int(h * 0.38)
    for dx, dy in ((-26, -14), (-8, -30), (12, -26), (28, -8), (30, 12),
                   (10, 26), (-12, 24), (-30, 6)):
        draw.line([(ex, ey), (ex + dx, ey + dy)], fill=(250, 190, 60),
                  width=4)
    draw.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(250, 220, 120))
    # jet silhouette
    jx, jy = x0 + int(w * 0.78), y0 + int(h * 0.16)
    draw.polygon([(jx, jy), (jx + 26, jy + 6), (jx, jy + 10),
                  (jx + 4, jy + 5)], fill=(200, 200, 200))
    draw.line([(jx, jy + 5), (jx - 16, jy + 5)], fill=(250, 190, 60),
              width=3)
    # radar dish on a small base
    rx, ry = x0 + int(w * 0.14), y0 + int(h * 0.50)
    draw.arc([rx - 16, ry - 16, rx + 16, ry + 16], start=200, end=340,
             fill=(220, 220, 220), width=4)
    draw.line([(rx, ry), (rx - 6, ry + 18)], fill=(220, 220, 220), width=3)
    # three small drones heading right
    for k in range(3):
        dx = x0 + int(w * (0.60 + k * 0.07))
        dy = y0 + int(h * (0.66 + k * 0.06))
        draw.ellipse([dx, dy, dx + 7, dy + 4], fill=(230, 230, 230))


def draw_summit(draw, box):
    """Three flags above a table: the Shenzhen trilateral."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(232, 226, 208))
    flag_w = int(w * 0.24)
    flag_h = int(h * 0.42)
    fy = y0 + int(h * 0.10)
    # United States: stripes and blue canton
    ux = x0 + int(w * 0.07)
    for s in range(7):
        colour = (178, 34, 52) if s % 2 == 0 else (255, 255, 255)
        draw.rectangle([ux, fy + s * flag_h // 7, ux + flag_w,
                        fy + (s + 1) * flag_h // 7], fill=colour)
    draw.rectangle([ux, fy, ux + flag_w // 2, fy + flag_h // 2],
                   fill=(40, 60, 120))
    # China: red field, one large gold star
    cx = x0 + int(w * 0.38)
    draw.rectangle([cx, fy, cx + flag_w, fy + flag_h], fill=(222, 41, 16))
    draw.ellipse([cx + 10, fy + 8, cx + 26, fy + 24], fill=GOLD)
    # Russia: white, blue, red tricolour
    rx = x0 + int(w * 0.69)
    for s, colour in enumerate(((255, 255, 255), (0, 57, 166),
                               (213, 0, 50))):
        draw.rectangle([rx, fy + s * flag_h // 3, rx + flag_w,
                        fy + (s + 1) * flag_h // 3], fill=colour)
    # table and three chairs
    ty = y0 + int(h * 0.74)
    draw.rectangle([x0 + int(w * 0.08), ty, x1 - int(w * 0.08),
                    ty + 8], fill=(120, 72, 30))
    for lx in (0.12, 0.88):
        draw.rectangle([x0 + int(w * lx), ty + 8, x0 + int(w * lx) + 6,
                        y1 - 4], fill=(90, 54, 22))
    for cxp in (0.18, 0.50, 0.82):
        px = x0 + int(w * cxp)
        draw.ellipse([px - 9, ty - 30, px + 9, ty - 12], fill=(52, 52, 50))
        draw.rectangle([px - 7, ty - 12, px + 7, ty], fill=(52, 52, 50))


def draw_measles(draw, box):
    """Spiky virus balls over a rising case chart."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(250, 238, 232))
    # virus: red disc with spikes
    for vx, vy, r in ((0.24, 0.30, 20), (0.70, 0.24, 15)):
        cx, cy = x0 + int(w * vx), y0 + int(h * vy)
        for k in range(10):
            ang = k * 36
            import math
            dx = int((r + 8) * math.cos(math.radians(ang)))
            dy = int((r + 8) * math.sin(math.radians(ang)))
            draw.line([(cx, cy), (cx + dx, cy + dy)], fill=RED, width=3)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        draw.ellipse([cx - r // 2, cy - r // 2, cx - r // 4, cy - r // 4],
                     fill=(255, 150, 140))
    # bar chart of cases, rising steeply
    base = y0 + int(h * 0.88)
    for k, bh in enumerate((0.12, 0.20, 0.30, 0.44)):
        bx = x0 + int(w * (0.14 + k * 0.20))
        bw = int(w * 0.12)
        draw.rectangle([bx, base - int(h * bh), bx + bw, base],
                       fill=RED if k == 3 else (200, 90, 80))
    draw.line([(x0 + int(w * 0.08), base), (x1 - int(w * 0.08), base)],
              fill=INK, width=2)


def draw_nvidia(draw, box):
    """A green chip and a steeply rising revenue chart."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(232, 244, 232))
    # chip
    cx0, cy0 = x0 + int(w * 0.10), y0 + int(h * 0.14)
    cx1, cy1 = x0 + int(w * 0.46), y0 + int(h * 0.62)
    for k in range(4):
        px = cx0 + 8 + k * (cx1 - cx0 - 16) // 3
        draw.line([(px, cy0 - 10), (px, cy0)], fill=GREEN, width=3)
        draw.line([(px, cy1), (px, cy1 + 10)], fill=GREEN, width=3)
    draw.rectangle([cx0, cy0, cx1, cy1], fill=(22, 110, 52))
    draw.rectangle([cx0 + 12, cy0 + 12, cx1 - 12, cy1 - 12],
                   outline=(160, 220, 170), width=2)
    # rising bars
    base = y0 + int(h * 0.90)
    for k, bh in enumerate((0.16, 0.30, 0.52, 0.72)):
        bx = x0 + int(w * (0.54 + k * 0.11))
        bw = int(w * 0.07)
        draw.rectangle([bx, base - int(h * bh), bx + bw, base],
                       fill=GREEN if k < 3 else (16, 150, 70))
    # arrow over the bars
    ax0, ay0 = x0 + int(w * 0.55), y0 + int(h * 0.62)
    ax1, ay1 = x0 + int(w * 0.94), y0 + int(h * 0.16)
    draw.line([(ax0, ay0), (ax1, ay1)], fill=INK, width=4)
    draw.polygon([(ax1, ay1), (ax1 - 12, ay1 + 2), (ax1 - 2, ay1 + 12)],
                 fill=INK)


def draw_cyclone(draw, box):
    """A spiral storm over a small island."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(226, 238, 244))
    import math
    cx, cy = x0 + int(w * 0.50), y0 + int(h * 0.46)
    # spiral arms
    for arm in range(3):
        points = []
        for t in range(0, 121):
            ang = math.radians(t * 3 + arm * 120)
            r = 4 + t * 0.42
            points.append((cx + int(r * math.cos(ang)),
                           cy + int(r * math.sin(ang))))
        draw.line(points, fill=(40, 90, 140), width=5)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255),
                 outline=(40, 90, 140), width=2)
    # island below the storm
    iy = y0 + int(h * 0.86)
    draw.polygon([(x0 + int(w * 0.30), iy), (x0 + int(w * 0.44), iy - 14),
                  (x0 + int(w * 0.58), iy - 10), (x0 + int(w * 0.72), iy)],
                 fill=(74, 120, 80))
    draw.rectangle([x0, iy, x1, y1], fill=SEA)
    # rain streaks
    for k in range(6):
        rx = x0 + int(w * (0.10 + k * 0.15))
        draw.line([(rx, y0 + int(h * 0.68)), (rx - 6, y0 + int(h * 0.80))],
                  fill=(120, 160, 190), width=2)


def draw_ebola(draw, box):
    """A clinic cross and a steep outbreak curve."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(243, 236, 224))
    # clinic tent
    tx0, ty0 = x0 + int(w * 0.08), y0 + int(h * 0.52)
    tx1, ty1 = x0 + int(w * 0.44), y0 + int(h * 0.88)
    draw.polygon([(tx0, ty1), (tx0, ty0 + 18), ((tx0 + tx1) // 2, ty0),
                  (tx1, ty0 + 18), (tx1, ty1)], fill=(240, 240, 235),
                 outline=INK)
    draw.rectangle([tx0 + 8, ty0 + 26, tx0 + 26, ty0 + 32], fill=RED)
    draw.rectangle([tx0 + 14, ty0 + 20, tx0 + 20, ty0 + 38], fill=RED)
    # outbreak curve, rising steeply
    import math
    points = []
    for t in range(0, 101):
        px = x0 + int(w * (0.52 + t * 0.0044))
        py = y0 + int(h * 0.82) - int(h * 0.55 * (t / 100.0) ** 2)
        points.append((px, py))
    draw.line(points, fill=RED, width=4)
    draw.ellipse([points[-1][0] - 5, points[-1][1] - 5,
                  points[-1][0] + 5, points[-1][1] + 5], fill=RED)
    # small case dots along the curve
    for t in (20, 45, 70):
        px = x0 + int(w * (0.52 + t * 0.0044))
        py = y0 + int(h * 0.82) - int(h * 0.55 * (t / 100.0) ** 2)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)


def draw_quake(draw, box):
    """A seismograph trace with a sharp spike."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(235, 232, 222))
    mid = y0 + h // 2
    pts = [(x0 + 6, mid)]
    import math
    for t in range(1, 40):
        px = x0 + 6 + int(t * (w - 12) / 40)
        amp = 2 if t < 18 else (26 if 18 <= t < 24 else 4)
        py = mid + int(amp * math.sin(t * 2.4))
        pts.append((px, py))
    draw.line(pts, fill=INK, width=2)
    # white badge behind the magnitude so the trace never crosses the text
    bx, by = x0 + w // 2, mid
    draw.ellipse([bx - 17, by - 15, bx + 17, by + 15], fill=(255, 255, 255),
                 outline=RED, width=2)
    draw.text((bx - 11, by - 10), "6.0", font=SANS_BOLD(18), fill=RED)


def draw_dome(draw, box):
    """The US Capitol dome, simplified, for the Senate result."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(232, 236, 240))
    cx = x0 + w // 2
    base = y0 + int(h * 0.88)
    # dome
    draw.pieslice([cx - 34, y0 + int(h * 0.10), cx + 34, y0 + int(h * 0.62)],
                  start=180, end=360, fill=(245, 245, 240), outline=INK)
    draw.rectangle([cx - 3, y0 + int(h * 0.02), cx + 3, y0 + int(h * 0.12)],
                   fill=INK)
    # drum and columns
    draw.rectangle([cx - 38, y0 + int(h * 0.60), cx + 38, base], fill=(245, 245, 240),
                   outline=INK)
    for k in range(5):
        kx = cx - 30 + k * 15
        draw.line([(kx, y0 + int(h * 0.64)), (kx, base)], fill=INK, width=2)
    draw.rectangle([x0 + int(w * 0.10), base, x1 - int(w * 0.10), base + 4],
                   fill=INK)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def story_panel(draw, box, tag_text, headline, body, art):
    """One grid panel: picture on top, headline and two body lines below."""
    x0, y0, x1, y1 = box
    panel_frame(draw, box)
    art_h = int((y1 - y0) * 0.40)
    art(draw, (x0 + 2, y0 + 2, x1 - 2, y0 + 2 + art_h))
    tx = x0 + 10
    ty = y0 + 2 + art_h + 6
    ty = tag(draw, tx, ty, tag_text) + 5
    head_font = SANS_BOLD(18)
    max_w = x1 - x0 - 20
    for line in wrap(draw, headline, head_font, max_w)[:2]:
        draw.text((tx, ty), line, font=head_font, fill=INK)
        ty += 21
    body_font = SANS(13)
    for line in wrap(draw, body, body_font, max_w)[:2]:
        draw.text((tx, ty), line, font=body_font, fill=(60, 60, 60))
        ty += 15


def build_image(path):
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    m = 26                      # page margin
    cx = WIDTH // 2
    right = WIDTH - m

    # ---- masthead ------------------------------------------------------
    centred(draw, cx, 24, "THE WORLD TODAY", SERIF_BOLD(64))
    rule(draw, m, right, 108, width=3)
    centred(draw, cx, 118, "WEDNESDAY 18 NOVEMBER 2026",
            SANS_BOLD(27), fill=RED)
    centred(draw, cx, 150,
            "ONE DAY IN PICTURES  \u2022  FROM CRIMEA TO THE COOK ISLANDS",
            SANS(15), fill=(80, 80, 78))
    rule(draw, m, right, 176, width=2)

    # ---- lead story: Kerch Bridge --------------------------------------
    lead = (m, 186, right, 436)
    panel_frame(draw, lead)
    draw_bridge(draw, (m + 2, 188, right - 2, 312))
    tag(draw, m + 12, 320, "LEAD STORY  \u2022  UKRAINE")
    draw.text((m + 12, 348), "KERCH BRIDGE FALLS INTO THE STRAIT",
              font=SANS_BOLD(30), fill=INK)
    deck = ("Ukraine says drones and missiles brought down a road arch of "
            "Russia's 19 km link to Crimea \u2014 the second strike in two days.")
    deck_font = SERIF(18)
    ty = 388
    for line in wrap(draw, deck, deck_font, right - m - 24):
        draw.text((m + 12, ty), line, font=deck_font, fill=(50, 50, 50))
        ty += 21

    # ---- grid of six stories -------------------------------------------
    cols = [(m, 336), (357, 667), (688, right)]
    rows = [(448, 658), (670, 880)]
    stories = [
        ("GULF ON EDGE", "US HITS IRAN, DRONES FLY BACK",
         "US jets hit an IRGC site on Qeshm; Iran hit back with drones "
         "at Bahrain and Kuwait.", draw_gulf),
        ("SHENZHEN SUMMIT", "THREE LEADERS, ONE TABLE",
         "Trump, Xi and Putin meet Thursday; Ukraine and trade top "
         "the agenda.", draw_summit),
        ("HEALTH", "US LOSES MEASLES-FREE STATUS",
         "Over 5,400 cases this year, the worst in decades, ends "
         "26 years of elimination.", draw_measles),
        ("MARKETS", "NVIDIA DOUBLES ITS REVENUE",
         "Q3 sales hit $115.8bn, up 103%, in the first results since "
         "Jensen Huang stepped down.", draw_nvidia),
        ("WEATHER", "CYCLONE XAVIER HITS CAT 5",
         "Winds of 220 km/h batter the Northern Cook Islands; gusts "
         "reach 315 km/h.", draw_cyclone),
        ("AFRICA", "EBOLA OUTBREAK SURGES IN DRC",
         "Cases more than doubled in three months to 11,000, with "
         "5,400 deaths, the UN says.", draw_ebola),
    ]
    for (y0, y1), row in zip(rows, (stories[:3], stories[3:])):
        for (x0, x1), (tag_text, headline, body, art) in zip(cols, row):
            story_panel(draw, (x0, y0, x1, y1), tag_text, headline,
                        body, art)

    # ---- bottom strip: two short items ----------------------------------
    strip_y0, strip_y1 = 892, 962
    panel_frame(draw, (m, strip_y0, right, strip_y1))
    half = (m + right) // 2
    draw.line([(half, strip_y0 + 6), (half, strip_y1 - 6)], fill=GREY,
              width=1)
    # quake, left half
    draw_quake(draw, (m + 8, strip_y0 + 6, m + 128, strip_y1 - 6))
    qfont = SANS_BOLD(17)
    draw.text((m + 138, strip_y0 + 10), "QUAKE SHAKES PAPUA NEW GUINEA",
              font=qfont, fill=INK)
    qbody = ("A shallow magnitude 6.0 quake at 10 km depth, GFZ reports. "
             "No casualties reported yet.")
    qbf = SANS(14)
    ty = strip_y0 + 34
    for line in wrap(draw, qbody, qbf, half - m - 150):
        draw.text((m + 138, ty), line, font=qbf, fill=(60, 60, 60))
        ty += 18
    # senate, right half
    draw_dome(draw, (half + 8, strip_y0 + 6, half + 128, strip_y1 - 6))
    draw.text((half + 138, strip_y0 + 10), "DEMOCRATS TAKE 56 SENATE SEATS",
              font=qfont, fill=INK)
    sbody = ("Mary Peltola wins Alaska's Senate seat, giving Democrats "
             "a 56-seat majority in the chamber.")
    ty = strip_y0 + 34
    for line in wrap(draw, sbody, qbf, right - half - 150):
        draw.text((half + 138, ty), line, font=qbf, fill=(60, 60, 60))
        ty += 18

    # ---- footer ---------------------------------------------------------
    centred(draw, cx, 972,
            "All pictures drawn in code  \u2022  Sources: AP, Reuters, "
            "Al Jazeera, NDTV, Fiji MetService, United Nations",
            SANS(13), fill=(90, 90, 88))

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    build_image(os.path.join(here, "entry.png"))
    print("entry.png written")
