"""Generate a complete, deterministic catalog of pytest functions from tests/.

Each function is one logical case; pytest parameterization can yield multiple
executed instances. Execution counts must come from JUnit, not this catalog.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQ = {"BIN": "FR-1..3", "RT": "FR-5..7", "AL": "FR-4", "RP": "FR-8", "SYS": "FR-1..7", "UI": "FR-1..8"}
MODULES = ("bins", "routing", "alerts", "reports", "system", "dashboard", "app", "demo", "smoke", "generate_reports")


def generate():
    lines = [
        "# Test Case Document", "", "**Project:** Smart City Waste Management System", "",
        "This is a static catalog of pytest test functions, not an execution report. "
        "Parametrized functions can generate multiple JUnit test instances. "
        "Use the final run's JUnit XML for collected/executed counts and results.", "",
        "| Test ID | Module | Description | Requirement | Type | Automated in |",
        "|---|---|---|---|---|---|",
    ]
    seen = set()
    for module in MODULES:
        path = ROOT / "tests" / f"test_{module}.py"
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for fn in tree.body:
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or not fn.name.startswith("test_"):
                continue
            parts = fn.name.split("_")
            if len(parts) >= 4 and parts[1] == "tc":
                case_id = "-".join(parts[1:4]).upper()
                description = " ".join(parts[4:])
                group = parts[2].upper()
            elif len(parts) >= 3 and parts[1] == "sys":
                case_id = "-".join(parts[1:3]).upper()
                description = " ".join(parts[3:])
                group = "SYS"
            else:
                case_id = f"AUTO-{module.upper().replace('_', '-')}-{fn.name[5:].upper().replace('_', '-')}"
                description = " ".join(parts[1:])
                group = "OTHER"
            if case_id in seen:
                raise ValueError(f"Duplicate test case ID: {case_id}")
            seen.add(case_id)
            kind = ("Streamlit AppTest" if module == "app" else
                    "System" if module == "system" else
                    "Support / smoke" if module in ("demo", "smoke", "generate_reports") else "Unit")
            requirement = REQ.get(group, "Tooling / smoke (not mapped to FR)")
            lines.append(f"| {case_id} | {module} | {description.capitalize()} | {requirement} | {kind} | `{path.name}::{fn.name}` |")
    lines += ["", "## Scope and interpretation", "",
              "- Routing TC-RT-13–19 test validation, assignment invariants, backlog, and **per-route** atomic completion; they do not establish a fleet-wide transaction.",
              "- TC-UI dashboard helper tests and Streamlit AppTest cases are distinct. AppTest is not a real-browser compatibility test.",
              "- Demo, smoke, and report-generator tests are explicitly cataloged with AUTO IDs, not silently omitted.",
              "- Root `app.py` and `demo.py` are outside configured `src/waste_mgmt` package coverage.",
              "- Python 3.10/3.11 Windows compatibility evidence is domain-only; it does not prove Streamlit UI compatibility.",
              "- The original ten-second full-suite target remains unmet absent new accepted evidence or requirement change.", ""]
    output = ROOT / "docs" / "Test_Case_Document.md"
    output.parent.mkdir(exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


if __name__ == "__main__":
    print(f"Wrote {generate()}")
