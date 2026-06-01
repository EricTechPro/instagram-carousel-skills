# Sources — claude-dynamic-workflows

**Mode:** Videos (3 YouTube creators) + Web verification (official Anthropic + reputable secondary)
**Topic:** Claude Code Dynamic Workflows feature (announced 2026-05-28)
**Compiled:** 2026-05-29

---

## Primary — YouTube creator videos

Extracted to `main💥/research/claude-dynamic-workflows/`.

| # | Creator | Title | Views | URL | Local file |
|---|---|---|---|---|---|
| 1 | Mark Kashef (77.5K subs) | The Claude Update Everyone Missed (Dynamic Workflows) | 1,228 | https://youtu.be/-tLlZqrXpo8 | `video-1.md` |
| 2 | Ray Amjad (44.8K subs) | The New Claude Code Feature Going Viral Right Now | 1,492 | https://youtu.be/kJ8FTPykawU | `video-2.md` |
| 3 | AI超元域 / win4r (71K subs) | Opus 4.8 + Dynamic Workflows 自动生成 Harness… | 9,384 | https://youtu.be/4C7hYW5sx0o | `video-3.md` |

Each MD has full transcript, top comments (top 50 root + top 10 replies),
channel stats, and categorized links.

---

## Primary — Anthropic official

| Source | What it confirmed |
|---|---|
| [Introducing Dynamic Workflows in Claude Code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) | Official feature announcement + Bun case study |
| [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) | Opus 4.8 release notes (same day as Dynamic Workflows) |
| [What's new in Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) | Per-feature spec, benchmark deltas |
| [Common workflows — Claude Code Docs](https://code.claude.com/docs/en/common-workflows) | Activation paths + config |

---

## Secondary — trade press

Used for cross-verification of facts the official blog didn't restate in
plain terms (e.g., 1,000-agent cap, version requirement, plan defaults).

- [TechCrunch — Opus 4.8 with new 'dynamic workflow' tool](https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/)
- [MarkTechPost — workflows capped at 1,000 subagents](https://www.marktechpost.com/2026/05/28/anthropic-ships-claude-opus-4-8-alongside-dynamic-workflows-and-cheaper-fast-mode-with-workflows-capped-at-1000-subagents/)
- [Simon Willison — "modest but tangible improvement"](https://simonwillison.net/2026/May/28/claude-opus-4-8/)
- [TestingCatalog — Anthropic launches dynamic workflows](https://www.testingcatalog.com/anthropic-launches-dynamic-workflows-for-claude-code/)
- [Pasquale Pillitteri — research preview, up to 1,000 subagents](https://pasqualepillitteri.it/en/news/3663/claude-code-dynamic-workflows-anthropic-research-preview)
- [TechTimes — Scripts Replace Context Windows](https://www.techtimes.com/articles/317363/20260529/claude-code-dynamic-workflows-scripts-replace-context-windows-ultracode-automates-orchestration.htm)
- [Help Net Security — Mythos-class models prep](https://www.helpnetsecurity.com/2026/05/29/anthropic-claude-opus-4-8/)
- [9to5Mac — Opus 4.8 details](https://9to5mac.com/2026/05/28/anthropic-upgrades-claude-with-new-opus-4-8-model-heres-whats-new/)
- [Axios — Opus 4.8 + Mythos prep](https://www.axios.com/2026/05/28/anthropic-opus-release-mythos)
- [WaveSpeed — release date, pricing, benchmarks, builder notes](https://wavespeed.ai/blog/posts/opus-4-8/)

---

## What was missing from the videos but present in official sources

- **Bun port "not yet in production"** — Anthropic's own blog explicitly
  caveats this. Video 3 omits the caveat entirely; Video 1 doesn't mention
  Bun at all.
- **1,000 subagent hard cap** per run — none of the 3 videos state this.
  One commenter on Video 1 hit it: "I just tried it with 496 agents.
  Burned 13.3M tokens in 18 minutes and ran out of tokens."
- **Claude Code v2.1.154+** requirement — Video 1 says "absolute latest
  version," Video 3 doesn't specify; Video 2 only says you need it enabled
  in `/config`.
- **Plan defaults** (Max/Team/API on by default, Pro off-by-default,
  Enterprise admin-controlled) — none of the 3 videos break this down.
- **Still in research preview** — Videos 1 and 2 imply it's a stable
  feature; the official blog and trade press explicitly tag it "research
  preview."
