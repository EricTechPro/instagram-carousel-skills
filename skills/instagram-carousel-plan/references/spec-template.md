# carousel-spec.md template

Write this to `instagram-carousel/<topic-slug>/spec/carousel-spec.md`. It is the **contract** the
generate skill renders. The user may edit any field directly before generating.

Use this exact structure (YAML-ish front block + one `## Slide N` block each + a caption block).

**Lead every `## Slide N` with a wireframe** — a small ASCII mock showing where each element lands on
the 1080×1350 canvas (badge → headline → subhead → ≤3 bullets → the Clawd/world → logo · tail ·
@handle). It lets the user *see* each slide like a layout mock before any image is rendered. The
renderer ignores it and draws from the `- key: value` fields beneath it — so keep wireframe lines
starting with `│`, `┌`, `└`, spaces, or `•` (never `#` or `- `, which would confuse the parser):

````markdown
---
topic: Top 5 GitHub repos every dev should clone
slug: top-5-github-repos
sequence: listicle
slide_count: 8
cta_goal: reach            # save-bait | reach | traffic
handle: "@erictech"                   # default from BRAND.md — don't invent one
style_ref: _reference-style           # project-root deck; swap images to change the look
accent_default: "#2BAADF"
audience: "junior devs drowning in boilerplate"
payoff: "clone 5 repos, ship faster this week"
---

# Layout
```
COVER → 01 → 02 → 03 → 04 → 05 → HOW-TO → CTA      (8 slides · "5 repos" promised on cover)
┌──────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌──────┐┌──────┐
│"5 dev││01/5 ││02/5 ││03/5 ││04/5 ││05/5 ││3 steps││"Save +│
│repos ││logo ││logo ││logo ││logo ││logo ││to use ││comment│
│swipe→││3bul ││3bul ││3bul ││3bul ││3bul ││signpost││REPOS" │
└──────┘└─────┘└─────┘└─────┘└─────┘└─────┘└──────┘└──────┘
 hook    →→→ open-loop tails carry the swipe →→→        save-reason CTA
```

## Slide 1
```text
┌──────────────────────────────── slide 1 · COVER
│   ‹ ALL FREE ›                              badge pill (omit on a bare cover)
│   ██ headline — Archivo Black, huge
│   ▁  subhead — one line
│   ♛  character_pose (Clawd + generated world)
│   [logo]                          swipe →   logo · open-loop tail
│   @handle                                   handle · bottom-left
└───────────────────────────────────────────────
```
- type: cover
- badge: "ALL FREE"
- headline: "5 repos every dev should clone"
- subhead: "stop rebuilding boilerplate from scratch"
- bullets: []
- open_loop_tail: "swipe →"
- featured_tool: github
- logo_file: github-logo.png
- accent_hex: "#2BAADF"
- character_pose: "crowned Clawd on a pile of code blocks, arms raised"
- card_style: none
- mimic_ui: none
- url: ""

## Slide 2
- type: item
- badge: "01/5"
- headline: "<repo name>"
- subhead: "which means: <benefit to you>"
- bullets: ["<fact 1>", "<fact 2>", "<fact 3>"]
- open_loop_tail: "…but #2 is the one nobody clones →"
- featured_tool: <tool>
- logo_file: <tool>-logo.png
- accent_hex: "<tool hex>"
- character_pose: "Clawd holding a wooden signpost"
- card_style: wooden-sign
- mimic_ui: github-repo-header      # optional: render the repo's header look in the card
- url: "github.com/owner/repo"

# … slides 3–6 same shape (items 02–05) …

## Slide 7
- type: howto
- badge: "PICK ANY METHOD"
- headline: "How to clone any repo"
- subhead: ""
- bullets: ["Method 01 — gh repo clone", "Method 02 — git clone URL", "Method 03 — download ZIP"]
- open_loop_tail: ""
- featured_tool: git
- logo_file: git-logo.png
- accent_hex: "#2BAADF"
- character_pose: "three Clawds at signposts"
- card_style: three-signposts
- mimic_ui: none
- url: ""

## Slide 8
- type: cta
- badge: "FREE GUIDE"
- headline: "Want the links?"
- subhead: "Comment REPOS and I'll DM you all 5"
- bullets: []
- open_loop_tail: ""
- featured_tool: github
- logo_file: github-logo.png
- accent_hex: "#2BAADF"
- character_pose: "Clawd holding a speech-bubble sign overhead"
- card_style: speech-bubble
- mimic_ui: none
- url: ""

# Post copy
caption: |
  5 repos that do the boilerplate for you 👇
  I cloned these so you don't have to rebuild auth, tests, and CI from zero.
  #2 saved me a full day this week.
  Comment REPOS and I'll DM you all five.
hashtags: ["#coding", "#developer", "#github", "#opensource", "#devtools", "#programming", "#claudeai", "#buildinpublic"]
dm_trigger: "REPOS"
````

## Rules for filling it
- `handle` + `accent_default`: read from `BRAND.md` at the project root (ships as `@erictech` /
  `#2BAADF`). Never invent a handle or accent — if `BRAND.md` is missing, ask the user once.
- `logo_file` + `accent_hex`: look up the featured tool in
  `../instagram-carousel-generate/references/tool-brand-colors.md`. Fall back to the BRAND.md
  `default_accent` if the tool has none.
- Respect density caps (headline ≤7 words, ≤3 bullets ≤6 words). **Generate renders the whole slide
  — text included — via GPT Image 2**, so keep each slide to ONE big idea with minimal copy and a
  punchy headline; it has to stop a scroll.
- Every slide gets a **vivid `character_pose` — it becomes the actual rendered scene**, so make it
  specific to that slide's idea. The topic is fanning out many agents, so visualize it: a master
  orchestrating a crowd of agent-Clawds, finder/refuter pairs, a search fan-out, an agent per
  document. (`card_style` is just a hint.)
- `terminal: "<command>"` renders as a **Claude Code CLI window** (dots + Claude logo + the command +
  an "Opus 4.8" status bar). Use it on workflow/command slides; keep the command short.
- Leave `mimic_ui: none` unless the research flagged a worth-showing source UI.
- Run the anti-AI scrub on every text field before saving.
