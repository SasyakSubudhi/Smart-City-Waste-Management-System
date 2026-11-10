from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


@pytest.fixture
def app():
    result = AppTest.from_file(str(APP), default_timeout=15).run()
    assert not result.exception
    return result


def click(app, label):
    next(button for button in app.button if button.label == label).click().run()
    assert not app.exception
    return app


def register(app, bin_id="B1"):
    app.text_input(key="new_id").set_value(bin_id)
    app.text_input(key="location").set_value("Park")
    return click(app, "Register bin")


def reading(app, value, bin_id="B1"):
    app.text_input(key="sensor_id").set_value(bin_id)
    app.number_input(key="reading").set_value(value)
    return click(app, "Send reading")


def test_tc_ui_08_start_empty(app):
    assert [tab.label for tab in app.tabs] == ["Bins", "Alerts", "Collection routes", "City report"]
    assert app.session_state.registry.all() == []
    assert app.session_state.plan is None
    assert app.metric[0].value == "0"
    assert app.text[0].value == "No bins registered."
    assert app.info[0].value == "No alerts."


def test_tc_ui_09_register_and_persist(app):
    register(app)
    assert app.success[0].value == "Bin registered."
    assert app.dataframe[0].value.iloc[0]["Status"] == "OK"
    app.run()
    assert app.session_state.registry.get("B1").location == "Park"
    assert app.metric[0].value == "1"


def test_tc_ui_10_duplicate_id_error(app):
    register(app)
    register(app)
    assert app.error[0].value == "bin B1 already registered"
    assert len(app.session_state.registry.all()) == 1


def test_tc_ui_11_empty_id_error(app):
    register(app, "")
    assert app.error[0].value == "bin_id must not be empty"
    assert app.session_state.registry.all() == []


def test_tc_ui_12_sensor_updates_alerts_and_report(app):
    register(app)
    reading(app, 95)
    assert app.success[0].value == "Sensor reading updated."
    assert app.dataframe[1].value.iloc[0]["Severity"] == "CRITICAL"
    assert [m.value for m in app.metric] == ["1", "95.0%", "0", "1"]
    assert "Total bins: 1" in app.text[0].value


def test_tc_ui_13_unknown_bin_error(app):
    reading(app, 90, "missing")
    assert app.error[0].value == "bin missing not found"


@pytest.mark.parametrize("value", [-1, 101])
def test_tc_ui_14_out_of_range_preserves_state(app, value):
    register(app)
    reading(app, 80)
    reading(app, value)
    assert app.error[0].value == "fill level must be between 0 and 100"
    assert app.session_state.registry.get("B1").fill_level == 80


def test_tc_ui_15_remove_and_unknown_remove(app):
    register(app)
    app.text_input(key="remove_id").set_value("B1")
    click(app, "Remove bin")
    assert app.success[0].value == "Bin removed."
    assert app.session_state.registry.all() == []
    click(app, "Remove bin")
    assert app.error[0].value == "bin B1 not found"


def test_tc_ui_16_plan_and_confirm_collection(app):
    register(app)
    reading(app, 95)
    click(app, "Plan routes")
    assert app.session_state.plan.routes[0].bin_ids == ("B1",)
    assert app.session_state.registry.get("B1").fill_level == 95
    click(app, "Confirm all collections")
    assert app.success[0].value == "All collections confirmed."
    assert app.session_state.registry.get("B1").fill_level == 0
    assert app.session_state.plan is None
    assert app.info[0].value == "No alerts."
    assert app.metric[3].value == "0"


def test_tc_ui_17_nothing_due(app):
    register(app)
    click(app, "Plan routes")
    assert app.session_state.plan.routes == ()
    assert any(info.value == "No routes planned." for info in app.info)
    assert next(b for b in app.button if b.label == "Confirm all collections").disabled


def test_tc_ui_18_backlog_and_empty_fleet(app):
    register(app)
    reading(app, 90)
    register(app, "B2")
    reading(app, 80, "B2")
    app.number_input(key="truck_capacity").set_value(1)
    click(app, "Plan routes")
    assert app.session_state.plan.unassigned_bin_ids == ("B2",)
    assert any("B2" in m.value for m in app.markdown)
    app.number_input(key="truck_count").set_value(0)
    click(app, "Plan routes")
    assert app.session_state.plan.unassigned_bin_ids == ("B1", "B2")


def test_tc_ui_19_edit_invalidates_saved_plan(app):
    register(app)
    reading(app, 90)
    click(app, "Plan routes")
    reading(app, 50)
    assert app.session_state.plan is None


def test_tc_ui_20_sessions_are_isolated(app):
    register(app)
    other = AppTest.from_file(str(APP), default_timeout=15).run()
    assert other.session_state.registry.all() == []


def test_tc_ui_24_severity_filter_and_reset(app):
    register(app)
    reading(app, 95)
    register(app, "B2")
    reading(app, 80, "B2")
    assert app.selectbox(key="alert_severity").value == "All"
    assert app.dataframe[1].value["Severity"].tolist() == ["CRITICAL", "WARNING"]
    for severity, expected in [("CRITICAL", ["B1"]), ("WARNING", ["B2"]),
                               ("All", ["B1", "B2"])]:
        app.selectbox(key="alert_severity").select(severity).run()
        assert not app.exception
        assert app.dataframe[1].value["Bin ID"].tolist() == expected
    assert app.session_state.registry.get("B1").fill_level == 95
    assert app.session_state.registry.get("B2").fill_level == 80


def test_tc_ui_25_filter_no_match_and_collection_refresh(app):
    register(app)
    reading(app, 80)
    app.selectbox(key="alert_severity").select("CRITICAL").run()
    assert any(i.value == "No alerts match this severity." for i in app.info)
    app.selectbox(key="alert_severity").select("WARNING").run()
    click(app, "Plan routes")
    click(app, "Confirm all collections")
    assert app.selectbox(key="alert_severity").value == "WARNING"
    assert any(i.value == "No alerts match this severity." for i in app.info)
    assert app.session_state.registry.get("B1").fill_level == 0


def test_tc_ui_26_confirmation_identifies_remaining_backlog(app):
    register(app)
    reading(app, 95)
    register(app, "B2")
    reading(app, 80, "B2")
    app.number_input(key="truck_capacity").set_value(1)
    click(app, "Plan routes")
    click(app, "Confirm all collections")
    assert app.success[0].value == (
        "All planned collections confirmed. Unassigned bins still need collection: B2. "
        "Plan routes again for the remaining bins.")
    assert app.session_state.plan is None
    assert app.session_state.registry.get("B1").fill_level == 0
    assert app.session_state.registry.get("B2").fill_level == 80
    assert app.dataframe[1].value["Bin ID"].tolist() == ["B2"]
    assert [m.value for m in app.metric] == ["2", "40.0%", "1", "0"]
    click(app, "Plan routes")
    assert app.session_state.plan.routes[0].bin_ids == ("B2",)
    click(app, "Confirm all collections")
    assert app.success[0].value == "All collections confirmed."
    assert app.session_state.registry.get("B2").fill_level == 0
