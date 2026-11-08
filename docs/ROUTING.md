# Collection routing

Implements FR-5, FR-6, FR-7 from Sasyak's SRS PR #2. Uses BinRegistry from PR #1. No additional runtime dependencies.

```python
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.routing import Truck, plan_routes, complete_route

bins = BinRegistry()
bins.add(Bin('B1', 'MG Road', 100, fill_level=95))
bins.add(Bin('B2', 'Park', 100, fill_level=80))
plan = plan_routes(bins, [Truck('T1', capacity_bins=1)])
assert plan.routes[0].bin_ids == ('B1',)
assert plan.unassigned_bin_ids == ('B2',)
complete_route(plan.routes[0], bins)
assert bins.get('B1').fill_level == 0
```

Threshold defaults to 70 and is inclusive. All integer values from 0 through 100 are allowed. Bins are sorted by descending fill, then bin ID for ties. Trucks are filled in caller-supplied order; capacity is a count of bins per trip, not litres. Empty routes are omitted. Unassigned IDs remain in priority order. Planning does not change bin readings.

Completion resolves all bin IDs before emptying any, so removing a bin after planning causes a KeyError without partial emptying. Completing the same Route twice raises ValueError, preserving readings received after completion. Operator confirmation is required: this package does not dispatch actual trucks. Plans are independent in-memory snapshots; the caller must manage one active plan to avoid double dispatch. There is no persistence or multi-user concurrency control.

This is priority-based assignment, not geographic distance optimization. The SRS does not define coordinates or road distances. The existing bin module is unchanged.

Run `python -m pytest --cov --cov-branch --cov-report=term-missing`. On 8 November 2026 the local combined suite passed 48 cases in 0.78 seconds, measuring 100% statement and branch coverage (96 statements, 38 branch outcomes). Runtime is environment-specific and CI must independently pass. 

## Validation after the bin fix

On 8 November 2026, main's merged PR #1 validation fix was integrated into this branch. The exact combined bin/routing snapshot passed 56 tests locally in 0.53 seconds, with 98/98 statements and 40/40 branch outcomes covered. Live CI must also pass before merge. No alerts, SAD or other teammate implementation was added.
