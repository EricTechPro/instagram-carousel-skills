# Brand profile — Hermes

A second brand profile, alongside the default `BRAND.md` (Eric Tech / Claude). It proves the skills
are **not locked to one brand**: same skill + scripts, totally different identity (vintage manga vs
voxel). To use it, the plan skill fills the spec `meta` from the values below; generate reads the
spec — nothing brand-specific is hardcoded in the scripts.

## Identity
- `handle`: `@erictechpro`
- `default_accent`: `monochrome`   <!-- pure black & white; emphasis is italic/bold, not a color -->
- `voice`: peer-to-peer, confident, concrete

## Mascot / host
- `name`: `Hermes`
- `description`: a stylish **vintage shoujo-manga girl** with a headband, drawn in **bold black ink**
  (see `character-references/hermes-logo.png`); she is the recurring host across slides.
- `reference_images`: `character-references/hermes-logo.png` (no full deck yet — passed as the
  few-shot style/character reference via `IG_CAROUSEL_STYLE`).

## World / style
- `style`: *Vintage shoujo manga — bold black ink line-art with screentone shading, high-contrast
  monochrome black & white, dramatic paneling, halftone dots. No color.*
- `surface`: *a clean manga title panel / boxed caption* (where the text sits on item slides).

## How the spec meta is filled (plan skill)
Write these into `carousel-spec.md` front-matter so generate renders Hermes, not Claude:
```yaml
handle: "@erictechpro"
accent_default: monochrome
mascot: "Hermes — a stylish vintage shoujo-manga girl with a headband, in bold black ink"
style: "vintage shoujo manga, bold black ink line-art with screentone, monochrome black & white, high-contrast, dramatic panels"
surface: "a clean manga title panel / caption box"
```
`character_pose` on each slide casts **Hermes (the manga girl)** as the host — reading, presenting,
reacting — in a manga panel. Leave `terminal` off unless the content truly shows a CLI.

## To generate with this profile
Pass the logo as the style reference:
```bash
IG_CAROUSEL_ASSETS="$PWD" IG_CAROUSEL_STYLE="examples/<slug>/style-ref" \
  python skills/instagram-carousel-generate/scripts/generate_carousel.py <spec> --allow-cli-spend --only 1
```
