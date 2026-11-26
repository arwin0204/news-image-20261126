#!/usr/bin/env python3
"""Draw a one-page newspaper image summing up world news of
Thursday, 26 November 2026. Pure Pillow, default fonts only.
Output: news-26-nov-2026.png (1024x1024, <= 1 MiB)."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (27, 42, 74)          # navy
RED = (163, 22, 33)         # dark red
GREY = (90, 90, 90)
BORDER = (60, 60, 60)
WHITE = (255, 255, 255)

def font(size):
    return ImageFont.load_default(size=size)

def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_icon(draw, kind, cx, cy, color):
    """Small simple geometric icon centred at (cx, cy)."""
    if kind == "trade":  # bar chart
        for i, h in enumerate((14, 24, 34)):
            x0 = cx - 22 + i * 16
            draw.rectangle([x0, cy + 18 - h, x0 + 10, cy + 18], fill=color)
        draw.line([cx - 26, cy + 18, cx + 26, cy + 18], fill=color, width=3)
    elif kind == "energy":  # flame
        draw.polygon([(cx, cy - 24), (cx + 14, cy + 2), (cx + 6, cy + 18),
                      (cx - 6, cy + 18), (cx - 14, cy + 2)], fill=color)
        draw.ellipse([cx - 6, cy + 2, cx + 6, cy + 14], fill=PAPER)
    elif kind == "security":  # shield
        draw.polygon([(cx - 18, cy - 16), (cx + 18, cy - 16), (cx + 18, cy + 2),
                      (cx, cy + 22), (cx - 18, cy + 2)], outline=color, width=4)
    elif kind == "space":  # rocket
        draw.polygon([(cx, cy - 24), (cx + 10, cy + 2), (cx - 10, cy + 2)], fill=color)
        draw.rectangle([cx - 10, cy + 2, cx + 10, cy + 14], fill=color)
        draw.ellipse([cx - 4, cy + 4, cx + 4, cy + 12], fill=PAPER)
        draw.polygon([(cx - 4, cy + 14), (cx + 4, cy + 14), (cx, cy + 24)], fill=color)
    elif kind == "labour":  # factory
        draw.rectangle([cx - 22, cy - 2, cx + 22, cy + 18], fill=color)
        draw.polygon([(cx - 22, cy - 2), (cx - 12, cy - 14), (cx - 2, cy - 2),
                      (cx + 8, cy - 14), (cx + 18, cy - 2)], fill=color)
        draw.rectangle([cx + 12, cy - 20, cx + 18, cy - 2], fill=color)
    elif kind == "conflict":  # warning triangle
        draw.polygon([(cx, cy - 22), (cx + 22, cy + 16), (cx - 22, cy + 16)],
                     outline=color, width=4)
        draw.line([cx, cy - 8, cx, cy + 6], fill=color, width=4)
        draw.point([cx, cy + 12], fill=color)

STORIES = [
    ("TRADE", "US proposes new tariffs on 14 partners",
     "Washington targets factory overcapacity; China faces the "
     "highest rates, Taiwan up to 15%.",
     (163, 22, 33), "trade"),
    ("ENERGY", "Houthis claim Saudi refinery strike",
     "Brent crude tops $94 as Yemen's Houthis claim attacks on "
     "Ras Tanura and Riyadh.",
     (14, 124, 123), "energy"),
    ("SECURITY", "Kim calls for wider nuclear deployment",
     "North Korea's leader orders tactical nuclear weapons spread "
     "across more domains.",
     (91, 42, 134), "security"),
    ("SPACE", "First Pakistani astronaut reaches Tiangong",
     "Muhammad Zeeshan Ali joins China's Shenzhou-24 crew - the "
     "station's first foreign visitor.",
     (27, 42, 74), "space"),
    ("LABOUR", "Bangladesh garment workers win 36% pay rise",
     "Minimum wage lifted for entry-level garment workers after "
     "talks with the government.",
     (46, 125, 50), "labour"),
    ("CONFLICT", "Sudan drone strikes kill 19 civilians",
     "Strikes hit Blue Nile state as the war's toll on civilians "
     "keeps growing.",
     (183, 121, 31), "conflict"),
]

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = font(62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf, fill=INK)
    d.line([60, 104, W - 60, 104], fill=INK, width=3)
    d.line([60, 110, W - 60, 110], fill=INK, width=1)

    date = "Thursday, 26 November 2026"
    df = font(46)
    d.text(((W - d.textlength(date, font=df)) / 2, 122), date, font=df, fill=RED)

    sub = "World news in one image - six stories from six regions"
    sf = font(26)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 178), sub, font=sf, fill=GREY)
    d.line([60, 212, W - 60, 212], fill=INK, width=2)

    # ---- Story grid: 2 columns x 3 rows ----
    margin, gutter = 32, 20
    top, bottom = 228, 972
    bw = (W - 2 * margin - gutter) // 2
    bh = (bottom - top - 2 * gutter) // 3
    kf, hf, bf = font(25), font(32), font(24)

    for i, (kicker, headline, summary, color, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (bw + gutter)
        y0 = top + row * (bh + gutter)
        x1, y1 = x0 + bw, y0 + bh
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BORDER, width=2)
        d.rectangle([x0, y0, x1, y0 + 8], fill=color)
        d.text((x0 + 16, y0 + 20), kicker, font=kf, fill=color)
        draw_icon(d, icon, x1 - 36, y0 + 32, color)
        lines = wrap(d, headline, hf, bw - 32)[:3]
        y = y0 + 56
        for ln in lines:
            d.text((x0 + 16, y), ln, font=hf, fill=INK)
            y += 38
        slines = wrap(d, summary, bf, bw - 32)[:3]
        y += 6
        for ln in slines:
            d.text((x0 + 16, y), ln, font=bf, fill=(40, 40, 40))
            y += 29

    # ---- Footer ----
    foot = "Sources: Reuters and world news wires - 26 November 2026"
    ff = font(21)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 988), foot, font=ff, fill=GREY)

    img.save("news-26-nov-2026.png", optimize=True)
    print("saved news-26-nov-2026.png", img.size)

if __name__ == "__main__":
    main()
