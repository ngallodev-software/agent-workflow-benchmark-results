# BM4 supplementary end-to-end product rubric

## Status

This is a **post-hoc supplementary rubric** applied to the frozen BM4 evidence. It does not replace, alter, or retroactively rescore the official BM4 machine score.

Official BM4 machine scores remain:

- Structured direct: **79.5 / 100**
- Agent-Workflow optimized: **86.0 / 100**
- Official gap: **+6.5 points**

The purpose of this secondary rubric is different: measure whether the delivered application works as an end-to-end product, including whether the required supplied data actually becomes visible and usable in the browser.

No model execution was rerun. No implementation was changed. Every secondary score below is derived from already-published BM4 evaluator, visual, source, and scoring evidence.

## Why a secondary rubric is warranted

The official scoring contract places **70 of 100 points** on Python/library behavior:

- hidden functional: 45
- public regression: 15
- robustness: 10

Only **10 of 100 points** are allocated to the live browser UI.

That weighting is appropriate for measuring library correctness, but it can understate an end-to-end product failure. In BM4, the structured-direct submission's Python/server path can load and validate `data/backlog.json`, so it earns the official `hidden.load` points and passes the public server contract. However, its browser code throws JavaScript errors, renders **zero priority items**, and leaves export disabled. The required product is a web application that presents the ranked backlog, so a supplementary product-oriented score should give much more weight to that integration failure.

The optimized submission renders all **six** expected backlog items. It still has several UI defects and therefore should not receive a near-perfect product score.

## Gating principle

Presentation credit that depends on real backlog data is earned only when the supplied fixture reaches the browser and the expected items are rendered.

If an implementation renders zero required data because of an application failure:

- it receives no credit for populated-data presentation;
- it receives no credit for interactions that require rendered items;
- the visual shell may still receive independent credit for properties that are actually observable, such as focus indication or responsive overflow.

This avoids pretending that an empty/broken shell demonstrates how the completed data-driven UI looks.

## 100-point supplementary rubric

| Dimension | Weight | Evidence basis |
| --- | ---: | --- |
| Core computation and data-layer correctness | 30 | Official hidden-functional evidence, proportionally scaled from 45 points |
| End-to-end data integration | 20 | Supplied fixture/API path, expected six-item browser render, populated browser state |
| Required interactive product behavior | 20 | Search/filter/sort, keyboard detail, export, empty/invalid states |
| Presentation and accessibility | 15 | Labels/landmarks, focus, responsive layout, observable populated-data presentation, runtime cleanliness |
| Robustness and failure handling | 5 | Official robustness evidence, proportionally scaled from 10 points |
| Engineering completeness and traceability | 10 | Official scope + engineering-quality evidence, proportionally scaled from 20 points |
| **Total** | **100** | |

## Applied BM4 product score

| Dimension | Max | Structured direct | Agent-Workflow optimized | Difference |
| --- | ---: | ---: | ---: | ---: |
| Core computation/data layer | 30 | 24 | 26 | +2 |
| End-to-end data integration | 20 | 5 | 20 | +15 |
| Required interactive behavior | 20 | 0 | 5 | +5 |
| Presentation/accessibility | 15 | 7 | 14 | +7 |
| Robustness/failure handling | 5 | 5 | 5 | 0 |
| Engineering completeness/traceability | 10 | 8 | 9 | +1 |
| **Supplementary product score** | **100** | **49** | **79** | **+30** |

## Point derivation

### 1. Core computation and data-layer correctness — 30 points

This reuses the frozen hidden-functional result, scaled from 45 to 30:

- Structured direct: 36/45 × 30 = **24**
- Agent-Workflow optimized: 39/45 × 30 = **26**

The optimized arm's advantage comes from the effort-floor edge case. Both arms still fail ranked-schema and export-ordering/rank checks.

### 2. End-to-end data integration — 20 points

| Check | Points | Direct | Optimized | Evidence |
| --- | ---: | ---: | ---: | --- |
| Python/server path loads supplied fixture | 5 | 5 | 5 | Both pass `hidden.load` and the public server contract |
| Browser renders expected six backlog items | 10 | 0 | 10 | Visual assessment: direct `item_count=0`; optimized `item_count=6` |
| Populated browser state demonstrates supplied data reached the product UI | 5 | 0 | 5 | Direct never populates the list; optimized renders the supplied backlog |
| **Subtotal** | **20** | **5** | **20** | |

Important distinction: the direct implementation **does load the required JSON in its Python/server path**. Its product failure is the browser integration/render path, not absence of `load_backlog()`.

### 3. Required interactive product behavior — 20 points

| Check | Points | Direct | Optimized | Evidence |
| --- | ---: | ---: | ---: | --- |
| Search/filter/sort works visibly | 6 | 0 | 0 | Frozen visual check fails for both |
| Keyboard item-detail interaction | 4 | 0 | 0 | Frozen visual check fails for both |
| Export current ordering | 6 | 0 | 3 | Direct export remains disabled; optimized downloads six rows but fails the complete rank/schema contract |
| Useful empty + invalid-data states | 4 | 0 | 2 | Direct fails both; optimized demonstrates invalid state but fails the empty-state check |
| **Subtotal** | **20** | **0** | **5** | |

Partial credit is explicit in this supplementary rubric. It is not retroactively applied to the official binary-per-check score.

### 4. Presentation and accessibility — 15 points

| Check | Points | Direct | Optimized | Evidence |
| --- | ---: | ---: | ---: | --- |
| Persistent labels and landmark | 4 | 0 | 4 | Direct required labels missing/mismatched; optimized passes |
| Visible keyboard focus | 3 | 3 | 3 | Both pass |
| Responsive/no horizontal overflow | 4 | 4 | 4 | Both pass all three frozen viewports |
| Populated-data presentation is actually observable | 3 | 0 | 3 | Direct renders zero items; optimized renders six |
| Runtime is clean of captured browser errors | 1 | 0 | 0 | Both have captured console/page errors; direct errors are fatal to rendering |
| **Subtotal** | **15** | **7** | **14** | |

This is the category that captures the user's central concern: the direct implementation's screenshots can demonstrate the shell's responsiveness and focus styling, but they **cannot demonstrate how the required ranked data presentation looks**, because no backlog items render.

### 5. Robustness and failure handling — 5 points

Scaled from the frozen robustness result:

- Structured direct: 10/10 × 5 = **5**
- Agent-Workflow optimized: 10/10 × 5 = **5**

### 6. Engineering completeness and traceability — 10 points

Scaled from frozen scope/completeness plus engineering quality (20 possible):

- Structured direct: (10 + 6)/20 × 10 = **8**
- Agent-Workflow optimized: (10 + 8)/20 × 10 = **9**

## Interpretation

The secondary score is:

- Structured direct: **49 / 100**
- Agent-Workflow optimized: **79 / 100**
- Difference: **+30 points**

This wider gap is not caused by inventing a new failure. It is caused by changing the measurement question.

The official score asks predominantly: **How much of the Python/library contract is correct?**

The supplementary score asks: **How complete and usable is the delivered data-driven web application end to end?**

Both are useful. They should be shown together, clearly labeled, rather than replacing one with the other.

## Portfolio-safe presentation

Recommended wording:

> The frozen benchmark scorer rated the two implementations 79.5 and 86.0 because 70% of that rubric measures Python/library correctness and only 10% measures the live UI. A separate post-hoc end-to-end product rubric, applied only to evidence already captured during BM4, scores the same outputs 49 and 79. The wider gap is driven primarily by browser integration: the direct implementation's server can load the supplied fixture, but its browser application throws JavaScript errors and renders zero backlog items, so its populated presentation cannot be meaningfully evaluated. The optimized implementation renders all six supplied items, although it still has interaction and export defects.

Always label **49/79** as the supplementary post-hoc product score and **79.5/86.0** as the official frozen machine score.

## Limitations

- This supplementary rubric was defined after observing the frozen BM4 evidence, so it is unsuitable as a pre-registered treatment-effect measure.
- It must not be used to rewrite the official BM4 score.
- It is intended as a transparent product-completeness lens for portfolio explanation and future benchmark-design improvement.
- A future benchmark revision should define this weighting before execution and should include an explicit end-to-end render/data-integration check in the frozen scoring contract.
