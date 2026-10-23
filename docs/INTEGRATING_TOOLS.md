# Integrating the stage tools (separate repositories)

The tools for static analysis, activation, verification and triage are developed in their own
repositories. They are not copied into this package. To connect one:

1. Pick the slot in `tools.yaml` (`s1` to `s4`), or add an entry under `extra_tools`.
2. Add a wrapper `stages/<slot>/run.sh` that calls the tool and writes the output files named in the stage README, using the schemas in `schemas/`.
   - Option A: place the tool under `stages/<slot>/tool/`.
   - Option B: keep it elsewhere and let the wrapper read the path from `tools.private.yaml`.
3. Record the tool commit in `tools.private.yaml` (never in `tools.yaml`).
4. Run `pipeline/run_pipeline.sh --plugin NAME --stages s1`.
5. Check that the output files validate against `schemas/` and, for s3 and s4, that `make check` still passes after you replace the `data/` file with the new output.

## Mapping (kept in tools.private.yaml, not released)

| Slot | Local tool |
|---|---|
| s1 | your static-analysis tool |
| s2 | your activation tool |
| s3 | your instrumentation and differential tool |
| s4 | your triage harness |

Only the neutral ids (static, activation, verification, triage) appear in this package.
