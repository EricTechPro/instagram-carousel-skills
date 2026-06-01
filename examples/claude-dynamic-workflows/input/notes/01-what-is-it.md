# Q1: What are Dynamic Workflows, mechanically?

_Drawn from: video-1 (Mark Kashef), video-2 (Ray Amjad), video-3 (win4r),
Anthropic blog._

## The one-sentence answer

Claude Code writes a JavaScript orchestration script on the fly for your
prompt, and a **runtime** executes that script — spawning tens to hundreds
of sub-agents in parallel, passing results between them via code (not
through Claude's context window).

## What's actually new vs sub-agents/skills

Before Dynamic Workflows, a Claude Code session orchestrated sub-agents
*itself*: every sub-agent's output went back into the orchestrator's
context window, the orchestrator picked the next sub-agent, passed inputs
in, and so on. **Tax:** ~90–95% of each sub-agent's output got re-injected
into the next sub-agent's prompt; orchestrator context filled fast and
orchestration quality degraded (Video 2, 0:49–3:06).

Dynamic Workflows breaks the loop. Claude writes a JS file that defines
phases, schemas (structured handoffs), conditionals, and loops. The
runtime executes the JS; sub-agent results are stored in **script
variables**, not in Claude's context. Only the final result returns to the
session (Video 3, 4:30; Video 2, 6:12).

## Anatomy of a workflow file (per Video 2 and Video 3)

```
meta:    name, description, phases
schemas: structured-handoff types (e.g. issue { id, title, users_affected })
phase 1: agent("...", schema) → result stored in JS var
phase 2: pipeline(agents) — stream results from one stage to the next
phase 3: while(budget > 50k) { agent(...) }
return:  final synthesized answer
```

The runtime primitives Claude can use:
- `agent(prompt, schema)` — spawn one sub-agent
- `schema` — force structured output
- **parallel** — fan out N agents at once (cap 16 concurrent, 1,000 total)
- **pipeline** — streamed-stage parallel: stage-2 of task-N starts the
  moment stage-1 of task-N finishes, without waiting for task-N+1
- Loops/conditionals (plain JS)
- Budget guards (e.g., `while(budget_remaining > 50_000)`)

## Concurrency limits

- 16 sub-agents run concurrently at any instant
- 1,000 sub-agents max per run (hard cap)

Confirmed by trade press; **not** mentioned in any of the 3 videos.
One commenter on Mark Kashef's video hit the cap from below: "I just
tried it with 496 agents. Burned 13.3M tokens in 18 minutes."

## Why the official source is more reliable than the videos here

Videos describe the feature in terms of what they observed running it.
The [Anthropic blog](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)
states the design intent explicitly: workflows are a way to *scale beyond a
single context window* by moving plan state into code. That framing is the
load-bearing insight — the keyword tricks and budget syntax are tactical.
