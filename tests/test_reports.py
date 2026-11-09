import pytest

from waste_mgmt.bins import Bin
from waste_mgmt.reports import (
    average_fill_level,
    render_text_report,
    status_summary,
    summary_by_waste_type,
)


def sample():
    return [
        Bin("B1", "a", 100, "general", 100),
        Bin("B2", "b", 100, "organic", 50),
        Bin("B3", "c", 100, "organic", 10),
    ]


def test_tc_rp_01_average_empty_list():
    assert average_fill_level([]) == 0.0


def test_tc_rp_02_average_fill_level():
    assert average_fill_level(sample()) == 53.33


def test_tc_rp_03_status_summary():
    assert status_summary(sample()) == {"OK": 2, "NEARLY_FULL": 0, "FULL": 1}


def test_tc_rp_04_summary_by_waste_type():
    assert summary_by_waste_type(sample()) == {"general": 100.0, "organic": 30.0}


def test_tc_rp_05_text_report_no_bins():
    assert render_text_report([]) == "No bins registered."


def test_tc_rp_06_text_report_contents():
    text = render_text_report(sample())
    assert "Total bins: 3" in text and "organic: 30.0%" in text


@pytest.mark.parametrize(
    "level,expected",
    [(0, "OK"), (69, "OK"), (70, "NEARLY_FULL"), (89, "NEARLY_FULL"), (90, "FULL"), (100, "FULL")],
)
def test_tc_rp_07_status_summary_boundaries(level, expected):
    summary = status_summary([Bin("B1", "x", 100, fill_level=level)])
    assert summary[expected] == 1 and sum(summary.values()) == 1


def test_tc_rp_08_status_summary_empty_has_all_keys():
    assert status_summary([]) == {"OK": 0, "NEARLY_FULL": 0, "FULL": 0}


def test_tc_rp_09_reports_do_not_modify_bins():
    bins = sample()
    before = [(b.bin_id, b.fill_level) for b in bins]
    render_text_report(bins)
    summary_by_waste_type(bins)
    assert [(b.bin_id, b.fill_level) for b in bins] == before
