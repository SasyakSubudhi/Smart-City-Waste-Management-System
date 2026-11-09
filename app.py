"""Streamlit presentation layer for the waste-management package."""

import sys
from pathlib import Path

import streamlit as st

# Support `streamlit run app.py` from a clone without installing the src package.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from waste_mgmt.bins import Bin, BinRegistry, VALID_TYPES
from waste_mgmt.dashboard import attempt, bin_rows, alert_rows, route_rows, filter_alert_rows
from waste_mgmt.routing import Truck, plan_routes, complete_route
from waste_mgmt.reports import average_fill_level, status_summary, render_text_report


def show_result(ok, result, message):
    """Invalidate stale plans after edits and render the refreshed session."""
    if ok:
        st.session_state.plan = None
        st.session_state.notice = message
        st.rerun()
    else:
        st.error(result)


st.set_page_config(page_title="City waste dashboard", page_icon="♻", layout="wide")
st.title("City waste dashboard")
st.caption("Monitor bins, review alerts and confirm completed collections.")
if "registry" not in st.session_state:
    st.session_state.registry = BinRegistry()
if "plan" not in st.session_state:
    st.session_state.plan = None
registry = st.session_state.registry
if "notice" in st.session_state:
    st.success(st.session_state.pop("notice"))

bins_tab, alerts_tab, routes_tab, report_tab = st.tabs(
    ["Bins", "Alerts", "Collection routes", "City report"])
with bins_tab:
    st.subheader("Manage bins")
    with st.form("register"):
        st.markdown("#### Register a bin")
        bin_id = st.text_input("Bin ID", key="new_id")
        location = st.text_input("Location", key="location")
        capacity = st.number_input("Capacity (litres)", value=100, step=1, key="capacity")
        waste_type = st.selectbox("Waste type", VALID_TYPES, key="waste_type")
        if st.form_submit_button("Register bin"):
            ok, result = attempt(lambda: registry.add(Bin(bin_id, location, capacity, waste_type)))
            show_result(ok, result, "Bin registered.")
    with st.form("sensor"):
        st.markdown("#### Send a sensor reading")
        sensor_id = st.text_input("Bin ID for reading", key="sensor_id")
        reading = st.number_input("Fill level (%)", value=0, step=1, key="reading")
        if st.form_submit_button("Send reading"):
            ok, result = attempt(lambda: registry.get(sensor_id).update_fill_level(reading))
            show_result(ok, result, "Sensor reading updated.")
    with st.form("remove"):
        remove_id = st.text_input("Bin ID to remove", key="remove_id")
        if st.form_submit_button("Remove bin"):
            ok, result = attempt(registry.remove, remove_id)
            show_result(ok, result, "Bin removed.")
    st.dataframe(bin_rows(registry), hide_index=True, use_container_width=True)

with alerts_tab:
    st.subheader("Overflow alerts")
    severity = st.selectbox("Severity", ("All", "CRITICAL", "WARNING"), key="alert_severity")
    rows = filter_alert_rows(alert_rows(registry), severity)
    if rows:
        st.dataframe(rows, hide_index=True, use_container_width=True)
    else:
        st.info("No alerts." if severity == "All" else "No alerts match this severity.")

with routes_tab:
    st.subheader("Collection routes")
    st.caption("Planning does not empty bins. Confirm only after collection finishes. "
               "Editing a bin clears the saved plan; creating a plan replaces it.")
    with st.form("fleet"):
        count = st.number_input("Number of trucks", min_value=0, value=1, step=1, key="truck_count")
        capacity_bins = st.number_input("Bins per truck", min_value=1, value=5, step=1, key="truck_capacity")
        if st.form_submit_button("Plan routes"):
            ok, result = attempt(lambda: plan_routes(
                registry, [Truck(f"T{i + 1}", capacity_bins) for i in range(count)]))
            if ok:
                st.session_state.plan = result
                st.success("Routes planned.")
            else:
                st.error(result)
    plan = st.session_state.plan
    if plan is not None:
        st.dataframe(route_rows(plan), hide_index=True, use_container_width=True)
        st.write("Unassigned bins:", ", ".join(plan.unassigned_bin_ids) or "None")
        if not plan.routes:
            st.info("No routes planned.")
        if st.button("Confirm all collections", disabled=not plan.routes):
            for route in plan.routes:
                ok, result = attempt(complete_route, route, registry)
                if not ok:
                    st.error(result)
                    break
            else:
                show_result(True, None, "All collections confirmed.")

with report_tab:
    st.subheader("City report")
    bins = registry.all()
    counts = status_summary(bins)
    columns = st.columns(4)
    columns[0].metric("Total bins", len(bins))
    columns[1].metric("Average fill", f"{average_fill_level(bins)}%")
    columns[2].metric("Nearly full", counts["NEARLY_FULL"])
    columns[3].metric("Full", counts["FULL"])
    st.text(render_text_report(bins))
