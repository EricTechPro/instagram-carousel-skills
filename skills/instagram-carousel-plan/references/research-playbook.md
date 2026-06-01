# Research Playbook → the research wiki

Goal: ground every slide in real facts. No invented stats, stars, or quotes. Output a small
markdown "wiki" under `instagram-carousel/<topic-slug>/input/` (the per-topic `input/` folder — if
the user handed you a research folder, this is where its notes go too).

## Output shape
```
input/
├── sources.md            # index: one row per source — title, url, type, one-line takeaway
├── <source-1-slug>.md    # the facts you pulled from source 1
├── <source-2-slug>.md
└── notes.md              # cross-source synthesis: the angle, the N items, the proof points
```
Keep each file short — you only need enough for tight copy.

## Per source type

### GitHub repos
Pull with `gh` (preferred) or web:
```bash
gh repo view <owner/repo> --json name,description,stargazerCount,url,homepageUrl,repositoryTopics
```
Capture: **stars**, one-line "what it is", **"why it matters"** (the So-What), primary language,
and any distinctive **visual detail** worth mimicking on a slide (e.g. "repo header: black top nav,
owner/name, star pill, About blurb on the right"). Note it as a `mimic_ui` candidate.

### Articles / links / trends
Use web search / firecrawl / WebFetch. Capture the claim, any number, the source, and the date.
Prefer primary sources. If a stat can't be verified, mark it `[unverified]` and don't put it on a slide.

### "This is trending"
Find *why* it's trending and the concrete artifact behind it (a release, a repo, a thread). The
carousel needs specifics, not "X is blowing up".

## Synthesis (`notes.md`)
Before writing copy, decide:
- The **one angle** (what's the through-line that makes these N items one story).
- The **ordered N items** (strongest first, 2nd-strongest last).
- The **proof points** (numbers, stars, names) mapped to the slides that will carry them.
- Any **`mimic_ui`** slides and which source they represent.

## Depth
- Sources pasted → research them (deep).
- No sources → skip research; write from the topic + the user's intake answers, and say so.
- Don't over-research: 5–15 minutes of fact-finding is plenty for a carousel.
