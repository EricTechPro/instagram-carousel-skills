# Q5: Gotchas, limits, and failure modes

## Token economics — when it's *not* worth it

### Real numbers from the videos

- **Mark Kashef** — 51-agent "needles in a haystack" data-room sweep:
  3.2M tokens, 23 min. The simpler 5-class issue categorization in
  Video 3: 11 agents, ~50K tokens each (~550K total), <5 min.
- **Commenter @allanrmartins** (Video 1): "I just tried it with 496
  agents. Burned 13.3M tokens in 18 minutes and ran out of tokens."
- **Commenter @terry2567** (Video 3): set `workflow+100K`, the run
  burned 569K. **Budget caps are soft, not hard.**

### Pattern: workflows beat agent-teams *only* when the task exceeds
one context window

Mark Kashef's argument (Video 1, 5:30):
- One agent team ≈ 250–300K tokens per task
- Running 3–4 agent teams sequentially = 1–1.5M tokens
- One workflow doing the same work via parallel + adversarial review =
  comparable spend with much lower wall-clock time

If you'd otherwise spin up 1 agent team and be done, workflows are an
*overspend*. The threshold is: would I need to re-prompt and pass
context across 3+ runs? Yes → workflow. No → just ask Claude.

## Hard limits

| Limit | Value | Source |
|---|---|---|
| Max concurrent sub-agents | **16** | Trade press, Video 3 |
| Max sub-agents per run | **1,000** | Trade press; videos didn't state |
| Required Claude Code version | **v2.1.154+** | Trade press |
| Token-budget enforcement | **Soft** (not a hard cap) | Video 3 commenter empirical |

## Plan-tier gotchas

- **Pro plan users** — off by default. Open `/config` → toggle
  Dynamic Workflows → true. Several Video 3 commenters were confused
  why the option wasn't visible — most likely an old Claude Code
  binary or a Pro plan without the toggle.
- **Enterprise** — off by default, requires admin enablement via
  managed settings. Will not appear in `/config` for end users.

## Sub-agent permission gap (called out by user @DaveDDD on Video 1)

> "The agents in a workflow don't follow the `allowed_tools` setting
> for agents — so this is just a more expensive way to allow
> vibecoders to produce more slop."

**Implication:** custom skill-defined sub-agent permissions don't carry
into workflow-spawned sub-agents. If you rely on `allowed_tools` to
prevent agents from touching certain files or running certain commands,
Dynamic Workflows can route around that. Validate before letting a
workflow run on a sensitive codebase.

(Anthropic blog does not address this. Worth surfacing as an open
question — possibly intentional design, possibly an early-preview gap.)

## Trust & validation problem (user @clarkmakes on Video 1)

> "I had Claude read a half-dozen small bank-statement PDFs… solid
> prompt, yet it missed entire pages of transactions."

Workflows compound this risk: per-agent error rates multiply across
1,000 agents. Mitigations the videos suggest:
- Always pair finders with adversarial refuters (devil's-advocate
  agents)
- Use schemas to force structured handoff — prevents free-form drift
- Validate sample outputs by hand before trusting an entire
  large-scale run

## Bun caveat

The Bun port — Anthropic's headline case study — is **not yet in
production**, per Anthropic's own blog. 99.8% test pass on the existing
suite ≠ a battle-tested runtime. Don't cite this as "Claude rewrote
Bun" in customer-facing copy; cite it as "750K-line proof of scale."

## Research preview status

The feature is still in **research preview** per the official launch
post and TechCrunch. Expect API changes, naming changes (already saw
`ultrawork` → `workflow`), and possible plan-tier shifts before GA.

## Observability question (raised by @jarad4621 on Video 1)

> "How are the workflows actually designed upfront? Do you have good
> tracing / tracking / observability?"

Today: `/workflows` is the only built-in observability surface
(tmux-style stage view, per-agent prompt + tokens + output). No
external tracing export, no run history beyond the session. For
high-stakes workflows, log saved JS + the final synthesis to disk
and treat that as your audit trail.

## Skill vs workflow confusion (multiple commenters across all 3 videos)

> "Can I just use a skill instead?"

Answer (consolidated): **No, they're orthogonal.** Skills are
prompt-following instructions Claude reads into its own context.
Workflows are scripts Claude *generates* and the runtime executes —
intermediate state lives in JS variables, not Claude's context. The
correct frame is:

- **Sub-agents** = Claude-spawned workers, results pollute orchestrator
  context
- **Skills** = prompt-bound instructions, results pollute Claude's
  context
- **Dynamic Workflows** = JS runtime, results stay in script variables;
  Claude only sees the final answer

You can use all three on the same task. Workflows shine when the task
needs more steps than one context window can hold.
