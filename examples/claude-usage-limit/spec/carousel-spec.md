---
topic: 5 settings that stopped my Claude Code usage limit
slug: claude-usage-limit
sequence: listicle
slide_count: 8
cta_goal: reach            # save-bait | reach | traffic
handle: "@erictechpro"                # real IG account username (from BRAND.md) — lettered into every slide
accent_default: "#D97757"             # Claude orange — the through-line for this Claude Code deck
mascot: "Clawd — a cute rounded orange voxel mascot, sometimes a tiny gold crown"
style: "polished 3D voxel children's-book render, sunny blue sky + green grass"
surface: "a cream paper note pinned to a wooden signboard"
style_ref: _reference-style
audience: "Claude Code users who hit their usage limit daily"
payoff: "5 settings that stop the limit — fix #1 drops MCP overhead 11.3% to 3%"
---

# Layout
```
COVER → PROBLEM → 01 → 02 → 03 → 04 → 05 → CTA        (8 slides · "5 fixes" promised on cover)
┌──────┐┌──────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌──────┐
│"19%  ││"paid ││01/5 ││02/5 ││03/5 ││04/5 ││05/5 ││"Save +│
│before││before││MCP  ││skills││CLAUDE││settings││deny ││comment│
│type" ││type" ││3bul ││3bul ││.md  ││3bul ││rules││TOKENS"│
└──────┘└──────┘└─────┘└─────┘└─────┘└─────┘└─────┘└──────┘
 hook    agitate  →→→ open-loop tails carry the swipe →→→     DM-trigger CTA
```

## Slide 1
```text
┌──────────────────────────────── slide 1 · COVER
│   ‹ 5 FIXES INSIDE ›                        badge pill
│   ██ Claude burns 19% before you type       headline — Archivo Black, huge
│   ▁  the settings that stopped my daily limit   subhead — one line
│   ♛  crowned Clawd guarding a context bar    character_pose (Clawd + world)
│   [claude]                        swipe →   logo · open-loop tail
│   @erictechpro                              handle · bottom-left
└───────────────────────────────────────────────
```
- type: cover
- badge: "5 FIXES INSIDE"
- headline: "Claude burns 19% before you type"
- subhead: "the 5 settings that stopped my daily limit"
- bullets: []
- open_loop_tail: "swipe →"
- featured_tool: claude
- logo_file: claude-logo.png
- accent_hex: "#D97757"
- character_pose: "a wide horizontal context-window progress bar styled like a terminal status meter — a rounded dark track filled 19% from the left in red-orange, with a small '19%' label at the end — shown clearly on its own band below the headline, fully visible and unobstructed; crowned Clawd stands to the right of the bar pointing up at it, not overlapping it"
- card_style: none
- mimic_ui: none
- url: ""

## Slide 2
```text
┌──────────────────────────────── slide 2 · PROBLEM (agitated)
│   ‹ THE LEAK ›                              badge pill
│   ██ You pay before prompt one              headline
│   ▁  MCP + skills + CLAUDE.md load first    subhead
│   • MCP tools: 11.3% of context             ≤3 bullets
│   • skills + CLAUDE.md stack on top
│   • then you finally start typing
│   ♛  Clawd watching a meter fill            character_pose
│   [claude]        fix #1 cuts it to 3% →    logo · tail
│   @erictechpro
└───────────────────────────────────────────────
```
- type: item
- badge: "THE LEAK"
- headline: "See the leak yourself"
- subhead: "run /context before you type — it's already 19% full"
- bullets: []
- terminal_lines: ["> /context", "context: 19% used before prompt 1", "MCP tools     11.3%", "CLAUDE.md      1.6%"]
- open_loop_tail: "fix #1 cuts it to 3% →"
- featured_tool: claude
- logo_file: claude-logo.png
- accent_hex: "#D97757"
- character_pose: "a small orange voxel Clawd mascot standing on the smooth grass beside the signpost, looking up worriedly at a small glowing red progress cube"
- card_style: wooden-sign
- mimic_ui: none
- url: ""

## Slide 3
```text
┌──────────────────────────────── slide 3 · FIX 01
│   ‹ 01/5 ›                                  badge
│   ██ Turn on Tool Search                    headline
│   ▁  one env var drops MCP 11.3% → 3%       subhead
│   ⌨  export ENABLE_TOOL_SEARCH=1            terminal (CLI window)
│   • lazy-loads MCP tools                    ≤3 bullets
│   • move Sentry/Vercel/Linear to CLI
│   • saves 800–1400 tokens per call
│   [cli]            …but #3 frees the most →  logo · tail
│   @erictechpro
└───────────────────────────────────────────────
```
- type: item
- badge: "01/5"
- headline: "Turn on Tool Search"
- subhead: "one env var drops MCP from 11.3% to 3%"
- bullets: ["Lazy-loads MCP tools", "Move Sentry/Vercel to CLI", "Saves 800–1400 tokens/call"]
- open_loop_tail: "…but #3 frees the most →"
- featured_tool: cli
- logo_file: cli-logo.png
- accent_hex: "#D97757"
- character_pose: "a small orange voxel Clawd standing on the smooth grass beside the signpost, holding up one glowing lightning-bolt block with both hands; plain uncluttered background, lots of open sky, NO wall of blocks, no scattered icons or extra props"
- card_style: wooden-sign
- mimic_ui: none
- terminal_lines: ["> export ENABLE_TOOL_SEARCH=true"]
- url: "github.com/obra/superpowers"

## Slide 4
```text
┌──────────────────────────────── slide 4 · FIX 02
│   ‹ 02/5 ›                                  badge
│   ██ Audit your skills                      headline
│   ▁  dead skills sit in context all session  subhead
│   • condense with Superpowers               ≤3 bullets
│   • cut skills you never call
│   • reclaims 1–3% per session
│   ♛  Clawd sorting skill cards              character_pose
│   [claude]      #3 reads on every prompt →  logo · tail
│   @erictechpro
└───────────────────────────────────────────────
```
- type: item
- badge: "02/5"
- headline: "Audit your skills"
- subhead: "dead skills sit in context every session"
- bullets: ["Condense with Superpowers", "Cut skills you never call", "Reclaims 1–3% per session"]
- terminal_lines: ["> ls ~/.claude/skills"]
- open_loop_tail: "#3 reads on every prompt →"
- featured_tool: claude
- logo_file: claude-logo.png
- accent_hex: "#D97757"
- character_pose: "a small orange voxel Clawd standing on the smooth grass beside the signpost, calmly holding a single glowing skill card; plain uncluttered background, NO piles of cards, no books, no scattered tags or extra props"
- card_style: wooden-sign
- mimic_ui: none
- url: "github.com/obra/superpowers"

## Slide 5
```text
┌──────────────────────────────── slide 5 · FIX 03
│   ‹ 03/5 ›                                  badge
│   ██ Put CLAUDE.md on a diet                headline
│   ▁  every session reads it before you type  subhead
│   • cut to under 200 lines                  ≤3 bullets
│   • move specifics to skills
│   • stop paying for dead rules
│   ♛  Clawd trimming a long scroll           character_pose
│   [claude]    #4 stops a silent drain →     logo · tail
│   @erictechpro
└───────────────────────────────────────────────
```
- type: item
- badge: "03/5"
- headline: "Put CLAUDE.md on a diet"
- subhead: "every session reads it before you type"
- bullets: ["Cut to under 200 lines", "Move specifics to skills", "Stop paying for dead rules"]
- code_file: "CLAUDE.md"
- code_lines: ["# CLAUDE.md — 38 lines", "## Stack", "- Next.js + Supabase", "## Rules", "- tests before commit", "# details -> .claude/skills/"]
- open_loop_tail: "#4 stops a silent drain →"
- featured_tool: claude
- logo_file: claude-logo.png
- accent_hex: "#D97757"
- character_pose: "Clawd snipping a long unrolled paper scroll with oversized scissors, the cut-off half fluttering away"
- card_style: wooden-sign
- mimic_ui: none
- url: ""

## Slide 6
```text
┌──────────────────────────────── slide 6 · FIX 04
│   ‹ 04/5 ›                                  badge
│   ██ Fix two hidden settings                headline
│   ▁  they stop a silent token drain          subhead
│   ⌨  export MAX_OUTPUT_LENGTH=20000         terminal (CLI window)
│   • lower auto-compact threshold            ≤3 bullets
│   • cap output length
│   • kills silent bash retries
│   [cli]      #5 keeps junk out for good →   logo · tail
│   @erictechpro
└───────────────────────────────────────────────
```
- type: item
- badge: "04/5"
- headline: "Fix two hidden settings"
- subhead: "auto-compact and output caps stop silent burn"
- bullets: ["Compact early at 75%", "Truncate giant bash output", "Stops silent context drain"]
- open_loop_tail: "#5 keeps junk out for good →"
- featured_tool: cli
- logo_file: cli-logo.png
- accent_hex: "#D97757"
- character_pose: "a small orange voxel Clawd standing on the smooth grass beside the signpost, turning one big dial with both hands; plain uncluttered background, NO panel of gauges, no extra props"
- card_style: wooden-sign
- mimic_ui: none
- terminal_lines: ["> export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=75", "> export BASH_MAX_OUTPUT_LENGTH=50000"]
- url: ""

## Slide 7
```text
┌──────────────────────────────── slide 7 · FIX 05
│   ‹ 05/5 ›                                  badge
│   ██ Deny the token hogs                    headline
│   ▁  block files Claude should never read    subhead
│   • deny node_modules + dist                ≤3 bullets
│   • deny lockfiles
│   • no more 5K-token reads
│   ♛  Clawd as a bouncer                     character_pose
│   [cli]                                     logo (strong close, no tail)
│   @erictechpro
└───────────────────────────────────────────────
```
- type: item
- badge: "05/5"
- headline: "Deny the token hogs"
- subhead: "block files Claude should never read"
- bullets: ["Deny node_modules + dist", "Deny lockfiles", "No more 5K-token reads"]
- code_file: "settings.json"
- code_lines: ["\"permissions\": {", "  \"deny\": [", "    \"Read(node_modules/**)\",", "    \"Read(dist/**)\",", "    \"Read(**/*.lock)\"", "  ]", "}"]
- open_loop_tail: ""
- featured_tool: cli
- logo_file: cli-logo.png
- accent_hex: "#D97757"
- character_pose: "a small orange voxel Clawd standing on the smooth grass beside the signpost, dressed as a bouncer with one hand raised in a clear stop gesture beside a single small crate; plain uncluttered background, NO stacks of crates, no extra props"
- card_style: wooden-sign
- mimic_ui: none
- url: ""

## Slide 8
```text
┌──────────────────────────────── slide 8 · CTA
│   ‹ FREE ›                                  badge
│   ██ Want my exact settings?                headline
│   ▁  comment TOKENS — I'll DM the config     subhead
│   ♛  Clawd holding a speech-bubble sign      character_pose
│   [claude]                                  logo
│   @erictechpro                              handle
└───────────────────────────────────────────────
```
- type: cta
- badge: "FREE"
- headline: "Want my exact settings?"
- subhead: "Comment TOKENS and I'll DM you the config"
- bullets: []
- open_loop_tail: ""
- featured_tool: claude
- logo_file: claude-logo.png
- accent_hex: "#D97757"
- character_pose: "a centered full-body orange voxel Clawd (tiny gold crown, sunglasses) standing on smooth grass, holding a big cream rounded speech-bubble overhead with both arms — the bubble is the text surface; TOKENS is the large orange word inside it"
- card_style: speech-bubble
- mimic_ui: none
- url: ""

# Post copy
caption: |
  Claude was eating 19% of my context before I typed a single prompt.
  These 5 settings stopped me hitting the usage limit daily.
  Fix #1 alone drops MCP overhead from 11.3% to 3%.
  Comment TOKENS and I'll DM you the exact config.
hashtags: ["#claudeai", "#claudecode", "#anthropic", "#aitools", "#devtools", "#coding", "#programming", "#softwareengineering", "#aicoding", "#buildinpublic"]
dm_trigger: "TOKENS"
