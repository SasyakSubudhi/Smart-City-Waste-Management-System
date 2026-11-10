# Shreya: viva and video preparation

Prepared 9 November 2026. This is a rehearsal guide, not proof of a recording,
personal understanding, board allocation or institutional acceptance.

## My scope and evidence
Shreya Yashodhara Singh (`yasho-26singh`): alerts and its tests/validation/handoff
(PR #5), SAD (PR #6), wording cleanup (#7), SAD follow-up revision on
docs/shreya-sad-update (PR #17, merged). Reviewed Shriya's routing/STP (#3/#4).
UI PR #16 is now merged after Shriya's independent approval and passing checks.
Reports/system tests/report generation belong to Shruti and are integrated team
dependencies, not my implementation contribution. No empty commits are needed.

## Explain the alert module
| Question | Answer to understand and demonstrate |
|---|---|
| Who owns thresholds? | Bin.status: <70 OK, 70..89 NEARLY_FULL, 90..100 FULL. Alerts consume status. |
| How is severity chosen? | OK is skipped; FULL maps to CRITICAL, NEARLY_FULL to WARNING. |
| Why critical first? | Sorting key is false for CRITICAL and true for WARNING; false sorts first. |
| Why stable? | Equal-key elements retain input order. We do not sort equal-severity IDs alphabetically. Same list gives the same ordering. |
| What does frozen mean? | Alert's fields cannot normally be reassigned. It is a snapshot, not a live link to Bin. |
| Does generation mutate bins? | No; it reads fields and creates Alert values. TC-AL-03 checks preservation. |
| After a reading or collection? | Generate a new list. Old alerts keep their old text/severity. TC-AL-05 covers this. |
| How is text produced? | Message includes bin ID, location and fill percent; format_alert prefixes `[SEVERITY]`. It is plain text, not HTML escaping. |
| Why separate modules? | Domain validation/status stay in bins; alerts/routing/reports use the same objects without duplicating policy. |
| What errors are handled? | Bin rejects invalid readings; alerts assume valid Bin objects and do not sanitize arbitrary external data. |

## Explain the three SAD sequences
1. Simulated sensor looks up a bin, submits a reading, validation precedes
   mutation, caller gets all bins and generates fresh prioritized alerts.
   Invalid values raise ValueError and preserve the previous reading.
2. Supervisor requests a plan from the registry and trucks. Due bins are selected
   inclusively and assigned by priority/capacity. After actual trip confirmation,
   complete_route resolves every ID, empties selected bins and marks completion.
   Missing IDs cause KeyError before any emptying; repeated completion is rejected.
3. The UI renders alerts from `registry.all()`, saves a plan, then calls
   `complete_route` from Collection routes. After successful confirmation it
   clears the plan and reruns, regenerating alerts and the city report. Streamlit
   renders all tab bodies on a script run; opening an already rendered tab alone
   does not invoke Python. SAD section 4.2 shows this third sequence.

Capacity is bin count, not litres. Routes are priority assignments, not shortest
paths. Independent plans can overlap; trusted callers manage one active plan.

## Explain the dashboard and UI
| Question | Answer to understand and demonstrate |
|---|---|
| What do helpers do? | bin_rows, alert_rows and route_rows adapt domain values for tables. Validation, classification and planning remain in the package. |
| What does attempt catch? | ValueError and KeyError only. KeyError's payload avoids extra representation quotes; unrelated programming errors propagate. |
| How does filtering work? | All/CRITICAL/WARNING selects fresh row dictionaries while preserving priority and tie order. It does not change readings or the saved plan; the selection survives reruns. |
| Why session_state? | It preserves the registry and one plan across Streamlit reruns, isolated per browser session. There is no disk persistence or shared multi-user dispatch state. |
| When is a plan invalidated? | Successful registration, reading updates or removal clear it. Failed edits preserve it. Planning again replaces the current plan. |
| What does planning change? | It saves assignments and backlog; readings are unchanged. plan_routes takes the registry itself, while alerts/reports take registry.all(). |
| What does confirmation change? | complete_route empties assigned bins. Success clears the saved plan, stores a transient notice and reruns so alerts/metrics refresh. |
| What if some bins were unassigned? | Only assigned bins are emptied. The success notice names remaining IDs and asks the supervisor to plan again; backlog readings/alerts remain. |
| Is confirmation atomic across trucks? | No. Validation/lookup prevents partial mutation within one route; an earlier completed route is not rolled back if a later route fails. |

Relevant presentation cases are TC-UI-01..31 across test_dashboard.py and
test_app.py. Explain severity filtering (21..25), backlog after confirmation (26),
session/empty-state guidance (27..28), plan invalidation/preservation (29..30) and
two-truck confirmation (31). IDs are scenarios, not parametrized execution totals.

## Rehearsal commands
From a fresh clone/update of the accepted main branch:

```text
python -m pip install -r requirements.txt
python -m pytest tests/test_alerts.py -q
python -m pytest --cov --cov-branch --cov-report=term-missing
```

Record the commit and actual output visible in your run. Before a demo, read
tests/test_alerts.py and reproduce 69 -> no alert, 70 -> WARNING, 90 -> CRITICAL,
and empty -> no alert. Explain why TC-AL-03 deliberately uses interleaved IDs:
it demonstrates priority and tie stability, not accidental alphabetical order.
TC-AL-06 demonstrates integration through the real registry/route API.

Statement coverage measures executed statements. Branch coverage measures
decision outcomes. Inspect both separately; a combined percentage or green CI
does not prove every requirement, platform or security property.
The configured coverage source is `src/waste_mgmt`. Root app.py and demo.py are
exercised by tests but excluded from that package percentage. Python 3.10/3.11
evidence is domain-only, not Streamlit/AppTest compatibility. The original
ten-second full-suite target remains unmet; no accepted replacement is inferred.

## Suggested spoken segment (rehearse in your own words)
"My module converts the bin model's status into alerts. Nearly full produces a
warning and full produces a critical alert. The output puts critical alerts first
and preserves input order inside each severity. Each alert is an immutable
snapshot, so I regenerate alerts after a reading changes or collection empties
a bin. My tests cover the exact boundaries, output format, unchanged bin state
and integration with route completion. The SAD shows this flow and the safe
collection flow; reports and routing remain separate components."

## Recording checklist and team coordination
The course requires a 1-minute and a 2-minute working-product sprint outcome
video. Coordinate your segment within those team recordings; do not assume two
additional personal videos are required or that four workdays equal four sprints.
Retain the existing silent, captioned videos. The supplied written requirements
do not explicitly require narration; this does not establish explicit instructor
approval. Prepare to explain your own contribution during the live viva.

| Show | Evidence to capture |
|---|---|
| Own contribution | PR #5/#6 and their actual author/review/merge records; follow-up PR if accepted |
| Working behavior | Boundary reading -> correct alert; collection -> refreshed alerts; actual console output |
| Quality | Focused alert tests and real full-suite output, with current commit |
| Design | Status-to-alert sequence and planning/completion sequence; explain state limits |
| Backlog | Your actual assigned items/story points if present; values need team verification |

Use an accepted working product for the sprint outcome shown. If using demo.py
or Streamlit, first confirm the relevant PR has merged and demonstrate the tested
version. Do not use the supplied tutorial video as your team's outcome video.
Avoid recording credentials, private browser tabs or personal data. Obtain the
actual deadline/extension from the instructor; the supplied 2-6 November testing
window has elapsed. Log real recording dates and locations after recording.

## Completed repository milestones (checked 10 November 2026)
- SRS v2 is merged through PR #13; the SAD's requirement allocation is reconciled.
- PR #15 created/uploaded the real 60-second and 120-second silent recordings and
  is merged. These are separate from the supplied tutorial video. Their actual
  recording date is 9 November; no earlier sprint execution date is inferred.
- UI #16 and SAD follow-up #17 are merged after independent approvals on their
  exact passing heads. No personal understanding or instructor acceptance is
  inferred from these merges.
- Command-line demo #14, alert edge tests #19, severity filtering #22 and SAD/viva
  corrections #23 are merged. Their merge records establish integration, not
  instructor acceptance or a fresh test measurement.
- Dashboard session/backlog guidance #28 and routing validation #29 are merged.
  Planner routes still contain tuple IDs. Manual routes require Route/Truck
  objects and a tuple of hashable IDs; malformed shapes fail before mutation.
  Non-iterable fleets raise ValueError, while one-use/empty generators work.
  Domain-only Windows CI verifies Python 3.10.11/3.11.9; it does not test the UI
  on those versions. See SAD sections 4.3, 4.4 and 5.3 for exact evidence.
- SAD v1.5 #30 merged as 93c82bf after Sasyak and Shriya independently approved
  head 43af049. The architecture/error-contract reconciliation is integrated.
- SRS v2.2 #31 merged as d9719bf after Shriya approved head b26c453. Its Windows
  domain-only Python 3.10/3.11 evidence correction is integrated; UI compatibility
  on those versions and institutional acceptance remain unverified.

## Remaining acceptance checks
At main d9719bf, Shruti's fresh Test Case Document and four final reports remain
pending after #29: the published reports still cite 915aac0 and the case document
does not yet list TC-RT-13..19. #30's SAD integration and #31's SRS portability
correction are completed, not open tasks. Subsequent editorial changes require
their own PR review; earlier approvals do not cover them. Also verify actual board owners/points;
instructor deadline/extension, silent-format acceptance and final demo/viva readiness.
Sasyak must coordinate NFR-2: Shriya measured the full UI-inclusive suite:
109 passed in 33.99s on Windows/Python 3.13.7 (core plus dashboard/AppTest).
UI-only time was not measured. This exceeds the ten-second full-suite requirement.
Passing coverage/CI
does not make that timing requirement pass. Domain modules use the standard
library; the Streamlit app has external dependencies and a local browser/server
boundary. Merged SRS v2.2 (#31), following v2.1 (#21), distinguishes this scope and describes the
proposed core/UI timing split. That proposal still requires acceptance; it does
not turn the original full-suite target into a pass. These checks remain pending or
unverified until the relevant evidence/decision exists.

## Why this guide remains in docs/
This is versioned team preparation material alongside the SAD, retained so the
same design explanations and evidence boundaries can be reviewed by teammates.
It is not a required testing report, an assessment rubric or proof of a recording,
personal authorship, human understanding or institutional approval. Actual
recordings live in docs/videos; acceptance depends on the course's requirements.
