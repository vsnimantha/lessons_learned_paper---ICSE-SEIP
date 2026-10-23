# Stage interfaces

| Stage | Reads | Writes | Schema |
|---|---|---|---|
| s1 | plugin sources | `s1_reports.jsonl`, `s1_candidates.jsonl` | `Cand` |
| s2 | plugin build, args, optional `Cand` | `s2_coverage.csv`, `s2_failures.jsonl`, `tests/` | `Act`, `Coverage`, `Failure` |
| s3 | plugin source, test programs, `configurations.csv` | `s3_records.csv` | `Obs`, `Delta` |
| s4 | escalated plugins, one test program each | `s4_verdicts.csv`, `s4_findings.csv`, `reproducers/` | `Contract`, `Verdict` |

## Independent eligibility (Algorithm 1)

- Activation runs only if the plugin has an input-dependent activation problem and can be built, loaded and run reproducibly.
- Verification runs only if the plugin is instrumentable and the chosen test inputs exercise a behavioural obligation.
- The two checks are independent. For the 13 plugins that entered both dynamic stages, test inputs for verification are the programs produced by activation. A plugin that is not eligible for activation (the four tutorial plugins) uses existing or trivial manually supplied inputs.
- Ineligibility is recorded with a code from `data/exclusion_reasons.csv`.

## Contract for a stage entry point

```
stages/<slot>/run.sh --out DIR [--plugin NAME]
exit 0 on success; non-zero only for tool failure, never for "no finding"
```
