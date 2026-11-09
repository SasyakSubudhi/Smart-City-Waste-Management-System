"""Command-line demo of the Smart City Waste Management System.

Run from the repository root:  python demo.py
Walks through one full cycle: register bins, read sensors, raise alerts,
plan truck routes, confirm a collection and print the city report.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from waste_mgmt.alerts import format_alert, generate_alerts  # noqa: E402
from waste_mgmt.bins import Bin, BinRegistry  # noqa: E402
from waste_mgmt.reports import render_text_report  # noqa: E402
from waste_mgmt.routing import Truck, complete_route, plan_routes  # noqa: E402


def step(title):
    print(f"\n=== {title} ===")


def show_alerts(registry):
    alerts = generate_alerts(registry.all())
    if not alerts:
        print("No alerts.")
    for alert in alerts:
        print(format_alert(alert))


def main():
    registry = BinRegistry()

    step("1. Register bins (FR-1)")
    for bin_ in (
        Bin("B1", "MG Road", 120, "general", 95),
        Bin("B2", "Indiranagar", 100, "organic", 72),
        Bin("B3", "Koramangala", 80, "recyclable", 20),
        Bin("B4", "Jayanagar", 90, "general", 85),
    ):
        registry.add(bin_)
        print(f"Added {bin_.bin_id} at {bin_.location}: {bin_.fill_level}% ({bin_.status})")

    step("2. Invalid sensor reading is rejected (FR-2)")
    try:
        registry.get("B3").update_fill_level(float("nan"))
    except ValueError as error:
        print(f"Rejected: {error}")
    print(f"B3 still at {registry.get('B3').fill_level}%")

    step("3. Alerts, CRITICAL first (FR-4)")
    show_alerts(registry)

    step("4. Plan routes with two trucks of capacity 2 and 1 (FR-5, FR-6)")
    plan = plan_routes(registry, [Truck("T1", 2), Truck("T2", 1)])
    for route in plan.routes:
        print(f"{route.truck.truck_id}: {', '.join(route.bin_ids)}")
    print(f"Unassigned: {', '.join(plan.unassigned_bin_ids) or 'none'}")

    step("5. Confirm collection for every route (FR-7)")
    for route in plan.routes:
        complete_route(route, registry)
        print(f"{route.truck.truck_id} completed")

    step("6. Alerts after collection")
    show_alerts(registry)

    step("7. City report (FR-8)")
    print(render_text_report(registry.all()))


if __name__ == "__main__":
    main()
