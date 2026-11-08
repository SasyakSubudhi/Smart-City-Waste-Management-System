# Day 3 validation and test case update

8 November 2026; Shreya (`yasho-26singh`).
Baseline main: 532c1919f33622f2628e46a6c10e67b0b6d55822.
Scope: alerts added to existing bins/routing. This is not the final Part-3
system validation or final-main coverage report.

Environment: Windows, Python 3.13.7, pytest 9.1.1, pytest-cov 7.1.0,
coverage 7.17.2. Command: `python -m pytest --cov --cov-branch
--cov-report=term-missing --cov-report=json:../day3-coverage.json
--junitxml=../day3-tests.xml` from repository root.

Observed: 68 passed in 0.55 seconds. Statements 116/116 (100%);
branch outcomes 44/44 (100%); independently exceed 80%. Alerts alone:
18/18 statements and 4/4 branch outcomes. Timings are environment-specific.
12 new alert test instances; 56 existing regression instances. CI is separate
live PR evidence. No report-module or browser test result is claimed.

| ID / pytest name prefix | Setup/action | Expected and observed (passed) |
|---|---|---|
| TC-AL-01 / test_tc_al_01 | Empty list and OK bin at 69 | Empty alerts |
| TC-AL-02 / test_tc_al_02 | Levels 0,69,70,89,90,100 | None,None,WARNING,WARNING,CRITICAL,CRITICAL |
| TC-AL-03 / test_tc_al_03 | Interleaved severities and OK | Critical first, stable ties, no mutation |
| TC-AL-04 / test_tc_al_04 | Warning at 70 and critical at 100 | Exact ID, location, percentage and severity text |
| TC-AL-05 / test_tc_al_05 | 69 -> 70 -> 90 -> empty | Fresh severity; old snapshot unchanged/frozen; alert cleared |
| TC-AL-06 / test_tc_al_06 | Registry -> alerts -> one-bin route -> complete | Only selected alert clears; backlog alert and OK reading preserved |

FR-4 maps to TC-AL-01..06. TC-AL-06 also exercises FR-5/6/7 integration.
Full SYS-01/02 remain pending report integration. Full final Test Case Document,
Unit Test Report, System Validation Report, Code Coverage Report and Branch
Coverage Report are Day 4/final-main deliverables; regenerate them after merging
all features. Never reuse kit coverage totals as final evidence.
