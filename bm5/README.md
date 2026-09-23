# BM5 — Structured Direct vs Agent-Workflow Slimmed

**Status: development benchmark finalized; human visual review may remain pending.**

BM5 measures the same structured Priority Picker task after Agent-Workflow OPT-001 through OPT-015 context/execution optimizations.

## Result at a glance

| Metric | Structured direct | Agent-Workflow slimmed | Candidate delta |
| --- | ---: | ---: | ---: |
| Machine score | 82.5 | 80.0 | -2.5 |
| Supplementary product score | 79.5 | 77.5 | -2.0 |
| Task wall time (s) | 961.135 | 776.132 | -185.003 |
| Executor active (s) | 960.388 | 738.118 | -222.270 |
| Measured host overhead (s) | 0.746 | 38.013 | 37.267 |
| Provider tokens | 2,309,077 | 2,073,769 | -235,308 |
| Input tokens | 2,269,371 | 2,039,740 | -229,631 |
| Cached input tokens | 2,054,912 | 1,820,160 | -234,752 |
| Output tokens | 39,706 | 34,029 | -5,677 |
| Reasoning output tokens | 14,793 | 12,996 | -1,797 |

## Published artifacts

- task/ — canonical task, prompts, official and supplementary scoring contracts, visual contract, runtime lock, and starting fixture;
- structured-direct/ — control final project, score, timing, usage, and visual evidence;
- agent-workflow-slimmed/ — candidate final project, score, timing, usage, and visual evidence;
- analysis/comparison.md — descriptive comparison;
- evidence/ — sanitized TypeSafe summary, benchmark receipts, and visual-harness correction provenance when applicable;
- methodology/ — environment and treatment definition.

Raw TypeSafe audit records and the full evidence archive are intentionally not published. Their hashes are recorded in result.json.
