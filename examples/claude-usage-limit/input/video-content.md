# Video content — the 5 fixes (from _publish.md)

The shipped video: **"I Was Hitting Claude's Usage Limit Daily Until This."** Core thesis:
the problem isn't your usage — it's the context Claude Code burns *before you type your first prompt*.

## The hook number
- Claude Code burns **~19% of context** before the first user prompt (MCP + skills + CLAUDE.md load).
- MCP tool definitions alone = **11.3%** of context overhead.

## The 5 fixes (in order)

### Fix 01 — Refine MCP
- `ENABLE_TOOL_SEARCH=1` env var lazy-loads MCP tools → drops MCP overhead **11.3% → ~3%**.
- Migrate MCP servers to their **CLI equivalents** (Sentry, Vercel, Linear, JIRA) →
  saves **800–1,400 tokens per call** and **~3–5K per index**.

### Fix 02 — Refine Skills
- Audit installed skills; condense / remove ones you never call (Superpowers helps).
- Reclaims **1–3% of context per session**.

### Fix 03 — Refine CLAUDE.md
- Every session reads CLAUDE.md before you type. Slim it down (target < 200 lines),
  move specialist instructions into `.claude/skills/`.

### Fix 04 — Refine Settings
- Lower the auto-compact threshold; set `MAX_OUTPUT_LENGTH` to stop **silent bash retries**
  that quietly drain your 5-hour window.

### Fix 05 — Refine Permissions
- Permission **deny** rules keep `node_modules`, `dist`, and lockfiles out of Claude's reads.

## Monetization / CTA in the video
- Skool community (skool.com/erictech) for the prompts; bookzero.ai mention.
- For IG we convert this to a **comment-to-DM** funnel (keyword TOKENS) — stronger for reach.

## Mentioned tools (real URLs)
- Superpowers — github.com/obra/superpowers
- Sentry CLI / Vercel CLI / Linear CLI / JIRA CLI
