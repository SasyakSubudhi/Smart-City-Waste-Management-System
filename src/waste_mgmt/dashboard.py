"""Presentation adapters; validation and decisions remain in domain modules."""

from .alerts import generate_alerts, format_alert


def attempt(action, *args):
    """Return a domain result or its original validation/lookup error message."""
    try:
        return True, action(*args)
    except KeyError as error:
        return False, str(error.args[0]) if error.args else str(error)
    except ValueError as error:
        return False, str(error)


def bin_rows(registry):
    return [{"Bin ID": b.bin_id, "Location": b.location,
             "Capacity (litres)": b.capacity_litres, "Waste type": b.waste_type,
             "Fill (%)": b.fill_level, "Status": b.status} for b in registry.all()]


def alert_rows(registry):
    return [{"Bin ID": a.bin_id, "Severity": a.severity,
             "Alert": format_alert(a)} for a in generate_alerts(registry.all())]


def filter_alert_rows(rows, severity="All"):
    """Return a fresh view of alert rows without changing their priority order."""
    if severity not in ("All", "CRITICAL", "WARNING"):
        raise ValueError("severity must be All, CRITICAL or WARNING")
    return [dict(row) for row in rows if severity == "All" or row["Severity"] == severity]


def route_rows(plan):
    if plan is None:
        return []
    return [{"Truck": r.truck.truck_id, "Bin IDs": ", ".join(r.bin_ids),
             "Completed": r.completed} for r in plan.routes]
