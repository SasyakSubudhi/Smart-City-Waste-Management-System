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

## Input and failure contract

`plan_routes(registry, trucks, threshold=70)` accepts an iterable of `Truck`
objects, including a one-use generator. It consumes that iterable once in supplied
order. An empty iterable is valid and leaves every due bin unassigned. A
non-iterable fleet such as `None` raises `ValueError` with a fleet-specific
message, rather than leaking the incidental `list(None)` TypeError. Invalid
members, duplicate truck IDs and invalid thresholds are also rejected before
planning changes any readings. Errors raised inside a caller's iterator are not
silently treated as an empty fleet.

`complete_route(route, registry)` returns `None` on success. It requires a
`Route` containing a real `Truck` and a **tuple of hashable bin IDs**. Prefer
routes returned by `plan_routes`, which already satisfy that shape. If creating
one manually, use `Route(Truck("T1", 1), ("B1",))`; the comma creates a tuple.
Do not supply `"B1"`, a list, bytes or a set as `bin_ids`.

Previously, the malformed route `Route(Truck("T", 2), "AB")` could treat the
string as two IDs and empty bins `A` and `B`. It is now rejected without changing
either reading. Unsupported route/truck objects and unhashable tuple members
also raise a clear `ValueError`. Existing tuple-based planner/UI/demo calls are
unchanged; callers that previously supplied lists manually must use tuples.

Validation happens before mutation: check route/truck/container, completion flag,
capacity and duplicate IDs, then resolve every ID. Only after all checks pass are
the selected bins emptied and `route.completed` set. An unknown registry ID still
raises `KeyError`, preserving every remaining reading and the completion flag.

## Allocation invariants

For any registry insertion order, concatenate the IDs in every route followed by
`plan.unassigned_bin_ids`. The result is exactly the due bins sorted by descending
fill and bin-ID ties, with every due ID represented once. Truck order is the
caller's order, not alphabetical truck-ID order. Each route is nonempty and no
longer than its truck's bin-count capacity. Excess idle trucks have no route.
The registry's own list order and readings remain unchanged by planning.

## Two-truck collection example

This example can be run from a clone with `src` on the Python import path. It
demonstrates confirmation in a different order from planning, preservation of
unassigned bins, and a new plan after completing the original one.

```python
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.routing import Truck, plan_routes, complete_route

city = BinRegistry()
for bin_id, level in (("A", 100), ("B", 95), ("C", 90), ("D", 80), ("quiet", 69)):
    city.add(Bin(bin_id, "City centre", 100, fill_level=level))

plan = plan_routes(city, [Truck("T1", 1), Truck("T2", 1)])
assert [r.bin_ids for r in plan.routes] == [("A",), ("B",)]
assert plan.unassigned_bin_ids == ("C", "D")

complete_route(plan.routes[1], city)  # T2 finishes first.
assert [r.completed for r in plan.routes] == [False, True]
assert city.get("A").fill_level == 100
assert city.get("B").fill_level == 0

complete_route(plan.routes[0], city)
assert all(r.completed for r in plan.routes)
assert [city.get(b).fill_level for b in ("C", "D", "quiet")] == [90, 80, 69]

next_plan = plan_routes(city, [Truck("next", 1)])
assert next_plan.routes[0].bin_ids == ("C",)
assert next_plan.unassigned_bin_ids == ("D",)
```

Completion is atomic for **one route**, not a transaction across a fleet. If a
later truck's route fails, an earlier completed route stays completed. A failed
missing-bin check can be retried after restoring the original bin. Do not reuse
a removed ID for a different physical bin and assume a saved route detects that
replacement: the model has no identity versioning or reservations. Discard stale
or overlapping plans; manage one active dispatch plan per registry.

## Regression evidence to inspect

| Case | Observable behavior |
|---|---|
| TC-RT-13 / 14 | Malformed manual routes and invalid truck objects fail without emptying bins |
| TC-RT-15 / 16 | Non-iterable fleet rejection; valid one-use and empty generators |
| TC-RT-17 | Three fleet shapes across all 24 insertion orders of four due bins; exact assignment/backlog, capacities and unchanged registry |
| TC-RT-18 | Second truck completes first; first remains pending; backlog readings and route flags stay independent |
| TC-RT-19 | Missing first, middle or last selected bin causes no partial update; retry after restoring the original bin succeeds |

Run `python -m pytest tests/test_routing.py -q` for the routing regression cases.
The historical measurements above describe their original revisions, not these
new cases. Final integrated reports must be regenerated by the evidence owner
after accepted changes merge; passing these checks does not establish road-distance
optimization, physical dispatch, whole-application portability or course acceptance.
