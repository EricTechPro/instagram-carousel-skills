# Claude Code Dynamic Workflows — synthesized

_Compiled 2026-05-29 from 3 YouTube creator videos + official Anthropic
sources; **updated 2026-05-30 with a 4th video (Nate Herk)** —
complexity-ladder framing, /goal-vs-workflow, and fresh cost data. See
[`sources.md`](./sources.md) for the source list and [`notes/`](./notes/)
for per-question deep-dives._

---

## TL;DR

- **What it is:** Claude writes a JavaScript orchestration script on the
  fly for your prompt; a runtime executes it, spawning **16 sub-agents in
  parallel up to a 1,000-agent hard cap** per run. Intermediate results
  stay in **script variables**, so the orchestrator's context window
  never fills up. Final result returns to the session.
- **Why it matters:** Sub-agents and skills both pollute Claude's context
  with every intermediate result; orchestration quality drops as the
  window fills. Workflows move plan state into code. This is *the*
  unlock for tasks that exceed one context window — large codebase
  audits, mass-document due diligence, multi-day refactors.
- **The hero case:** Jarred Sumner ported Bun's runtime from Zig to Rust
  in **11 days** — ~750K lines, 99.8% of the existing test suite
  passing — via 4 chained workflows. **Caveat:** Anthropic's own blog
  states the port is **not yet in production**. It's a scale proof, not
  a shipped product.
- **Status:** research preview. Live on Max/Team/API/Bedrock/Vertex/Foundry
  by default; **Pro plan = manual opt-in** via `/config`; Enterprise =
  admin-controlled. Requires Claude Code v2.1.154+.
- **Cost reality:** 51-agent runs burn 3M+ tokens in ~25 min. The
  `workflow+100K` budget hint is *soft* — one user set it and burned
  569K. Use only when one context window can't hold the task.

## Worked example — the activation flow that travels

```
# 1. Make sure your build is recent
$ claude --version    # ≥ 2.1.154

# 2. On Pro plan? Enable the feature
> /config
  ┌─ Dynamic Workflows: [false] → toggle to [true]

# 3. Type a prompt with the magic word
> workflow that audits every file under src/
  for missing authorization checks, has a second
  agent refute each finding, returns only confirmed
  issues with file and exact line.

  ↑ the word "workflow" goes rainbow-colored
  ↑ Claude writes a JS script and shows it for approval
  ↑ press y → runtime fans out 16 agents at a time

# 4. Watch progress (tmux-like layout)
> /workflows

# 5. Save the script for next time
  (in /workflows view) press S → saves JS to project/.claude/workflows/
```

## Key findings

### 1. The mechanical innovation is "plan-state in code, not context"

Sub-agents and skills are both Claude-mediated — every intermediate result
returns to Claude's context, where the next step is chosen by the model.
That's the orchestration tax (Video 2, 0:49). Workflows skip the model at
the joins: stage N's output is a JS variable that stage N+1 reads. The
runtime, not Claude, chooses the next step.

Concrete consequence: you can run a 51-agent workflow without the
orchestrator context window filling up at all. Final synthesis only.

📎 Detail: [`notes/01-what-is-it.md`](./notes/01-what-is-it.md)

### 2. Adversarial review (find-then-refute) is the load-bearing pattern

All 3 videos converge on the same shape:

```
parallel(
  pipeline(
    find(file_i),        # cheap model — Haiku finds candidates
    refute(finding_i),   # cheap model — adversarial check
  )
  for file_i in codebase
)
→ Opus synthesizes only the confirmed findings
```

Mark Kashef's framing: "micro devil's advocates running in the
background." Not "more agents = more better" — **paired agents** so
every claim has been challenged before reaching the user.

This pattern + Opus 4.8's ~4× reduction in unflagged code defects is why
the feature lands now, not 6 months ago.

📎 Detail: [`notes/03-use-cases.md`](./notes/03-use-cases.md)

### 3. The model bump (Opus 4.8) matters *because* of workflows

Anthropic's own positioning: Opus 4.8 alone is "a modest but tangible
improvement" (Simon Willison agrees). The interesting product story is
Dynamic Workflows. But the model bump is load-bearing for workflows
specifically:

- ~**4× fewer silently-unflagged code defects** — at 1,000 agents this
  compounds enormously
- **Mid-conversation `system` messages** — refuter agents can be
  sharpened mid-run without paying input-token cost
- **Fast mode: 2.5× speed, 3× cheaper** — Haiku scout stages get
  meaningfully cheaper, overnight optimization runs finish sooner

📎 Detail: [`notes/04-opus-48.md`](./notes/04-opus-48.md)

### 4. Token cost goes from "expensive" to "ruinous" fast — manage it

Real numbers:
- 11 agents, simple categorization: ~550K tokens, <5 min ✅ reasonable
- 41 agents, skill audit (Video 4): ~5M **input** tokens, all on Haiku —
  cheap-ish because input ≪ output, but still a heavy read
- 51 agents, deep document sweep: ~3.2M tokens, 23 min — pricey but
  justified if it replaces 8 hours of human work
- 496 agents (community attempt): 13.3M tokens, ran out of budget mid-run
- Whole-desktop crawl (Video 4): **half a $200/month plan in one ~30-min
  prompt** — workflows are input-token heavy (each agent re-reads its own
  context). A commenter hit 70% of their weekly limit on ultracode runs.

The `workflow+100K` syntax is a *signal*, not a contract — one Video 3
commenter blew through 5.7× their budget. Treat it as guidance for the
planner, not an enforced ceiling.

**Decision rule** (Mark Kashef): would I otherwise re-prompt and pass
context across 3+ runs? Yes → workflow. No → just ask Claude.

📎 Detail: [`notes/05-gotchas.md`](./notes/05-gotchas.md)

### 5. Three activation paths, one keyword, plus a built-in deep-research command

- **Keyword `workflow`** — turns rainbow in the input box → opt-in for
  that turn only
- **`/effort` → `ultracode`** — sticky mode, Claude auto-decides when to
  fan out
- **`/deep-research <topic>`** — native command that runs a multi-stage
  research workflow (decompose → parallel search → fetch → Opus
  synthesis). Video 3 demoed this on "Harness Engineering" — 5 stages,
  26 agents in stage 3, 75 in stage 4

📎 Detail: [`notes/02-activation.md`](./notes/02-activation.md)

### 6. Where workflows sit on the complexity ladder (Video 4)

Nate Herk's clearest contribution is a **decision ladder** for the
overlapping Claude Code primitives — pick the lowest rung that solves the
problem:

```
Just ask → Skill → Subagent → Agent team → /goal → Dynamic workflow
 (cheap)                                              (powerful + risky)
```

- **Skill = the *how*; workflow = the *how many*** (width/depth). Skills
  nest inside workflows — each workflow subagent can run your skills, MCP
  servers, and keys.
- **/goal vs workflow = depth vs width.** `/goal` loops one+ agents until
  `done == true` (can run hours); a workflow fans 50+ agents out
  horizontally, each runs **once**, results synthesize at the end. No loop.
- **Decision question:** "Does this break into many pieces that can run
  independently at the same time?" Yes → workflow. No → a single agent,
  skill, or `/goal`.
- **Honest caveat:** for automation / knowledge work (vs heavy coding),
  you may rarely need a workflow at all — knowing *what it does* beats
  using it daily.

`ultracode` (`/effort` → `ultracode`) is **extra-high reasoning +
workflows-on-by-default** — it bypasses most permission prompts and
orchestrates on nearly every turn. Most capable, most expensive; opt in
deliberately. Reliable manual trigger: "set me up a dynamic workflow to
do this" (the bare word `workflow` only rainbow-highlights, doesn't
guarantee invocation).

📎 Raw: [`../research/claude-dynamic-workflows/video-4.md`](../research/claude-dynamic-workflows/video-4.md)

### 7. There's a quiet sub-agent-permissions gap to validate before
shipping

User @DaveDDD (Video 1 comment) flagged that workflow-spawned sub-agents
don't honor the `allowed_tools` setting from your skill definitions.
Anthropic's blog doesn't address this. If you've used
`allowed_tools` as a guardrail to keep agents away from certain files or
shell commands, **test before trusting workflows on a sensitive codebase**
— the runtime may route around your restrictions.

📎 Detail: [`notes/05-gotchas.md`](./notes/05-gotchas.md)

## Open questions worth a follow-up pass

- **Tracing / observability.** `/workflows` shows live state but there's
  no export, no run history beyond the session, no integration with
  external tracers. High-stakes workflows currently rely on saved JS +
  final synthesis as their audit trail.
- **`allowed_tools` honoring.** Is the sub-agent-permission gap
  intentional (workflows trust the script) or an early-preview bug?
- **GA timing.** Naming already churned once
  (`ultrawork`/`autowork` → `workflow`). Worth checking back at Opus
  4.9 / Mythos-class launch before building tooling around the current
  surface.
- **Bun in production.** When does the Bun Rust port actually ship in a
  release build? That's the test of whether 750K lines + 99.8% tests
  translates to a maintainable codebase.

## What changed for *us* (yt-all-tools / EricTechOS)

Dynamic Workflows directly subsumes the kind of plumbing that
`Super Build`, `Super QA`, `Super Review`, and the `super-board` skill
provide. Several commenters across all 3 videos asked the same question
("do I still need superpowers / openclaw / hermes if I have workflows?").

**Short answer:** for *generic* parallel orchestration, the superpowers
stack will increasingly overlap with workflows. The superpowers stack
still wins where you want:
- Deterministic, hand-authored phase logic (your Build/QA/Review lanes
  are versioned scripts, not LLM-generated JS)
- GitHub-Project-driven curation surface (the board *is* the queue)
- Cross-machine portability via committed skill files
- Custom integrations (Telegram, Stripe, your own MCP servers)

What probably changes: skills that exist purely to spawn parallel sub-agent
batches inside one Claude session can shed orchestration code and let
Dynamic Workflows do the fan-out. Worth a separate audit pass.

## See also

- [`sources.md`](./sources.md) — primary + secondary sources, with notes
  on what the videos missed
- [`notes/01-what-is-it.md`](./notes/01-what-is-it.md) — mechanics
- [`notes/02-activation.md`](./notes/02-activation.md) — setup + paths
- [`notes/03-use-cases.md`](./notes/03-use-cases.md) — concrete cases
- [`notes/04-opus-48.md`](./notes/04-opus-48.md) — model deltas
- [`notes/05-gotchas.md`](./notes/05-gotchas.md) — limits + failure modes
- `../research/claude-dynamic-workflows/video-{1,2,3,4}.md` — raw
  extractions (transcripts, comments, metadata); video-4 = Nate Herk,
  complexity-ladder + cost reality
