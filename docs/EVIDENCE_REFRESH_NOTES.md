# Final Testing Evidence — Scope and Limitations

## Baseline, checkout, and evidence dates

- Repository: SasyakSubudhi/Smart-City-Waste-Management-System
- **Accepted application-source baseline:** `e293216f5156d7ec53fcf0d80aeac00cb459d0f1` (confirmed after PR #34, including the reconciled STP).
- **Original standalone test checkout:** `e293216f5156d7ec53fcf0d80aeac00cb459d0f1`, run **2026-11-10**.
- **Refreshed report-generator test checkout:** `c8496382ebe2e8e7950e0a7d3b83b7b061855469`, run **2026-11-11**. The four regenerated reports record this checkout as `c849638`.
- Test environment for these local runs: **macOS Darwin 25.6.0, Python 3.14.0**.

The accepted application baseline and the report-generator checkout are **different commits**. The later checkout is the evidence-refresh commit built on the accepted baseline; the PR's application/runtime and feature-test modules were not changed. A test result belongs to the checkout actually used for its execution, not automatically to an earlier source commit.

## Original standalone full-suite execution — 2026-11-10

- Checkout: `e293216f5156d7ec53fcf0d80aeac00cb459d0f1`.
- Full pytest suite: **162 collected, 162 passed, zero failures, zero skips**, completed in **2.95 seconds**.
- Package statement coverage: **162/162 (100%)**; branch outcomes: **64/64 (100%)** for `src/waste_mgmt`.
- Originating raw artifacts: [full-suite.xml](../evidence/full-suite.xml), [full-suite.log](../evidence/full-suite.log), and [coverage.json](../evidence/coverage.json).

These files document the standalone run; its timing is **not** the generator's timing.

## Refreshed report-generator execution — 2026-11-11

- Actual tested checkout: `c8496382ebe2e8e7950e0a7d3b83b7b061855469`.
- Unit test execution: **158/158 passed**, **2.94 seconds**.
- System validation execution: **4/4 passed**, **0.19 seconds**.
- Separate coverage execution: **3.26 seconds**.
- Total report-generation time: **6.53 seconds**; generator exit status: **0 (PASS)**.
- Generator coverage: **162/162 statements and 64/64 branch outcomes (100% each)** for `src/waste_mgmt` on the stated Python 3.14 environment.
- Originating raw artifacts: [unit.xml](../evidence/report-generator/unit.xml), [system.xml](../evidence/report-generator/system.xml), [cov.json](../evidence/report-generator/cov.json), [generator.log](../evidence/report-generator/generator.log), and [exit-status.txt](../evidence/report-generator/exit-status.txt).
- Corresponding refreshed reports: [Unit Test Report](Unit_Test_Report.md), [System Validation Report](System_Validation_Report.md), [Code Coverage Report](Code_Coverage_Report.md), and [Branch Coverage Report](Branch_Coverage_Report.md).

The generator's unit, system, and coverage runs are separate executions. Their durations and the total generator duration must not be confused with the standalone full-suite duration. The earlier generator measurements **2.93/0.18/3.15/6.42 seconds** are historical observations superseded by the refreshed report-generation artifacts; they are **not** the provenance of the current reports.

## Coverage scope and interpreter differences

Coverage measures only the Python package under `src/waste_mgmt`. Root-level `app.py` and `demo.py` are excluded from the package coverage denominator; 100% package coverage does not imply 100% repository-wide coverage.

Coverage denominators can differ by interpreter and execution environment. The macOS/Python 3.14 measurements above must not be combined with or relabeled as the separate Windows CI measurements (for example, Windows/Python 3.12 reported 174/174 package statements and 64/64 branch outcomes).

## Routing atomicity

Routing completion guarantees atomic behavior **within each individual route**. It does not establish fleet-wide transaction atomicity across multiple trucks or routes.

## Historical and compatibility evidence

Previously published evidence referring to commit `915aac0` belongs to an earlier baseline and must not be represented as evidence generated from either checkout described above.

Python 3.10/3.11 Windows compatibility evidence is **domain-only**, not a complete Windows UI/system validation. Any later CI results are separate observations tied to their own run environment and checkout.

## Performance target

The **2.95-second** standalone full-suite result met the original **10-second** target **on the recorded macOS environment only**. It does not establish cross-environment performance acceptance or imply that Windows CI meets the same threshold.

## Review status

The evidence and CI results do not constitute independent approval, final release approval, or course acceptance. Independent re-review is requested from @vasun26shriya; this PR must not be self-approved or automatically merged.
