# Sprint outcome screen recordings

Both files are real, silent Windows screen captures recorded on 9 November 2026.
Names and module credits are visible on screen. There is no voice narration.

| Outcome | Video | Duration |
|---|---|---|
| Sprint 1 | [sprint1_demo.mp4](sprint1_demo.mp4) | 1 minute |
| Sprint 2 | [sprint2_demo.mp4](sprint2_demo.mp4) | 2 minutes |

Download the MP4s if the GitHub inline viewer does not play them. Both are below
the chosen 25 MB web-upload threshold, so external viewing links are unnecessary.

## What is recorded

Sprint 1 shows real Bin/BinRegistry registration, the OK / NEARLY_FULL / FULL
statuses, rejection of decimal 50.5 and out-of-range 150 without state mutation,
the actual `docs/SRS.md`, and each member's name/module contribution.

Sprint 2 shows real critical-first alerts, two one-bin trucks, B2 remaining
unassigned, confirmation of both selected routes, refreshed alerts and city report,
the actual test process output, and the matching successful GitHub Actions run.

Source revision: `1344aaf94155af94c4832ed0a3bfc371f8ff1f63`.
CI evidence: https://github.com/SasyakSubudhi/Smart-City-Waste-Management-System/actions/runs/42586850263

The recording window is a local display driver invoking the unchanged Python
package APIs and real test subprocess. It is not a merged graphical product UI.
`demo.py` and the proposed Streamlit UI were not on the recorded main revision,
so the clips do not claim to show those unmerged files. The original tutorial
video was not reused. Product output and test results were not replaced with
preset success screens. Only capture padding was trimmed for readability, and
the actual CI-window capture is joined to the end of the integrated-flow clip.

The team's proposed silent format uses readable captions/module credits. Confirm
any separate instructor requirement for spoken narration before final submission.
These captures demonstrate current outcomes; they do not backdate sprint evidence.

## Review before merge

Check playback, legibility, required content, source/CI match and the actual test
summary. Optional SRT files are sidecar caption tracks; the video already contains
visible headings and credits. No browser/private meeting content is intended for
these clips. Request independent review from Shreya or Shruti and merge only after
approval and required CI checks pass.
