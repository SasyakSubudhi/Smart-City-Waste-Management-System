"""Run the real test suite and write the four test reports into docs/.

Usage:  python generate_reports.py   (from the repository root)
Needs:  pip install -r requirements.txt

Reports record the git commit, date, platform and the actual result. If any test fails
or a coverage metric is below the target, the reports say FAIL and this script exits 1.
"""

import datetime
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
TARGET = 80.0  # percent, statements and branches each


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def git_commit():
    r = run(["git", "rev-parse", "--short", "HEAD"])
    commit = r.stdout.strip() if r.returncode == 0 else "unknown"
    dirty = run(["git", "status", "--porcelain", "--", "src", "tests"]).stdout.strip()
    return commit + (" (+ uncommitted source/test changes)" if dirty else "")


def header(title):
    return (
        f"# {title}\n\nProject: Smart City Waste Management System  \n"
        f"Date: {datetime.date.today().isoformat()}  \nCommit: {git_commit()}  \n"
        f"Environment: Python {platform.python_version()} on {platform.system()} {platform.release()}  \n"
    )


def run_pytest(args, junit):
    cmd = [sys.executable, "-m", "pytest", *args, f"--junitxml={junit}", "-q", "-p", "no:cacheprovider"]
    proc = run(cmd)
    if not (ROOT / junit).exists():
        sys.exit(f"pytest produced no results for {args}:\n{proc.stdout}\n{proc.stderr}")
    return proc


def parse_junit(path):
    root = ET.parse(path).getroot()
    rows = []
    for tc in root.iter("testcase"):
        status = "PASS"
        if tc.find("failure") is not None or tc.find("error") is not None:
            status = "FAIL"
        elif tc.find("skipped") is not None:
            status = "SKIP"
        rows.append((tc.get("classname").split(".")[-1], tc.get("name"), status, float(tc.get("time"))))
    return rows


def table(rows):
    out = ["| # | Test file | Test case | Result | Time (s) |", "|---|---|---|---|---|"]
    for i, (f, n, s, t) in enumerate(rows, 1):
        out.append(f"| {i} | {f}.py | `{n}` | {s} | {t:.3f} |")
    return "\n".join(out)


def counts(rows):
    return len(rows), sum(r[2] == "PASS" for r in rows), sum(r[2] == "FAIL" for r in rows)


def rate(p, n):
    return "n/a" if n == 0 else f"{100 * p / n:.1f}%"


def verdict(ok):
    return "PASS" if ok else "FAIL"


def main():
    # 1. Unit tests (everything except the system journeys)
    run_pytest(["tests", "--ignore=tests/test_system.py"], "unit.xml")
    unit = parse_junit(ROOT / "unit.xml")
    n, p, f = counts(unit)
    unit_ok = n > 0 and f == 0
    (DOCS / "Unit_Test_Report.md").write_text(
        header("Unit Test Report") + f"Tool: pytest\n\n**Overall: {verdict(unit_ok)}**\n\n## Summary\n\n"
        f"| Total | Passed | Failed | Pass rate |\n|---|---|---|---|\n| {n} | {p} | {f} | {rate(p, n)} |\n\n"
        f"## Results\n\n{table(unit)}\n"
    )

    # 2. System validation (end-to-end journeys)
    run_pytest(["tests/test_system.py"], "system.xml")
    system = parse_junit(ROOT / "system.xml")
    n2, p2, f2 = counts(system)
    sys_ok = n2 > 0 and f2 == 0
    (DOCS / "System_Validation_Report.md").write_text(
        header("System Validation Report")
        + f"Tool: pytest (end-to-end scenarios in `tests/test_system.py`, one per STP scenario SYS-01..SYS-04)\n\n"
        f"**Overall: {verdict(sys_ok)}**\n\n## Summary\n\n"
        f"| Scenarios | Passed | Failed | Pass rate |\n|---|---|---|---|\n| {n2} | {p2} | {f2} | {rate(p2, n2)} |\n\n"
        f"## Scenario results\n\n{table(system)}\n\n"
        "Each scenario's docstring names the SRS requirements it validates. These are automated package-level "
        "tests; no UI exists, so no browser validation was performed.\n"
    )

    # 3 & 4. Coverage (full suite). Statements and branches are checked separately.
    run([sys.executable, "-m", "pytest", "--cov", "--cov-branch", "--cov-report=json:cov.json",
         "--cov-report=html:docs/coverage_html", "-q", "-p", "no:cacheprovider"])
    cov = json.loads((ROOT / "cov.json").read_text())
    t = cov["totals"]
    stmt_pct = t["percent_statements_covered"]
    nb = t["num_branches"]
    br_pct = 100.0 if nb == 0 else 100 * t["covered_branches"] / nb
    stmt_ok, br_ok = stmt_pct >= TARGET, br_pct >= TARGET

    rows = ["| File | Statements | Missed | Statement coverage |", "|---|---|---|---|"]
    brows = ["| File | Branches | Covered | Missed | Branch coverage |", "|---|---|---|---|---|"]
    for name, d in sorted(cov["files"].items()):
        s = d["summary"]
        rows.append(f"| {name} | {s['num_statements']} | {s['missing_lines']} | {s['percent_statements_covered']:.1f}% |")
        fb = s["num_branches"]
        pct = 100.0 if fb == 0 else 100 * s["covered_branches"] / fb
        brows.append(f"| {name} | {fb} | {s['covered_branches']} | {s['missing_branches']} | {pct:.1f}% |")

    (DOCS / "Code_Coverage_Report.md").write_text(
        header("Code Coverage Report (Statement Coverage)")
        + f"Tool: coverage.py via pytest-cov\n\n**Target: {TARGET:.0f}% - {verdict(stmt_ok)}**\n\n"
        f"**Overall: {stmt_pct:.1f}%** ({t['covered_lines']} of {t['num_statements']} statements executed)\n\n"
        + "\n".join(rows)
        + "\n\nA browsable HTML version is in `docs/coverage_html/index.html`. Coverage shows which code ran, "
        "not that every requirement is correct.\n"
    )
    (DOCS / "Branch_Coverage_Report.md").write_text(
        header("Branch Coverage Report")
        + f"Tool: coverage.py (`branch = True`) via pytest-cov\n\n**Target: {TARGET:.0f}% - {verdict(br_ok)}**\n\n"
        f"**Overall: {br_pct:.1f}%** ({t['covered_branches']} of {nb} branch outcomes taken)\n\n"
        + "\n".join(brows)
        + "\n\nA branch is each True/False outcome of an `if`, loop or conditional expression.\n"
    )

    for tmp in ("unit.xml", "system.xml", "cov.json", ".coverage"):
        (ROOT / tmp).unlink(missing_ok=True)

    ok = unit_ok and sys_ok and stmt_ok and br_ok
    print(f"Unit: {p}/{n} passed | System: {p2}/{n2} passed | Statement {stmt_pct:.1f}% | Branch {br_pct:.1f}%")
    print("RESULT:", "PASS" if ok else "FAIL (see reports)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
