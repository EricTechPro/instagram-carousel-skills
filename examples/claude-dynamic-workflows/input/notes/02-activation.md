# Q2: How do you turn it on? What's the minimum setup?

_Drawn from: video-1, video-2, video-3, Claude Code docs._

## Hard requirements

- **Claude Code v2.1.154 or later** (all platforms). Confirmed in trade
  press; videos say "absolute latest version."
- **Plan eligibility:**
  - Max, Team, API, Bedrock, Vertex, Foundry → **on by default**
  - **Pro plan** → off by default; enable in `/config` → Dynamic Workflows
  - **Enterprise** → off by default; admin-controlled via managed settings

## Three activation paths (videos agree)

### Path 1 — keyword `workflow` (per-turn opt-in)

Type the literal word `workflow` somewhere in your prompt. It turns
**rainbow-colored** in the input box → Dynamic Workflows is requested for
that turn. Example: *"Build a workflow that audits every file under SRC for
missing authorization checks…"* (Video 1, 1:23; Video 2, 4:00; Video 3,
1:30).

**Note:** the keyword was `ultrawork` / `autowork` in prior previews;
official launch renamed it to `workflow`.

### Path 2 — `/effort` → `ultracode`

Run `/effort` and pick `ultracode`. The whole input box becomes a rainbow
border, signaling Claude will use deep reasoning *and* auto-enable
workflows whenever the prompt looks workflow-shaped (Video 2, 4:08;
Video 3, 8:13).

### Path 3 — built-in `/deep-research` command

A native command that runs a multi-stage research workflow on whatever
topic you give it. Demoed in Video 3 (8:55–10:46): typed
`/deep-research Harness Engineering` → got 5 stages, 26 agents in stage 3,
75 agents in the verification stage.

## Budget control

Add `+<tokens>` after the keyword: `workflow+100k` caps that run at
roughly 100K tokens (Video 3, 2:21). Caveat — one commenter on Video 3
hit 569K despite setting `+100K`, so the cap is best-effort, not a hard
ceiling. Treat it as a soft budget signal.

## Inspecting a running workflow

`/workflows` opens a tmux-like multi-pane view (Video 3, 2:35). You see:
- Stage-by-stage progress
- Per-agent status (running / done / queued)
- Per-agent prompt + model + token spend + output
- Arrow keys to navigate

`X` kills the workflow; `S` saves the JS to a project file for reuse
(Video 3, 12:21).

## Resuming + appending stages

You can re-enter a workflow by run ID and add a 9th stage to an 8-stage
run — only the new stage runs (Video 2, 10:02). Saved workflow JS files
go into a per-project location (path shown briefly in Video 3) and
become reusable templates the team can commit + share.

## Minimum setup for a first-timer

1. Update Claude Code to ≥ v2.1.154
2. If on Pro: `/config` → toggle `Dynamic Workflows` to `true`
3. Type a prompt with the word `workflow` in it
4. Watch the rainbow color confirmation
5. Approve when Claude shows the generated JS script preview
