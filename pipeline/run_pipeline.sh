#!/usr/bin/env bash
# Stage orchestrator. Runs s1..s4 in order, skips a stage whose tool is not present and
# says exactly what is missing. Eligibility is per stage (see docs/STAGE_INTERFACES.md):
# a plugin that is not eligible for a stage is recorded, not silently dropped.
#   usage: pipeline/run_pipeline.sh [--plugin NAME] [--stages s1,s2,s3,s4] [--dry-run]
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGES="s1,s2,s3,s4"; PLUGIN=""; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --plugin) PLUGIN="$2"; shift 2;;
    --stages) STAGES="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    *) echo "unknown argument $1" >&2; exit 2;;
  esac
done
declare -A DIR=( [s1]=s1-static [s2]=s2-activation [s3]=s3-verification [s4]=s4-triage )
OUT="$ROOT/pipeline/work"; mkdir -p "$OUT"
missing=0
for s in ${STAGES//,/ }; do
  entry="$ROOT/stages/${DIR[$s]}/run.sh"
  if [ ! -x "$entry" ]; then
    echo "[$s] MISSING  no executable $entry (place the stage tool there; see stages/${DIR[$s]}/README.md)"
    missing=$((missing+1)); continue
  fi
  echo "[$s] RUN      $entry ${PLUGIN:+--plugin $PLUGIN}"
  [ "$DRY" -eq 1 ] && continue
  "$entry" --out "$OUT/$s" ${PLUGIN:+--plugin "$PLUGIN"} || { echo "[$s] FAILED"; exit 1; }
done
echo "stages missing: $missing"
echo "Paper numbers can still be reproduced from data/: run 'make check'."
exit 0
