# Stage 3: differential verification

**Slot for:** the instrumentation and differential tool, kept in its own repository.

## Input
- Plugin source, test programs (`tests/<plugin>/*.c`), the configuration list in
  `data/configurations.csv`.

## What the stage does
1. Instruments the plugin (libclang) behind an 11-check safety gate.
2. Builds 15 variants of the instrumented plugin (optimisation, sanitizer, hardening
   settings, see `data/configurations.csv`) and a `-g` BASE.
3. Runs each test program with every variant and with BASE. Compares binaries
   and call frames. DEBUG and O0 rows are noise controls and are never labelled.
4. Labels each comparison: `UNLABELLED` (not investigated), `OPTIMISED_AWAY`,
   `CONFIRMED_BENIGN` (runtime benign), `LIKELY_BUG` (escalated).

## Output
- `s3_records.csv` with the columns of `data/records.csv`.

## Reproduce
`data/records.csv` (1,163 records) is the authoritative per-record output of this
stage in this archive. `python3 analysis/check_consistency.py` recomputes the funnel
(15 | 90 | 300 | 630) and the correlation from it.
