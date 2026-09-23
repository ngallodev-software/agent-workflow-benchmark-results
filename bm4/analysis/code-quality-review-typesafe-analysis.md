# BM4 code-review analysis: deterministic review with TypeSafe supplements

## Primary review

The deterministic per-file review remains the primary judgment: Structured Direct averages **87.1%** and Agent-Workflow Optimized **87.7%**, a **+0.6 percentage-point** difference for Optimized. TypeSafe outputs are advisory cross-checks; they do not replace or alter the file scores, findings, benchmark machine scores, or acceptance.

A source-grounded correction was made to the deterministic write-up. The earlier version claimed an unhashable `status` could cause a raw `TypeError`; the control uses a tuple of statuses, so membership does not hash the input. The concern is withdrawn and the deterministic score is unchanged. This correction is recorded in `code-quality-review-gpt6-luna.md`.

## TypeSafe experiments

| Run | Questions | Requests | Input tokens | Output tokens | Structured Direct | Optimized | Mean confidence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v1 generic rubric, full tree | 56 Score | 1 | 29,637 | 1,166 | 64.05% | 56.79% | 0.339 |
| v2 role rubric, full tree | 56 Score | 1 | 32,511 | 1,166 | 65.77% | 58.25% | 0.380 |
| v2 role rubric, matched file | 56 Score | 7 | 38,295 | 1,190 | 63.25% | 58.80% | 0.348 |
| v2 role rubric, matched file, reversed candidates | 56 Score | 7 | 38,372 | 1,190 | 55.67% | 59.72% | 0.377 |
| Deterministic finding cross-checks | 4 Noul | 1 | 1,228 | 83 | n/a | n/a | n/a |
| **Total** | **228 typed judgments** | **17** | **140,043** | **4,795** | — | — | — |

The original TypeSafe request averaged **64.05%** for Structured Direct and **56.79%** for Optimized. That apparent −7.26 point difference is not stable: the v2 matched-file result reduced the gap to −4.45 points, while reversing candidates changed it to +4.05 points. Mean absolute file-score movement was 7.80 points when changing the rubric, 6.59 points when changing full-tree versus matched-file context, and 7.32 points when reversing candidate order. The largest individual movement was 33.7 points between v1 and v2, 13.91 points between context variants, and 22.86 points between candidate-order variants.

The broad full-tree v2 response differed between one scalar score and its probability-weighted expectation by 0.04. The JSON keeps both values and marks the inconsistency; one response was normalized from the already captured DEBUG log rather than re-requested.

## Token cost relative to BM4

The two BM4 runs recorded **5,987,443 combined input and output tokens**. The TypeSafe review and cross-checks used **144,838 tokens**, about **2.42%** of that total. The SDK reports token counts but did not return monetary cost; no dollar estimate is inferred here. The seven-request matched-file batch used about **18% more input tokens** than the one-request full-tree v2 pass because requirements and request overhead were repeated.

## Readout

TypeSafe helped reveal prompt, context, response-consistency, and candidate-order sensitivity. It also challenged a faulty statement in the deterministic draft, but the source itself resolved that issue; the Noul probability for that proposition was 0.51. Another directly verifiable concern, missing range validation in `calculate_priority`, received a yes probability of 0.31. This demonstrates why probabilities must stay advisory. Two other source-grounded concerns received higher support probabilities, but TypeSafe returned no rationale or line citations.

Use the full-tree v2 Score request as an economical broad supplement, with the deterministic report first. Use selective Noul checks for concrete disputed findings and provide exact source excerpts. Keep the TypeSafe percentages out of winner claims unless repeated, order-balanced results are calibrated against independent human reviews.

## Artifacts

- `code-quality-review-typesafe.md` — deterministic review first, followed by the original TypeSafe Score supplement and focused Noul checks.
- `code-quality-review-typesafe-v2-full-tree.md` — role-aware broad pass.
- `code-quality-review-typesafe-v2-matched-file.md` — isolated file-pair context experiment.
- `code-quality-review-typesafe-v2-matched-file-reversed.md` — candidate-order experiment.
- `typesafe-request-response-review.md` — prompt/context analysis and recommendations.
- `typesafe-deterministic-finding-checks.json` — machine-readable Noul receipt.

The SDK DEBUG logs are private because they contain complete request and response bodies, including submitted code.
