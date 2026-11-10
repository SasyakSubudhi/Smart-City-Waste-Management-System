# Final Testing Evidence — Scope and Limitations

## Accepted source baseline

- Repository: SasyakSubudhi/Smart-City-Waste-Management-System
- Accepted source commit: e293216f5156d7ec53fcf0d80aeac00cb459d0f1
- Evidence refresh date: 2026-11-10
- Test environment: macOS (Darwin 25.6.0), Python 3.14.0

## Current validation

The complete pytest suite collected and passed 162 tests, with zero failures and zero skips.

The full-suite run completed in 2.95 seconds on the recorded macOS environment.

The report generator separately executed:
- Unit tests: 158 passed out of 158, in 2.93 seconds.
- System validation: 4 passed out of 4, in 0.18 seconds.
- Coverage run: 3.15 seconds.
- Total report generation: 6.42 seconds.

These are separate executions. Their timings must not be combined into a single test-run duration.

## Coverage scope

Coverage measures the Python package under src/waste_mgmt.

- Statements: 162 of 162 covered (100%).
- Branch outcomes: 64 of 64 covered (100%).

The root-level app.py and demo.py scripts are outside this package coverage scope. Their exclusion must not be interpreted as proof of 100% coverage across the entire repository.

## Routing atomicity

Routing completion guarantees atomic behavior within each individual route. It does not establish fleet-wide transaction atomicity across multiple trucks or routes.

## Historical evidence

Previously published evidence referring to commit 915aac0 belongs to an earlier source baseline and must not be represented as evidence generated from the accepted commit above.

Earlier Python 3.10/3.11 Windows domain-only validation is historical evidence. The current refresh does not claim a new Windows test run.

## Performance target

The recorded full-suite run completed in 2.95 seconds, meeting the original 10-second target on this macOS environment.

This does not establish that the target is met across every supported environment.

## Review status

These reports document test execution and coverage. They do not constitute independent review, final release approval, or course acceptance.

Independent review is requested from @vasun26shriya.
