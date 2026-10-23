#!/usr/bin/env bash
# Copy the triage data from the separate triage-study repository into this artefact.
#   usage: scripts/import_triage_repo.sh /path/to/triage-repo
# Copies verdicts, findings table and reproducers; does not modify the source repo.
set -eu
SRC="${1:?path to triage repository}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$SRC/triage/plugin_verdicts.csv" ] || { echo "not a triage repository: $SRC" >&2; exit 2; }
cp "$SRC/triage/plugin_verdicts.csv" "$ROOT/data/verdicts.csv"
[ -f "$SRC/data/records.csv" ] && cp "$SRC/data/records.csv" "$ROOT/data/records.csv"
mkdir -p "$ROOT/stages/s4-triage/reproducers"
if [ -d "$SRC/triage/reports" ]; then cp -r "$SRC/triage/reports" "$ROOT/stages/s4-triage/reproducers/"; fi
echo "imported. Re-run: make check   then review stages/s4-triage/reproducers/ for stray private paths (grep -r)"
