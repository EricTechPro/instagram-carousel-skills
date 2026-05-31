# Slide templates & `mimic_ui` panels

This file covers the **per-slide-type composition** and the optional **`mimic_ui`** panels
(rendering a source's distinctive UI — a GitHub repo header, a code editor — inside the card).

For exact coordinates/fonts/sizes of the standard text overlay, see `layout-templates.md`.
For the background-plate prompts, see `plate-templates.md`.

## Standard slide types (handled by `compose_slide.py`)
| type | what the composer draws |
|---|---|
| `cover` | big Archivo headline (key word in accent), subhead, badge, `swipe →`, handle |
| `item` | "0k/N" label, headline, "which means" subhead, ≤3 accent bullets, URL, logo, open-loop tail |
| `howto` | three step blocks (METHOD 0k / title / one-line desc) |
| `cta` | eyebrow, big headline with the comment word in accent, subhead, `save this post` |

These are fully implemented in `compose_slide.py`.

## `mimic_ui` panels — status: documented, agent-assisted (full auto = v0.2)
When a slide's `mimic_ui` is set, render a **clean, flat, schematic** mock of the source UI inside
the card (never a generated image — keep it crisp and legible). For v0.1 the agent composes these
with the same Pillow primitives in `compose_slide.py` (it is straightforward `ImageDraw` work);
a built-in `--mimic` mode is planned for v0.2. Recipes:

### `github-repo-header`
- Dark bar `#0D1117`, height ~64px across the card width. Left: real GitHub logo PNG + `owner / repo`
  in JetBrains Mono white. Right: a star pill `★ N` (N from the research).
- Below: a light row with the repo description (Space Grotesk) and 2–3 topic chips filled in `ACCENT`.

### `code-editor`
- Dark panel `#1E1E1E`, three window dots (red/amber/green), ≤6 lines of monospace pseudo-code.
  Use simple syntax tints (keyword in accent, string muted). Suggest code; don't reproduce a real file.

### `dashboard` / `metric`
- White inner card; one big Archivo number in `ACCENT` + a JetBrains Mono label under it.
  For "N stars", "Nx faster", "used by N", etc.

## Rule
Keep `mimic_ui` panels **schematic** — they communicate "this is a GitHub repo / an editor / a
metric" at a glance. Don't chase pixel-perfect reproduction; legibility beats fidelity on a phone.
If a slide doesn't set `mimic_ui` (or sets `none`), the composer just renders the standard type.
