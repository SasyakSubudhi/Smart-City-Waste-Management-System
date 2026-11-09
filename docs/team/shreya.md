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
| Architecture | docs/SAD.md; docs/VIVA_VIDEO_NOTES.md | Initial SAD merged in #6; template and UI sequence updates proposed in #17 |
| Web UI | app.py; src/waste_mgmt/dashboard.py; tests/test_dashboard.py; tests/test_app.py; docs/UI.md | Proposed in #16; not merged at this snapshot |
| Supporting evidence | docs/DAY3_VALIDATION.md; docs/DAY4_HANDOFF.md; UI/alert entries in docs/Test_Case_Document.md and generate_test_case_doc.py | Shared document updates associated with my feature PRs; regenerate after integration |
| Team contribution record | docs/team/shreya.md | This documentation PR; no runtime behavior change |

Bin management, routing, reports and their teammate implementation remain credited
to their actual authors. Reviewing them is separate from implementing them.

## Pull requests opened

These entries predate the PR introducing this record; that hosting PR supplies
its own creation date and review history. [All authored PRs](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pulls?q=is%3Apr+author%3Ayasho-26singh)
provide the live history as further contributions are accepted.

| PR | Work | Opened (IST) | State at snapshot |
|---|---|---|---|
| [#5](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/5) | Implement FR-4 overflow alerts with regression tests and Day 4 handoff | 2026-11-08 | Merged 2026-11-08 |
| [#6](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/6) | Add architecture document with actual APIs and UML sequences | 2026-11-08 | Merged 2026-11-08 |
| [#7](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/7) | Simplify Day 3 documentation wording | 2026-11-08 | Merged 2026-11-08 |
| [#16](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/16) | Add four-tab Streamlit web dashboard with UI tests | 2026-11-09 | Open at snapshot |
| [#17](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/17) | Update SAD for integrated system and supplied architecture template | 2026-11-09 | Open at snapshot |
| [#19](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/19) | Add alert batch-boundary, ordering and snapshot edge tests | 2026-11-09 | Open at snapshot |

## Independent reviews submitted

| PR / review evidence | Submitted (IST) | Recorded action | Reviewed head |
|---|---|---|---|
| [#3](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/3#pullrequestreview-5817455726) | 2026-11-08 | COMMENTED | `81b3f0e` |
| [#4](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/4#pullrequestreview-5817455957) | 2026-11-08 | APPROVED | `d90a374` |
| [#15](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/15#pullrequestreview-5824923724) | 2026-11-09 | APPROVED | `bae39c9` |
| [#14](https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/pull/14#pullrequestreview-5825110461) | 2026-11-09 | APPROVED | `bd10972` |

PR #3 was a post-merge comment, not an approval. PR #4 was an STP approval. PR #15
was reviewed after downloading/playing both recordings and verifying source/CI;
it is merged. PR #14 was checked on its exact head, including every changed line,
the full test suite and direct demo execution, before approval. These records do
not imply that my own PRs were self-approved or that a course evaluator accepted
the artifacts.

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
- The severity filter is planned on feature/alerts-ui-filter only after #16 merges.
  No filter implementation or acceptance is claimed in this record.

Required command used for these checks:

~~~text
python -m pytest --cov --cov-branch --cov-report=term-missing
~~~

Local observations above use Windows/Python 3.13.7; GitHub CI separately uses
Windows/Python 3.12. Durations are measured test-session times, not a UI response
benchmark. Different branch counts are expected because #16's AppTest suite is
not part of the other branches. No final-main coverage result is inferred by
combining separate branch results.

## Boundaries and remaining work

Independent reviewers must approve my feature/document PRs and required checks
must pass before merge. Contribution counts, story points, completed sprint dates,
recordings and human viva readiness are not inferred from this file. Backlog
allocation needs its own actual board evidence. Read the implementation and tests
before explaining them in the viva. Existing commit authorship and shared history
are preserved; no empty commits or teammate contributions are used as my work.
