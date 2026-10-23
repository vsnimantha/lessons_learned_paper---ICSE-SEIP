#!/usr/bin/env python3
"""Summarise the raw Stage 1 reports (stages/s1-static/reports/*.json) into
data/s1_reports.csv (one row per plugin) and data/s1_high_signal.csv (one row per
high-signal report). Pure standard library."""
import csv, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "stages", "s1-static", "reports")
OK = ("PARSED_CLEAN", "PARSED_WITH_FINDINGS")


def failing_files(reason):
    return [m.group(1) for m in re.finditer(r"(?:^|; )([^:;]+\.(?:c|cc|cpp|h)): ", reason or "")]


def tool_complete(tool):
    o = tool["outcome"]
    if o in OK:
        return True
    if o == "PARSED_WITH_FINDINGS_PARTIAL":
        # failures confined to out-of-scope test code do not change completion
        full = re.findall(r"(?:^|; )([^;]+?\.(?:c|cc|cpp)): (/[^ ]+)", tool.get("reason", ""))
        return bool(full) and all("/testcases/" in p for _, p in full)
    return False


def in_scope(plugin, f):
    return "/testcases/" not in f and not (plugin == "02_help_version" and f.endswith("/test.c"))


rows, hs = [], []
for path in sorted(glob.glob(os.path.join(REP, "*.json"))):
    d = json.load(open(path))
    cc, gx = d["cppcheck"], d["gxx"]
    if cc["outcome"] == "PARSE_FAILED" and gx["outcome"] == "PARSE_FAILED":
        cls = "F"
    elif tool_complete(cc) and tool_complete(gx):
        cls = "C"
    else:
        cls = "P"
    name = d["plugin"]
    rows.append({"report_plugin": name, "cppcheck_outcome": cc["outcome"], "gxx_outcome": gx["outcome"],
                 "s1_class": cls, "high_signal_raw": d["high_signal_count"],
                 "source_files": len(d["source_files"])})
    for f in d["high_signal_findings"]:
        hs.append({"report_plugin": name, "tool": f["tool"], "file": f["file"].split("/", 3)[-1] if "/" in f["file"] else f["file"],
                   "line": f["line"], "id": f["id"], "in_scope": int(in_scope(name, f["file"]))})
w = csv.DictWriter(open(os.path.join(ROOT, "data", "s1_reports.csv"), "w", newline=""), fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)
w = csv.DictWriter(open(os.path.join(ROOT, "data", "s1_high_signal.csv"), "w", newline=""), fieldnames=list(hs[0]))
w.writeheader(); w.writerows(hs)
print("wrote", len(rows), "plugins and", len(hs), "high-signal reports")
