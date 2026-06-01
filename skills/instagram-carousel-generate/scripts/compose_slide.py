#!/usr/bin/env python3
"""Composite one carousel slide: a generated background + exact text + logo → 1080x1350 PNG.

The image model renders only the world (sky/grass/Clawd/blank card). This script draws all
copy with the bundled fonts and pastes the real logo PNG, so text and brand marks are
pixel-accurate and on-brand. Pure Pillow, no network.

Usage:
    python compose_slide.py --slide-json slide.json --background bg.png --out slide-01.png
    # slide.json is one slide block from carousel-spec.md, as JSON (the orchestrator writes it).

A slide dict looks like:
    {"type":"item","badge":"01/5","headline":"...","subhead":"...","bullets":["..."],
     "open_loop_tail":"...","accent_hex":"#2BAADF","logo_file":"github-logo.png",
     "url":"github.com/owner/repo","handle":"@erictech","mimic_ui":"none"}
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
MARGIN = 80
BOTTOM_SAFE = H - 420  # keep load-bearing copy above this y

# ---- colors -----------------------------------------------------------------
TEXT = "#0F172A"
MUTED = "#475569"
CARD = "#F4EEE2"
BORDER = "#E2E8F0"
WHITE = "#FFFFFF"
DEFAULT_ACCENT = "#2BAADF"

# family -> (variable-font filename, preferred named instance, static fallbacks)
FONT_SPECS = {
    "archivo":      ("Archivo.ttf", "Black", ["Archivo-Black.ttf", "Archivo-Bold.ttf"]),
    "archivo-bold": ("Archivo.ttf", "Bold", ["Archivo-Bold.ttf", "Archivo-Black.ttf"]),
    "grotesk":      ("SpaceGrotesk.ttf", "Regular", ["SpaceGrotesk-Regular.ttf"]),
    "grotesk-bold": ("SpaceGrotesk.ttf", "Bold", ["SpaceGrotesk-Bold.ttf", "SpaceGrotesk-Medium.ttf"]),
    "mono":         ("JetBrainsMono.ttf", "SemiBold", ["JetBrainsMono-SemiBold.ttf", "JetBrainsMono-Medium.ttf"]),
}


def resolve_assets() -> Path:
    """Asset resolution contract: env → skill-relative → ~/.claude install."""
    candidates = []
    env = os.environ.get("IG_CAROUSEL_ASSETS")
    if env:
        candidates.append(Path(env))
    # scripts/ → [0]=scripts [1]=<skill> [2]=skills [3]=repo-root-or-.claude [4]=project-root
    here = Path(__file__).resolve()
    candidates.append(here.parents[2])                       # bare-clone fallback (skills/ has no assets)
    if len(here.parents) > 3:
        candidates.append(here.parents[3])                   # bare clone: repo root holds assets/
        candidates.append(here.parents[3] / "instagram-carousel")   # install.sh: .claude/instagram-carousel
    if len(here.parents) > 4:
        candidates.append(here.parents[4] / "instagram-carousel")
    candidates.append(Path.home() / ".claude" / "instagram-carousel")
    for base in candidates:
        if (base / "assets" / "fonts").is_dir() or (base / "fonts").is_dir():
            return base
    # fall back to the first existing candidate so the script still runs with default fonts
    for base in candidates:
        if base.exists():
            return base
    return here.parent


def font(assets: Path, family: str, size: int) -> ImageFont.FreeTypeFont:
    fonts_dir = assets / "assets" / "fonts"
    if not fonts_dir.is_dir():
        fonts_dir = assets / "fonts"
    var_file, instance, fallbacks = FONT_SPECS.get(family, ("", "Regular", []))
    # prefer the variable font + named instance (weight)
    p = fonts_dir / var_file
    if p.exists():
        try:
            f = ImageFont.truetype(str(p), size)
            try:
                f.set_variation_by_name(instance)
            except (OSError, ValueError, AttributeError):
                pass
            return f
        except OSError:
            pass
    for name in fallbacks:                       # static weights, if a user added them
        sp = fonts_dir / name
        if sp.exists():
            try:
                return ImageFont.truetype(str(sp), size)
            except OSError:
                pass
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)  # common on CI/Linux
    except OSError:
        return ImageFont.load_default()


def logo_path(assets: Path, logo_file: str) -> Path | None:
    if not logo_file or logo_file in ("none", "-", ""):
        return None
    for base in (assets / "character-references", assets):
        p = base / logo_file
        if p.exists():
            return p
    return None


# ---- drawing helpers --------------------------------------------------------
def text_w(draw, s, fnt, tracking=0.0):
    if not tracking:
        return draw.textlength(s, font=fnt)
    return sum(draw.textlength(ch, font=fnt) + tracking for ch in s)


def draw_tracked(draw, xy, s, fnt, fill, tracking=0.0):
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, assets, s, max_w, start, min_size, max_lines, family="archivo"):
    """Shrink an Archivo headline until it fits max_w within max_lines."""
    size = start
    while size >= min_size:
        fnt = font(assets, family, size)
        lines = wrap(draw, s, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines, size
        size -= 4
    fnt = font(assets, family, min_size)
    return fnt, wrap(draw, s, fnt, max_w), min_size


def rounded_pill(draw, text, cx, y, assets, fill=CARD, fg=TEXT, border=BORDER):
    fnt = font(assets, "mono", 24)
    tracking = 2.0
    tw = text_w(draw, text.upper(), fnt, tracking)
    pad_x, pad_y = 20, 12
    w = tw + pad_x * 2
    h = 30 + pad_y * 2
    x0 = cx - w / 2
    draw.rounded_rectangle([x0, y, x0 + w, y + h], radius=h / 2, fill=fill, outline=border, width=1)
    draw_tracked(draw, (x0 + pad_x, y + pad_y - 2), text.upper(), fnt, fg, tracking)
    return y + h


def accent_marker(draw, x, y, size, color):
    draw.rounded_rectangle([x, y, x + size, y + size], radius=3, fill=color)


# ---- main composition -------------------------------------------------------
def safe_accent(value: str) -> str:
    """Return a Pillow-parseable color, falling back to DEFAULT_ACCENT.

    Spec fields may carry placeholders (e.g. "<tool hex>") or typos; a bad
    accent must not crash the whole compose run.
    """
    from PIL import ImageColor
    if value:
        try:
            ImageColor.getrgb(value)
            return value
        except (ValueError, AttributeError):
            pass
    return DEFAULT_ACCENT


def crop_cover(bg: Image.Image) -> Image.Image:
    bg = bg.convert("RGB")
    bw, bh = bg.size
    scale = max(W / bw, H / bh)
    nb = bg.resize((round(bw * scale), round(bh * scale)), Image.LANCZOS)
    nw, nh = nb.size
    left, top = (nw - W) // 2, (nh - H) // 2
    return nb.crop((left, top, left + W, top + H))


def compose(slide: dict, background: str, out: str, assets: Path) -> dict:
    accent = safe_accent(slide.get("accent_hex") or DEFAULT_ACCENT)
    img = crop_cover(Image.open(background)) if background and Path(background).exists() \
        else Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    drawn = []  # (field, bbox) for verification

    # badge
    badge = slide.get("badge") or ""
    if badge and badge != "none":
        rounded_pill(draw, badge, W // 2, 70, assets, fg=TEXT)
        drawn.append(("badge", (W // 2, 70)))

    stype = slide.get("type", "item")
    y = 200

    if stype == "cover":
        fnt, lines, size = fit_headline(draw, assets, slide.get("headline", ""),
                                        W - 2 * MARGIN, 120, 56, 3)
        for ln in lines:
            draw.text((MARGIN, y), ln, font=fnt, fill=TEXT)
            y += int(size * 1.05)
        drawn.append(("headline", (MARGIN, 200)))
        sub = slide.get("subhead") or ""
        if sub:
            sf = font(assets, "grotesk", 40)
            for ln in wrap(draw, sub, sf, W - 2 * MARGIN):
                draw.text((MARGIN, y), ln, font=sf, fill=MUTED)
                y += 52
            drawn.append(("subhead", (MARGIN, y)))
        tail = slide.get("open_loop_tail") or "swipe →"
        tf = font(assets, "grotesk-bold", 32)
        draw.text((W - MARGIN - draw.textlength(tail, font=tf), BOTTOM_SAFE + 120),
                  tail, font=tf, fill=accent)

    elif stype == "cta":
        eb = font(assets, "mono", 26)
        draw_tracked(draw, (MARGIN, y), "WANT THE LINKS?", eb, MUTED, 2.0)
        y += 70
        fnt, lines, size = fit_headline(draw, assets, slide.get("headline", ""),
                                        W - 2 * MARGIN, 100, 52, 3)
        for ln in lines:
            draw.text((MARGIN, y), ln, font=fnt, fill=accent)
            y += int(size * 1.05)
        drawn.append(("headline", (MARGIN, y)))
        sub = slide.get("subhead") or ""
        if sub:
            sf = font(assets, "grotesk", 38)
            for ln in wrap(draw, sub, sf, W - 2 * MARGIN):
                draw.text((MARGIN, y), ln, font=sf, fill=TEXT)
                y += 50
        save = font(assets, "grotesk-bold", 30)
        draw.text((W - MARGIN - draw.textlength("save this post", font=save), BOTTOM_SAFE + 120),
                  "save this post", font=save, fill=accent)

    else:  # item / howto
        label = slide.get("badge") or ""
        fnt, lines, size = fit_headline(draw, assets, slide.get("headline", ""),
                                        W - 2 * MARGIN, 76, 44, 2, family="archivo-bold")
        for ln in lines:
            draw.text((MARGIN, y), ln, font=fnt, fill=TEXT)
            y += int(size * 1.1)
        drawn.append(("headline", (MARGIN, 200)))
        sub = slide.get("subhead") or ""
        if sub:
            sf = font(assets, "grotesk-bold", 36)
            for ln in wrap(draw, sub, sf, W - 2 * MARGIN):
                draw.text((MARGIN, y), ln, font=sf, fill=accent)
                y += 46
            drawn.append(("subhead", (MARGIN, y)))
        y += 12
        for b in (slide.get("bullets") or [])[:3]:
            bf = font(assets, "grotesk", 34)
            accent_marker(draw, MARGIN, y + 10, 22, accent)
            for i, ln in enumerate(wrap(draw, b, bf, W - 2 * MARGIN - 50)):
                draw.text((MARGIN + 44, y), ln, font=bf, fill=TEXT)
                y += 46
            drawn.append(("bullet", (MARGIN, y)))
        url = slide.get("url") or ""
        if url:
            uf = font(assets, "mono", 24)
            draw.text((MARGIN, min(y + 16, BOTTOM_SAFE - 40)), url, font=uf, fill=MUTED)
            drawn.append(("url", (MARGIN, y)))
        tail = slide.get("open_loop_tail") or ""
        if tail:
            tf = font(assets, "grotesk", 28)
            draw.text((MARGIN, BOTTOM_SAFE + 100), tail, font=tf, fill=MUTED)

    # featured logo (real PNG, never generated)
    lp = logo_path(assets, slide.get("logo_file", ""))
    if lp:
        try:
            logo = Image.open(lp).convert("RGBA")
            target = 120
            logo.thumbnail((target, target), Image.LANCZOS)
            img.paste(logo, (W - MARGIN - logo.width, BOTTOM_SAFE - logo.height - 10), logo)
            drawn.append(("logo", (W - MARGIN, BOTTOM_SAFE)))
        except OSError:
            pass

    # handle
    handle = slide.get("handle") or ""
    if handle:
        hf = font(assets, "mono", 26)
        draw.text((72, 1250), handle, font=hf, fill=MUTED)

    img.save(out, "PNG")
    return {"out": out, "size": img.size, "drawn": [d[0] for d in drawn], "accent": accent}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--slide-json", required=True, help="path to a JSON file with one slide dict")
    ap.add_argument("--background", default="", help="generated background PNG (optional)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    slide = json.loads(Path(args.slide_json).read_text())
    assets = resolve_assets()
    result = compose(slide, args.background, args.out, assets)
    if result["size"] != (W, H):
        print(f"ERROR: output is {result['size']}, expected {(W, H)}", file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
