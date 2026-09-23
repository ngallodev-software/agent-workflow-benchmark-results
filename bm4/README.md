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
