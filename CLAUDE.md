# instagram-carousel-skills — repo rules

A standalone, public skill repo. Two skills: `instagram-carousel-plan` and
`instagram-carousel-generate`.

## Portability is the prime directive
- **No hardcoded user paths or personal IDs** in committed files. Resolve assets via the
  documented order: `$IG_CAROUSEL_ASSETS` → skill-relative `../../assets` → `~/.claude/instagram-carousel/`.
- **Brand defaults live in `BRAND.md`, not in the skills.** Handle, accent, voice, and mascot are
  read from `BRAND.md` at the project root; the style deck is `_reference-style/` (also project
  root, resolved via `$IG_CAROUSEL_STYLE` → project root → installed assets → legacy). Don't
  re-hardcode `@erictech` / `#2BAADF` / `Clawd` into a skill — point at `BRAND.md`.
- **No dependency on Superpowers or any sibling project.** The useful parts are embedded in
  `references/` (and attributed). If an external skill is present, reference it as a bonus, never require it.
- Everything must work after a single `/plugin install` or `./install.sh`.

## Layout
- `skills/<name>/SKILL.md` + `references/` (+ `scripts/` for generate).
- `marketplace.json` at repo root (`source: "./"`); `.claude-plugin/plugin.json` is the plugin.
- `VERSION` is the single source of truth; keep `plugin.json` + `marketplace.json` in sync.

## Cutting a release (super-board style)
One command does the version bump + tag + zip + GitHub release:
1. Add a `## v<version> — <date>` section to `RELEASE-NOTES.md` describing the changes.
2. Run `./scripts/release.sh <version>` (e.g. `0.2.0`). Use `--dry-run` first to preview.

It validates semver + a clean tree, syncs `VERSION` + `skills/*/VERSION` + `plugin.json` +
`marketplace.json`, builds the `.claude/`-shaped release zip (no `__pycache__`/`.DS_Store`),
commits `release: vX.Y.Z`, tags, pushes, and creates the GitHub release using that version's
RELEASE-NOTES section as the body. Refuses to overwrite an existing tag/release.

## When editing skills
- Keep the plan/generate split sharp: planning never spends image credits; generation never rewrites copy.
- Generation must gate on a cost estimate and a prereq (HiggsField CLI or MCP) check before any spend.
- Don't break the asset-resolution contract or the CI smoke test (`.github/workflows/smoke.yml`).
