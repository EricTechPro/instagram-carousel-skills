# Install

You don't clone anything or run a plugin command yourself. **Hand the repo URL to your coding
agent and let it install.** Pick the agent you use below, copy the block, and paste it in — the
agent clones the repo, copies both skills into your project, and wires up the assets.

The only difference between the two is how slides get *rendered*:

| Agent | Renders with |
|---|---|
| **Claude Code** | HiggsField **CLI** + GPT Image 2 |
| **Claude Cowork** | HiggsField **MCP** |

Pick one. Either way you get the full toolkit (both skills + assets + your editable `BRAND.md` and
`_reference-style/`).

---

## Claude Code

Renders slides with the **HiggsField CLI** (GPT Image 2). Paste this into Claude Code:

```
Install the Instagram Carousel skills into this project.
Repo: https://github.com/EricTechPro/instagram-carousel-skills
Read the repo's docs/install.md and follow it for the Claude Code (HiggsField CLI) path.
```

## Claude Cowork

Renders slides with the **HiggsField MCP**. Paste this into Cowork:

```
Install the Instagram Carousel skills into this workspace.
Repo: https://github.com/EricTechPro/instagram-carousel-skills
Read the repo's docs/install.md and follow it for the Claude Cowork (HiggsField MCP) path.
```

---

## After it installs

The agent drops two skills into `.claude/skills/`, shared assets into
`.claude/instagram-carousel/`, and two editable files — **`BRAND.md`** and **`_reference-style/`**
— at your project root. Re-running the installer never overwrites those two.

**HiggsField auth is a separate step** — you only need it to *generate* images, not to *plan*. The
generate skill checks it before spending any credits and walks you through it. Full setup (CLI
login, MCP connection, cost gating, failure modes) lives in
[`skills/instagram-carousel-generate/references/higgsfield-setup.md`](skills/instagram-carousel-generate/references/higgsfield-setup.md).
