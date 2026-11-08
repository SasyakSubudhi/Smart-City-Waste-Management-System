# Day 4 integration handoff

8 November 2026. Day 3 author: Shreya (`yasho-26singh`).

## Merge and review order
Routing PR #3 is already merged. Shreya reviewed its exact head: 56 tests,
98/98 statements and 40/40 branch outcomes. STP PR #4 was reviewed and approved
at d90a374c1ca8062c98950073e6b86c135745f582; its CI passed. Shriya/maintainer
must merge #4. Its own old baseline contains only the smoke test; this is not
evidence of final project coverage. Day 3 feature and SAD branches start at
merged routing main; STP is documentation-only so no code dependency is blocked.

Shruti reviews Day 3 alerts and SAD PRs; merge only after independent approval
and green CI. Shriya may handle merging after that review. Pull latest main
before reports, then system tests, then regenerated report documents. Keep
reports/system work in Shruti's contribution rather than attributing it to Shreya.

## Working public API
```python
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.alerts import generate_alerts, format_alert
from waste_mgmt.routing import Truck, plan_routes, complete_route

registry = BinRegistry()
registry.add(Bin('B1', 'Park', 100, fill_level=95))
assert format_alert(generate_alerts(registry.all())[0]).startswith('[CRITICAL]')
plan = plan_routes(registry, [Truck('T1', 1)])
assert plan.routes[0].bin_ids == ('B1',)
assert plan.unassigned_bin_ids == ()
complete_route(plan.routes[0], registry)
assert plan.routes[0].completed
assert generate_alerts(registry.all()) == []
```

Alerts and kit reports take `registry.all()`; routing takes `registry` itself.
Replace kit system-test import `complete_collection` with `complete_route`.
Replace dictionary plan access with `.routes`, `.unassigned_bin_ids`, and each
route's `.bin_ids`. `Truck.assigned` does not exist. Do not replace routing to
make the obsolete tests pass. Complete only operator-confirmed routes and avoid
overlapping active plans. Regenerate alerts after any state change.

## Required Day 4 checks
Adapt all four kit system journeys to the current API: collection and reports;
sensor changes; capacity/backlog; removal and stale-route atomicity. Test alerts
and report totals before/after collection, empty registry and all status boundaries.
Inspect report scripts: propagate failed pytest exit status and never overwrite
failure evidence with a success claim. Reports must record actual final commit,
date, environment, pass/fail/blocked status and separate coverage metrics.

Day 3 regression: 68 tests passed; 116/116 statements and 44/44 branch outcomes.
Run final-main tests again after Day 4, including report and system cases. Upload
all four Part-3 reports and updated Test Case Document to docs via reviewed PR.
Coverage's combined percentage is insufficient: verify statements and branches
each independently meet 80%.

## Open team requirements
Reports, system validation, report generators, final videos, SRS use-case diagram
and security objectives/requirements remain team work. No UI exists; assign it
explicitly if required. Check backlog, story points, actual sprint evidence and
collaborator access. The kit's four workdays do not prove four course sprints.

## Explain in the viva
Bin owns thresholds; alerts read status, never change bins. Frozen Alert values
are snapshots. Stable sorting puts critical first without reordering equal severity.
Routes count bins, expose backlog and resolve all IDs before emptying. Statement
coverage measures executed statements; branch coverage measures decision outcomes.
Read the implementation and tests before presenting this contribution.
