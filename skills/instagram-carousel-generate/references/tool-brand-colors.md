# Tool → accent color + logo (shared by plan & generate)

When a slide features a specific tool/brand, the accent color and logo come from here. If the
featured tool isn't listed, use the default Eric Tech blue `#2BAADF` and no logo (or the closest
match). Logo files live in `character-references/` (bundled; swappable / extendable by the user).

| Tool / brand | accent_hex | logo_file |
|---|---|---|
| (default / Eric Tech) | `#2BAADF` | — |
| Claude / Anthropic | `#D97757` | claude-logo.png |
| Clawd (mascot) | `#D97757` | claude-mascot-sticker.png |
| GitHub | `#0F172A` | github-logo.png |
| Git | `#F05133` | git-logo.png |
| OpenAI / Codex | `#8B5CF6` | — (purple accent; add a logo to use one) |
| Stripe | `#635BFF` | stripe-logo.png |
| Supabase | `#3ECF8E` | supabase-logo.png |
| Figma | `#F24E1E` | figma-logo.png |
| VS Code | `#007ACC` | vscode-logo.png |
| Playwright | `#2EAD33` | playwright-logo.png |
| Obsidian | `#7C3AED` | obsidian-logo.png |
| YouTube | `#FF0000` | youtube-logo.png |
| CLI / terminal | `#0F172A` | cli-logo.png |

## Adding a tool
1. Drop ``<tool>-logo.png`` into `character-references/` (transparent PNG, square-ish).
2. Add a row here with its brand hex.
Both skills pick it up automatically — no reindexing.

## Notes
- These hex values are the tools' recognizable brand colors; verify against the brand's guidelines
  if exactness matters for a sponsor.
- Accent is applied by `compose_slide.py` to markers, key headline words, and the swipe/CTA chrome.
- The logo is **pasted as a real PNG** (never generated) to keep brand marks faithful and avoid
  `ip_detected` rejections from the image model.
