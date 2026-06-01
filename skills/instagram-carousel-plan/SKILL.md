---
name: instagram-carousel-plan
description: Plan an Instagram carousel — research a topic/sources and write the per-slide copy, caption, hashtags, and comment-to-DM trigger into a reviewable carousel-spec.md (no images, no credits). Use whenever the user wants to plan, outline, draft, write, or structure an Instagram/IG carousel or swipe post, or turn/repurpose a topic, links, article, GitHub repos, or a video into one — even if they say "make" or "create" a carousel but have no spec yet. Also /instagram-carousel-plan. NOT for rendering images from an already-approved spec (use instagram-carousel-generate for that), and NOT for a website "carousel"/slider UI component, a LinkedIn post, a content calendar, or single-image graphics.
---

# Instagram Carousel — Plan

Spec-driven marketing: turn a topic (and any sources) into a **research wiki + `carousel-spec.md`**
the user approves *before* any image credits are spent. This skill writes words and structure only —
`instagram-carousel-generate` renders the images.

## When to use
- "Plan an Instagram carousel for <topic>"
- "I want to make a carousel about <these GitHub repos / this trend / this article>"
- User pastes links/sources and wants them turned into a carousel
- `/instagram-carousel-plan`

## When NOT to use
- The user already has an approved `carousel-spec.md` and wants images → `instagram-carousel-generate`
- Generic social copy unrelated to a carousel → a general copywriting skill

## The project folder it creates
Everything for one carousel lives under the **current project root** — one folder per topic, each
with the same three-part shape so every carousel is laid out identically (input → spec → output):
```
instagram-carousel/
└── <topic-slug>/                 e.g. claude-dynamic-workflows/
    ├── input/                    # the research "wiki" — one .md per source + sources.md index
    ├── spec/
    │   └── carousel-spec.md      # the approved spec (slides + caption + hashtags + DM-trigger)
    └── output/                   # slides (written later by instagram-carousel-generate)
```
Create `instagram-carousel/<topic-slug>/input/` first; slug the topic (lowercase, hyphens). If the
user already has a research folder, copy or point its notes into `input/` rather than starting blank.

## Workflow (research → copy → spec → approve)

### 1. Ask what they have
"What's the topic, and what resources do you have — links, GitHub repos, an article, a trend?"
Capture everything they paste. (e.g. "top 5 Claude skills" + 5 repo URLs.)

### 2. Intake — ask at most 4 questions
Read `references/intake-questions.md`. Ask with `AskUserQuestion` (2–3 options each, **best default
first**). Four or fewer:
1. **Audience + pain** — who it's for and the painful before-state.
2. **Payoff + proof** — the after-state and any hard number.
3. **Sequence** — Listicle / Tutorial / Comparison / Mistakes / Standard (auto-guess from topic).
4. **CTA goal** — Save-bait / Reach (comment-to-DM) / Traffic (link-in-bio).

**Do not ask** about accent color or research depth — auto-decide and report in one line.

### 3. Research → build the wiki
Read `references/research-playbook.md`. For each link: web search / firecrawl / WebFetch the facts.
For repos: `gh` or web for **stars, one-line "what it is", "why it matters"**, and notable UI/visual
detail worth showing (e.g. "GitHub repo header: black top nav, repo name, star count" — a slide can
*mimic* that look). Write each source to `input/<source-slug>.md` and an index `input/sources.md`.
This is the grounding "wiki" the copy is built from — no invented facts.

### 4. Write the copy
Read `references/copy-frameworks.md` and `references/sequence-patterns.md`. Apply, in order:
- **Cover hook** — pick a formula; make the headline *specific* (a number, a named outcome).
- **Per item** — `what it is` + **"which means <benefit to YOU>"** (the So-What bridge), grounded in
  the research. If a slide should *mimic a source UI* (a repo header, a screenshot), note it in
  `card_style` / a `mimic_ui` hint so generate can render that panel.
- **Retention** — number the payload + promise it on the cover; open-loop tails ("…but #4 →").
- **CTA** — a **save-reason** CTA matched to the chosen goal.
- **Post-level copy** — also write the **Instagram caption** (hook line + value + CTA), a **hashtag
  set** (mix of reach + niche), and the exact **"comment KEYWORD" DM-trigger** line.
- **Density caps** — headline ≤7 words · subhead ≤12 · ≤3 bullets ≤6 words · one idea/slide.
- **Anti-AI scrub (mandatory)** — run the cut-list in `copy-frameworks.md` before emitting.

### 5. Emit the spec
First read **`BRAND.md`** at the project root for the brand defaults (`handle`, `default_accent`,
`voice`) — never invent a handle or accent; if it's missing, ask the user once. The **`handle` is the
user's real Instagram account username** (the one the carousel will post from), and generate letters it
into *every* slide — so confirm it's right here, in cheap text, rather than after images are rendered
(changing it later forces a full re-render of the deck). Then write
`instagram-carousel/<topic-slug>/spec/carousel-spec.md` using `references/spec-template.md`:
global meta + **ASCII layout diagram** + one block per slide — **each led by an ASCII wireframe**
(where badge/headline/subhead/bullets/mascot/logo/handle land) so the user can review the layout
before rendering — + the caption/hashtags/DM-trigger block.

### 6. Approve + hand off (spec-driven marketing)
Show the **ASCII layout** and **2–3 cover-headline options** in chat (skimmable). Tell the user they
can **edit any text directly in `carousel-spec.md`** — once they're happy it's set in stone. Then:
> "Spec ready at `<path>`. Edit the copy there if you want, then say 'generate the carousel'." →
> `instagram-carousel-generate`.

## The spec schema (per slide)
`n · type(cover|item|howto|cta) · badge · headline · subhead · bullets[] · open_loop_tail ·
featured_tool · logo_file · accent_hex · character_pose · card_style · mimic_ui · url`

`logo_file` and `accent_hex` are auto-filled from
`../instagram-carousel-generate/references/tool-brand-colors.md` based on the featured tool.

## Files
| Path | Purpose |
|---|---|
| `references/intake-questions.md` | The ≤4 questions + smart defaults (embedded brainstorming-lite) |
| `references/copy-frameworks.md` | Hooks, So-What bridge, specificity, caption + CTA, anti-AI scrub |
| `references/sequence-patterns.md` | 5 sequence templates + retention mechanics |
| `references/research-playbook.md` | How to research links / repos / trends into the wiki |
| `references/spec-template.md` | `carousel-spec.md` schema + ASCII layout + caption block |
