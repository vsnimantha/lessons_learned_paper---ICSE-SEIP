# Provenance of each data file

| File | Source | Status |
|---|---|---|
| `data/records.csv` | differential records of the verification stage (1,163 rows) | authoritative, copied from the triage-study repository |
| `data/configurations.csv` | the 15 variants and DEBUG/O0 | copied from the triage-study repository |
| `data/verdicts.csv` | plugin verdicts (17 rows) | copied from the triage-study repository |
| `data/findings.csv` | findings D1 to D15 with grade, severity, disclosure state | built from the triage-study repository; disclosure state is a snapshot, update before release |
| `data/plugins.csv` | participation matrix and per-plugin figures | transcribed from the study papers; S3 and S4 columns agree with the records, S1 columns are verified against the raw reports by `make check`, S2 columns still need the raw activation outputs; exclusion reasons are TODO |
| `data/ledger.csv` | merged defect ledger (27 defects) | transcribed from the study papers; verify against the stage repositories |
| `data/exclusion_reasons.csv` | taxonomy of ineligibility codes | new, to be applied per plugin |
| `data/s1_reports.csv`, `data/s1_high_signal.csv` | summaries of `data/static_reports/*.json` made by `scripts/import_s1_reports.py` | authoritative (raw reports of the baseline run) |
| `data/activation_coverage.csv`, `data/activation_branch_extra.csv` | plugin-source line coverage, median of five runs, five approaches, 16 plugins; two branch-coverage values from the activation paper text | transcribed from the activation paper; per-run data not yet available |
| `data/s1_sensitivity.csv` | B0, B1, S1, S2 sensitivity configurations | transcribed from the static paper and the Stage 1 report |
| `data/activation_bugs.csv`, `data/activation_templates.csv`, `data/activation_notes.md` | flagged programs and distinct defects per plugin, template characteristics, notes on the coverage table | transcribed from the activation paper |
