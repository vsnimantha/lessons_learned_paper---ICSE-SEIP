#!/usr/bin/env python3
"""Recompute every number that the ICSE SEIP paper
"Loaded Is Not Activated: Lessons from Testing GCC Plugins" states from data/*.csv.

Exit status 0 only if every check passes. Each check names the paper location.
Run:  make check-seip
"""
import collections, sys
from common import read_csv, comparisons

results = []


def check(name, got, want, where):
    ok = got == want
    results.append(ok)
    print(("PASS" if ok else "FAIL"), name, "got", got, "want", want, "[" + where + "]")


def on(v):
    return v == "1"


plugins = read_csv("plugins.csv")
ledger = read_csv("ledger.csv")
findings = read_csv("findings.csv")
records = read_csv("records.csv")
verdicts = read_csv("verdicts.csv")
abugs = read_csv("activation_bugs.csv")
tmpl = read_csv("activation_templates.csv")
cost = read_csv("stage_cost.csv")
comp = comparisons(records)

# ---- Table V: corpora
check("static-analysis plugins", len(plugins), 25, "Table V")
check("activation plugins", sum(on(p["enters_s2"]) for p in plugins), 16, "Table V")
check("verification/triage plugins", sum(on(p["enters_s3"]) for p in plugins), 17, "Table V")

# ---- Table V and Episode 4: static analysis
cls = collections.Counter(p["s1_class"] for p in plugins)
check("fully / partially / not analysed", (cls["C"], cls["P"], cls["F"]), (8, 16, 1), "Table V, Episode 4")
s1hs = read_csv("s1_high_signal.csv")
check("raw high-signal reports", len(s1hs), 18, "Table V")
check("distinct plugin-source cases", sum(int(p["s1_cases"]) for p in plugins), 13, "Table V")
risk = [p for p in plugins if "Risk" in p["s4_status"]]
check("risk cases", len(risk), 2, "Table V (11 defects / 2 risks)")
check("S1-reported ledger defects", sum(on(r["s1_reported"]) for r in ledger), 11, "Table V (11 defects)")

# ---- Table V: activation
check("reproducible plugin-specific failures", sum(int(r["distinct_defects"]) for r in abugs), 7, "Table V")
check("flaggable by default warnings (activation study)",
      sum(r["static_flagged_in_activation_paper"].startswith("yes") for r in abugs), 2, "Table V")
check("reported by our static baseline",
      sum(on(r["s1_reported"]) and on(r["s2_reproduced"]) for r in ledger), 1, "Table V")
check("developer-confirmed activation defects",
      sum(1 for r in abugs if r["status_in_activation_paper"] == "developer-confirmed"), 1, "Table V")

# ---- Table V and Episode 6: triage funnel
lab = collections.Counter(r["label"] for r in comp)
check("records", len(records), 1163, "Table V")
check("comparisons", len(comp), 1035, "Episode 6")
check("baseline rows", len(records) - len(comp), 128, "Episode 6")
check("test programs", len({(r["plugin"], r["test"]) for r in records}), 69, "Table V")
check("not investigated", lab["UNLABELLED"], 15, "Episode 6")
check("runtime-confirmed benign", lab["CONFIRMED_BENIGN"], 300, "Episode 6")
check("statically discharged", lab["OPTIMISED_AWAY"], 90, "Episode 6")
check("escalated candidates", lab["LIKELY_BUG"], 630, "abstract, Episode 6")
inv = len(comp) - lab["UNLABELLED"]
check("investigated comparisons", inv, 1020, "abstract")
check("resolved automatically", lab["CONFIRMED_BENIGN"] + lab["OPTIMISED_AWAY"], 390, "abstract")
check("resolved share (%)", round(100 * 390 / inv, 1), 38.2, "Episode 6")

# ---- Table V and Case 3: adjudication
flagged = {r["plugin"] for r in comp if r["label"] == "LIKELY_BUG"}
check("flagged plugins", len(flagged), 12, "Episode 6")
examined = [v for v in verdicts if v["verdict"] != "not examined"]
flagged_verdicts = [v for v in examined if v["group"] in ("bug", "benign")]
check("flagged plugins with findings", sum(1 for v in flagged_verdicts if v["findings"]), 5, "Table V")
check("flagged plugins without findings", sum(1 for v in flagged_verdicts if not v["findings"]), 7, "Table V")
check("confirmed findings", len(findings), 15, "abstract, Table V")
check("plugins with findings (incl. audited SecRetAddress)", sum(1 for v in examined if v["findings"]), 6, "abstract")
pat = read_csv("patches.csv")
check("patched plugins", len(pat), 6, "abstract (patch per finding)")
check("findings covered by patches", sorted(f for r in pat for f in r["findings"].split(";")),
      sorted(f["finding_id"] for f in findings), "abstract")

# ---- Case 3: stackleak vs latent_entropy
sl = [r for r in comp if r["plugin"] == "stack_leak" and r["label"] == "LIKELY_BUG"]
le = [r for r in comp if r["plugin"] == "latent_entropy" and r["label"] == "LIKELY_BUG"]
check("stackleak / latent_entropy likely-bug records", (len(sl), len(le)), (60, 60), "Case 3")
tags = lambda rs: {t for r in rs for t in r["tags"].split("+") if t}
check("same three tags on both", tags(sl) & tags(le), {"COMPLEXITY_CHANGE", "INLINED_COMPLEX_LOGIC", "VOLATILE_RETURN"}, "Case 3")
# Case 4: SecRetAddress
sra = [r for r in comp if r["plugin"] == "SecRetAddress"]
check("SecRetAddress benign comparisons", sum(r["label"] == "CONFIRMED_BENIGN" for r in sra), 60, "Case 4")

# ---- Section V: complementarity (ledger is transcribed; verify against stage repositories)
chan = [on(r["s1_reported"]) + on(r["s2_reproduced"]) + on(r["s4_confirmed"]) for r in ledger]
check("ledger defects", len(ledger), 27, "Section V")
check("found by exactly one stage", sum(c == 1 for c in chan), 21, "Section V")

# ---- cost numbers
check("template authoring (min per plugin, range)", (min(int(r["authoring_minutes"]) for r in tmpl), max(int(r["authoring_minutes"]) for r in tmpl)),
      (10, 15), "Cost allocation")
s2 = {(r["stage"], r["unit"]): (r["low"], r["high"]) for r in cost}
check("CPU hours per search run", s2[("S2", "CPU hours per run")], ("24", "36"), "Cost allocation")
check("search runs per plugin", [r["note"] for r in cost if r["unit"] == "CPU hours per run"], ["five runs per plugin"], "Cost allocation")

# ---- Case 3: contract sweep (transcribed per-configuration data)
sw = read_csv("contract_sweeps.csv")
check("sweep configurations", len(sw), 15, "Case 3")
check("latent_entropy original: configurations violating the contract",
      sum(r["latent_entropy_original_instrumented"] == "no" for r in sw), 14, "Case 3")
check("latent_entropy patched: configurations violating the contract",
      sum(r["latent_entropy_patched_instrumented"] == "no" for r in sw), 0, "Case 3")
check("stackleak instrumented-function counts (2 in 5, 3 in 10)",
      sorted(collections.Counter(r["stackleak_instrumented"] for r in sw).items()), [("2", 5), ("3", 10)], "Case 3 (benign: set follows inlining)")
check("mean removed symbols, stackleak / latent_entropy (rounded)",
      (round(sum(int(r["sym_removed"]) for r in sl) / len(sl)), round(sum(int(r["sym_removed"]) for r in le) / len(le))), (19, 20), "Case 3")

print()
print("%d of %d checks passed" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
