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
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
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


def resolve_ref_set(assets: Path) -> list[Path]:
    """The fixed few-shot deck passed on every generation to lock the world (no drift)."""
    for d in (assets / "assets" / "style-reference", assets / "style-reference"):
        if d.is_dir():
            return sorted(p for p in d.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    return []


def hf_cost(prompt: str) -> str:
    r = subprocess.run(["higgsfield", "generate", "cost", "gpt_image_2",
                        "--prompt", prompt, "--json"], capture_output=True, text=True)
    return r.stdout.strip()


def hf_upload(path: Path) -> str:
    """Upload one reference image, return its id (per higgsfield-setup.md)."""
    r = subprocess.run(["higgsfield", "upload", str(path), "--json"],
                       capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return ""
    return data.get("id") or data.get("image_id") or ""


def hf_generate(prompt: str, ref_ids: list[str], seed: int, out_png: Path) -> dict:
    cmd = ["higgsfield", "generate", "create", "gpt_image_2", "--prompt", prompt,
           "--aspect_ratio", "3:4", "--resolution", "2k", "--quality", "high",
           "--batch_size", "2", "--seed", str(seed), "--wait", "--json"]
    for rid in ref_ids:
        cmd += ["--image", rid]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"status": "failed", "raw": r.stdout + r.stderr}
    return data


def hf_fetch_plate(data: dict, dest: Path) -> str:
    """Resolve the generated background to a local file: a local path is used as-is; a URL
    is downloaded to dest. Returns the local path, or "" if nothing usable was returned."""
    src = data.get("output_path") or data.get("local_path") or data.get("url") or ""
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
    if im.size != (W, H):
        issues.append(f"{png.name}: {im.size} != {(W, H)}")
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
    ap.add_argument("--seed", type=int, default=42)
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
    out_dir = spec_path.parent / "slides"
    out_dir.mkdir(exist_ok=True)
    assets = cs.resolve_assets()

    problems = check_prereqs(args.dry_run)
    if problems:
        print("Prereqs not met:")
        for p in problems:
            print("  ✗", p)
        return 1

    print(f"Spec: {meta.get('topic','?')} — {len(slides)} slides → {out_dir}")
    ref_ids: list[str] = []
    if not args.dry_run:
        per = hf_cost(build_plate_prompt({"type": "item"}))
        print("Cost estimate (per slide):", per or "run `higgsfield generate cost` to see")
        print(f"This will generate ~{len(slides)} backgrounds.")
        # Upload the fixed reference set once; reuse the ids on every slide (locks the world).
        refs = resolve_ref_set(assets)
        ref_ids = [rid for rid in (hf_upload(p) for p in refs) if rid]
        print(f"Reference set: {len(ref_ids)}/{len(refs)} images uploaded")

    rendered = []
    for i, slide in enumerate(slides, 1):
        if args.only and i != args.only:
            continue
        out_png = out_dir / f"slide-{i:02d}.png"
        if out_png.exists() and not args.only and not args.dry_run:
            print(f"  · slide {i:02d} exists, skipping (delete to re-render)")
            rendered.append(out_png)
            continue

        bg = ""
        if not args.dry_run:
            data = hf_generate(build_plate_prompt(slide), ref_ids, args.seed, out_png)
            if str(data.get("status", "")).lower() not in ("success", "completed", "done"):
                print(f"  ✗ slide {i:02d} generation status={data.get('status')}; skipping")
                continue
            bg = hf_fetch_plate(data, out_png)

        slide.setdefault("handle", meta.get("handle", ""))
        cs.compose(slide, bg, str(out_png), assets)
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
