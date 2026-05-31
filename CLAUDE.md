# instagram-carousel-skills — repo rules

A standalone, public skill repo. Two skills: `instagram-carousel-plan` and
`instagram-carousel-generate`.

## Portability is the prime directive
- **No hardcoded user paths or personal IDs** in committed files. Resolve assets via the
  documented order: `$IG_CAROUSEL_ASSETS` → skill-relative `../../assets` → `~/.claude/instagram-carousel/`.
- **No dependency on Superpowers or any sibling project.** The useful parts are embedded in
  `references/` (and attributed). If an external skill is present, reference it as a bonus, never require it.
- Everything must work after a single `/plugin install` or `./install.sh`.

## Layout
- `skills/<name>/SKILL.md` + `references/` (+ `scripts/` for generate).
- `marketplace.json` at repo root (`source: "./"`); `.claude-plugin/plugin.json` is the plugin.
- `VERSION` is the single source of truth; keep `plugin.json` + `marketplace.json` in sync.

## When editing skills
- Keep the plan/generate split sharp: planning never spends image credits; generation never rewrites copy.
- Generation must gate on a cost estimate and a prereq (HiggsField CLI or MCP) check before any spend.
- Don't break the asset-resolution contract or the CI smoke test (`.github/workflows/smoke.yml`).
