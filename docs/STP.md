# Software Test Plan

## 1 Test plan identifier

STP-SCWM-1.0, prepared 8 November 2026. Project: Smart City Waste Management System. Responsible coordinator: Shriya Vasundhara Singh (vasun26shriya). AI-assisted draft for team review. IEEE-style test-plan structure; no claim of formal standards certification.

## 2 Introduction and references

Validate the standalone Python waste_mgmt package against FR-1 through FR-16, NFR-1 through NFR-6 and SR-1 through SR-5 in docs/SRS.md (v2.0). Bin management and the fill-level validation fix are merged in PR #1. Routing PR #3 is merged and uses that bin API. No physical sensors, dispatch hardware, shortest-path optimization, authentication or external services are in the supplied SRS scope.

## 3 Test items and responsibilities

| Item | Requirements | Implementation and unit-test owner |
|---|---|---|
| Bins and registry | FR-1, FR-2, FR-3 | Sasyak Subudhi |
| Route selection, assignment, completion | FR-5, FR-6, FR-7 | Shriya Vasundhara Singh |
| Alerts and their severity ordering | FR-4 | Shreya Yashodhara Singh |
| Summary statistics | FR-8 | Shruti Choudhary |
| Integration tests, final reports, manual demo | All | Shared; assign reviewer for each change |

Each author adds feature tests and runs them before pushing. Another teammate reviews each PR; the author does not approve their own PR. Owner merges only after actual approval and passing CI. This plan does not create or imply approvals.

## 4 Features to test and acceptance criteria

| Requirements | Coverage and expected outcome |
|---|---|
| FR-1 | Add/list/get/remove; duplicate IDs rejected; unknown IDs raise KeyError |
| FR-2 | Valid 0–100 readings accepted; out-of-range rejected with no silent update |
| FR-3 | 0/69 OK, 70/89 NEARLY_FULL, 90/100 FULL |
| FR-4 | WARNING for nearly full, CRITICAL for full; critical entries first |
| FR-5 | Threshold inclusive; fullest first; deterministic ties; no truck over capacity; no duplicate assignment within a plan |
| FR-6 | Fleet exhaustion and empty fleet return every unassigned due bin in priority order |
| FR-7 | Completing a route empties its bins only; missing bins cause no partial update; repeat completion is rejected |
| FR-8 | Total, average fill, counts by status and mean fill by waste type; define empty-data results with report-module owner |
| NFR-1 | Boundary, type and missing-entity errors are clear and preserve valid state |
| NFR-2 | Full suite's reported elapsed test time below 10 seconds; record platform and time; exclude dependency installation |
| NFR-3 | Statements and branch outcomes each at least 80% for all application modules |
| NFR-4 | Feature branches, local checks, PR, independent approval and green CI evidenced in GitHub |

## 5 Test approach

### 5.1 Security and integrity validation

Objectives: reject malformed input and prevent unintended bin-state changes. Validate routing threshold type/range, truck identity/capacity, duplicate trucks and forged duplicate/over-capacity routes. Test missing bins before completion and ensure no partial emptying; test repeated completion after a fresh reading. Restrict repository main changes through required PR review and CI. Never commit credentials or fabricate approvals. Authentication/network security testing is outside the current standalone package scope; add it if a UI or service introduces those boundaries.

Resolved dependency limitation: PR #1 is merged and fixes fill-level validation. The bin module now rejects NaN, infinity, booleans, decimals, strings and None with ValueError; out-of-range integers remain rejected. TC-BIN-11 (tc_bin_11) covers invalid readings and preservation of the existing fill level, and TC-BIN-12 (tc_bin_12) covers NaN passed to the constructor through the same validation check. This gap is fixed by the bin validation tests, not by routing tests.

### 5.2 Unit tests

Use pytest with isolated in-memory registries. Assert returned values, exact assignment order, raised errors and state before/after operations. Parameterize boundaries. No network or real sensor required. Test IDs are embedded in function names for traceability.

### 5.3 Integration and system scenarios

| ID | Steps and expected result | Execution status |
|---|---|---|
| SYS-01 | Register low/nearly/full bins; generate alerts; plan collection; complete route; regenerate report and alerts. Only selected bins empty and totals remain consistent | Automated in tests/test_system.py; passing |
| SYS-02 | Apply new reading; verify changed status, corresponding alert and routing eligibility | Automated in tests/test_system.py; passing |
| SYS-03 | Due bins exceed fleet capacity; every leftover bin appears in unassigned output, with no duplication | Automated in tests/test_system.py; passing |
| SYS-04 | Remove a bin; queries report missing; city totals exclude it; stale route completion makes no partial changes | Automated in tests/test_system.py; passing |

If a UI is introduced, add browser tests for the same journeys, keyboard use, narrow-screen layout and visible error handling. Do not equate package tests with UI validation.

### 5.4 Local and CI execution

From the repository root:

```text
python -m pip install -r requirements.txt
python -m pytest --cov --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --junitxml=unit-tests.xml --cov-fail-under=80
```

The existing GitHub Actions Windows runner uses Python 3.12. Record actual CI result per PR. The coverage gate currently combines statements and branches, so inspect coverage.json separately to verify each individual metric meets 80%. Do not claim the combined flag alone proves both gates.

### 5.5 Traceability and minimum cases

| Requirement | Test identifiers |
|---|---|
| FR-1 | TC-BIN-06 through TC-BIN-10, SYS-01, SYS-04 |
| FR-2 | TC-BIN-03, TC-BIN-11, TC-BIN-12, SYS-02 |
| FR-3 | TC-BIN-04 |
| FR-5 | TC-RT-01 through TC-RT-04, TC-RT-06, TC-RT-07, TC-RT-09, TC-RT-10 |
| FR-6 | TC-RT-05, SYS-03 |
| FR-7 | TC-RT-08, TC-RT-11, TC-RT-12, SYS-01 |
| FR-4 | TC-AL-01 through TC-AL-06, SYS-01, SYS-02 |
| FR-8 | TC-RP-01 through TC-RP-09, SYS-01, SYS-04 |
| FR-9 | TC-BIN-02 |
| FR-10 | TC-BIN-05, SYS-01 |
| FR-11 | TC-BIN-10 |
| FR-12 | TC-AL-04 |
| FR-13 | TC-RT-09, TC-RT-10 |
| FR-14 | TC-RT-07 |
| FR-15 | TC-RT-08, TC-RT-11, TC-RT-12, SYS-04 |
| FR-16 | TC-RP-05, TC-RP-06 |
| NFR-5 | TC-AL-03, TC-RT-02 (alerts and routing; report-line ordering is not separately tested) |
| NFR-6 | CI run on Python 3.12 only; Python 3.10 and 3.11 are untested |
| SR-1 | TC-BIN-03, TC-BIN-11, TC-BIN-12 |
| SR-2 | TC-BIN-02 |
| SR-3 | TC-RT-08, TC-RT-11, TC-RT-12, SYS-04 |
| SR-4 | TC-AL-03, TC-RP-09 |
| SR-5 | GitHub ruleset and pull request history |

This exceeds the course's 7–10 minimum test-case requirement. All test IDs listed here exist in `tests/`; FR-9 to FR-16, NFR-5, NFR-6 and SR-1 to SR-5 were added in SRS v2.0. Keep the Test Case Document synchronized with actual test names after sprint changes.

## 6 Features not tested

Real sensor hardware, road-distance optimization, production deployment, persistence, multi-user concurrency and authorization are not in this SRS. Performance of a real city fleet is not established by a sub-10-second unit suite. Test these only if requirements expand.

## 7 Pass and fail criteria

All applicable tests pass; no unresolved defect affecting a required feature; statements and branches each meet 80%; full suite meets the time target; acceptance scenarios and documentation agree. Any failed assertion, unhandled exception or silent state corruption fails its case. Coverage does not prove requirement completeness.

## 8 Suspension and resumption

Stop acceptance testing when dependency code is missing, collection fails or environment setup prevents execution. Log the blocker and commit. Resume after the blocker is fixed and rerun affected tests plus full regression after integration. Do not label blocked/planned cases as passed.

## 9 Test deliverables

Version-controlled tests, updated Test Case Document, Unit Test Report, System Validation Report, Code Coverage Report and Branch Coverage Report in docs/. Generate reports from real runs, recording commit, environment, date, expected/observed results and failures. Keep machine-readable JUnit and coverage evidence as attachments/artifacts. The reports are produced by generate_reports.py and generate_test_case_doc.py from real pytest runs.

## 10 Environment and data

Python 3.10+ as specified in SRS; CI Python 3.12 on Windows; pytest and pytest-cov installed from requirements. Use synthetic IDs/locations and small repeatable bin fleets. Reset registries between tests. Routing capacity is measured in bin counts, not litres. No external runtime dependencies are needed.

## 11 Schedule and risks

The original testing window (2–6 November) has elapsed. The git history shows work on 7, 8 and 9 November 2026 (see docs/DEVIATIONS.md). Merged: bins, routing, alerts, reports, SAD, STP, system tests and the four test reports. Pending: this SRS/STP update (PR #13), the demo script (PR #14), the web UI, the project backlog evidence and the two sprint videos. Remaining risks: the original request asks for a UI and none is merged yet, so this is an open deviation that needs the instructor's acceptance if the UI is not delivered; real sensor integration and road-distance routing are not implemented and are recorded in docs/DEVIATIONS.md. Python 3.10 and 3.11 have not been tested.

## 12 Review and approvals

Prepared for Shriya's review on 8 November 2026. Dependency status: PR #1 and PR #2 are merged; routing PR #3 is merged. For this STP, teammate approval: pending. Repository owner approval: pending. CI: refer to live PR checks. No approval of this STP is implied by this document.
