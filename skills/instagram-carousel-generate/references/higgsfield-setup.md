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

### Saving renders on the MCP path (write real images into `output/`)
The deliverable is **image files** — `output/slide-01.png … slide-NN.png` — never a download script.
Hosts like Cowork sandbox the network and **block HiggsField's CDN** (`*.cloudfront.net` →
`403 blocked-by-allowlist`), so a plain `curl`/fetch of the returned URL writes nothing. Save in this
priority order and stop at the first that works:

1. **Inline bytes (preferred — works even when the CDN is blocked).** If the MCP tool result carries the
   render as inline/base64 image content, decode it and write the bytes straight to
   `output/slide-NN.png`. No network call, so the allowlist can't bite.
2. **Fetch the URL.** If the result only gives a URL, download it into `output/` (works when the host
   isn't sandboxed, or the CDN host is allowlisted).
3. **Last resort only.** If the fetch returns `403 blocked-by-allowlist` **and** no inline bytes are
   available, write `output/download_slides.sh` (mapping each final pick → `slide-NN.png`) and tell the
   user to run it on their own machine. This is a labelled fallback — never the primary deliverable.

To make images land in-sandbox, either the MCP must return bytes (option 1) or the user allowlists the
HiggsField CDN host in the Cowork connector/network settings. Verify at the end: every
`output/slide-NN.png` exists, is a non-zero PNG, and reached a **success** terminal status.

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
| fetch `403 blocked-by-allowlist` | host sandboxes HiggsField's CDN (Cowork) | write the render's bytes from the MCP tool result directly (no fetch); else `download_slides.sh` fallback + allowlist the CDN host. See "Saving renders on the MCP path". |

## Prereq check order (skill runs this first, before any spend)
1. HiggsField reachable (CLI `account status` OK, or MCP connected).
2. `python3 -c "import PIL"` OK (else `pip install -r requirements.txt`).
3. Assets resolve: fonts + character-references via the asset contract; `_reference-style/` via
   the project root (see BRAND.md).
Print the exact remedy for whichever fails, and stop.
