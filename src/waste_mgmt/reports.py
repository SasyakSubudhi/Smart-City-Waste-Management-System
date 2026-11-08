"""FR-8 summary statistics and plain-text city report (owner: Shruti Choudhary).

Functions take a list of bins (use ``registry.all()``). They only read bins and
never change them. An empty list returns zero-valued results, not an error.
"""

from .bins import Bin

STATUSES = ("OK", "NEARLY_FULL", "FULL")


def average_fill_level(bins: list[Bin]) -> float:
    """Mean fill percentage rounded to 2 places; 0.0 when there are no bins."""
    if not bins:
        return 0.0
    return round(sum(b.fill_level for b in bins) / len(bins), 2)


def status_summary(bins: list[Bin]) -> dict:
    """Count of bins per status; every status key is always present."""
    summary = {status: 0 for status in STATUSES}
    for b in bins:
        summary[b.status] += 1
    return summary


def summary_by_waste_type(bins: list[Bin]) -> dict:
    """Mean fill level per waste type."""
    groups: dict = {}
    for b in bins:
        groups.setdefault(b.waste_type, []).append(b)
    return {t: average_fill_level(items) for t, items in groups.items()}


def render_text_report(bins: list[Bin]) -> str:
    """Plain-text city summary (not HTML)."""
    if not bins:
        return "No bins registered."
    s = status_summary(bins)
    lines = [
        "SMART CITY WASTE REPORT",
        f"Total bins: {len(bins)}",
        f"Average fill: {average_fill_level(bins)}%",
        f"OK: {s['OK']}  Nearly full: {s['NEARLY_FULL']}  Full: {s['FULL']}",
    ]
    for waste_type, avg in sorted(summary_by_waste_type(bins).items()):
        lines.append(f"  {waste_type}: {avg}%")
    return "\n".join(lines)
