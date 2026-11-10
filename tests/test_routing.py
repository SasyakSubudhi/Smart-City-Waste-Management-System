from itertools import permutations

import pytest
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.routing import Truck, Route, plan_routes, complete_route


def registry(*levels):
    result = BinRegistry()
    for bin_id, level in levels:
        result.add(Bin(bin_id, "City centre", 100, fill_level=level))
    return result


def test_tc_rt_01_select_threshold_inclusive():
    bins = registry(("low", 69), ("edge", 70), ("full", 90))
    plan = plan_routes(bins, [Truck("T1", 5)])
    assert plan.routes[0].bin_ids == ("full", "edge")
    assert not plan.unassigned_bin_ids
    assert [b.fill_level for b in bins.all()] == [69, 70, 90]


def test_tc_rt_02_fullest_first_and_deterministic_ties():
    bins = registry(("Z", 90), ("B", 100), ("A", 90), ("C", 75))
    plan = plan_routes(bins, [Truck("T1", 4)])
    assert plan.routes[0].bin_ids == ("B", "A", "Z", "C")


def test_tc_rt_03_capacity_and_multiple_trucks():
    bins = registry(("A", 100), ("B", 90), ("C", 80))
    plan = plan_routes(bins, [Truck("T1", 1), Truck("T2", 2)])
    assert [(r.truck.truck_id, r.bin_ids) for r in plan.routes] == [("T1", ("A",)), ("T2", ("B", "C"))]
    assert not plan.unassigned_bin_ids


@pytest.mark.parametrize("threshold,expected", [(0,("A","B")), (100,("A",)), (90,("A",))])
def test_tc_rt_04_custom_threshold(threshold, expected):
    assert plan_routes(registry(("A",100),("B",0)), [Truck("T",2)], threshold).routes[0].bin_ids == expected


def test_tc_rt_05_overflow_and_no_fleet():
    bins = registry(("A", 100), ("B", 90), ("C", 80))
    assert plan_routes(bins, [Truck("T",1)]).unassigned_bin_ids == ("B", "C")
    assert plan_routes(bins, []).unassigned_bin_ids == ("A", "B", "C")


def test_tc_rt_06_empty_registry_and_no_due_bins():
    assert not plan_routes(registry(), [Truck("T",1)]).routes
    plan = plan_routes(registry(("A",10)), [Truck("T",1)])
    assert plan.routes == () and plan.unassigned_bin_ids == ()


@pytest.mark.parametrize("value", [-1,101,True,70.5,"70",None])
def test_tc_rt_07_invalid_threshold(value):
    with pytest.raises(ValueError, match="threshold"):
        plan_routes(registry(), [], value)


def test_tc_rt_08_complete_route():
    bins = registry(("A",100),("B",80),("C",10))
    route = plan_routes(bins,[Truck("T",1)]).routes[0]
    complete_route(route,bins)
    assert route.completed and bins.get("A").fill_level == 0
    assert bins.get("B").fill_level == 80 and bins.get("C").fill_level == 10
    bins.get("A").update_fill_level(85)
    with pytest.raises(ValueError, match="already completed"):
        complete_route(route,bins)
    assert bins.get("A").fill_level == 85


@pytest.mark.parametrize("truck_id,capacity", [("",1),(" ",1),(None,1),(1,1),("T",0),("T",-1),("T",True),("T",1.5)])
def test_tc_rt_09_invalid_truck(truck_id,capacity):
    with pytest.raises(ValueError):
        Truck(truck_id,capacity)


def test_tc_rt_10_invalid_fleet():
    with pytest.raises(ValueError, match="unique"):
        plan_routes(registry(),[Truck("T",1),Truck("T",2)])
    with pytest.raises(ValueError, match="Truck objects"):
        plan_routes(registry(),["T"])


def test_tc_rt_11_missing_bin_atomic_completion():
    bins = registry(("A",100),("B",90))
    route = plan_routes(bins,[Truck("T",2)]).routes[0]
    bins.remove("B")
    with pytest.raises(KeyError):
        complete_route(route,bins)
    assert bins.get("A").fill_level == 100 and not route.completed


@pytest.mark.parametrize("ids", [(),("A","B","C"),("A","A")])
def test_tc_rt_12_invalid_route(ids):
    bins = registry(("A",90),("B",80),("C",70))
    with pytest.raises(ValueError):
        complete_route(Route(Truck("T",2),ids),bins)
    assert bins.get("A").fill_level == 90


@pytest.mark.parametrize("ids", ["AB", b"AB", ["A", "B"], {"A", "B"},
                                 None, 7, ("A", ["B"])])
def test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying(ids):
    bins = registry(("A", 90), ("B", 80))
    route = Route(Truck("T", 2), ids)
    with pytest.raises(ValueError, match="bin_ids"):
        complete_route(route, bins)
    assert [(b.bin_id, b.fill_level) for b in bins.all()] == [("A", 90), ("B", 80)]
    assert route.completed is False


@pytest.mark.parametrize("route", [None, object(), Route(None, ("A",)),
                                   Route("T", ("A",))])
def test_tc_rt_14_reject_invalid_route_or_truck_objects(route):
    bins = registry(("A", 90))
    with pytest.raises(ValueError, match="Route|Truck"):
        complete_route(route, bins)
    assert bins.get("A").fill_level == 90


@pytest.mark.parametrize("fleet", [None, 1, True])
def test_tc_rt_15_non_iterable_fleet_has_clear_validation_error(fleet):
    bins = registry(("A", 90))
    with pytest.raises(ValueError, match="fleet must be an iterable of Truck objects"):
        plan_routes(bins, fleet)
    assert bins.get("A").fill_level == 90


def test_tc_rt_16_fleet_generator_is_consumed_once_and_empty_is_supported():
    bins = registry(("A", 100), ("B", 90), ("C", 80))
    supplied = []

    def fleet():
        for truck_id in ("T2", "T1"):
            supplied.append(truck_id)
            yield Truck(truck_id, 1)

    plan = plan_routes(bins, fleet())
    assert supplied == ["T2", "T1"]
    assert [(r.truck.truck_id, r.bin_ids) for r in plan.routes] == [
        ("T2", ("A",)), ("T1", ("B",))]
    assert plan.unassigned_bin_ids == ("C",)
    assert plan_routes(bins, iter(())).unassigned_bin_ids == ("A", "B", "C")
    assert [b.fill_level for b in bins.all()] == [100, 90, 80]


@pytest.mark.parametrize("fleet_spec,expected_routes,expected_backlog", [
    ((("Z", 1), ("A", 1)), (("Z", ("C",)), ("A", ("A",))), ("B", "D")),
    ((("A", 2), ("Z", 3), ("idle", 1)),
     (("A", ("C", "A")), ("Z", ("B", "D"))), ()),
    ((("only", 3),), (("only", ("C", "A", "B")),), ("D",)),
])
def test_tc_rt_17_assignment_invariants_across_registry_orders(
        fleet_spec, expected_routes, expected_backlog):
    due = (("A", 90), ("B", 90), ("C", 100), ("D", 75))
    fleet = [Truck(truck_id, capacity) for truck_id, capacity in fleet_spec]
    for order in permutations(due):
        bins = registry(*order, ("quiet", 69))
        before = [(b.bin_id, b.fill_level) for b in bins.all()]
        plan = plan_routes(bins, fleet)
        assert tuple((r.truck.truck_id, r.bin_ids) for r in plan.routes) == expected_routes
        assert plan.unassigned_bin_ids == expected_backlog
        assigned = tuple(bin_id for route in plan.routes for bin_id in route.bin_ids)
        assert assigned + plan.unassigned_bin_ids == ("C", "A", "B", "D")
        assert len(set(assigned + plan.unassigned_bin_ids)) == 4
        assert all(0 < len(r.bin_ids) <= r.truck.capacity_bins for r in plan.routes)
        assert [(b.bin_id, b.fill_level) for b in bins.all()] == before
        assert plan_routes(bins, fleet) == plan


def test_tc_rt_18_complete_trucks_out_of_order_preserves_backlog():
    bins = registry(("A", 100), ("B", 95), ("C", 90), ("D", 80), ("quiet", 69))
    plan = plan_routes(bins, [Truck("T1", 1), Truck("T2", 1)])
    assert plan.unassigned_bin_ids == ("C", "D")
    assert complete_route(plan.routes[1], bins) is None
    assert [r.completed for r in plan.routes] == [False, True]
    assert {b.bin_id: b.fill_level for b in bins.all()} == {
        "A": 100, "B": 0, "C": 90, "D": 80, "quiet": 69}
    fresh = plan_routes(bins, [Truck("next", 2)])
    assert fresh.routes[0].bin_ids == ("A", "C")
    assert fresh.unassigned_bin_ids == ("D",)
    assert not any(r.completed for r in fresh.routes)
    assert complete_route(plan.routes[0], bins) is None
    assert all(r.completed for r in plan.routes)
    assert plan.unassigned_bin_ids == ("C", "D")
    assert {b.bin_id: b.fill_level for b in bins.all()} == {
        "A": 0, "B": 0, "C": 90, "D": 80, "quiet": 69}


@pytest.mark.parametrize("missing_id", ["A", "B", "C"])
def test_tc_rt_19_missing_bin_anywhere_is_atomic_and_retryable(missing_id):
    bins = registry(("A", 100), ("B", 90), ("C", 80), ("quiet", 10))
    route = plan_routes(bins, [Truck("T", 3)]).routes[0]
    removed = bins.get(missing_id)
    bins.remove(missing_id)
    before = {b.bin_id: b.fill_level for b in bins.all()}
    with pytest.raises(KeyError, match=missing_id):
        complete_route(route, bins)
    assert {b.bin_id: b.fill_level for b in bins.all()} == before
    assert route.completed is False
    bins.add(removed)
    complete_route(route, bins)
    assert route.completed is True
    assert {b.bin_id: b.fill_level for b in bins.all()} == {
        "A": 0, "B": 0, "C": 0, "quiet": 10}
