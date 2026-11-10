# Unit Test Report

Project: Smart City Waste Management System

Date: 2026-11-10

Commit: e293216

Environment: Python 3.14.0 on Darwin 25.6.0

Tool: pytest

**Overall: PASS**

## Summary

| Total | Passed | Failed | Skipped | Pass rate |
|---|---|---|---|---|
| 158 | 158 | 0 | 0 | 100.0% |

## Results

| # | Test file | Test case | Result | Time (s) |
|---|---|---|---|---|
| 1 | test_alerts.py | `test_tc_al_01_empty_and_ok` | PASS | 0.000 |
| 2 | test_alerts.py | `test_tc_al_02_boundaries[0-None]` | PASS | 0.000 |
| 3 | test_alerts.py | `test_tc_al_02_boundaries[69-None]` | PASS | 0.000 |
| 4 | test_alerts.py | `test_tc_al_02_boundaries[70-WARNING]` | PASS | 0.000 |
| 5 | test_alerts.py | `test_tc_al_02_boundaries[89-WARNING]` | PASS | 0.000 |
| 6 | test_alerts.py | `test_tc_al_02_boundaries[90-CRITICAL]` | PASS | 0.000 |
| 7 | test_alerts.py | `test_tc_al_02_boundaries[100-CRITICAL]` | PASS | 0.000 |
| 8 | test_alerts.py | `test_tc_al_03_priority_stability_and_no_mutation` | PASS | 0.000 |
| 9 | test_alerts.py | `test_tc_al_04_format[70-WARNING]` | PASS | 0.000 |
| 10 | test_alerts.py | `test_tc_al_04_format[100-CRITICAL]` | PASS | 0.000 |
| 11 | test_alerts.py | `test_tc_al_05_updated_reading_empty_and_snapshot` | PASS | 0.000 |
| 12 | test_alerts.py | `test_tc_al_06_registry_route_completion_and_backlog` | PASS | 0.000 |
| 13 | test_alerts.py | `test_tc_al_07_mixed_boundaries_in_one_batch` | PASS | 0.000 |
| 14 | test_alerts.py | `test_tc_al_08_many_equal_severity_keep_input_order[80-WARNING]` | PASS | 0.000 |
| 15 | test_alerts.py | `test_tc_al_08_many_equal_severity_keep_input_order[95-CRITICAL]` | PASS | 0.000 |
| 16 | test_alerts.py | `test_tc_al_09_emptying_preserves_saved_alert_and_its_format[70-WARNING]` | PASS | 0.000 |
| 17 | test_alerts.py | `test_tc_al_09_emptying_preserves_saved_alert_and_its_format[90-CRITICAL]` | PASS | 0.000 |
| 18 | test_app.py | `test_tc_ui_08_start_empty` | PASS | 0.343 |
| 19 | test_app.py | `test_tc_ui_09_register_and_persist` | PASS | 0.066 |
| 20 | test_app.py | `test_tc_ui_10_duplicate_id_error` | PASS | 0.063 |
| 21 | test_app.py | `test_tc_ui_11_empty_id_error` | PASS | 0.052 |
| 22 | test_app.py | `test_tc_ui_12_sensor_updates_alerts_and_report` | PASS | 0.065 |
| 23 | test_app.py | `test_tc_ui_13_unknown_bin_error` | PASS | 0.053 |
| 24 | test_app.py | `test_tc_ui_14_out_of_range_preserves_state[-1]` | PASS | 0.073 |
| 25 | test_app.py | `test_tc_ui_14_out_of_range_preserves_state[101]` | PASS | 0.073 |
| 26 | test_app.py | `test_tc_ui_15_remove_and_unknown_remove` | PASS | 0.072 |
| 27 | test_app.py | `test_tc_ui_16_plan_and_confirm_collection` | PASS | 0.097 |
| 28 | test_app.py | `test_tc_ui_17_nothing_due` | PASS | 0.064 |
| 29 | test_app.py | `test_tc_ui_18_backlog_and_empty_fleet` | PASS | 0.102 |
| 30 | test_app.py | `test_tc_ui_19_edit_invalidates_saved_plan` | PASS | 0.083 |
| 31 | test_app.py | `test_tc_ui_20_sessions_are_isolated` | PASS | 0.100 |
| 32 | test_app.py | `test_tc_ui_24_severity_filter_and_reset` | PASS | 0.110 |
| 33 | test_app.py | `test_tc_ui_25_filter_no_match_and_collection_refresh` | PASS | 0.102 |
| 34 | test_app.py | `test_tc_ui_26_confirmation_identifies_remaining_backlog` | PASS | 0.132 |
| 35 | test_app.py | `test_tc_ui_27_empty_session_explains_setup_and_data_lifetime` | PASS | 0.057 |
| 36 | test_app.py | `test_tc_ui_28_no_trucks_distinguished_from_nothing_due` | PASS | 0.084 |
| 37 | test_app.py | `test_tc_ui_29_registry_changes_clear_saved_plan[register]` | PASS | 0.085 |
| 38 | test_app.py | `test_tc_ui_29_registry_changes_clear_saved_plan[remove]` | PASS | 0.086 |
| 39 | test_app.py | `test_tc_ui_30_failed_edits_preserve_collectable_plan[duplicate-bin B1 already registered]` | PASS | 0.099 |
| 40 | test_app.py | `test_tc_ui_30_failed_edits_preserve_collectable_plan[reading-fill level must be between 0 and 100]` | PASS | 0.097 |
| 41 | test_app.py | `test_tc_ui_30_failed_edits_preserve_collectable_plan[remove-bin missing not found]` | PASS | 0.097 |
| 42 | test_app.py | `test_tc_ui_31_filter_preserves_two_truck_plan_and_confirmation` | PASS | 0.120 |
| 43 | test_bins.py | `test_tc_bin_01_create_valid_bin` | PASS | 0.000 |
| 44 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs0]` | PASS | 0.000 |
| 45 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs1]` | PASS | 0.000 |
| 46 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs2]` | PASS | 0.000 |
| 47 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs3]` | PASS | 0.000 |
| 48 | test_bins.py | `test_tc_bin_03_fill_level_out_of_range[-1]` | PASS | 0.000 |
| 49 | test_bins.py | `test_tc_bin_03_fill_level_out_of_range[101]` | PASS | 0.000 |
| 50 | test_bins.py | `test_tc_bin_04_status_boundaries[0-OK]` | PASS | 0.000 |
| 51 | test_bins.py | `test_tc_bin_04_status_boundaries[69-OK]` | PASS | 0.000 |
| 52 | test_bins.py | `test_tc_bin_04_status_boundaries[70-NEARLY_FULL]` | PASS | 0.000 |
| 53 | test_bins.py | `test_tc_bin_04_status_boundaries[89-NEARLY_FULL]` | PASS | 0.000 |
| 54 | test_bins.py | `test_tc_bin_04_status_boundaries[90-FULL]` | PASS | 0.000 |
| 55 | test_bins.py | `test_tc_bin_04_status_boundaries[100-FULL]` | PASS | 0.000 |
| 56 | test_bins.py | `test_tc_bin_05_empty_resets_level` | PASS | 0.000 |
| 57 | test_bins.py | `test_tc_bin_06_registry_add_get_all` | PASS | 0.000 |
| 58 | test_bins.py | `test_tc_bin_07_registry_duplicate_rejected` | PASS | 0.000 |
| 59 | test_bins.py | `test_tc_bin_08_registry_missing_bin` | PASS | 0.000 |
| 60 | test_bins.py | `test_tc_bin_09_registry_remove` | PASS | 0.000 |
| 61 | test_bins.py | `test_tc_bin_10_registry_filter_by_status` | PASS | 0.000 |
| 62 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[nan]` | PASS | 0.000 |
| 63 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[inf]` | PASS | 0.000 |
| 64 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[True]` | PASS | 0.000 |
| 65 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[False]` | PASS | 0.000 |
| 66 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[50.5]` | PASS | 0.000 |
| 67 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[50]` | PASS | 0.000 |
| 68 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[None]` | PASS | 0.000 |
| 69 | test_bins.py | `test_tc_bin_12_non_integer_fill_level_rejected_in_constructor` | PASS | 0.000 |
| 70 | test_dashboard.py | `test_tc_ui_01_attempt_returns_result_and_passes_arguments` | PASS | 0.000 |
| 71 | test_dashboard.py | `test_tc_ui_02_attempt_preserves_domain_errors[error0-invalid]` | PASS | 0.000 |
| 72 | test_dashboard.py | `test_tc_ui_02_attempt_preserves_domain_errors[error1-missing]` | PASS | 0.000 |
| 73 | test_dashboard.py | `test_tc_ui_02_attempt_preserves_domain_errors[error2-]` | PASS | 0.000 |
| 74 | test_dashboard.py | `test_tc_ui_03_unexpected_errors_propagate` | PASS | 0.000 |
| 75 | test_dashboard.py | `test_tc_ui_04_bin_rows_are_read_only` | PASS | 0.000 |
| 76 | test_dashboard.py | `test_tc_ui_05_alert_rows_preserve_priority_and_format` | PASS | 0.000 |
| 77 | test_dashboard.py | `test_tc_ui_06_route_rows_none_and_empty` | PASS | 0.000 |
| 78 | test_dashboard.py | `test_tc_ui_07_route_rows_show_completion_without_mutation` | PASS | 0.000 |
| 79 | test_dashboard.py | `test_tc_ui_21_filter_preserves_rows_order_and_source[All-expected0]` | PASS | 0.000 |
| 80 | test_dashboard.py | `test_tc_ui_21_filter_preserves_rows_order_and_source[CRITICAL-expected1]` | PASS | 0.000 |
| 81 | test_dashboard.py | `test_tc_ui_21_filter_preserves_rows_order_and_source[WARNING-expected2]` | PASS | 0.000 |
| 82 | test_dashboard.py | `test_tc_ui_22_filter_empty_and_no_match` | PASS | 0.000 |
| 83 | test_dashboard.py | `test_tc_ui_23_filter_invalid_severity` | PASS | 0.000 |
| 84 | test_demo.py | `test_demo_script_runs_full_cycle` | PASS | 0.001 |
| 85 | test_generate_reports.py | `test_counts_include_skipped_tests` | PASS | 0.000 |
| 86 | test_generate_reports.py | `test_parse_junit_detects_pass_fail_and_skip` | PASS | 0.005 |
| 87 | test_generate_reports.py | `test_run_pytest_rejects_old_xml` | PASS | 0.001 |
| 88 | test_generate_reports.py | `test_run_pytest_rejects_invalid_xml` | PASS | 0.001 |
| 89 | test_generate_reports.py | `test_skipped_tests_make_report_fail` | PASS | 0.001 |
| 90 | test_generate_reports.py | `test_failed_pytest_makes_report_fail` | PASS | 0.001 |
| 91 | test_generate_reports.py | `test_low_coverage_fails` | PASS | 0.001 |
| 92 | test_generate_reports.py | `test_failed_coverage_command_fails` | PASS | 0.001 |
| 93 | test_generate_reports.py | `test_main_returns_failure_when_unit_tests_fail` | PASS | 0.000 |
| 94 | test_reports.py | `test_tc_rp_01_average_empty_list` | PASS | 0.000 |
| 95 | test_reports.py | `test_tc_rp_02_average_fill_level` | PASS | 0.000 |
| 96 | test_reports.py | `test_tc_rp_03_status_summary` | PASS | 0.000 |
| 97 | test_reports.py | `test_tc_rp_04_summary_by_waste_type` | PASS | 0.000 |
| 98 | test_reports.py | `test_tc_rp_05_text_report_no_bins` | PASS | 0.000 |
| 99 | test_reports.py | `test_tc_rp_06_text_report_contents` | PASS | 0.000 |
| 100 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[0-OK]` | PASS | 0.000 |
| 101 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[69-OK]` | PASS | 0.000 |
| 102 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[70-NEARLY_FULL]` | PASS | 0.000 |
| 103 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[89-NEARLY_FULL]` | PASS | 0.000 |
| 104 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[90-FULL]` | PASS | 0.000 |
| 105 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[100-FULL]` | PASS | 0.000 |
| 106 | test_reports.py | `test_tc_rp_08_status_summary_empty_has_all_keys` | PASS | 0.000 |
| 107 | test_reports.py | `test_tc_rp_09_reports_do_not_modify_bins` | PASS | 0.000 |
| 108 | test_routing.py | `test_tc_rt_01_select_threshold_inclusive` | PASS | 0.000 |
| 109 | test_routing.py | `test_tc_rt_02_fullest_first_and_deterministic_ties` | PASS | 0.000 |
| 110 | test_routing.py | `test_tc_rt_03_capacity_and_multiple_trucks` | PASS | 0.000 |
| 111 | test_routing.py | `test_tc_rt_04_custom_threshold[0-expected0]` | PASS | 0.000 |
| 112 | test_routing.py | `test_tc_rt_04_custom_threshold[100-expected1]` | PASS | 0.002 |
| 113 | test_routing.py | `test_tc_rt_04_custom_threshold[90-expected2]` | PASS | 0.000 |
| 114 | test_routing.py | `test_tc_rt_05_overflow_and_no_fleet` | PASS | 0.000 |
| 115 | test_routing.py | `test_tc_rt_06_empty_registry_and_no_due_bins` | PASS | 0.000 |
| 116 | test_routing.py | `test_tc_rt_07_invalid_threshold[-1]` | PASS | 0.000 |
| 117 | test_routing.py | `test_tc_rt_07_invalid_threshold[101]` | PASS | 0.000 |
| 118 | test_routing.py | `test_tc_rt_07_invalid_threshold[True]` | PASS | 0.000 |
| 119 | test_routing.py | `test_tc_rt_07_invalid_threshold[70.5]` | PASS | 0.000 |
| 120 | test_routing.py | `test_tc_rt_07_invalid_threshold[70]` | PASS | 0.000 |
| 121 | test_routing.py | `test_tc_rt_07_invalid_threshold[None]` | PASS | 0.000 |
| 122 | test_routing.py | `test_tc_rt_08_complete_route` | PASS | 0.000 |
| 123 | test_routing.py | `test_tc_rt_09_invalid_truck[-1]` | PASS | 0.000 |
| 124 | test_routing.py | `test_tc_rt_09_invalid_truck[ -1]` | PASS | 0.000 |
| 125 | test_routing.py | `test_tc_rt_09_invalid_truck[None-1]` | PASS | 0.000 |
| 126 | test_routing.py | `test_tc_rt_09_invalid_truck[1-1]` | PASS | 0.000 |
| 127 | test_routing.py | `test_tc_rt_09_invalid_truck[T-0]` | PASS | 0.000 |
| 128 | test_routing.py | `test_tc_rt_09_invalid_truck[T--1]` | PASS | 0.000 |
| 129 | test_routing.py | `test_tc_rt_09_invalid_truck[T-True]` | PASS | 0.000 |
| 130 | test_routing.py | `test_tc_rt_09_invalid_truck[T-1.5]` | PASS | 0.000 |
| 131 | test_routing.py | `test_tc_rt_10_invalid_fleet` | PASS | 0.000 |
| 132 | test_routing.py | `test_tc_rt_11_missing_bin_atomic_completion` | PASS | 0.000 |
| 133 | test_routing.py | `test_tc_rt_12_invalid_route[ids0]` | PASS | 0.000 |
| 134 | test_routing.py | `test_tc_rt_12_invalid_route[ids1]` | PASS | 0.000 |
| 135 | test_routing.py | `test_tc_rt_12_invalid_route[ids2]` | PASS | 0.000 |
| 136 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[AB0]` | PASS | 0.000 |
| 137 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[AB1]` | PASS | 0.000 |
| 138 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[ids2]` | PASS | 0.000 |
| 139 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[ids3]` | PASS | 0.000 |
| 140 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[None]` | PASS | 0.000 |
| 141 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[7]` | PASS | 0.000 |
| 142 | test_routing.py | `test_tc_rt_13_reject_malformed_bin_id_containers_without_emptying[ids6]` | PASS | 0.000 |
| 143 | test_routing.py | `test_tc_rt_14_reject_invalid_route_or_truck_objects[None]` | PASS | 0.000 |
| 144 | test_routing.py | `test_tc_rt_14_reject_invalid_route_or_truck_objects[route1]` | PASS | 0.000 |
| 145 | test_routing.py | `test_tc_rt_14_reject_invalid_route_or_truck_objects[route2]` | PASS | 0.000 |
| 146 | test_routing.py | `test_tc_rt_14_reject_invalid_route_or_truck_objects[route3]` | PASS | 0.000 |
| 147 | test_routing.py | `test_tc_rt_15_non_iterable_fleet_has_clear_validation_error[None]` | PASS | 0.000 |
| 148 | test_routing.py | `test_tc_rt_15_non_iterable_fleet_has_clear_validation_error[1]` | PASS | 0.000 |
| 149 | test_routing.py | `test_tc_rt_15_non_iterable_fleet_has_clear_validation_error[True]` | PASS | 0.000 |
| 150 | test_routing.py | `test_tc_rt_16_fleet_generator_is_consumed_once_and_empty_is_supported` | PASS | 0.000 |
| 151 | test_routing.py | `test_tc_rt_17_assignment_invariants_across_registry_orders[fleet_spec0-expected_routes0-expected_backlog0]` | PASS | 0.001 |
| 152 | test_routing.py | `test_tc_rt_17_assignment_invariants_across_registry_orders[fleet_spec1-expected_routes1-expected_backlog1]` | PASS | 0.001 |
| 153 | test_routing.py | `test_tc_rt_17_assignment_invariants_across_registry_orders[fleet_spec2-expected_routes2-expected_backlog2]` | PASS | 0.001 |
| 154 | test_routing.py | `test_tc_rt_18_complete_trucks_out_of_order_preserves_backlog` | PASS | 0.000 |
| 155 | test_routing.py | `test_tc_rt_19_missing_bin_anywhere_is_atomic_and_retryable[A]` | PASS | 0.000 |
| 156 | test_routing.py | `test_tc_rt_19_missing_bin_anywhere_is_atomic_and_retryable[B]` | PASS | 0.000 |
| 157 | test_routing.py | `test_tc_rt_19_missing_bin_anywhere_is_atomic_and_retryable[C]` | PASS | 0.000 |
| 158 | test_smoke.py | `test_package_imports` | PASS | 0.000 |

## Execution Time

- Unit tests: 2.93 seconds
- System tests: 0.18 seconds
- Coverage run: 3.15 seconds
- Total validation pipeline: 6.42 seconds
