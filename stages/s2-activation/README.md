# Stage 2: plugin-aware activation

**Slot for:** the activation tool (search-based program generation), kept in its own repository.

## Input
- Plugin build, plugin arguments, `Cand` records from Stage 1 (optional).
- Seed programs and the activation condition of the plugin (what makes it act).

## What the stage does
Genetic programming over C programs. Population 100, 100 generations, tournament
size 3, crossover probability 0.8. Fitness uses **plugin-scoped** coverage, not
whole-compiler coverage. Failures (crash, assertion, diagnostics) are deduplicated.

## Output
- `s2_coverage.csv` : per plugin, baseline and evolved plugin line coverage.
- `s2_failures.jsonl` : one `Failure` per deduplicated failure, with minimised program.
- `tests/<plugin>/*.c` : the evolved programs. Stage 3 selects its inputs from here
  when the plugin is eligible for both dynamic stages.

## Eligibility
A plugin enters Stage 2 only if it has an input-dependent activation problem and can
be built, loaded and run reproducibly. Reasons for non-entry use the codes in
`data/exclusion_reasons.csv`.

## Reproduce the paper numbers from this stage
Raw per-run activation outputs are **not** in this archive yet (TODO).
`data/plugins.csv` holds the per-plugin coverage and failure counts used by the paper.
