from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("assets/placeholders")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 1000

FILES = [
    ("bakeries.png", "BAKERIES", "Fresh bread, pastries, and cakes", (247, 132, 35), "bakeries"),
    ("coffee_roasteries.png", "COFFEE", "Specialty roasts and espresso", (160, 104, 56), "coffee"),
    ("breweries.png", "BREWERIES", "Local beer and craft brewing", (40, 100, 184), "breweries"),
    ("distilleries.png", "DISTILLERIES", "Small-batch spirits and gin", (112, 76, 180), "distilleries"),
    ("delicatessen.png", "DELI", "Fine foods, cured meats, and pantry goods", (78, 167, 126), "deli"),
    ("butcher_shops.png", "BUTCHERS", "Quality meats and specialist cuts", (227, 58, 64), "butcher"),
    ("seafood_producers.png", "SEAFOOD", "Fresh fish and shellfish", (34, 161, 201), "seafood"),
    ("local_soft_drinks.png", "SOFT DRINKS", "Sodas, tonics, and non-alcoholic blends", (249, 180, 40), "soft_drinks"),
    ("local_snacks.png", "SNACKS", "Bites, bars, and savory treats", (220, 88, 132), "snacks"),
    ("fruits_and_vegetables.png", "PRODUCE", "Seasonal fruit, vegetables, and herbs", (111, 173, 81), "produce"),
    ("default.png", "PRODUCER", "No image available", (160, 160, 165), "default"),
]

# -----------------------
# Fonts
# -----------------------
def load_font(size, bold=False):
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
            "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else
        [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttf",
            "/System/Library/Fonts/Supplemental/Verdana.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()

TITLE_FONT = load_font(84, bold=True)
SUB_FONT = load_font(34, bold=False)
SMALL_FONT = load_font(28, bold=False)
PILL_FONT = load_font(34, bold=True)

# -----------------------
# Helpers
# -----------------------
def blend(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def make_background(base_rgb, accent_rgb):
    base = Image.new("RGBA", (W, H), (*base_rgb, 255))
    tint = blend(base_rgb, accent_rgb, 0.12)
    top = Image.new("RGBA", (W, H), (*tint, 255))
    mask = Image.linear_gradient("L").resize((W, H))
    return Image.composite(top, base, mask)

def draw_soft_blobs(draw, accent_rgb):
    for x1, y1, x2, y2, alpha in [
        (-120, -120, 430, 350, 24),
        (1160, -160, 1750, 280, 20),
        (1140, 760, 1760, 1200, 18),
        (-220, 720, 350, 1200, 16),
    ]:
        draw.ellipse((x1, y1, x2, y2), fill=(*accent_rgb, alpha))

def draw_card(draw, accent_rgb):
    draw.rounded_rectangle((82, 62, W - 72, H - 58), radius=42, fill=(0, 0, 0, 18))
    draw.rounded_rectangle(
        (70, 50, W - 90, H - 80),
        radius=42,
        fill=(255, 255, 255, 240),
        outline=(*accent_rgb, 40),
        width=3,
    )

def draw_pill(draw, title, accent_rgb):
    x1, y1, x2, y2 = 110, 112, 500, 198
    draw.rounded_rectangle((x1, y1, x2, y2), radius=28, fill=(*accent_rgb, 255))
    bbox = draw.textbbox((0, 0), title, font=PILL_FONT)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        (x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 2),
        title,
        fill=(255, 255, 255),
        font=PILL_FONT,
    )

def draw_dots(draw, accent_rgb):
    for i in range(5):
        x = 120 + i * 34
        y = 225
        draw.ellipse((x, y, x + 11, y + 11), fill=(*accent_rgb, 200))

def text_centered(draw, text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, fill=fill, font=font)

def draw_footer(draw, subtitle, accent_rgb):
    text_centered(draw, "No image available", 705, TITLE_FONT, (25, 25, 30))
    text_centered(draw, subtitle, 812, SUB_FONT, (95, 95, 104))
    text_centered(draw, "Range Innovation", 875, SMALL_FONT, (*accent_rgb, 220))

def draw_icon_badge(draw, accent_rgb):
    cx, cy = 780, 430
    # softer background badge
    draw.ellipse((cx - 220, cy - 220, cx + 220, cy + 220), fill=(*accent_rgb, 70))
    # white disc with colored ring
    draw.ellipse((cx - 165, cy - 165, cx + 165, cy + 165), fill=(255, 255, 255, 245))
    draw.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), outline=accent_rgb, width=16)
    return cx, cy

# -----------------------
# Icon drawing helpers
# -----------------------
def draw_bakery(draw, cx, cy, c):
    # loaf
    draw.rounded_rectangle((cx - 120, cy - 22, cx + 120, cy + 74), radius=38, fill=c)
    # scoring
    for dx in (-60, 0, 60):
        draw.line((cx + dx - 18, cy - 2, cx + dx + 20, cy + 26), fill=(255, 255, 255), width=8)
    # steam
    for dx in (-48, 0, 48):
        draw.arc((cx + dx - 28, cy - 100, cx + dx + 28, cy - 40), start=180, end=350, fill=c, width=8)

def draw_coffee(draw, cx, cy, c):
    # cup body
    draw.rounded_rectangle((cx - 100, cy - 8, cx + 72, cy + 102), radius=26, fill=c)
    # handle
    draw.arc((cx + 42, cy + 6, cx + 132, cy + 82), start=265, end=95, fill=c, width=12)
    # saucer
    draw.line((cx - 94, cy + 112, cx + 68, cy + 112), fill=c, width=12)
    # steam
    draw.arc((cx - 62, cy - 124, cx - 2, cy - 20), start=200, end=340, fill=c, width=8)
    draw.arc((cx + 6, cy - 132, cx + 68, cy - 20), start=200, end=340, fill=c, width=8)

def draw_breweries(draw, cx, cy, c):
    # hop cone: a stack of filled petals
    petals = [
        (cx - 36, cy - 112, cx + 36, cy - 42),
        (cx - 68, cy - 70, cx - 4, cy + 6),
        (cx + 4, cy - 70, cx + 68, cy + 6),
        (cx - 52, cy - 16, cx + 52, cy + 66),
    ]
    for box in petals:
        draw.ellipse(box, fill=c)
    draw.line((cx, cy + 62, cx, cy + 126), fill=c, width=10)
    draw.line((cx - 18, cy + 92, cx + 18, cy + 92), fill=c, width=10)

def draw_distillery(draw, cx, cy, c):
    # bottle
    draw.polygon(
        [
            (cx - 36, cy - 128), (cx + 12, cy - 128),
            (cx + 12, cy - 98), (cx + 34, cy - 78),
            (cx + 34, cy + 114), (cx - 58, cy + 114),
            (cx - 58, cy - 78), (cx - 36, cy - 98)
        ],
        fill=c
    )
    # label
    draw.rounded_rectangle((cx - 46, cy - 10, cx + 22, cy + 34), radius=10, fill=(255, 255, 255))
    # glass
    draw.ellipse((cx + 58, cy - 4, cx + 132, cy + 94), outline=c, width=10)
    draw.line((cx + 95, cy + 94, cx + 95, cy + 126), fill=c, width=8)

def draw_deli(draw, cx, cy, c):
    # cheese wedge
    draw.polygon([(cx - 122, cy + 54), (cx - 12, cy - 100), (cx + 128, cy - 54), (cx + 28, cy + 90)], fill=c)
    # holes
    for bx, by, r in [(-52, -20, 14), (8, -40, 10), (44, 0, 12)]:
        draw.ellipse((cx + bx - r, cy + by - r, cx + bx + r, cy + by + r), fill=(255, 255, 255))
    # base line
    draw.line((cx - 108, cy + 54, cx + 28, cy + 54), fill=(255, 255, 255), width=8)

def draw_butcher(draw, cx, cy, c):
    # steak
    draw.ellipse((cx - 130, cy - 20, cx + 94, cy + 98), fill=c)
    # marbling
    draw.ellipse((cx - 34, cy + 4, cx + 6, cy + 44), fill=(255, 255, 255))
    draw.ellipse((cx + 14, cy - 6, cx + 46, cy + 26), fill=(255, 255, 255))
    # bone/handle hint
    draw.line((cx + 104, cy - 92, cx + 154, cy - 42), fill=c, width=12)
    draw.line((cx + 154, cy - 42, cx + 132, cy - 20), fill=c, width=12)

def draw_seafood(draw, cx, cy, c):
    # fish
    draw.ellipse((cx - 130, cy - 40, cx + 48, cy + 72), fill=c)
    draw.polygon([(cx + 48, cy - 40), (cx + 150, cy + 12), (cx + 48, cy + 72)], fill=c)
    # eye
    draw.ellipse((cx - 84, cy - 2, cx - 68, cy + 14), fill=(255, 255, 255))
    # fin
    draw.polygon([(cx - 8, cy - 18), (cx + 28, cy + 12), (cx + 0, cy + 32)], fill=(255, 255, 255))

def draw_soft_drinks(draw, cx, cy, c):
    # bottle
    draw.polygon(
        [
            (cx - 36, cy - 126), (cx + 12, cy - 126),
            (cx + 12, cy - 98), (cx + 34, cy - 78),
            (cx + 34, cy + 114), (cx - 58, cy + 114),
            (cx - 58, cy - 78), (cx - 36, cy - 98)
        ],
        fill=c
    )
    # bubbles
    for bx, by, r in [(-102, -32, 10), (82, -26, 12), (108, 18, 8), (22, 56, 10)]:
        draw.ellipse((cx + bx - r, cy + by - r, cx + bx + r, cy + by + r), outline=c, width=7)

def draw_snacks(draw, cx, cy, c):
    # packet
    draw.polygon([(cx - 104, cy - 116), (cx + 24, cy - 116), (cx + 78, cy + 102), (cx - 62, cy + 102)], fill=c)
    # label band
    draw.rectangle((cx - 80, cy - 80, cx + 8, cy - 62), fill=(255, 255, 255))
    # chips
    for bx, by in [(102, -8), (128, 16), (110, 40)]:
        draw.ellipse((cx + bx - 14, cy + by - 14, cx + bx + 14, cy + by + 14), fill=(255, 255, 255))

def draw_produce(draw, cx, cy, c):
    # basket
    draw.arc((cx - 124, cy - 6, cx + 124, cy + 126), start=180, end=360, fill=c, width=12)
    draw.line((cx - 92, cy + 96, cx + 92, cy + 96), fill=c, width=12)
    draw.line((cx - 52, cy + 18, cx - 18, cy + 96), fill=c, width=8)
    draw.line((cx + 2, cy + 8, cx + 2, cy + 96), fill=c, width=8)
    draw.line((cx + 52, cy + 18, cx + 18, cy + 96), fill=c, width=8)
    # produce
    draw.ellipse((cx - 122, cy - 112, cx - 58, cy - 48), fill=c)
    draw.ellipse((cx - 14, cy - 132, cx + 58, cy - 62), fill=c)
    draw.polygon([(cx + 84, cy - 28), (cx + 118, cy - 82), (cx + 150, cy - 28)], fill=c)

def draw_default(draw, cx, cy, c):
    # generic producer silhouette
    draw.ellipse((cx - 60, cy - 118, cx + 60, cy + 2), outline=c, width=10)
    draw.rounded_rectangle((cx - 90, cy + 10, cx + 90, cy + 124), radius=32, outline=c, width=10)
    draw.line((cx - 90, cy + 124, cx - 90, cy + 168), fill=c, width=10)
    draw.line((cx + 90, cy + 124, cx + 90, cy + 168), fill=c, width=10)

ICON_FUNCS = {
    "bakeries": draw_bakery,
    "coffee": draw_coffee,
    "breweries": draw_breweries,
    "distilleries": draw_distillery,
    "deli": draw_deli,
    "butcher": draw_butcher,
    "seafood": draw_seafood,
    "soft_drinks": draw_soft_drinks,
    "snacks": draw_snacks,
    "produce": draw_produce,
    "default": draw_default,
}

# -----------------------
# Render
# -----------------------
def make_one(filename, title, subtitle, accent, icon_key):
    base = (251, 248, 242)
    img = make_background(base, blend(base, accent, 0.16))
    draw = ImageDraw.Draw(img, "RGBA")

    draw_soft_blobs(draw, accent)
    draw_card(draw, accent)
    draw_pill(draw, title, accent)
    draw_dots(draw, accent)

    cx, cy = draw_icon_badge(draw, accent)
    ICON_FUNCS.get(icon_key, draw_default)(draw, cx, cy, accent)

    draw_footer(draw, subtitle, accent)
    img.save(OUT / filename)

def main():
    for filename, title, subtitle, accent, icon_key in FILES:
        make_one(filename, title, subtitle, accent, icon_key)
        print(f"wrote {OUT / filename}")

if __name__ == "__main__":
    main()