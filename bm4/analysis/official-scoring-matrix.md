# BM4 official frozen scoring matrix

This document expands the official frozen BM4 machine scores without changing them.

- Structured direct: **79.5 / 100**
- Agent-Workflow optimized: **86.0 / 100**
- Official difference: **+6.5 points**

The scoring contract is binary per check; there is no partial credit in the official score.

## Dimension totals

| Dimension | Max | Structured direct | Agent-Workflow optimized | Difference |
| --- | ---: | ---: | ---: | ---: |
| Hidden functional | 45 | 36 | 39 | 3 |
| Public regression | 15 | 15 | 15 | 0 |
| Robustness | 10 | 10 | 10 | 0 |
| Accessibility / UI | 10 | 2.5 | 4 | 1.5 |
| Scope / completeness | 10 | 10 | 10 | 0 |
| Engineering quality | 10 | 6 | 8 | 2 |

The entire official +6.5-point difference comes from three checks:

- **+3.0** — `hidden.formula.effort-floor`: optimized passes; direct fails.
- **+1.5** — `ui.labels-landmark`: optimized passes; direct fails.
- **+2.0** — `quality.verification-plan`: optimized passes; direct fails.

## Full check matrix

| Dimension | Check | Max | Direct | Optimized | Delta | Direct result | Optimized result |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| Hidden functional | `hidden.formula.integer` — Frozen formula for integer factors | 4 | 4 | 4 | +0 | PASS — integer formula equals 10.0 | PASS — integer formula equals 10.0 |
| Hidden functional | `hidden.formula.decimal-rounding` — Decimal inputs and four-place rounding | 4 | 4 | 4 | +0 | PASS — decimal formula is rounded to four places | PASS — decimal formula is rounded to four places |
| Hidden functional | `hidden.formula.effort-floor` — Effort denominator floors at one | 3 | 0 | 3 | +3 | FAIL — calculate_priority floors effort at one: BacklogValidationError: item must include numeric impact, urgency, effort, confidence, and risk | PASS — calculate_priority floors effort at one |
| Hidden functional | `hidden.tie.score` — Primary score descending ordering | 3 | 3 | 3 | +0 | PASS — score descending is primary | PASS — score descending is primary |
| Hidden functional | `hidden.tie.urgency` — Urgency descending tie breaker | 3 | 3 | 3 | +0 | PASS — equal scores use urgency descending | PASS — equal scores use urgency descending |
| Hidden functional | `hidden.tie.impact` — Impact descending tie breaker | 3 | 3 | 3 | +0 | PASS — equal score/urgency uses impact descending | PASS — equal score/urgency uses impact descending |
| Hidden functional | `hidden.tie.id` — ID ascending final tie breaker | 3 | 3 | 3 | +0 | PASS — final tie uses ID ascending | PASS — final tie uses ID ascending |
| Hidden functional | `hidden.ranked-schema` — Ranked records contain rank and score without mutating input | 3 | 0 | 0 | +0 | FAIL — ranked records expose scores without mutating input | FAIL — ranked records expose scores without mutating input |
| Hidden functional | `hidden.search.title` — Case-insensitive title search | 2 | 2 | 2 | +0 | PASS — title search is case-insensitive | PASS — title search is case-insensitive |
| Hidden functional | `hidden.search.description` — Case-insensitive description search | 2 | 2 | 2 | +0 | PASS — description search is case-insensitive | PASS — description search is case-insensitive |
| Hidden functional | `hidden.filters.combined` — Search, status and risk filters compose | 3 | 3 | 3 | +0 | PASS — query/status/risk compose | PASS — query/status/risk compose |
| Hidden functional | `hidden.sort.supported` — Supported sort keys and directions are deterministic | 3 | 3 | 3 | +0 | PASS — supported keys and directions sort deterministically | PASS — supported keys and directions sort deterministically |
| Hidden functional | `hidden.sort.invalid` — Unsupported sort key or direction is rejected | 2 | 2 | 2 | +0 | PASS — invalid sort key/direction rejected | PASS — invalid sort key/direction rejected |
| Hidden functional | `hidden.export` — Export preserves current ordering and ranks | 3 | 0 | 0 | +0 | FAIL — export contains deterministic order and ranks | FAIL — export contains deterministic order and ranks |
| Hidden functional | `hidden.load` — JSON loading validates the supplied fixture | 2 | 2 | 2 | +0 | PASS — supplied fixture loads and validates | PASS — supplied fixture loads and validates |
| Hidden functional | `hidden.determinism` — Repeated operations are deterministic and non-mutating | 2 | 2 | 2 | +0 | PASS — repeatable operations do not mutate caller data | PASS — repeatable operations do not mutate caller data |
| Public regression | `public.formula` — Visible formula regression test | 3 | 3 | 3 | +0 | PASS — test_frozen_formula (__main__.PriorityTests.test_frozen_formula) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK | PASS — test_frozen_formula (__main__.PriorityTests.test_frozen_formula) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK |
| Public regression | `public.ranking` — Visible ranking regression test | 3 | 3 | 3 | +0 | PASS — test_ranking_uses_frozen_tie_breakers (__main__.PriorityTests.test_ranking_uses_frozen_tie_breakers) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK | PASS — test_ranking_uses_frozen_tie_breakers (__main__.PriorityTests.test_ranking_uses_frozen_tie_breakers) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK |
| Public regression | `public.validation` — Visible validation regression test | 3 | 3 | 3 | +0 | PASS — test_malformed_range_is_rejected (__main__.PriorityTests.test_malformed_range_is_rejected) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK | PASS — test_malformed_range_is_rejected (__main__.PriorityTests.test_malformed_range_is_rejected) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK |
| Public regression | `public.filter-sort` — Visible filter and sort regression test | 3 | 3 | 3 | +0 | PASS — test_filter_and_sort (__main__.PriorityTests.test_filter_and_sort) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK | PASS — test_filter_and_sort (__main__.PriorityTests.test_filter_and_sort) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.000s OK |
| Public regression | `public.export-server` — Visible export and server regression tests | 3 | 3 | 3 | +0 | PASS — test_export_and_server_contract (__main__.PriorityTests.test_export_and_server_contract) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.007s OK | PASS — test_export_and_server_contract (__main__.PriorityTests.test_export_and_server_contract) ... ok ---------------------------------------------------------------------- Ran 1 test in 0.007s OK |
| Robustness | `robust.required-fields` — Missing required fields are rejected | 2 | 2 | 2 | +0 | PASS — missing fields rejected | PASS — missing fields rejected |
| Robustness | `robust.types-ranges-status` — Types, ranges, statuses and booleans are validated | 2 | 2 | 2 | +0 | PASS — types/ranges/statuses/booleans rejected | PASS — types/ranges/statuses/booleans rejected |
| Robustness | `robust.empty-duplicate` — Empty input succeeds and duplicate IDs fail | 2 | 2 | 2 | +0 | PASS — empty accepted and duplicates rejected | PASS — empty accepted and duplicates rejected |
| Robustness | `robust.malformed-load` — Malformed roots and JSON fail usefully | 2 | 2 | 2 | +0 | PASS — malformed roots and JSON rejected usefully | PASS — malformed roots and JSON rejected usefully |
| Robustness | `robust.scale` — One thousand items rank within two seconds | 2 | 2 | 2 | +0 | PASS — one thousand items rank within two seconds | PASS — one thousand items rank within two seconds |
| Accessibility / UI | `ui.live-app` — The submitted live application loads | 1 | 0 | 0 | +0 | FAIL — live URL loaded; playwright=1.60.0; browser=151.0.7922.173; app_count=1; item_count=0; errors=["pageerror:Cannot read properties of null (reading 'addEventListener')", 'console:error:Failed to load resource: the server responded with a status of 404 (Not Found)', "pageerror:Cannot read properties of null (reading 'addEventListener')", "pageerror:Cannot read properties of null (reading 'addEventListener')"]; navigation_errors=[] | FAIL — live URL loaded; playwright=1.60.0; browser=151.0.7922.173; app_count=1; item_count=6; errors=['console:error:Failed to load resource: the server responded with a status of 404 (Not Found)']; navigation_errors=[] |
| Accessibility / UI | `ui.labels-landmark` — Persistent labels and one main landmark | 1.5 | 0 | 1.5 | +1.5 | FAIL — labels={'search-input': 0, 'status-filter': 0, 'risk-filter': 0, 'sort-control': 0}; main_count=1 | PASS — labels={'search-input': 1, 'status-filter': 1, 'risk-filter': 1, 'sort-control': 1}; main_count=1 |
| Accessibility / UI | `ui.search-filter-sort` — Search, filters and sort visibly update results | 2 | 0 | 0 | +0 | FAIL — initial=0; search=[]; blocked=0; sort_options=['priority-desc', 'priority-asc', 'urgency-desc', 'impact-desc', 'effort-asc', 'title-asc']; selected=priority-asc; before=[]; after=[] | FAIL — initial=6; search=[None]; blocked=1; sort_options=['priority-desc', 'priority-asc', 'urgency-desc', 'impact-desc', 'effort-asc', 'title-asc']; selected=priority-asc; before=[None, None, None, None, None, None]; after=[None, None, None, None, None, None] |
| Accessibility / UI | `ui.keyboard-detail` — Keyboard activation opens complete detail | 1 | 0 | 0 | +0 | FAIL — solution check failed: TimeoutError: Locator.focus: Timeout 30000ms exceeded. Call log: - waiting for locator("[data-testid=\"priority-item\"]").first | FAIL — solution check failed: TimeoutError: Locator.inner_text: Timeout 30000ms exceeded. Call log: - waiting for locator("[data-testid=\"item-detail\"]") |
| Accessibility / UI | `ui.visible-focus` — Computed focus indicator is visible | 1 | 1 | 1 | +0 | PASS — computed active-control style={'outlineStyle': 'solid', 'outlineWidth': '3px', 'boxShadow': 'none', 'borderColor': 'rgb(8, 126, 117)'} | PASS — computed active-control style={'outlineStyle': 'solid', 'outlineWidth': '3px', 'boxShadow': 'none', 'borderColor': 'rgb(216, 225, 227)'} |
| Accessibility / UI | `ui.responsive` — No horizontal overflow at all frozen viewports | 1.5 | 1.5 | 1.5 | +0 | PASS — no-overflow results=[True, True, True]; captured=3/3 | PASS — no-overflow results=[True, True, True]; captured=3/3 |
| Accessibility / UI | `ui.download` — Export produces a verified JSON download | 1.5 | 0 | 0 | +0 | FAIL — solution check failed: TimeoutError: Locator.click: Timeout 30000ms exceeded. Call log: - waiting for locator("[data-testid=\"export-button\"]") - locator resolved to <button disabled type="button" class="export-button" data-testid="export-button">…</button> - attempting click action 2 × waiting for element to be visible, enabled and stable - element is not enabled - retrying click action - waiting 20ms 2 × waiting for element to be visible, enabled and stable - element is not enabled - retrying click action - waiting 100ms 58 × waiting for element to be visible, enabled and stable - element is not enabled - retrying click action - waiting 500ms | FAIL — filename=priority-ordering.json; rows=6 |
| Accessibility / UI | `ui.empty-invalid` — Useful empty and invalid-data states are present | 0.5 | 0 | 0 | +0 | FAIL — empty_text=''; invalid_state=False | FAIL — empty_text=''; invalid_state=True |
| Scope / completeness | `scope.required-files` — Required Python and web files exist | 2 | 2 | 2 | +0 | PASS — required Python and web files exist | PASS — required Python and web files exist |
| Scope / completeness | `scope.plan` — Benchmark plan retains requirement traceability | 2 | 2 | 2 | +0 | PASS — phase plan retained | PASS — phase plan retained |
| Scope / completeness | `scope.readme` — README documents formula, operation and verification | 2 | 2 | 2 | +0 | PASS — README documents scoring, operation and tests | PASS — README documents scoring, operation and tests |
| Scope / completeness | `scope.immutable-input` — Supplied backlog remains unchanged | 2 | 2 | 2 | +0 | PASS — supplied fixture retained | PASS — supplied fixture retained |
| Scope / completeness | `scope.no-dependencies` — No package-manager dependency surface is added | 2 | 2 | 2 | +0 | PASS — no external dependency surface | PASS — no external dependency surface |
| Engineering quality | `quality.compile` — Python source and tests compile | 2 | 2 | 2 | +0 | PASS —  | PASS —  |
| Engineering quality | `quality.no-stubs` — No TODO or NotImplemented implementation stubs remain | 2 | 2 | 2 | +0 | PASS — no implementation stubs remain | PASS — no implementation stubs remain |
| Engineering quality | `quality.formula-doc` — Formula and tie breakers are documented | 2 | 0 | 0 | +0 | FAIL — formula and tie breakers documented | FAIL — formula and tie breakers documented |
| Engineering quality | `quality.verification-plan` — Plan records verification and non-targets | 2 | 0 | 2 | +2 | FAIL — plan records verification and non-targets | PASS — plan records verification and non-targets |
| Engineering quality | `quality.deterministic-design` — Implementation is concise, deterministic and dependency-free | 2 | 2 | 2 | +0 | PASS — implementation remains bounded and has no undeclared network client | PASS — implementation remains bounded and has no undeclared network client |

## Why the official score gap can look too small

The frozen contract weights the implementation as follows:

- hidden functional: **45/100**
- public regression: **15/100**
- robustness: **10/100**
- accessibility/live UI: **10/100**
- scope/completeness: **10/100**
- engineering quality: **10/100**

So **70/100 points** are Python/library correctness and robustness, while only **10/100 points** measure the live browser product.

Both implementations pass `hidden.load`: their Python/server path loads and validates the supplied JSON fixture. The structured-direct product failure occurs later in the browser integration path. Its visual evidence shows `item_count=0` plus JavaScript errors, so the required ranked data never becomes visible to the user.

Because the official UI bucket is only 10 points, that severe product-level failure does not produce a correspondingly large official score gap. The supplementary end-to-end product rubric in `end-to-end-product-rubric.md` exists to make that distinction explicit without modifying the frozen score.
