# Unit Test Report

Project: Smart City Waste Management System

Date: 2026-11-09

Commit: 3fb2ce3

Environment: Python 3.12.10 on Windows 2025Server

Tool: pytest

**Overall: PASS**

## Summary

| Total | Passed | Failed | Skipped | Pass rate |
|---|---|---|---|---|
| 127 | 127 | 0 | 0 | 100.0% |

## Results

| # | Test file | Test case | Result | Time (s) |
|---|---|---|---|---|
| 1 | test_alerts.py | `test_tc_al_01_empty_and_ok` | PASS | 0.001 |
| 2 | test_alerts.py | `test_tc_al_02_boundaries[0-None]` | PASS | 0.001 |
| 3 | test_alerts.py | `test_tc_al_02_boundaries[69-None]` | PASS | 0.001 |
| 4 | test_alerts.py | `test_tc_al_02_boundaries[70-WARNING]` | PASS | 0.001 |
| 5 | test_alerts.py | `test_tc_al_02_boundaries[89-WARNING]` | PASS | 0.001 |
| 6 | test_alerts.py | `test_tc_al_02_boundaries[90-CRITICAL]` | PASS | 0.001 |
| 7 | test_alerts.py | `test_tc_al_02_boundaries[100-CRITICAL]` | PASS | 0.001 |
| 8 | test_alerts.py | `test_tc_al_03_priority_stability_and_no_mutation` | PASS | 0.001 |
| 9 | test_alerts.py | `test_tc_al_04_format[70-WARNING]` | PASS | 0.001 |
| 10 | test_alerts.py | `test_tc_al_04_format[100-CRITICAL]` | PASS | 0.001 |
| 11 | test_alerts.py | `test_tc_al_05_updated_reading_empty_and_snapshot` | PASS | 0.001 |
| 12 | test_alerts.py | `test_tc_al_06_registry_route_completion_and_backlog` | PASS | 0.001 |
| 13 | test_alerts.py | `test_tc_al_07_mixed_boundaries_in_one_batch` | PASS | 0.001 |
| 14 | test_alerts.py | `test_tc_al_08_many_equal_severity_keep_input_order[80-WARNING]` | PASS | 0.001 |
| 15 | test_alerts.py | `test_tc_al_08_many_equal_severity_keep_input_order[95-CRITICAL]` | PASS | 0.001 |
| 16 | test_alerts.py | `test_tc_al_09_emptying_preserves_saved_alert_and_its_format[70-WARNING]` | PASS | 0.001 |
| 17 | test_alerts.py | `test_tc_al_09_emptying_preserves_saved_alert_and_its_format[90-CRITICAL]` | PASS | 0.001 |
| 18 | test_app.py | `test_tc_ui_08_start_empty` | PASS | 0.738 |
| 19 | test_app.py | `test_tc_ui_09_register_and_persist` | PASS | 0.223 |
| 20 | test_app.py | `test_tc_ui_10_duplicate_id_error` | PASS | 0.190 |
| 21 | test_app.py | `test_tc_ui_11_empty_id_error` | PASS | 0.162 |
| 22 | test_app.py | `test_tc_ui_12_sensor_updates_alerts_and_report` | PASS | 0.201 |
| 23 | test_app.py | `test_tc_ui_13_unknown_bin_error` | PASS | 0.163 |
| 24 | test_app.py | `test_tc_ui_14_out_of_range_preserves_state[-1]` | PASS | 0.207 |
| 25 | test_app.py | `test_tc_ui_14_out_of_range_preserves_state[101]` | PASS | 0.238 |
| 26 | test_app.py | `test_tc_ui_15_remove_and_unknown_remove` | PASS | 0.205 |
| 27 | test_app.py | `test_tc_ui_16_plan_and_confirm_collection` | PASS | 0.241 |
| 28 | test_app.py | `test_tc_ui_17_nothing_due` | PASS | 0.187 |
| 29 | test_app.py | `test_tc_ui_18_backlog_and_empty_fleet` | PASS | 0.273 |
| 30 | test_app.py | `test_tc_ui_19_edit_invalidates_saved_plan` | PASS | 0.233 |
| 31 | test_app.py | `test_tc_ui_20_sessions_are_isolated` | PASS | 0.316 |
| 32 | test_app.py | `test_tc_ui_24_severity_filter_and_reset` | PASS | 0.295 |
| 33 | test_app.py | `test_tc_ui_25_filter_no_match_and_collection_refresh` | PASS | 0.280 |
| 34 | test_bins.py | `test_tc_bin_01_create_valid_bin` | PASS | 0.001 |
| 35 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs0]` | PASS | 0.001 |
| 36 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs1]` | PASS | 0.001 |
| 37 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs2]` | PASS | 0.001 |
| 38 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs3]` | PASS | 0.001 |
| 39 | test_bins.py | `test_tc_bin_03_fill_level_out_of_range[-1]` | PASS | 0.001 |
| 40 | test_bins.py | `test_tc_bin_03_fill_level_out_of_range[101]` | PASS | 0.001 |
| 41 | test_bins.py | `test_tc_bin_04_status_boundaries[0-OK]` | PASS | 0.001 |
| 42 | test_bins.py | `test_tc_bin_04_status_boundaries[69-OK]` | PASS | 0.001 |
| 43 | test_bins.py | `test_tc_bin_04_status_boundaries[70-NEARLY_FULL]` | PASS | 0.001 |
| 44 | test_bins.py | `test_tc_bin_04_status_boundaries[89-NEARLY_FULL]` | PASS | 0.001 |
| 45 | test_bins.py | `test_tc_bin_04_status_boundaries[90-FULL]` | PASS | 0.001 |
| 46 | test_bins.py | `test_tc_bin_04_status_boundaries[100-FULL]` | PASS | 0.001 |
| 47 | test_bins.py | `test_tc_bin_05_empty_resets_level` | PASS | 0.001 |
| 48 | test_bins.py | `test_tc_bin_06_registry_add_get_all` | PASS | 0.001 |
| 49 | test_bins.py | `test_tc_bin_07_registry_duplicate_rejected` | PASS | 0.001 |
| 50 | test_bins.py | `test_tc_bin_08_registry_missing_bin` | PASS | 0.001 |
| 51 | test_bins.py | `test_tc_bin_09_registry_remove` | PASS | 0.001 |
| 52 | test_bins.py | `test_tc_bin_10_registry_filter_by_status` | PASS | 0.001 |
| 53 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[nan]` | PASS | 0.001 |
| 54 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[inf]` | PASS | 0.001 |
| 55 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[True]` | PASS | 0.001 |
| 56 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[False]` | PASS | 0.001 |
| 57 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[50.5]` | PASS | 0.001 |
| 58 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[50]` | PASS | 0.001 |
| 59 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[None]` | PASS | 0.001 |
| 60 | test_bins.py | `test_tc_bin_12_non_integer_fill_level_rejected_in_constructor` | PASS | 0.001 |
| 61 | test_dashboard.py | `test_tc_ui_01_attempt_returns_result_and_passes_arguments` | PASS | 0.001 |
| 62 | test_dashboard.py | `test_tc_ui_02_attempt_preserves_domain_errors[error0-invalid]` | PASS | 0.001 |
| 63 | test_dashboard.py | `test_tc_ui_02_attempt_preserves_domain_errors[error1-missing]` | PASS | 0.001 |
| 64 | test_dashboard.py | `test_tc_ui_02_attempt_preserves_domain_errors[error2-]` | PASS | 0.001 |
| 65 | test_dashboard.py | `test_tc_ui_03_unexpected_errors_propagate` | PASS | 0.001 |
| 66 | test_dashboard.py | `test_tc_ui_04_bin_rows_are_read_only` | PASS | 0.001 |
| 67 | test_dashboard.py | `test_tc_ui_05_alert_rows_preserve_priority_and_format` | PASS | 0.001 |
| 68 | test_dashboard.py | `test_tc_ui_06_route_rows_none_and_empty` | PASS | 0.001 |
| 69 | test_dashboard.py | `test_tc_ui_07_route_rows_show_completion_without_mutation` | PASS | 0.001 |
| 70 | test_dashboard.py | `test_tc_ui_21_filter_preserves_rows_order_and_source[All-expected0]` | PASS | 0.001 |
| 71 | test_dashboard.py | `test_tc_ui_21_filter_preserves_rows_order_and_source[CRITICAL-expected1]` | PASS | 0.001 |
| 72 | test_dashboard.py | `test_tc_ui_21_filter_preserves_rows_order_and_source[WARNING-expected2]` | PASS | 0.001 |
| 73 | test_dashboard.py | `test_tc_ui_22_filter_empty_and_no_match` | PASS | 0.001 |
| 74 | test_dashboard.py | `test_tc_ui_23_filter_invalid_severity` | PASS | 0.001 |
| 75 | test_demo.py | `test_demo_script_runs_full_cycle` | PASS | 0.002 |
| 76 | test_generate_reports.py | `test_counts_include_skipped_tests` | PASS | 0.001 |
| 77 | test_generate_reports.py | `test_parse_junit_detects_pass_fail_and_skip` | PASS | 0.013 |
| 78 | test_generate_reports.py | `test_run_pytest_rejects_old_xml` | PASS | 0.003 |
| 79 | test_generate_reports.py | `test_run_pytest_rejects_invalid_xml` | PASS | 0.003 |
| 80 | test_generate_reports.py | `test_skipped_tests_make_report_fail` | PASS | 0.003 |
| 81 | test_generate_reports.py | `test_failed_pytest_makes_report_fail` | PASS | 0.002 |
| 82 | test_generate_reports.py | `test_low_coverage_fails` | PASS | 0.003 |
| 83 | test_generate_reports.py | `test_failed_coverage_command_fails` | PASS | 0.004 |
| 84 | test_generate_reports.py | `test_main_returns_failure_when_unit_tests_fail` | PASS | 0.001 |
| 85 | test_reports.py | `test_tc_rp_01_average_empty_list` | PASS | 0.001 |
| 86 | test_reports.py | `test_tc_rp_02_average_fill_level` | PASS | 0.001 |
| 87 | test_reports.py | `test_tc_rp_03_status_summary` | PASS | 0.001 |
| 88 | test_reports.py | `test_tc_rp_04_summary_by_waste_type` | PASS | 0.001 |
| 89 | test_reports.py | `test_tc_rp_05_text_report_no_bins` | PASS | 0.001 |
| 90 | test_reports.py | `test_tc_rp_06_text_report_contents` | PASS | 0.001 |
| 91 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[0-OK]` | PASS | 0.001 |
| 92 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[69-OK]` | PASS | 0.001 |
| 93 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[70-NEARLY_FULL]` | PASS | 0.001 |
| 94 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[89-NEARLY_FULL]` | PASS | 0.001 |
| 95 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[90-FULL]` | PASS | 0.001 |
| 96 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[100-FULL]` | PASS | 0.001 |
| 97 | test_reports.py | `test_tc_rp_08_status_summary_empty_has_all_keys` | PASS | 0.001 |
| 98 | test_reports.py | `test_tc_rp_09_reports_do_not_modify_bins` | PASS | 0.001 |
| 99 | test_routing.py | `test_tc_rt_01_select_threshold_inclusive` | PASS | 0.001 |
| 100 | test_routing.py | `test_tc_rt_02_fullest_first_and_deterministic_ties` | PASS | 0.001 |
| 101 | test_routing.py | `test_tc_rt_03_capacity_and_multiple_trucks` | PASS | 0.001 |
| 102 | test_routing.py | `test_tc_rt_04_custom_threshold[0-expected0]` | PASS | 0.001 |
| 103 | test_routing.py | `test_tc_rt_04_custom_threshold[100-expected1]` | PASS | 0.001 |
| 104 | test_routing.py | `test_tc_rt_04_custom_threshold[90-expected2]` | PASS | 0.001 |
| 105 | test_routing.py | `test_tc_rt_05_overflow_and_no_fleet` | PASS | 0.001 |
| 106 | test_routing.py | `test_tc_rt_06_empty_registry_and_no_due_bins` | PASS | 0.001 |
| 107 | test_routing.py | `test_tc_rt_07_invalid_threshold[-1]` | PASS | 0.001 |
| 108 | test_routing.py | `test_tc_rt_07_invalid_threshold[101]` | PASS | 0.001 |
| 109 | test_routing.py | `test_tc_rt_07_invalid_threshold[True]` | PASS | 0.001 |
| 110 | test_routing.py | `test_tc_rt_07_invalid_threshold[70.5]` | PASS | 0.001 |
| 111 | test_routing.py | `test_tc_rt_07_invalid_threshold[70]` | PASS | 0.001 |
| 112 | test_routing.py | `test_tc_rt_07_invalid_threshold[None]` | PASS | 0.001 |
| 113 | test_routing.py | `test_tc_rt_08_complete_route` | PASS | 0.001 |
| 114 | test_routing.py | `test_tc_rt_09_invalid_truck[-1]` | PASS | 0.001 |
| 115 | test_routing.py | `test_tc_rt_09_invalid_truck[ -1]` | PASS | 0.001 |
| 116 | test_routing.py | `test_tc_rt_09_invalid_truck[None-1]` | PASS | 0.001 |
| 117 | test_routing.py | `test_tc_rt_09_invalid_truck[1-1]` | PASS | 0.001 |
| 118 | test_routing.py | `test_tc_rt_09_invalid_truck[T-0]` | PASS | 0.001 |
| 119 | test_routing.py | `test_tc_rt_09_invalid_truck[T--1]` | PASS | 0.001 |
| 120 | test_routing.py | `test_tc_rt_09_invalid_truck[T-True]` | PASS | 0.001 |
| 121 | test_routing.py | `test_tc_rt_09_invalid_truck[T-1.5]` | PASS | 0.001 |
| 122 | test_routing.py | `test_tc_rt_10_invalid_fleet` | PASS | 0.001 |
| 123 | test_routing.py | `test_tc_rt_11_missing_bin_atomic_completion` | PASS | 0.001 |
| 124 | test_routing.py | `test_tc_rt_12_invalid_route[ids0]` | PASS | 0.001 |
| 125 | test_routing.py | `test_tc_rt_12_invalid_route[ids1]` | PASS | 0.001 |
| 126 | test_routing.py | `test_tc_rt_12_invalid_route[ids2]` | PASS | 0.001 |
| 127 | test_smoke.py | `test_package_imports` | PASS | 0.001 |

## Execution Time

- Unit tests: 5.29 seconds
- System tests: 0.44 seconds
- Coverage run: 10.25 seconds
- Total validation pipeline: 16.21 seconds
