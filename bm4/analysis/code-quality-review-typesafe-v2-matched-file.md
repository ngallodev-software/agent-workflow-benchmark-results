# Combined code quality review

## Deterministic review

# BM4 source code quality review

Static review of the published final-project source in both BM4 arms. Scores are reviewer judgments on a 0–100 scale, not the benchmark machine scores. They weigh task correctness and edge handling most heavily, then maintainability, accessibility, and fit for the file’s role. Related files were read together where behavior crosses Python, HTML, JavaScript, and CSS. No tests or live browser checks were run for this review.

## Structured Direct

### `priority_picker/__init__.py` — 95%

**Strengths:** Correctly minimal package marker; no accidental import side effects or unnecessary exports.

**Weaknesses:** Provides no package-level public API, but the task does not require one and the module is intentionally small.

### `priority_picker/priority.py` — 86%

**Strengths:** Good boundary between validation, ranking, filtering, sorting, export, and loading. Decimal-based arithmetic avoids common floating-point score drift; booleans, non-finite values, and out-of-range factors are rejected. Input dictionaries are copied before sorting or export conversion. Errors identify the field or record, and deterministic default ranking implements the specified score/urgency/impact/ID order.

**Weaknesses:** `filter_items` searches title and description but not ID. Non-priority descending sorts reverse the earlier ID ordering for equal values, and priority ascending uses ascending urgency/impact as tie-breakers; those tie policies are not documented. `load_backlog` leaves filesystem errors raw, which is acceptable for the server to catch but less consistent for direct callers.

**Review correction:** An earlier draft said an unhashable `status` could leak `TypeError`. `STATUSES` is a tuple, so membership does not hash the supplied value; an invalid list value is rejected through `BacklogValidationError`. That concern is withdrawn. The score is unchanged.

### `priority_picker/server.py` — 88%

**Strengths:** Small standard-library server with clear routing, content types, useful API errors, and resolved-path containment before serving static files. Configuration is limited to host, port, and data path. No new dependency or framework is introduced.

**Weaknesses:** It is a development server with no request logging, cache/security headers, or production deployment boundary documented in the code. The broad `NotImplementedError` API catch appears unrelated to normal backlog loading and can mask an unexpected implementation defect as a client data error.

### `priority_picker/web/app.js` — 82%

**Strengths:** Escapes dynamic content before inserting HTML, keeps filter/sort/render behavior in small functions, supports keyboard-operable detail buttons, shows fetch failures, and exports the current visible ordering. Default priority sorting has the required tie-breaks.

**Weaknesses:** Search omits IDs even though IDs are useful selectors and the other arm supports them. Select controls listen to both `input` and `change`, causing redundant renders in browsers that emit both. Score display recalculates with JavaScript floating-point arithmetic while ordering primarily trusts the server value, so displayed and sorted scores can differ at rounding boundaries. The empty-state is distinct from the fetch-error path, but its summary wording and result count could better distinguish zero total from zero filtered results.

### `priority_picker/web/index.html` — 88%

**Strengths:** Semantic landmarks, explicit labels, native controls, useful status/error regions, export button state, and stable test hooks. Detail interaction is a real button with `aria-expanded` and `aria-controls`; content is deferred until needed.

**Weaknesses:** Several summary values start as em dashes and depend on JavaScript; that is a reasonable progressive enhancement tradeoff for this app. The result count is not independently announced as filters change, so screen-reader feedback depends on the live list region.

### `priority_picker/web/styles.css` — 89%

**Strengths:** Coherent visual system, clear focus-visible treatment, deliberate desktop/tablet/mobile layouts, and sensible text wrapping and overflow control. The component states have consistent spacing and color.

**Weaknesses:** Most rules are compressed into very long lines, making later review and targeted edits harder. Several colors are repeated as literals instead of using the existing custom properties. The CSS is responsive by construction, but this static review does not confirm the target viewport rendering.

### `tests/public/test_priority.py` — 82%

**Strengths:** Covers the frozen formula, default tie ordering, malformed and duplicate records, Decimal handling, non-mutation, empty input, supported sorting/filtering, scale, export, and module importability.

**Weaknesses:** `urlopen` is unused. Despite its server-contract test name, it only checks that `Handler.do_GET` is callable; it does not exercise an HTTP request or response. There is no focused test for unhashable status input, ID search, sort ties in both directions, or the UI behavior.

## Agent-Workflow Optimized

### `priority_picker/__init__.py` — 95%

**Strengths:** Correctly minimal package marker with no import side effects.

**Weaknesses:** No package-level API, which is not required by the task.

### `priority_picker/priority.py` — 84%

**Strengths:** Exact Decimal score calculation with explicit half-even rounding, useful validation errors, shallow-copy preservation, duplicate detection, and support for Decimal numeric inputs. Code is organized around the requested public functions. Default `rank_items` ordering uses the contract’s score/urgency/impact/ID sequence.

**Weaknesses:** `calculate_priority` does not itself enforce the 1–5 range (the normal backlog path validates first), leaving its public API less safe when called directly. `filter_items` assumes `query` is a string and silently treats unsupported status/risk filters as no matches. `sort_items` has no deterministic ID tie-breaker for equal primary values; default priority sorting also omits the specified urgency/impact tie-breakers. Filtering includes IDs, unlike Structured Direct. Export preserves caller order, which is useful for exporting a current UI ordering but makes the name ambiguous when called directly.

### `priority_picker/server.py` — 88%

**Strengths:** Same compact, dependency-free design and static path containment as Structured Direct. API errors are serialized consistently, and the server supports an explicit data path for isolated runs.

**Weaknesses:** Same development-server limitations: no production boundary, response hardening, or request logging. The broad `NotImplementedError` catch can misclassify unexpected failures as invalid backlog data.

### `priority_picker/web/app.js` — 89%

**Strengths:** Validates API payload shape, required fields, numeric ranges, status values, and duplicate IDs at the client boundary. Escapes interpolated content, searches IDs as well as title/description, handles empty/error states distinctly, retains an open detail by item ID across rerenders, and restores keyboard focus after toggling. Integer-scaled `BigInt` scoring avoids binary floating-point rounding drift for supported decimal inputs.

**Weaknesses:** The custom BigInt score routine is substantially more complex than needed for the bounded 1–5 data and depends on BigInt support in the browser. `aria-expanded` is present, but the detail button has no `aria-controls` relationship to its panel. `URL.revokeObjectURL` is delayed with a fixed one-second timeout; that may be short for a slow download consumer. Status labels are title-cased inconsistently (`in_progress` is formatted, other values retain lowercase).

### `priority_picker/web/index.html` — 88%

**Strengths:** Semantic sections, native labeled controls, a live result count, status/error message region, descriptive headings, and stable test hooks. Summary cards expose useful workload counts.

**Weaknesses:** Detail controls and panels are created by JavaScript without a declared `aria-controls` link. The static page itself has no meaningful backlog content before JavaScript loads, which is reasonable for the API-driven app but limits progressive enhancement.

### `priority_picker/web/styles.css` — 86%

**Strengths:** Consistent design tokens, responsive layouts at desktop/tablet/mobile widths, visible keyboard focus, and careful card/list/detail layouts. The design aligns well with the HTML structure.

**Weaknesses:** Nearly the entire stylesheet is a single line, which materially hurts readability and maintainability. `font-smooth` is non-standard and can be removed without affecting core layout. Some CSS properties and color values are repeated despite available custom properties. Responsive behavior was not confirmed in a browser as part of this static review.

### `tests/public/test_priority.py` — 84%

**Strengths:** Covers formula, ranking, invalid inputs, Decimal support and caller-data preservation, empty input, invalid sort arguments, filters, export, and the server handler contract. It checks an invalid non-string sort key as well as ordinary bad values.

**Weaknesses:** `urlopen` is unused. The server test checks method presence rather than HTTP behavior. It does not test default ranking tie-breakers, unsupported filter values/query types, non-finite Decimal inputs, large-input performance, or browser interactions.

## Comparative read

Agent-Workflow Optimized has the stronger browser-side defensive checks, ID search, score arithmetic, and interaction continuity. Structured Direct has simpler client code and more explicit server-side deterministic tie handling. Both Python implementations are competent and dependency-free, but both leave gaps around explicit sort/filter edge contracts; the control has a status-type validation hole, while the candidate has weaker default `sort_items` tie behavior. The server files are functionally near-identical. The biggest maintainability concern in both arms is CSS compression, especially the candidate’s single-line stylesheet.

The file scores are independent review judgments and should not be read as a statistically meaningful treatment comparison. The study is one development pair, and this review did not run tests or browser checks.

## TypeSafe ADK/API design for a faster, more balanced review

### Decision boundary

Use TypeSafe only as a second-opinion semantic reviewer for bounded quality judgments. It should assess code against the same BM4 contract and source evidence; deterministic code should inventory files, validate response schemas, calculate aggregates, preserve provenance, and render the report. A reviewer remains responsible for final scores and prose. TypeSafe must not invent source facts, modify files, or decide benchmark acceptance.

### Smallest useful flow

1. **Project state deterministically.** Enumerate the same seven source files per arm; attach treatment ID, relative path, language/role, SHA-256, exact source text, and only the relevant canonical-task requirements. Include paired HTML/JS/CSS context so UI behavior is assessed in context. Exclude benchmark scores and treatment labels from the judgment payload where practical to reduce anchoring.
2. **Batch independent `Score` judgments.** Ask the same versioned, self-contained rubric for each file across four ordered dimensions: contract/correctness, boundary/error handling, maintainability, and usability/accessibility (adapt the last dimension to the file’s role). Define five behaviorally distinct levels (0–4) in the question instructions. Batch file/dimension questions through the official TypeSafe ADK/API where its current contract permits. Do not replace these with one omnibus quality question.
3. **Validate and normalize locally.** The adapter checks response shape and question IDs, records the raw distributions, and distinguishes API failure from a valid uncertain answer. A deterministic policy converts each dimension’s expected 0–4 level to a percentage, then combines the fixed dimensions with documented weights. Keep the current human-reviewed score alongside the TypeSafe advisory score until calibration supports any change.
4. **Check proposed findings with `Noul`.** For each source-cited concern proposed by a deterministic check or human reviewer, ask the narrow proposition “Does the cited code support this concern under requirement X?” Include line range and requirement text. Noul only validates or flags review; it does not generate findings or suppress a finding automatically. Uncertain or contradictory results stay visible for human resolution.
5. **Write a compact application-owned receipt.** Store rubric/question-set version, file hashes, model/config identifier, normalized distributions, usage/latency if returned, fallback state, and source references. Keep secrets out of state and logs. Render the Markdown report from these receipts plus reviewer-approved prose.

### Token/time control and balance

Precompute the file inventory, hashes, language metadata, requirement map, line references, and simple static facts once. Send identical review instructions and code context for both arms in one bounded batch if the current API limits allow; otherwise split by arm, not by arbitrary file, so context stays coherent. Cache only by source hash plus question-set/model/policy version. That avoids repeat semantic calls on unchanged files and makes a BM4 rerun comparable. Do not trim code using token heuristics before review: source details are evidence, and omitted lines can hide defects. Measure total input tokens, wall time, disagreement rate, and human correction time against this manual review before claiming savings.

### Authority and rollout

Start in shadow/advisory mode. TypeSafe distributions and Noul checks are review evidence, not code-quality truth. Keep deterministic bounds checks and receipt validation local; on API failure, return the ordinary manual review without retrying identical semantic requests. Calibrate the score-to-percent mapping against independently reviewed examples before using it to influence headline scores. Version the projector, criteria, weights, questions, model choice, and aggregation policy. Verify current official SDK/API contracts and batch limits before implementation; this design does not assume a particular method signature.

### Consultation gate

No TypeSafe integration has been implemented. The proposed next step is a read-only shadow evaluator that emits a side-by-side advisory receipt and Markdown comparison, without changing the existing BM4 score or report. Review this boundary and the four-dimension rubric before implementation.

## TypeSafe advisory supplement

> Supplemental semantic evidence only. It does not replace, revise, or average into the deterministic review, benchmark machine scores, eligibility, human review, or acceptance.

Model: `jev-1.13.0`  
Left source: `/lump/apps/agent-workflow-benchmark-results/bm4/structured-direct/final-project`  
Right source: `/lump/apps/agent-workflow-benchmark-results/bm4/agent-workflow-optimized/final-project`  
Question set: `benchmark-code-quality/v2`  
Context scope: `matched-file`  
Candidate order: `balanced`  
Review mode: `comparative`  
Source files: 7 matched pairs; requests: 7; input tokens: 38295; output tokens: 1190

Composite percentages are deterministic weighted averages of TypeSafe expected 0–4 scores. Files have equal weight in arm averages.

| File | Left | Right | Delta (right − left) | Left strength / review focus | Right strength / review focus |
| --- | ---: | ---: | ---: | --- | --- |
| `priority_picker/__init__.py` | 72.9% | 74.0% | +1.0 pp | maintainability / correctness | maintainability / usability |
| `priority_picker/priority.py` | 55.3% | 56.1% | +0.8 pp | robustness / usability | robustness / maintainability |
| `priority_picker/server.py` | 56.0% | 57.1% | +1.2 pp | maintainability / correctness | maintainability / usability |
| `priority_picker/web/app.js` | 39.3% | 44.2% | +4.9 pp | usability / robustness | robustness / maintainability |
| `priority_picker/web/index.html` | 74.0% | 65.5% | -8.4 pp | maintainability / robustness | maintainability / robustness |
| `priority_picker/web/styles.css` | 68.3% | 61.1% | -7.2 pp | maintainability / robustness | maintainability / correctness |
| `tests/public/test_priority.py` | 77.1% | 53.6% | -23.5 pp | usability / robustness | usability / correctness |

## Per-file dimensions

### `priority_picker/__init__.py`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 2.74 / 0.00 | 2.88 / 0.07 |
| robustness | 25% | 2.86 / 0.05 | 3.02 / 0.19 |
| maintainability | 25% | 3.15 / 0.29 | 3.07 / 0.22 |
| usability | 15% | 3.04 / 0.20 | 2.85 / 0.04 |

### `priority_picker/priority.py`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 2.20 / 0.33 | 2.22 / 0.26 |
| robustness | 25% | 2.28 / 0.34 | 2.37 / 0.16 |
| maintainability | 25% | 2.19 / 0.38 | 2.13 / 0.21 |
| usability | 15% | 2.16 / 0.39 | 2.27 / 0.24 |

### `priority_picker/server.py`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 2.18 / 0.17 | 2.25 / 0.18 |
| robustness | 25% | 2.27 / 0.40 | 2.27 / 0.31 |
| maintainability | 25% | 2.32 / 0.19 | 2.41 / 0.24 |
| usability | 15% | 2.19 / 0.36 | 2.19 / 0.36 |

### `priority_picker/web/app.js`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 1.47 / 0.46 | 1.78 / 0.23 |
| robustness | 25% | 1.40 / 0.56 | 1.98 / 0.41 |
| maintainability | 25% | 1.75 / 0.51 | 1.62 / 0.29 |
| usability | 15% | 1.79 / 0.55 | 1.63 / 0.33 |

### `priority_picker/web/index.html`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 3.02 / 0.42 | 2.63 / 0.31 |
| robustness | 25% | 2.63 / 0.45 | 2.39 / 0.35 |
| maintainability | 25% | 3.21 / 0.34 | 2.88 / 0.37 |
| usability | 15% | 2.94 / 0.48 | 2.56 / 0.35 |

### `priority_picker/web/styles.css`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 2.69 / 0.34 | 2.21 / 0.30 |
| robustness | 25% | 2.56 / 0.29 | 2.51 / 0.25 |
| maintainability | 25% | 3.00 / 0.43 | 2.69 / 0.29 |
| usability | 15% | 2.66 / 0.36 | 2.47 / 0.29 |

### `tests/public/test_priority.py`

| Dimension | Weight | Left score / confidence | Right score / confidence |
| --- | ---: | ---: | ---: |
| correctness | 35% | 3.12 / 0.53 | 2.09 / 0.76 |
| robustness | 25% | 2.94 / 0.56 | 2.16 / 0.69 |
| maintainability | 25% | 3.14 / 0.51 | 2.16 / 0.70 |
| usability | 15% | 3.14 / 0.53 | 2.21 / 0.69 |

## Arm averages

- Left: 63.2%
- Right: 58.8%

## Limits

Scores are qualitative model judgments, not verified defects or proof that code works. Confidence and distributions are retained in the JSON sidecar. Run deterministic tests and independent human review for acceptance.
