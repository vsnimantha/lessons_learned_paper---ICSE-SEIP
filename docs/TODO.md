# Open items before release

## SEIP paper (check each before the repository is made public)
- [ ] D2 grade: `findings.csv` says A; the adjudication draft regrades it to B (10 bugs / 5 violations vs 11 / 4). The SEIP paper avoids the split and says "15 confirmed findings".
- [ ] Static split: this package recomputes 8 / 16 / 1 from the raw reports; the static-analysis manuscript text used 13 / 11 / 1 in an earlier draft. Make both agree.
- [ ] Case 1 states all four missing-return functions in DFED are currently uncalled (`ledger.csv` L21 to L24). An earlier draft said `isLoad` had a live caller. Verify against the DFED source.
- [ ] Disclosure state of every finding (D5 in particular) before claiming "reported" anywhere.
- [ ] Triage resolved share: 390 of 1,020 (38.2%) here vs 533 of 1,163 (45.8%) in the accepted triage paper.
- [ ] Add raw evidence for Case 3: contract-sweep runs (`data/contract_sweeps.csv` is transcribed), the 16-plugin-build assembly comparison for stackleak, and the 47-versus-0 trace counts (differential study repository).
- [ ] Replace `\datarepo` in the paper with the real URL; add a LICENSE.

- [ ] Exclusion reasons: done for the 4 Roffirim plugins outside activation (NO_MEANINGFUL_SEARCH_OBJECTIVE). Still open: 5 plugins outside activation (05_my_first_pass, CTraps, KayrebtCallgraphs, gcc-jump-master, gcc-python-plugin) and 8 outside verification (`plugins.csv`, columns `s2_exclusion_reason`, `s3_exclusion_reason`).
- [x] Raw Stage 1 reports imported (`data/static_reports/`); completion classes, 18 raw reports, 16 in scope and 13 cases are recomputed by `make check-seip`. Sensitivity run (B1, S1, S2) not yet imported.
- [ ] Raw Stage 2 activation runs. Medians over five runs for all 16 plugins and four baselines are now in `data/activation_coverage.csv` (from the activation paper table) and are kept for reference. Still needed: per-run values (per-run effect sizes, IQRs) and the 7 crash defects' logs.
- [ ] Which of the 7 activation defects were new and which were re-found.
- [x] Verification inputs: activation programs for the 13 plugins in both dynamic stages, existing or trivial inputs for the four tutorial plugins (author's latest instruction; the verification paper says otherwise).
- [x] Why the Stage 1 baseline missed the DFED missing return: `g++` stopped on `DFED_Plugin.cpp` (missing `DFEDcreator.h`), and Cppcheck raised no missing-return report there (see `data/static_reports/dfed_plugin_static_analysis_report.json`).
- [x] Cost data: stage times supplied by the author (data/stage_cost.csv). Still not reported: trace storage and instrumentation overhead.
- [ ] Disclosure state of D4 and D5 (`data/findings.csv`). D1 and D6 to D15 were reported in October 2026 (author).
