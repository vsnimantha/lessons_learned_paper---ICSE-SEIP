# Stage 1: Static Analysis of GCC Plugins

**Full-corpus sweep, per-case adjudication, developer confirmation, configuration sensitivity, and open items**

Static analysis (Cppcheck 2.13.0 and `g++ -Wall -Wextra -fsyntax-only`) was applied to all 25 plugins in the corpus. Findings are treated as **candidates requiring adjudication, not confirmed bugs**. Where possible, adjudicated findings were submitted to the original plugin developer (Section 6). Exposure labels were then fixed from the full plugin source and each plugin's makefile (Section 1.4). Analysis failures are reported as an explicit coverage limitation, never as a silent pass. A configuration sensitivity run (Section 7) tests whether the low-customisation baseline understates what the tools can do. This report is aligned with the paper: completion is counted per in-scope file, and the terminology matches the paper's Section 2.2.

---

## 1. Summary

### 1.1 Complete sweep (all 25 plugins)

Repository-directory names are retained in this report. Where the paper uses a shortened subject name, the corresponding paper name appears in parentheses or in the subject inventory. The table below is the primary, low-customisation baseline. Section 7 gives the sensitivity rerun.

| # | Plugin | Completion | Signal | HS |
|---|--------|------------|--------|:--:|
| 1 | 01_first | Complete | Clean | 0 |
| 2 | 02_help_version | Complete | High \* | 1 |
| 3 | 03_parameters | Complete | Clean | 0 |
| 4 | 04_callbacks | Complete | Low | 0 |
| 5 | 05_my_first_pass | Complete | Low | 0 |
| 6 | CTraps-gcc-master (CTraps) | Partial | **High** | 5 |
| 7 | Compiler (static_analyser) | Partial | **High** | 1 |
| 8 | KayrebtCallgraphs_gcc-plugin (KayrebtCallgraphs) | Partial | No HS | 0 |
| 9 | SecRetAddress | Complete | Low | 0 |
| 10 | arm_ssp | Failed | None | 0 |
| 11 | cfed_plugin | Partial | **High** | 3 |
| 12 | cprintf | Complete | Low | 0 |
| 13 | dfed_plugin | Partial | **High** | 5 |
| 14 | funcp-encrypt | Partial | No HS | 0 |
| 15 | gcc-jump-master | Partial | **High** | 1 |
| 16 | gcc-plugins-for-oi | Partial | No HS | 0 |
| 17 | gcc-python-plugin-master (gcc-python-plugin) | Partial | No HS | 0 |
| 18 | gcc_assert_introspect | Partial | No HS | 0 |
| 19 | instrument-attribute | Partial | No HS | 0 |
| 20 | latent_entropy | Partial | No HS | 0 |
| 21 | randomize_layout | Partial | No HS | 0 |
| 22 | reftrack-plugin | Complete | **High** \* | 2 |
| 23 | sancov | Partial | No HS | 0 |
| 24 | stack_leak | Partial | No HS | 0 |
| 25 | struck_Leak (structleak) | Partial | No HS | 0 |

\* One high-signal report from `02_help_version` (`test.c`) and one from `reftrack-plugin` (`testcases/cycle.c`) are in test code and were excluded during adjudication (Section 4). Failures confined to out-of-scope test code do not change a plugin's completion category, so `reftrack-plugin` remains Complete.

### 1.2 Outcome distribution

| Completion | Count | Meaning |
|------------|:-----:|---------|
| Complete | 8 (32%) | both tools terminated over every in-scope file |
| Partial | 16 (64%) | at least one tool or in-scope file could not be completed |
| Failed | 1 (4%) | neither tool produced meaningful source-level output |

**Coverage finding:** both tools completed their configured processing for **8 of 25 plugins (32%)**. The plugin-level label is recomputed from per-file outcomes: a subject counts as Partial whenever `g++` fails on any in-scope file, even if the subject produced a high-signal report (`CTraps`, `cfed_plugin`, `dfed_plugin`, `gcc-jump-master`). The earlier driver label marked a subject partial only when a whole tool failed, which overstated completion (13 of 25, 52%). Failures came from missing project headers, GCC-internal headers absent from GCC 13, target-specific identifiers on an x86 host, and, for Cppcheck, C++ sources parsed as C because the driver did not force the language. This is a property of the configured runs, not of the tools' best achievable coverage. The sensitivity run (Section 7) quantifies part of that gap: forcing C++ for Cppcheck raises complete subjects from 8 to 12 without changing the high-signal reports.

### 1.3 Case tally (defects and risks)

Every retained in-scope case is classified as either a **defect** or a **risk** for which the available evidence does not establish a current violation. No retained in-scope case was dismissed as a definite tool false positive, but this is not a precision estimate: the subset was chosen for its close relationship to language-level correctness.

| Category | Count |
|----------|:-----:|
| Defects matching a previously reproduced failure | 1 |
| Defects with no reproduced failure | 10 |
| Risks | 2 |
| **Total cases (high-signal)** | **13** |

The 18 raw high-signal reports (16 Cppcheck, 2 `g++`, none reported by both) reduce to 16 in scope after excluding 2 test-code reports, and to 13 cases after merging 3 pairs of Cppcheck diagnostics on the same line. Eleven cases were reported only by Cppcheck and two only by `g++` (`fprintf2` and the CTraps wrapper).

### 1.4 Exposure (present execution context)

Exposure does not change a case's status as a defect or a risk. It records the strongest available evidence about whether the case is reached. Categories are nominal, not a severity scale. The labels below were decided primarily from full-source inspection, including handlers, reads and assignments, callers, registrations, and makefiles. No plugins were executed specifically for this static-analysis study. The `fprintf2` manifested label and the `upD` differential observations come from preceding dynamic investigations.

| Exposure | Status | Count | Cases |
|----------|--------|:-----:|-------|
| Manifested | Defect | 1 | static_analyser `fprintf2` |
| Live | Defect | 0 | none |
| Reachable UB | Defect | 5 | cfed and dfed dangling `msg` (x2); cfed `upD`; CTraps null-to-`%s` (x2) |
| Latent | Defect (1), Risk (1) | 2 | CTraps `thd_ctr` wrapper (defect); reftrack `cur_fn` (risk) |
| Currently uncalled | Defect | 4 | dfed `isLoad`, `selected_register2`, `selected_register`, `getUsedRegisters` |
| Unresolved | Risk | 1 | gcc-jump `ehdr` |

A currently-uncalled defect could become exposed if a future caller executes the fall-through path. Adding a caller alone would not establish that the defective branch is feasible. The two risks (`cur_fn`, `ehdr`) are not defects until a feasible invalid read is demonstrated.

One additional called missing-return defect was found by inspection but not reported by either tool: the one-argument `DFED_PLUGIN::findArgumentValue` (`DFED_Plugin.cpp:127`) discards its callee's result and reaches the end without returning a value. The wrapper is called at `DFED_Plugin.cpp:161` and `:197`. This defect is outside the 13 cases, which are tool-reported by construction, and no exposure label is assigned here.

---

## 2. Defects matching earlier investigations

Only one case matches a previously reproduced failure. The cfed and dfed dangling pointers are adjudicated defects, but no resulting failure was reproduced, so they are not counted as previously known.

### 2.1 static_analyser, missing return in `fprintf2` (previously reproduced)

- **File:** `Compiler/unit.h:282`
- **Tool:** `g++` (`-Wreturn-type`) only. Cppcheck could not parse this subject, in the baseline and in every sensitivity configuration (Section 7).

```cpp
int fprintf2(FILE *stream, const char *format, ...)   // non-void
{
    if (!debugoutput) return 0;                       // the ONLY return
    va_list ap; va_start(ap, format);
    vfprintf(stream, format, ap); va_end(ap); fflush(fp);
}                                                     // falls off end
```

When `debugoutput` is true, control reaches the end of a non-void function without returning a value, causing undefined behaviour. At `-O0`, this manifested as the confirmed static_analyser SIGILL crash. **Exposure: manifested.**

### 2.2 Known failures that static analysis did not find

`cprintf` (unchecked `gimple_call_arg` index in `build_spec_function`, `gcc_hell.cpp:309`) and `SecRetAddress` (`single_pred` on an exit block with several predecessors, `plugin.cpp:153`) were previously reproduced as segmentation faults. Neither tool reported them; their low-signal reports were unrelated. The sweep therefore rediscovered **1 of 3** previously known failures. Both subjects are Complete in the baseline and in the sensitivity run, and the corrected configuration reports nothing more for them, so this blind spot is not a parsing artefact.

---

## 3. Defects and risks from this sweep

### 3.1 dfed_plugin, dangling pointer to local `msg` (reachable UB)

- **File:** `DFED_Plugin.cpp:148`
- **Tool:** Cppcheck (`returnDanglingLifetime`)

```cpp
char msg[1024];
snprintf(msg, 1024, "Argument %s not found!\n...", key, "...");
throw (const char*) msg;
```

The pointer is invalid once the frame unwinds. Two of the three handlers of this pointer type read it: the handler in the plugin entry function and the one in `implementDetectionTechnique` both print it with `%s`. The third handler, around the function-name lookup, discards it. Both plugins are built as `gnu++14` with exceptions enabled. **Developer feedback (Section 6):** the error path is triggered and the construction is unsafe; observed behaviour does not establish safe lifetime handling. **Exposure: reachable UB**, based on source inspection. The plugins were not run specifically for this study, and stale storage may still appear to hold the message in some executions.

### 3.2 cfed_plugin, dangling pointer to local `msg` (reachable UB)

- **File:** `CFED_Plugin.cpp:145`
- **Tool:** Cppcheck (`returnDanglingLifetime`)

The pattern is identical because the two plugins share this argument-handling code. The handlers in `plugin_init` (line 121) and `implementDetectionTechnique` (line 197) print the expired buffer. **Exposure: reachable UB.**

### 3.3 dfed_plugin, missing return in `isLoad` (currently uncalled)

- **File:** `InstrType.cpp:362`
- **Tool:** Cppcheck (`missingReturn`)

```cpp
bool InstrType::isLoad(rtx_insn* expr) {
    if (INSN_P(expr)) {
        rtx set = XEXP(expr, 3);
        if (XEXP(set, 0)->code == REG) {
            if (findCode(XEXP(set, 1), MEM)) { return true; }
            // If this path executes, control reaches
            // the end without returning a value.
        } else { return false; }
    } else { return false; }
}
```

If the `INSN_P && REG && !findCode` path executes, control reaches the end of the `bool` function without returning a value. **Source status: defect.** A search of the whole `dfed_plugin` tree finds only the declaration (`InstrType.h:43`) and the definition; there is no call, address use, or registration, and the source comment says the function is "not yet tested." **Exposure: currently uncalled.**

**Conflict to resolve:** the developer said the function is called. This report follows the inspected source. The developer may have meant another function (`isLoadMultipleWritebackSP` is called) or a different version. If a call site is found, exposure must be reassessed; invocation alone would not establish execution of the defective branch.

### 3.4 cfed_plugin, uninitialised value `CFCSSpath.upD` (reachable UB)

- **File:** `CFCSS.cpp:296` (declaration), struct in `structsHolder.h:21`
- **Tool:** Cppcheck (`uninitvar`, `uninitStructMember`)

```cpp
struct CFCSSpath {
    unsigned int startBBId;
    unsigned int endBBId;
    unsigned int upD;
};

CFCSSpath path;
path.startBBId = idBB;
path.endBBId = idSuccs;       // upD left uninitialised

if (predIds.size() > 1) {
    // ...
    (*it).upD = upD;          // assigned only on some paths
}
```

`upD` is assigned (`CFCSS.cpp:254`) only for edges into blocks with more than one predecessor and only for non-primary predecessors. `insertEnd` reads `(*it).upD` for every edge leaving a block (lines 117, 120, 149) and emits it with `emitMovRegInt`, so edges into single-predecessor blocks are read without any assignment.

Preceding differential runs produced stable, small emitted values across builds, but stability does not establish correct initialisation. The specific unassigned read was not independently confirmed through a new instrumented execution for this study. **Developer feedback (Section 6):** the code relies on an unguaranteed zero default. **Exposure: reachable UB**, based on the source-level def-use path.

### 3.5 reftrack-plugin, uninitialised member `cur_fn` (risk, latent)

- **File:** `reftrack.cc:1006` (constructor), member at `:1034`
- **Tool:** Cppcheck (`uninitMemberVar`)

```cpp
reftrack_pass(gcc::context *ctx)
    : gimple_opt_pass(reftrack_data, ctx) { }

function *cur_fn;  // set later in init()
```

This is a risk, not a proven defect: `init()` is the first statement of `instrument_gseq`, so `cur_fn` is assigned before it is read on the observed control flow. Initialising the member in the constructor would still reduce reliance on the current assignment order. **Exposure: latent.**

### 3.6 gcc-jump, uninitialised member `ehdr` (risk, unresolved)

- **File:** `elf.cpp:46` (constructor), member `ehdr` at `:55`
- **Tool:** Cppcheck (`uninitMemberVar`)

```cpp
elf_file() : fp(NULL), byte_get(NULL) { }  // ehdr not initialised

elf_internal_ehdr ehdr;                    // filled later by fread (:408)
```

`ehdr` is populated by `fread` before its observed reads (`file->ehdr.*` at line 318 onward). Behaviour after a failed or partial file read has not been established, so the case remains unresolved. **Developer confirmation pending; different author.**

### 3.7 CTraps, null pointer passed to `%s` (x2, reachable UB)

- **Files:** `cganom_plugin.cpp:66`, `cgtest_plugin.cpp:73`
- **Tool:** Cppcheck (`nullPointer`)

```cpp
char *p = getenv("CGTEST_GRAPH");
if (p != NULL) {
    // ...
} else {
    fprintf(stderr, "Couldn't load the graph from %s\n", p);
    abort();
}
```

`getenv` may return `NULL`, and the `else` branch, reached exactly when `p == NULL`, passes that pointer to `%s`, which the C library does not guarantee to accept. This report avoids the phrase "null dereference" because no crash from this conversion was reproduced. The practical impact is limited because `abort()` follows immediately. **Exposure: reachable UB.** **Developer confirmation pending; different author.**

### 3.8 CTraps, missing return in `__call_real_pthread_create` (latent)

- **File:** `thd_ctr.c:58`
- **Tool:** `g++` (`-Wreturn-type`) only

```c
int __call_real_pthread_create(...) {
    __real_pthread_create(thread, attr, start_routine, arg);
}  // no return from a function declared int
```

The `g++` report arose because the driver analyses every `.c` file as C++, where reaching the end of a value-returning function is undefined. The plugin's own build differs: `Runtime/Makefile` compiles `%.c` files with `gcc-4.8` and `CFLAGS`, that is, as C, where reaching the end is undefined only if the caller uses the value.

The analogous sibling wrapper propagates the wrapped status, indicating that status propagation is the local implementation convention. The only current caller (`RWCalls.cpp:244`) discards the result. **Source status: defect. Exposure: latent**, because no undefined execution is currently established under the subject's C build.

---

## 4. Currently-uncalled defects and excluded test-code items

| Plugin | Candidate | Location | Verdict |
|--------|-----------|----------|---------|
| dfed_plugin | `isLoad` no return | `InstrType.cpp:362` | **Currently uncalled** in the inspected source: declaration and definition only. Conflicts with the developer statement; see Section 3.3. |
| dfed_plugin | `selected_register2` no return | `S_SWIFT_R.cpp:267` | **Currently uncalled:** no caller. Developer confirms never called. |
| dfed_plugin | `getUsedRegisters` no return | `GeneralDFED.cpp:125` | **Currently uncalled:** called only from itself. Developer confirms never called. |
| dfed_plugin | `selected_register` no return | `S_SWIFT_R.cpp:244` | **Currently uncalled:** called only from itself. Developer confirms never called. |
| 02_help_version | negative index | `test.c:49` | **Excluded:** test program, not plugin code. |
| reftrack-plugin | null dereference of `prev` | `testcases/cycle.c:47` | **Excluded:** test case, not plugin code. |

None of the four functions is virtual or referenced through a function pointer. Each function contains a source-level missing-return defect. No external entry path was found in the inspected version. A future caller could expose the defect, but the defective path would still need to execute before undefined behaviour occurred. The two excluded items are in test code and out of scope.

---

## 5. Interpretation

Across 25 plugins, both tools completed the configured processing for 8 (32%); 16 were partial and one produced no meaningful result. The tools emitted 18 high-signal reports across 7 plugins, which reduce to 13 cases: 11 defects and 2 risks. No retained case was dismissed as a definite false positive, which is not a precision estimate. The 13 cases distribute by exposure as follows:

- **1 manifested defect:** `fprintf2`, previously reproduced as a crash.
- **5 reachable-UB defects:** cfed and dfed dangling `msg` (x2), cfed `upD`, and CTraps null-to-`%s` (x2), based on source inspection.
- **1 latent defect:** CTraps `thd_ctr` wrapper, built as C with its result discarded.
- **1 latent risk:** reftrack `cur_fn`.
- **4 currently-uncalled defects:** `isLoad` and three other dfed missing returns.
- **1 unresolved risk:** gcc-jump `ehdr`.

**Mechanisms:** (1) missing return, 6 cases, all defects (`fprintf2` manifested, four currently uncalled, CTraps wrapper latent); (2) dangling pointer, 2 cases, both defects; (3) uninitialised value, 1 case, a defect (`upD`); (4) initialisation or ordering risk, 2 cases, both retained as risks (`cur_fn`, `ehdr`); and (5) null pointer passed to a string conversion, 2 cases, both defects.

**Sensitivity of these results (Section 7):** forcing C++ (S1) lifts completion to 12 complete, 13 partial, and none failed, but produces the same high-signal set. The 13 cases therefore do not depend on the language misclassification in the baseline, while the coverage limitation is only partly a configuration artefact: `g++` failures and two Cppcheck failures persist.

> **A clean or low-signal result does not mean a plugin is defect-free.**
> The tools are blind to failures caused by violated GCC API preconditions, such as the confirmed `cprintf` and `SecRetAddress` segmentation faults, both of which scanned as low signal. They also omitted the called missing-return defect in `DFED_PLUGIN::findArgumentValue` under this configuration. This stage is a useful but insufficient early filter, motivating the dynamic stages that follow it.

**Open items:**

1. Resolve the `isLoad` conflict by finding a call site or confirming with the developer which function or version was intended.
2. Obtain developer confirmation for the CTraps and gcc-jump findings from their respective authors.
3. Optionally execute the reachable-UB cases to convert feasible paths into observed failures where possible.
4. Rerun `funcp-encrypt` in the sensitivity configuration once its sources are available (they were not in the plugin folder used for Section 7), and, if desired, add a native-build run (real makefile flags and a matching GCC version) for the subjects that still fail.

---

## 6. Developer confirmation

Adjudicated cfed and dfed findings were submitted to the original plugin developer. The table records the feedback and how this report treats it.

| Finding | Location | Developer feedback | Report treatment |
|---------|----------|--------------------|------------------|
| `isLoad` missing return | `InstrType.cpp:362` | Confirmed source bug; developer states that the function is called. | Source defect accepted; the claimed call conflicts with the inspected version, so exposure remains currently uncalled pending a call site or version clarification. |
| `selected_register2` | `S_SWIFT_R.cpp:267` | Never called. | Currently uncalled. |
| `selected_register` | `S_SWIFT_R.cpp:244` | Never called. | Currently uncalled. |
| `getUsedRegisters` | `GeneralDFED.cpp:125` | Never called. | Currently uncalled. |
| `upD` uninitialised read | `CFCSS.cpp` | Real concern; relies on an unguaranteed zero default. | Reachable UB based on the source-level def-use path. |
| dangling `msg` (cfed, dfed) | `CFED_Plugin.cpp`, `DFED_Plugin.cpp` | Error path is triggered; construction is unsafe. | Reachable UB because handlers read expired storage. |

Developer feedback covers seven cases across two related plugins and should not be treated as seven independent confirmations. Developer feedback informs interpretation of intent where available but does not define correctness. Where feedback conflicts with the inspected source, this report follows the source evidence. A defect need not be presently failing to remain a source defect; exposure labels calibrate the available execution evidence.

---

## 7. Configuration sensitivity run

**Purpose.** The baseline deliberately uses uniform, low-customisation commands. Three of its driver quirks could understate the tools: Cppcheck receives `--std=c++14` but no `--language=c++`, so C-suffixed files containing C++ syntax are parsed as C; Cppcheck receives no GCC plugin headers; and a timeout counts as failure. This run tests how much of the coverage limitation is caused by those choices, changing one factor at a time.

**Configurations.** Same Cppcheck 2.13.0 and `g++` 13.3.0 on Ubuntu 24.04, same enabled checks, same in-scope file lists, same high-signal selection rules, and completion computed per in-scope file (failures under `testcases/` ignored).

- **B0 (original baseline):** Cppcheck invoked once per subject (batch); the saved reports.
- **B1 (per-file baseline):** the baseline commands run per file. Changes only invocation granularity.
- **S1 (language fix):** B1 plus `--language=c++` for Cppcheck; `g++` additionally receives `-Wno-narrowing` and the plugin `c-family` include path. Changes only the language setting relative to B1.
- **S2 (language fix plus GCC headers):** S1 plus the GCC plugin include directories for Cppcheck; per-file timeout 300 s. Changes only the headers relative to S1.

B1, S1 and S2 were run on 24 of 25 subjects. The sources of `funcp-encrypt` were unavailable for the rerun, so it keeps its baseline label (Partial). `CTraps` was rebuilt from its archive. The archive keeps `funcp-encrypt`'s saved baseline output but not its source snapshot, which is a contained reproducibility limitation.

**Results.**

| Configuration | Complete | Partial | Failed | Cppcheck files parsed (of 124) | `g++` files parsed (of 124) |
|---------------|:--------:|:-------:|:------:|:------------------------------:|:---------------------------:|
| B0 (batch baseline) | 8 | 16 | 1 | not recorded per file | not recorded per file |
| B1 (per-file baseline) | 8 | 16 | 1 | 98 | 33 |
| S1 (language fix) | 12 | 13 | 0 | 103 | 33 |
| S2 (S1 plus GCC headers) | 8 | 15 | 2 | 92 | 33 |

Completion columns cover all 25 subjects (`funcp-encrypt` counted as Partial in every row); file counts cover the 24 rerun subjects.

**Reading the sequence.**

1. **B0 to B1: invocation granularity alone changes nothing at plugin level.** Per-file execution reproduces the 8/16/1 split and the 18 baseline high-signal reports. File-level counts can differ: for `gcc-python-plugin` the batch run treated the whole subject as failed, whereas per-file execution lets Cppcheck process 16 of 35 in-scope files in both B1 and S1.
2. **B1 to S1: forcing C++ produces the completion gain.** Five of the eight Cppcheck failures recover fully (`arm_ssp`, `latent_entropy`, `sancov`, `stack_leak`, `struck_Leak`), raising parsed in-scope files from 98 to 103 and plugin-level completion from 8/16/1 to 12/13/0. `Compiler` (a syntax error in the project header `new_imm_use.h`) and `randomize_layout` (a `#error` requiring a different GCC version) still fail. `arm_ssp` moves from Failed to Partial because `g++` still rejects the target-specific `gen_load_tp_hard` call. The 16 of 35 `gcc-python-plugin` files are not part of this gain, since they are processed identically in B1 and S1.
3. **S1 to S2: supplying GCC plugin headers to Cppcheck hurts.** Its parser rejects the headers themselves (an `internalAstError` in `value-range.h`, a `#error Unknown BITS_PER_UNIT` in `tree.h`, and macro-expansion failures), so success falls from 103 to 92 files and two subjects (`arm_ssp`, `gcc-plugins-for-oi`) end as Failed. Cppcheck also emits hundreds of reports located inside the GCC headers, which are outside plugin source and were excluded.
4. **`g++` results are unchanged.** In every configuration `g++` parses 33 of the 124 in-scope files, so its failures come from missing GCC-internal declarations, version mismatches, and target-specific identifiers rather than from the flags varied here. Fixing them requires the native build (matching GCC version and target).
5. **Blind spots persist.** `cprintf` and `SecRetAddress` stay Complete and low-signal, so the two API-precondition failures remain undetected; this is a semantic limit, not a parsing artefact.

**Report accounting.**

| Set | Count | Note |
|-----|:-----:|------|
| Baseline raw high-signal reports | 18 | reproduced by B1 |
| Test-code exclusions | 2 | `02_help_version/test.c`, `reftrack-plugin/testcases/cycle.c` |
| Baseline in-scope reports | 16 | |
| Baseline cases | 13 | after merging 3 pairs |
| Demonstration-input reports | 4 | see below; not part of the 18, so the total is not 22 |
| S2 candidates | 3 | see below |

**Four demonstration-input reports.** Per-file execution (B1) exposes four `missingReturn` reports in `demo.c` of `gcc-python-plugin`. The batch baseline could not report them: Cppcheck failed on that subject as a whole, and the driver discards all output from failed runs. `demo.c` is a demonstration input, not plugin source, so the reports are outside the plugin-source scope and alter neither the 18 baseline reports nor the 13 cases. Separately, Cppcheck cannot expand the macro providing the return (`Py_RETURN_NONE`), which makes the reports doubtful, but scope was decided by the file's role and not by that observation.

**Three S2 candidates (false alarms).** S2 adds three null-pointer reports in `gcc_assert_introspect/plugin.c` (`nullPointerRedundantCheck` at line 108, `ctunullpointer` at line 108, and `nullPointerRedundantCheck` at line 1084). They appear only when Cppcheck has the GCC headers, because only then can it expand `EXPR_LOCATION(stmt)` (`tree.h:1269`), which contains the null test `CAN_HAVE_LOCATION_P(stmt)`, that is, `((stmt) && EXPR_P (stmt))` (`tree.h:1291`). That test comes after `stmt` has already been dereferenced (`TREE_CODE(expr)` at line 108, `TREE_CODE(stmt)` at 1080, `COND_EXPR_COND(stmt)` at 1084), and every caller in `iterate_function_body` has already dereferenced its argument (`TREE_CODE(stmt)` at 1108, `TREE_CODE(body)` at 1104). A null value would therefore have failed earlier, so the reports are adjudicated as sensitivity-only false alarms, excluded from the baseline 18 reports and 13 cases. This is a single-reviewer judgement. The per-report notes are in `S2_false_alarms.md` in the replication archive.

**Conclusion for the paper.** The low-customisation baseline understates Cppcheck's parsing reach (plugin-level completion 32% versus 48% after the language fix) but not its findings. The coverage limitation is therefore partly configuration-driven and partly intrinsic to analysing plugins outside their native build. The primary results in Sections 1 to 6 remain the reported baseline, with this section as the sensitivity analysis.

---

### Legend

- **Complete:** both tools terminated over every in-scope file.
- **Partial:** a tool or in-scope file could not be completed; not to be read as clean.
- **Failed:** neither tool produced meaningful source-level output.
- **High / Low / Clean / No HS:** at least one high-signal report / low-signal diagnostics only / no retained diagnostic / no high-signal report from the analysed portion.

*Findings are candidates requiring manual adjudication. Developer feedback informs interpretation of intent where available but does not define correctness. Source excerpts have instrumentation and logging lines elided; line numbers refer to the original plugin source.*