# Priority Picker v2 plan

## Requirements map

- Python API: implement the frozen four-decimal score, strict record and duplicate-ID validation, deterministic ranking, filtering, sorting with rejected unsupported keys/directions, JSON export, and backlog loading. Decimal factor values in range are valid. Return copied data and avoid mutating caller sequences or dictionaries.
- Dashboard: serve the validated, ranked backlog from the existing stdlib HTTP server. Build a responsive page with summary counts, labeled search/status/risk/sort controls, ranked rows and all five factors, keyboard-operable details, JSON download of the current ordering, and useful empty/error states. Keep every required `data-testid` hook.
- Constraints: stdlib Python and browser-native HTML/CSS/JS only; leave `data/backlog.json` unchanged; update focused public tests and concise run instructions; support 1,000 records under two seconds; avoid page overflow at 1440×1000, 834×1112, and 390×844.

## Intended file changes

- `priority_picker/priority.py`: implement the required public functions and validation error handling; keep results independent of caller-owned containers.
- `priority_picker/server.py`: inspected and retained unchanged; it already serves the static assets and ranked endpoint, and maps validation failures to useful JSON errors.
- `priority_picker/web/index.html`, `app.js`, `styles.css`: implement the labeled dashboard, interactions, accessibility, responsive layout, empty/error presentation, and current-order JSON download.
- `tests/public/test_priority.py`: extend focused coverage for Decimal values and rounding, malformed records and duplicate IDs, empty input, deterministic ties, unsupported sort arguments, non-mutation, filtering, export, and 1,000-item ranking.
- `README.md`: replace starter text with concise launch and verification instructions.
- `BENCHMARK_PLAN.md`: this phase plan and evidence record.

## Execution evidence

- `rtk python -m unittest discover -s tests/public -v`: 10 tests passed (0.049 seconds), including Decimal values, malformed records, duplicates, empty input, non-mutation, rejected sort arguments, export, and 1,000-item ranking.
- `rtk python -m compileall -q priority_picker tests/public`, `rtk node --check priority_picker/web/app.js`, and `rtk git diff --check`: passed.
- Direct `Handler.do_GET` exercise with temporary data returned HTTP 200 for valid and empty backlogs; HTTP 422 with useful JSON errors for duplicate IDs and malformed JSON; HTTP 200 for `/`, `/app.js`, and `/styles.css`; and HTTP 404 for a traversal path.
- No browser automation tool is available in this environment. A previous headless Chromium attempt exited when crashpad socket setup was denied. Responsive rendering at the three target sizes, live keyboard interaction, and an actual browser download remain unverified. The browser source exposes native labeled controls and buttons for keyboard operation; source inspection is not a substitute for browser verification.
- `rtk git diff -- data/backlog.json` is empty; the supplied fixture remains unchanged. The untracked `.agent-workflow-benchmark/` path is benchmark-managed and was not opened or modified. Test-generated `__pycache__` directories were removed.
- Final scope review: changes are limited to the Python module, browser-native UI, focused public tests, README, and this plan. No dependencies or network imports were added. The existing server code required no edit.

## Risks and non-targets

- Remaining uncertainty: browser rendering, keyboard interaction, responsive overflow, and downloaded-file behavior could not be exercised because the sandbox blocks local sockets and Chromium startup. The export uses the active filtered ordering in code, but a real browser download was not verified.
- Non-targets: changing the frozen score or task requirements; editing supplied backlog data; dependencies, build systems, external services, analytics, authentication, persistence, or unrelated abstractions; inspecting benchmark-managed evidence paths.

## Phase-one evidence

- Inspected the starter source, README, and `tests/public/test_priority.py`; found Python API stubs, a minimal page, and five visible tests covering formula, tie order, one invalid range, filtering/sorting, export, and handler presence.
- `rg --files` showed the starter file set; `git status --short --branch` showed the benchmark worktree and an untracked benchmark evidence directory, which was not inspected or modified.
- Read-only data summary: `data/backlog.json` is a six-item array with all nine required fields and all four allowed statuses.
- No implementation or test commands were run in this analyze-plan phase.
- At plan creation, only `BENCHMARK_PLAN.md` had changed. Remaining uncertainty at that point: implementation, browser behavior, and acceptance checks.
