#!/usr/bin/env python3
"""Batch keyframe generator for storyboard shots.

Reads a shot table (JSON), generates one keyframe image per shot via the
generate-image Ducky endpoint, names outputs deterministically, retries on
rate limits, and skips shots whose output already exists so a run can resume.

Input JSON: a list of objects, each requiring:
    shot      shot id, e.g. "00", "01"   -> used in the filename
    prompt    full keyframe prompt text
Optional:
    note      free text, copied into the manifest

Usage:
    batch_generate.py shots.json --out-dir out/ep01 --prefix ep01
    batch_generate.py shots.json --out-dir out/ep01 --prefix ep01 --only 03,07
    batch_generate.py shots.json --out-dir out/ep01 --prefix ep01 --force
    batch_generate.py cands.json --out-dir out/cand --prefix su_lin --variants 4

With --variants N, each entry produces N candidates named
<prefix>_shot<id>_v1.png .. _vN.png for human selection. Resume counts
existing variants and tops up only the missing ones.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

DEFAULT_GENERATOR = os.path.expanduser("~/.claude/skills/generate-image/generate_image.py")
MAX_ATTEMPTS = 4
BASE_BACKOFF = 45  # Ducky rate-limits aggressively; start high.


def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", file=sys.stderr, flush=True)


def generate_one(prompt, out_dir, generator, timeout):
    """Call the generator once. Return the produced path, or raise."""
    before = set(os.listdir(out_dir)) if os.path.isdir(out_dir) else set()
    proc = subprocess.run(
        ["python3", generator, "--prompt", prompt, "--output-dir", out_dir],
        capture_output=True, text=True, timeout=timeout,
    )
    combined = proc.stdout + proc.stderr
    if "Too Many Request" in combined:
        raise RuntimeError("rate_limited")
    if proc.returncode != 0:
        raise RuntimeError(f"generator exit {proc.returncode}: {combined.strip()[:300]}")

    for line in reversed(proc.stdout.strip().splitlines()):
        line = line.strip()
        if line.endswith(".png") and os.path.exists(line):
            return line
    after = set(os.listdir(out_dir)) - before
    if after:
        return os.path.join(out_dir, after.pop())
    raise RuntimeError(f"no image produced: {combined.strip()[:300]}")


def main():
    ap = argparse.ArgumentParser(description="Batch-generate storyboard keyframes.")
    ap.add_argument("shots", help="JSON file: list of {shot, prompt, note?}")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--prefix", default="shot", help="filename prefix, e.g. ep01")
    ap.add_argument("--generator", default=os.environ.get("PIPELINE_GENERATOR", DEFAULT_GENERATOR))
    ap.add_argument("--only", help="comma-separated shot ids to generate")
    ap.add_argument("--force", action="store_true", help="regenerate even if output exists")
    ap.add_argument("--delay", type=float, default=8.0, help="seconds between shots")
    ap.add_argument("--variants", type=int, default=1,
                    help="candidates per entry, for human selection")
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()

    if not os.path.isfile(args.generator):
        sys.exit(f"generator not found: {args.generator}")

    with open(args.shots, encoding="utf-8") as fh:
        shots = json.load(fh)
    if args.only:
        wanted = {s.strip() for s in args.only.split(",")}
        shots = [s for s in shots if str(s["shot"]) in wanted]
    if not shots:
        sys.exit("no shots selected")

    os.makedirs(args.out_dir, exist_ok=True)
    manifest_path = os.path.join(args.out_dir, "manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)

    done, skipped, failed = [], [], []

    total_jobs = len(shots) * args.variants
    job_no = 0

    for shot in shots:
        sid = str(shot["shot"])

        for v in range(1, args.variants + 1):
            job_no += 1
            if args.variants == 1:
                final = os.path.join(args.out_dir, f"{args.prefix}_shot{sid}.png")
                key = sid
            else:
                final = os.path.join(args.out_dir, f"{args.prefix}_shot{sid}_v{v}.png")
                key = f"{sid}_v{v}"

            if os.path.exists(final) and not args.force:
                log(f"({job_no}/{total_jobs}) {key}: exists, skip")
                skipped.append(key)
                continue

            ok = False
            for attempt in range(1, MAX_ATTEMPTS + 1):
                try:
                    log(f"({job_no}/{total_jobs}) {key}: generating (attempt {attempt})")
                    produced = generate_one(shot["prompt"], args.out_dir, args.generator, args.timeout)
                    if os.path.abspath(produced) != os.path.abspath(final):
                        os.replace(produced, final)
                    manifest[key] = {
                        "file": os.path.basename(final),
                        "prompt": shot["prompt"],
                        "note": shot.get("note", ""),
                        "generated_at": datetime.now().isoformat(timespec="seconds"),
                    }
                    log(f"({job_no}/{total_jobs}) {key}: saved {os.path.basename(final)}")
                    done.append(key)
                    ok = True
                    break
                except RuntimeError as exc:
                    if str(exc) == "rate_limited":
                        wait = BASE_BACKOFF * attempt
                        log(f"  rate limited, waiting {wait}s")
                        time.sleep(wait)
                        continue
                    log(f"  error: {exc}")
                    if attempt < MAX_ATTEMPTS:
                        time.sleep(10 * attempt)
                except subprocess.TimeoutExpired:
                    log("  timeout")
                    if attempt < MAX_ATTEMPTS:
                        time.sleep(10 * attempt)

            if not ok:
                failed.append(key)
                log(f"({job_no}/{total_jobs}) {key}: FAILED after {MAX_ATTEMPTS} attempts")

            with open(manifest_path, "w", encoding="utf-8") as fh:
                json.dump(manifest, fh, ensure_ascii=False, indent=2)

            if job_no < total_jobs:
                time.sleep(args.delay)

    log(f"done={len(done)} skipped={len(skipped)} failed={len(failed)}")
    if failed:
        log(f"failed shots: {','.join(failed)}")
        log(f"retry with: --only {','.join(sorted({k.split(chr(95)+chr(118))[0] for k in failed}))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
