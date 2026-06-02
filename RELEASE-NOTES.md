# Release notes

## v0.4.0 — 2026-06-01

### Fix: the MCP/Cowork path now writes real images into `output/`, not a download script

- **`references/higgsfield-setup.md`** — new "Saving renders on the MCP path" section. On hosts that
  sandbox the network and block HiggsField's CDN (`*.cloudfront.net → 403 blocked-by-allowlist`, e.g.
  Cowork), the agent must save each render's **inline/base64 bytes** straight to `output/slide-NN.png`
  (no network, so the allowlist can't bite). Fetching the URL is the second choice; writing a
  `download_slides.sh` is now an explicitly-labelled **last resort**, never the primary deliverable.
  Added a `blocked-by-allowlist` row to the failure-mode table and a note that getting images
  in-sandbox requires either MCP-returned bytes or allowlisting the CDN host.
- **`SKILL.md`** — §6 Deliver now states the MCP-path deliverable is image files in `output/`, with the
  bytes saved directly from the MCP tool result.

## v0.3.1 — 2026-06-01

### Fix: a single odd HiggsField response no longer crashes the batch

- **`generate_carousel.py`** — `hf_generate()` now always returns a dict. The CLI can return a
  single object, a list of jobs, or an **empty list** (a transient miss); previously an empty list
  reached `main()`, which called `.get()` on it and aborted the whole render with `AttributeError`,
  killing every remaining slide. Now a bad/empty response is treated as a failed slide — that one is
  skipped and the batch continues (re-roll it later with `--only N`).
- Corrected a stale inline comment ("crops to 1080x1350" → resizes to the full 3:4 plate).

## v0.3.0 — 2026-06-01

### Brand-portable rendering + a second worked example

- **Brand-portable render path.** `style`, `mascot`, `surface`, `accent_default`, and `handle` now
  flow **BRAND profile → spec `meta` → prompt** — nothing brand-specific is baked into
  `build_slide_prompt()` anymore. The Claude/Clawd look is just the neutral fallback. Set
  `accent_default: monochrome` for a pure black-&-white brand (emphasis becomes italic, no color);
  the terminal panel's app/status labels come from meta too.
- **Run multiple brands, no code.** Add a `BRAND.<name>.md` profile and point generation at a
  per-brand reference deck with `IG_CAROUSEL_STYLE=<folder>` — your default `_reference-style/` is
  never touched.
- **New example — `examples/hermes-agent-use-cases/`.** A full 8-slide deck in a completely
  different identity (vintage shoujo-manga, monochrome B&W, `@erictechpro`) rendered by the *same*
  scripts from a real YouTube video — proof the look isn't locked to Clawd/voxel.
- **The handle is the Instagram account username, and it's lettered into every slide.** Both skills
  now confirm it in cheap text before any spend; the generate skill verifies it on the cover-first
  render and flags that a wrong handle (or any brand field) means re-rolling the deck.
- **README corrected + Examples section.** Fixed stale pipeline claims (it described `1080×1350` +
  Pillow text overlay + "free" text fixes — all wrong since GPT Image 2 letters the whole slide) and
  added a linked `input → spec → output` walkthrough for both examples.
- **Default handle → `@erictechpro`**; tightened both skills' trigger descriptions.
- **Fix:** `release.sh` now syncs `.claude-plugin/marketplace.json` (the manifest moved there).

## v0.2.0 — 2026-06-01

### Modular brand + discoverable style

- **`BRAND.md`** — every brand default (handle, accent, voice, mascot) now lives in one editable
  file at the project root. The skills read it instead of hardcoding `@erictech` / `#2BAADF` /
  Clawd. Rebrand by editing one file.
- **`_reference-style/`** (renamed from `assets/style-reference`) now installs at the **project
  root** so the few-shot style deck is easy to find and swap.
- Install is **non-clobbering** for both — a re-install keeps your edited `BRAND.md` and images.
- Reference resolution: `$IG_CAROUSEL_STYLE` → project root → installed assets → legacy path.
- CI smoke asserts `BRAND.md` + `_reference-style/` land at the project root.

## v0.1.0 — 2026-05-31

### Initial public release

Two standalone, composable skills for planning and generating on-brand Instagram carousels from
a coding agent — no Superpowers or sibling-project dependencies.

**`instagram-carousel-plan`** — research + copywriting → spec
- ≤4-question intake (audience+pain, payoff+proof, sequence, CTA goal); accent/research/voice auto-defaulted.
- Researches pasted links/repos into a `research/` wiki (no invented facts).
- Embedded carousel copywriting frameworks: cover hook formulas, the "which means…" benefit
  bridge, retention mechanics (numbered payload + open-loop tails), IG-oriented save/DM CTAs, a
  mandatory anti-AI scrub, and hard density caps.
- Emits `instagram-carousel/<topic>/carousel-spec.md` with an ASCII layout + per-slide blocks +
  post caption, hashtags, and a DM-trigger.

**`instagram-carousel-generate`** — spec → 1080×1350 slides (hybrid pipeline)
- HiggsField GPT Image 2 renders a **text-free background plate** (sky/grass world, Clawd, blank card).
- Pillow overlays exact text (Archivo / Space Grotesk / JetBrains Mono) and pastes **real logo PNGs**
  — pixel-accurate type and brand marks, IG-safe margins, per-slide accent = the featured tool's brand.
- Consistency via a fixed reference set + pinned seed (no slide-to-slide drift).
- Cost-gates before any credit spend; verifies dims, status, and world-color drift; builds a contact sheet.
- Works in Claude Code, and in Clockwork/cowork via the HiggsField MCP.

**Repo**
- Self-marketplace plugin layout (`marketplace.json` at root, `.claude-plugin/plugin.json`).
- `install.sh` (project or `--global`) + agent-followable `INSTALL.md` ("just ask your agent").
- Bundled fonts, style-reference deck, curated tool logos. Complete 8-slide example spec.
- CI smoke: installs into a temp project and dry-run renders all 8 example slides at 1080×1350.

Install: download the release zip below and unzip into your project's `.claude/`, or tell your
agent *"Install the skills from https://github.com/EricTechPro/instagram-carousel-skills"*.
