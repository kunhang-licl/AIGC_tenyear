#!/usr/bin/env bash
# Generate a four-panel character turnaround sheet via the generate-image skill.
# Usage: gen_quad_sheet.sh "<prompt>" [output-dir]
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 \"<prompt>\" [output-dir]" >&2
  exit 1
fi

QUAD_PROMPT="$1"
QUAD_OUTDIR="${2:-./output/quad-sheets}"
QUAD_GEN="${CHARACTER_QUAD_GENERATOR:-$HOME/.claude/skills/generate-image/generate_image.py}"

if [ ! -f "$QUAD_GEN" ]; then
  echo "error: generate-image script not found at $QUAD_GEN" >&2
  echo "set CHARACTER_QUAD_GENERATOR to its path" >&2
  exit 1
fi

mkdir -p "$QUAD_OUTDIR"

at-cli exec skill 'generate-image' -- \
  python3 "$QUAD_GEN" --prompt "$QUAD_PROMPT" --output-dir "$QUAD_OUTDIR"
