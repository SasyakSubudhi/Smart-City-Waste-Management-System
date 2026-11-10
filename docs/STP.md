# Software Test Plan

Project: Smart City Waste Management System  
Identifier: STP-SCWM-1.3\
Coordinator: Shriya Vasundhara Singh (`vasun26shriya`)  
Original preparation: 8 November 2026; template alignment: 9 November 2026; status alignment v1.2: 9 November 2026; routing/compatibility update v1.3: 10 November 2026\
Status: v1.1 and v1.2 merged through PRs #18 and #25; v1.3 routing/compatibility follow-up independently approved and merged through PR #29 on 10 November 2026. This status-only reconciliation requires its own independent review.

Maintained test plan; approvals for merged revisions remain recorded in section 15. PR #29 approvals apply to its recorded head, not automatically to later edits. IEEE-style test-plan structure; no claim of formal standards certification.

## 1 Introduction

Purpose: define scope, strategy, environments, responsibilities, evidence and exit decisions for the Python domain package and merged Streamlit presentation layer. This revision follows the supplied Test_Plan_Template for SE (1).docx sections 1–15, including security validation in 5.1. It plans and records the evidence boundary; it does not sign off the whole course submission.

References: docs/SRS.md (SRS v2.1 merged through PR #21, following v2.0 in PR #13; its proposed performance split still awaits acceptance), docs/SAD.md, docs/ROUTING.md, tests/, .github/workflows/ci.yml, the supplied Test Plan template, and the course checklist. Jira is not required; GitHub branches, PRs and checks supply collaboration evidence.

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
| NFR-2 | Original full-suite target: below 10 seconds. Currently partial/unmet after UI integration. Record full-suite elapsed time/platform, excluding installation; a core/UI split is only proposed in SRS v2.1 and has no accepted separate UI limit |
| NFR-3 | Statements and branch outcomes each at least 80%; inspect each metric separately and disclose measured source/exclusions in section 14 |
| NFR-4 | Feature branches, local checks, PR, independent approval and green CI evidenced in GitHub |

Additional requirements from the merged SRS are covered as follows:

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
| NFR-6 | Windows domain CI observed on Python 3.10.11/3.11.9; regular CI 3.12 and local 3.13.7. Streamlit UI remains untested on 3.10/3.11; no all-platform claim |
| SR-1 | Reject malformed fill readings before storing them |
| SR-4 | Alert/report generation preserves readings |
| SR-5 | Inspect protected-main/review/check evidence; no claim that functional tests prove absence of secrets |

FR-8 empty-data behavior is implemented: empty status counts and average are zero, and the text report says No bins registered. TC-RP-01/05/08 cover these cases. Empty per-waste-type output must not be presented as a separate tested assertion unless a case actually asserts it. Section 13 maps requirements to concrete evidence.

## 4 Features Not to be Tested

Real sensors, dispatch hardware, road-distance optimization, production infrastructure, persistence and multi-user concurrency have no implementation to validate in the recorded package. No claims of city-scale load, authentication, encryption or network penetration testing are made.

The Streamlit UI is merged through PR #16, severity filtering through #22, and the command-line demo through #14. Their implementation/integration is complete; course, formal browser-usability, accessibility and production acceptance are not inferred. AppTest exercises UI behavior headlessly, while package tests alone do not validate browser layout or a deployed service. The earlier recording display aid is not the product GUI. Obtain instructor acceptance for any omitted feature or proposed requirement exception.

## 5 Test Approach / Strategy

Levels: isolated module tests, cross-module integration/system scenarios, full regression after accepted changes, and separately observed demo/UI acceptance. Functional and input-integrity cases are automated. The suite-time check is a bounded local observation, not a load benchmark. Formal browser usability, keyboard/narrow-screen evaluation and accessibility acceptance remain unverified despite the implemented UI and headless AppTest cases.

Entry criteria: identified source revision, installed test dependencies, isolated synthetic registry data, stable required module APIs and an environment that can collect tests. Exit criteria: all applicable planned cases executed, no unresolved required-feature defect, each coverage metric at least 80%, and current requirement/evidence agreement. The original below-ten-second whole-suite criterion remains unmet; final performance sign-off is blocked until an accepted requirement revision or verified improvement. A proposed core/UI split is not a passing result. Partial NFRs and unreviewed delivery work prevent an unconditional final sign-off.

### 5.1 Security and integrity validation

Objectives: reject malformed input and prevent unintended bin-state changes. Validate routing threshold type/range, truck identity/capacity, duplicate trucks and forged duplicate/over-capacity routes. Test missing bins before completion and ensure no partial emptying; test repeated completion after a fresh reading. Restrict repository main changes through required PR review and CI. Never commit credentials or fabricate approvals. The domain package has no authentication/network service. The merged Streamlit UI introduces a browser/local-server boundary, with no authentication, TLS or production-deployment validation claimed. Any broader exposure requires its own security requirements and evidence.

Routing follow-up: TC-RT-13/14 exercise malformed manual route containers and
invalid Route/Truck objects, including the previously unsafe string `"AB"` that
could be interpreted as IDs `A` and `B`. Completion must reject them before any
reading changes. TC-RT-15 verifies a non-iterable fleet gives ValueError;
TC-RT-16 preserves valid one-use and empty-generator behavior. These checks
strengthen NFR-1 and the FR-13/FR-15/SR-3 input-integrity boundary without adding
authentication, physical dispatch or changes to another member's domain module.

Resolved dependency limitation: PR #1 is merged and fixes fill-level validation. The bin module now rejects NaN, infinity, booleans, decimals, strings and None with ValueError; out-of-range integers remain rejected. TC-BIN-11 (tc_bin_11) covers invalid readings and preservation of the existing fill level, and TC-BIN-12 (tc_bin_12) covers NaN passed to the constructor through the same validation check. This gap is fixed by the bin validation tests, not by routing tests.

### 5.2 Unit tests

Use pytest with isolated in-memory registries. Assert returned values, exact assignment order, raised errors and state before/after operations. Parameterize boundaries. No network or real sensor required. Test IDs are embedded in function names for traceability.

TC-RT-17 checks three fleet configurations across every permutation of four due
bins. Assert the complete ordered partition (assigned IDs plus backlog), unique
coverage of due bins, capacity limits, omission of idle trucks and unchanged
registry order/readings. TC-RT-18 completes the second truck before the first,
then checks independent completion flags and preserved backlog. TC-RT-19 removes
the first, middle or last route bin; each failure must preserve all remaining
readings, and a retry after restoring the original bin must complete cleanly.
These are routing regressions, not a claim of a fleet-wide transaction or a
replacement for Shruti's system scenarios. Manual routes now require the declared
tuple-based bin_ids contract; planner, UI and demo already use tuples.

### 5.3 Integration and system scenarios

| ID | Steps and expected result | Execution status |
|---|---|---|
| SYS-01 | Register low/nearly/full bins; generate alerts; plan collection; complete route; regenerate report and alerts. Only selected bins empty and totals remain consistent | Automated in tests/test_system.py; passing |
| SYS-02 | Apply new reading; verify changed status, corresponding alert and routing eligibility | Automated in tests/test_system.py; passing |
| SYS-03 | Due bins exceed fleet capacity; every leftover bin appears in unassigned output, with no duplication | Automated in tests/test_system.py; passing |
| SYS-04 | Remove a bin; queries report missing; city totals exclude it; stale route completion makes no partial changes | Automated in tests/test_system.py; passing |

The merged tests/test_app.py and tests/test_dashboard.py exercise registration, errors, alerts, routes, collection, report refresh, sessions and severity filtering through AppTest/adapters. Keyboard use, narrow-screen layout and formal accessibility need separately observed evidence. Do not equate package coverage or AppTest with a live-browser/accessibility acceptance run.

### 5.4 Local and CI execution

From the repository root:

```text
python -m pip install -r requirements.txt
python -m pytest --cov --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --junitxml=unit-tests.xml --cov-fail-under=80
```

The existing GitHub Actions Windows runner uses Python 3.12. Record actual CI result per PR. The coverage gate currently combines statements and branches, so inspect coverage.json separately to verify each individual metric meets 80%. Do not claim the combined flag alone proves both gates.

## 6 Test Environment

Domain target: Python 3.10+ as specified in SRS; observed CI Python 3.12 on Windows and local Python 3.13.7. The new domain-only Windows jobs pass on Python 3.10.11 and 3.11.9; this does not establish Streamlit/AppTest compatibility on those versions or portability to untested operating systems. Install pytest, pytest-cov and Streamlit from requirements. Use synthetic IDs/locations and small repeatable bin fleets. Reset registries between tests. Routing capacity is measured in bin counts, not litres. The four domain modules use the standard library; the UI requires Streamlit and its transitive dependencies.

Observed local environment: Windows, Python 3.13.7. CI configuration: Windows runner, Python 3.12. Declare each observed version rather than treating one run as proof of every supported version. Synthetic bins have fixed IDs, text locations, fill boundaries and small truck fleets; there is no live sensor, personal or production data. Do not share mutable registries between independent cases.

### 6.1 Domain compatibility evidence (10 November 2026)

The `Domain compatibility` workflow checks the four domain modules without
installing Streamlit. It runs bins, alerts, routing, reports, system and smoke
cases; it excludes app/dashboard, demo and report-generator tests. These are
**113 selected domain cases**, not the 153-case expanded suite. Both statement
and branch thresholds are checked separately and XML/JSON artifacts retained.

| Environment | Observed domain result | Statement / branch outcomes | Evidence |
|---|---|---|---|
| Windows / CPython 3.10.11 | 113 passed in 0.58s | 154/154; 60/60 (100% each) | [Job 129729817133](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/actions/runs/42786760419/job/129729817133) |
| Windows / CPython 3.11.9 | 113 passed in 0.66s | 154/154; 60/60 (100% each) | [Job 129729817649](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/actions/runs/42786760419/job/129729817649) |

Recorded PR #29 head: `f66b3fe9e5b657ae4aa8ddedb936acc50b5eaf2e`.
These results are read from the completed workflow logs; they are not local runs
or claims about this evidence-documentation commit testing itself. Domain
support on those Windows versions now has evidence. The UI, other OS targets and
unobserved interpreter releases remain outside this matrix. The SRS owner can
reconcile its older untested-version wording after independent acceptance.
Domain-only elapsed times do not satisfy or redefine the original full-suite
NFR-2 target; the proposed core/UI split still awaits acceptance.

## 7 Test Schedule

Course targets: backlog 12 October; Sprint 1 19–23 October; Sprint 2 26–30 October; testing 2–6 November 2026. Those targets are historical and are not replaced by invented completion dates. Repository work is evidenced on 7–9 November; confirm the current submission deadline with the instructor.

As checked on 9 November at source main 3eecc7d2de529eba58b52666873081865d8e9069: core modules/system tests, SRS v2.0 #13, demo #14, UI #16, SAD #17, STP v1.1 #18, alert edge tests #19, contribution record #20, SRS v2.1 #21, severity filter #22, SAD/guide update #23 and editorial #8 are merged. That v1.2 status alignment subsequently merged in #25. The v1.3 routing/compatibility follow-up subsequently merged in PR #29 on 10 November 2026 as `b77e22380f2e7252860681a9eded919bd2d204b2`, after independent approvals of head `dc6bba05aae6dc514008daf0f60a125b407f39d7` by Shreya and Sasyak (section 15). Two actual silent recordings were recorded on 9 November and merged to main in PR #15 after Shreya approved their head; merge commit 84d6bd4a4613129a335a08defe01dd0620d5325b. Recording and repository review/merge are complete. Their source is main 1344aaf; they show 86 passing tests and 100% measured coverage. Spoken narration/instructor acceptance is not claimed.

Remaining sequence: independently review this status-only reconciliation, rerun regression after further accepted source changes, have the evidence owner regenerate final reports, resolve the partial NFR-2/NFR-6 evidence or acceptance decisions, confirm course acceptance of the merged silent recordings and freeze the agreed release. This plan does not assign completion dates for work not performed.

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

Ownership boundary: Sasyak owns SRS/setup/bins and his correction PRs; Shriya owns routing/STP; Shreya owns alerts/SAD and the merged UI; Shruti owns reports/system tests/final evidence. Each reviewer checks the exact latest head. Repository-owner release coordination and instructor sign-off remain separate decisions.

## 10 Risks and Mitigation

| Risk | Mitigation / unresolved boundary |
|---|---|
| Requirement/document drift across open PRs | Review this STP follow-up against merged SRS v2.1 on main and reconcile later accepted requirement changes |
| Old routing kit interface | Preserve registry/object APIs and run the integrated regression suite |
| Report evidence becomes stale | Keep tested source, actual run date/platform and exit status; evidence owner regenerates after source integration |
| Coverage mistaken for acceptance | Check each requirement's assertions and process/manual evidence, not only percentages |
| Unsupported compatibility/determinism claim | Keep report-order and untested-version gaps explicit until actual evidence is added by the responsible owner |
| Course acceptance of UI or silent format unconfirmed | Keep implemented UI/recording evidence separate from instructor, accessibility and final-demo acceptance |
| Original deadlines elapsed | Ask instructor for current deadline; keep actual dates |

## 11 Assumptions & Dependencies

This revision uses the requirement IDs and qualifications of merged SRS v2.1 on main (PR #21), following v2.0 in #13. STP v1.1 is already merged in #18; this follow-up preserves the prior evidence while synchronizing UI/demo and performance status. The proposed core/UI timing split is not instructor-approved. Section 6.1 now supplies domain-only Windows evidence for Python 3.10.11/3.11.9; NFR-6 remains qualified because it does not establish UI compatibility on those versions or untested platforms. No broad acceptance is inferred. The tests use a standalone in-memory model and trusted callers; there is no real dispatch or persistence guarantee. Source, test collection and dependencies must match the recorded evidence. Follow-up API/UI changes require affected-case review. Existing reviews and attribution are preserved; approval is never inferred from document preparation.

## 12 Suspension & Resumption Criteria

Stop acceptance testing when dependency code is missing, collection fails or environment setup prevents execution. Log the blocker and commit. Resume after the blocker is fixed and rerun affected tests plus full regression after integration. Do not label blocked/planned cases as passed.

Also suspend final sign-off when the tested revision cannot be identified or a required delivery has no evidence. Resume only after the responsible owner resolves the condition and records the actual retest. Preserve failed outputs for investigation; do not substitute stale passing reports.

## 13 Test Case Management & Traceability

| Requirement | Test identifiers |
|---|---|
| FR-1 | TC-BIN-06 through TC-BIN-10, SYS-01, SYS-04 |
| FR-2 | TC-BIN-03, TC-BIN-11, TC-BIN-12, SYS-02 |
| FR-3 | TC-BIN-04 |
| FR-5 | TC-RT-01 through TC-RT-04, TC-RT-06, TC-RT-07, TC-RT-09, TC-RT-10, TC-RT-16, TC-RT-17 |
| FR-6 | TC-RT-05, TC-RT-17, TC-RT-18, SYS-03 |
| FR-7 | TC-RT-08, TC-RT-11, TC-RT-12, TC-RT-18, TC-RT-19, SYS-01 |
| FR-4 | TC-AL-01 through TC-AL-09, SYS-01, SYS-02; TC-UI-05 and TC-UI-21 through TC-UI-25 cover presentation/filter behavior |
| FR-8 | TC-RP-01 through TC-RP-09, SYS-01, SYS-04 |
| FR-9 | TC-BIN-02 |
| FR-10 | TC-BIN-05, SYS-01 |
| FR-11 | TC-BIN-10 |
| FR-12 | TC-AL-04 |
| FR-13 | TC-RT-09, TC-RT-10, TC-RT-14, TC-RT-15, TC-RT-16 |
| FR-14 | TC-RT-07 |
| FR-15 | TC-RT-08, TC-RT-11, TC-RT-12, TC-RT-13, TC-RT-14, TC-RT-19, SYS-04 |
| FR-16 | TC-RP-05, TC-RP-06 |
| NFR-1 | TC-BIN-02, TC-BIN-03, TC-BIN-11, TC-BIN-12, TC-RT-07 through TC-RT-15, TC-RT-19; invalid state preserved |
| NFR-2 | Full-suite elapsed time and exact revision/platform; partial/unmet against the original 10-second target. Core/UI split remains proposed, with no UI-only timing inferred |
| NFR-3 | coverage.json statement and branch counters checked separately |
| NFR-4 | Independent PR review, required successful checks and repository rules; process evidence, not a pytest case |
| NFR-5 | TC-AL-03, TC-RT-02, TC-RT-17 (alerts and routing; report-line ordering is not separately tested) |
| NFR-6 | Section 6.1 domain-only Windows jobs: 3.10.11/3.11.9, each 113 passed. Existing CI 3.12/local 3.13.7 remain separate. UI on 3.10/3.11 and other platforms unverified |
| SR-1 | TC-BIN-03, TC-BIN-11, TC-BIN-12 |
| SR-2 | TC-BIN-02 |
| SR-3 | TC-RT-08, TC-RT-11, TC-RT-12, TC-RT-13, TC-RT-14, TC-RT-18, TC-RT-19, SYS-04 |
| SR-4 | TC-AL-03, TC-RP-09 |
| SR-5 | GitHub ruleset and pull request history |

This exceeds the course's 7–10 minimum test-case requirement. The listed automated IDs exist in `tests/`; process checks and compatibility targets are not automated test IDs. FR-9 to FR-16, NFR-5, NFR-6 and SR-1 to SR-5 refer to the merged SRS v2.1 on main (PR #21, following #13). Keep the Test Case Document synchronized with actual test names after sprint changes.

This is requirement-to-evidence planning. It does not replace case-level expected/actual records. NFR-2/5/6 are explicitly partial, process requirements need repository evidence, and a clean test run does not prove every planned scope item is delivered.

## 14 Test Metrics & Reporting

Report collected/executed/passed/failed/skipped/errored parametrized instances separately from unique scenario IDs. The historical pre-UI recording baseline has 86 executed passing instances (82 unit/smoke and 4 system). Source: main 1344aaf94155af94c4832ed0a3bfc371f8ff1f63. The 9 November recording run reports 4.26 seconds on Python 3.13.7, 140/140 statements and 54/54 branch outcomes covered. See PR #15 for the actual recording and its referenced source CI run; later changes require new evidence.

Historical integrated observation (9 November 2026): source main `3eecc7d2de529eba58b52666873081865d8e9069`, including merged UI, alert edge/filter cases and demo, passed **122 tests in 61.59 seconds** on Windows/Python 3.13.7 using `python -m pytest --cov --cov-branch --cov-fail-under=80 --cov-report=term-missing --cov-report=json:../stp-status-coverage.json`, exit 0. JSON and terminal counters show 160/160 statements and 58/58 branch outcomes (100% each) for configured `src/waste_mgmt`. Root `app.py` and `demo.py` are exercised by tests but outside this coverage denominator. This full-suite time exceeds the original ten-second NFR-2 target; no UI-only duration, accepted core/UI split, Python 3.10/3.11 result or instructor approval is inferred. This observation supplements the historical recording result; it does not regenerate Shruti's final report files or claim a new report tested its own commit.

Routing follow-up observation (10 November 2026): the runtime/test source published in PR #29 head `f66b3fe9e5b657ae4aa8ddedb936acc50b5eaf2e` passed the full local suite, **153 passed in 84.35s**, Windows/Python 3.13.7, exit 0. Separate counters: 174/174 statements and 64/64 branch outcomes for `src/waste_mgmt` (100% each). The earlier attempt had 152 passes and one initial AppTest startup error at its existing 15-second timeout; the unchanged rerun passed. No UI code or timeout was changed. The selected domain matrix in 6.1 has a different count/scope and must not be combined with this full-suite result. The original whole-suite performance criterion remains unmet. Final integrated report/test-case regeneration stays with the evidence owner after accepted source changes merge.

Formulas: pass rate = passed/executed with skipped/not-run separately disclosed; statement coverage = covered statements/total statements; branch coverage = covered branch outcomes/total branch outcomes. If a denominator is zero, report not applicable rather than inventing a percentage. Record elapsed suite time, open defects by severity and requirement evidence gaps. Defect density/aging are not established without a maintained issue baseline; no values are invented here.

Provide execution summaries per reviewed source and a final summary after integration. Do not infer overall requirement coverage from code coverage or count all RTM rows as passing when manual/process or partial evidence remains open.

## 15 Approvals

| Role | Responsible member | Record |
|---|---|---|
| Test-plan coordinator / Day 2 author | Shriya Vasundhara Singh | Prepared v1.1/v1.2 on 9 November 2026 and this v1.3 routing/compatibility follow-up on 10 November 2026; not self-approval |
| Merged STP v1.1 independent review | Sasyak Subudhi | [Approved #18 head 301e073](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/18#pullrequestreview-5825328284); merged as cf88a21f0e2f5a5d60cb66cce8665aca56170a5f |
| Merged editorial follow-up | Shreya Yashodhara Singh | [Approved #8 head 1aeac72](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/8#pullrequestreview-5825669243); merged as 5b46c9c4a09d254db1f8106355944a05680c2337 |
| Merged v1.2 status alignment | Sasyak Subudhi | [Approved #25 head 41fbe66](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/25#pullrequestreview-5829776673); merged as 88259bba045cac83481e203601dd939c44e95def |
| Merged v1.3 routing/compatibility follow-up | Shreya Yashodhara Singh and Sasyak Subudhi | [Shreya approved #29 head dc6bba0](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/29#pullrequestreview-5839459117); [Sasyak approved the same head](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/29#pullrequestreview-5839470092); merged on 10 November 2026 as b77e22380f2e7252860681a9eded919bd2d204b2 |
| Status-only reconciliation of the merged v1.3 record | Independent teammate reviewer | Pending for these new wording edits only; PR #29 approvals are not reused |
| Repository owner / release coordinator | Sasyak Subudhi | Final integration/release sign-off not claimed |
| Instructor / course acceptance | Course evaluator | Not recorded; confirm UI/deadline/recording exceptions where needed |

Routing/STP baseline PRs #3/#4, template alignment #18, editorial #8, status alignment #25 and v1.3 routing/compatibility follow-up #29 are merged with their actual records. The earlier measurements in sections 6.1 and 14 remain tied to their recorded source revisions; this status-only edit claims no new execution or final-report regeneration. Its own required checks and independent review must pass before merge. Repository approvals do not imply course/instructor acceptance or a changed performance threshold.
