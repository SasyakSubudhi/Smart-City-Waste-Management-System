# Test Case Document

**Project:** Smart City Waste Management System

Updated after the sprints to match the implemented behaviour. Each test case is implemented in code under `tests/`; the Test ID is derived from the test function name.

| Test ID | Module | Description | Requirement | Type | Automated in |
|---|---|---|---|---|---|
| TC-BIN-01 | bins | Create valid bin | FR-1..3 | Unit | `test_bins.py::test_tc_bin_01_create_valid_bin` |
| TC-BIN-02 | bins | Invalid bin rejected | FR-1..3 | Unit | `test_bins.py::test_tc_bin_02_invalid_bin_rejected` |
| TC-BIN-03 | bins | Fill level out of range | FR-1..3 | Unit | `test_bins.py::test_tc_bin_03_fill_level_out_of_range` |
| TC-BIN-04 | bins | Status boundaries | FR-1..3 | Unit | `test_bins.py::test_tc_bin_04_status_boundaries` |
| TC-BIN-05 | bins | Empty resets level | FR-1..3 | Unit | `test_bins.py::test_tc_bin_05_empty_resets_level` |
| TC-BIN-06 | bins | Registry add get all | FR-1..3 | Unit | `test_bins.py::test_tc_bin_06_registry_add_get_all` |
| TC-BIN-07 | bins | Registry duplicate rejected | FR-1..3 | Unit | `test_bins.py::test_tc_bin_07_registry_duplicate_rejected` |
| TC-BIN-08 | bins | Registry missing bin | FR-1..3 | Unit | `test_bins.py::test_tc_bin_08_registry_missing_bin` |
| TC-BIN-09 | bins | Registry remove | FR-1..3 | Unit | `test_bins.py::test_tc_bin_09_registry_remove` |
| TC-BIN-10 | bins | Registry filter by status | FR-1..3 | Unit | `test_bins.py::test_tc_bin_10_registry_filter_by_status` |
| TC-BIN-11 | bins | Non integer fill level rejected | FR-1..3 | Unit | `test_bins.py::test_tc_bin_11_non_integer_fill_level_rejected` |
| TC-BIN-12 | bins | Non integer fill level rejected in constructor | FR-1..3 | Unit | `test_bins.py::test_tc_bin_12_non_integer_fill_level_rejected_in_constructor` |
| TC-RT-01 | routing | Select threshold inclusive | FR-5..7 | Unit | `test_routing.py::test_tc_rt_01_select_threshold_inclusive` |
| TC-RT-02 | routing | Fullest first and deterministic ties | FR-5..7 | Unit | `test_routing.py::test_tc_rt_02_fullest_first_and_deterministic_ties` |
| TC-RT-03 | routing | Capacity and multiple trucks | FR-5..7 | Unit | `test_routing.py::test_tc_rt_03_capacity_and_multiple_trucks` |
| TC-RT-04 | routing | Custom threshold | FR-5..7 | Unit | `test_routing.py::test_tc_rt_04_custom_threshold` |
| TC-RT-05 | routing | Overflow and no fleet | FR-5..7 | Unit | `test_routing.py::test_tc_rt_05_overflow_and_no_fleet` |
| TC-RT-06 | routing | Empty registry and no due bins | FR-5..7 | Unit | `test_routing.py::test_tc_rt_06_empty_registry_and_no_due_bins` |
| TC-RT-07 | routing | Invalid threshold | FR-5..7 | Unit | `test_routing.py::test_tc_rt_07_invalid_threshold` |
| TC-RT-08 | routing | Complete route | FR-5..7 | Unit | `test_routing.py::test_tc_rt_08_complete_route` |
| TC-RT-09 | routing | Invalid truck | FR-5..7 | Unit | `test_routing.py::test_tc_rt_09_invalid_truck` |
| TC-RT-10 | routing | Invalid fleet | FR-5..7 | Unit | `test_routing.py::test_tc_rt_10_invalid_fleet` |
| TC-RT-11 | routing | Missing bin atomic completion | FR-5..7 | Unit | `test_routing.py::test_tc_rt_11_missing_bin_atomic_completion` |
| TC-RT-12 | routing | Invalid route | FR-5..7 | Unit | `test_routing.py::test_tc_rt_12_invalid_route` |
| TC-AL-01 | alerts | Empty and ok | FR-4 | Unit | `test_alerts.py::test_tc_al_01_empty_and_ok` |
| TC-AL-02 | alerts | Boundaries | FR-4 | Unit | `test_alerts.py::test_tc_al_02_boundaries` |
| TC-AL-03 | alerts | Priority stability and no mutation | FR-4 | Unit | `test_alerts.py::test_tc_al_03_priority_stability_and_no_mutation` |
| TC-AL-04 | alerts | Format | FR-4 | Unit | `test_alerts.py::test_tc_al_04_format` |
| TC-AL-05 | alerts | Updated reading empty and snapshot | FR-4 | Unit | `test_alerts.py::test_tc_al_05_updated_reading_empty_and_snapshot` |
| TC-AL-06 | alerts | Registry route completion and backlog | FR-4 | Unit | `test_alerts.py::test_tc_al_06_registry_route_completion_and_backlog` |
| TC-AL-07 | alerts | Mixed boundaries in one batch | FR-4 | Unit | `test_alerts.py::test_tc_al_07_mixed_boundaries_in_one_batch` |
| TC-AL-08 | alerts | Many equal severity keep input order | FR-4 | Unit | `test_alerts.py::test_tc_al_08_many_equal_severity_keep_input_order` |
| TC-AL-09 | alerts | Emptying preserves saved alert and its format | FR-4 | Unit | `test_alerts.py::test_tc_al_09_emptying_preserves_saved_alert_and_its_format` |
| TC-RP-01 | reports | Average empty list | FR-8 | Unit | `test_reports.py::test_tc_rp_01_average_empty_list` |
| TC-RP-02 | reports | Average fill level | FR-8 | Unit | `test_reports.py::test_tc_rp_02_average_fill_level` |
| TC-RP-03 | reports | Status summary | FR-8 | Unit | `test_reports.py::test_tc_rp_03_status_summary` |
| TC-RP-04 | reports | Summary by waste type | FR-8 | Unit | `test_reports.py::test_tc_rp_04_summary_by_waste_type` |
| TC-RP-05 | reports | Text report no bins | FR-8 | Unit | `test_reports.py::test_tc_rp_05_text_report_no_bins` |
| TC-RP-06 | reports | Text report contents | FR-8 | Unit | `test_reports.py::test_tc_rp_06_text_report_contents` |
| TC-RP-07 | reports | Status summary boundaries | FR-8 | Unit | `test_reports.py::test_tc_rp_07_status_summary_boundaries` |
| TC-RP-08 | reports | Status summary empty has all keys | FR-8 | Unit | `test_reports.py::test_tc_rp_08_status_summary_empty_has_all_keys` |
| TC-RP-09 | reports | Reports do not modify bins | FR-8 | Unit | `test_reports.py::test_tc_rp_09_reports_do_not_modify_bins` |
| SYS-01 | system | Full collection cycle | FR-1..7 | System | `test_system.py::test_sys_01_full_collection_cycle` |
| SYS-02 | system | Sensor update changes alert and routing | FR-1..7 | System | `test_system.py::test_sys_02_sensor_update_changes_alert_and_routing` |
| SYS-03 | system | Limited truck capacity leaves unassigned bins | FR-1..7 | System | `test_system.py::test_sys_03_limited_truck_capacity_leaves_unassigned_bins` |
| SYS-04 | system | Removed bin and stale route are safe | FR-1..7 | System | `test_system.py::test_sys_04_removed_bin_and_stale_route_are_safe` |
