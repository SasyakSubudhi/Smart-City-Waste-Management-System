import pytest
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.routing import Truck, plan_routes, complete_route
from waste_mgmt.dashboard import attempt, bin_rows, alert_rows, route_rows


def city():
    registry = BinRegistry()
    registry.add(Bin("A", "Park", 100, fill_level=80))
    registry.add(Bin("B", "Market", 200, "organic", 95))
    return registry


def test_tc_ui_01_attempt_returns_result_and_passes_arguments():
    assert attempt(pow, 2, 3) == (True, 8)


@pytest.mark.parametrize("error", [ValueError("invalid"), KeyError("missing")])
def test_tc_ui_02_attempt_preserves_domain_errors(error):
    def fail():
        raise error
    assert attempt(fail) == (False, str(error))


def test_tc_ui_03_unexpected_errors_propagate():
    with pytest.raises(TypeError):
        attempt(lambda: 1 + "x")


def test_tc_ui_04_bin_rows_are_read_only():
    registry = city()
    assert bin_rows(BinRegistry()) == []
    rows = bin_rows(registry)
    assert rows[0] == {"Bin ID": "A", "Location": "Park", "Capacity (litres)": 100,
                       "Waste type": "general", "Fill (%)": 80, "Status": "NEARLY_FULL"}
    rows[0]["Fill (%)"] = 0
    assert registry.get("A").fill_level == 80


def test_tc_ui_05_alert_rows_preserve_priority_and_format():
    assert alert_rows(BinRegistry()) == []
    rows = alert_rows(city())
    assert [r["Severity"] for r in rows] == ["CRITICAL", "WARNING"]
    assert rows[0] == {"Bin ID": "B", "Severity": "CRITICAL",
                       "Alert": "[CRITICAL] Bin B at Market is 95% full"}


def test_tc_ui_06_route_rows_none_and_empty():
    assert route_rows(None) == []
    assert route_rows(plan_routes(BinRegistry(), [])) == []


def test_tc_ui_07_route_rows_show_completion_without_mutation():
    registry = city()
    plan = plan_routes(registry, [Truck("T1", 2)])
    assert route_rows(plan) == [{"Truck": "T1", "Bin IDs": "B, A", "Completed": False}]
    assert registry.get("B").fill_level == 95
    complete_route(plan.routes[0], registry)
    assert route_rows(plan)[0]["Completed"] is True
