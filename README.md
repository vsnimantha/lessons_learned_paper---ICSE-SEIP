# Replication package: "Loaded Is Not Activated: Lessons from Testing GCC Plugins"

Data behind the quantitative claims and cases of the ICSE 2027 SEIP paper. The paper is an
experience report over a multi-year programme of studies on one corpus of 25 GCC plugins.
This package holds the per-record data of those studies.

**Status (read first).** Stage 1 numbers are recomputed from the raw static reports in
`stages/s1-static/reports/`. The per-record triage data (Stage 3 and 4) are authoritative.
The Stage 2 (activation) columns and the merged defect ledger are transcribed from paper tables
because the raw activation runs are not in this package yet (see `docs/TODO.md`).

## Quick start (standard library only, Python 3.8+)

```
make check-seip   # recompute every number the paper states (43 checks); `make check` is an alias
```

## Paper claim to data

| Paper location | Claim | Data |
|---|---|---|
| Table V, Episode 4 | 25 plugins; 8 fully / 16 partially / 1 not analysed | `data/plugins.csv`, `stages/s1-static/reports/` |
| Table V | 18 raw high-signal reports, 13 distinct cases, 11 defects and 2 risks | `data/s1_high_signal.csv`, `data/plugins.csv` |
| Table V, Episode 5 | 16 plugins; 7 reproducible failures; 1 developer-confirmed; 2 flaggable by default warnings, 1 reported by our static baseline | `data/activation_bugs.csv`, `data/ledger.csv` |
| Table V, Episode 6 | 17 plugins; 69 programs; 1,163 records = 1,035 comparisons + 128 baseline rows | `data/records.csv` |
| Abstract, Episode 6 | 15 not investigated, 90 statically discharged, 300 runtime benign, 630 escalated; 390 of 1,020 investigated resolved (38.2%) | `data/records.csv` |
| Table V, abstract | 12 flagged plugins; 5 with and 7 without findings; 15 confirmed findings in 6 plugins | `data/verdicts.csv`, `data/findings.csv`, `data/patches.csv` |
| Case 1, Case 2 | DFED: four uncalled missing-return functions vs the live `findArgumentValue` crash | `data/ledger.csv` (L02, L21 to L24), `data/activation_bugs.csv`, `stages/s1-static/reports/dfed_plugin_static_analysis_report.json` |
| Case 3 | stackleak and latent_entropy: 60 likely-bug records each, same tags, mean 19 / 20 removed symbols, opposite verdicts; latent_entropy loses instrumentation in 14 of 15 configurations | `data/records.csv`, `data/contract_sweeps.csv`, `data/verdicts.csv`, `data/findings.csv` (D5) |
| Case 4 | SecRetAddress: 60 benign records, compiler crash on noreturn functions (D1) | `data/records.csv`, `data/findings.csv` |
| Section V | 27 defects, 21 found by exactly one stage | `data/ledger.csv` |
| Cost allocation | 10 to 15 min per template, 24 to 36 CPU-hours per run, 5 runs per plugin | `data/stage_cost.csv`, `data/activation_templates.csv` |

## Layout

```
data/       corpus, per-record differential data, verdicts, findings, ledger, costs
analysis/   check_seip.py (recomputes the paper's numbers), common.py
stages/     one directory per stage; stage 1 holds the raw static reports
schemas/    JSON Schemas of the typed artifacts passed between stages
pipeline/   stage orchestrator (needs the stage tools, see docs/INTEGRATING_TOOLS.md)
docs/       overview, stage interfaces, provenance, TODO
```

## Known limits

- Plugins are tied to GCC internals: the triage study pins GCC 13.3 on x86-64, the differential
  verification spans GCC 10 to 14.
- The 15 findings were reproduced on the study copies; upstream commits are in `data/activation_bugs.csv` and
  `docs/PROVENANCE.md`. Disclosure states in `data/findings.csv` are a snapshot and may be out of date.
- Resolved share: the paper reports 390 of 1,020 investigated comparisons (38.2%). Counting the 128 baseline rows and 15 uninvestigated comparisons as resolved would give 533 of 1,163 (45.8%), the figure of the earlier triage study.
- Not in this package yet: the raw contract-sweep runs, the stackleak 16-plugin-build assembly comparison, and the 47-versus-0 stackleak trace counts (from the differential study's own repository). `data/contract_sweeps.csv` is transcribed.
- The Dockerfile is untested.
