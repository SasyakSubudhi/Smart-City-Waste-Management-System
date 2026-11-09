
import subprocess
import xml.etree.ElementTree as ET

import generate_reports as reports


def test_counts_include_skipped_tests():
    rows = [
        ("test_a", "case_1", "PASS", 0.1),
        ("test_a", "case_2", "FAIL", 0.2),
        ("test_a", "case_3", "SKIP", 0.0),
    ]

    assert reports.counts(rows) == (3, 1, 1, 1)


def test_parse_junit_detects_pass_fail_and_skip(tmp_path):
    xml = tmp_path / "results.xml"
    xml.write_text(
        """<testsuites>
        <testsuite>
            <testcase classname="tests.test_a" name="passed" time="0.1"/>
            <testcase classname="tests.test_a" name="failed" time="0.2">
                <failure message="assertion failed"/>
            </testcase>
            <testcase classname="tests.test_a" name="skipped" time="0">
                <skipped/>
            </testcase>
        </testsuite>
        </testsuites>"""
    )

    rows = reports.parse_junit(xml)

    assert [row[2] for row in rows] == ["PASS", "FAIL", "SKIP"]


def test_run_pytest_rejects_old_xml(monkeypatch, tmp_path):
    old_xml = tmp_path / "unit.xml"
    old_xml.write_text("<testsuites/>")

    monkeypatch.setattr(reports, "ROOT", tmp_path)

    def fake_run(cmd):
        assert not old_xml.exists()
        return subprocess.CompletedProcess(cmd, 1, "", "pytest failed")

    monkeypatch.setattr(reports, "run", fake_run)

    rows, proc, errors = reports.run_pytest([], "unit.xml")

    assert rows == []
    assert proc.returncode == 1
    assert errors


def test_run_pytest_rejects_invalid_xml(monkeypatch, tmp_path):
    xml = tmp_path / "unit.xml"
    monkeypatch.setattr(reports, "ROOT", tmp_path)

    def fake_run(cmd):
        xml.write_text("not valid xml")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(reports, "run", fake_run)

    rows, proc, errors = reports.run_pytest([], "unit.xml")

    assert rows == []
    assert errors


def test_skipped_tests_make_report_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(reports, "DOCS", tmp_path)
    monkeypatch.setattr(reports, "header", lambda title: "")

    rows = [("test_a", "case_1", "SKIP", 0.0)]
    proc = subprocess.CompletedProcess([], 0, "", "")

    assert not reports.write_test_report(
        "Unit Test Report", rows, proc, []
    )

    report = (tmp_path / "Unit_Test_Report.md").read_text()
    assert "SKIP" in report
    assert "FAIL" in report


def test_failed_pytest_makes_report_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(reports, "DOCS", tmp_path)
    monkeypatch.setattr(reports, "header", lambda title: "")

    rows = [("test_a", "case_1", "PASS", 0.1)]
    proc = subprocess.CompletedProcess([], 1, "", "execution failed")

    assert not reports.write_test_report(
        "Unit Test Report", rows, proc, ["pytest exited with status 1"]
    )


def test_low_coverage_fails(monkeypatch, tmp_path):
    monkeypatch.setattr(reports, "DOCS", tmp_path)
    monkeypatch.setattr(reports, "header", lambda title: "")

    coverage = {
        "totals": {
            "percent_statements_covered": 70.0,
            "num_branches": 10,
            "covered_branches": 7,
        },
        "files": {},
    }

    proc = subprocess.CompletedProcess([], 0, "", "")

    stmt_ok, branch_ok, stmt_pct, branch_pct = (
        reports.write_coverage_reports(coverage, proc, [])
    )

    assert not stmt_ok
    assert not branch_ok
    assert stmt_pct == 70.0
    assert branch_pct == 70.0


def test_failed_coverage_command_fails(monkeypatch, tmp_path):
    monkeypatch.setattr(reports, "ROOT", tmp_path)
    monkeypatch.setattr(reports, "DOCS", tmp_path / "docs")

    docs = tmp_path / "docs"
    docs.mkdir()
    (tmp_path / "cov.json").write_text('{"old": "data"}')
    (docs / "coverage_html").mkdir()
    (docs / "coverage_html" / "index.html").write_text("old")

    def fake_run(cmd):
        assert not (tmp_path / "cov.json").exists()
        assert not (docs / "coverage_html").exists()
        return subprocess.CompletedProcess(cmd, 1, "", "coverage failed")

    monkeypatch.setattr(reports, "run", fake_run)

    coverage, proc, errors = reports.run_coverage()

    assert coverage is None
    assert proc.returncode == 1
    assert errors

def test_main_returns_failure_when_unit_tests_fail(monkeypatch):
    monkeypatch.setattr(
        reports,
        "run_pytest",
        lambda args, junit: (
            [],
            subprocess.CompletedProcess([], 1, "", "failed"),
            ["pytest exited with status 1"],
        ),
    )

    monkeypatch.setattr(
        reports,
        "write_test_report",
        lambda *args, **kwargs: False,
    )

    monkeypatch.setattr(
        reports,
        "run_coverage",
        lambda: (
            None,
            subprocess.CompletedProcess([], 1, "", "failed"),
            ["coverage failed"],
        ),
    )

    monkeypatch.setattr(
        reports,
        "write_coverage_reports",
        lambda *args: (False, False, 0.0, 0.0),
    )

    assert reports.main() == 1
