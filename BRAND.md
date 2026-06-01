# Brand profile

One file that holds every brand default the carousel skills use. **Edit this to make the
carousels yours** — change the handle, accent, voice, and mascot, then swap the images in
`_reference-style/`. The values below ship configured for Eric Tech; replace them and both
skills follow. Nothing brand-specific is hardcoded in the skills.

## Identity
- `handle`: `@erictech`
- `default_accent`: `#2BAADF`   <!-- used when a slide's featured tool has no brand color -->
- `voice`: `eric-tech-tone`     <!-- a voice skill to use IF installed; otherwise: peer-to-peer, confident, concrete -->

## Mascot / character
- `name`: `Clawd`
- `description`: voxel / Minecraft-style orange mascot; sometimes a tiny gold crown ("the boss")
- `reference_images`: `_reference-style/`   <!-- the few-shot deck that defines the whole look -->

## World / style
The generated world (sky, grass, cream cards) is defined entirely by the images in
`_reference-style/`. Swap those images to restyle every future carousel — no code changes.

## How the skills read this
- **plan** fills each spec's `handle` and `accent_default` from *Identity* above, and picks the
  *voice* (the named skill if present, else the fallback). It never invents a handle or accent.
- **generate** passes `_reference-style/` as the fixed reference set and renders the *mascot*
  described here.

## To rebrand (anyone other than Eric Tech)
1. Edit *Identity* (your `@handle`, `default_accent`, `voice`).
2. Replace the images in `_reference-style/` with your own style deck.
3. Swap the logo PNGs in `character-references/` and update
   `skills/instagram-carousel-generate/references/tool-brand-colors.md`.

That's the whole rebrand — three edits, no code.
