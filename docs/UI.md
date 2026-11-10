# Web dashboard

## Run

From the repository root with Python 3.12:

```text
python -m pip install -r requirements.txt
streamlit run app.py
```

If Streamlit's executable is not on PATH, use `python -m streamlit run app.py`.
Open the local URL printed by Streamlit. app.py calls the package interfaces
directly. The separate command-line demonstration, merged in PR #14, runs with
`python demo.py`; it is not the Streamlit app or the recording viewer.

## Tabs and requirements

| Tab | Actions and requirements |
|---|---|
| Bins | Register/list/remove bins (FR-1), send validated sensor readings (FR-2), display derived status (FR-3) |
| Alerts | Display package-generated alerts, CRITICAL before WARNING; filter All / CRITICAL / WARNING; show `No alerts.` when All is empty (FR-4) |
| Collection routes | Choose fleet size and bin-count capacity; plan fullest-first routes (FR-5), show unassigned IDs (FR-6), confirm completed collections (FR-7) |
| City report | Total bins, average fill, nearly-full/full counts and package text report (FR-8) |

## State and errors

The Alerts severity selector defaults to All. CRITICAL and WARNING show only
matching rows, preserving the package's priority and same-severity order.
Filtering does not alter bins, alerts or the collection plan. With no matching
rows it shows `No alerts match this severity.`. The selected severity survives
ordinary reruns, including collection confirmation; the rows regenerate from the
updated registry. Choose All to restore the complete list. The pure adapter
copies row dictionaries and rejects unsupported severity options with ValueError.

Registry and plan live in `st.session_state`, isolated per browser session.
There is no persistence: a new session starts empty. The page states that data
is not saved to disk. An empty Bins table points to the registration form; the
Collection routes tab explains how to create a plan when none is saved.
Forms submit explicitly.
Package ValueError and KeyError messages appear through `st.error`; the KeyError
payload is displayed without Python's surrounding representation quotes. Successful
operations use `st.success`. Reading fields deliberately allow out-of-range
integers so the package remains responsible for validation. Errors do not clear
a valid saved plan. Successful bin edits clear the plan to avoid stale IDs or
readings; planning again replaces the one active plan. Planning never empties
bins. Confirm all collections only after the simulated trips finish; success
clears the plan to prevent repeated collection. Zero trucks exposes all due IDs
as unassigned and displays guidance to add a truck and replan. With nothing due,
the page explains the 70% planning threshold and confirmation is disabled.
If a confirmed plan had unassigned bins, its success notice names those bins and
asks the supervisor to plan again. Only the assigned bins are emptied; backlog
readings and alerts remain. The cleared plan cannot be confirmed twice. The
completion notice appears on the next rerun, not as a persistent dispatch log.

The four domain modules and their existing tests are unchanged. dashboard.py
only adapts domain objects to table rows and wraps documented errors. app.py
contains presentation and session orchestration, with all classification,
validation, route assignment and reporting delegated to the package. No network
sensor, geographic routing, account authentication or production dispatch is added.
Keep this local simulation on a trusted machine.

## Tests and viva guide

Run `python -m pytest --cov --cov-branch --cov-report=term-missing`.
The coverage source remains `src/waste_mgmt`; app.py is tested headlessly by
Streamlit AppTest but is outside that source. Check statement and branch coverage
independently. `tests/test_dashboard.py` covers adapters and exception handling;
`tests/test_app.py` covers forms, errors, state preservation, collection, backlog,
empty data and session isolation. UI IDs run consecutively across both files.
TC-UI-26..31 additionally cover backlog after confirmation, empty-state guidance,
registration/removal invalidation, rejected edits preserving a usable plan, and
severity filtering followed by two-truck confirmation.
`python generate_test_case_doc.py` includes both files in the Test Case Document.
Historical final testing reports predate this feature and must not be treated
as evidence for the expanded suite.

To explain the code: attempt invokes a supplied callable and catches only the
two domain error classes; unexpected programming errors propagate. Row helpers
copy fields into dictionaries without changing domain state. Each form calls a
domain operation through attempt. A successful edit stores a notice and reruns
so every tab reflects the same updated state. Alerts/report metrics call the
existing package functions. A plan is a snapshot containing routes and backlog;
confirmation delegates emptying to complete_route.

## Validation snapshot (9 November 2026)

On Windows/Python 3.13.7 with Streamlit 1.67.0, the expanded suite passed
108 tests before the error-message follow-up: 154/154 statements and 56/56 branch
outcomes covered. The first run took 65.36 seconds and a clean rerun took 55.73
seconds. The expanded AppTest suite exceeds the older sub-10-second target;
NFR-2 needs a team-agreed update or a separate performance criterion. CI separately
validates Windows/Python 3.12. The follow-up adds an empty-KeyError adapter case;
its current execution results are recorded in the PR rather than overwriting this
historical measurement.

### Measured follow-up run

On 9 November 2026, from `feature/web-ui` at runtime revision `f4651fd`,
`python -m pytest --cov --cov-branch --cov-report=term-missing` completed on
Windows/Python 3.13.7 with Streamlit 1.67.0: **109 passed in 23.49 seconds**,
156/156 statements and 56/56 branch outcomes covered (100% each). This is pytest's
reported test-session time, excluding dependency installation and the browser
click-through. It exceeds the 10-second full-suite target; it does not claim a
UI response-time measurement or predict other machines' timing. Earlier recorded
times above are historical runs, not replacements for this observation.

A live `python -m streamlit run app.py` session was opened in Chrome and all four
tabs were clicked: register UI-DEMO, set reading to 95, inspect alerts, plan and
confirm collection, and verify report total 1 / mean 0.0% / full 0 afterward.

### Dashboard follow-up validation (10 November 2026)

On branch `fix/dashboard-session-safety`, runtime/test revision `ff7360f` based
on main `915aac0`, the command
`python -m pytest --cov --cov-branch --cov-report=term-missing --cov-report=json:../dashboard-safety-coverage.json`
passed **140 tests in 29.42 seconds** on Windows/Python 3.13.7 with Streamlit
1.67.0. Package statement coverage was 160/160 and branch coverage 58/58, each
100%. This is the full suite including AppTest; it exceeds the original
ten-second target. app.py remains outside the package coverage source. The
follow-up interactions were checked headlessly with AppTest; the browser
click-through above is historical evidence for the original UI, not a new manual
check of this follow-up. Windows/Python 3.12 CI and independent review are separate
checks on the published PR.
