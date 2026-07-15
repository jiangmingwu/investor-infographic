from __future__ import annotations

import base64
import hashlib
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OFFICIAL_LOGO_ASSETS = {
    "ccb": {
        "path": "/Users/jiangming/templates/assets/company_logos/ccb-official.png",
        "source_url": "https://www2.ccb.com/chn/fileDir/bg_image/2020031015231379393.png",
        "retrieved": "2026-06-24",
        "sha256": "e0eb33430eb24b7844480172a7186181cf7a4d0cd393cb584137c0cefb6c43b6",
    },
    "kioxia": {
        "path": "/Users/jiangming/templates/assets/company_logos/kioxia-official.png",
        "source_url": "https://www.kioxia-holdings.com/etc.clientlibs/kioxia-libs/clientlibs/kioxia/resources/component/kioxia_logo.svg",
        "retrieved": "2026-07-04",
        "sha256": "b23a0a5018ab234a9436c0d61c643775cbf92c047bb1086232c63834a3e206e9",
    },
    "unitedhealth": {
        "path": "/Users/jiangming/templates/assets/company_logos/unitedhealth-official.png",
        "source_url": "https://www.unitedhealthgroup.com/content/dam/UHG/Images/_corporate/_logos/logos-uhg.zip",
        "retrieved": "2026-07-04",
        "sha256": "bdb317900b892f5593ae3026790670b3a56c161b35dabe94c2e98e7e4b1aebfb",
    },
    "morganstanley": {
        "path": "/Users/jiangming/templates/assets/company_logos/morganstanley-official.png",
        "source_url": "https://www.morganstanley.com/content/dam/msdotcom/newsroom/media-resources/MorganStanley_Logo_Black.zip",
        "retrieved": "2026-07-04",
        "sha256": "5e27e942d803e55231e501664599357b3b8d5e721b325743c46f6afa30d3185b",
    },
}


LOGO_SLUGS = {
    "mastercard",
    "costco",
    "intel",
    "netflix",
    "caterpillar",
    "bankofamerica",
    "ccb",
    "abbvie",
    "ge",
    "kioxia",
    "unitedhealth",
    "morganstanley",
}


def _font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ]
    for path in candidates:
        if path and Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _official_logo_record(slug: str) -> dict[str, str] | None:
    record = OFFICIAL_LOGO_ASSETS.get(slug)
    if not record:
        return None

    asset_path = Path(record["path"])
    if not asset_path.is_file():
        raise FileNotFoundError(f"Missing official logo asset for {slug}: {asset_path}")
    actual_hash = hashlib.sha256(asset_path.read_bytes()).hexdigest()
    if actual_hash != record["sha256"]:
        raise ValueError(f"Official logo asset hash mismatch for {slug}")
    return record


def _official_logo_svg(slug: str, label: str) -> str | None:
    record = _official_logo_record(slug)
    if not record:
        return None

    data = base64.b64encode(Path(record["path"]).read_bytes()).decode("ascii")
    source = escape(record["source_url"], quote=True)
    return f"""
<svg role="img" aria-label="{label}" data-brand-source="{source}" viewBox="0 0 600 120" xmlns="http://www.w3.org/2000/svg">
  <image href="data:image/png;base64,{data}" x="0" y="0" width="600" height="120" preserveAspectRatio="xMidYMid meet"/>
</svg>"""


def logo_svg(slug: str, label: str | None = None) -> str:
    label = escape(label or slug)
    official_svg = _official_logo_svg(slug, label)
    if official_svg:
        return official_svg

    svgs = {
        "mastercard": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 180 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="72" cy="50" r="35" fill="#EB001B"/>
  <circle cx="108" cy="50" r="35" fill="#F79E1B" fill-opacity=".92"/>
  <text x="90" y="102" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="700" fill="#231F20">mastercard</text>
</svg>""",
        "costco": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <text x="110" y="53" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="42" font-weight="900" fill="#E31837">COSTCO</text>
  <path d="M24 65h172" stroke="#005DAA" stroke-width="7" stroke-linecap="round"/>
  <text x="110" y="91" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="22" font-weight="900" fill="#005DAA" letter-spacing="1.2">WHOLESALE</text>
</svg>""",
        "intel": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 180 120" xmlns="http://www.w3.org/2000/svg">
  <text x="90" y="76" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, Helvetica, sans-serif" font-size="64" font-weight="800" fill="#0068B5">intel</text>
</svg>""",
        "netflix": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <path d="M31 17h18l41 86H72L31 17z" fill="#B20710"/>
  <path d="M72 17h18v86H72z" fill="#E50914"/>
  <path d="M31 17h18v86H31z" fill="#E50914"/>
  <path d="M49 17l23 86h18L49 17z" fill="#831010" opacity=".55"/>
</svg>""",
        "caterpillar": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <rect x="18" y="25" width="184" height="70" rx="6" fill="#111111"/>
  <path d="M91 90l19-43 19 43z" fill="#F7C600"/>
  <text x="110" y="76" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="58" font-weight="900" fill="#FFFFFF">CAT</text>
</svg>""",
        "bankofamerica": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(44 16) skewX(-13)">
    <rect x="0" y="0" width="42" height="13" fill="#D4001A"/>
    <rect x="50" y="0" width="42" height="13" fill="#D4001A"/>
    <rect x="17" y="23" width="42" height="13" fill="#004C97"/>
    <rect x="67" y="23" width="42" height="13" fill="#004C97"/>
    <rect x="0" y="46" width="42" height="13" fill="#D4001A"/>
    <rect x="50" y="46" width="42" height="13" fill="#D4001A"/>
  </g>
  <text x="110" y="101" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="700" fill="#004C97">Bank of America</text>
</svg>""",
        "abbvie": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <text x="110" y="70" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, Helvetica, sans-serif" font-size="52" font-weight="800" fill="#C2185B">AbbVie</text>
</svg>""",
        "ge": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 180 120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="90" cy="58" r="42" fill="#0A5CAA"/>
  <circle cx="90" cy="58" r="34" fill="none" stroke="#FFFFFF" stroke-width="4"/>
  <text x="90" y="75" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-size="48" font-style="italic" font-weight="700" fill="#FFFFFF">GE</text>
</svg>""",
        "kioxia": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <text x="110" y="72" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="43" font-weight="900" fill="#B0007A">KIOXIA</text>
</svg>""",
        "unitedhealth": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 220 120" xmlns="http://www.w3.org/2000/svg">
  <path d="M48 25h46l12 16v45H48z" fill="#005DAA"/>
  <path d="M60 38h26v9H60zM60 55h34v9H60zM60 72h25v9H60z" fill="#FFFFFF"/>
  <text x="153" y="55" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="800" fill="#005DAA">UnitedHealth</text>
  <text x="153" y="82" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#005DAA">Group</text>
</svg>""",
        "morganstanley": f"""
<svg role="img" aria-label="{label}" viewBox="0 0 240 120" xmlns="http://www.w3.org/2000/svg">
  <text x="120" y="57" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-size="34" font-weight="700" fill="#1E4E8C">Morgan</text>
  <text x="120" y="88" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-size="34" font-weight="700" fill="#1E4E8C">Stanley</text>
</svg>""",
    }
    if slug not in svgs:
        raise KeyError(f"Missing verified logo asset for {slug}")
    return svgs[slug]


def logo_mark_html(slug: str, label: str | None = None) -> str:
    return f"<div class='mark logo-mark'>{logo_svg(slug, label)}</div>"


def logo_chip_html(slug: str, label: str | None = None) -> str:
    return f"<div class='brand-chip'>{logo_svg(slug, label)}</div>"


def draw_company_logo(draw: ImageDraw.ImageDraw, slug: str, box: tuple[int, int, int, int]) -> bool:
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    cx = x0 + w / 2

    official = _official_logo_record(slug)
    if official:
        logo = Image.open(official["path"]).convert("RGBA")
        max_w = max(1, int(w * 0.88))
        max_h = max(1, int(h * 0.72))
        logo.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        px = int(x0 + (w - logo.width) / 2)
        py = int(y0 + (h - logo.height) / 2)
        draw._image.paste(logo, (px, py), logo)
        return True

    if slug == "mastercard":
        r = int(min(w, h) * 0.24)
        cy = y0 + int(h * 0.43)
        draw.ellipse([cx - r * 1.25, cy - r, cx + r * 0.75, cy + r], fill="#EB001B")
        draw.ellipse([cx - r * 0.75, cy - r, cx + r * 1.25, cy + r], fill="#F79E1B")
        font = _font(int(h * 0.16), True)
        text = "mastercard"
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, y0 + int(h * 0.74)), text, fill="#231F20", font=font)
        return True

    if slug == "costco":
        font_top = _font(int(h * 0.28), True)
        font_bottom = _font(int(h * 0.15), True)
        top = "COSTCO"
        bottom = "WHOLESALE"
        tw = draw.textlength(top, font=font_top)
        draw.text((cx - tw / 2, y0 + int(h * 0.22)), top, fill="#E31837", font=font_top)
        line_y = y0 + int(h * 0.58)
        draw.line([x0 + int(w * 0.12), line_y, x1 - int(w * 0.12), line_y], fill="#005DAA", width=max(3, int(h * 0.04)))
        bw = draw.textlength(bottom, font=font_bottom)
        draw.text((cx - bw / 2, y0 + int(h * 0.64)), bottom, fill="#005DAA", font=font_bottom)
        return True

    if slug == "intel":
        font = _font(int(h * 0.45), True)
        text = "intel"
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, y0 + int(h * 0.28)), text, fill="#0068B5", font=font)
        return True

    if slug == "netflix":
        red = "#E50914"
        dark = "#8A0F12"
        left = x0 + int(w * 0.28)
        top = y0 + int(h * 0.15)
        bw = int(w * 0.16)
        bh = int(h * 0.72)
        draw.rectangle([left, top, left + bw, top + bh], fill=red)
        draw.polygon([(left + bw, top), (left + bw * 2, top), (left + bw * 3, top + bh), (left + bw * 2, top + bh)], fill=dark)
        draw.rectangle([left + bw * 2, top, left + bw * 3, top + bh], fill=red)
        return True

    if slug == "caterpillar":
        rect = [x0 + int(w * 0.07), y0 + int(h * 0.20), x1 - int(w * 0.07), y1 - int(h * 0.18)]
        draw.rounded_rectangle(rect, radius=int(h * 0.05), fill="#111111")
        font = _font(int(h * 0.42), True)
        text = "CAT"
        tw = draw.textlength(text, font=font)
        tx = cx - tw / 2
        ty = y0 + int(h * 0.33)
        draw.text((tx, ty), text, fill="#FFFFFF", font=font)
        draw.polygon([(cx - int(w * 0.09), y1 - int(h * 0.21)), (cx, y0 + int(h * 0.44)), (cx + int(w * 0.09), y1 - int(h * 0.21))], fill="#F7C600")
        return True

    if slug == "bankofamerica":
        red = "#D4001A"
        blue = "#004C97"
        stripe_w = int(w * 0.25)
        stripe_h = max(5, int(h * 0.09))
        sx = x0 + int(w * 0.23)
        sy = y0 + int(h * 0.12)
        for row, color in enumerate([red, blue, red]):
            y = sy + row * int(h * 0.22)
            draw.polygon([(sx, y), (sx + stripe_w, y), (sx + stripe_w - int(w * 0.08), y + stripe_h), (sx - int(w * 0.08), y + stripe_h)], fill=color)
            draw.polygon([(sx + int(w * 0.34), y), (sx + int(w * 0.34) + stripe_w, y), (sx + int(w * 0.34) + stripe_w - int(w * 0.08), y + stripe_h), (sx + int(w * 0.34) - int(w * 0.08), y + stripe_h)], fill=color)
        font = _font(int(h * 0.14), True)
        text = "Bank of America"
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, y0 + int(h * 0.76)), text, fill=blue, font=font)
        return True

    if slug == "abbvie":
        font = _font(int(h * 0.34), True)
        text = "AbbVie"
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, y0 + int(h * 0.34)), text, fill="#C2185B", font=font)
        return True

    if slug == "ge":
        blue = "#0A5CAA"
        r = int(min(w, h) * 0.34)
        cy = y0 + int(h * 0.48)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=blue)
        draw.ellipse([cx - int(r * .82), cy - int(r * .82), cx + int(r * .82), cy + int(r * .82)], outline="#FFFFFF", width=max(2, int(h * .025)))
        font = _font(int(h * 0.34), True)
        text = "GE"
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, cy - int(h * 0.18)), text, fill="#FFFFFF", font=font)
        return True

    if slug == "kioxia":
        font = _font(int(h * 0.30), True)
        text = "KIOXIA"
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, y0 + int(h * 0.36)), text, fill="#B0007A", font=font)
        return True

    if slug == "unitedhealth":
        blue = "#005DAA"
        sx = x0 + int(w * 0.10)
        sy = y0 + int(h * 0.20)
        draw.rounded_rectangle([sx, sy, sx + int(w * 0.28), sy + int(h * 0.50)], radius=int(h * 0.03), fill=blue)
        for i, ww in enumerate([0.18, 0.23, 0.15]):
            yy = sy + int(h * (0.11 + 0.14 * i))
            draw.rectangle([sx + int(w * 0.06), yy, sx + int(w * (0.06 + ww)), yy + int(h * 0.045)], fill="#FFFFFF")
        font = _font(int(h * 0.16), True)
        text = "UnitedHealth"
        draw.text((x0 + int(w * 0.43), y0 + int(h * 0.30)), text, fill=blue, font=font)
        font2 = _font(int(h * 0.15), True)
        draw.text((x0 + int(w * 0.43), y0 + int(h * 0.50)), "Group", fill=blue, font=font2)
        return True

    if slug == "morganstanley":
        font = _font(int(h * 0.20), True)
        text1 = "Morgan"
        text2 = "Stanley"
        tw1 = draw.textlength(text1, font=font)
        tw2 = draw.textlength(text2, font=font)
        draw.text((cx - tw1 / 2, y0 + int(h * 0.27)), text1, fill="#1E4E8C", font=font)
        draw.text((cx - tw2 / 2, y0 + int(h * 0.50)), text2, fill="#1E4E8C", font=font)
        return True

    return False
