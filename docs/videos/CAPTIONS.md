# Silent captions and timing sheet

These are proposed captions for real screen recordings, not spoken narration.
Adjust the cuts to real operations; never speed up or replace output to misstate it.

## Sprint 1 about 60 seconds

| Time | Show | Caption |
|---|---|---|
| 0–6 s | Product heading and team credit | Sprint 1 outcome — Smart City Waste Management System |
| 6–23 s | Real registration and statuses | Sasyak Subudhi — bin management and SRS. Validated readings determine bin status. |
| 23–39 s | Reject 50.5 and 150; show preserved value | Invalid readings raise ValueError without changing the bin. |
| 39–51 s | Real main-branch SRS in docs/SRS.md | Shriya Vasundhara Singh — routing and STP. Requirements guide collection behavior and tests. |
| 51–60 s | Team credit; product remains visible | Shreya Yashodhara Singh — alerts and SAD. Shruti Choudhary — reports and system validation. |

## Sprint 2 about 120 seconds

| Time | Show | Caption |
|---|---|---|
| 0–12 s | Actual bins and fill levels | Sasyak — validated bin data drives the collection flow. |
| 12–29 s | Real ordered alerts | Shreya — FULL becomes CRITICAL; NEARLY_FULL becomes WARNING. Critical alerts appear first. |
| 29–51 s | Two truck assignments and unassigned B2 | Shriya — fullest-first routing respects truck capacity and exposes the backlog. |
| 51–68 s | Confirm each selected route | Only selected bins are emptied. The unassigned bin remains due. |
| 68–86 s | Fresh alerts and city report | Shruti — report totals and status counts reflect the new state. |
| 86–108 s | Run real pytest command; show final summary | Automated tests and statement/branch coverage — show the actual result. |
| 108–120 s | Actual matching Actions run, green | Reviewed changes and successful CI on the recorded revision. |

Names and module credits should remain legible without reading quickly. Text-only
credits identify module ownership; they do not claim a teammate personally narrated.
