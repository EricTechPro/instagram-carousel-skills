# Release notes

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
