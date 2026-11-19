# Smart City Waste Management System

Monitors waste-bin fill levels, raises overflow alerts, plans garbage-truck routes and produces city-wide reports.

**Team:** Sasyak Subudhi (PES1UG24AM256) | Shriya Vasundhara Singh (PES1UG24AM269) | Shreya Yashodhara Singh (PES1UG24AM266) | Shruti Choudhary (PES1UG24AM271)

## Run locally
```bash
pip install -r requirements.txt
python demo.py                # walk through one full collection cycle
pytest --cov --cov-branch     # run all tests with statement + branch coverage
python generate_reports.py    # regenerate the four test reports in docs/
```

## What the demo shows
`demo.py` registers four bins, rejects an invalid sensor reading, prints alerts (CRITICAL first), plans routes for two trucks, confirms the collection, and prints the city report.

## Structure
| Path | Purpose |
|---|---|
| `src/waste_mgmt/` | Application code (bins, alerts, routing, reports) |
| `tests/` | Unit tests, system tests and the demo test |
| `demo.py` | Command-line demo of the whole system |
| `docs/` | SRS, SAD, STP, Test Case Document, deviations note and test reports |
| `docs/videos/` | Sprint 1 (1 minute) and Sprint 2 (2 minute) demo videos |
| `.github/workflows/ci.yml` | CI: runs tests on every push and pull request |
| `.github/workflows/domain-compatibility.yml` | CI: domain tests on Python 3.10 and 3.11 |
| `.github/workflows/release.yml` | CD: publishes a GitHub Release after CI passes on `main` |
| `build_release.py` | Packages the app, package and four reports into the release zip |

## Continuous delivery
When a pull request merges and the CI workflow passes on `main`, the Release workflow checks out that commit, regenerates the four validation reports, runs `python build_release.py` and publishes `smart-city-waste-management.zip` as a GitHub Release tagged `v1.0.<run number>`. Download it from the repository's Releases page, extract it and run `python -m pip install -r requirements.txt` then `python -m streamlit run app.py`. Nothing is deployed to a server.

## Documents
- Requirements: `docs/SRS.md` | Architecture: `docs/SAD.md` | Test plan: `docs/STP.md`
- Differences from the submitted documents: `docs/DEVIATIONS.md`
- Reports: `docs/Unit_Test_Report.md`, `docs/System_Validation_Report.md`, `docs/Code_Coverage_Report.md`, `docs/Branch_Coverage_Report.md`

## Contributing
One feature = one branch = one pull request with tests, reviewed by a teammate, merged only when CI is green. See `docs/STP.md` for roles.

### Workflow for every new feature
```
main -> git pull -> feature/new-feature -> add code + tests -> pytest -> git add . -> git commit -> git push
     -> Pull Request to main -> GitHub Actions (test passes) -> 1 teammate approval -> merge -> main
```
