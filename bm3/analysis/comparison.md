# BM3 comparison analysis

## Summary

The Agent-Workflow arm produced a modestly higher observed machine score (79 vs 75), while using substantially more model time and tokens. Because required visual evidence is absent, both observed scores are invalid for eligible composite/winner calculations; they are retained as descriptive machine-scoring evidence.

The +4 score difference comes from two machine-scored areas: the Agent-Workflow output received full robustness credit where the control lost 2 points for malformed-JSON error handling, and full scope/completeness credit where the control lost 2 points for README documentation. Both arms shared the same hidden-functional failures around the effort-floor contract, ranked-record schema, deterministic export/rank output, and formula documentation.

## Efficiency

| Metric | Structured direct | Agent-Workflow full | Delta | Relative delta |
| --- | ---: | ---: | ---: | ---: |
| Task wall | 546.758 s | 1482.263 s | +935.505 s | +171.1% |
| Executor active | 546.360 s | 1462.947 s | +916.587 s | +167.8% |
| Measured host overhead | 0.398 s | 19.316 s | +18.917 s | — |
| Provider tokens | 963,980 | 3,309,966 | +2,345,986 | +243.4% |
| Cached input | 789,504 | 3,007,488 | +2,217,984 | +280.9% |
| Uncached input | 148,085 | 253,514 | +105,429 | +71.2% |
| Output | 26,391 | 48,964 | +22,573 | +85.5% |
| Reasoning output | 4,535 | 15,569 | +11,034 | +243.3% |
| Local estimate | $0.0771 | $0.1696 | +$0.0925 | +120.1% |

Measured host overhead explains only ~2.0% of the wall-time delta. The dominant difference is extra executor/model-active work.

Cached-input growth explains ~94.5% of the total-token delta. This is the strongest quantitative signal for BM4: reduce repeated/replayed context and the downstream work that it induces.

## Phase breakdown

| Phase | Direct wall | AW wall | Wall delta | Direct tokens | AW tokens | Token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Analyze/plan | 72.571 s | 272.984 s | +200.413 s | 137,734 | 362,104 | +224,370 |
| Implement | 278.492 s | 903.977 s | +625.485 s | 336,683 | 1,884,413 | +1,547,730 |
| Verify/repair | 195.695 s | 305.301 s | +109.606 s | 489,563 | 1,063,449 | +573,886 |

The implementation phase dominates the regression: it accounts for about two thirds of the wall-time delta and roughly 66% of the token delta.

## Relation to Round 2

Round 2 compared raw direct execution with Agent-Workflow and showed +105.6% wall time and +347.1% total tokens for the workflow arm, but it did not include machine-quality scoring and contained a prompt-discipline confound. BM3 removes that confound. The absolute overhead remains large, and BM3 now shows that most of it is model-active/context-related rather than host lifecycle bookkeeping.

The BM3 result should therefore be used as the baseline for the optimization loop rather than interpreted as a final verdict on Agent-Workflow.
