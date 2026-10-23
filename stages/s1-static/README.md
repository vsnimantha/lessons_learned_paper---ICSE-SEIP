# Stage 1: static analysis and report triage

**Slot for:** the static-analysis tool of the study (kept in its own repository).
Put the tool here, or symlink it, or point `tools.private.yaml` at it.

## Input
- `corpus/<plugin>/` : plugin source tree (one directory per plugin).
- `data/plugins.csv` : plugin list.

## What the stage does
1. Runs Cppcheck 2.13.0 and `g++ 13.3.0 -fsyntax-only -Wall -Wextra` on each plugin.
2. Parses every report into one record. Parse failures are kept and counted.
3. Classifies the run: **C** complete, **P** partial (some files not processed), **F** failed.
4. Keeps *high-signal* report classes as candidates (for example missing return,
   null passed to `%s`, dangling local, uninitialised read).

## Output (typed artifacts, see `schemas/`)
- `s1_reports.jsonl` : one `Report` per tool message.
- `s1_candidates.jsonl` : one `Cand` per high-signal report, with `plugin`, `file`,
  `line`, `class`, `entry_point_hint`.
- Completion class per plugin goes to `data/plugins.csv` column `s1_class`.

## Hand-off to Stage 2
`Cand` records tell Stage 2 which plugin function to reach. The hand-off is manual in
the study (stated as a limitation). Automating it is future work.

## Reproduce the paper numbers from this stage
The 25 raw reports of the baseline run are in `reports/` (Cppcheck 2.13.0, g++ 13.3.0,
Ubuntu 24.04). `python3 scripts/import_s1_reports.py` summarises them into
`data/s1_reports.csv` and `data/s1_high_signal.csv`, and `make check` recomputes the
completion classes (8 complete, 16 partial, 1 failed), the 18 raw high-signal reports,
the 16 in-scope reports and the 13 cases. A failure confined to `testcases/` does not
change completion. The author's Stage 1 write-up is `docs/STAGE1_REPORT_source.md`.
