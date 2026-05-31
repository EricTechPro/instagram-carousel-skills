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

## From zero (clean machine, nothing pre-installed)

If you're starting in a fresh project that has **no Superpowers and no HiggsField**, this is the
whole list:

1. **Get the skills** (pick one):
   - Plugin: `/plugin marketplace add EricTechPro/instagram-carousel-skills` then
     `/plugin install instagram-carousel@instagram-carousel-skills`
   - Or clone + script:
     `git clone https://github.com/EricTechPro/instagram-carousel-skills && cd instagram-carousel-skills && ./install.sh /path/to/your/project`
2. **Python + Pillow** (for cropping/compositing): `pip install -r requirements.txt`
   (or `pip install Pillow`).
3. **HiggsField** (only needed to *generate* images, not to *plan*): either
   `npm install -g @higgsfield/cli && higgsfield auth login`, **or** connect the HiggsField MCP in
   your host (Clockwork/cowork). Verify the CLI with `higgsfield account status`.
4. Optional: `gh` and/or a web-search tool, for source research in the plan step.

You do **not** need Superpowers or any sibling project. That's it — then say
"plan an instagram carousel for &lt;topic&gt;".

## Install

### Claude Code (plugin)

```bash
/plugin marketplace add EricTechPro/instagram-carousel-skills
/plugin install instagram-carousel@instagram-carousel-skills
```

### Any project (clone + script)

```bash
git clone https://github.com/EricTechPro/instagram-carousel-skills
cd instagram-carousel-skills
./install.sh /path/to/your/project     # or: ./install.sh --global
export IG_CAROUSEL_ASSETS="$HOME/.claude/instagram-carousel"   # if you used --global
```

### Clockwork / cowork

Clockwork and cowork are Claude Code hosts, so the **plugin marketplace flow above works there
too** — run the same two `/plugin` commands. Then connect HiggsField at the host level (see
below). *(Any cowork-specific "add skill repo" UI beyond the standard plugin flow is not verified
here — use the plugin marketplace path, which is supported everywhere.)*

## HiggsField setup (required for `generate`)

The generate skill renders slides with HiggsField GPT Image 2. Use **either**:

- **CLI:** `npm install -g @higgsfield/cli` then `higgsfield auth login`
  (verify with `higgsfield account status`).
- **MCP (Clockwork/cowork):** connect the **HiggsField MCP** in your host's connector settings.

The skill auto-detects which is available and checks it **before** spending any credits.
Full notes: [`skills/instagram-carousel-generate/references/higgsfield-setup.md`](skills/instagram-carousel-generate/references/higgsfield-setup.md).

## How it works (60 seconds)

1. **Plan** asks at most four questions (audience+pain, payoff+proof, sequence, CTA goal),
   researches any links/repos you give it, and writes save-worthy copy using embedded carousel
   copywriting frameworks. It emits `carousel-spec.md` and shows you a skimmable ASCII layout.
2. You approve the copy (cheap — no images yet).
3. **Generate** renders the cover first so you can lock the look, then renders the rest of the
   deck against a fixed reference set + pinned seed so every slide shares one world, character,
   and type. Output is cropped to exactly 1080×1350.

## Requirements

- A Claude Code host (CLI, app, Clockwork, cowork…).
- HiggsField — CLI **or** MCP (above).
- Python 3 + Pillow (`pip install -r requirements.txt`) — used to crop slides and build a
  contact sheet.
- Optional: `gh` and/or a web search/firecrawl tool for source research.

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

## Credits

Copywriting frameworks distilled (and attributed in `copy-frameworks.md`) from
`marcolang/marketing-skills@instagram-carousel` and the marketing skill set. Skill-system
patterns inspired by [Superpowers](https://github.com/obra/superpowers).

## License

MIT — see [LICENSE](LICENSE).
