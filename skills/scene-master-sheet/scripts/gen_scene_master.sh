#!/usr/bin/env bash
# Generate a wide scene master reference image via the generate-image skill.
# Usage: gen_scene_master.sh "<prompt>" [output-dir]
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 \"<prompt>\" [output-dir]" >&2
  exit 1
fi

SCENE_PROMPT="$1"
SCENE_OUTDIR="${2:-./output/scene-masters}"
SCENE_GEN="${CHARACTER_SCENE_GENERATOR:-$HOME/.claude/skills/generate-image/generate_image.py}"

if [ ! -f "$SCENE_GEN" ]; then
  echo "error: generate-image script not found at $SCENE_GEN" >&2
  echo "set CHARACTER_SCENE_GENERATOR to its path" >&2
  exit 1
fi

mkdir -p "$SCENE_OUTDIR"

at-cli exec skill 'generate-image' -- \
  python3 "$SCENE_GEN" --prompt "$SCENE_PROMPT" --output-dir "$SCENE_OUTDIR"
