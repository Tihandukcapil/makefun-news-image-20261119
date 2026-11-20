#!/usr/bin/env python3
"""Compose the front page for Thursday 19 November 2026.

One 1024x1024 newspaper front page, drawn entirely in code with PIL:
masthead naming the day, region chips, a number strip, 3 large + 10 small
featured stories (13), a dotted world map with numbered pins, a further
27 stories, a DATE CHECK box and a sources footer. 40 stories in all.

Everything is original work written in this session: the layout, the
drawings and the wording are ours. Facts were verified against news
round-ups for 19 November 2026 (Algenom, Level Headlines, Pollar,
Helsinki Times, Reuters/AP/BBC reporting via those round-ups, IMD).
Stories that belong to another day (Qeshm strike 17 Nov, Kuwait/Bahrain
drone interceptions 18 Nov, Anthropic's $83 pricing 18 Nov, Van Gogh's
$190.4m sale 18 Nov, Voyager 1 one light-day 18 Nov, the EU's EUR45bn
Ukraine loan proposal 18 Nov) are deliberately left out and named in
the DATE CHECK box, so the page never presents another day's news as
Thursday's.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (248, 243, 231)
INK = (25, 25, 25)
RED = (163, 22, 33)
NAVY = (30, 58, 95)
GOLD = (176, 132, 0)
TEAL = (14, 107, 107)
GREY = (107, 101, 88)
LIGHT = (238, 231, 214)
RULE = (25, 25, 25)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, fnt_path, sizes, max_w, max_lines, draw):
    """Try font sizes largest-first; return (font, lines) fitting the box."""
    for size in sizes:
        fnt = font(fnt_path, size)
        lines = wrap(text, fnt, max_w, draw)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(fnt_path, sizes[-1])
    return fnt, wrap(text, fnt, max_w, draw)[:max_lines]


# ---------------------------------------------------------------- stories
# art: key into ART draw functions. lon/lat: map pin (featured only).
FEATURED = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT", region="Asia", art="summit",
         lon=114.1, lat=22.5,
         headline="Trump, Xi and Putin hold first three-way summit",
         sub=("About 70 minutes beside APEC, then a Declaration toward Peace on "
              "nuclear risks and UN reform \u2014 no arms deal, no mention of "
              "Ukraine or Iran."),
         src="AP \u00b7 Reuters"),
    dict(n=2, place="THE HAGUE", topic="LAW", region="Europe", art="court",
         lon=4.3, lat=52.1,
         headline="World Court: Myanmar committed genocide",
         sub=("By 9\u20136 the court found Myanmar guilty over the 2017 crackdown; "
              "about 10,000 were killed, 700,000+ fled. Inquiries, returns and "
              "compensation ordered."),
         src="UN News \u00b7 BBC"),
    dict(n=3, place="NEW YORK", topic="MARKETS", region="Americas", art="ipo",
         lon=-74.0, lat=40.7,
         headline="Anthropic starts trading after the biggest IPO on record",
         sub=("Priced at $83, the Claude maker raised $81.3bn \u2014 past SpaceX's "
              "$75bn. Shares opened at $111.50 and briefly valued it near $2tn."),
         src="CNBC \u00b7 Reuters"),
    dict(n=4, place="WORLDWIDE", topic="GAMES", region="Global", art="gta",
         lon=174.8, lat=-36.8,
         headline="GTA VI is out, 13 years after GTA V",
         sub=("Rockstar's sequel unlocked at midnight local time, New Zealand "
              "first. 15.9m pre-orders, $1.54bn; 99 on Metacritic."),
         src="Reuters \u00b7 Sensor Tower"),
    dict(n=5, place="ANTALYA", topic="CLIMATE", region="Europe", art="cop",
         lon=30.7, lat=36.9,
         headline="COP31 draft drops fossil fuels and the $120bn aid goal",
         sub=("The text shrank from 144 paragraphs to 80, names no fuel and no "
              "dollar figure for adaptation. Talks are due to end on Friday."),
         src="Reuters \u00b7 AFP"),
    dict(n=6, place="ODISHA", topic="STORM", region="Asia", art="cyclone",
         lon=85.8, lat=19.8,
         headline="Cyclone Akvan nears India's coast",
         sub=("Odisha moved 100,000+ to shelters, aiming for 200,000, ahead of "
              "Friday landfall near Puri."),
         src="IMD \u00b7 PTI"),
    dict(n=7, place="RIYADH", topic="GULF", region="Middle East", art="tower",
         lon=46.7, lat=24.7,
         headline="Houthi missile hits Riyadh's tallest tower",
         sub=("Reuters: missile struck the PIF Tower, windows blown out on "
              "7\u20138 floors; none hurt."),
         src="Reuters \u00b7 AP"),
    dict(n=8, place="KYIV", topic="WAR", region="Europe", art="bridge",
         lon=30.5, lat=50.4,
         headline="Ukraine hits Crimea bridge again",
         sub=("A third strike in a week halted trains across the Kerch Bridge, "
              "hours before the summit."),
         src="Reuters \u00b7 Euronews"),
    dict(n=9, place="SEOUL", topic="EDUCATION", region="Asia", art="exam",
         lon=127.0, lat=37.5,
         headline="Half a million sit Korea's Suneung",
         sub=("551,864 candidates at 1,312 centres; flights paused, and phone "
              "alerts caught 22 with devices."),
         src="AP"),
    dict(n=10, place="GREENLAND", topic="SECURITY", region="Europe", art="ice",
         lon=-51.7, lat=64.2,
         headline="Denmark backs Arctic pact with US",
         sub=("Parliament voted 109\u20130 for the US\u2013Denmark\u2013Greenland deal, "
              "updating the 1951 pact."),
         src="AP"),
    dict(n=11, place="CANBERRA", topic="ECONOMY", region="Oceania", art="jobs",
         lon=149.1, lat=-35.3,
         headline="Australia's jobless rate jumps to 4.9%",
         sub=("The highest since October 2021: 43,500 jobs lost in October; "
              "youth joblessness at 11.3%."),
         src="ABS \u00b7 ABC"),
    dict(n=12, place="GAZA", topic="WAR", region="Middle East", art="tank",
         lon=34.5, lat=31.5,
         headline="Israeli armour pushes into central Gaza",
         sub=("Tanks moved toward Salah al-Din Street, past the Yellow Line. "
              "Hamas calls it a ceasefire breach."),
         src="AP"),
    dict(n=13, place="JAKARTA", topic="LAW", region="Asia", art="gavel",
         lon=106.8, lat=-6.2,
         headline="Indonesia passes asset-seizure law",
         sub=("After an 18-year wait, the state may seize assets of Rp1bn or "
              "more without a conviction."),
         src="Antara"),
]

ALSO = [
    (14, "FLORIDA", "Americas", "Floods shut schools again; 15.3 in. rain."),
    (15, "BOGOT\u00c1", "Americas", "Unions hold a national strike in Colombia."),
    (16, "NAIROBI", "Africa", "Jepchirchir banned 3 years for doping."),
    (17, "PARIS", "Europe", "Left splits over M\u00e9lenchon; he could win."),
    (18, "BENGHAZI", "Africa", "Cocaine, millions of pills seized in Libya."),
    (19, "WASHINGTON", "Americas", "Court asked to let EPA cancel $16bn grants."),
    (20, "NEW YORK", "Americas", "Musk: \u201cnot MAGA\u201d after $400m+ on GOP."),
    (21, "MISSISSIPPI", "Americas", "Democrats query 230,000 inactive voters."),
    (22, "SHENZHEN", "Asia", "APEC adopts Shenzhen Declaration on trade."),
    (23, "MEXICO CITY", "Americas", "Banxico cuts rates to 6.25%, 3\u20132 vote."),
    (24, "CARACAS", "Americas", "Hegseth signs US\u2013Venezuela military deal."),
    (25, "WASHINGTON", "Americas", "Vance: no \u201cforever war\u201d in the Gulf."),
    (26, "MANAMA", "Middle East", "Bapco refinery back after the attacks."),
    (27, "RIYADH", "Middle East", "Gulf leaders: don't strike Iran, Trump told."),
    (28, "NAIROBI", "Africa", "Kenya floods kill six; Ruto addresses nation."),
    (29, "BAGHDAD", "Middle East", "Six French ISIL members jailed for life."),
    (30, "CANBERRA", "Oceania", "Australia sanctions West Bank settlers."),
    (31, "AUCKLAND", "Oceania", "NZ plays first as GTA VI unlocks at midnight."),
    (32, "WASHINGTON", "Americas", "Senators warn AI cyber threats grow."),
    (33, "NATURE", "Global", "Nature: mantle currents explain \u201clost\u201d eons."),
    (34, "ROME", "Europe", "Author Corrado Augias dies at 91."),
    (35, "MOGADISHU", "Africa", "Somalia expels the UAE ambassador."),
    (36, "SUDAN", "Africa", "Court sentences absent RSF chief to death."),
    (37, "PRETORIA", "Africa", "Central bank holds rate at 7.25%."),
    (38, "CANARIES", "Europe", "Record 11,000 migrants in 15 days."),
    (39, "WELLINGTON", "Oceania", "Court: pay equity cuts broke rights law."),
    (40, "TONGA", "Oceania", "Drought emergency takes effect."),
]

NUMBERS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court genocide vote"),
    ("$81.3bn", "biggest IPO on record"),
    ("15.9m", "GTA VI pre-orders"),
    ("200,000", "in Akvan's evacuation zone"),
    ("109\u20130", "Denmark votes for the Arctic pact"),
]

REGION_ORDER = ["Asia", "Middle East", "Europe", "Africa", "Americas",
                "Oceania", "Global"]
REGION_COLORS = {"Asia": (163, 22, 33), "Middle East": (176, 110, 0),
                 "Europe": (30, 58, 95), "Africa": (14, 107, 107),
                 "Americas": (90, 60, 140), "Oceania": (40, 110, 60),
                 "Global": (90, 90, 90)}

DATE_CHECK = ("DATE CHECK \u2014 Every story on this page happened, or was first "
              "reported, on Thursday 19 November 2026. Left out as other days' "
              "news: US strikes on Iran's Qeshm Island (17 Nov) \u00b7 Iranian drone "
              "interceptions over Kuwait and Bahrain (18 Nov) \u00b7 Anthropic's $83 "
              "pricing (18 Nov \u2014 trading began Thursday) \u00b7 Van Gogh's record "
              "$190.4m sale (18 Nov) \u00b7 Voyager 1 crossing one light-day (18 Nov) "
              "\u00b7 the EU's proposed \u20ac45bn Ukraine loan (18 Nov).")
FOOTER = ("Every story here happened, or was first reported, on Thursday 19 November 2026, in any time zone; "
          "disputed claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, BBC, Al Jazeera, "
          "UN News, CNBC, ABC, IMD, Antara. Pictures and map: original, drawn in code.")


# ---------------------------------------------------------------- art
def _flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
    for i in range(0, 7, 2):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(240, 240, 240))
    d.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=(30, 58, 95))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 3 + c * w * 0.09, y + 3 + r * h * 0.16,
                       x + 6 + c * w * 0.09, y + 6 + r * h * 0.16],
                      fill=(255, 255, 255))


def _flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + 2, y + 2, x + 8, y + 8], fill=(255, 222, 0))
    for sx, sy in [(0.62, 0.18), (0.78, 0.32), (0.78, 0.55), (0.62, 0.68)]:
        d.ellipse([x + sx * w, y + sy * h, x + sx * w + 3, y + sy * h + 3],
                  fill=(255, 222, 0))


def _flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 0))


def art_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 92))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(214, 128, 60))
    for bx, bw, bh in [(0.02, 0.10, 0.34), (0.16, 0.08, 0.46), (0.30, 0.12, 0.30),
                       (0.58, 0.09, 0.40), (0.72, 0.11, 0.28), (0.88, 0.08, 0.44)]:
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h * 0.98],
                    fill=(22, 28, 58))
    d.ellipse([x + w * 0.44, y + h * 0.08, x + w * 0.56, y + h * 0.24],
              fill=(255, 196, 90))
    fw, fh = w * 0.17, h * 0.22
    for i, fl in enumerate((_flag_us, _flag_cn, _flag_ru)):
        fx = x + w * (0.10 + i * 0.36)
        d.line([fx + fw / 2, y + h * 0.30, fx + fw / 2, y + h * 0.62],
               fill=(220, 220, 220), width=2)
        fl(d, fx, y + h * 0.30, fw, fh)
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h * 0.78],
                fill=(120, 72, 40))
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h * 0.66],
                fill=(230, 220, 200))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 200))
    d.polygon([(x + w * 0.08, y + h * 0.42), (x + w * 0.50, y + h * 0.10),
               (x + w * 0.92, y + h * 0.42)], fill=(150, 120, 80))
    d.rectangle([x + w * 0.10, y + h * 0.42, x + w * 0.90, y + h * 0.48],
                fill=(120, 95, 60))
    for i in range(4):
        cx = x + w * (0.18 + i * 0.21)
        d.rectangle([cx, y + h * 0.48, cx + w * 0.07, y + h * 0.86],
                    fill=(245, 240, 225))
    d.rectangle([x + w * 0.08, y + h * 0.86, x + w * 0.92, y + h * 0.92],
                fill=(120, 95, 60))
    # scales of justice
    sx, sy = x + w * 0.78, y + h * 0.60
    d.line([sx, sy - 18, sx, sy + 12], fill=(60, 50, 30), width=2)
    d.line([sx - 16, sy - 12, sx + 16, sy - 12], fill=(60, 50, 30), width=2)
    for s in (-1, 1):
        d.line([sx + s * 16, sy - 12, sx + s * 12, sy + 2], fill=(60, 50, 30),
               width=1)
        d.polygon([(sx + s * 12 - 6, sy + 2), (sx + s * 12 + 6, sy + 2),
                   (sx + s * 12, sy + 10)], fill=(200, 160, 60))
    d.rectangle([x + w * 0.03, y + h * 0.06, x + w * 0.30, y + h * 0.24],
                fill=(163, 22, 33))
    d.text((x + w * 0.05, y + h * 0.09), "9\u20136", font=font(SANS_B, 15),
           fill=(255, 255, 255))


def art_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 30, 54))
    pts = [(0.06, 0.78), (0.20, 0.70), (0.34, 0.74), (0.48, 0.55),
           (0.62, 0.58), (0.76, 0.34), (0.94, 0.18)]
    for i in range(len(pts) - 1):
        d.line([x + pts[i][0] * w, y + pts[i][1] * h,
                x + pts[i + 1][0] * w, y + pts[i + 1][1] * h],
               fill=(60, 220, 120), width=4)
    for px, py in pts:
        d.ellipse([x + px * w - 3, y + py * h - 3, x + px * w + 3, y + py * h + 3],
                  fill=(60, 220, 120))
    d.text((x + w * 0.06, y + h * 0.06), "ANT", font=font(SANS_B, 16),
           fill=(255, 255, 255))
    d.text((x + w * 0.60, y + h * 0.60), "$83", font=font(SANS_B, 22),
           fill=(255, 210, 60))


def art_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 30, 110))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(30, 16, 50))
    d.ellipse([x + w * 0.62, y + h * 0.10, x + w * 0.86, y + h * 0.42],
              fill=(255, 170, 60))
    for bx, bw, bh in [(0.04, 0.10, 0.42), (0.18, 0.08, 0.58), (0.32, 0.12, 0.36),
                       (0.52, 0.09, 0.50), (0.68, 0.07, 0.62)]:
        d.rectangle([x + bx * w, y + h - bh * h, x + (bx + bw) * w, y + h * 0.98],
                    fill=(20, 10, 36))
    # palm
    px, py = x + w * 0.88, y + h * 0.62
    d.line([px, py, px, py - h * 0.30], fill=(20, 60, 20), width=3)
    for a in (-0.9, -0.4, 0.1, 0.6):
        import math
        ex = px + math.cos(a - 1.57) * w * 0.12
        ey = py - h * 0.30 + math.sin(a - 1.57) * h * 0.12
        d.line([px, py - h * 0.30, ex, ey], fill=(30, 120, 50), width=2)
    d.text((x + w * 0.06, y + h * 0.08), "VI", font=font(SERIF_B, 30),
           fill=(255, 255, 255))


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 230, 225))
    cx, cy, r = x + w * 0.30, y + h * 0.45, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 140, 190))
    d.ellipse([cx - r * 0.55, cy - r * 0.30, cx + r * 0.25, cy + r * 0.45],
              fill=(90, 170, 90))
    d.ellipse([cx - r * 0.2, cy - r * 0.75, cx + r * 0.7, cy - r * 0.1],
              fill=(90, 170, 90))
    # thermometer
    tx = x + w * 0.62
    d.rounded_rectangle([tx, y + h * 0.12, tx + w * 0.08, y + h * 0.72],
                        radius=6, fill=(255, 255, 255), outline=(163, 22, 33),
                        width=2)
    d.ellipse([tx - 3, y + h * 0.66, tx + w * 0.08 + 3, y + h * 0.88],
              fill=(213, 0, 0))
    d.rectangle([tx + 2, y + h * 0.30, tx + w * 0.08 - 2, y + h * 0.72],
                fill=(213, 0, 0))
    d.text((x + w * 0.05, y + h * 0.78), "FOSSIL FUELS", font=font(SANS_B, 11),
           fill=(163, 22, 33))
    d.line([x + w * 0.04, y + h * 0.84, x + w * 0.52, y + h * 0.84],
           fill=(163, 22, 33), width=3)


def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 215, 235))
    cx, cy = x + w * 0.50, y + h * 0.45
    for k, r in enumerate([8, 16, 25, 34]):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              start=200 + k * 40, end=200 + k * 40 + 230,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=(30, 58, 95))
    for i in range(6):
        rx = x + w * (0.08 + i * 0.15)
        d.line([rx, y + h * 0.80, rx - 4, y + h * 0.95], fill=(60, 120, 180),
               width=2)
    d.rectangle([x, y + h * 0.92, x + w, y + h], fill=(120, 140, 90))


def art_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 42, 78))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(30, 26, 50))
    tx = x + w * 0.38
    d.polygon([(tx, y + h * 0.08), (tx + w * 0.24, y + h * 0.08),
               (tx + w * 0.17, y + h * 0.95), (tx + w * 0.07, y + h * 0.95)],
              fill=(90, 100, 140))
    for r in range(6):
        for c in range(2):
            d.rectangle([tx + w * (0.07 + c * 0.08), y + h * (0.16 + r * 0.12),
                         tx + w * (0.11 + c * 0.08), y + h * (0.20 + r * 0.12)],
                        fill=(255, 210, 90))
    d.ellipse([x + w * 0.62, y + h * 0.10, x + w * 0.86, y + h * 0.34],
              fill=(120, 120, 130))
    d.ellipse([x + w * 0.66, y + h * 0.14, x + w * 0.82, y + h * 0.30],
              fill=(80, 80, 90))
    d.polygon([(x + w * 0.50, y + h * 0.20), (x + w * 0.78, y + h * 0.12),
               (x + w * 0.72, y + h * 0.42), (x + w * 0.56, y + h * 0.44)],
              fill=(150, 150, 160))


def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 225))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(70, 110, 160))
    d.line([x + w * 0.05, y + h * 0.70, x + w * 0.95, y + h * 0.70],
           fill=(40, 40, 40), width=4)
    for i in range(5):
        bx = x + w * (0.12 + i * 0.18)
        d.line([bx, y + h * 0.70, bx, y + h * 0.88], fill=(40, 40, 40), width=3)
    import math
    sx, sy = x + w * 0.72, y + h * 0.42
    for k in range(8):
        a = k * math.pi / 4
        d.line([sx, sy, sx + math.cos(a) * 16, sy + math.sin(a) * 16],
               fill=(255, 180, 0), width=3)
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 120, 0))
    d.rectangle([x + w * 0.08, y + h * 0.60, x + w * 0.30, y + h * 0.68],
                fill=(120, 30, 30))


def art_exam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    d.ellipse([x + w * 0.78, y + h * 0.06, x + w * 0.96, y + h * 0.30],
              fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    d.line([x + w * 0.87, y + h * 0.18, x + w * 0.87, y + h * 0.10],
           fill=(163, 22, 33), width=2)
    d.line([x + w * 0.87, y + h * 0.18, x + w * 0.92, y + h * 0.20],
           fill=(163, 22, 33), width=2)
    for r in range(2):
        for c in range(3):
            dx = x + w * (0.10 + c * 0.26)
            dy = y + h * (0.42 + r * 0.30)
            d.rectangle([dx, dy, dx + w * 0.20, dy + h * 0.10], fill=(150, 110, 70))
            d.rectangle([dx + w * 0.03, dy - h * 0.08, dx + w * 0.17, dy],
                        fill=(255, 255, 255), outline=(120, 120, 120))
            d.ellipse([dx + w * 0.07, dy - h * 0.22, dx + w * 0.13, dy - h * 0.14],
                      fill=(220, 180, 140))


def art_ice(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 220, 235))
    d.polygon([(x, y + h), (x + w * 0.30, y + h * 0.30),
               (x + w * 0.55, y + h)], fill=(230, 240, 245))
    d.polygon([(x + w * 0.40, y + h), (x + w * 0.68, y + h * 0.18),
               (x + w * 0.95, y + h)], fill=(210, 228, 238))
    d.polygon([(x + w * 0.30, y + h * 0.30), (x + w * 0.38, y + h * 0.42),
               (x + w * 0.22, y + h * 0.42)], fill=(255, 255, 255))
    d.rectangle([x + w * 0.06, y + h * 0.08, x + w * 0.42, y + h * 0.26],
                fill=(255, 255, 255), outline=(163, 22, 33), width=2)
    d.rectangle([x + w * 0.06, y + h * 0.15, x + w * 0.42, y + h * 0.19],
                fill=(163, 22, 33))
    d.text((x + w * 0.52, y + h * 0.08), "109\u20130", font=font(SANS_B, 16),
           fill=(163, 22, 33))


def art_jobs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 232, 220))
    vals = [0.62, 0.55, 0.58, 0.42, 0.30]
    bw = w * 0.13
    for i, v in enumerate(vals):
        bx = x + w * (0.08 + i * 0.18)
        d.rectangle([bx, y + h * (0.85 - v), bx + bw, y + h * 0.85],
                    fill=(163, 22, 33) if i >= 3 else (90, 90, 90))
    d.line([x + w * 0.06, y + h * 0.12, x + w * 0.94, y + h * 0.72],
           fill=(163, 22, 33), width=3)
    d.polygon([(x + w * 0.94, y + h * 0.72), (x + w * 0.82, y + h * 0.70),
               (x + w * 0.90, y + h * 0.58)], fill=(163, 22, 33))


def art_tank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 205, 150))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(190, 160, 100))
    d.line([x, y + h * 0.68, x + w, y + h * 0.68], fill=(120, 100, 60), width=2)
    tx, ty = x + w * 0.30, y + h * 0.55
    d.rounded_rectangle([tx, ty - h * 0.16, tx + w * 0.34, ty + h * 0.06],
                        radius=6, fill=(90, 95, 70))
    d.rectangle([tx + w * 0.30, ty - h * 0.12, tx + w * 0.55, ty - h * 0.06],
                fill=(70, 75, 55))
    d.ellipse([tx + w * 0.04, ty + h * 0.04, tx + w * 0.12, ty + h * 0.12],
              fill=(60, 65, 45))
    d.ellipse([tx + w * 0.16, ty + h * 0.04, tx + w * 0.24, ty + h * 0.12],
              fill=(60, 65, 45))
    for i in range(6):
        lx = x + w * (0.12 + i * 0.15)
        d.line([lx, y + h * 0.30, lx + 8, y + h * 0.30], fill=(200, 160, 0),
               width=3)
    d.text((x + w * 0.62, y + h * 0.10), "YELLOW LINE", font=font(SANS_B, 9),
           fill=(120, 90, 0))


def art_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    d.rectangle([x + w * 0.12, y + h * 0.20, x + w * 0.60, y + h * 0.82],
                fill=(255, 255, 255), outline=(150, 150, 150))
    for i, ln in enumerate([0.36, 0.30, 0.38, 0.22]):
        d.line([x + w * 0.18, y + h * (0.30 + i * 0.12),
                x + w * (0.18 + ln), y + h * (0.30 + i * 0.12)],
               fill=(120, 120, 120), width=2)
    import math
    gx, gy = x + w * 0.72, y + h * 0.42
    d.line([gx - 14, gy + 18, gx + 14, gy - 18], fill=(110, 70, 40), width=5)
    d.rounded_rectangle([gx - 16, gy - 26, gx + 16, gy - 12], radius=4,
                        fill=(90, 55, 30))
    d.ellipse([gx - 12, gy + 16, gx + 12, gy + 24], fill=(150, 110, 70))


ART = {"summit": art_summit, "court": art_court, "ipo": art_ipo,
       "gta": art_gta, "cop": art_cop, "cyclone": art_cyclone,
       "tower": art_tower, "bridge": art_bridge, "exam": art_exam,
       "ice": art_ice, "jobs": art_jobs, "tank": art_tank,
       "gavel": art_gavel}

# ---------------------------------------------------------------- map
# Dotted world map, 60 cols x 24 rows, lon -180..180, lat 84..-54.
# '#' = land. Positions are approximate by design.
MAP_GRID = [
    "......######................###.........###################....",
    "....##########..............####........#######################..",
    "...############............####...###..#########################.",
    "..##############...........###....######..######################",
    "..###############..........##.....######.#######################",
    "...#############...........########.#########################",
    "....############............######.############################",
    ".....##########............#######.##########################...",
    "......########...........##########################.########...",
    ".......######...........#############################.#####....",
    "........####............############################..###......",
    ".........##.............###########################...##.......",
    "..........##...........##########################....#.........",
    "..........###..........#######################...###..........",
    "...........###.........######################....####..........",
    "...........####........###################......###............",
    "............###........#################.......#####...........",
    "............###.........###############.......########.........",
    ".............##.........##############.......#########.........",
    ".............##..........############........########....##....",
    "..............#...........##########.........######.....##.....",
    "..............#............########............................",
    "...............#...........######..............................",
    "............................................................",
]


def draw_map(d, x, y, w, h, pins):
    """Dotted world map with numbered red pins for the featured stories."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    cols, rows = 60, 24
    cw, ch = w / cols, h / rows
    for r, row in enumerate(MAP_GRID):
        for c, ch_ in enumerate(row[:cols]):
            if ch_ == "#":
                cx = x + (c + 0.5) * cw
                cy = y + (r + 0.5) * ch
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=(235, 230, 215))
    for n, lon, lat in pins:
        px = x + (lon + 180) / 360 * w
        py = y + (84 - lat) / 138 * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(163, 22, 33),
                  outline=(255, 255, 255), width=1)
        fnt = font(SANS_B, 9)
        tw = d.textlength(str(n), font=fnt)
        d.text((px - tw / 2, py - 5), str(n), font=fnt, fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
MARGIN = 14
CW = W - 2 * MARGIN  # 996 usable


def draw_panel(d, st, x, y, w, h, large):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=INK, width=1)
    pad = 8 if large else 6
    art_h = 68 if large else 56
    ART[st["art"]](d, x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 4
    # kicker: number + place + topic
    kick = "%d \u00b7 %s \u00b7 %s" % (st["n"], st["place"], st["topic"])
    kf = font(SANS_B, 11 if large else 9)
    d.text((x + pad, ty), kick, font=kf, fill=RED)
    ty += (15 if large else 13)
    # headline, max 2 lines
    hf, hlines = fit_lines(st["headline"], SERIF_B,
                           [17, 16, 15] if large else [13, 12, 11],
                           w - 2 * pad, 2, d)
    for ln in hlines:
        d.text((x + pad, ty), ln, font=hf, fill=INK)
        ty += (20 if large else 15)
    ty += 2
    # subline: only as many lines as fit above the pinned source line
    src_y = y + h - 13
    lh = 13 if large else 12
    max_sub = max(1, (src_y - 3 - ty) // lh)
    sf, slines = fit_lines(st["sub"], SANS,
                           [11, 10, 9] if large else [10, 9, 8],
                           w - 2 * pad, max_sub, d)
    for ln in slines:
        d.text((x + pad, ty), ln, font=sf, fill=(45, 45, 45))
        ty += lh
    # source, pinned to the bottom
    d.text((x + pad, src_y), "\u2014 " + st["src"],
           font=font(SANS, 8), fill=GREY)


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for st in FEATURED:
        counts[st["region"]] += 1
    for _, _, reg, _ in ALSO:
        counts[reg] += 1
    return counts


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip
    d.text((MARGIN, 6), "THE WHOLE WORLD IN A DAY", font=font(SANS_B, 12),
           fill=INK)
    rt = "40 STORIES \u00b7 ONE DAY \u00b7 EVERY CONTINENT"
    rf = font(SANS_B, 10)
    d.text((W - MARGIN - d.textlength(rt, font=rf), 8), rt, font=rf, fill=RED)
    d.line([MARGIN, 26, W - MARGIN, 26], fill=RULE, width=2)

    # ---- masthead: the date is the headline
    mf = font(SERIF_B, 56)
    d.text((MARGIN, 30), "Thursday 19 November 2026", font=mf, fill=INK)
    sub = ("Trump, Xi and Putin share one table \u00b7 The World Court finds "
           "genocide in Myanmar \u00b7 The biggest IPO ever starts trading")
    sf = font(SERIF_I, 16)
    if d.textlength(sub, font=sf) > CW:
        sf = font(SERIF_I, 15)
    d.text((MARGIN, 96), sub, font=sf, fill=RED)
    d.line([MARGIN, 118, W - MARGIN, 118], fill=RULE, width=1)

    # ---- region chips (computed from the story data, always consistent)
    counts = region_counts()
    cx = MARGIN
    cy = 124
    for reg in REGION_ORDER:
        label = "%s %d" % (reg.upper(), counts[reg])
        fnt = font(SANS_B, 10)
        tw = d.textlength(label, font=fnt)
        d.rectangle([cx, cy, cx + tw + 12, cy + 20], fill=REGION_COLORS[reg])
        d.text((cx + 6, cy + 4), label, font=fnt, fill=(255, 255, 255))
        cx += tw + 12 + 6
    d.line([MARGIN, 150, W - MARGIN, 150], fill=RULE, width=1)

    # ---- number strip
    cell_w = CW / len(NUMBERS)
    for i, (num, cap) in enumerate(NUMBERS):
        x0 = MARGIN + i * cell_w
        nf = font(SANS_B, 22)
        d.text((x0 + (cell_w - d.textlength(num, font=nf)) / 2, 156), num,
               font=nf, fill=RED)
        cf = font(SANS, 9)
        d.text((x0 + (cell_w - d.textlength(cap, font=cf)) / 2, 182), cap,
               font=cf, fill=(60, 60, 60))
        if i:
            d.line([x0, 156, x0, 194], fill=(200, 192, 175), width=1)
    d.line([MARGIN, 200, W - MARGIN, 200], fill=RULE, width=1)

    # ---- 3 large panels
    gap = 8
    lw = (CW - 2 * gap) // 3
    for i, st in enumerate(FEATURED[:3]):
        draw_panel(d, st, MARGIN + i * (lw + gap), 206, lw, 188, True)

    # ---- 10 small panels, 2 rows of 5
    sw = (CW - 4 * gap) // 5
    for r in range(2):
        for c in range(5):
            st = FEATURED[3 + r * 5 + c]
            draw_panel(d, st, MARGIN + c * (sw + gap), 400 + r * 166,
                       sw, 160, False)

    # ---- bottom: map + also list
    by = 732
    bh = 168
    map_w = 440
    d.rectangle([MARGIN, by, MARGIN + map_w, by + bh], outline=INK, width=1)
    d.text((MARGIN + 8, by + 5), "WHERE IT HAPPENED", font=font(SANS_B, 11),
           fill=RED)
    pins = [(st["n"], st["lon"], st["lat"]) for st in FEATURED]
    draw_map(d, MARGIN + 8, by + 24, map_w - 16, bh - 44, pins)
    d.text((MARGIN + 8, by + bh - 16),
           "Red numbers mark stories 1\u201313. Positions are approximate.",
           font=font(SANS, 8), fill=GREY)

    ax = MARGIN + map_w + 8
    aw = W - MARGIN - ax
    d.rectangle([ax, by, ax + aw, by + bh], outline=INK, width=1)
    d.text((ax + 8, by + 5), "ALSO ON THURSDAY 19 NOVEMBER \u2014 27 MORE STORIES",
           font=font(SANS_B, 11), fill=RED)
    col_w = (aw - 16) // 2
    row_h = (bh - 26) // 14
    for idx, (n, place, _reg, text) in enumerate(ALSO):
        col = idx // 14
        row = idx % 14
        ix = ax + 8 + col * col_w
        iy = by + 26 + row * row_h
        head = "%d %s " % (n, place)
        for size in (8, 7):
            bfnt = font(SANS_B, size)
            fnt = font(SANS, size)
            if (d.textlength(head, font=bfnt)
                    + d.textlength(text, font=fnt) <= col_w - 4):
                break
        d.text((ix, iy), head, font=bfnt, fill=RED)
        d.text((ix + d.textlength(head, font=bfnt), iy),
               text, font=fnt, fill=INK)

    # ---- date check
    dy = 906
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 58], outline=RED, width=2)
    df = font(SANS, 10)
    dlines = wrap(DATE_CHECK, df, CW - 20, d)
    ty = dy + 6
    for ln in dlines:
        d.text((MARGIN + 10, ty), ln, font=df, fill=INK)
        ty += 13

    # ---- footer
    ff = font(SANS, 8)
    flines = wrap(FOOTER, ff, CW, d)
    ty = 972
    for ln in flines:
        d.text((MARGIN, ty), ln, font=ff, fill=GREY)
        ty += 11

    img.save(OUT, "JPEG", quality=88)
    return OUT


if __name__ == "__main__":
    import hashlib
    p = build()
    b = open(p, "rb").read()
    print(p, len(b), "bytes, sha256", hashlib.sha256(b).hexdigest())
    im = Image.open(p)
    print(im.size, im.format)
