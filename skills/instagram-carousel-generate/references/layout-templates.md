# Pillow layout templates (the text/logo overlay)

`compose_slide.py` draws these onto the cropped 1080×1350 background. Coordinates are in pixels;
origin top-left. All text stays ≥80px from edges and out of the bottom 420px (except chrome).
Fonts from `assets/fonts/`. Colors from `visual-system.md`; `ACCENT` = the slide's `accent_hex`.

## Shared chrome (all slides)
- **Handle** `@…`: x=72, y=1250, JetBrains Mono 26px, color `#475569`.
- **Badge** (pill): top-center, y≈70. Cream fill `#F4EEE2`, 1px border `#E2E8F0`, JetBrains Mono
  24px UPPERCASE 0.12em, text `#0F172A`. Pad 18×10, rounded 24.
- Keep everything inside x:[80, 1000], y:[80, 930] for load-bearing copy.

## cover
- **Headline:** Archivo Black, start ~120px size, auto-shrink to fit width 936 / max 3 lines,
  tracking −0.04em, color `#0F172A` with the key number/word in `ACCENT`. Top block y≈150.
- **Subhead:** Space Grotesk 40px, `#475569`, below headline.
- **`swipe →`:** bottom-right x≈900 y≈1250, Space Grotesk Italic 30px, `ACCENT`.
- Logo (featured): small, top-right corner, ~96px, 80px margin.

## item
- **Card region:** the cream card area from the plate, roughly x:[90,990], y:[150,900].
- **Label** "0k/N" or "REPO 0k": JetBrains Mono 26px UPPERCASE, `#475569`, top of card.
- **Headline:** Archivo Bold ~72px, `#0F172A`, ≤2 lines, tracking −0.03em.
- **Subhead** ("which means…"): Space Grotesk 36px, `ACCENT`, italic optional.
- **Bullets:** up to 3, Space Grotesk 34px `#0F172A`, each with a small `ACCENT` square marker.
  Line spacing 1.4.
- **URL:** JetBrains Mono 24px, `#475569`, near the bottom of the card.
- **Logo:** the featured tool PNG, ~120px, placed beside the character or bottom-right of the card.
- **open_loop_tail:** Space Grotesk Italic 28px, `#475569`, just under the card.

## howto
- Three mini-cards (from the plate signposts). For each: JetBrains Mono "METHOD 0k" 22px label,
  Archivo Bold 40px title, Space Grotesk 28px one-line description. Centered per signpost.

## cta
- **Eyebrow:** "WANT THE LINKS?" JetBrains Mono 26px UPPERCASE `#475569`.
- **Headline:** Archivo Black ~96px, the comment word in `ACCENT` ("Comment **REPOS**").
- **Subhead:** Space Grotesk 38px `#0F172A` ("and I'll DM you all 5").
- **`save this post`:** bottom-right, Space Grotesk Italic 30px `ACCENT`.

## mimic_ui panel recipes (flat vector, drawn — not generated)
Render inside the card as a clean UI mock so it's always legible:
- **github-repo-header:** dark bar `#0D1117` height 64 with `JetBrains Mono` white `owner / repo`
  on the left and a star pill (`★ N`) on the right; below it a light row with the repo description
  and topic chips in `ACCENT`. Paste the real GitHub logo PNG at the bar's left.
- **code-editor:** dark panel `#1E1E1E`, 3 window dots, a few lines of monospace pseudo-code with
  simple syntax-color accents. Keep ≤6 lines.
- **dashboard / metric:** white card, a big Archivo number in `ACCENT` + a JetBrains Mono label.
Keep panels schematic — suggest the UI, don't reproduce it pixel-for-pixel.

## Auto-fit rules
- Always shrink-to-fit headlines before wrapping to a 3rd line. If still overflowing, the copy
  violated the density caps — surface it rather than rendering unreadable text.
- Assert every text field from the spec was drawn; record the bounding boxes for the safe-zone check.
