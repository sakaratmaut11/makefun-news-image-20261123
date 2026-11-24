#!/usr/bin/env python3
"""THE DAY'S RECORD - NI23 G3 compose script for akun17 (@sakaratmaut8193).

Draws a one-page newspaper front page for Monday 23 November 2026 with PIL.
Lead story: pool #46 - the FBI investigates a suspected hack of its main
criminal-justice database (AP wire, 23 Nov 2026). Trio chosen by this
builder: #46 (lead) + #1 Hormuz tankers burning + #43 Democrats take the
US House 258-173. All facts and figures come only from ni23-pool.md.
The dotted_map below is an original hand-plotted dot grid, pins numbered
by card; the legend marks every region colour.

Usage: python3 compose.py <variant A|B|C> <output.png>
Local-only tool; the submitted program is main.py (stdlib copy-only).
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
PLAY_BLACK = FONT_DIR + "PlayfairDisplay-Black.ttf"
PLAY_BOLD = FONT_DIR + "PlayfairDisplay-Bold.ttf"
ARCH = FONT_DIR + "Archivo.ttf"
ARCH_B = FONT_DIR + "Archivo-Bold.ttf"

W = H = 1024

REGION_COLORS = {
    "N. AMERICA": (49, 89, 127),
    "MIDDLE EAST": (168, 91, 31),
    "EUROPE": (79, 112, 56),
    "SOUTH ASIA": (122, 78, 140),
    "SE ASIA": (46, 122, 114),
    "AFRICA": (140, 59, 46),
    "ASIA-PACIFIC": (107, 122, 42),
    "GLOBAL": (85, 80, 73),
}

NUMS = [
    ("258-173", "US HOUSE RESULT"),
    ("720/9d", "INDIA AT WELLINGTON"),
    ("7 + 50", "FOUND / MISSING, INDONESIA"),
    ("14", "MISSING IN KYIV"),
    ("$3,538", "GOLD, PER OUNCE"),
    ("Rs 28,000 cr", "TATA STEEL PIPE SALE"),
]

TL = [
    ("00:02", "UN lethal-AI talks"),
    ("01:00", "Kyiv boy freed"),
    ("02:00", "Sydney on COP31"),
    ("AM", "India 720/9d Wellington"),
    ("NOON", "COP31 closes, no deal"),
    ("PM", "FBI hack probe"),
]

BRIEFS = [
    "IRGC claims 2 Patriot radars",
    "Houthi missile downed by Saudi",
    "UN talks on lethal AI weapons",
    "US releases UFO footage anew",
    "Albanese: COP31 flop verdict",
    "Ship towed off Finland coast",
    "Blast hits ship in Benghazi",
    "UK-EU reset a 'landmark'",
    "Myanmar junta slams ASEAN",
    "Nepal's Shah meets PM Modi",
    "Guru Nanak Jayanti in India",
    "Indonesia: 7 found, 50 lost",
    "India chase Wellington win",
    "India win ODI series 3-2",
    "Anupama defends IBSF crown",
    "World Chess Championship live",
    "Kota bus tragedy: 9 dead",
    "SpiceJet plea; IndiGo 65.9%",
    "BRICS roundtable at IFFI Goa",
    "AI centre opens at IIT Patna",
    "Rs 4,000 cr Arunachal push",
    "JEE Main registration closes",
    "Google $5m for IIT AI study",
    "Trump attacks Schumer",
    "Miley Cyrus marries Morando",
    "Ewing joins Mets for $95m",
]

dc = ("Xi-Trump-Putin summit, 19 Nov 2026 · "
      "SpiceJet Rs 5,500 cr raise, 18 Nov · "
      "Paolo Bulgari dies, rep. 22 Nov · "
      "24 killed, South Sudan, 22 Nov · "
      "Bolsonaro in ICU, 22 Nov 2026 · "
      "Korea edu minister quits, 22 Nov · "
      "Indonesia fire as event, 22 Nov")

MAP_ROWS = [
    "                                              ",
    "        ####                                  ",
    "     #########      ##   #############        ",
    "    ###########    #### #################     ",
    "     #########      ########################  ",
    "      #######        #####################    ",
    "       #####  ##      #################       ",
    "        ###  ####      ###############   ##   ",
    "             ######     #############  ####   ",
    "            ########     ###########  ######  ",
    "            ########      #########    ####   ",
    "             ######        #######      ##    ",
    "             #####          #####       ##    ",
    "              ###           ####              ",
    "              ##            ###         ##    ",
    "                                    ######    ",
    "                                   ########   ",
    "                                    ####      ",
]

PINS = {
    1: (29, 7), 2: (9, 4), 3: (11, 5), 4: (43, 16), 5: (25, 3),
    6: (26, 4), 7: (27, 5), 8: (23, 2), 9: (31, 8), 10: (34, 9),
    11: (19, 5), 12: (6, 9), 13: (21, 4),
}


def fb(n):
    return ImageFont.truetype(ARCH_B, n)


def fr(n):
    return ImageFont.truetype(ARCH, n)


def fsr(n):
    return ImageFont.truetype(ARCH, n)


def fp(path, n):
    return ImageFont.truetype(path, n)


def fit(path, text, size, max_w, min_size=10):
    s = size
    while s > min_size:
        f = fp(path, s)
        if f.getlength(text) <= max_w:
            return f
        s -= 1
    return fp(path, min_size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def icon(d, name, x, y, s, ink, accent):
    """Tiny pictogram drawn with plain PIL shapes inside an s-by-s box."""
    if name == "flame":
        d.polygon([(x + s * .5, y), (x + s * .85, y + s * .55),
                   (x + s * .7, y + s), (x + s * .3, y + s),
                   (x + s * .15, y + s * .55)], outline=accent, width=2)
        d.ellipse([x + s * .38, y + s * .5, x + s * .62, y + s * .85], fill=accent)
    elif name == "columns":
        for i in range(3):
            cx = x + 2 + i * (s - 4) // 2
            d.rectangle([cx, y + 4, cx + 3, y + s - 3], fill=ink)
        d.line([x, y + 2, x + s, y + 2], fill=ink, width=2)
    elif name == "trophy":
        d.rectangle([x + s * .3, y + 1, x + s * .7, y + s * .55], outline=ink, width=2)
        d.arc([x, y, x + s * .4, y + s * .5], 90, 270, fill=ink, width=2)
        d.arc([x + s * .6, y, x + s, y + s * .5], 270, 90, fill=ink, width=2)
        d.line([x + s // 2, y + s * .55, x + s // 2, y + s * .8], fill=ink, width=2)
        d.line([x + s * .25, y + s - 2, x + s * .75, y + s - 2], fill=accent, width=3)
    elif name == "drone":
        for cx, cy in [(x + 3, y + 3), (x + s - 3, y + 3), (x + 3, y + s - 3), (x + s - 3, y + s - 3)]:
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=ink, width=2)
        d.rectangle([x + s * .35, y + s * .35, x + s * .65, y + s * .65], fill=accent)
    elif name == "star":
        cx, cy, r = x + s / 2, y + s / 2, s / 2
        pts = []
        for i in range(10):
            ang = -1.57 + i * 0.628
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=accent)
    elif name == "globe":
        d.ellipse([x + 1, y + 1, x + s - 1, y + s - 1], outline=ink, width=2)
        d.line([x + 1, y + s // 2, x + s - 1, y + s // 2], fill=ink, width=1)
        d.line([x + s // 2, y + 1, x + s // 2, y + s - 1], fill=ink, width=1)
    elif name == "ship":
        d.polygon([(x + 2, y + s * .6), (x + s - 2, y + s * .6),
                   (x + s * .75, y + s), (x + s * .25, y + s)], outline=ink, width=2)
        d.rectangle([x + s * .35, y + s * .25, x + s * .65, y + s * .6], outline=accent, width=2)
    elif name == "coin":
        d.ellipse([x + 1, y + 1, x + s - 1, y + s - 1], outline=accent, width=2)
        d.text((x + s * .34, y + s * .14), "$", font=fb(int(s * .6)), fill=ink)
    elif name == "gavel":
        d.line([x + 3, y + s - 3, x + s * .6, y + s * .4], fill=ink, width=3)
        d.rectangle([x + s * .5, y + 2, x + s - 1, y + s * .3], outline=accent, width=2)
        d.line([x + 2, y + s - 2, x + s * .6, y + s - 2], fill=ink, width=2)
    elif name == "flag":
        d.line([x + 3, y, x + 3, y + s], fill=ink, width=2)
        d.polygon([(x + 3, y + 1), (x + s, y + s * .25), (x + 3, y + s * .5)], fill=accent)
    elif name == "ball":
        d.ellipse([x + 1, y + 1, x + s - 1, y + s - 1], outline=ink, width=2)
        d.arc([x - s * .3, y, x + s * .5, y + s], 300, 60, fill=accent, width=2)
        d.arc([x + s * .5, y, x + s * 1.3, y + s], 120, 240, fill=accent, width=2)
    else:
        d.rectangle([x, y, x + s, y + s], outline=ink, width=2)


def lead(d, x, y, w, h, region, icon_name, src, head, deck, kind, num,
         ink, accent, card_bg):
    """The big card #1. kind doubles as its illustration key."""
    d.rectangle([x, y, x + w, y + h], fill=card_bg, outline=ink, width=2)
    d.rectangle([x + 8, y + 8, x + 34, y + 34], fill=ink)
    d.text((x + 15, y + 12), str(num), font=fb(17), fill=card_bg)
    chip = region + " - LEAD STORY"
    cf = fb(12)
    cw = d.textlength(chip, font=cf) + 14
    d.rectangle([x + 42, y + 8, x + 42 + cw, y + 34], fill=REGION_COLORS[region])
    d.text((x + 49, y + 14), chip, font=cf, fill=(255, 255, 255))
    d.text((x + w - 8 - d.textlength(src, font=cf), y + 14), src, font=cf, fill=accent)
    hf = fp(PLAY_BOLD, 27)
    lines = wrap(d, head, hf, w - 190)
    assert len(lines) <= 2, lines
    yy = y + 42
    for ln in lines:
        d.text((x + 12, yy), ln, font=hf, fill=ink)
        yy += 32
    df = fr(15)
    dl = wrap(d, deck, df, w - 190)
    assert len(dl) <= 2, dl
    for ln in dl:
        d.text((x + 12, yy + 4), ln, font=df, fill=ink)
        yy += 19
    # illustration: server racks + magnifier + warning mark
    ix, iy, iw, ih = x + w - 172, y + 44, 160, 100
    for i in range(3):
        rx = ix + i * (iw // 3) + 3
        d.rectangle([rx, iy + 6, rx + iw // 3 - 10, iy + ih - 18], outline=ink, width=3)
        for j in range(4):
            cy = iy + 18 + j * ((ih - 44) // 4)
            d.rectangle([rx + 7, cy, rx + iw // 3 - 17, cy + 11], outline=ink, width=2)
            d.ellipse([rx + iw // 3 - 28, cy + 3, rx + iw // 3 - 22, cy + 9], fill=accent)
    mx, my, mr = ix + iw - 40, iy + ih - 42, 24
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=accent, width=5)
    d.line([mx + mr * .7, my + mr * .7, mx + mr + 13, my + mr + 13], fill=accent, width=6)
    d.polygon([(mx, my - 13), (mx - 11, my + 8), (mx + 11, my + 8)], outline=ink, width=3)
    d.text((mx - 3, my - 7), "!", font=fb(17), fill=ink)


def mini(d, x, y, w, h, region, icon_name, src, head, deck, kind, num,
         ink, accent, card_bg):
    """One grid card. kind doubles as its illustration key."""
    d.rectangle([x, y, x + w, y + h], fill=card_bg, outline=ink, width=1)
    d.rectangle([x + 5, y + 5, x + 27, y + 27], fill=ink)
    nf = fb(13)
    t = str(num)
    d.text((x + 16 - d.textlength(t, font=nf) / 2, y + 8), t, font=nf, fill=card_bg)
    cfl = fb(10)
    cw2 = d.textlength(region, font=cfl) + 10
    d.rectangle([x + 31, y + 5, x + 31 + cw2, y + 23], fill=REGION_COLORS[region])
    d.text((x + 36, y + 9), region, font=cfl, fill=(255, 255, 255))
    d.text((x + w - 7 - d.textlength(src, font=cfl), y + 9), src, font=cfl, fill=accent)
    hf = fb(24)
    lines = head.split("\n")
    assert len(lines) == 2 and all(d.textlength(l, font=hf) <= w - 14 for l in lines), lines
    yy = y + 30
    for ln in lines:
        d.text((x + 7, yy), ln, font=hf, fill=ink)
        yy += 25
    df = fr(14)
    dl = wrap(d, deck, df, w - 14)
    assert len(dl) <= 2, (deck, dl)
    fy = y + h - 4 - 15 * len(dl)
    for ln in dl:
        d.text((x + 7, fy), ln, font=df, fill=ink)
        fy += 15
    icon(d, kind, x + w - 22, y + h - 22, 16, ink, accent)


def dotted_map(d, x, y, w, h, ink, accent, card_bg):
    """Original dotted world map with numbered pins and a colour legend."""
    d.rectangle([x, y, x + w, y + h], fill=card_bg, outline=ink, width=2)
    d.text((x + 10, y + 7), "WHERE THE DAY HAPPENED", font=fb(13), fill=ink)
    d.text((x + 10, y + 23), "DOTTED MAP - PINS MARK THE CARD NUMBERS",
           font=fb(9), fill=accent)
    gx, gy, cell = x + 14, y + 38, 5.2
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx, cy = gx + c * cell, gy + r * cell
                d.ellipse([cx, cy, cx + 3.0, cy + 3.0], fill=(150, 138, 116))
    pf = fb(8)
    for num, (c, r) in PINS.items():
        cx, cy = gx + c * cell + 2, gy + r * cell + 2
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=accent, outline=ink)
        t = str(num)
        d.text((cx - d.textlength(t, font=pf) / 2, cy - 4), t, font=pf, fill=(255, 255, 255))
    leg = list(REGION_COLORS.items()) + [("12 = WORLD MARKETS", (85, 80, 73))]
    lf2 = fb(9)
    for ri, row_items in enumerate([leg[:5], leg[5:]]):
        lx = x + 10
        ly2 = y + h - 26 + ri * 13
        for name, col in row_items:
            d.rectangle([lx, ly2 + 1, lx + 8, ly2 + 9], fill=col)
            d.text((lx + 11, ly2), name, font=lf2, fill=ink)
            lx += 11 + d.textlength(name, font=lf2) + 9


def build(variant):
    if variant == "A":
        paper, card_bg = (233, 227, 213), (247, 243, 233)
        ink, accent = (58, 42, 28), (154, 123, 28)
        lead_right = False
    elif variant == "B":
        paper, card_bg = (240, 234, 220), (250, 247, 240)
        ink, accent = (46, 32, 21), (122, 92, 20)
        lead_right = False
    else:
        paper, card_bg = (222, 213, 194), (238, 232, 218)
        ink, accent = (64, 48, 31), (176, 138, 46)
        lead_right = True

    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)
    M = 26

    d.rectangle([8, 8, W - 9, H - 9], outline=ink, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=accent, width=1)

    kick = "39 STORIES - 8 REGIONS - EVERY ONE FROM 23 NOVEMBER 2026"
    kf = fit(ARCH_B, kick, 15, W - 2 * M)
    d.text(((W - d.textlength(kick, font=kf)) / 2, 18), kick, font=kf, fill=accent)
    d.line([M, 42, W - M, 42], fill=ink, width=2)

    mast = "THE DAY'S RECORD"
    mf = fit(PLAY_BLACK, mast, 76, W - 2 * M)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 48), mast, font=mf, fill=ink)
    d.line([M, 126, W - M, 126], fill=accent, width=3)
    date = "Monday 23 November 2026"
    df = fit(PLAY_BOLD, date, 30, 560)
    d.text(((W - d.textlength(date, font=df)) / 2, 132), date, font=df, fill=ink)

    sy = 168
    d.rectangle([M, sy, W - M, sy + 40], outline=ink, width=2)
    bw = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(NUMS):
        cx = M + i * bw
        if i:
            d.line([cx, sy + 4, cx, sy + 36], fill=accent, width=1)
        nf = fit(ARCH_B, num, 22, bw - 8)
        d.text((cx + (bw - d.textlength(num, font=nf)) / 2, sy + 3), num, font=nf, fill=ink)
        lf = fit(ARCH_B, lab, 10, bw - 6)
        d.text((cx + (bw - d.textlength(lab, font=lf)) / 2, sy + 26), lab, font=lf, fill=accent)

    ly, lh = 216, 152
    lead_w, map_w = 556, 388
    if lead_right:
        map_x, lead_x = M, W - M - lead_w
    else:
        lead_x, map_x = M, W - M - map_w
    lead(d, lead_x, ly, lead_w, lh, "N. AMERICA", "database", "AP WIRE",
         "FBI PROBES HACK OF ITS JUSTICE DATABASE",
         "Agents probe a suspected hack of the FBI's main justice database in Washington.",
         "database", 1, ink, accent, card_bg)
    dotted_map(d, map_x, ly, map_w, lh, ink, accent, card_bg)

    gy0, gh, gap = 376, 112, 8
    gw = (W - 2 * M - 3 * gap) // 4
    mini(d, M, gy0, gw, gh, "MIDDLE EAST", "flame", "AP LIVE",
         "TANKERS BURN IN\nHORMUZ STRAIT",
         "Iran-US war widens into the Gulf; IRGC warns of unrest", "flame", 2,
         ink, accent, card_bg)
    mini(d, M + (gw + gap), gy0, gw, gh, "N. AMERICA", "columns", "BBC",
         "DEMOCRATS WIN\nHOUSE 258-173",
         "Biggest House majority since 1992 after a North Carolina flip", "columns", 3,
         ink, accent, card_bg)
    mini(d, M + 2 * (gw + gap), gy0, gw, gh, "SOUTH ASIA", "trophy", "OBSERVER VOICE",
         "INDIA'S 720/9\nA NZ RECORD",
         "Highest Test total ever posted on New Zealand soil", "trophy", 4,
         ink, accent, card_bg)
    mini(d, M + 3 * (gw + gap), gy0, gw, gh, "EUROPE", "drone", "JAGRAN JOSH",
         "14 MISSING,\nKYIV STRIKE",
         "Zelenskiy says 14 missing after drones hit a Kyiv block", "drone", 5,
         ink, accent, card_bg)
    mini(d, M, gy0 + (gh + gap), gw, gh, "EUROPE", "star", "BBC",
         "KYIV BOY, 7,\nPULLED ALIVE",
         "Out after hours under debris; 6 killed in Kyiv", "star", 6,
         ink, accent, card_bg)
    mini(d, M + (gw + gap), gy0 + (gh + gap), gw, gh, "EUROPE", "globe", "BBC / AP",
         "COP31 ENDS\nWITHOUT A DEAL",
         "COP31's Turkish draft omits 'fossil fuels' for good", "globe", 7,
         ink, accent, card_bg)
    mini(d, M + 2 * (gw + gap), gy0 + (gh + gap), gw, gh, "EUROPE", "ship", "BBC",
         "RUSSIAN SHIP\nBURNS - FINLAND",
         "Vessel still ablaze after attack in Gulf of Finland", "ship", 8,
         ink, accent, card_bg)
    mini(d, M + 3 * (gw + gap), gy0 + (gh + gap), gw, gh, "SOUTH ASIA", "coin", "OBSERVER VOICE",
         "TATA STEEL SALE:\nRs 28,000 CR",
         "Steel-pipe unit sold to APL Apollo for Rs 28,000 crore", "coin", 9,
         ink, accent, card_bg)
    mini(d, M, gy0 + 2 * (gh + gap), gw, gh, "SE ASIA", "gavel", "GUARDIAN / NYT",
         "MYANMAR GUILTY\nOF GENOCIDE",
         "ICJ rules Rohingya campaign genocide; 700,000+ fled in 2017", "gavel", 10,
         ink, accent, card_bg)
    mini(d, M + (gw + gap), gy0 + 2 * (gh + gap), gw, gh, "EUROPE", "flag", "JAGRAN JOSH",
         "LISBON MARCHES\nON LIVING COSTS",
         "Thousands march in Lisbon, Portugal, on living costs", "flag", 11,
         ink, accent, card_bg)
    mini(d, M + 2 * (gw + gap), gy0 + 2 * (gh + gap), gw, gh, "GLOBAL", "coin", "OBSERVER VOICE",
         "GOLD SLIDES TO\n$3,538 AN OUNCE",
         "Down over $2,000 from the 2026 record of $5,595", "coin", 12,
         ink, accent, card_bg)
    mini(d, M + 3 * (gw + gap), gy0 + 2 * (gh + gap), gw, gh, "EUROPE", "ball", "BBC",
         "ALCARAZ TAKES\nATP FINALS",
         "First ATP Finals crown for Alcaraz, beating Zverev", "ball", 13,
         ink, accent, card_bg)

    ty = gy0 + 3 * (gh + gap) + 4
    d.rectangle([M, ty, W - M, ty + 24], outline=ink, width=1)
    lab = "THE DAY IN UTC"
    lf3 = fb(12)
    d.text((M + 8, ty + 5), lab, font=lf3, fill=accent)
    tl_text = " - ".join(when + " " + what for when, what in TL)
    tf = fit(ARCH, tl_text, 12, W - 2 * M - 130)
    d.text((M + 124, ty + 5), tl_text, font=tf, fill=ink)

    by = ty + 32
    bh = 948 - by
    also_w = 700
    d.rectangle([M, by, M + also_w, by + bh], outline=ink, width=2)
    d.text((M + 10, by + 6), "ALSO ON 23 NOVEMBER - STORIES 14-39", font=fb(15), fill=ink)
    d.line([M + 8, by + 30, M + also_w - 8, by + 30], fill=accent, width=2)
    af = fsr(13)
    abf = fb(13)
    colw = (also_w - 28) // 3
    per = 9
    for i, title in enumerate(BRIEFS):
        col = i // per
        row = i % per
        x = M + 10 + col * colw
        y = by + 36 + row * 15
        d.text((x, y), str(14 + i), font=abf, fill=accent)
        tf2 = fit(ARCH, title, 13, colw - 28, min_size=11)
        d.text((x + 25, y), title, font=tf2, fill=ink)
    dx = M + also_w + 10
    dw = W - M - dx
    red = (165, 30, 25)
    d.rectangle([dx, by, dx + dw, by + bh], outline=red, width=3)
    d.text((dx + 10, by + 6), "DATE CHECK - NOT 23 NOV", font=fb(14), fill=red)
    d.text((dx + 10, by + 26), "Checked and kept out of the news:",
           font=fsr(11), fill=ink)
    dcf = fsr(11)
    yy = by + 44
    for item in dc.split(" · "):
        ls = wrap(d, item, dcf, dw - 20)
        assert len(ls) <= 2, (item, ls)
        for ln in ls:
            d.text((dx + 10, yy), ln, font=dcf, fill=ink)
            yy += 13
        yy += 3

    foot = ("Every story happened, or was first reported, on Monday 23 November 2026. "
            "Contested claims are attributed.")
    fof = fit(ARCH, foot, 12, W - 2 * M)
    d.text(((W - d.textlength(foot, font=fof)) / 2, 956), foot, font=fof, fill=ink)
    od = "Original drawings. - THE DAY'S RECORD, one page, the whole day."
    d.text(((W - d.textlength(od, font=fof)) / 2, 974), od, font=fof, fill=accent)
    return img


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g3-akun17/entry.png"
    build(variant).save(out)
    print("saved", out)
