# Instagram Carousel Skills

Turn a topic + a few sources into a finished, on-brand Instagram carousel — without leaving
your coding agent. Two skills that compose: **plan** writes the copy, **generate** renders the
slides.

```text
"plan an instagram carousel for the top 5 GitHub repos every dev should clone"
        │
        ▼   instagram-carousel-plan   (asks ≤4 questions, researches, writes copy)
   carousel-spec.md  +  an ASCII layout you can skim
        │
        ▼   instagram-carousel-generate   (HiggsField GPT Image 2)
   slide-01.png … slide-08.png   (1080×1350, one consistent world)
```

You do **not** need Superpowers or any sibling project.

## Install

Pick one. All three drop the two skills into `.claude/skills/` and the shared assets (fonts,
style references, logos) into `.claude/instagram-carousel/`, which the generate skill finds
automatically.

**A — Ask your agent (easiest).** In any project, tell Claude (or any coding agent):

> *"Install the skills from https://github.com/EricTechPro/instagram-carousel-skills"*

It clones the repo and runs the installer. (It follows [INSTALL.md](INSTALL.md).)

**B — Plugin (Claude Code, Clockwork, cowork).**

```bash
/plugin marketplace add EricTechPro/instagram-carousel-skills
/plugin install instagram-carousel@instagram-carousel-skills
```

**C — Clone + script, or release zip.**

```bash
git clone https://github.com/EricTechPro/instagram-carousel-skills
cd instagram-carousel-skills
./install.sh /path/to/your/project     # or: ./install.sh --global  (~/.claude)
```

Prefer no clone? Download the latest [release zip](../../releases/latest) and
`unzip instagram-carousel-skills-v*.zip -d your-project/.claude/`.

Then install Python + Pillow (used to crop/compose slides and build the contact sheet):

```bash
pip install -r requirements.txt    # or: pip install Pillow
```

That's it for planning. To **generate** images you also need HiggsField (below).

> Assets resolve automatically (`.claude/instagram-carousel/`). Only set
> `IG_CAROUSEL_ASSETS` if you keep the assets somewhere non-standard.

## HiggsField setup (only needed to generate)

The generate skill renders backgrounds with HiggsField GPT Image 2. Use **either**:

- **CLI:** `npm install -g @higgsfield/cli` then `higgsfield auth login`
  (verify with `higgsfield account status`).
- **MCP (Clockwork/cowork):** connect the **HiggsField MCP** in your host's connector settings.

The skill auto-detects which is available and checks it **before** spending any credits.
Full notes: [`references/higgsfield-setup.md`](skills/instagram-carousel-generate/references/higgsfield-setup.md).

## How it works (60 seconds)

1. **Plan** asks at most four questions (audience+pain, payoff+proof, sequence, CTA goal),
   researches any links/repos you give it, and writes save-worthy copy using embedded carousel
   copywriting frameworks. It emits `carousel-spec.md` and shows you a skimmable ASCII layout.
2. You approve the copy (cheap — no images yet) and can edit any field directly in the spec.
3. **Generate** renders the cover first so you can lock the look, then renders the rest of the
   deck against a fixed reference set + pinned seed so every slide shares one world, character,
   and type. Output is cropped to exactly 1080×1350, plus a contact sheet.

## The two skills

| Skill | Does | Trigger |
|---|---|---|
| `instagram-carousel-plan` | Research + copywriting → `carousel-spec.md` + ASCII layout | "plan an instagram carousel for …" |
| `instagram-carousel-generate` | Spec → fully-rendered 1080×1350 slides | "generate the carousel" |

## What this is NOT

- Not an auto-poster/scheduler — you publish to Instagram yourself.
- Not a Reels/video tool — static carousels only.
- Not a general image generator — it is opinionated to one branded visual system (editable in
  `skills/instagram-carousel-generate/references/visual-system.md`).

## Requirements

- A Claude Code host (CLI, app, Clockwork, cowork…).
- Python 3 + Pillow (`pip install -r requirements.txt`).
- HiggsField (CLI or MCP) — only to *generate*, not to *plan*.
- Optional: `gh` and/or a web-search tool for source research in the plan step.

## Credits

Copywriting frameworks distilled (and attributed in `copy-frameworks.md`) from
`marcolang/marketing-skills@instagram-carousel` and the marketing skill set. Skill-system
patterns inspired by [Superpowers](https://github.com/obra/superpowers).

## License

MIT — see [LICENSE](LICENSE).
