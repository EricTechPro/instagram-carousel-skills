# Instagram Carousel Skills

Turn any Instagram post or pile of sources into a finished, on-brand Instagram carousel — without
leaving your agent. Use it right inside **Claude Code** or **Claude Cowork**: two skills combine,
one to **write the plan** and one to **generate** the slides.

```text
  ── 1 · PLAN ─ writes the copy ──                          ── 2 · GENERATE ─ renders the slides ──

  a folder of IG posts,        ┌──────────┐                 ┌──────────┐
  links, research files,  ───▶ │   plan   │ ───▶  spec  ───▶ │ generate │ ───▶  slide-01.png … slide-08.png
  or just a topic              │  skill   │      (.md)        │  skill   │       1080×1350, one consistent world
  "plan a carousel for X"      └──────────┘   you approve     └──────────┘       "generate the carousel"
                                              & can edit it
```

The **plan** skill researches your topic/sources and writes the per-slide copy, caption, hashtags,
and DM-trigger into a reviewable `carousel-spec.md`. You approve it (cheap — no images yet). The
**generate** skill renders that spec into 1080×1350 slides via HiggsField, one consistent set.

## Prerequisites

| Need | Why |
|---|---|
| **Claude Code** *or* **Claude Cowork** | the host that runs the two skills |
| **Python 3.9+** with `pip` | crops + composes slides (Pillow) and builds the contact sheet |
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

Two editable files land at your project root on install and are **never overwritten** on re-install:

1. **Set your style.** Browse Instagram / Pinterest (or any platform) for carousels whose look you
   want. Download a handful of reference posts and drop them into **`_reference-style/`** — this
   few-shot deck is what defines the whole generated world (sky, cards, mascot, palette). Swap these
   images and every future carousel restyles, no code changes.
2. **Edit `BRAND.md`.** Fill in your handle, accent color, voice, and mascot. Both skills read this
   — nothing brand-specific is hardcoded.

## Step 3 — Plan a carousel

Pick a topic and point the skill at whatever you've got — pasted links, GitHub repos, an article, or
a **file path to your own research notes** (Obsidian vault, a wiki, a folder of clippings). Trigger
the plan skill:

```
plan an instagram carousel for the top 5 GitHub repos every dev should clone
```

It asks ≤4 questions, researches your sources, and writes `carousel-spec.md` — the copy plus a
skimmable ASCII layout. Edit any field directly in that file; once you're happy, it's locked.

## Step 4 — Generate the slides

Approve the spec, then trigger the generate skill:

```
generate the carousel
```

It shows a cost estimate first, locks the cover to fix the look, then renders the rest against a
fixed reference set + pinned seed so every slide shares one world. Output is cropped to 1080×1350
plus a contact sheet. Single-slide text fixes re-compose for free; only background regens spend.

## How it works (under the hood)

- **plan** never spends image credits — it only researches and writes copy into the spec.
- **generate** uses a **hybrid pipeline**: HiggsField GPT Image 2 makes the text-free background
  (the world + mascot + a blank card); Pillow overlays headlines, bullets, URLs, and the real logo
  PNGs — so all text and brand marks are pixel-accurate and editable without re-spending credits.
- Consistency comes from passing the **same reference set + same pinned seed** to every slide, never
  chaining slide N−1 (which causes drift).

## License

MIT — see [LICENSE](LICENSE).
