import pytest

from waste_mgmt.bins import Bin, BinRegistry


def test_tc_bin_01_create_valid_bin():
    b = Bin("B1", "MG Road", 120, "organic", 30)
    assert b.bin_id == "B1" and b.fill_level == 30 and b.waste_type == "organic"


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(bin_id="", location="x", capacity_litres=100),
        dict(bin_id="B1", location="x", capacity_litres=0),
        dict(bin_id="B1", location="x", capacity_litres=100, waste_type="metal"),
        dict(bin_id="B1", location="x", capacity_litres=100, fill_level=150),
    ],
)
def test_tc_bin_02_invalid_bin_rejected(kwargs):
    with pytest.raises(ValueError):
        Bin(**kwargs)


@pytest.mark.parametrize("level", [-1, 101])
def test_tc_bin_03_fill_level_out_of_range(level):
    b = Bin("B1", "x", 100)
    with pytest.raises(ValueError):
        b.update_fill_level(level)


@pytest.mark.parametrize(
    "level,expected",
    [(0, "OK"), (69, "OK"), (70, "NEARLY_FULL"), (89, "NEARLY_FULL"), (90, "FULL"), (100, "FULL")],
)
def test_tc_bin_04_status_boundaries(level, expected):
    assert Bin("B1", "x", 100, fill_level=level).status == expected


def test_tc_bin_05_empty_resets_level():
    b = Bin("B1", "x", 100, fill_level=95)
    b.empty()
    assert b.fill_level == 0 and b.status == "OK"


def test_tc_bin_06_registry_add_get_all():
    r = BinRegistry()
    b = Bin("B1", "x", 100)
    r.add(b)
    assert r.get("B1") is b and r.all() == [b]


def test_tc_bin_07_registry_duplicate_rejected():
    r = BinRegistry()
    r.add(Bin("B1", "x", 100))
    with pytest.raises(ValueError):
        r.add(Bin("B1", "y", 100))


def test_tc_bin_08_registry_missing_bin():
    r = BinRegistry()
    with pytest.raises(KeyError):
        r.get("nope")
    with pytest.raises(KeyError):
        r.remove("nope")


def test_tc_bin_09_registry_remove():
    r = BinRegistry()
    r.add(Bin("B1", "x", 100))
    r.remove("B1")
    assert r.all() == []


def test_tc_bin_10_registry_filter_by_status():
    r = BinRegistry()
    r.add(Bin("B1", "x", 100, fill_level=95))
    r.add(Bin("B2", "x", 100, fill_level=10))
    assert [b.bin_id for b in r.by_status("FULL")] == ["B1"]


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True, False, 50.5, "50", None])
def test_tc_bin_11_non_integer_fill_level_rejected(bad):
    b = Bin("B1", "x", 100)
    with pytest.raises(ValueError):
        b.update_fill_level(bad)
    assert b.fill_level == 0


def test_tc_bin_12_non_integer_fill_level_rejected_in_constructor():
    with pytest.raises(ValueError):
        Bin("B1", "x", 100, fill_level=float("nan"))
