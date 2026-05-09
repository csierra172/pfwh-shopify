#!/usr/bin/env python3
"""
Primavera Flowers image generator — cheapest OpenAI tier.

Defaults: gpt-image-1, quality=low, 1024x1024 → ~$0.011 per image.
Reads OPENAI_API_KEY from env, falls back to ~/.zshrc grep.

Stdlib only (no pip install required).
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

API_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_MODEL = "gpt-image-1"
DEFAULT_QUALITY = "low"
DEFAULT_SIZE = "1024x1024"

# Cost in USD per image at default config (gpt-image-1 low 1024x1024)
COST_PER_IMAGE = {
    ("gpt-image-1", "low"): 0.011,
    ("gpt-image-1", "medium"): 0.042,
    ("gpt-image-1", "high"): 0.167,
    ("gpt-image-2", "low"): 0.040,
    ("gpt-image-2", "medium"): 0.080,
    ("gpt-image-2", "high"): 0.210,
    ("dall-e-3", "standard"): 0.040,
    ("dall-e-3", "hd"): 0.080,
    ("dall-e-2", "standard"): 0.016,
}

PRESETS = {
    "hero": [
        "Editorial commercial photograph: hand-tied bouquet of pink garden roses, blush peonies, white ranunculus, eucalyptus, wrapped in cream kraft paper, on a white marble countertop. Soft diffused window light from the left, golden hour. Shallow depth of field. Style: New York florist boutique. No people, no text, no logos.",
        "Overhead flatlay: cream and peach garden roses, white ranunculus, sage eucalyptus, on a linen-covered wooden table. Pruning shears and twine to one side. Soft daylight. Editorial magazine style. No text, no logos.",
        "Close-up macro: a single pink garden rose with dewdrops, soft focus background of more bouquet behind, ultra-fine petal detail, golden hour backlight. No people, no text.",
    ],
    "lifestyle": [
        "Candid iPhone-style photo: woman in a Washington Heights apartment unwrapping a Primavera bouquet of pink peonies and roses, kraft paper visible, golden hour through window. Warm, intimate, real. No brand text on packaging.",
        "Lifestyle shot: a small wooden kitchen table with a sage-green ceramic vase holding pink garden roses and eucalyptus, morning light, coffee cup nearby, tasteful upper Manhattan apartment vibe. No people, no text.",
        "Office desk corner: a small bud vase with 3 stems of ranunculus, laptop and notebook just out of focus, soft cool morning light. No text overlays.",
        "Restaurant table at golden hour: low arrangement of seasonal blush flowers in a white compote vase, place setting partially in frame, candid editorial. No people in foreground, no text.",
        "Hands holding a wrapped bouquet: cream peonies, pink roses, kraft paper, sage ribbon, shallow depth of field, indoors near a brownstone window. No faces visible.",
    ],
    "ig": [
        "Vertical 4:5 Instagram tile: a single white peony close-up against soft sage-green linen backdrop. Editorial florist aesthetic. No text.",
        "Vertical 4:5 IG tile: hands tying a bouquet of pink garden roses with sage twine, top-down view, kraft paper visible, natural light. No faces, no text.",
        "Vertical 4:5 IG tile: overhead view of a flower shop workbench with stems being trimmed, scattered eucalyptus leaves, scissors, cream wrapping paper. No text.",
        "Vertical 4:5 IG tile: a delivery van or bicycle in front of a Manhattan brownstone with a wrapped bouquet visible in the basket, golden hour. No text, no logos.",
        "Vertical 4:5 IG tile: candle, ceramic vase with flowers, open book on a side table, warm cozy upper-Manhattan-apartment vibe. No text.",
        "Vertical 4:5 IG tile: macro detail of a ranunculus bloom, water droplets, sage and cream palette, magazine quality. No text.",
        "Vertical 4:5 IG tile: a flower designer in a sage-green apron arranging stems in a studio, hands and apron visible, no face. Editorial. No text.",
        "Vertical 4:5 IG tile: birthday-themed bouquet of pink and cream roses with a kraft tag tied with twine, top-down on white marble. No readable text on tag.",
        "Vertical 4:5 IG tile: sympathy white standing spray with white roses, lilies, and greenery on a wooden easel, soft warm light, dignified. No text.",
    ],
    "sympathy": [
        "Sympathy arrangement: white standing spray of white roses, lilies, and greenery on a dark wooden easel inside a quiet funeral home. Soft warm directional light, dignified, somber but beautiful. No people, no text.",
        "Sympathy: low casket-spray-style arrangement of white peonies, white roses, eucalyptus, and white hydrangea on a polished surface, soft side light, restrained palette. No text.",
        "Sympathy: a small condolence bouquet wrapped in cream paper sitting on a granite headstone surrounded by green grass, soft overcast light, contemplative. No text.",
        "Sympathy: hand reaching to place a single white rose on a closed condolence card on a wooden table, soft natural light, no faces visible. No text on card.",
    ],
    "bilingual": [
        "Día de las Madres bouquet: pink peonies, garden roses, ranunculus, wrapped in kraft paper with a single sage ribbon, on a marble surface, warm sunlight. Spanish-Latin warmth, no text overlays.",
        "Mother's Day arrangement: cream peonies and pink roses in a ceramic vase on a tile counter, with a small kraft envelope leaning beside it, golden hour. No readable text.",
        "Latina mother and daughter (only hands and torsos visible) sharing a bouquet of pink flowers in a sunlit kitchen, warm intimate domestic moment. No faces, no text.",
        "Spanish-language Día de las Madres setup: dining table with flowers as centerpiece, small wrapped gift, candle, warm afternoon light. No people, no text overlays.",
    ],
    "wholesale": [
        "Office reception bouquet: tall structural arrangement of white orchids, eucalyptus, and white roses on a polished marble reception desk in a modern Manhattan office lobby, soft morning light. No text.",
        "Restaurant table flowers: minimal low arrangement of seasonal blush flowers in a cylindrical glass vase on a set dinner table, candle light, intimate fine-dining mood. No people, no text.",
        "Salon: a sage ceramic vase with curated stems of garden roses and eucalyptus on a marble counter beside styling tools, modern boutique aesthetic, warm light. No text.",
    ],
}


def read_api_key():
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    zshrc = Path.home() / ".zshrc"
    if zshrc.exists():
        for line in zshrc.read_text().splitlines():
            m = re.match(r'\s*export\s+OPENAI_API_KEY\s*=\s*"([^"]+)"', line)
            if m:
                return m.group(1).strip()
    return ""


def call_openai(api_key, model, prompt, quality, size, timeout=120):
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "response_format": "b64_json",
    }).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def generate_one(api_key, model, quality, size, prompt, out_path, retries=3):
    if out_path.exists():
        return ("skip", out_path, None)
    last_err = None
    for attempt in range(retries):
        try:
            r = call_openai(api_key, model, prompt, quality, size)
            b64 = r["data"][0]["b64_json"]
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(base64.b64decode(b64))
            return ("ok", out_path, None)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="ignore")[:300]
            last_err = f"{e.code} {body}"
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            return ("fail", out_path, last_err)
        except Exception as e:
            last_err = f"{type(e).__name__}: {str(e)[:200]}"
            time.sleep(2 ** attempt)
    return ("fail", out_path, last_err)


def main():
    p = argparse.ArgumentParser(description="Primavera image generator")
    p.add_argument("--preset", default="hero", choices=list(PRESETS.keys()) + ["all"])
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--quality", default=DEFAULT_QUALITY, choices=["low", "medium", "high", "standard", "hd"])
    p.add_argument("--size", default=DEFAULT_SIZE)
    p.add_argument("--count", type=int, help="Override prompt count for the preset")
    p.add_argument("--out-dir", default=str(Path.home() / "Downloads" / "pfwh-images"))
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--dry-run", action="store_true", help="Print plan without calling API")
    args = p.parse_args()

    api_key = read_api_key()
    if not api_key and not args.dry_run:
        print("ERROR: OPENAI_API_KEY not set in env or ~/.zshrc", file=sys.stderr)
        sys.exit(2)

    presets_to_run = list(PRESETS.keys()) if args.preset == "all" else [args.preset]
    jobs = []
    for preset in presets_to_run:
        prompts = PRESETS[preset]
        if args.count:
            prompts = (prompts * ((args.count // len(prompts)) + 1))[: args.count]
        for i, prompt in enumerate(prompts, start=1):
            out = Path(args.out_dir) / preset / f"{preset}-{i:02d}.png"
            jobs.append((preset, i, prompt, out))

    cost_per = COST_PER_IMAGE.get((args.model, args.quality), 0.04)
    total_cost = len(jobs) * cost_per
    print(f"Plan: {len(jobs)} images · model={args.model} · quality={args.quality} · size={args.size}")
    print(f"Estimated cost: ${total_cost:.2f} (${cost_per:.3f}/img)")
    print(f"Output: {args.out_dir}")
    if args.dry_run:
        for preset, i, prompt, out in jobs:
            print(f"  [{preset} #{i}] -> {out}")
        return

    print(f"Generating with {args.workers} parallel workers...")
    ok, skip, fail = 0, 0, 0
    failures = []
    manifest = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {
            ex.submit(generate_one, api_key, args.model, args.quality, args.size, prompt, out): (preset, i, out)
            for preset, i, prompt, out in jobs
        }
        for fut in as_completed(futures):
            preset, i, out = futures[fut]
            status, path, err = fut.result()
            if status == "ok":
                ok += 1
                print(f"  OK   [{preset} #{i:02d}] {path}")
                manifest.append({"preset": preset, "index": i, "path": str(path)})
            elif status == "skip":
                skip += 1
                print(f"  SKIP [{preset} #{i:02d}] {path} (already exists)")
                manifest.append({"preset": preset, "index": i, "path": str(path)})
            else:
                fail += 1
                print(f"  FAIL [{preset} #{i:02d}] {err}", file=sys.stderr)
                failures.append({"preset": preset, "index": i, "error": err})

    manifest_path = Path(args.out_dir) / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps({"images": manifest, "failures": failures}, indent=2))
    print(f"\nDone: {ok} generated, {skip} skipped, {fail} failed")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
