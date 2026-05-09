---
name: pfwh-image-generator
description: Generate Primavera Flowers product/lifestyle/ad imagery via OpenAI gpt-image-1 at the cheapest tier (~$0.011 per 1024x1024 image, quality=low). Outputs PNGs to ~/Downloads/pfwh-images/<style>/. Use when the user says "generate flower images", "make pfwh photos", "generate hero/IG/sympathy images", or invokes `/pfwh-image-generator`. Reads OPENAI_API_KEY from env or ~/.zshrc.
---

# Primavera Flowers — image generator

Generates batches of Primavera-branded imagery using OpenAI's cheapest viable image model (`gpt-image-1` at `quality=low`, ~$0.011 per 1024x1024 PNG).

## When to use

- "generate flower images for primavera"
- "make hero / IG grid / sympathy / bilingual photos"
- "rebuild the IG tiles"
- "/pfwh-image-generator"

## Cost reference (May 2026)

| Model | Quality | Size | Cost / image |
|---|---|---|---|
| **gpt-image-1** | low (default) | 1024x1024 | **~$0.011** |
| gpt-image-1 | medium | 1024x1024 | ~$0.04 |
| gpt-image-1 | high | 1024x1024 | ~$0.17 |
| gpt-image-2 | low | 1024x1024 | ~$0.04 |
| gpt-image-2 | high | 1024x1024 | ~$0.21 |
| dall-e-3 | standard | 1024x1024 | $0.04 |

Default is **gpt-image-1 / low / 1024x1024 / square** = $0.011/image. A full 25-image batch ≈ $0.28.

## Style presets (built in)

| Preset | Count default | Use case |
|---|---|---|
| `hero` | 3 | Homepage hero, marble + window light bouquet flatlays |
| `lifestyle` | 5 | UGC-style, hand-tied bouquets in WaHi apartments |
| `ig` | 9 | Instagram grid tiles, vertical 4:5 |
| `sympathy` | 4 | Standing sprays, dignified, soft funeral home light |
| `bilingual` | 4 | Día de las Madres, Spanish-language Mother's Day |
| `wholesale` | 3 | Office/restaurant arrangements in commercial spaces |
| `all` | 28 total | Run every preset in parallel |

## Inputs (auto-inferred or asked)

1. **Preset** — one of the above (default `hero`)
2. **Brand name** — defaults to `Primavera Flowers`
3. **Output dir** — defaults to `~/Downloads/pfwh-images/<preset>/`
4. **Quality** — `low` (default, cheapest) | `medium` | `high`

## Workflow

```bash
# Read OPENAI_API_KEY from env, fallback to ~/.zshrc grep
OPENAI_API_KEY="${OPENAI_API_KEY:-$(grep -m1 OPENAI_API_KEY ~/.zshrc 2>/dev/null | sed -E 's/.*="([^"]+)".*/\1/')}"

# Run the generator
python3 ~/.claude/skills/pfwh-image-generator/scripts/generate.py \
  --preset hero \
  --quality low \
  --count 3
```

The script:
1. Reads `OPENAI_API_KEY` from env (or `~/.zshrc`)
2. Loads built-in prompts for the requested preset
3. Calls `https://api.openai.com/v1/images/generations` with model=`gpt-image-1`, quality=`low` in 4-way parallel
4. Decodes the b64 response → writes `<output_dir>/<preset>-NN.png`
5. Reports total cost + paths

## Critical defaults

- **Model**: `gpt-image-1` (do NOT use gpt-image-2 unless quality required — 4x cost)
- **Quality**: `low` (do NOT escalate to medium/high without user approval — 4x and 17x cost)
- **Size**: `1024x1024` square (cheapest tier)
- **Background**: white or neutral, matching brand sage/blush palette
- **Branding rule**: do NOT render text overlays — Shopify will overlay headlines via Liquid

## Sandbox/Mac note

This skill **only runs from a host with reachable `api.openai.com`** — your Mac terminal works; Claude Code on the Web (sandbox) does not (egress proxy blocks `Host not in allowlist`).

To run from your Mac after pulling this repo:
```bash
cp -r .claude/skills/pfwh-image-generator ~/.claude/skills/
# Then invoke from any Claude Code session on your Mac:
/pfwh-image-generator hero
```

## Upload to Shopify CDN (optional follow-up)

After generating, upload the PNGs to Shopify CDN via Admin API (`fileCreate` mutation) so they get permanent CDN URLs you can paste into theme sections. The script writes a `manifest.json` listing all generated paths — use that as input to a separate uploader.
