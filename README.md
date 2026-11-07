# Smart City Waste Management System

Monitors waste-bin fill levels, raises overflow alerts, plans garbage-truck routes and produces city-wide reports.

**Team:** Sasyak Subudhi (PES1UG24AM256) | Shriya Vasundhara Singh (PES1UG24AM269) | Shreya Yashodhara Singh (PES1UG24AM266) | Shruti Choudhary (PES1UG24AM271)

## Run locally
```bash
pip install -r requirements.txt
pytest --cov --cov-branch     # run all tests with statement + branch coverage
python generate_reports.py    # regenerate the four test reports in docs/
```

## Structure
| Path | Purpose |
|---|---|
| `src/waste_mgmt/` | Application code (bins, alerts, routing, reports) |
| `tests/` | Unit tests and system tests |
| `docs/` | SRS, SAD, STP, Test Case Document and test reports |
| `.github/workflows/ci.yml` | CI: runs tests on every push and pull request |

## Contributing
One feature = one branch = one pull request with tests, reviewed by a teammate, merged only when CI is green. See `docs/STP.md` for roles.

### Workflow for every new feature
```
main -> git pull -> feature/new-feature -> add code + tests -> pytest -> git add . -> git commit -> git push
     -> Pull Request to main -> GitHub Actions (test passes) -> 1 teammate approval -> merge -> main
```
