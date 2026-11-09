from dataclasses import FrozenInstanceError
import pytest
from waste_mgmt.bins import Bin, BinRegistry
from waste_mgmt.alerts import generate_alerts, format_alert
from waste_mgmt.routing import Truck, plan_routes, complete_route


def make_bin(bin_id="B1", level=0):
    return Bin(bin_id, "City centre", 100, fill_level=level)


def test_tc_al_01_empty_and_ok():
    assert generate_alerts([]) == []
    assert generate_alerts([make_bin(level=69)]) == []


@pytest.mark.parametrize("level,severity", [(0,None),(69,None),(70,"WARNING"),
                                          (89,"WARNING"),(90,"CRITICAL"),(100,"CRITICAL")])
def test_tc_al_02_boundaries(level, severity):
    alerts = generate_alerts([make_bin(level=level)])
    assert [a.severity for a in alerts] == ([] if severity is None else [severity])


def test_tc_al_03_priority_stability_and_no_mutation():
    bins = [make_bin("W2",80),make_bin("C2",90),make_bin("O",10),
            make_bin("W1",70),make_bin("C1",100)]
    before = [(b.bin_id,b.fill_level) for b in bins]
    alerts = generate_alerts(bins)
    assert [a.bin_id for a in alerts] == ["C2","C1","W2","W1"]
    assert [(b.bin_id,b.fill_level) for b in bins] == before


@pytest.mark.parametrize("level,severity", [(70,"WARNING"),(100,"CRITICAL")])
def test_tc_al_04_format(level,severity):
    alert = generate_alerts([make_bin(level=level)])[0]
    assert alert.bin_id == "B1"
    assert alert.message == f"Bin B1 at City centre is {level}% full"
    assert format_alert(alert) == f"[{severity}] Bin B1 at City centre is {level}% full"


def test_tc_al_05_updated_reading_empty_and_snapshot():
    bin = make_bin(level=69)
    assert generate_alerts([bin]) == []
    bin.update_fill_level(70)
    old = generate_alerts([bin])[0]
    bin.update_fill_level(90)
    assert generate_alerts([bin])[0].severity == "CRITICAL"
    assert old.severity == "WARNING" and "70%" in old.message
    with pytest.raises(FrozenInstanceError):
        old.severity = "CRITICAL"
    bin.empty()
    assert generate_alerts([bin]) == []


def test_tc_al_06_registry_route_completion_and_backlog():
    registry = BinRegistry()
    for bin in [make_bin("A",95),make_bin("B",80),make_bin("C",10)]:
        registry.add(bin)
    plan = plan_routes(registry,[Truck("T",1)])
    assert plan.unassigned_bin_ids == ("B",)
    assert [a.bin_id for a in generate_alerts(registry.all())] == ["A","B"]
    complete_route(plan.routes[0],registry)
    assert [a.bin_id for a in generate_alerts(registry.all())] == ["B"]
    assert registry.get("C").fill_level == 10


def test_tc_al_07_mixed_boundaries_in_one_batch():
    bins = [make_bin(f"B{level}", level) for level in (69, 70, 89, 90, 100)]
    alerts = generate_alerts(bins)
    assert [(a.bin_id, a.severity) for a in alerts] == [
        ("B90", "CRITICAL"), ("B100", "CRITICAL"),
        ("B70", "WARNING"), ("B89", "WARNING"),
    ]
    assert [b.fill_level for b in bins] == [69, 70, 89, 90, 100]


@pytest.mark.parametrize("level,severity", [(80, "WARNING"), (95, "CRITICAL")])
def test_tc_al_08_many_equal_severity_keep_input_order(level, severity):
    # Reverse IDs and alternating fill values catch accidental ID/fill sorting.
    bins = [make_bin(f"B{i:02d}", level + i % 2) for i in range(39, -1, -1)]
    expected = [b.bin_id for b in bins]
    first = generate_alerts(bins)
    second = generate_alerts(bins)
    assert [a.bin_id for a in first] == expected
    assert all(a.severity == severity for a in first)
    assert first == second
    assert first is not second


@pytest.mark.parametrize("level,severity", [(70, "WARNING"), (90, "CRITICAL")])
def test_tc_al_09_emptying_preserves_saved_alert_and_its_format(level, severity):
    bin = make_bin("saved", level)
    alerts = generate_alerts([bin])
    expected_message = f"Bin saved at City centre is {level}% full"
    expected_text = f"[{severity}] {expected_message}"
    bin.empty()
    # The old snapshot keeps its reading and severity after source state changes.
    assert alerts[0].message == expected_message
    assert alerts[0].severity == severity
    assert format_alert(alerts[0]) == expected_text
    assert generate_alerts([bin]) == []
