import time
import datetime
import json
import platform
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

TARGET = 80.0


def run(cmd):
    return subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True
    )


def git_commit():
    result = run(["git", "rev-parse", "--short", "HEAD"])
    commit = result.stdout.strip() if result.returncode == 0 else "unknown"

    dirty = run(
        ["git", "status", "--porcelain", "--", "src", "tests"]
    )
    if dirty.returncode == 0 and dirty.stdout.strip():
        commit += " (+ uncommitted source/test changes)"

    return commit


def header(title):
    return (
        f"# {title}\n\n"
        "Project: Smart City Waste Management System\n\n"
        f"Date: {datetime.date.today().isoformat()}\n\n"
        f"Commit: {git_commit()}\n\n"
        f"Environment: Python {platform.python_version()} "
        f"on {platform.system()} {platform.release()}\n\n"
    )

def parse_junit(path):
    root = ET.parse(path).getroot()
    rows = []

    for tc in root.iter("testcase"):
        status = "PASS"

        if tc.find("failure") is not None or tc.find("error") is not None:
            status = "FAIL"
        elif tc.find("skipped") is not None:
            status = "SKIP"

        classname = tc.get("classname") or "unknown"
        name = tc.get("name") or "unnamed"
        duration = float(tc.get("time") or 0)

        rows.append((
            classname.split(".")[-1],
            name,
            status,
            duration
        ))

    return rows


def run_pytest(args, junit):
    output = ROOT / junit

    # Never allow an earlier run's XML to be reused.
    output.unlink(missing_ok=True)

    cmd = [
        sys.executable, "-m", "pytest",
        *args,
        f"--junitxml={junit}",
        "-q",
        "-p", "no:cacheprovider"
    ]

    proc = run(cmd)
    errors = []

    if proc.returncode != 0:
        errors.append(
            f"pytest exited with status {proc.returncode}"
        )

    if not output.is_file():
        errors.append("pytest did not produce a JUnit XML report")
        rows = []
    else:
        try:
            rows = parse_junit(output)
        except (ET.ParseError, OSError, ValueError) as exc:
            errors.append(f"Could not parse JUnit XML: {exc}")
            rows = []

    if not rows:
        errors.append("No test cases were recorded")

    return rows, proc, errors


def table(rows):
    result = [
        "| # | Test file | Test case | Result | Time (s) |",
        "|---|---|---|---|---|"
    ]

    for i, (filename, name, status, duration) in enumerate(rows, 1):
        result.append(
            f"| {i} | {filename}.py | `{name}` | "
            f"{status} | {duration:.3f} |"
        )

    return "\n".join(result)


def counts(rows):
    return (
        len(rows),
        sum(row[2] == "PASS" for row in rows),
        sum(row[2] == "FAIL" for row in rows),
        sum(row[2] == "SKIP" for row in rows)
    )


def rate(passed, total):
    return "n/a" if total == 0 else f"{100 * passed / total:.1f}%"


def verdict(ok):
    return "PASS" if ok else "FAIL"


def diagnostic_text(proc, errors):
    parts = []

    if errors:
        parts.append("Problems:\n" + "\n".join(
            f"- {error}" for error in errors
        ))

    if proc.stdout:
        parts.append("Standard output:\n" + proc.stdout)

    if proc.stderr:
        parts.append("Standard error:\n" + proc.stderr)

    return "\n\n".join(parts) or "No diagnostic output."


def write_test_report(title, rows, proc, errors, system=False):
    total, passed, failed, skipped = counts(rows)
    ok = (
        proc.returncode == 0
        and total > 0
        and failed == 0
        and skipped == 0
        and not errors
    )

    summary_title = "Scenarios" if system else "Total"
    results_title = "Scenario results" if system else "Results"

    description = ""
    if system:
        description = (
            "Each scenario's docstring names the SRS requirements "
            "it validates. These are automated package-level tests; "
            "no browser validation is claimed.\n\n"
        )

    content = (
        header(title)
        + f"Tool: pytest\n\n"
        + f"**Overall: {verdict(ok)}**\n\n"
        + "## Summary\n\n"
        + f"| {summary_title} | Passed | Failed | Skipped | Pass rate |\n"
        + "|---|---|---|---|---|\n"
        + f"| {total} | {passed} | {failed} | {skipped} | "
        + f"{rate(passed, total)} |\n\n"
        + f"## {results_title}\n\n"
        + table(rows)
        + "\n\n"
        + description
    )

    if errors or proc.returncode != 0:
        content += (
            "\n## Execution diagnostics\n\n"
            "```text\n"
            + diagnostic_text(proc, errors)
            + "\n```\n"
        )

    filename = (
        "System_Validation_Report.md"
        if system else "Unit_Test_Report.md"
    )
    (DOCS / filename).write_text(content)

    return ok


def run_coverage():
    cov_json = ROOT / "cov.json"
    coverage_data = ROOT / ".coverage"
    html_dir = DOCS / "coverage_html"

    # Remove all old coverage outputs before starting.
    cov_json.unlink(missing_ok=True)
    coverage_data.unlink(missing_ok=True)
    shutil.rmtree(html_dir, ignore_errors=True)

    cmd = [
        sys.executable, "-m", "pytest",
        "--cov",
        "--cov-branch",
        "--cov-report=json:cov.json",
        "--cov-report=html:docs/coverage_html",
        "-q",
        "-p", "no:cacheprovider"
    ]

    proc = run(cmd)
    errors = []

    if proc.returncode != 0:
        errors.append(
            f"Coverage pytest command exited with status {proc.returncode}"
        )

    coverage = None

    if not cov_json.is_file():
        errors.append("Coverage command did not produce cov.json")
    else:
        try:
            coverage = json.loads(cov_json.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"Could not read coverage JSON: {exc}")

    if not html_dir.is_dir() or not (html_dir / "index.html").is_file():
        errors.append("Coverage HTML report was not generated")

    return coverage, proc, errors


def write_coverage_reports(coverage, proc, errors):
    valid = coverage is not None
    stmt_pct = 0.0
    br_pct = 0.0
    stmt_ok = False
    br_ok = False

    rows = [
        "| File | Statements | Missed | Statement coverage |",
        "|---|---|---|---|"
    ]
    brows = [
        "| File | Branches | Covered | Missed | Branch coverage |",
        "|---|---|---|---|---|"
    ]

    if valid:
        try:
            totals = coverage["totals"]
            stmt_pct = float(totals["percent_statements_covered"])
            branches = totals["num_branches"]
            covered = totals["covered_branches"]
            br_pct = 100.0 if branches == 0 else 100 * covered / branches

            stmt_ok = stmt_pct >= TARGET
            br_ok = br_pct >= TARGET

            for name, data in sorted(coverage["files"].items()):
                summary = data["summary"]
                rows.append(
                    f"| {name} | {summary['num_statements']} | "
                    f"{summary['missing_lines']} | "
                    f"{summary['percent_statements_covered']:.1f}% |"
                )

                file_branches = summary["num_branches"]
                file_covered = summary["covered_branches"]
                pct = (
                    100.0 if file_branches == 0
                    else 100 * file_covered / file_branches
                )
                brows.append(
                    f"| {name} | {file_branches} | {file_covered} | "
                    f"{summary['missing_branches']} | {pct:.1f}% |"
                )

        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"Invalid coverage data: {exc}")
            valid = False
            stmt_ok = False
            br_ok = False

    overall_ok = valid and not errors

    statement_content = (
        header("Code Coverage Report (Statement Coverage)")
        + f"Tool: coverage.py via pytest-cov\n\n"
        + f"**Target: {TARGET:.0f}% - {verdict(stmt_ok and overall_ok)}**\n\n"
        + f"**Overall: {stmt_pct:.1f}%**\n\n"
        + "\n".join(rows)
        + "\n"
    )

    branch_content = (
        header("Branch Coverage Report")
        + f"Tool: coverage.py (`branch = True`) via pytest-cov\n\n"
        + f"**Target: {TARGET:.0f}% - {verdict(br_ok and overall_ok)}**\n\n"
        + f"**Overall: {br_pct:.1f}%**\n\n"
        + "\n".join(brows)
        + "\n"
    )

    if not overall_ok:
        details = diagnostic_text(proc, errors)
        statement_content += f"\n## Execution diagnostics\n\n```text\n{details}\n```\n"
        branch_content += f"\n## Execution diagnostics\n\n```text\n{details}\n```\n"

    (DOCS / "Code_Coverage_Report.md").write_text(statement_content)
    (DOCS / "Branch_Coverage_Report.md").write_text(branch_content)

    return stmt_ok and overall_ok, br_ok and overall_ok, stmt_pct, br_pct




def append_pipeline_timing(total_time, unit_time, system_time, coverage_time):
    timing = (
        "## Execution Time\n\n"
        f"- Unit tests: {unit_time:.2f} seconds\n"
        f"- System tests: {system_time:.2f} seconds\n"
        f"- Coverage run: {coverage_time:.2f} seconds\n"
        f"- Total validation pipeline: {total_time:.2f} seconds\n"
    )

    filenames = [
        "Unit_Test_Report.md",
        "System_Validation_Report.md",
        "Code_Coverage_Report.md",
        "Branch_Coverage_Report.md",
    ]

    for filename in filenames:
        report = DOCS / filename
        if report.is_file():
            content = report.read_text()
            marker = "\n## Execution Time"
            if marker in content:
                content = content.split(marker, 1)[0]
            report.write_text(content.rstrip() + "\n\n" + timing)


def main():
    total_start = time.perf_counter()

    unit_start = time.perf_counter()
    unit_rows, unit_proc, unit_errors = run_pytest(
        ["tests", "--ignore=tests/test_system.py"],
        "unit.xml"
    )
    unit_time = time.perf_counter() - unit_start

    unit_ok = write_test_report(
        "Unit Test Report", unit_rows, unit_proc, unit_errors
    )

    system_start = time.perf_counter()
    system_rows, system_proc, system_errors = run_pytest(
        ["tests/test_system.py"],
        "system.xml"
    )
    system_time = time.perf_counter() - system_start

    system_ok = write_test_report(
        "System Validation Report",
        system_rows,
        system_proc,
        system_errors,
        system=True
    )

    coverage_start = time.perf_counter()
    coverage, cov_proc, cov_errors = run_coverage()
    coverage_time = time.perf_counter() - coverage_start

    stmt_ok, br_ok, stmt_pct, br_pct = write_coverage_reports(
        coverage, cov_proc, cov_errors
    )

    total_time = time.perf_counter() - total_start
    append_pipeline_timing(total_time, unit_time, system_time, coverage_time)
    ok = unit_ok and system_ok and stmt_ok and br_ok

    unit_total, unit_passed, _, _ = counts(unit_rows)
    sys_total, sys_passed, _, _ = counts(system_rows)

    print(
        f"Unit: {unit_passed}/{unit_total} passed ({unit_time:.2f}s) | "
        f"System: {sys_passed}/{sys_total} passed ({system_time:.2f}s) | "
        f"Coverage: {coverage_time:.2f}s | "
        f"Statement: {stmt_pct:.1f}% | Branch: {br_pct:.1f}%"
    )
    print(f"Total report generation time: {total_time:.2f}s")
    print("RESULT:", "PASS" if ok else "FAIL (see reports and evidence)")

    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
