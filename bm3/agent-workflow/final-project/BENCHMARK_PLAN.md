# Priority Picker v2 phase-one plan

## Scope and requirements map

| Requirement | Planned approach | Planned verification |
| --- | --- | --- |
| Frozen score and deterministic ranking | Implement the exact weighted formula, four-place rounding, and score/urgency/impact/id tie-breakers in `priority.py`. | Formula, decimal, tie-break, empty-input, and 1,000-item tests. |
| Strict backlog contract | Validate list records, required fields, types/ranges, allowed statuses, non-empty unique IDs, and useful errors through `BacklogValidationError`; preserve caller data and accept `Decimal` values. | Malformed-field, duplicate, invalid-status, decimal, non-mutation, and JSON-loading tests. |
| Public Python API | Implement filtering, supported-key/direction sorting, ranking, JSON export, and loading without mutating input sequences or dictionaries. Unsupported sort options raise the validation error. | Focused unit tests plus the visible public suite. |
| Dashboard and stable hooks | Build a semantic responsive layout with summary counts, labeled search/status/risk/sort controls, ranked factor cards, and the required `data-testid` hooks: `priority-app`, `search-input`, `status-filter`, `risk-filter`, `sort-control`, `priority-list`, `priority-item`, `item-detail`, and `export-button`. | Static inspection and browser checks at desktop, tablet, and mobile viewports. |
| Details, keyboard, states, and export | Make each item detail action keyboard-operable, expose description and all factors, show empty and invalid-data states, and download the currently displayed ordering as JSON. | Keyboard-only interaction, empty/invalid fixtures, and export-content checks. |
| Dependency-free delivery | Keep the stdlib server and browser-native HTML/CSS/JS; leave `data/backlog.json` unchanged and add no services, dependencies, build tooling, analytics, auth, or persistence. | `git diff --stat`, dependency review, server smoke test, and unchanged-data check. |

## Intended file changes

- `priority_picker/priority.py`: implement validation, scoring, ranking, filtering, sorting, export, and load behavior. Use copied records/results so public functions never mutate caller-owned data.
- `priority_picker/web/index.html`: replace the starter placeholder with the accessible dashboard structure and all stable hooks.
- `priority_picker/web/app.js`: fetch `/api/items`, render counts/list/details, handle controls and keyboard activation, manage error/empty states, and export the current ordering as JSON.
- `priority_picker/web/styles.css`: add the responsive dashboard styling, readable factor/status treatment, focus states, and overflow-safe mobile layout.
- `tests/public/test_priority.py`: retain the visible regression coverage and add focused v2 tests for the corrected determinism, validation, immutability, empty/scale, export, and server-facing behavior.
- `README.md`: document the stdlib test command and local server launch/usage instructions.

No change is planned for `data/backlog.json`. `priority_picker/server.py` should remain unchanged unless implementation testing identifies a narrowly necessary serving/error-path fix.

## Verification plan

Run from the repository root:

```sh
python -m unittest discover -s tests/public -v
python -m unittest discover -s tests -v
python -m json.tool data/backlog.json >/dev/null
python -m priority_picker.server --host 127.0.0.1 --port 0 --data data/backlog.json
```

The server smoke check will query `/api/items` and the static page before stopping the process. Add a small direct benchmark test for ranking 1,000 valid records and assert it completes comfortably below two seconds on the benchmark host.

Visual and accessibility checks:

- Load the served page at 1440x1000, 834x1112, and 390x844; confirm no horizontal page overflow and that controls/list/details remain usable.
- Use keyboard only to reach every control, activate an item detail, close/change detail state, and trigger export; verify visible focus and semantic labels.
- Check normal, empty-filter, empty-input, and invalid-API states; verify the list rank, score, status, five factors, and detail breakdown match the API.
- Confirm export JSON reflects the current filtered/sorted ordering and that errors are visible and actionable.

## Risks and mitigations

- `Decimal` values and JSON serialization can be lost through careless numeric coercion; validate numeric values without converting caller records in place and test exact rounded output.
- Stable ordering can regress when UI sorting and Python sorting diverge; keep sort keys explicit and test every supported direction/key against deterministic IDs.
- Narrow screens can overflow from factor/detail layouts; use wrapping/grid min-width constraints and test all three required viewport sizes.
- A malformed API response must not leave a blank dashboard; render a visible invalid-data state and cover it with a fixture or mocked response.
- The current server uses a relative default data path; README launch instructions will run it from the repository root, while explicit `--data` remains the reliable alternate.

## Explicit non-targets

Do not change supplied backlog data, add external packages or network services, introduce a build system, add authentication/analytics/persistence, redesign the server beyond the required API/static serving, or add unrelated abstractions.

## Phase-one and implementation evidence

- Inspected the starter source, data, README, and `tests/public/test_priority.py` before editing.
- Implemented the stdlib priority API, validation/immutability rules, responsive dashboard, keyboard-operable controls, details, empty/error states, and current-order export.
- `python -m unittest discover -s tests/public -v` — 9 tests passed, including Decimal values, malformed data, immutability, empty input, and 1,000-item performance.
- `python -m json.tool data/backlog.json >/dev/null` — passed; fixture remains unchanged.
- HTTP listener smoke check — blocked by the controlled worker's `PermissionError: [Errno 1] Operation not permitted` when binding a local socket; the server code path remains covered by the public contract test.
- Remaining uncertainty: Chromium/Chrome launch is blocked by the worker's crashpad socket policy, so visual pixel capture and native download behavior require host/browser verification; static hook, CSS, and JavaScript syntax checks passed.

## Verify-repair pass

- `python -m unittest discover -s tests/public -v` — 9 tests passed.
- `python -m unittest discover -s tests -v` — no additional tests discovered; command completed successfully.
- `python -m json.tool data/backlog.json`, `python -m py_compile priority_picker/*.py tests/public/test_priority.py`, and `node --check priority_picker/web/app.js` — passed; supplied data is unchanged.
- Direct edge checks — passed for Decimal scoring, tuple/generator-compatible inputs, non-mutation, risk filtering, deterministic sorting, malformed numeric values, export serialization, and required HTML hooks.
- No source repair was required after the contradiction, drift, scope, and stale-document review; the implementation commit is already the current HEAD.
