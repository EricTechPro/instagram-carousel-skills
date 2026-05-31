# carousel-spec.md template

Write this to `instagram-carousel/<topic-slug>/carousel-spec.md`. It is the **contract** the
generate skill renders. The user may edit any field directly before generating.

Use this exact structure (YAML-ish front block + one `## Slide N` block each + a caption block):

````markdown
---
topic: Top 5 GitHub repos every dev should clone
slug: top-5-github-repos
sequence: listicle
slide_count: 8
cta_goal: reach            # save-bait | reach | traffic
handle: "@erictech"
style_ref: assets/style-reference     # swap images here to change the look
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
- `logo_file` + `accent_hex`: look up the featured tool in
  `../instagram-carousel-generate/references/tool-brand-colors.md`. Default blue `#2BAADF` if none.
- Respect density caps (headline ≤7 words, ≤3 bullets ≤6 words).
- Every slide gets a `character_pose` and a `card_style` from the generate skill's vocab.
- Leave `mimic_ui: none` unless the research flagged a worth-showing source UI.
- Run the anti-AI scrub on every text field before saving.
