# Handoff from Shriya to Shreya

Prepared 8 November 2026 with AI assistance. This is an interface and work guide, not evidence of human approval or completed future features.

## Current work and release prerequisites

Repository: https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System

- PR #1: bin management, Sasyak. Awaiting validation fix and review.
- PR #2: SRS, Sasyak. Awaiting review and merge.
- PR #3: routing, Shriya. Depends on #1. Awaiting independent review.
- PR #4: test plan and this handoff, Shriya. Awaiting independent review.

Shriya reviews #1 and #2. Shreya reviews #3 and #4. Merge only after genuine review and successful CI, in order #1, #2, #3, #4. After Sasyak changes bins, update routing from the merged main and rerun the full suite. Do not use an older copied bin file. Recheck all live PR states; the list above is a preparation snapshot.

Once these merges finish, clone the team repository directly or pull its latest main. Begin each new feature on a separate branch from main. Do not fork or copy all kit folders into main.

## Shreya's assigned deliverables

1. Overflow alerts: src/waste_mgmt/alerts.py and tests/test_alerts.py, branch feature/alerts. Implements FR-4. Preserve CRITICAL before WARNING and no alerts below 70.
2. Software Architecture and Design: docs/SAD.md, separate branch docs/sad. Describe the actual code, including the routing interface below. Include the required component description/diagram, architecture pattern, requirement traceability, security architecture, at least two sequence diagrams, API design and error handling.

The kit's alert module and its five tests work unchanged with the current bin/routing implementation. They use generate_alerts(registry.all()), not generate_alerts(registry). This was checked in an isolated scratch copy: five alerts tests and six reports tests passed together. This is compatibility evidence, not a claim that these modules are on main.

## Routing interface to use

```python
from waste_mgmt.routing import Truck, Route, RoutingPlan, plan_routes, complete_route

plan = plan_routes(registry, [Truck('T1', capacity_bins=2)], threshold=70)
for route in plan.routes:
    print(route.truck.truck_id, route.bin_ids, route.completed)
print(plan.unassigned_bin_ids)
if plan.routes:
    complete_route(plan.routes[0], registry)
```

| API or field | Meaning |
|---|---|
| plan_routes(registry, trucks, threshold=70) | Accepts BinRegistry, not registry.all(); returns RoutingPlan |
| Truck(truck_id, capacity_bins) | Immutable truck identity and positive integer capacity |
| plan.routes | Tuple of nonempty Route objects |
| route.truck | Assigned Truck |
| route.bin_ids | Tuple of bin IDs in visit priority order |
| route.completed | Set true after successful completion |
| plan.unassigned_bin_ids | Tuple of due IDs beyond fleet capacity |
| complete_route(route, registry) | Empties that route's bins; returns None |

Threshold is inclusive. Highest fill goes first; equal readings sort by bin ID. Trucks fill in input order. Empty fleet means no routes and all due bins unassigned. This is collection-priority planning, not distance optimization. Capacity counts bins, not litres.

Planning leaves sensor readings unchanged. Completion first resolves all IDs; a missing bin raises KeyError before any bin is emptied. Repeated completion, duplicate route IDs or over-capacity routes raise ValueError. Each plan is an independent in-memory snapshot; the caller must avoid running overlapping active plans. There is no persistence, authentication, vehicle dispatch or multi-user lock.

## Integration example for alerts

After alerts.py is introduced on Shreya's branch, this complete example should run with PYTHONPATH=src (pytest.ini already sets this for pytest):

```python
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.alerts import generate_alerts
from waste_mgmt.routing import Truck, plan_routes, complete_route

registry = BinRegistry()
registry.add(Bin('B1', 'MG Road', 120, 'general', 95))
registry.add(Bin('B2', 'Park', 100, 'organic', 72))
registry.add(Bin('B3', 'Library', 80, 'recyclable', 20))
assert [a.severity for a in generate_alerts(registry.all())] == ['CRITICAL', 'WARNING']
plan = plan_routes(registry, [Truck('T1', 1)])
assert plan.routes[0].bin_ids == ('B1',)
assert plan.unassigned_bin_ids == ('B2',)
complete_route(plan.routes[0], registry)
assert registry.get('B1').fill_level == 0
assert [(a.bin_id, a.severity) for a in generate_alerts(registry.all())] == [('B2', 'WARNING')]
```

## SAD corrections relative to the kit

Describe Registry -> plan_routes -> RoutingPlan/Route, followed by operator confirmation -> complete_route -> Bin.empty. Remove references to complete_collection, Truck.assigned, dictionary plans and list input for plan_routes. Keep the alerts and reports functions accepting bin lists. Describe real exception behavior and module limitations. Any module diagram or sequence diagram must show these same names.

Use one sequence diagram for sensor update -> status -> alert and another for route planning -> capacity/backlog -> collection completion. Explain integrity validation and Git review controls, without inventing login, encryption, persistence or physical sensors that do not exist.

## Test and handoff checklist

```text
python -m pip install -r requirements.txt
python -m pytest --cov --cov-branch --cov-report=term-missing --cov-fail-under=80
```

- Confirm main contains the merged routing and STP before starting Day 3.
- Read and understand #3/#4 before approving; do not approve solely because CI is green.
- Add the alerts module and its five tests; run the full suite locally before pushing.
- Run the integration example above and record actual results.
- Check statements and branches each meet the STP's 80% target; the existing combined coverage flag alone is not a separate gate for each.
- Open alerts and SAD PRs separately and obtain Shruti's review.
- Keep SRS/STP/SAD requirement names consistent and flag design deviations.

Baseline before Sasyak's fix: 48 combined bin/routing/smoke cases passed locally with 100% measured statement and branch coverage. These are not the final Day 3 counts; regenerate after every relevant change.

## Notes for Shruti after Day 3

Reports module and its six kit tests work without routing changes. The kit's system tests do not: replace complete_collection with complete_route, pass the registry into plan_routes, read tuple fields from RoutingPlan/Route, and assert post-completion bin state instead of a collected-count return. Do not overwrite routing with the kit version. Regenerate test documents, reports and HTML from the actual final main; do not reuse kit coverage totals or dates. Report-generation scripts should check pytest return codes and guard zero-test/zero-branch cases before claiming success.

## Outstanding course-wide work

The package and kit have no application UI. The original user request requires a UI, so the team must assign its implementation and browser validation. The two course sprint videos, GitHub Project/backlog/story points, course-required SRS security objectives/requirements and use-case diagram, final documentation, and genuine team reviews remain separate completion checks. Neither this handoff nor CI claims they are complete.
