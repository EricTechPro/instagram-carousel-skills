---
name: instagram-carousel-generate
description: Generate Instagram carousel slide images from an approved carousel-spec.md. Use when the user says "generate the carousel", "render the slides", "make the carousel images", or /instagram-carousel-generate. Renders full 3:4 portrait slides via HiggsField GPT Image 2 — the model letters ALL the text itself from a rich full-slide prompt; no Pillow text overlay. To write or edit the copy first, use instagram-carousel-plan.
---

# Instagram Carousel — Generate

Render an approved `carousel-spec.md` into `slide-01.png … slide-NN.png`, one consistent set in the
project's `output/` folder.

**Pipeline (learned the hard way — keep it this way):** GPT Image 2 renders the **whole slide** —
world, mascot, the cream card/sign, AND every line of text — from one rich per-slide prompt built by
`build_slide_prompt()`. Pillow only **resizes the returned plate to 1080-wide** (no crop). GPT Image 2
letters text well, so we let it; quoting each string in the prompt keeps spelling exact.

> **Do NOT** go back to the old "blank card + Pillow text overlay" approach. It produced text that
> overflowed the card, baked-on garble, and badges floating on the sky. The model owns the layout now.

## When to use
- "Generate the carousel" / "render the slides" after `instagram-carousel-plan` produced a spec
- `/instagram-carousel-generate` · or the user edited `carousel-spec.md` by hand and wants it rendered

## When NOT to use
- No spec yet, or the copy needs work → `instagram-carousel-plan`

## The style contract (match the reference deck — NOT "Minecraft")
**Brand-portable:** the *specific* look below (voxel world, Clawd, orange) is just the **default brand**.
`build_slide_prompt` reads `style` / `mascot` / `surface` / `accent_default` / `handle` from the spec
**meta** (filled by the plan skill from the active profile — `BRAND.md`, or `BRAND.<name>.md`), with
the Claude look only as a fallback. To render a different brand (e.g. the Hermes manga profile): set
those meta fields, set `accent_default: monochrome` for B&W, and point `IG_CAROUSEL_STYLE` at a
per-brand reference folder (even just that brand's logo). See `examples/hermes-agent-use-cases/`.

The default look is defined by `_reference-style/` (project root, swappable per `BRAND.md`). Hold to it:
- **Reference style, not a busy game world.** Polished, soft-lit, premium 3D children's-book render.
  A small, **cute, rounded** mascot (Clawd) — never a cluttered blocky Minecraft scene. Lots of open sky.
- **One big idea per slide, minimal text.** A **huge elegant serif headline is the hero**; one short
  sub-line; at most a few short bullets or a single terminal line. It must stop a scroll.
- **Cover** = headline across the upper half over open sky + the hero scene below + a small `swipe →`.
  **Items** = the text on a cream paper note pinned to a **wooden signboard**; mascot small at the base.
- **Visualize the idea with agents.** The topic is fanning out many agents, so use a rich
  `character_pose`: a master orchestrating a crowd, finder/refuter pairs, a search fan-out, an agent
  per document. This creativity is the point — make each slide its own scene.
- **Terminal slides** render the `terminal` field as the **Claude Code CLI**: dark window, traffic-light
  dots + a small Claude sunburst logo, the `> command` in mono, and an **"Opus 4.8" status bar**.
- **Brand marks:** `@erictech` small in **white** at the bottom-left. **No** redundant editorial tail or
  bottom arrows (just `swipe →` on the cover). Accent + handle + mascot all come from `BRAND.md`.
- **Output the FULL plate** — generate 3:4, resize to 1080 wide (~1080×1447). **Never crop to 4:5**;
  that slices the headline top and the handle bottom.

## Prereqs — check FIRST, before any credit spend
Read `references/higgsfield-setup.md`. Verify:
1. **HiggsField** — CLI (`higgsfield account status` succeeds) **or** MCP (Clockwork/cowork connected).
2. **Python 3 + Pillow** (`pip install -r requirements.txt`) — for resizing + the contact sheet.
3. **Assets resolve** — the `_reference-style/` deck (style references passed on every generation) and
   `BRAND.md`, via the asset contract. Print the resolution order if nothing is found.
If anything is missing, print the exact fix and **stop** — never silently spend credits.

## Workflow

### 1. Load + validate the spec
Parse `carousel-spec.md`. Confirm each slide has a `headline`, a `character_pose`, and (for terminal
slides) a `terminal` string. Resolve the `_reference-style/` deck — it's the few-shot style lock.

### 2. Cost gate
Run `higgsfield generate cost gpt_image_2 …` once, multiply by slide count, show the **total + count**,
and require **one explicit confirmation** before the batch. Carousels are exactly where a surprise bill bites.

### 3. Cover first — lock the look
Generate **only the cover** (`generate_carousel.py <spec> --allow-cli-spend --only 1`). Show it. The
cover proves the style/world/typography cheaply. Adjust the spec (headline, `character_pose`) and
re-roll the cover until it's right **before** spending on the rest.

### 4. Render the rest
Run `generate_carousel.py <spec> --allow-cli-spend` (skips already-rendered slides). Per slide it
builds the full-slide prompt, calls GPT Image 2 with the `_reference-style/` deck as references,
downloads the plate, and resizes to 1080-wide. Writes each `output/slide-NN.png` as it completes; a
re-run resumes the missing ones. **Single-slide re-roll:** `--only N` (≈7 credits).

### 5. Verify (gates "done")
- Each file: PNG, non-zero, **1080-wide portrait** (≈1080×1447).
- Generation reached a **success** terminal status (not nsfw / ip_detected / failed).
- Eyeball each: text spelled right, headline big, scene clean (not cluttered), accent + mascot on-brand.
- Build a **contact-sheet montage** → `output/_contact-sheet.png`. Report credits spent vs the estimate.

### 6. Deliver
Report all `output/*.png` paths + the contact sheet. Surface the caption + hashtags + DM-trigger for
copy-paste. To fix a slide, edit its spec fields and re-roll just that one with `--only N`.

## Consistency (no slide-to-slide drift)
Pass the **same `_reference-style/` deck on every generation** plus the same locked `STYLE` preamble in
the prompt. `gpt_image_2` has no seed — consistency rides on identical references + preamble. Never
chain slide N−1 as a reference for slide N.

## Free preview / CI
`--dry-run` composes a quick Pillow placeholder of the layout (no credits) — used by CI to prove the
pipeline runs and the spec parses. It is **not** the real look; the real slide is the GPT plate.

## Files
| Path | Purpose |
|---|---|
| `scripts/generate_carousel.py` | Orchestrator: prereqs → cost → `build_slide_prompt` → GPT Image 2 → resize plate → verify. Holds `STYLE` + the per-type prompt builder. |
| `scripts/compose_slide.py` | Pillow helpers + the `--dry-run` placeholder composer (not used for real renders). |
| `references/visual-system.md` | Palette, fonts, world, IG-safe zones (style intent). |
| `references/higgsfield-setup.md` | CLI + MCP setup, prereq checks, cost gating, failure modes. |
| `references/tool-brand-colors.md` | tool → accent hex + logo filename (shared with plan). |
| `references/plate-templates.md` · `layout-templates.md` | Legacy hybrid-era notes; superseded by `build_slide_prompt`. |
