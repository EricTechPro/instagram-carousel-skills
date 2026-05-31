# Instagram Carousel Skills — Design Spec (v2, post-review)

**Status:** revised after 3-agent review · **Owner:** EricTechPro · **Date:** 2026-05-31

A **standalone, public** skill repo (`EricTechPro/instagram-carousel-skills`) that turns a
topic + sources into a branded Instagram carousel. Two composable skills:

1. **`instagram-carousel-plan`** — research + copywriting → a reviewable `carousel-spec.md`
2. **`instagram-carousel-generate`** — spec → rendered 1080×1350 slide images

Installable from **any Claude Code host** (incl. Clockwork/cowork) and as a plain clone, with
no dependency on Superpowers or sibling projects. Useful parts of brainstorming + marketing
skills are **embedded** (distilled, attributed), not imported.

> **v2 changes** fold in the three review passes (DX/portability, copywriting, generation).
> The single biggest change: **hybrid generation** — the model makes the *image*, Pillow
> composites the *text + logos* (§5).

---

## 1. Goals & non-goals

**Goals**
- One topic → on-brand, swipeable carousel matching the locked Eric Tech visual system.
- Hard split: *plan* (cheap, text, iterated) before *generate* (spends image credits).
- Standalone after one plugin install or `git clone` + `install.sh` — no superpowers, no BookKeepingApp.
- Portable: no hardcoded user paths/IDs; tokens + fonts + logos bundled in the repo.
- Pixel-exact, accurate text and brand logos (not model-hallucinated lettering).

**Non-goals**
- Auto-posting/scheduling (user posts manually). · Reels/video. · A general image generator.

---

## 2. Locked visual system (baked in, portable)

**World (constant every slide):** bright blue sky + soft white clouds + green grass strip ·
voxel "Clawd" mascot host (posed per slide) · cream paper cards (signs on posts, pinned notes,
speech bubbles) · handle bottom-left · pill badge top · "swipe →"/"save this post" chrome.

**Type (composited by Pillow, not generated):**
- Headlines → `Archivo` Black/Bold, tracking −0.03…−0.05em
- Body → `Space Grotesk`
- Labels / "REPO 01" / URLs → `JetBrains Mono`, 11px, uppercase, 0.12em tracking
- Fonts bundled as TTFs in `assets/fonts/` (OFL — redistributable).

**Color:** bg `#FFFFFF`, surface `#F8FAFC`, border `#E2E8F0`, text `#0F172A`, muted `#475569`,
**signature blue `#2BAADF`** (default accent). Secondary glows: purple `#8B5CF6`, teal `#14B8A6`.

**Per-slide accent = featured tool's brand** (auto from map; default blue if none):
Claude → clay `#D97757` · GitHub → `#0F172A` · OpenAI/Codex → purple `#8B5CF6` ·
Stripe → `#635BFF` · Supabase → `#3ECF8E` · Figma → `#F24E1E` · Eric Tech → `#2BAADF`.

**IG-safe layout:** all text ≥ 80px from edges; keep critical copy out of bottom ~420px.
(Programmatically enforced — Pillow knows every text bbox.)

---

## 3. Repo structure (self-marketplace, matches super-board/superpowers)

```
instagram-carousel-skills/
├── README.md                       # superpowers-style; leads with install; "Use in Clockwork/cowork"
├── CLAUDE.md                        # repo house rules (house pattern)
├── LICENSE                          # MIT
├── VERSION                          # single source of truth; plugin.json reads same
├── install.sh                       # ./install.sh [dir] (default $PWD) | --global → ~/.claude
├── requirements.txt                 # Pillow (text/logo compositing)
├── .gitignore
├── marketplace.json                 # AT REPO ROOT, source "./", lists the plugin
├── .claude-plugin/
│   └── plugin.json                  # name: "instagram-carousel", version mirrors VERSION
├── .github/workflows/smoke.yml      # install.sh into tmp → assert both SKILL.md land
├── assets/
│   ├── fonts/                       # Archivo, Space Grotesk, JetBrains Mono TTFs (OFL)
│   ├── style-reference/             # reference carousel (few-shot + style lock for the model)
│   └── sample-output/               # one rendered sample deck + contact sheet
├── character-references/            # canonical clawd-voxel.png + curated tool-logo PNGs (standalone)
├── skills/
│   ├── instagram-carousel-plan/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── intake-questions.md      # embedded brainstorming-lite + marketing grill (≤4 Qs)
│   │       ├── copy-frameworks.md       # hooks, "which means" bridge, specificity, anti-AI scrub
│   │       ├── sequence-patterns.md     # standard/listicle/tutorial/comparison/mistakes + retention
│   │       ├── research-playbook.md     # sources/links/repos (firecrawl/WebSearch/gh)
│   │       └── spec-template.md         # carousel-spec.md schema + ASCII layout block
│   └── instagram-carousel-generate/
│       ├── SKILL.md
│       ├── references/
│       │   ├── visual-system.md         # §2 verbatim
│       │   ├── plate-templates.md       # background-plate prompts (NO text) per slide type
│       │   ├── layout-templates.md      # Pillow text/logo layout per slide type (coords, sizes)
│       │   ├── tool-brand-colors.md     # tool → accent hex + logo filename
│       │   └── higgsfield-setup.md      # CLI + MCP (Clockwork) setup, prereq checks, cost gating
│       └── scripts/
│           ├── generate_carousel.py     # plate gen (HiggsField CLI) + crop + PIL compose + verify
│           └── compose_slide.py         # pure-PIL: plate + text + logo → 1080×1350 (no network)
└── SPEC.md                          # this file (kept in-repo as design record)
```

**Runtime asset-resolution contract** (used by both skills, prevents fresh-clone failure):
1. `$IG_CAROUSEL_ASSETS` env var if set →
2. `<skill_dir>/../../assets` and `../../character-references` (plugin/clone layout) →
3. `~/.claude/instagram-carousel/` (where `--global` install drops them).
First hit wins; skill errors with the resolution order printed if none found.

---

## 4. Skill 1 — `instagram-carousel-plan`

**Trigger:** "plan an instagram carousel", "carousel for <topic>", "/instagram-carousel-plan".

**Flow**
1. **Resolve input** — topic + any sources/links/repo URLs pasted.
2. **Intake — ≤4 questions, AskUserQuestion, 2–3 options each, defaults pre-picked:**
   - **Q1 Audience + pain** — who it's for and the painful before-state (presets + "Other").
   - **Q2 Payoff + proof** — after-state and any hard number (drives cover specificity).
   - **Q3 Sequence** — Listicle / Tutorial / Comparison / Mistakes / Standard (auto-guess from topic).
   - **Q4 CTA goal** — Save-bait (8, dense) / Reach (5, comment-to-DM) / Traffic (6, link-in-bio).
   - **Auto-defaulted, not asked:** accent = per-tool map; research depth = deep iff sources pasted;
     voice = `eric-tech-tone` if present else peer/confident. Reported in one line, user can override.
3. **Research** (if sources/repos) — `research-playbook.md`: WebSearch/firecrawl for links;
   `gh`/web for repos (stars, one-line value, "why it matters"). Condense to notes.
4. **Write copy** via embedded `copy-frameworks.md`:
   - Cover **hook formulas** (value/listicle, contrarian, curiosity-result, "stop X do this").
   - Per item: **"what it is" + "which means [benefit to you]"** bridge (the So-What engine).
   - **Specificity gate** (vague→concrete) + **mandatory anti-AI scrub** (cut very/just/leverage/
     seamless/robust/"in today's fast-paced world"/"dive in"/"game-changer", passive→active, no `!`).
   - **Retention:** number the payload + promise it on the cover; open-loop tails ("…but #4 →");
     **save-reason CTA** ("Save this — you'll want it next time you start a project").
   - Density: headline ≤7 words · subhead ≤12 · ≤3 bullets ≤6 words · one idea per slide.
5. **Emit `carousel-spec.md`** to `./carousel/<slug>/` (default). In the yt-all-tools repo this
   maps to `main💥/slides/<slug>/`. Includes a skimmable **ASCII layout diagram** + per-slide blocks.
6. **Show the ASCII diagram + 2–3 cover-headline options in chat**, confirm copy, iterate, hand off.

**`carousel-spec.md` per-slide schema:**
`n · type(cover|item|howto|cta) · badge · headline · subhead · bullets[] · open_loop_tail ·
featured_tool · logo_file · accent_hex · character_pose · card_style · url`

**ASCII diagram** (shown in chat + written into the spec) — "Top 5 GitHub repos":
```
COVER → 01 → 02 → 03 → 04 → 05 → HOW-TO → CTA      (8 slides · "5 repos" promised on cover)
┌──────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌──────┐┌──────┐
│"5 dev││01/5 ││02/5 ││03/5 ││04/5 ││05/5 ││3 steps││"Save  │
│repos ││logo ││logo ││logo ││logo ││logo ││to use ││this + │
│swipe→││3bul ││3bul ││3bul ││3bul ││3bul ││signpost││comment│
│blue  ││tool ││tool ││tool ││tool ││tool ││ blue  ││ REPOS"│
└──────┘└─────┘└─────┘└─────┘└─────┘└─────┘└──────┘└──────┘
 hook    open-loop tails carry the swipe →→→            save-reason CTA
```

---

## 5. Skill 2 — `instagram-carousel-generate` (pure GPT Image 2, fully-rendered slides)

**Trigger:** "generate the carousel", "render the slides", "/instagram-carousel-generate", or
auto-handoff after plan approval.

> **Chosen approach:** full slides — text, card, logo and all — are rendered by HiggsField
> `gpt_image_2`, for the "baked-into-the-3D-world" look of the reference carousel. We accept the
> known text-rendering risk and counter it with the mitigations below. (A hybrid PIL-overlay path
> stays documented in `references/plate-templates.md` as a fallback if text quality is unacceptable.)

**Prereqs (checked first, `higgsfield-setup.md`):** HiggsField via **CLI** (`higgsfield` on PATH +
`higgsfield account status` OK) **or MCP** (Clockwork/cowork). Plus Python 3 + Pillow (for crop only).
If missing: print exact install/auth commands + MCP connector name, then stop.

**Text-accuracy mitigations (because everything is generated):**
- Enforce the plan's density caps hard — headline ≤7 words, bullets ≤6 words, short URLs.
- `batch_size 2` per slide → auto-pick the cleanest, surface both for tricky text.
- Per-slide regeneration is cheap and isolated (never re-batch the whole deck for one bad slide).
- Prompt spells the exact text in quotes + "render this text exactly, correct spelling, no extra words."

**Consistency mechanism (no drift):** one **fixed reference set reused identically on every slide**
— canonical `clawd-voxel.png` + the once-approved **cover** + `assets/style-reference/` few-shot —
passed as repeated `--image` refs with the **same locked preamble** and a **pinned seed** (discover
via `higgsfield model get gpt_image_2 --json`; one seed for the whole deck). Never chain slide N−1.

**Flow**
1. Read `carousel-spec.md`; resolve every `logo_file`/`character_pose` via the asset contract —
   **abort before any credits if a reference is missing.**
2. **Cost gate:** `higgsfield generate cost gpt_image_2 …` → show total estimate × slide count,
   require one confirmation before the batch.
3. **BFS — approve the cover.** Generate the cover (`aspect_ratio 3:4`, `resolution 2k`), crop to
   1080×1350, show the user; lock the look + seed, or adjust once.
4. **DFS — all remaining slides** with the fixed reference set + pinned seed (serial; write each as
   it completes; skip already-rendered on re-run; `batch_size 2`, keep best).
5. **Crop** each to exactly 1080×1350 (Pillow, center-crop, no padding).
6. **Verify (gates "done"):** terminal status = success (not nsfw/ip_detected/failed) · PNG,
   non-zero, exactly 1080×1350 · **sky/grass mean-color within tolerance of cover** (drift proxy) ·
   build a **contact-sheet montage** + report credits spent vs estimate · flag any slide whose
   generated text the agent reads back as wrong (visual check) for one-tap regen.
7. Report paths + contact sheet. Single-slide fixes regen that one slide only.

**Aspect ratio:** generate `3:4` @ `2k` (1080×1440), center-crop to exactly 1080×1350 (trims 90px,
content kept center). No padding (letterbox bars look broken on IG).

**IP note:** naming brands + asking the model to draw logos can trigger `ip_detected` rejections.
The wrapper detects non-success terminal statuses and stops cleanly; if a brand logo is rejected,
fall back to passing that logo as a reference `--image` (or the documented PIL-paste fallback).

**MCP vs CLI:** `generate_carousel.py` is the CLI-mode renderer + cropper for both modes. On the MCP
path the *skill/agent* drives the HiggsField MCP tools call-by-call, then runs the crop locally.
Documented explicitly — one Python wrapper does not cover both.

---

## 6. Standalone & cross-harness strategy

- **No superpowers:** `intake-questions.md` embeds a ≤4-question brainstorming-lite + marketing grill.
- **No forced marketing install:** `copy-frameworks.md` distills `marcolang@instagram-carousel` +
  `mkt-social-content`/`mkt-copywriting`/`mkt-copy-editing` (attributed in a `## Credits`). If those
  skills are present, the plan skill may reference them for extra depth.
- **HiggsField is the one hard external dep**, made explicit in `higgsfield-setup.md` (CLI + MCP).
- **Install reality (honest):** the verified path is the standard Claude Code plugin marketplace
  flow, which every Claude Code host (incl. Clockwork/cowork) inherits:
  `/plugin marketplace add EricTechPro/instagram-carousel-skills` →
  `/plugin install instagram-carousel@instagram-carousel-skills`. MCP is connected at the **harness
  level** (host's connector UI), not by this repo. README marks any cowork-specific step as
  "assumed" unless verified.

---

## 7. README (superpowers-style, short)

Order: one-line what-it-is → **install block first** (plugin marketplace; clone+install.sh;
`--global`) → 60-sec "how it works" (plan → generate, the two-layer model in one sentence) →
HiggsField setup → Requirements → the two skills at a glance → sample carousel image → "What this
is NOT" → Credits → License. Lead with the copy-pasteable install command.

---

## 8. Decisions resolved (were open in v1)

- **Repo name:** `instagram-carousel-skills`. **Plugin name:** `instagram-carousel`.
- **Logos:** bundle a **curated** subset (Clawd + common dev-tool logos) in `character-references/`;
  `$IG_CAROUSEL_CHARACTER_DIR` overrides for "bring your own."
- **Default output:** `./carousel/<slug>/` in any project; `main💥/slides/<slug>/` only in yt-all-tools.
- **Clawd for others:** ship the mascot as default; override via env var.
- **Open spike (pre-build, 1 slide):** bake off `gpt_image_2` vs **Nano Banana 2** for the
  Clawd-bearing plate (NB2 is reference/character-trained, up to 8 refs). Pick whichever holds the
  mascot better; the rest of the pipeline is generator-agnostic.

---

## 9. Acceptance criteria

- Fresh clone in scratch dir → `install.sh` → both skills load; asset contract resolves.
- `plan` → valid `carousel-spec.md` + ASCII diagram from topic + 1 source, asking ≤4 Qs, copy passes
  the anti-AI scrub.
- `generate` → N slides at exactly 1080×1350, text/logos pixel-accurate, visibly consistent world,
  contact sheet produced, no safe-zone violations, credits reported.
- README install (plugin + clone) followable end-to-end; no hardcoded `/Users/...` paths or IDs.
- CI smoke (`install.sh` into tmp, both SKILL.md present) passes.
