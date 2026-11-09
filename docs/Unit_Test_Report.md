# Unit Test Report

Project: Smart City Waste Management System  
Date: 2026-11-09  
Commit: 99650f8  
Environment: Python 3.14.0 on Darwin 25.6.0  
Tool: pytest

**Overall: PASS**

## Summary

| Total | Passed | Failed | Pass rate |
|---|---|---|---|
| 82 | 82 | 0 | 100.0% |

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
| 13 | test_bins.py | `test_tc_bin_01_create_valid_bin` | PASS | 0.000 |
| 14 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs0]` | PASS | 0.000 |
| 15 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs1]` | PASS | 0.000 |
| 16 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs2]` | PASS | 0.000 |
| 17 | test_bins.py | `test_tc_bin_02_invalid_bin_rejected[kwargs3]` | PASS | 0.000 |
| 18 | test_bins.py | `test_tc_bin_03_fill_level_out_of_range[-1]` | PASS | 0.000 |
| 19 | test_bins.py | `test_tc_bin_03_fill_level_out_of_range[101]` | PASS | 0.000 |
| 20 | test_bins.py | `test_tc_bin_04_status_boundaries[0-OK]` | PASS | 0.000 |
| 21 | test_bins.py | `test_tc_bin_04_status_boundaries[69-OK]` | PASS | 0.000 |
| 22 | test_bins.py | `test_tc_bin_04_status_boundaries[70-NEARLY_FULL]` | PASS | 0.000 |
| 23 | test_bins.py | `test_tc_bin_04_status_boundaries[89-NEARLY_FULL]` | PASS | 0.000 |
| 24 | test_bins.py | `test_tc_bin_04_status_boundaries[90-FULL]` | PASS | 0.000 |
| 25 | test_bins.py | `test_tc_bin_04_status_boundaries[100-FULL]` | PASS | 0.000 |
| 26 | test_bins.py | `test_tc_bin_05_empty_resets_level` | PASS | 0.000 |
| 27 | test_bins.py | `test_tc_bin_06_registry_add_get_all` | PASS | 0.000 |
| 28 | test_bins.py | `test_tc_bin_07_registry_duplicate_rejected` | PASS | 0.000 |
| 29 | test_bins.py | `test_tc_bin_08_registry_missing_bin` | PASS | 0.000 |
| 30 | test_bins.py | `test_tc_bin_09_registry_remove` | PASS | 0.000 |
| 31 | test_bins.py | `test_tc_bin_10_registry_filter_by_status` | PASS | 0.000 |
| 32 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[nan]` | PASS | 0.000 |
| 33 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[inf]` | PASS | 0.000 |
| 34 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[True]` | PASS | 0.000 |
| 35 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[False]` | PASS | 0.000 |
| 36 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[50.5]` | PASS | 0.000 |
| 37 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[50]` | PASS | 0.000 |
| 38 | test_bins.py | `test_tc_bin_11_non_integer_fill_level_rejected[None]` | PASS | 0.000 |
| 39 | test_bins.py | `test_tc_bin_12_non_integer_fill_level_rejected_in_constructor` | PASS | 0.000 |
| 40 | test_reports.py | `test_tc_rp_01_average_empty_list` | PASS | 0.000 |
| 41 | test_reports.py | `test_tc_rp_02_average_fill_level` | PASS | 0.000 |
| 42 | test_reports.py | `test_tc_rp_03_status_summary` | PASS | 0.000 |
| 43 | test_reports.py | `test_tc_rp_04_summary_by_waste_type` | PASS | 0.000 |
| 44 | test_reports.py | `test_tc_rp_05_text_report_no_bins` | PASS | 0.000 |
| 45 | test_reports.py | `test_tc_rp_06_text_report_contents` | PASS | 0.000 |
| 46 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[0-OK]` | PASS | 0.000 |
| 47 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[69-OK]` | PASS | 0.000 |
| 48 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[70-NEARLY_FULL]` | PASS | 0.000 |
| 49 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[89-NEARLY_FULL]` | PASS | 0.000 |
| 50 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[90-FULL]` | PASS | 0.000 |
| 51 | test_reports.py | `test_tc_rp_07_status_summary_boundaries[100-FULL]` | PASS | 0.000 |
| 52 | test_reports.py | `test_tc_rp_08_status_summary_empty_has_all_keys` | PASS | 0.000 |
| 53 | test_reports.py | `test_tc_rp_09_reports_do_not_modify_bins` | PASS | 0.000 |
| 54 | test_routing.py | `test_tc_rt_01_select_threshold_inclusive` | PASS | 0.000 |
| 55 | test_routing.py | `test_tc_rt_02_fullest_first_and_deterministic_ties` | PASS | 0.000 |
| 56 | test_routing.py | `test_tc_rt_03_capacity_and_multiple_trucks` | PASS | 0.000 |
| 57 | test_routing.py | `test_tc_rt_04_custom_threshold[0-expected0]` | PASS | 0.000 |
| 58 | test_routing.py | `test_tc_rt_04_custom_threshold[100-expected1]` | PASS | 0.000 |
| 59 | test_routing.py | `test_tc_rt_04_custom_threshold[90-expected2]` | PASS | 0.000 |
| 60 | test_routing.py | `test_tc_rt_05_overflow_and_no_fleet` | PASS | 0.000 |
| 61 | test_routing.py | `test_tc_rt_06_empty_registry_and_no_due_bins` | PASS | 0.000 |
| 62 | test_routing.py | `test_tc_rt_07_invalid_threshold[-1]` | PASS | 0.000 |
| 63 | test_routing.py | `test_tc_rt_07_invalid_threshold[101]` | PASS | 0.000 |
| 64 | test_routing.py | `test_tc_rt_07_invalid_threshold[True]` | PASS | 0.000 |
| 65 | test_routing.py | `test_tc_rt_07_invalid_threshold[70.5]` | PASS | 0.000 |
| 66 | test_routing.py | `test_tc_rt_07_invalid_threshold[70]` | PASS | 0.000 |
| 67 | test_routing.py | `test_tc_rt_07_invalid_threshold[None]` | PASS | 0.000 |
| 68 | test_routing.py | `test_tc_rt_08_complete_route` | PASS | 0.000 |
| 69 | test_routing.py | `test_tc_rt_09_invalid_truck[-1]` | PASS | 0.000 |
| 70 | test_routing.py | `test_tc_rt_09_invalid_truck[ -1]` | PASS | 0.000 |
| 71 | test_routing.py | `test_tc_rt_09_invalid_truck[None-1]` | PASS | 0.000 |
| 72 | test_routing.py | `test_tc_rt_09_invalid_truck[1-1]` | PASS | 0.000 |
| 73 | test_routing.py | `test_tc_rt_09_invalid_truck[T-0]` | PASS | 0.000 |
| 74 | test_routing.py | `test_tc_rt_09_invalid_truck[T--1]` | PASS | 0.000 |
| 75 | test_routing.py | `test_tc_rt_09_invalid_truck[T-True]` | PASS | 0.000 |
| 76 | test_routing.py | `test_tc_rt_09_invalid_truck[T-1.5]` | PASS | 0.000 |
| 77 | test_routing.py | `test_tc_rt_10_invalid_fleet` | PASS | 0.000 |
| 78 | test_routing.py | `test_tc_rt_11_missing_bin_atomic_completion` | PASS | 0.000 |
| 79 | test_routing.py | `test_tc_rt_12_invalid_route[ids0]` | PASS | 0.000 |
| 80 | test_routing.py | `test_tc_rt_12_invalid_route[ids1]` | PASS | 0.000 |
| 81 | test_routing.py | `test_tc_rt_12_invalid_route[ids2]` | PASS | 0.000 |
| 82 | test_smoke.py | `test_package_imports` | PASS | 0.000 |
