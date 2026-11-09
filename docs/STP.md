# Software Test Plan

Project: Smart City Waste Management System  
Identifier: STP-SCWM-1.1  
Coordinator: Shriya Vasundhara Singh (`vasun26shriya`)  
Original preparation: 8 November 2026; template alignment: 9 November 2026  
Status: proposed revision; independent review and merge pending.

Provenance retained from v1.0: AI-assisted draft for team review. IEEE-style test-plan structure; no claim of formal standards certification.

## 1 Introduction

Purpose: define scope, strategy, environments, responsibilities, evidence and exit decisions for the standalone Python package. This revision follows the supplied Test_Plan_Template for SE (1).docx sections 1–15, including security validation in 5.1. It plans and records the evidence boundary; it does not sign off the whole course submission.

References: docs/SRS.md (merged SRS v2.0 on main, from PR #13), docs/SAD.md, docs/ROUTING.md, tests/, .github/workflows/ci.yml, the supplied Test Plan template, and the course checklist. Jira is not required; GitHub branches, PRs and checks supply collaboration evidence.

Definitions: FR = functional requirement; NFR = nonfunctional requirement; SR = security requirement; RTM = requirements traceability matrix; CI = continuous integration. A test ID names a scenario; parametrized pytest instances are counted separately.

## 2 Test Items

Bins and registry, alert generation/formatting, route planning/completion, and report statistics/text are the integrated test items. The dependency is the real BinRegistry interface, not the old kit dictionaries. Alerts/reports take registry.all(); routing takes the registry. Responsibility assignments are in section 9.

## 3 Features to be Tested

| Requirements | Coverage and expected outcome |
|---|---|
| FR-1 | Add/list/get/remove; duplicate IDs rejected; unknown IDs raise KeyError |
| FR-2 | Valid 0–100 readings accepted; out-of-range rejected with no silent update |
| FR-3 | 0/69 OK, 70/89 NEARLY_FULL, 90/100 FULL |
| FR-4 | WARNING for nearly full, CRITICAL for full; critical entries first |
| FR-5 | Threshold inclusive; fullest first; deterministic ties; no truck over capacity; no duplicate assignment within a plan |
| FR-6 | Fleet exhaustion and empty fleet return every unassigned due bin in priority order |
| FR-7 | Completing a route empties its bins only; missing bins cause no partial update; repeat completion is rejected |
| FR-8 | Total, average fill, counts by status and mean fill by waste type; empty average/status/report behavior has TC-RP-01/05/08 assertions |
| NFR-1 | Boundary, type and missing-entity errors are clear and preserve valid state |
| NFR-2 | Full suite's reported elapsed test time below 10 seconds; record platform and time; exclude dependency installation |
| NFR-3 | Statements and branch outcomes each at least 80% for all application modules |
| NFR-4 | Feature branches, local checks, PR, independent approval and green CI evidenced in GitHub |

Additional proposed SRS v2 requirements are covered as follows:

| Requirements | Expected outcome / evidence boundary |
|---|---|
| FR-9 / SR-2 | Invalid bin IDs, capacities and waste types are rejected during creation |
| FR-10 | Collection resets selected bin readings to zero |
| FR-11 | Status-filtered registry output contains matching bins |
| FR-12 | Alerts render the expected plain text |
| FR-13 | Invalid truck identity/capacity, duplicate trucks and non-Truck fleet entries are rejected |
| FR-14 | Threshold must be an integer in 0–100; bool, decimal, text and None are rejected |
| FR-15 / SR-3 | Reject invalid/stale routes without partial mutation; reject a repeated completion after a fresh reading |
| FR-16 | City-report text and defined empty-registry output match assertions |
| NFR-5 | Routing ties and alert order have test evidence; report-line determinism remains unverified separately |
| NFR-6 | Python 3.12 Windows CI and observed Python 3.13.7 local run; 3.10/3.11 remain untested targets |
| SR-1 | Reject malformed fill readings before storing them |
| SR-4 | Alert/report generation preserves readings |
| SR-5 | Inspect protected-main/review/check evidence; no claim that functional tests prove absence of secrets |

FR-8 empty-data behavior is implemented: empty status counts and average are zero, and the text report says No bins registered. TC-RP-01/05/08 cover these cases. Empty per-waste-type output must not be presented as a separate tested assertion unless a case actually asserts it. Section 13 maps requirements to concrete evidence.

## 4 Features Not to be Tested

Real sensors, dispatch hardware, road-distance optimization, production infrastructure, persistence and multi-user concurrency have no implementation to validate in the recorded package. No claims of city-scale load, authentication, encryption or network penetration testing are made.

The original UI request remains an open delivery requirement. The proposed Streamlit UI (PR #16) and command-line demo (PR #14) need their own integration/acceptance evidence once merged. Package tests do not validate browser interaction, accessibility or a deployed service; a display window used for recording is not the product GUI. Obtain instructor acceptance if a requested feature is omitted.

## 5 Test Approach / Strategy

Levels: isolated module tests, cross-module integration/system scenarios, full regression after accepted changes, and separately observed demo/UI acceptance. Functional and input-integrity cases are automated. The suite-time check is a bounded local observation, not a load benchmark. Browser usability/accessibility remain pending with the UI.

Entry criteria: identified source revision, installed test dependencies, isolated synthetic registry data, stable required module APIs and an environment that can collect tests. Exit criteria: all applicable planned cases executed, no unresolved required-feature defect, each coverage metric at least 80%, measured suite time below 10 seconds, and current requirement/evidence agreement. Partial NFRs and unreviewed delivery work prevent an unconditional final sign-off.

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

## 6 Test Environment

Python 3.10+ as specified in SRS; CI Python 3.12 on Windows; pytest and pytest-cov installed from requirements. Use synthetic IDs/locations and small repeatable bin fleets. Reset registries between tests. Routing capacity is measured in bin counts, not litres. No external runtime dependencies are needed.

Observed local environment: Windows, Python 3.13.7. CI configuration: Windows runner, Python 3.12. Declare each observed version rather than treating one run as proof of every supported version. Synthetic bins have fixed IDs, text locations, fill boundaries and small truck fleets; there is no live sensor, personal or production data. Do not share mutable registries between independent cases.

## 7 Test Schedule

Course targets: backlog 12 October; Sprint 1 19–23 October; Sprint 2 26–30 October; testing 2–6 November 2026. Those targets are historical and are not replaced by invented completion dates. Repository work is evidenced on 7–9 November; confirm the current submission deadline with the instructor.

As checked on 9 November: the four core modules, system cases and SRS v2.0 corrections in PR #13 are merged; demo #14, UI #16, SAD update #17 and this STP revision #18 are open. Two actual silent recordings were recorded on 9 November and merged to main in PR #15 after Shreya approved their head; merge commit 84d6bd4a4613129a335a08defe01dd0620d5325b. Recording and repository review/merge are complete. Their source is main 1344aaf; they show 86 passing tests and 100% measured coverage. Spoken narration/instructor acceptance is not claimed.

Remaining sequence: review accepted requirement changes, integrate approved source/UI/demo work, rerun regression, have the evidence owner regenerate final reports, confirm course acceptance of the merged silent recordings and freeze the agreed release. This plan does not assign completion dates for work not performed.

## 8 Test Deliverables

Version-controlled tests, updated Test Case Document, Unit Test Report, System Validation Report, Code Coverage Report and Branch Coverage Report in docs/. Generate reports from real runs, recording commit, environment, date, expected/observed results and failures. Keep machine-readable JUnit and coverage evidence as attachments/artifacts. The reports are produced by generate_reports.py and generate_test_case_doc.py from real pytest runs.

Keep defect reports in PR reviews/issues with reproduction steps, affected revision, expected versus observed behavior, owner and retest outcome. The course test-case document and four testing reports remain Shruti's evidence ownership; this revision does not regenerate them or certify their tooling. Recordings and optional sidecar captions are merged in PR #15; instructor acceptance of their silent format and recording date remains unconfirmed. Final report regeneration must follow the final accepted source, not this plan's date.

## 9 Roles and Responsibilities

| Item | Requirements | Implementation and unit-test owner |
|---|---|---|
| Bins and registry | FR-1, FR-2, FR-3 | Sasyak Subudhi |
| Route selection, assignment, completion | FR-5, FR-6, FR-7 | Shriya Vasundhara Singh |
| Alerts and their severity ordering | FR-4 | Shreya Yashodhara Singh |
| Summary statistics | FR-8 | Shruti Choudhary |
| Integration tests, final reports, manual demo | All | Shared; assign reviewer for each change |

Each author adds feature tests and runs them before pushing. Another teammate reviews each PR; the author does not approve their own PR. Owner merges only after actual approval and passing CI. This plan does not create or imply approvals.

Ownership boundary: Sasyak owns SRS/setup/bins and his correction PRs; Shriya owns routing/STP; Shreya owns alerts/SAD and the proposed UI; Shruti owns reports/system tests/final evidence. Each reviewer checks the exact latest head. Repository-owner release coordination and instructor sign-off remain separate decisions.

## 10 Risks and Mitigation

| Risk | Mitigation / unresolved boundary |
|---|---|
| Requirement/document drift across open PRs | Review this STP follow-up against merged SRS v2.0 on main and reconcile later accepted requirement changes |
| Old routing kit interface | Preserve registry/object APIs and run the integrated regression suite |
| Report evidence becomes stale | Keep tested source, actual run date/platform and exit status; evidence owner regenerates after source integration |
| Coverage mistaken for acceptance | Check each requirement's assertions and process/manual evidence, not only percentages |
| Unsupported compatibility/determinism claim | Keep report-order and untested-version gaps explicit until actual evidence is added by the responsible owner |
| Missing UI or silent format not accepted | Independently review UI delivery and confirm course recording requirements |
| Original deadlines elapsed | Ask instructor for current deadline; keep actual dates |

## 11 Assumptions & Dependencies

This revision uses the requirement IDs and corrected traceability of merged SRS v2.0 on main (PR #13). PR #13 is already merged; this STP revision preserves its SRS/deviations changes. The tests use a standalone in-memory model and trusted callers; there is no real dispatch or persistence guarantee. Source, test collection and dependencies must match the recorded evidence. Follow-up API/UI changes require affected-case review. Existing reviews and attribution are preserved; approval is never inferred from document preparation.

## 12 Suspension & Resumption Criteria

Stop acceptance testing when dependency code is missing, collection fails or environment setup prevents execution. Log the blocker and commit. Resume after the blocker is fixed and rerun affected tests plus full regression after integration. Do not label blocked/planned cases as passed.

Also suspend final sign-off when the tested revision cannot be identified or a required delivery has no evidence. Resume only after the responsible owner resolves the condition and records the actual retest. Preserve failed outputs for investigation; do not substitute stale passing reports.

## 13 Test Case Management & Traceability

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
| NFR-1 | TC-BIN-02, TC-BIN-03, TC-BIN-11, TC-BIN-12, TC-RT-07 through TC-RT-12; invalid state preserved |
| NFR-2 | Actual pytest elapsed time and platform in the tested-revision evidence |
| NFR-3 | coverage.json statement and branch counters checked separately |
| NFR-4 | Independent PR review, required successful checks and repository rules; process evidence, not a pytest case |
| NFR-5 | TC-AL-03, TC-RT-02 (alerts and routing; report-line ordering is not separately tested) |
| NFR-6 | CI Python 3.12 and observed local Python 3.13.7; Python 3.10 and 3.11 are untested |
| SR-1 | TC-BIN-03, TC-BIN-11, TC-BIN-12 |
| SR-2 | TC-BIN-02 |
| SR-3 | TC-RT-08, TC-RT-11, TC-RT-12, SYS-04 |
| SR-4 | TC-AL-03, TC-RP-09 |
| SR-5 | GitHub ruleset and pull request history |

This exceeds the course's 7–10 minimum test-case requirement. The listed automated IDs exist in `tests/`; process checks and compatibility targets are not automated test IDs. FR-9 to FR-16, NFR-5, NFR-6 and SR-1 to SR-5 refer to the merged SRS v2.0 on main (PR #13). Keep the Test Case Document synchronized with actual test names after sprint changes.

This is requirement-to-evidence planning. It does not replace case-level expected/actual records. NFR-5/6 are explicitly partial, process requirements need repository evidence, and a clean test run does not prove every planned scope item is delivered.

## 14 Test Metrics & Reporting

Report collected/executed/passed/failed/skipped/errored parametrized instances separately from unique scenario IDs. The recorded integrated baseline has 86 executed passing instances (82 unit/smoke and 4 system). Source: main 1344aaf94155af94c4832ed0a3bfc371f8ff1f63. The 9 November recording run reports 4.26 seconds on Python 3.13.7, 140/140 statements and 54/54 branch outcomes covered. See PR #15 for the actual recording and its referenced source CI run; later changes require new evidence.

Formulas: pass rate = passed/executed with skipped/not-run separately disclosed; statement coverage = covered statements/total statements; branch coverage = covered branch outcomes/total branch outcomes. If a denominator is zero, report not applicable rather than inventing a percentage. Record elapsed suite time, open defects by severity and requirement evidence gaps. Defect density/aging are not established without a maintained issue baseline; no values are invented here.

Provide execution summaries per reviewed source and a final summary after integration. Do not infer overall requirement coverage from code coverage or count all RTM rows as passing when manual/process or partial evidence remains open.

## 15 Approvals

| Role | Responsible member | Record |
|---|---|---|
| Test-plan coordinator / Day 2 author | Shriya Vasundhara Singh | Prepared revision 1.1 on 9 November 2026; not self-approval |
| Independent teammate reviewer | Requested on this follow-up PR | Pending; use actual GitHub review and exact head |
| Repository owner / release coordinator | Sasyak Subudhi | Final integration/release sign-off not claimed |
| Instructor / course acceptance | Course evaluator | Not recorded; confirm UI/deadline/recording exceptions where needed |

Routing/STP baseline PRs #3/#4 are merged. Historical review evidence remains in their PRs. This revision is a new proposal, so it does not borrow their approvals. Required CI must pass and an independent teammate must approve before this follow-up merges.
