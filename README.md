# Instagram Carousel Skills

Turn any Instagram post or pile of sources into a finished, on-brand Instagram carousel — without
leaving your agent. Use it right inside **Claude Code** or **Claude Cowork**: two skills combine,
one to **write the plan** and one to **generate** the slides.

```text
  ── 1 · PLAN ─ writes the copy ──                          ── 2 · GENERATE ─ renders the slides ──

  a folder of IG posts,        ┌──────────┐                 ┌──────────┐
  links, research files,  ───▶ │   plan   │ ───▶  spec  ───▶ │ generate │ ───▶  slide-01.png … slide-08.png
  or just a topic              │  skill   │      (.md)        │  skill   │       full 3:4 portrait, one consistent world
  "plan a carousel for X"      └──────────┘   you approve     └──────────┘       "generate the carousel"
                                              & can edit it
```

The **plan** skill researches your topic/sources and writes the per-slide copy, caption, hashtags,
and DM-trigger into a reviewable `carousel-spec.md`. You approve it (cheap — no images yet). The
**generate** skill renders that spec into full 3:4 portrait slides via HiggsField GPT Image 2 — which
letters every slide's text itself — as one consistent set.

## Prerequisites

| Need | Why |
|---|---|
| **Claude Code** *or* **Claude Cowork** | the host that runs the two skills |
| **Python 3.9+** with `pip` | resizes the rendered plates (Pillow) and builds the contact sheet |
| **HiggsField** — CLI *or* MCP | renders backgrounds — only needed to **generate**, not to **plan** |
| *(optional)* `gh` / a web-search tool | source research during planning |

`pip install -r requirements.txt` (Pillow) is run for you by the installer. HiggsField auth is a
separate step the generate skill walks you through before any credits are spent — see
[`higgsfield-setup.md`](skills/instagram-carousel-generate/references/higgsfield-setup.md).

## Step 1 — Install

You don't clone anything or run a plugin command. Hand the repo URL to your agent and it installs
for itself. Pick your host and copy the block — full details in **[INSTALL.md](INSTALL.md)**.

- **Claude Code** (renders with the HiggsField **CLI** + GPT Image 2):

  ```
  Install the Instagram Carousel skills into this project.
  Repo: https://github.com/EricTechPro/instagram-carousel-skills
  Read the repo's docs/install.md and follow it for the Claude Code (HiggsField CLI) path.
  ```

- **Claude Cowork** (renders with the HiggsField **MCP**):

  ```
  Install the Instagram Carousel skills into this workspace.
  Repo: https://github.com/EricTechPro/instagram-carousel-skills
  Read the repo's docs/install.md and follow it for the Claude Cowork (HiggsField MCP) path.
  ```

## Step 2 — Make it yours

Two things land at your project root on install — **never overwritten** on re-install.

**`_reference-style/`** — defines the look
- Browse Instagram / Pinterest for carousels you like
- Download a few posts → drop them in this folder
- Sets the whole world: sky, cards, mascot, palette
- Swap the images → every future carousel restyles

**`BRAND.md`** — defines the brand
- Your `@handle` + accent color
- Voice + mascot
- Both skills read it; nothing is hardcoded

## Step 3 — Plan a carousel — `/instagram-carousel-plan`

Run the slash command with the sources you have — paste links, or point it at a folder of research
notes (reference the path in square brackets):

```
/instagram-carousel-plan from these links: <url1> <url2> <url3>
```
```
/instagram-carousel-plan plan a carousel from my research in [path/to/research-folder]
```

It asks ≤4 questions, researches your sources, and writes `carousel-spec.md` (the copy + a skimmable
ASCII layout). Edit any field directly in that file; once you're happy, it's locked. See a real
run in [`examples/claude-dynamic-workflows/`](examples/claude-dynamic-workflows) — input → spec → output.

## Step 4 — Generate the slides — `/instagram-carousel-generate`

Approve the spec, then run the slash command — bare to use the latest spec, or with its file path:

```
/instagram-carousel-generate
```
```
/instagram-carousel-generate instagram-carousel/<slug>/carousel-spec.md
```

It shows a cost estimate first, locks the cover (cheap — one slide), then renders the rest as full
3:4 portrait slides + a contact sheet. GPT Image 2 letters every slide's text *into* the image, so a
copy edit means re-rolling that slide (a small credit spend) — there's no free text layer. That's why
the cover is locked first and the `@handle` is confirmed before the full batch.

## Examples

Two complete runs ship in [`examples/`](examples), each laid out the same way — **input → spec → output**:

- **[`claude-dynamic-workflows/`](examples/claude-dynamic-workflows)** — the default Eric Tech look (voxel "Clawd", blue accent).
  - [`input/`](examples/claude-dynamic-workflows/input) — the research wiki the copy was built from (one `.md` per source)
  - [`spec/carousel-spec.md`](examples/claude-dynamic-workflows/spec/carousel-spec.md) — the approved spec: slides + caption + hashtags + DM-trigger
  - [`output/`](examples/claude-dynamic-workflows/output) — the rendered `slide-01.png … slide-NN.png` + `_contact-sheet.png`
- **[`hermes-agent-use-cases/`](examples/hermes-agent-use-cases)** — a totally different brand from the *same* skills: vintage shoujo-manga, monochrome B&W, `@erictechpro`. Proof nothing is hardcoded.
  - [`input/`](examples/hermes-agent-use-cases/input) — the research wiki (one `.md` per source)
  - [`spec/carousel-spec.md`](examples/hermes-agent-use-cases/spec/carousel-spec.md) — the approved spec
  - [`output/`](examples/hermes-agent-use-cases/output) — the rendered slides + `_contact-sheet.png`
  - [`style-ref/`](examples/hermes-agent-use-cases/style-ref) — the per-brand reference deck (pointed at via `IG_CAROUSEL_STYLE`) that restyles the whole carousel **without touching** `_reference-style/`

## Under the hood

- **Skills:** plan, then generate
- **Image model:** HiggsField GPT Image 2 — letters every slide's text itself (no Pillow text overlay)
- **Render path:** Claude Code → CLI; Cowork → MCP
- **Style:** the images in `_reference-style/` are passed as the reference set on every render — swap them to restyle
- **Pillow:** resizes the returned plate to 1080-wide + builds the contact sheet
- **Dependencies:** Python 3.9+, Pillow
- **Planning:** zero image credits spent

## License

MIT — see [LICENSE](LICENSE).
