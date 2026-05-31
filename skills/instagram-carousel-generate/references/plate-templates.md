# Background-plate prompts (GPT Image 2 — NO text)

The model renders the **world only**: sky, clouds, grass, Clawd posed, and a **blank cream card**
with an empty zone where Pillow will draw the copy. It never writes text or draws brand logos
(those are composited — see `layout-templates.md`). This keeps prompts short and text accurate.

## Locked preamble (prepend to every plate prompt)
```
3D voxel render, bright blue sky with soft white clouds, green grass strip along the bottom,
cheerful sunny scene, soft shadows, shallow depth of field. A blocky Minecraft-style orange
mascot character ("Clawd"). Clean blank cream/off-white paper card with a smooth empty surface
and NO text, NO lettering, NO logos. Portrait composition. Match the style of the reference images.
```

## References passed on EVERY generation (fixed set — prevents drift)
- `assets/style-reference/ref-00-cover.jpg` … (the approved few-shot deck) — style lock.
- The **once-approved cover** background (after BFS) — world lock.
- A canonical Clawd reference (crop one from the style-reference deck if no standalone file).
Pass them as repeated `--image` flags. **Pin one seed** for the whole deck
(`higgsfield model get gpt_image_2 --json` to find the param) — same seed every slide.

## Per-type plate additions
- **cover:** "crowned mascot standing on a pile of small code blocks, arms raised, big empty
  area at the top for a headline."
- **item:** "mascot beside a wooden sign on a post (or holding a pinned note); large blank cream
  card filling the upper two-thirds, empty."
- **howto:** "three small wooden signposts in a row on the grass, each with a small blank card;
  mascot(s) beside them."
- **cta:** "mascot holding a large blank speech-bubble sign overhead, empty surface."

## mimic_ui slides
When a slide has `mimic_ui` (e.g. `github-repo-header`), the plate still generates only the
world + a **larger blank card/panel**. The UI mock (e.g. a dark top nav bar, repo name row, star
pill) is drawn by `compose_slide.py` as a flat vector-style panel inside the card — not generated.
This guarantees the UI is legible and correct. See `slide-templates.md` for the panel recipes.

## Rules
- Keep the full prompt **under ~200 tokens** — the model distorts long prompts.
- Phrase the empty zone **positively** ("clean blank cream card, smooth surface") — gpt_image_2 has
  no negative_prompt.
- `aspect_ratio 3:4`, `resolution 2k`, `quality high`, `batch_size 2`.
- If a generation returns a non-success terminal status (nsfw / ip_detected / failed), stop and
  report — never write a zero-byte file.
