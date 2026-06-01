# Q3: What are the concrete use cases shown across the 3 videos?

## The hero case — Bun port (Anthropic blog, referenced by Video 3)

Jarred Sumner (Oven, makers of Bun) used Dynamic Workflows to migrate
Bun's JavaScript runtime **from Zig to Rust**:

- ~**750,000 lines** of Rust generated
- **99.8%** of the existing test suite still passing
- **11 days** first commit → merge
- **4 coordinated workflows** in sequence:
  1. **Lifetime mapping** — one workflow mapped the right Rust lifetime
     for every struct field in the Zig codebase
  2. **Parallel porting** — hundreds of agents writing each `.rs` file
     as a behavior-identical port of its `.zig` counterpart, with **two
     reviewers per file**
  3. **Build/test fix loop** — drove the build + test suite until clean
  4. **Optimization pass** — overnight workflow removing unnecessary
     copies, opening one PR per optimization

**Crucial caveat the videos miss:** Anthropic's own blog says this port
is **not yet in production**. It's a credible proof of scale, not a
shipped product. Treat the "11 days, 750K lines" line as a benchmark,
not a guarantee.

## Use cases demoed in the 3 videos

### Code-side (video-2, video-3)

| Use case | Workflow shape |
|---|---|
| Multi-round implement → review → fix loop with early-exit | implement → 3× (review // fix) with break-on-pass |
| Large-codebase security audit | Per-file find-bug agents (Haiku) → cross-validator agents (Haiku) → Opus synthesis (Video 3, 10:46) |
| Dead-code sweep | While-loop: find dead code → remove → end on 2 empty rounds OR after 8 iterations |
| Triage Sentry issues by user impact | Pull issues (MCP) → JS filter → pipeline(fix, verify) per issue |
| GitHub issue categorization (Bun-style) | 10 Haiku scouts + 1 Opus summarizer — 11 agents, ~50K tokens each (Video 3, 3:46) |
| PRD-driven red/green/refactor | Per task: write failing test → run → implement → green test → refactor → next task |
| Deep research on a topic | Decompose → parallel search → parallel fetch → Opus citation-synthesis |

### Business / industry-side (video-1, Mark Kashef speedrun)

| Industry | Workflow | Token budget impression |
|---|---|---|
| Law / M&A | Due diligence on 70+ contracts in a data room, flag deal-killers | His 51-agent "needles in a haystack" run: ~3.2M tokens, 23 min |
| Finance | Audit every CSV / QuickBooks row for duplicates, outliers, miscategorized — verify each flag against source rows | Not stated |
| Healthcare | Check every patient chart against guidelines.md, flag documentation gaps — *must run on Bedrock for HIPAA* | Not stated |
| Insurance | Triage claims into `auto-approve/` and `needs-human/` folders + priority queue | Not stated |
| Real estate | Abstract a lease portfolio into one table (rent, renewal, term, key dates) overnight | Not stated |
| Recruiting | Score every resume against a rubric.md, second-pass bias check, ranked shortlist with rationale | Not stated |
| Marketing | Audit 100+ competitor sites for messaging/offers/SEO gaps, cross-check, return one sheet | "An agent team would struggle past 1,000 — workflow shines" |
| Compliance | Check every policy against a standard, flag gaps, refute false positives, prioritized remediation list | Not stated |

## When *not* to use it (consensus from all 3 videos)

- Small, single-shot tasks Claude can do in one session
- Generic chat / Q&A
- Tasks where you can't define a clean beginning/middle/end (workflows
  are designed to run autonomously to completion)
- "Wide but shallow" tasks where one big context window would actually
  win (workflows trade context for tokens — only pays off when the task
  exceeds what one window can hold)

## The mental model that travels (Mark Kashef)

> Spin up **micro devil's advocates** running in the background to make
> sure that by the time you get a confirmed insight, it is as
> meritorious as possible and ideally as data-backed as possible.

Two agents per finding — one to find, one to refute — is the
load-bearing pattern, not just "more agents = more better."
