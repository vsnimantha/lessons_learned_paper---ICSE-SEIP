# Stage 4: contract-driven triage and adjudication

**Slot for:** the triage harness, kept in its own repository.

## Input
- Escalated plugins from Stage 3 (`LIKELY_BUG` records), plugin source, one test
  program per plugin.

## What the stage does
1. Reads the plugin selection logic and writes a **contract** (what the plugin must do).
2. Automated investigator: six steps, including the precondition check
   "did the plugin act?".
3. Adjudication by contract: probes, ASan, Valgrind, `-fchecking=2`, libstdc++ debug mode.
4. Sweep over 15 configurations of the **program** build flags (Stage 3 varies the
   plugin build instead).
5. Verdict per plugin and grade per finding.

## Verdicts
- Grade A bug, Grade B contract violation.
- Confirmed benign (contract holds in all 15 configurations).
- Benign, out of scope or non-impacting.
- Not examined.

## Output
- `data/verdicts.csv` (per plugin), `data/findings.csv` (D1 to D15), `reproducers/`.

## Reproduce
Triage reproducers live in a separate data repository (see
`scripts/import_triage_repo.sh`). The verdict table here is copied from it.
Triage used GCC 13.3 on x86-64.
