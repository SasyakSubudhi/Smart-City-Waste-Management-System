import runpy
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent / "demo.py"


def test_demo_script_runs_full_cycle(capsys):
    runpy.run_path(str(DEMO), run_name="__main__")
    out = capsys.readouterr().out
    before, after = out.split("6. Alerts after collection")
    assert "[CRITICAL] Bin B1 at MG Road is 95% full" in before
    assert "Rejected: fill level must be an integer" in before
    assert "T1: B1, B4" in before and "T2: B2" in before
    assert "Unassigned: none" in before
    assert "No alerts." in after.split("7. City report")[0]
    assert "SMART CITY WASTE REPORT" in after and "Total bins: 4" in after
