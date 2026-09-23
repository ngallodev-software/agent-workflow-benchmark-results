# BM4 — Structured Direct vs Agent-Workflow Optimized

**Status: development benchmark finalized; human visual review may remain pending.**

BM4 measures the same structured Priority Picker task after Agent-Workflow OPT-001 through OPT-007 context/execution optimizations.

## Result at a glance

| Metric | Structured direct | Agent-Workflow optimized | Candidate delta |
| --- | ---: | ---: | ---: |
| Machine score | 79.5 | 86.0 | 6.5 |
| Task wall time (s) | 754.186 | 1,182.853 | 428.667 |
| Executor active (s) | 754.074 | 1,128.800 | 374.727 |
| Measured host overhead (s) | 0.112 | 54.053 | 53.941 |
| Provider tokens | 1,678,393 | 4,309,050 | 2,630,657 |
| Input tokens | 1,642,042 | 4,258,210 | 2,616,168 |
| Cached input tokens | 1,403,392 | 3,998,208 | 2,594,816 |
| Output tokens | 36,351 | 50,840 | 14,489 |
| Reasoning output tokens | 12,442 | 20,723 | 8,281 |

## Published artifacts

- task/ — canonical task, prompts, scoring and visual contracts, runtime lock, and starting fixture;
- structured-direct/ — control final project, score, timing, usage, and visual evidence;
- agent-workflow-optimized/ — candidate final project, score, timing, usage, and visual evidence;
- analysis/comparison.md — descriptive comparison;
- evidence/ — sanitized TypeSafe summary, benchmark receipts, and visual-harness correction provenance when applicable;
- methodology/ — environment and treatment definition.

Raw TypeSafe audit records and the full evidence archive are intentionally not published. Their hashes are recorded in result.json.

## TypeSafe/Jev evidence

The benchmark runner made three pre-treatment qualification calls, one for each phase context. All three Agent-Workflow route recommendations matched deterministic control, and the paired treatments contained no semantic-routing calls. This establishes that the configured route path ran on the phase inputs; it does not show a TypeSafe effect on BM4's task score, time, or provider-token totals.

BM4 also contains separate TypeSafe source-review experiments over the finished projects. The matched-file `benchmark-code-quality/v2` run used Jev `jev-1.13.0` for seven paired source files in seven requests (38,295 input tokens, 1,190 output tokens, 1.601 seconds reported service duration). Its advisory aggregate quality percentages were 63.25 for structured direct and 58.80 for Agent-Workflow optimized. These are semantic review estimates, not benchmark machine scores or human-reviewed findings; they do not affect eligibility or acceptance. Different question sets and review variants are preserved under `analysis/` and should not be pooled.

The sanitized route receipt is [typesafe-qualification-summary.json](evidence/typesafe-qualification-summary.json); the review detail is [the matched-file advisory report](analysis/code-quality-review-typesafe-v2-matched-file.md) with its [structured receipt](analysis/code-quality-review-typesafe-v2-matched-file.json). Raw route audit records are not public. See [Jev/System One](https://typesafe.ai/blog/introducing-system-one-models-and-jev) and the [Agent-Workflow integration](https://github.com/ngallodev-software/agent-workflow#optional-bounded-semantic-decisions).
