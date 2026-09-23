# Priority Picker v2 implementation plan and evidence

## Requirement map

- Python API validates all required fields, unique IDs, statuses, and numeric ranges; accepts decimal numbers; does not mutate inputs; calculates the frozen four-place score; and supports deterministic rank, filter, sort, export, and load operations.
- Browser dashboard presents counts, labeled search/status/risk/sort controls, ranked rows, all scoring factors, keyboard-operable detail disclosure, JSON export of the current ordering, and clear invalid and empty states.
- Layout uses native HTML/CSS/JavaScript and adapts to desktop, tablet, and mobile without added dependencies. Required `data-testid` hooks are present.
- Standard-library server reads the supplied `data/backlog.json`, which remains unchanged.
- Focused public tests and concise startup/API guidance are included.

## Scope and explicit non-targets

Changed for this verify-repair phase: `priority_picker/web/styles.css` and this plan. The existing Python API, page markup, browser behavior, tests, and README were reviewed and retained.

No dependencies, services, build system, persistence, analytics, authentication, or unrelated abstractions were added. `data/backlog.json` was preserved. The pre-existing untracked benchmark-owned worktree path was left untouched.

## Verification evidence

Checks run for Agent Run `bench-2f04a4980796a39e5f091d89-verify-repair`:

- Public suite: `python -B -m unittest discover -s tests/public -v` — 8 tests passed.
- Standard-library compilation and `node --check priority_picker/web/app.js` — passed.
- Browser verification in Chromium/Playwright at 1440×1000, 834×1112, and 390×844 — no horizontal overflow. Enter opened item details; empty search and malformed API data showed useful messages; JSON export downloaded all six currently ordered items.
- Ranking 1,000 valid records took 0.0179 seconds.
- HTTP integration fetched `/` and `/api/items`; the dashboard hook was present and the API returned all six supplied items.
- `git diff --check` passed. `data/backlog.json` has no diff.

## Remaining uncertainty

No known requirement remains unverified in this phase. Cross-browser behavior beyond the available Chromium run was not checked.
