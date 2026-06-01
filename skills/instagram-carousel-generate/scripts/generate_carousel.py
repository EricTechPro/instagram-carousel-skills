#!/usr/bin/env python3
"""Orchestrate carousel rendering from an approved carousel-spec.md.

Pipeline per slide: HiggsField GPT Image 2 renders a text-free background plate (CLI path) →
compose_slide.py crops to 1080x1350 and overlays exact text + the real logo → verify.

This is the CLI-mode driver. On the MCP path (Clockwork/cowork) the agent drives the HiggsField
MCP tools itself and calls compose_slide.compose() directly; this file's parser + verify +
contact-sheet helpers are still reused.

Usage:
    python generate_carousel.py carousel-spec.md                 # full run (prompts for cost confirmation)
    python generate_carousel.py carousel-spec.md --dry-run       # compose over blank plates, no credits
    python generate_carousel.py carousel-spec.md --only 3        # (re)render just slide 3
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose_slide as cs  # noqa: E402

W, H = cs.W, cs.H


# ---- spec parsing -----------------------------------------------------------
def _coerce(v: str):
    v = v.strip()
    if v.startswith("[") or v.startswith("{"):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            return v.strip("[]")
    # Quoted value: return the inner string up to the closing quote, ignoring any trailing
    # inline comment (e.g. `handle: "@erictechpro" # default from BRAND.md`).
    if v[:1] in ('"', "'"):
        q = v[0]
        end = v.find(q, 1)
        return v[1:end] if end != -1 else v[1:]
    # Unquoted value: drop a trailing inline comment that follows whitespace ("  # …"),
    # but keep leading-# values like hex colors (`#2BAADF`).
    m = re.search(r"\s#", v)
    if m:
        v = v[:m.start()].strip()
    return v


def parse_spec(path: Path) -> dict:
    text = path.read_text()
    meta: dict = {}
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if fm:
        for line in fm.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = _coerce(v)

    slides = []
    for block in re.split(r"^##\s+Slide\s+\d+\s*$", text, flags=re.MULTILINE)[1:]:
        slide = {}
        for line in block.splitlines():
            m = re.match(r"\s*-\s*([a-z_]+)\s*:\s*(.*)$", line)
            if m:
                slide[m.group(1)] = _coerce(m.group(2))
            if line.strip().startswith("#") or line.strip().startswith("caption:"):
                break
        if slide:
            slide.setdefault("handle", meta.get("handle", ""))
            slides.append(slide)

    post = {}
    cap = re.search(r"caption:\s*\|\n(.*?)(?:\nhashtags:|\Z)", text, re.DOTALL)
    if cap:
        post["caption"] = "\n".join(l[2:] if l.startswith("  ") else l
                                    for l in cap.group(1).splitlines()).strip()
    ht = re.search(r"hashtags:\s*(\[.*?\])", text)
    if ht:
        post["hashtags"] = _coerce(ht.group(1))
    dm = re.search(r"dm_trigger:\s*(.+)", text)
    if dm:
        post["dm_trigger"] = _coerce(dm.group(1))
    return {"meta": meta, "slides": slides, "post": post}


# ---- prereqs ----------------------------------------------------------------
def check_prereqs(dry_run: bool) -> list[str]:
    problems = []
    try:
        import PIL  # noqa: F401
    except ImportError:
        problems.append("Pillow missing → pip install -r requirements.txt")
    assets = cs.resolve_assets()
    if not (assets / "character-references").is_dir() and not (assets / "assets").is_dir():
        problems.append(f"assets not found; set IG_CAROUSEL_ASSETS (looked under {assets})")
    if not dry_run:
        if not shutil.which("higgsfield"):
            problems.append("higgsfield CLI not on PATH → npm i -g @higgsfield/cli "
                            "(or use the MCP path in Clockwork/cowork)")
        else:
            r = subprocess.run(["higgsfield", "account", "status", "--json"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                problems.append("higgsfield not authenticated → higgsfield auth login")
    return problems


# ---- generation (CLI) -------------------------------------------------------
# Locked preamble — keep in sync with references/plate-templates.md. The model renders the
# world only (no text, no logos); Pillow draws all copy and pastes real logos.
PLATE_PREAMBLE = (
    "3D voxel render, bright blue sky with soft white clouds, green grass strip along the "
    "bottom, cheerful sunny scene, soft shadows, shallow depth of field. A blocky "
    'Minecraft-style orange mascot character ("Clawd"). Clean blank cream/off-white paper card '
    "with a smooth empty surface and NO text, NO lettering, NO logos. Portrait composition. "
    "Match the style of the reference images."
)
PLATE_BY_TYPE = {
    "cover": "Crowned mascot standing on a pile of small code blocks, arms raised; big empty area at the top for a headline.",
    "item":  "Mascot beside a wooden sign on a post (or holding a pinned note); large blank cream card filling the upper two-thirds, empty.",
    "howto": "Three small wooden signposts in a row on the grass, each with a small blank card; mascots beside them.",
    "cta":   "Mascot holding a large blank speech-bubble sign overhead, empty surface.",
}


def build_plate_prompt(slide: dict) -> str:
    """Per-type background plate prompt (no text/logos) — see plate-templates.md."""
    return PLATE_PREAMBLE + " " + PLATE_BY_TYPE.get(slide.get("type", "item"), PLATE_BY_TYPE["item"])


# ---- full-slide prompt (GPT Image 2 renders the text too) -------------------
# Brand-neutral fallbacks (used only when the spec meta omits these). The active brand profile
# (BRAND.md / BRAND.<name>.md) supplies `style`, `mascot`, `surface`, `accent_default`, `handle`
# into the spec meta, so NOTHING brand-specific is baked into the render path — these defaults just
# reproduce the original Claude/Clawd look for back-compat.
DEFAULT_STYLE = (
    "Polished, soft-lit premium 3D illustration in a friendly children's-book style — match the "
    "reference images closely. Sunny scene: bright blue sky, soft white clouds, a green grass strip. "
    "Keep the composition clean and uncluttered with lots of open sky and breathing room. Tall "
    "portrait 4:5 composition."
)
DEFAULT_MASCOT = "a small, cute, rounded orange voxel mascot named Clawd with tiny dark sunglasses"
DEFAULT_SURFACE = "a cream paper note pinned to a wooden signboard on a post"

_MONO_ACCENTS = {"", "monochrome", "mono", "none", "bw", "b&w", "black and white", "black & white"}


def _q(s: str) -> str:
    """Quote-safe text for the prompt: collapse whitespace, neutralize double quotes."""
    return " ".join(str(s).split()).replace('"', "'").strip()


def build_slide_prompt(slide: dict, meta: dict) -> str:
    """A complete-slide prompt: ONE big elegant serif headline is the hero, minimal supporting text,
    a host/mascot, framed per the brand's surface. GPT Image 2 renders the scene AND the text.
    Style, mascot, surface, accent, handle, and terminal labels all come from the spec meta (filled
    from the active BRAND profile); the constants above are only neutral fallbacks. Every string is
    quoted so the model letters it exactly."""
    style = _q(meta.get("style") or DEFAULT_STYLE)
    mascot = _q(meta.get("mascot") or DEFAULT_MASCOT)
    surface = _q(meta.get("surface") or DEFAULT_SURFACE)
    accent = str(slide.get("accent_hex") or meta.get("accent_default") or "").strip()
    mono = accent.lower() in _MONO_ACCENTS
    handle = _q(slide.get("handle") or meta.get("handle") or "")
    stype = slide.get("type", "item")
    headline, subhead = _q(slide.get("headline", "")), _q(slide.get("subhead", ""))
    badge = _q(slide.get("badge", "") or "")
    bullets = [_q(b) for b in (slide.get("bullets") or []) if b][:3]
    terminal = _q(slide.get("terminal", "") or "")
    pose = _q(slide.get("character_pose", "") or f"the host — {mascot}")

    emph = ("Emphasize the most important word in italic (monochrome — no color)." if mono
            else f"Set the most important word in italic in the accent color {accent}.")
    bullet_tone = "black" if mono else accent

    p = [style]
    p.append(f'HERO HEADLINE — the focus of the slide, VERY LARGE bold elegant serif, easy to read '
             f'while scrolling: "{headline}". {emph}')
    if subhead:
        p.append(f'One short supporting line, smaller, beneath it: "{subhead}".')

    if stype == "cover":
        if badge and badge.lower() != "none":
            p.append(f'A small badge reading "{badge}".')
        p.append(f"The headline spans the upper portion. Below it, large and central, the scene: "
                 f"{pose}. Bottom-right, a small italic label: \"swipe →\".")
    else:
        p.append(f"The text sits on {surface}, centered with generous margins — minimal wording, big headline.")
        if badge and badge.lower() != "none":
            p.append(f'A small tracked uppercase label at the top: "{badge}".')
        if bullets:
            items = "; ".join(f'"{b}"' for b in bullets)
            p.append(f"A short list, each line led by a small {bullet_tone} square bullet: {items}.")
        if terminal:
            term_app = _q(meta.get("terminal_app") or "Claude Code")
            term_status = _q(meta.get("terminal_status") or "Opus 4.8")
            p.append(f'A compact terminal panel styled like the {term_app} CLI: dark rounded window, '
                     f'three small red/yellow/green dots and a tiny app logo in the title bar, white '
                     f'monospace text "> {terminal}", and a thin bottom status bar reading "{term_status}".')
        p.append(f"In a small scene, the host: {pose}.")
    if handle:
        p.append(f'At the very bottom-left, small high-contrast text: "{handle}".')
    p.append("Minimal text overall, big readable type, clean and uncluttered, no watermark, and no "
             "extra arrows or captions along the bottom edge.")
    return " ".join(p)


def _find_upward(start: Path, name: str, max_up: int = 4) -> Path | None:
    """Walk up from `start` looking for a directory named `name` (project-root discovery)."""
    p = start.resolve()
    for _ in range(max_up + 1):
        if (p / name).is_dir():
            return p / name
        if p.parent == p:
            break
        p = p.parent
    return None


def resolve_ref_set(assets: Path, spec_path: Path | None = None) -> list[Path]:
    """The fixed few-shot deck passed on every generation to lock the world (no drift).

    Resolution order for the user-editable `_reference-style/` (see BRAND.md):
      env IG_CAROUSEL_STYLE → project root (up from the spec, then cwd) → installed assets →
      legacy `assets/style-reference`.
    """
    bases: list[Path] = []
    env = os.environ.get("IG_CAROUSEL_STYLE")
    if env:
        bases.append(Path(env))
    for start in (spec_path.parent if spec_path else None, Path.cwd()):
        if start:
            found = _find_upward(start, "_reference-style")
            if found:
                bases.append(found)
    bases += [assets / "_reference-style", assets.parent / "_reference-style",
              assets / "assets" / "style-reference"]  # installed + legacy fallback
    for d in bases:
        if d and Path(d).is_dir():
            imgs = sorted(p for p in Path(d).iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
            if imgs:
                return imgs
    return []


def hf_cost(prompt: str) -> str:
    r = subprocess.run(["higgsfield", "generate", "cost", "gpt_image_2",
                        "--prompt", prompt, "--json"], capture_output=True, text=True)
    return r.stdout.strip()


def hf_generate(prompt: str, ref_paths: list[Path]) -> dict:
    """Generate one background plate. `--image` accepts local paths (auto-uploaded), so we
    pass the fixed reference set directly — no separate upload step. gpt_image_2 has no
    `seed` param, so consistency rides on the same refs + same locked prompt every slide."""
    cmd = ["higgsfield", "generate", "create", "gpt_image_2", "--prompt", prompt,
           "--aspect_ratio", "3:4", "--resolution", "2k", "--quality", "high",
           "--batch_size", "1", "--wait", "--wait-timeout", "5m", "--json"]
    for p in ref_paths:
        cmd += ["--image", str(p)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"status": "failed", "raw": (r.stdout + r.stderr)[:400]}
    return data[0] if isinstance(data, list) and data else data


def hf_fetch_plate(data: dict, dest: Path) -> str:
    """Resolve the generated background to a local file: a local path is used as-is; a URL
    is downloaded to dest. Returns the local path, or "" if nothing usable was returned."""
    src = data.get("result_url") or data.get("output_path") or data.get("local_path") or data.get("url") or ""
    if not src:
        return ""
    if src.startswith(("http://", "https://")):
        import urllib.request
        plate = dest.with_suffix(".plate.png")
        try:
            urllib.request.urlretrieve(src, plate)
            return str(plate)
        except OSError:
            return ""
    return src if Path(src).exists() else ""


# ---- verify + contact sheet -------------------------------------------------
def verify(png: Path) -> list[str]:
    from PIL import Image
    issues = []
    if not png.exists() or png.stat().st_size == 0:
        return [f"{png.name}: missing/empty"]
    im = Image.open(png)
    w, h = im.size
    # Real slides are the full plate (1080-wide portrait); dry-run previews are 1080x1350.
    if w != 1080 or not (1080 <= h <= 1600):
        issues.append(f"{png.name}: {im.size} is not a 1080-wide portrait")
    return issues


def contact_sheet(pngs: list[Path], out: Path):
    from PIL import Image
    if not pngs:
        return
    thumb_w = 270
    thumbs = []
    for p in pngs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((thumb_w, thumb_w * H // W), Image.LANCZOS)
        thumbs.append(im)
    cols = min(4, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    pad = 12
    cw, ch = thumbs[0].size
    sheet = Image.new("RGB", (cols * cw + pad * (cols + 1), rows * ch + pad * (rows + 1)), "#FFFFFF")
    for i, t in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet.paste(t, (pad + c * (cw + pad), pad + r * (ch + pad)))
    sheet.save(out, "PNG")


# ---- main -------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--dry-run", action="store_true", help="compose over blank plates, no credits")
    ap.add_argument("--allow-cli-spend", action="store_true",
                    help="opt in to spending HiggsField credits via this CLI driver (omit to stay free)")
    ap.add_argument("--only", type=int, default=0, help="render only slide N")
    args = ap.parse_args(argv)

    # Spend guard: without --dry-run or --allow-cli-spend, never call the paid API. The supported
    # generation path is the agent/MCP flow in SKILL.md (cost gate + fixed refs + pinned seed);
    # this CLI driver renders backgrounds only when you explicitly opt in.
    if not args.dry_run and not args.allow_cli_spend:
        print("Refusing to spend credits without an explicit opt-in.\n"
              "  • Preview free (white plates):  --dry-run\n"
              "  • Spend credits via this CLI:   --allow-cli-spend\n"
              "  • Or drive generation from your agent per SKILL.md (cost-gated, recommended).")
        return 2

    spec_path = Path(args.spec)
    parsed = parse_spec(spec_path)
    slides, meta = parsed["slides"], parsed["meta"]
    # Per-topic layout is input/ → spec/carousel-spec.md → output/. When the spec sits in a `spec/`
    # subfolder, slides go to the sibling `output/`; for a flat spec they land beside it in `output/`.
    spec_dir = spec_path.parent
    topic_root = spec_dir.parent if spec_dir.name == "spec" else spec_dir
    out_dir = topic_root / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    assets = cs.resolve_assets()

    problems = check_prereqs(args.dry_run)
    if problems:
        print("Prereqs not met:")
        for p in problems:
            print("  ✗", p)
        return 1

    print(f"Spec: {meta.get('topic','?')} — {len(slides)} slides → {out_dir}")
    ref_paths: list[Path] = []
    if not args.dry_run:
        per = hf_cost(build_plate_prompt({"type": "item"}))
        print("Cost estimate (per slide):", per or "run `higgsfield generate cost` to see")
        print(f"This will generate ~{len(slides)} backgrounds.")
        # Fixed reference set passed on every slide (same refs + locked prompt = consistent world).
        ref_paths = resolve_ref_set(assets, spec_path)
        print(f"Reference set: {len(ref_paths)} images")

    rendered = []
    for i, slide in enumerate(slides, 1):
        if args.only and i != args.only:
            continue
        out_png = out_dir / f"slide-{i:02d}.png"
        if out_png.exists() and not args.only and not args.dry_run:
            print(f"  · slide {i:02d} exists, skipping (delete to re-render)")
            rendered.append(out_png)
            continue

        slide.setdefault("handle", meta.get("handle", ""))
        if args.dry_run:
            # Free structural preview (and CI): Pillow draws a placeholder of the layout.
            cs.compose(slide, "", str(out_png), assets)
        else:
            # GPT Image 2 renders the WHOLE slide — world, mascot AND all the text — from a
            # full-slide prompt. Pillow only crops the result to 1080x1350.
            data = hf_generate(build_slide_prompt(slide, meta), ref_paths)
            if str(data.get("status", "")).lower() not in ("success", "completed", "done"):
                print(f"  ✗ slide {i:02d} generation status={data.get('status')}; skipping")
                continue
            plate = hf_fetch_plate(data, out_png)
            if plate and Path(plate).exists():
                # Go with the FULL plate — resize to 1080 wide, keep its native 3:4 height so
                # nothing GPT composed (headline top / handle bottom) gets cropped away.
                src = cs.Image.open(plate).convert("RGB")
                pw, ph = src.size
                img = src.resize((1080, round(1080 * ph / pw)), cs.Image.LANCZOS)
            else:
                img = cs.Image.new("RGB", (1080, 1440), "#FFFFFF")
            img.save(str(out_png), "PNG")
        issues = verify(out_png)
        print(("  ✓ " if not issues else "  ! ") + f"slide {i:02d} " + (" ".join(issues)))
        rendered.append(out_png)

    contact_sheet([p for p in rendered if p.exists()], out_dir / "_contact-sheet.png")
    print(f"\nDone. {len(rendered)} slides in {out_dir}")
    if parsed["post"]:
        print("\n--- caption ---\n" + parsed["post"].get("caption", ""))
        print("hashtags:", " ".join(parsed["post"].get("hashtags", [])))
        print("DM trigger:", parsed["post"].get("dm_trigger", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
