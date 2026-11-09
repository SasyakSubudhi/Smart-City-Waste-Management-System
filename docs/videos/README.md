# Sprint outcome recordings

Status: recording preparation only. The team has not yet supplied the two actual
screen recordings. This directory must not be treated as completed video evidence.

## Required files

- `sprint1_demo.mp4`: about one minute, real bin registration, rejected invalid
  readings, actual statuses and `docs/SRS.md`.
- `sprint2_demo.mp4`: about two minutes, real alerts, two truck assignments,
  unassigned bins, confirmed collection, city report, live tests/coverage and the
  matching successful GitHub Actions run.

Silent recording is the team's proposed format. Use readable on-screen member
names/module credits and short explanatory captions. Confirm any separate
instructor narration requirement. Record the actual working application; do not
replace it with generated footage, fabricated test output or the supplied tutorial.

## Before capture

Pull reviewed main, install requirements, and run the actual suite. At the checked
main revision `1344aaf94155af94c4832ed0a3bfc371f8ff1f63`, 86 tests passed with
100% measured statement and branch coverage. This is a dated preflight result,
not a claim about a future recording. Recheck the real recording revision.

`demo.py` is still in PR #14 at preparation time. Run `python demo.py` only after
it actually merges. Run a web UI only if its reviewed files/dependencies actually
exist on main; a CLI video does not prove a graphical interface is implemented.

## Upload and review

If an MP4 exceeds the team's 25 MB web-upload threshold, upload the actual video
to Google Drive and replace the relevant pending entry below with its real view
link. Do not add invented links or call a pending recording complete.

| Outcome | File or actual viewing link | Status |
|---|---|---|
| Sprint 1 | Pending team capture | Not recorded |
| Sprint 2 | Pending team capture | Not recorded |

Use branch `docs/demo-videos`. Keep the PR in draft until actual playable videos
or verified viewing links are present. Ask Shreya (`yasho-26singh`) or Shruti
(`codeninja-1234`) to review them. Merge only after independent approval and CI.
