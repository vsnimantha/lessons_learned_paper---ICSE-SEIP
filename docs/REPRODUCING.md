# Reproducing the paper's numbers

```
make check-seip
```
Needs only Python 3.8+ (standard library). `analysis/check_seip.py` recomputes every number the paper states from
`data/` and prints PASS or FAIL with the paper location of each number.

To regenerate the static-analysis summaries from the raw reports in `data/static_reports/`:
```
python3 scripts/import_s1_reports.py
```
The corpus plugins are third-party code and are not redistributed here; `data/plugins.csv` lists them.
