# Overview

One study, four stages, one corpus (25 GCC plugins).

1. **S1 static analysis**: Cppcheck and `g++ -Wall -Wextra` reports, filtered to high-signal classes.
2. **S2 activation**: genetic programming over C programs with plugin-scoped coverage.
3. **S3 differential verification**: an instrumented plugin built in 15 variants and compared with a `-g` BASE (binary and call-frame diff).
4. **S4 triage and adjudication**: a written contract per plugin decides whether flagged differences are defects.

Each stage has its own eligibility. A plugin can be eligible for activation and not for
verification and the other way round. The participation matrix (25 / 16 / 17 / 13, 3
activation only, 4 verification only, 5 static only) is in `data/plugins.csv`.

Evidence is passed as typed artifacts (`schemas/`). The final product is the merged ledger of
27 defects (`data/ledger.csv`) with the channel that found each one.
