# Priority Picker v3 — implementation plan and evidence

## Requirements map

- **Python contract:** implement the frozen score formula, required field/range/status validation, unique IDs, decimal support, deterministic ranking/tie breaks, filtering, sorting with errors for unsupported keys/directions, JSON export, and file loading. Public operations must preserve caller-owned inputs; empty backlogs are valid.
- **Dashboard:** fetch the backlog through the existing API; show counts, search/status/risk/sort controls, ranked factor breakdowns, keyboard-operable item details, and JSON export of the current ordering. Include useful loading, empty, invalid-data, and export feedback states.
- **Explainability and observability:** give each factor an explanation reachable on hover and focus; implement the specified test IDs, status/tier/selection states, and a default-off debug panel with request, control, state, and error details. Debug mode must not affect application results.
- **Responsive/accessibility:** no horizontal page overflow at 1440×1000, 834×1112, or 390×844; visible control labels, keyboard operation, visible focus/selection, and usable layouts at all three sizes.
- **Constraints:** standard library and browser-native assets only; leave `data/backlog.json` unchanged; add focused public tests and concise run/use instructions.

## Intended file changes

- `priority_picker/priority.py` — implement and validate the public Python API, preserving inputs and deterministic behavior.
- `priority_picker/web/index.html`, `styles.css`, `app.js` — implement the dashboard, responsive presentation, interactions, factor help, export feedback, and debug surface.
- `priority_picker/server.py` — adjust only if inspection or integration shows the existing API/static serving needs a focused change for the UI contract.
- `tests/public/test_priority.py` — extend with focused validation, decimal, immutability, tie-break, filter/sort error, empty, scale, and export coverage.
- `README.md` — concise launch, use, and verification instructions.
- `data/backlog.json` — explicit non-target; do not change.

## Verification plan

- Run `python -m unittest discover -s tests/public -v` after implementation.
- Add focused checks for malformed/missing fields, duplicate IDs, empty input, decimal values, caller-input immutability, unsupported sort options, and correct export ordering; exercise 1,000 valid items against the two-second limit.
- Start with `python -m priority_picker.server` and use the browser to verify data loading, filters, sort, detail selection, export JSON and visible confirmation, invalid/empty states, and debug fields/update behavior.
- At 1440×1000, 834×1112, and 390×844, check for horizontal overflow and usable controls/list layout. Keyboard-check labels, tab order, factor tooltip focus, item selection/detail interaction, export, and debug toggle. Check at least three fixture status styles and top-three styling.

## Risks and open checks

- The current public suite covers only the score, one tie, range rejection, basic filter/sort, export, and server handler presence; it does not cover the UI or most corrected-v2 and BM5 requirements.
- There is no browser automation dependency in scope. Visual, hover/focus, keyboard, and responsive checks are therefore planned as manual browser checks unless the environment provides an existing browser workflow without adding dependencies.
- Keep server changes narrow: the starter already exposes ranked items at `/api/items`, and the debug request surface can report that client request without adding a service.

## Explicit non-targets

- No changes to task requirements or supplied backlog data.
- No package-manager dependencies, build systems, network services, analytics, authentication, persistence, or unrelated abstractions.
- No changes to the canonical requirements, supplied fixture, benchmark evidence paths, or server architecture.

## Implement phase evidence

- Implemented all seven public Python functions with validation, duplicate detection, four-place scoring, stable default tie-breaks, filters, sorting-option errors, deep-copy isolation, JSON export, and file loading. `Decimal` values work in direct API calls and export.
- Replaced the placeholder page with a responsive dashboard, labeled controls, status and tier styling, focusable factor explanations, keyboard item selection, detail breakdown, JSON export feedback, and default-off debug diagnostics. The existing server endpoint was sufficient and remains unchanged. `data/backlog.json` remains unchanged.
- Expanded the public suite from five to ten focused tests, including malformed/duplicate inputs, decimal values, unsupported sorts, empty input, mutation isolation, export, and 1,000-item performance. Updated the run/use README.
- Commands and results: `rtk proxy python -m unittest discover -s tests/public -v` — 10 tests passed (including the 1,000-item check, completed in 0.040s); `rtk proxy python -m py_compile priority_picker/priority.py priority_picker/server.py` — passed; `rtk proxy node --check priority_picker/web/app.js` — passed; `rtk proxy git diff --check` — passed. The server could not bind a local port in this sandbox (`PermissionError: Operation not permitted`). Chromium is installed, but its headless launch was blocked by the sandbox's profile-directory and crashpad socket permissions; the browser harness was removed. HTTP/browser interaction and viewport checks therefore could not be completed.
- Files changed: `priority_picker/priority.py`, `priority_picker/web/index.html`, `priority_picker/web/styles.css`, `priority_picker/web/app.js`, `tests/public/test_priority.py`, `README.md`, and this plan. `priority_picker/server.py` and the supplied fixture were not changed.
- Remaining uncertainty: browser-only hover, keyboard, download, and pixel-level no-overflow behavior could not be exercised here; responsive layouts and focus/hover states are implemented in browser-native assets. No dependency or build tooling was added.

## Verify-repair phase evidence

- Re-ran `rtk proxy python -m unittest discover -s tests/public -v` — all 10 tests passed in 0.076s, including malformed/duplicate input, empty input, decimals, immutability, export, and 1,000-item ranking.
- Ran `rtk proxy python -m py_compile priority_picker/priority.py priority_picker/server.py`, `rtk proxy node --check priority_picker/web/app.js`, and `rtk git diff --check` — all passed.
- Confirmed the unchanged supplied fixture loads 6 items across 4 statuses (`blocked`, `in_progress`, `planned`, `ready`). `rtk git diff -- data/backlog.json` was empty.
- Attempted to start the server on port 0; sandbox socket creation failed with `PermissionError: Operation not permitted`. Playwright is installed and has a bundled Chromium, but launch stops at `sandbox_host_linux.cc` with `Operation not permitted`. Browser interaction, keyboard, download, and viewport overflow checks remain unverified for this reason.
- No implementation defect requiring repair was found during source review; no code or tests were changed in this phase. This evidence section is the only phase update.
