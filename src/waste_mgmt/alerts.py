"""FR-4 overflow alerts. AI-assisted implementation for Shreya's review."""

from dataclasses import dataclass
from .bins import Bin


@dataclass(frozen=True)
class Alert:
    bin_id: str
    severity: str
    message: str


def generate_alerts(bins: list[Bin]) -> list[Alert]:
    """Return fresh snapshots, critical first; preserve input order within severity.

    Read through Bin.status so boundary policy stays in the domain model.
    Does not mutate bins or retain alerts between calls.
    """
    alerts = []
    for bin in bins:
        status = bin.status
        if status == "OK":
            continue
        severity = "CRITICAL" if status == "FULL" else "WARNING"
        alerts.append(Alert(bin.bin_id, severity,
                            f"Bin {bin.bin_id} at {bin.location} is {bin.fill_level}% full"))
    return sorted(alerts, key=lambda alert: alert.severity != "CRITICAL")


def format_alert(alert: Alert) -> str:
    """Render an alert for plain-text display (not HTML)."""
    return f"[{alert.severity}] {alert.message}"
