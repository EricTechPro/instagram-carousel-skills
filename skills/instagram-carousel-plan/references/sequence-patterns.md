# Sequence Patterns

Five carousel shapes. Each keeps the locked visual world; only copy + slide count change.
All use: **numbered payload promised on the cover**, **open-loop tails** between slides, and a
**save-reason CTA** as the last slide.

## Listicle  (default for "top N", 7–9 slides)
`Cover(promise N) → 01 → 02 → … → 0N → [optional How-to] → CTA`
- Each item slide: badge "0k/N", headline = the item, subhead = "which means…", ≤3 bullets, the
  featured tool's logo + accent, open-loop tail.
- Strongest item at 01, second-strongest at 0N.

## Tutorial  (how-to / process, 7 slides)
`Cover(the outcome) → Why it matters → Step 1 → Step 2 → Step 3 → Result → CTA`
- Slide 2 names the stakes (what you lose without this). Steps are numbered, one action each.

## Comparison  (X vs Y, 5–6 slides)
`Cover(the matchup) → Option A → Option B → Head-to-head → Verdict → CTA`
- A and B slides use each tool's own accent; the verdict uses your pick's accent.

## Mistakes  (high-save, 6–8 slides)
`Cover("N mistakes killing your X") → Mistake 01 → … → 0N → The fix → CTA`
- Each mistake slide: the wrong thing (problem-agitate) + the one-line correction. Contrarian hook.

## Standard  (default otherwise, 6–7 slides)
`Cover(hook) → The problem (agitated) → The solution → Proof → How it works → CTA`
- Don't jump cover → solution. The pain slide (2) is what makes the payoff land.

## "Mimic a source UI" slides
When the research notes a source's distinctive look (a GitHub repo header, a dashboard, a code
editor), an item slide may render that as a **panel inside the cream card** instead of bullets.
Set `mimic_ui` on that slide (e.g. `mimic_ui: github-repo-header`) and keep a one-line caption.
`instagram-carousel-generate` turns that hint into the panel — see its `slide-templates.md`.

## Slide-count guardrail
Instagram allows up to 20, but 6–10 is the sweet spot. If the topic has more items than that,
group them or split into two carousels — tell the user, don't silently truncate.
