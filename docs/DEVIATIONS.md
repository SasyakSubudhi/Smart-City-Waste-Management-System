# Deviations from the Submitted Documents

This note lists every place where the project differs from the originally submitted SRS (v1.0), SAD and Test Plan, or from the course plan, with the reason. Items marked **pending** are not done yet and are not claimed as complete.

## 1. Product and requirements
| # | Original | Current state | Reason / status |
|---|---|---|---|
| 1 | The team's problem statement asks for routes based on location, vehicle capacity, priority **and distance**. | Routes are **priority and capacity based only**: fullest bins first, ties by bin ID, at most `capacity_bins` bins per truck. No distances or coordinates are used. | The SRS defines locations as text labels only, with no coordinates or travel-distance model. Distance-based routing is **not implemented** and is future work. See `docs/ROUTING.md`. |
| 2 | SRS v1.0 FR-2 only required readings to be inside 0-100. | FR-2 requires **whole numbers** from 0 to 100; NaN, infinity, booleans, decimals, text and `None` are rejected (tests `tc_bin_11`, `tc_bin_12`). | Found in review of PR #1: NaN and `True` pass a plain range check. Fixed before merge. |
| 3 | SRS v1.0 had FR-1 to FR-8 and NFR-1 to NFR-4, with no security section or diagrams. | SRS v2.0 (PR #13, **pending approval**) adds FR-9 to FR-16, NFR-5, NFR-6, security objectives SO-1 to SO-3, security requirements SR-1 to SR-5, two use-case diagrams and a traceability matrix. | To follow the SRS template. The new functional requirements describe behaviour that was already implemented and tested. NFR-5 (report-line ordering) and NFR-6 (Python 3.10/3.11) are only partly verified; see the SRS traceability table. |
| 4 | The original project request asks for a system **with a UI**. | **Open deviation.** The merged package has no graphical interface. A command-line demo (`demo.py`, PR #14) is pending, and a Streamlit web UI is planned (owner: Shreya Yashodhara Singh) but not merged. | Using GitHub for collaboration does not waive the UI requirement. If the UI is not delivered, the instructor's acceptance of this deviation is required; none has been obtained. |

## 2. Design and interfaces
| # | Original plan | Current state | Reason |
|---|---|---|---|
| 5 | Early kit design planned routes as dictionaries (`plan["routes"]`) and a `complete_collection` function. | Routing returns a `RoutingPlan` of `Route` objects (`routes`, `unassigned_bin_ids`) and uses `complete_route(route, registry)`. Alerts and reports take `registry.all()`; routing takes the registry. | The merged routing module uses immutable plan objects and atomic completion. Later modules and system tests were adapted to it. `docs/SAD.md` describes the final interfaces. |
| 6 | Test Plan listed alert, report and system test IDs as planned. | Implemented on `main`: `TC-AL-01..06`, `TC-RP-01..09`, `SYS-01..04`; 86 automated tests pass on `main` (82 unit and 4 system). The demo test and any UI tests are **pending** with PR #14 and the UI PR. | Implemented on 8 and 9 November 2026 (git history). |

## 3. Process and schedule
| # | Course plan | Actual | Reason |
|---|---|---|---|
| 7 | Backlog 12 Oct, Sprint 1 on 19-23 Oct, Sprint 2 on 26-30 Oct, testing 2-6 Nov. | The 2-6 Nov testing window has elapsed. The git history shows work on 7, 8 and 9 Nov 2026. The GitHub Project backlog and the sprint plans are **pending** and will be recorded with their real creation dates. | The team started late. Dates are taken from the commit and PR history; nothing is back-dated. Ask the instructor about the current deadline. |
| 8 | Sprint outcome videos (1 minute and 2 minutes) showing the working product. | Two real silent screen recordings were recorded on 9 Nov 2026 and merged to `main` in PR #15 (reviewed and approved by Shreya): `docs/videos/sprint1_demo.mp4` (60 seconds) and `docs/videos/sprint2_demo.mp4` (120 seconds), with captions and subtitle files. They are **silent**: module credits are shown as on-screen text, and no spoken narration or team speaking is claimed. | The course wording asks for 1-minute and 2-minute working-product videos. Whether silent, captioned videos are acceptable, and whether a 9 Nov recording date is acceptable, has not been confirmed with the instructor. They show the package APIs through a local recording viewer, not the Streamlit UI (PR #16, pending). |
| 9 | Test reports generated after all testing. | The four reports on `main` were generated from the code at the commit named in each report. They will be regenerated after the pending PRs merge. The reports record the Python version used. | Counts and coverage are only valid for the commit and Python version recorded in each report. |

## 4. Use of AI tools
As permitted by the course FAQ, AI tools helped write code, tests and documents. Every team member is expected to read and be able to explain the code and documents they own.
