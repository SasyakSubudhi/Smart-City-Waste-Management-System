"""System validation tests: end-to-end journeys across bins, alerts, routing and reports.

Each scenario names the SRS requirements it validates (see docs/SRS.md).
Alerts and reports take ``registry.all()``; routing takes the registry itself.
"""

import pytest

from waste_mgmt.alerts import generate_alerts
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.reports import average_fill_level, status_summary
from waste_mgmt.routing import Truck, complete_route, plan_routes


def build_city():
    reg = BinRegistry()
    reg.add(Bin("B1", "MG Road", 120, "general", 95))
    reg.add(Bin("B2", "Indiranagar", 100, "organic", 72))
    reg.add(Bin("B3", "Koramangala", 80, "recyclable", 20))
    return reg


def test_sys_01_full_collection_cycle():
    """FR-1..FR-8: register -> alert -> plan -> confirmed collection -> alerts and report refresh."""
    reg = build_city()
    assert [(a.bin_id, a.severity) for a in generate_alerts(reg.all())] == [
        ("B1", "CRITICAL"),
        ("B2", "WARNING"),
    ]
    assert status_summary(reg.all()) == {"OK": 1, "NEARLY_FULL": 1, "FULL": 1}

    plan = plan_routes(reg, [Truck("T1", 10)])
    assert [r.bin_ids for r in plan.routes] == [("B1", "B2")]
    assert plan.unassigned_bin_ids == ()
    # planning must not change readings
    assert reg.get("B1").fill_level == 95 and reg.get("B2").fill_level == 72

    complete_route(plan.routes[0], reg)
    assert plan.routes[0].completed
    assert reg.get("B1").fill_level == 0 and reg.get("B2").fill_level == 0
    assert reg.get("B3").fill_level == 20  # only the selected bins are emptied
    assert generate_alerts(reg.all()) == []
    assert status_summary(reg.all()) == {"OK": 3, "NEARLY_FULL": 0, "FULL": 0}
    assert average_fill_level(reg.all()) == 6.67


def test_sys_02_sensor_update_changes_alert_and_routing():
    """FR-2, FR-3, FR-4, FR-5: a new reading changes status, alert and route eligibility."""
    reg = build_city()
    assert plan_routes(reg, [Truck("T1", 10)]).routes[0].bin_ids == ("B1", "B2")

    reg.get("B3").update_fill_level(92)
    critical = [a.bin_id for a in generate_alerts(reg.all()) if a.severity == "CRITICAL"]
    assert critical == ["B1", "B3"]
    assert plan_routes(reg, [Truck("T1", 10)]).routes[0].bin_ids == ("B1", "B3", "B2")


def test_sys_03_limited_truck_capacity_leaves_unassigned_bins():
    """FR-5, FR-6: overflow beyond fleet capacity is reported once, in priority order."""
    reg = build_city()
    reg.get("B3").update_fill_level(80)
    plan = plan_routes(reg, [Truck("T1", 1)])
    assert [r.bin_ids for r in plan.routes] == [("B1",)]
    assert plan.unassigned_bin_ids == ("B3", "B2")  # 80 before 72, no duplicates, none lost
    assert plan_routes(reg, []).unassigned_bin_ids == ("B1", "B3", "B2")


def test_sys_04_removed_bin_and_stale_route_are_safe():
    """FR-1, FR-7: a decommissioned bin is not planned and a stale route changes nothing."""
    reg = build_city()
    plan = plan_routes(reg, [Truck("T1", 5)])
    reg.remove("B1")
    with pytest.raises(KeyError):
        complete_route(plan.routes[0], reg)
    assert not plan.routes[0].completed
    assert reg.get("B2").fill_level == 72  # no partial emptying

    fresh = plan_routes(reg, [Truck("T1", 5)])
    assert fresh.routes[0].bin_ids == ("B2",)
    assert status_summary(reg.all()) == {"OK": 1, "NEARLY_FULL": 1, "FULL": 0}
