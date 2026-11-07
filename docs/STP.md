# Software Test Plan

## 1 Test plan identifier

STP-SCWM-1.0, prepared 8 November 2026. Project: Smart City Waste Management System. Responsible coordinator: Shriya Vasundhara Singh (vasun26shriya). AI-assisted draft for team review. IEEE-style test-plan structure; no claim of formal standards certification.

## 2 Introduction and references

Validate the standalone Python waste_mgmt package against FR-1 through FR-8 and NFR-1 through NFR-4 in docs/SRS.md, currently proposed in PR #2. Bin management is proposed in PR #1. Routing depends on that bin API. These documents and branches are pending review, so final traceability must be rechecked when they merge. No physical sensors, dispatch hardware, shortest-path optimization, authentication or external services are in the supplied SRS scope.

## 3 Test items and responsibilities

| Item | Requirements | Implementation and unit-test owner |
|---|---|---|
| Bins and registry | FR-1, FR-2, FR-3 | Sasyak Subudhi |
| Route selection, assignment, completion | FR-5, FR-6, FR-7 | Shriya Vasundhara Singh |
| Alerts and their severity ordering | FR-4 | Shreya Yashodhara Singh (yasho-26singh) |
| Summary statistics | FR-8 | Shruti Choudhary (codeninja-1234) |
| Integration tests and final reports | All | Shruti Choudhary; review by Sasyak |
| Architecture and design specification | All | Shreya Yashodhara Singh |
| Manual demo | All | Shared; each member explains their module |

Each author adds feature tests and runs them before pushing. Another teammate reviews each PR; the author does not approve their own PR. Owner merges only after actual approval and passing CI. This plan does not create or imply approvals.

Reviewer rotation from the supplied kit: Sasyak's work is reviewed by Shriya; Shriya's by Shreya; Shreya's by Shruti; Shruti's by Sasyak. See SHREYA_HANDOFF.md for the actual routing interface and integration examples. The kit's four working days are a task split, not a replacement for the course's two required sprints or evidence of their completion.

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

Known dependency limitation: the bin module's numeric checks currently allow some noninteger values despite the SRS integer assumption. Add cross-module type validation cases and report failures to its owner; do not claim this gap is closed by routing tests.

### 5.2 Unit tests

Use pytest with isolated in-memory registries. Assert returned values, exact assignment order, raised errors and state before/after operations. Parameterize boundaries. No network or real sensor required. Test IDs are embedded in function names for traceability.

### 5.3 Integration and system scenarios

| ID | Steps and expected result | Execution status |
|---|---|---|
| SYS-01 | Register low/nearly/full bins; generate alerts; plan collection; complete route; regenerate report and alerts. Only selected bins empty and totals remain consistent | Planned; alerts/reports pending |
| SYS-02 | Apply new reading; verify changed status, corresponding alert and routing eligibility | Planned; alerts pending |
| SYS-03 | Due bins exceed fleet capacity; every leftover bin appears in unassigned output, with no duplication | Routing unit coverage exists; full system case planned |
| SYS-04 | Remove a bin; queries report missing; city totals exclude it; stale route completion makes no partial changes | Routing missing-bin unit case exists; report integration planned |

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
| FR-2 | TC-BIN-03, SYS-02 |
| FR-3 | TC-BIN-04 |
| FR-4 | TC-AL-01 through TC-AL-05 (planned), SYS-01, SYS-02 |
| FR-5 | TC-RT-01 through TC-RT-04, TC-RT-06, TC-RT-07, TC-RT-09, TC-RT-10 |
| FR-6 | TC-RT-05, SYS-03 |
| FR-7 | TC-RT-08, TC-RT-11, TC-RT-12, SYS-01 |
| FR-8 | TC-RP-01 through TC-RP-06 (planned), SYS-01, SYS-04 |

This exceeds the course's 7–10 minimum test-case requirement. Planned alert/report/system IDs are commitments, not claims that tests already exist. Keep the Test Case Document synchronized with actual test names after sprint changes.

## 6 Features not tested

Real sensor hardware, road-distance optimization, production deployment, persistence, multi-user concurrency and authorization are not in this SRS. Performance of a real city fleet is not established by a sub-10-second unit suite. Test these only if requirements expand.

## 7 Pass and fail criteria

All applicable tests pass; no unresolved defect affecting a required feature; statements and branches each meet 80%; full suite meets the time target; acceptance scenarios and documentation agree. Any failed assertion, unhandled exception or silent state corruption fails its case. Coverage does not prove requirement completeness.

## 8 Suspension and resumption

Stop acceptance testing when dependency code is missing, collection fails or environment setup prevents execution. Log the blocker and commit. Resume after the blocker is fixed and rerun affected tests plus full regression after integration. Do not label blocked/planned cases as passed.

## 9 Test deliverables

Version-controlled tests, updated Test Case Document, Unit Test Report, System Validation Report, Code Coverage Report and Branch Coverage Report in docs/. Generate reports from real runs, recording commit, environment, date, expected/observed results and failures. Keep machine-readable JUnit and coverage evidence as attachments/artifacts. The README references generate_reports.py, which is not present on main; report generation remains a team task rather than an assumed working command.

## 10 Environment and data

Python 3.10+ as specified in SRS; CI Python 3.12 on Windows; pytest and pytest-cov installed from requirements. Use synthetic IDs/locations and small repeatable bin fleets. Reset registries between tests. Routing capacity is measured in bin counts, not litres. No external runtime dependencies are needed.

## 11 Schedule and risks

Record actual dates; the original 2–6 November testing window has elapsed. Finish and review dependent feature PRs, run integrated regression, execute pending system cases, then generate final reports and freeze the release. Key risks: unmerged dependencies, changing module APIs, absent alert/report implementations, undeclared type-validation gaps, missing report generator and lack of any current UI. Owners must explicitly resolve these before claiming final completion.

## 12 Review and approvals

Prepared for Shriya's review on 8 November 2026. Teammate approval: pending. Repository owner approval: pending. CI: refer to live PR checks. No approval is implied by this document.
