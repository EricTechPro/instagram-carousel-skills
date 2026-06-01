---
name: instagram-carousel-generate
description: Use when the user has an approved carousel-spec.md and wants the slide images rendered — generates a branded background per slide with HiggsField GPT Image 2, then overlays exact text + logos with Pillow, cropping each to 1080x1350. Locks one consistent world/character/type across the deck via a fixed reference set + pinned seed. Checks HiggsField (CLI or MCP) and gates on a cost estimate before spending credits. Triggers on "generate the carousel", "render the slides", or /instagram-carousel-generate. To write or change the copy first, use instagram-carousel-plan.
---

# Instagram Carousel — Generate

Render an approved `carousel-spec.md` into `slide-01.png … slide-NN.png` (1080×1350), one
consistent set. **Hybrid pipeline:** HiggsField GPT Image 2 makes the *background* (sky/grass world,
Clawd posed, a blank cream card); Pillow overlays the *text and logos* exactly — so headlines,
bullets, URLs and brand marks are pixel-accurate, on-brand, and editable without re-spending credits.

## When to use
- "Generate the carousel" / "render the slides" after `instagram-carousel-plan` produced a spec
- `/instagram-carousel-generate`
- User edited `carousel-spec.md` by hand and wants it rendered

## When NOT to use
- No spec yet, or the copy needs work → `instagram-carousel-plan`

## Prereqs — check FIRST, before any credit spend
Read `references/higgsfield-setup.md`. Verify:
1. **HiggsField** — CLI (`higgsfield account status` succeeds) **or** MCP (Clockwork/cowork connected).
2. **Python 3 + Pillow** (`pip install -r requirements.txt`).
3. **Assets resolve** — fonts + reference images + logos via the asset contract (env
   `IG_CAROUSEL_ASSETS` → skill-relative `../../assets` & `../../character-references` →
   `~/.claude/instagram-carousel/`). Print the resolution order if nothing is found.
If anything is missing, print the exact fix and **stop** — do not silently fail or spend credits.

## Workflow

### 1. Load + validate the spec
Parse `carousel-spec.md`. For every slide resolve `logo_file` and `character_pose` against the
asset contract. **Abort before any credits if a referenced logo/asset is missing** — list what's missing.

### 2. Cost gate
Run `higgsfield generate cost gpt_image_2 …` once, multiply by slide count, and show the user the
**total estimate + slide count**. Require one explicit confirmation before the batch. (A carousel is
exactly the case where a surprise bill matters.)

### 3. BFS — lock the cover + the world
Generate the **cover background** only (`aspect_ratio 3:4`, `resolution 2k`), passing the fixed
reference set (see below). Crop to 1080×1350, overlay the cover text, show the user. They confirm
the look (and the **seed** is locked) — or adjust the prompt/style once and regenerate the cover.

### 4. DFS — the rest of the deck
For each remaining slide, generate the background with the **same fixed reference set + same pinned
seed + same locked preamble** (see `references/plate-templates.md`). Serial; `batch_size 2`, keep the
cleaner plate; **write each `slide-NN.png` as it completes and skip already-rendered slides on re-run.**

### 5. Compose each slide (Pillow, no network)
Run `scripts/compose_slide.py` per slide: crop the background to 1080×1350, then draw the badge,
headline, subhead, bullets, URL, handle, and "swipe/save" chrome with the bundled fonts at the exact
sizes/tracking/accent from `references/layout-templates.md`, and **paste the real logo PNG**. If the
slide has `mimic_ui`, render that panel (e.g. a GitHub repo header) per `references/layout-templates.md`.
All text/logo accuracy lives here — never in the model.

### 6. Verify (gates "done")
- Each file: PNG, non-zero, **exactly 1080×1350**.
- Background generation reached a **success** terminal status (not nsfw / ip_detected / failed).
- Every spec text field for the slide was actually drawn (the composer asserts this).
- Accent color on the slide matches `accent_hex`; no text within 80px of edges or in the bottom 420px.
- **Drift proxy:** the sky strip + grass strip mean-color of each slide is within tolerance of the
  cover's. Flag outliers for a one-tap background regen.
- Build a **contact-sheet montage** (all slides side by side) → `slides/_contact-sheet.png`.
- Report credits spent vs the estimate.

### 7. Deliver
Report all `slides/*.png` paths + the contact sheet. Surface the caption + hashtags + DM-trigger from
the spec for copy-paste. Single-slide fixes: re-run `compose_slide.py` for a text change (free), or
regen just that one background.

## Consistency mechanism (no slide-to-slide drift)
Pass the **same reference set on every generation**: the canonical Clawd reference, the once-approved
cover, and the `style-reference/` deck as few-shot — plus one **pinned seed** for the whole deck.
**Never** chain slide N−1 as the reference for slide N (that causes drift). Keep the generation prompt
short (world + Clawd + blank card only — no copy to spell).

## Files
| Path | Purpose |
|---|---|
| `references/visual-system.md` | Locked colors, fonts, world, chrome, IG-safe zones |
| `references/plate-templates.md` | Background-only prompts (no text) per slide type + seed/refs |
| `references/layout-templates.md` | Pillow text/logo layout per slide type (coords, sizes, tracking) |
| `references/tool-brand-colors.md` | tool → accent hex + logo filename (shared with plan) |
| `references/higgsfield-setup.md` | CLI + MCP setup, prereq checks, cost gating, failure modes |
| `scripts/generate_carousel.py` | Orchestrator: prereqs → cost → gen backgrounds (CLI) → compose → verify |
| `scripts/compose_slide.py` | Pure-PIL: background + text + logo + chrome → 1080×1350 |
