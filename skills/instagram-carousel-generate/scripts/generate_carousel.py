#!/usr/bin/env python3
"""Orchestrate carousel rendering from an approved carousel-spec.md.

Pipeline per slide: HiggsField GPT Image 2 renders a text-free background plate (CLI path) →
compose_slide.py crops to 1080x1350 and overlays exact text + the real logo → verify.

This is the CLI-mode driver. On the MCP path (Clockwork/cowork) the agent drives the HiggsField
MCP tools itself and calls compose_slide.compose() directly; this file's parser + verify +
contact-sheet helpers are still reused.

Usage:
    python generate_carousel.py SPEC.md                 # full run (prompts for cost confirmation)
    python generate_carousel.py SPEC.md --dry-run       # compose over blank plates, no credits
    python generate_carousel.py SPEC.md --only 3        # (re)render just slide 3
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
def hf_cost(prompt: str) -> str:
    r = subprocess.run(["higgsfield", "generate", "cost", "gpt_image_2",
                        "--prompt", prompt, "--json"], capture_output=True, text=True)
    return r.stdout.strip()


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
    ap.add_argument("--only", type=int, default=0, help="render only slide N")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args(argv)

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
    if not args.dry_run:
        print("Cost estimate (per slide):", hf_cost("plate") or "run `higgsfield generate cost` to see")
        print(f"This will generate ~{len(slides)} backgrounds. Re-run with credits confirmed.")

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
            # NOTE: upload the fixed reference set once and reuse ref ids here.
            data = hf_generate("plate prompt — see plate-templates.md", [], args.seed, out_png)
            if str(data.get("status", "")).lower() not in ("success", "completed", "done"):
                print(f"  ✗ slide {i:02d} generation status={data.get('status')}; skipping")
                continue
            bg = data.get("output_path") or data.get("local_path") or ""

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
