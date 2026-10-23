# Reproducing

## Level 1: paper numbers (minutes, no GCC)
```
make check-seip
```
`check_seip.py` prints PASS or FAIL with the paper location of each number.

## Level 2: rerun a stage on one plugin
Requires the stage tool in its slot and the toolchain: GCC 13.3 (x86-64) for triage, GCC 10 to 14
for differential verification, Cppcheck 2.13.0 for static analysis.
```
pipeline/run_pipeline.sh --plugin SecRetAddress --stages s4
```

## Level 3: full pipeline
Needs all four tools, the corpus under `corpus/` and several hours. Genetic programming is stochastic;
seeds, compiler versions, plugin commits and flags are recorded per run.
The corpus plugins are third-party code and are not redistributed here; `data/plugins.csv` lists them.
