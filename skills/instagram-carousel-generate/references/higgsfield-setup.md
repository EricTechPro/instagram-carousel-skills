# HiggsField setup, prereqs & failure modes

The generate skill needs HiggsField GPT Image 2 to render backgrounds. Two paths — the skill
auto-detects which is available and adapts.

## Path A — CLI (local machines)
```bash
npm install -g @higgsfield/cli      # exposes: higgsfield, higgs, hf
higgsfield auth login               # browser/device login; approve the page
higgsfield account status --json    # MUST succeed before you trust auth
```
- Do **not** print or request tokens. Don't run `higgsfield auth token`.
- Confirm the model + params:
```bash
higgsfield model get gpt_image_2 --json   # aspect_ratio, quality, resolution, batch_size, seed?
```
- gpt_image_2 aspect ratios: `1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3` — **no 4:5**. Use `3:4` then crop.

### Generate (CLI, one-shot)
```bash
higgsfield generate cost   gpt_image_2 --prompt "<plate prompt>" --json     # estimate first
higgsfield upload <ref.png|jpg> --json                                       # per reference image
higgsfield generate create gpt_image_2 \
  --prompt "<plate prompt>" \
  --image <ref_id_1> --image <ref_id_2> --image <ref_id_3> \
  --aspect_ratio 3:4 --resolution 2k --quality high --batch_size 2 \
  --seed <PINNED_SEED> --wait --json
```
Parse the returned job JSON for the output URL/path; download; then hand to `compose_slide.py`.

## Path B — MCP (Clockwork / cowork)
- Connect the **HiggsField MCP** in the host's connector/settings UI (account-level; this repo does
  not install it).
- On this path the **skill/agent drives the HiggsField MCP tools call-by-call** (cost → create →
  wait → fetch). `generate_carousel.py` is **not** the driver here — but its `compose_slide.py` step
  still runs locally to crop + overlay, as long as the harness has a filesystem.
- If the host has no local filesystem, the agent composes via the same Pillow logic in-process.

## Cost gating (always)
A carousel spends per slide. Run `generate cost` once, multiply by slide count, show the total +
count, and require **one** confirmation before the batch. Report actual credits spent at the end.

## Failure modes & handling
| Symptom | Cause | Handling |
|---|---|---|
| `Not authenticated` | login not completed | run `auth login`, wait for browser approval, re-check `account status` |
| terminal status `ip_detected` | prompt named/drew a brand | logos are PIL-pasted, not generated — keep the plate prompt brand-free; never ask the model to draw a logo |
| terminal status `nsfw`/`failed` | model refused/errored | stop, report; regen that one plate; don't write a zero-byte file |
| world drifts across slides | chained refs / no seed | use the FIXED reference set + the one PINNED seed every slide; never chain N−1 |
| text garbled | text was generated | it shouldn't be — all copy is Pillow-composited; if you see baked text, the plate prompt leaked copy |
| unknown model id | id changed | re-run `model list --image --json`, use the exact id |

## Prereq check order (skill runs this first, before any spend)
1. HiggsField reachable (CLI `account status` OK, or MCP connected).
2. `python3 -c "import PIL"` OK (else `pip install -r requirements.txt`).
3. Assets resolve (fonts, style-reference, character-references) via the asset contract.
Print the exact remedy for whichever fails, and stop.
