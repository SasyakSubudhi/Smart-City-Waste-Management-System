"""Rebuild docs/Test_Case_Document.md from the test functions in tests/.

Usage: python generate_test_case_doc.py
"""
import ast
import pathlib

ROOT = pathlib.Path(__file__).parent
REQ = {"BIN": "FR-1..3", "RT": "FR-5..7", "AL": "FR-4", "RP": "FR-8", "SYS": "FR-1..7", "UI": "FR-1..8"}
lines = [
    "# Test Case Document", "",
    "**Project:** Smart City Waste Management System", "",
    "Updated after the sprints to match the implemented behaviour. Each test case is implemented in code "
    "under `tests/`; the Test ID is derived from the test function name.", "",
    "| Test ID | Module | Description | Requirement | Type | Automated in |",
    "|---|---|---|---|---|---|",
]
for m in ("bins", "routing", "alerts", "reports", "system", "dashboard", "app"):
    p = ROOT / "tests" / f"test_{m}.py"
    if not p.exists():
        continue
    for fn in ast.parse(p.read_text()).body:
        if not (isinstance(fn, ast.FunctionDef) and fn.name.startswith("test_")):
            continue
        parts = fn.name.split("_")
        if parts[1] == "tc":
            tid, desc = "-".join(parts[1:4]).upper(), " ".join(parts[4:])
            group = parts[2].upper()
        else:
            tid, desc = "-".join(parts[1:3]).upper(), " ".join(parts[3:])
            group = "SYS"
        typ = "UI" if m == "app" else ("System" if m == "system" else "Unit")
        lines.append(f"| {tid} | {m} | {desc.capitalize()} | {REQ[group]} | {typ} | `{p.name}::{fn.name}` |")
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs" / "Test_Case_Document.md").write_text("\n".join(lines) + "\n")
print("Wrote docs/Test_Case_Document.md")
