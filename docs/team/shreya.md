# Shreya Yashodhara Singh

GitHub: [yasho-26singh](https://github.com/yasho-26singh). Role: alerts, Software
Architecture Document (SAD), and the web UI. This is a responsibility/evidence
record, not a CODEOWNERS rule or proof of grade allocation.

Snapshot checked 9 November 2026. Dates below are calendar dates in Asia/Kolkata
(IST), derived from GitHub's created/merged/submitted timestamps. Open PRs remain
pending independent acceptance; a published branch is not a merged contribution.

## Files within my responsibility

| Area | Files | Evidence/state |
|---|---|---|
| Alerts | src/waste_mgmt/alerts.py; tests/test_alerts.py | Initial implementation merged in #5; additional edge tests proposed in #19 |
| Architecture | docs/SAD.md; docs/VIVA_VIDEO_NOTES.md | Initial SAD merged in #6; template/UI sequences merged in #17; current follow-up #23 open |
| Web UI | app.py; src/waste_mgmt/dashboard.py; tests/test_dashboard.py; tests/test_app.py; docs/UI.md | Merged in #16; severity filter published in #22, awaiting merge |
| Supporting evidence | docs/DAY3_VALIDATION.md; docs/DAY4_HANDOFF.md; UI/alert entries in docs/Test_Case_Document.md and generate_test_case_doc.py | Shared document updates associated with my feature PRs; regenerate after integration |
| Team contribution record | docs/team/shreya.md | This documentation PR; no runtime behavior change |

Bin management, routing, reports and their teammate implementation remain credited
to their actual authors. Reviewing them is separate from implementing them.

## Pull requests opened

Each numbered entry below is an actual authored PR, including this record's
hosting PR #20. Statuses are refreshed after the #16/#17 merges. [All authored PRs](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pulls?q=is%3Apr+author%3Ayasho-26singh)
provide the live history as further contributions are accepted.

| PR | Work | Opened (IST) | State at snapshot |
|---|---|---|---|
| [#5](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/5) | Implement FR-4 overflow alerts with regression tests and Day 4 handoff | 2026-11-08 | Merged 2026-11-08 |
| [#6](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/6) | Add architecture document with actual APIs and UML sequences | 2026-11-08 | Merged 2026-11-08 |
| [#7](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/7) | Simplify Day 3 documentation wording | 2026-11-08 | Merged 2026-11-08 |
| [#16](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/16) | Add four-tab Streamlit web dashboard with UI tests | 2026-11-09 | Merged 2026-11-09 |
| [#17](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/17) | Update SAD for integrated system and supplied architecture template | 2026-11-09 | Merged 2026-11-09 |
| [#19](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/19) | Add alert batch-boundary, ordering and snapshot edge tests | 2026-11-09 | Open at snapshot |
| [#20](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/20) | Record Shreya's role and verified PR contribution history | 2026-11-09 | Open at snapshot |
| [#22](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/22) | Filter the Alerts tab by severity | 2026-11-09 | Open at snapshot |
| [#23](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/23) | Refresh viva checklist and architecture after UI integration | 2026-11-09 | Open at snapshot |

## Independent reviews submitted

| PR / review evidence | Submitted (IST) | Recorded action | Reviewed head |
|---|---|---|---|
| [#3](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/3#pullrequestreview-5817455726) | 2026-11-08 | COMMENTED | `81b3f0e` |
| [#4](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/4#pullrequestreview-5817455957) | 2026-11-08 | APPROVED | `d90a374` |
| [#15](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/15#pullrequestreview-5824923724) | 2026-11-09 | APPROVED | `bae39c9` |
| [#14](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/14#pullrequestreview-5825110461) | 2026-11-09 | APPROVED | `bd10972` |
| [#8](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/8#pullrequestreview-5825457988) | 2026-11-09 | CHANGES_REQUESTED | `065a318` |
| [#21](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/21#pullrequestreview-5825562681) | 2026-11-09 | APPROVED | `40c6fd7` |

PR #3 was a post-merge comment, not an approval. PR #4 was an STP approval. PR #15
was reviewed after downloading/playing both recordings and verifying source/CI;
it is merged. PR #14 was checked on its exact head, including every changed line,
the full test suite and direct demo execution, before approval. These records do
not imply that my own PRs were self-approved or that a course evaluator accepted
the artifacts. PR #8 received changes requested for its real STP conflict at
065a318; that is a dated review, not an assertion about a later corrected head.
PR #21 was approved at 40c6fd7 after full-diff/source review and an exact-head
109-case run; it does not certify instructor acceptance of a timing revision.

## Current substantive follow-up

- #16: lookup errors display their KeyError message without representation quotes;
  docs/UI.md records actual measured test duration and environment. The full-suite
  result was 109 passed in 23.49s, 156/156 statements and 56/56 branch outcomes.
- #17: follows the course SAD template and adds a third sequence for supervisor
  alerts/collection/refresh, distinguishing eager Streamlit render from tab clicks.
- #19: adds mixed boundaries in one batch, 40 equal-severity bins in supplied order,
  and retained alert text/format after emptying. Existing empty-input and severity
  formatting cases are reused, not copied. Its full suite passed 91 cases in 0.90s,
  with 140/140 statements and 54/54 branch outcomes covered.
- #22 publishes the severity filter after #16 merged: All/CRITICAL/WARNING,
  preserved order and fresh rows after collection. Its branch passed 116 tests in
  25.73s with 160/160 statements and 58/58 branch outcomes. It is independently
  approved but remains unmerged at this snapshot; this is not final-main evidence.
- #23 fixes full-UI-inclusive timing labels and preserves the original 0.71s
  historical observation. It awaits independent re-review after corrections.

Required command used for these checks:

~~~text
python -m pytest --cov --cov-branch --cov-report=term-missing
~~~

Local observations above use Windows/Python 3.13.7; GitHub CI separately uses
Windows/Python 3.12. Durations are measured test-session times, not a UI response
benchmark. Different branch counts reflect each branch's source baseline; the old #19/#20
bases do not include #16's AppTest suite. No final-main coverage result is inferred by
combining separate branch results.

## Boundaries and remaining work

Independent reviewers must approve my feature/document PRs and required checks
must pass before merge. Contribution counts, story points, completed sprint dates,
recordings and human viva readiness are not inferred from this file. Backlog
allocation needs its own actual board evidence. Read the implementation and tests
before explaining them in the viva. Existing commit authorship and shared history
are preserved; no empty commits or teammate contributions are used as my work.
