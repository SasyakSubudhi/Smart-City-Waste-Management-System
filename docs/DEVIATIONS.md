# Deviations from the Submitted Documents

This note lists every place where the final system differs from the originally submitted SRS (v1.0), SAD and Test Plan, or from the course plan, with the reason. It is written for the final demo.

## 1. Product and requirements
| # | Original | Final | Reason |
|---|---|---|---|
| 1 | The team's problem statement asks for routes based on location, vehicle capacity, priority **and distance**. | Routes are **priority and capacity based only**: fullest bins first, ties by bin ID, at most `capacity_bins` bins per truck. No distances or coordinates are used. | The SRS defines locations as text labels only, with no coordinates or travel-distance model. A distance model (for example shortest path over a road graph) is future work. See `docs/ROUTING.md`. |
| 2 | SRS v1.0 FR-2 only required readings to be inside 0-100. | FR-2 now requires **whole numbers** from 0 to 100; NaN, infinity, booleans, decimals, text and `None` are rejected (tests `tc_bin_11`, `tc_bin_12`). | Found in review of PR #1: NaN and `True` pass a plain range check. Fixed before merge. |
| 3 | SRS v1.0 had FR-1 to FR-8 and NFR-1 to NFR-4, with no security section or diagrams. | SRS v2.0 adds FR-9 to FR-16, NFR-5, NFR-6, security objectives SO-1 to SO-3, security requirements SR-1 to SR-5, two use-case diagrams and a traceability matrix. | To follow the course SRS template and checklist. The new functional requirements describe behaviour that was already implemented and tested. |
| 4 | Product described as an application with users. | There is **no graphical interface**; the product is a Python package with a command-line demo (`demo.py`). | The task allows implementation on GitHub only; the SRS scope excludes hardware, network and authentication. |

## 2. Design and interfaces
| # | Original plan | Final | Reason |
|---|---|---|---|
| 5 | Early kit design planned routes as dictionaries (`plan["routes"]`) and a `complete_collection` function. | Routing returns a `RoutingPlan` of `Route` objects (`routes`, `unassigned_bin_ids`) and uses `complete_route(route, registry)`. Alerts and reports take `registry.all()`; routing takes the registry. | The merged routing module uses immutable plan objects and atomic completion. Later modules and system tests were adapted to it. `docs/SAD.md` describes the final interfaces. |
| 6 | Test Plan listed alert, report and system test IDs as planned. | All planned groups now exist: `TC-AL-01..06`, `TC-RP-01..09`, `SYS-01..04`; total 87 automated tests. | Implemented during Sprints 2 and 3. |

## 3. Process and schedule
| # | Course plan | Actual | Reason |
|---|---|---|---|
| 7 | Backlog 12 Oct, Sprint 1 on 19-23 Oct, Sprint 2 on 26-30 Oct, testing 2-6 Nov. | Development and testing were done in four daily iterations on 7-10 Nov 2026: Day 1 bins and SRS, Day 2 routing and STP, Day 3 alerts and SAD, Day 4 reports, system tests and test reports. The GitHub Project backlog was created from the SRS on 9 Nov. | The team started late. The dates and PR history in GitHub show the real timeline. |
| 8 | Sprint outcome videos recorded during each sprint. | The 1-minute and 2-minute demo videos are recorded at the end and added to `docs/videos/`. | Same reason as 7. |
| 9 | Test reports generated after all testing. | Reports are regenerated from the final `main` commit by `generate_reports.py` and record the commit, date and environment. Earlier reports were generated on Python 3.14 (macOS); CI uses Python 3.12 on Windows. | Statement counts can differ slightly between Python versions; both runs pass with 100% coverage. |

## 4. Use of AI tools
As permitted by the course FAQ, GPT-based tools helped write code, tests and documents. This is stated in the pull requests, commit messages and review comments. Every team member is expected to read and be able to explain the code and documents they own.
