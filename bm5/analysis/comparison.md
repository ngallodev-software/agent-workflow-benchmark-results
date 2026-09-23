# BM5 comparison analysis

BM5 is the post-optimization development study comparing structured direct execution with the steering-first Agent-Workflow treatment.

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

## Amplification telemetry

Per-arm timing.json files preserve available model-turn, tool-call, command-execution, launch-prompt, and injected-context diagnostics.

## Visual evidence

Per-arm visual directories contain the sanitized assessment plus desktop, tablet, and mobile screenshots. Application failures are scored as solution failures rather than benchmark harness failures.

## Interpretation boundary

This is a single paired development run. Treat the measurements as descriptive evidence for the optimization loop, not as a generalized winner claim.
