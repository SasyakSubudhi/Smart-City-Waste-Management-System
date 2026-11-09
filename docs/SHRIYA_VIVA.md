# Shriya: routing and Test Plan preparation

Owner: Shriya Vasundhara Singh (`vasun26shriya`), Day 2. This is a preparation aid, not a claim that the viva or individual rehearsal has happened.

## My contribution

Routing is merged in PR #3; the original Test Plan is merged in PR #4. The template-alignment follow-up organizes the plan around the supplied 15 sections, updates integrated evidence and keeps pending deliveries explicit. Show the actual PRs and their review/check records. Use your own assigned Project items/points once the owner supplies board evidence; do not invent them.

Suggested introduction: “I implemented the collection-route planner and its tests, and maintained our Software Test Plan. The planner chooses bins by fill priority and truck capacity, reports bins that cannot be assigned, and validates a route before confirming collection.”

## Routing decisions I should explain

- `plan_routes(registry, trucks, threshold=70)` receives the registry. Due bins include the threshold; 69 is excluded and 70 included by default.
- Sort by descending fill level, then bin ID for deterministic ties. This is priority/capacity assignment. Locations are labels; the algorithm does not optimize travel distance.
- `Truck.capacity_bins` counts bins. Trucks are assigned in supplied fleet order. Each due bin occurs once across assigned routes and `plan.unassigned_bin_ids`.
- Plans expose `.routes` and `.unassigned_bin_ids`; routes expose `.truck`, `.bin_ids` and `.completed`. Do not treat plans as dictionaries.
- Planning preserves readings. `complete_route(route, registry)` returns `None`; inspect the mutated bins and `route.completed` for the result.
- Before emptying bins, completion validates route shape/capacity/duplicates and resolves every ID. A missing bin therefore prevents partial emptying. Already-completed routes reject another completion, including after a newer sensor reading.
- Alerts and reports consume `registry.all()`. Regenerate them after collection to see updated state.

## Tests to open during rehearsal

| Test ID | What its assertions demonstrate |
|---|---|
| TC-RT-01 / 04 | Inclusive default/custom thresholds and planning without state mutation |
| TC-RT-02 | Fullest-first order and bin-ID ties |
| TC-RT-03 / 05 | Multiple trucks, bin-count capacity, overflow and empty fleet |
| TC-RT-06 | Empty registry or no due bins |
| TC-RT-07 | Invalid threshold type/range |
| TC-RT-08 | Selected bins reset; untouched bins preserved; repeated completion rejects a fresh reading |
| TC-RT-09 / 10 | Invalid trucks and duplicate/invalid fleet entries |
| TC-RT-11 / 12 | Missing-bin atomicity and invalid route structures |
| SYS-01 through SYS-04 | Integrated flow, updated readings, fleet backlog and removed-bin safety |

Read the assertions, not just the test names. The baseline contains 86 parametrized test instances; that is not 86 unique requirement IDs. The recorded baseline reaches 100% statement and branch coverage; coverage does not establish UI acceptance, all Python versions, security guarantees or shortest-path behavior.

## A small worked example

Bins B1=95, B4=85, B2=72, B3=20; trucks T1 and T2 each hold one bin. At threshold 70 the due order is B1, B4, B2. T1 receives B1, T2 receives B4, and B2 remains unassigned. Completing those two routes sets only B1/B4 to zero. B2 remains 72 and produces a WARNING; B3 remains 20. The four-bin average is 23.0.

## Test Plan questions

Explain why section 5.1 validates input/integrity rather than claiming nonexistent authentication/TLS testing. Explain unit versus system versus browser acceptance, separate statement/branch metrics, actual revision/platform/date evidence, and why partial portability/report-order requirements stay explicit. Explain independent review, green CI and protected main. A plan is not an executed report or an approval record.

## Before the individual viva

Open routing.py, tests/test_routing.py and the latest accepted STP. Trace the example yourself and run the suite locally. Practise the introduction in your own words. The silent video has module credits, but it does not establish that you spoke or rehearsed; confirm any separate narration rule with the instructor. Check the final merged version after teammates integrate their changes.
