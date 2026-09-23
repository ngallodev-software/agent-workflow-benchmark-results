# Priority Picker v3 — phase-one plan

## Requirements map

- **Python contract:** implement the frozen score formula, item validation (including unique IDs, required fields, decimal values, and useful errors), deterministic ranking, filtering, sorting with rejected unsupported keys/directions, JSON export, and loading. Preserve caller-owned inputs; support empty input and 1,000-item ranking.
- **Dashboard:** replace the placeholder with a responsive ranked backlog interface, summary counts, labeled search/status/risk/sort controls, item detail interaction, JSON export, and useful loading/invalid/empty states. Match all required `data-testid` hooks.
- **Explainability and hierarchy:** provide all five factor explanations on hover and keyboard focus, a distinct summary and control panel, score and status hooks, visible status distinctions, top-three styling, and an accessible visible selected state.
- **Feedback and observability:** show a persistent, non-modal export success message. Keep debug mode off by default; when enabled, expose deterministic request, state, error, and bound-control details with the specified text and attributes. Control changes and initial load update the panel.
- **Constraints:** use Python standard library and browser-native HTML/CSS/JavaScript only. Keep `data/backlog.json` unchanged. Add focused public coverage and concise run instructions.

## Starter inspection

- `priority_picker/priority.py` declares the required API; all functions except JSON-root handling in `load_backlog` are stubs.
- `priority_picker/server.py` serves `/api/items` and the static web files using the standard library.
- `priority_picker/web/index.html`, `app.js`, and `styles.css` are placeholders.
- `tests/public/test_priority.py` currently checks the basic formula, ID tie-break, one malformed range, basic filter/sort, export, and the server handler. It has no UI, accessibility, scale, decimal, immutability, duplicate-ID, empty-input, unsupported-sort, or debug/export-feedback coverage.
- `data/backlog.json` contains six items spanning all four statuses. The worktree began with an unrelated untracked `.agent-workflow-benchmark/` path; preserve it.

## Intended file changes

- `priority_picker/priority.py`: implement and validate the Python API contract without mutating inputs.
- `priority_picker/web/index.html`, `app.js`, `styles.css`: implement the dashboard, interactions, required hooks, responsive layout, accessible factor help, export feedback, and debug surface.
- `tests/public/test_priority.py`: expand focused tests for malformed and empty data, decimals, immutability, deterministic ranking/sorting, filtering, export, and the 1,000-item performance bound where stable.
- `README.md`: replace starter text with concise setup/run and usage instructions.
- `BENCHMARK_PLAN.md`: retain this requirements map and append actual implementation/verification evidence and any remaining uncertainty during the implementation phase.

## Verification commands for implementation phase

- `python -m unittest discover -s tests/public -v` — public regression and added Python contract tests.
- A focused standard-library script or added test for 1,000 valid records, checking deterministic output and elapsed time below two seconds.
- Start the server with `python -m priority_picker.server --host 127.0.0.1 --port 8000`; request `/` and `/api/items` and check successful HTML/JSON responses. Also exercise malformed-data handling through the API if supported by a temporary fixture, without changing supplied data.
- In a browser, inspect the page at 1440×1000, 834×1112, and 390×844 for overflow and usable controls; test keyboard-only navigation, focus/hover factor help, selection, empty and invalid states, export download/status, and debug panel updates/hooks.

## Visual and accessibility checks

- Confirm visible labels remain associated with search, status, risk, and sort controls at each target viewport; controls wrap or stack without horizontal page overflow.
- Confirm top three items stand out, at least the fixture's four statuses have distinct badges, and selection has both visible styling and an accessible selected state.
- Tab to each factor help trigger and verify its matching tooltip is visible; also verify mouse hover. Open/close/select item details and operate export/debug using the keyboard.
- Check empty, request-failure/invalid-data, successful export, and debug-off/default states. Verify debug attributes reflect the initial request and subsequent control changes, and export feedback remains visible for deterministic capture.

## Risks and non-targets

- The visible suite does not exercise browser behavior, so browser checks are necessary; no browser automation dependency is permitted by the task constraints.
- Keep the score formula and default tie-break order exactly as specified; avoid relying on incidental source order for ties.
- Non-targets: modifying `data/backlog.json`; adding dependencies, build systems, network services, analytics, authentication, persistence, or unrelated abstractions; changing canonical requirements; editing benchmark-owned evidence paths or the unrelated untracked baseline path.

## Phase-one evidence

- Implemented scoring, validation, deterministic rank/filter/sort, JSON export, and backlog loading in `priority_picker/priority.py`. Decimal inputs are accepted and serialized as JSON numbers; returned records are copies.
- Replaced the placeholder page with the responsive dashboard and required controls, details, factor help, status/tier styling, export feedback, and debug observability in `priority_picker/web/index.html`, `app.js`, and `styles.css`.
- Expanded public contract coverage and added concise run/API instructions in `tests/public/test_priority.py` and `README.md`.
- `python -m unittest discover -s tests/public -v`: passed, 12 tests. The 1,000-item deterministic ranking test also asserts runtime below two seconds.
- `node --check priority_picker/web/app.js`: passed.
- `python -m py_compile priority_picker/priority.py priority_picker/server.py`: passed.
- `git diff --check`: passed.
- Attempted `python -m priority_picker.server --host 127.0.0.1 --port 8000`; the managed environment denied socket creation with `PermissionError: [Errno 1] Operation not permitted`, so live HTTP smoke checks could not run.
- No browser automation is installed in the exposed tool set, so viewport rendering, keyboard interaction, hover/focus tooltip, and download behavior have not been exercised in a browser. Responsive breakpoints, labels, focus states, keyboard-native controls, and event handlers are implemented and source-reviewed.
- Review confirmed the supplied fixture is unchanged and the only intended tracked edits are the six implementation/documentation/test files listed above. The initial untracked `.agent-workflow-benchmark/` path and generated Python bytecode are preserved as baseline/runtime artifacts.

## Verify-repair phase evidence

- `python -m unittest discover -s tests/public -v`: passed, 12 tests, including decimal, empty, malformed, immutability, deterministic tie-break, and 1,000-item timing coverage.
- `node --check priority_picker/web/app.js`, `python -m py_compile priority_picker/priority.py priority_picker/server.py`, and `git diff --check`: passed.
- Loaded and ranked the supplied fixture through the public Python API: 6 items across all four statuses; top item `BKL-103`.
- Confirmed the required UI hooks, focus-visible styles, focus and hover factor tooltip rules, and responsive breakpoints by source inspection. Browser tooling is unavailable in the exposed tool set, so rendered viewport, keyboard, and download behavior could not be exercised.
- Retried the standard-library server smoke check; the managed environment denied socket creation with `PermissionError: [Errno 1] Operation not permitted`. No HTTP request could be made.
- No implementation defect was exposed by the available checks. `data/backlog.json` remains unchanged; the only new tracked change in this phase is this evidence update. Untracked benchmark/runtime artifacts were preserved.
