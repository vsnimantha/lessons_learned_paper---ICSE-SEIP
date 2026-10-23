# Notes on data/activation_coverage.csv

Source: the activation paper (coverage table, median of five runs, plugin-source line coverage).

- Csmith and AFL++ are applicable to 11 plugins in that paper (bug table marks `gcc_assert_introspect`, `CFED`, `SecRetAddress`, `instrument_attribute` and `oi` as not applicable; its Wilcoxon tests use n = 11, W = 66).
- Its coverage table nevertheless prints Csmith 41.3 and AFL++ 45.2 for `instrument_attribute`. These two values conflict with the applicability rule and with n = 11, so they are left empty here. Confirm which is right.
- Two branch-coverage values appear in its text: `cprintf` 24.4 to 67.6, `SecRetAddress` 21.6 to 92.2 (`activation_branch_extra.csv`).
