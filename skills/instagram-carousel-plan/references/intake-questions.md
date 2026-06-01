# Intake Questions (embedded brainstorming-lite + marketing grill)

Ask **at most 4** via `AskUserQuestion`. List the best default first. The style is already
decided — these questions are only about the *content strategy*, not the look.

## The 4 questions

### Q1 — Audience + pain  *(the one that matters most)*
> "Who is this for, and what's the painful before-state?"
Drives the hook, the problem framing, and the emotional register. Offer 2–3 topic-derived presets
+ "Other (type it)". Example presets for a dev-tools topic:
- "Devs drowning in boilerplate / setup"
- "Founders who can't ship fast enough"
- "People who know AI tools exist but not which to use"

### Q2 — Payoff + proof
> "What's the after-state, and do you have a hard number?"
Feeds the cover's specificity and the CTA recap. Presets:
- "A concrete metric (e.g. 4 hrs → 15 min)"
- "A clear outcome, no number (ship faster / never X again)"
- "Status/credibility (used by N people, N stars)"

### Q3 — Sequence
> "What shape is this?"
Auto-guess from the topic phrasing, then confirm:
- **Listicle** — "top N", "N tools", "N tips" (default for "top N" topics)
- **Tutorial** — "how to X", a process
- **Comparison** — "X vs Y"
- **Mistakes** — "N mistakes", "stop doing X" (high-save)
- **Standard** — hook → problem → solution → proof → CTA (default otherwise)

### Q4 — CTA goal
> "What should the post *do*?"
Changes the whole arc and the final slide:
- **Save-bait** — dense reference, "save this", ~8 slides (default for listicles)
- **Reach** — comment-to-DM funnel, ~5 slides
- **Traffic** — link-in-bio, ~6 slides

## Auto-decided — DO NOT ask (defaults from `BRAND.md` at the project root)
- **Accent color** → per-tool brand map, falling back to BRAND.md `default_accent`.
- **Research depth** → deep if sources were pasted, skip if none.
- **Voice** → the voice skill named in BRAND.md (`eric-tech-tone`) if present, else peer-to-peer confident.
- **Style** → whatever images are in `_reference-style/` (project root).

Report these in one line so the user can override:
> "Defaults: per-tool accents · deep research on your 3 links · peer voice. Say if you'd rather change any."

## Rule
If the user already answered something in their opening message ("top 5 repos, comment-to-DM,
for junior devs"), **don't re-ask it** — confirm it in the one-line summary and skip that question.
Fewer questions is better; 0–2 is fine when the brief is rich.
