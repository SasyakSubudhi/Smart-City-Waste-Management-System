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

## Explain the two SAD sequences
1. Simulated sensor looks up a bin, submits a reading, validation precedes
   mutation, caller gets all bins and generates fresh prioritized alerts.
   Invalid values raise ValueError and preserve the previous reading.
2. Supervisor requests a plan from the registry and trucks. Due bins are selected
   inclusively and assigned by priority/capacity. After actual trip confirmation,
   complete_route resolves every ID, empties selected bins and marks completion.
   Missing IDs cause KeyError before any emptying; repeated completion is rejected.

Capacity is bin count, not litres. Routes are priority assignments, not shortest
paths. Independent plans can overlap; trusted callers manage one active plan.

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

## Completed repository milestones (checked 9 November 2026)
- SRS v2 is merged through PR #13; the SAD's requirement allocation is reconciled.
- PR #15 created/uploaded the real 60-second and 120-second silent recordings and
  is merged. These are separate from the supplied tutorial video. Their actual
  recording date is 9 November; no earlier sprint execution date is inferred.
- UI #16 and SAD follow-up #17 are merged after independent approvals on their
  exact passing heads. No personal understanding or instructor acceptance is
  inferred from these merges.

## Remaining acceptance checks
Demo #14 integration; review/integration of alert edge tests and severity filtering;
current report consistency coordinated with Shruti; actual board owners/points;
instructor deadline/extension, silent-format acceptance and final demo/viva readiness.
Sasyak must coordinate NFR-2: Shriya's reviewed UI suite passed 109 tests in 33.99s,
which exceeds the existing ten-second full-suite requirement. Passing coverage/CI
does not make that timing requirement pass. Domain modules use the standard
library; the Streamlit app has external dependencies and a local browser/server
boundary. The SRS owner must qualify that scope. These checks remain pending or
unverified until the relevant evidence/decision exists.

## Why this guide remains in docs/
This is versioned team preparation material alongside the SAD, retained so the
same design explanations and evidence boundaries can be reviewed by teammates.
It is not a required testing report, an assessment rubric or proof of a recording,
personal authorship, human understanding or institutional approval. Actual
recordings live in docs/videos; acceptance depends on the course's requirements.
