# Web dashboard

## Run

From the repository root with Python 3.12:

```text
python -m pip install -r requirements.txt
streamlit run app.py
```

If Streamlit's executable is not on PATH, use `python -m streamlit run app.py`.
Open the local URL printed by Streamlit. No separate demo.py exists in the
current baseline; app.py calls the package interfaces directly.

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
There is no persistence: a new session starts empty. Forms submit explicitly.
Package ValueError and KeyError messages appear through `st.error`; the KeyError
payload is displayed without Python's surrounding representation quotes. Successful
operations use `st.success`. Reading fields deliberately allow out-of-range
integers so the package remains responsible for validation. Errors do not clear
a valid saved plan. Successful bin edits clear the plan to avoid stale IDs or
readings; planning again replaces the one active plan. Planning never empties
bins. Confirm all collections only after the simulated trips finish; success
clears the plan to prevent repeated collection. Zero trucks exposes all due IDs
as unassigned. With nothing due, confirmation is disabled.

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
