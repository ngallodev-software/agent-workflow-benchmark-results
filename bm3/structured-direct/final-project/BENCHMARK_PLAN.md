# Priority Picker v2 phase-one plan

## Requirements map

- `priority_picker/priority.py`: implement the frozen score formula, strict
  validation (including required fields, types/ranges, statuses, duplicate
  IDs, and useful errors), deterministic ranking, filtering, supported sorting,
  JSON export, and backlog loading. Preserve caller inputs by copying output
  records; accept decimal numeric values and empty lists.
- `priority_picker/server.py`: keep the stdlib server boundary; ensure valid
  ranked data and validation/JSON/file errors produce useful API responses.
- `priority_picker/web/index.html`, `app.js`, `styles.css`: replace the stub
  with a responsive, keyboard-operable dashboard using all required
  `data-testid` hooks. Provide summary counts, labeled search/status/risk/sort
  controls, ranked factor display, accessible item detail interaction,
  current-order JSON download, and empty/invalid states.
- `tests/public/test_priority.py` (and focused additions if needed): cover
  corrected v2 determinism, immutability, decimal values, malformed records,
  empty input, scale, filters/sorts, export, and server behavior.
- `README.md`: add concise standard-library run/test instructions and the
  browser/server workflow.
- `data/backlog.json`: leave unchanged.

## Intended file changes

1. Implement the existing public API in `priority_picker/priority.py`; avoid
   new dependencies or abstractions.
2. Build the UI in the existing three web files and use the existing API route.
3. Add focused regression tests and update the README.
4. Do not add build tooling, services, persistence, analytics, auth, or other
   unrelated files.

## Verification commands

Planned after implementation:

```sh
python -m unittest discover -s tests/public -v
python -m compileall -q priority_picker tests/public
python - <<'PY'
from priority_picker.priority import load_backlog, rank_items
items = load_backlog("data/backlog.json")
assert len(items) == 6
assert len(rank_items(items)) == 6
PY
```

Also exercise a generated 1,000-item valid backlog and malformed/duplicate,
empty, decimal, immutable-input, unsupported-sort, and export cases with the
focused tests. Start `python -m priority_picker.server --port 8000` and check
`/api/items`, static assets, and invalid-data responses.

## Visual and accessibility checks

- Inspect at 1440x1000, 834x1112, and 390x844: no horizontal overflow,
  readable hierarchy, usable control spacing, and sensible list/detail layout.
- Verify visible labels remain associated with controls; keyboard-only tab,
  enter/space, focus visibility, and detail open/close work.
- Verify empty and invalid API states are understandable, factor values and
  score remain visible, and export downloads the displayed ordering as JSON.
- Confirm all stable hooks exist exactly: `priority-app`, `search-input`,
  `status-filter`, `risk-filter`, `sort-control`, `priority-list`,
  `priority-item`, `item-detail`, and `export-button`.

## Risks and mitigations

- Numeric booleans or non-finite values can pass loose Python checks: reject
  them explicitly while allowing real decimal values in 1..5.
- Sorting/filtering can accidentally mutate records or consume iterators:
  validate/copy once and return new lists; test input snapshots.
- Browser state can diverge from displayed ordering: keep one current filtered
  and sorted collection as the render/export source.
- Invalid JSON/API failures can otherwise look blank: render a distinct error
  state and keep the controls operable where possible.
- Responsive card layouts can overflow long titles/descriptions: wrap text
  and test the narrow viewport explicitly.

## Explicit non-targets

No changes to the canonical task requirements or supplied backlog data; no
package manager, third-party dependency, build system, database, network
service beyond the supplied stdlib server, authentication, persistence,
analytics, or unrelated refactor. No visual claim is made until the UI is
implemented and inspected.

## Phase evidence

Commands run:

- `python -m unittest discover -s tests/public -v`: **passed**, 7 tests.
- `python -m compileall -q priority_picker tests/public`: **passed**.
- Direct edge checks: decimal values and Decimal export, empty input, duplicate
  and malformed records, immutable outputs, unsupported sorting, 1,000-item
  ranking in 0.0167s, and export: **passed**.
- `node --check priority_picker/web/app.js`: **passed**.
- `git diff --check`: **passed**.

The stdlib server/API smoke check could not connect because this environment
denies socket creation (`PermissionError: Operation not permitted`); static
server code and the handler contract remain covered without opening a port.
No browser viewport automation is available in this worktree, so visual
checks are limited to responsive CSS inspection and stable-hook inspection.

The repair pass corrected descending sort ties to keep ID ascending, made
Decimal values JSON-exportable without mutating inputs, escaped interpolated
UI text, and constrained long text in the responsive card/detail grid.

Files changed in this phase: `priority_picker/priority.py`,
`priority_picker/server.py` unchanged, `priority_picker/web/index.html`,
`priority_picker/web/app.js`, `priority_picker/web/styles.css`,
`tests/public/test_priority.py`, `README.md`, and this plan.
