# BM4 comparison analysis

BM4 is the post-optimization development study comparing structured direct execution with the optimized Agent-Workflow treatment.

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

## Amplification telemetry

Per-arm timing.json files preserve available model-turn, tool-call, command-execution, launch-prompt, and injected-context diagnostics.

## Visual evidence

Per-arm visual directories contain the sanitized assessment plus desktop, tablet, and mobile screenshots. Application failures are scored as solution failures rather than benchmark harness failures.

## Interpretation boundary

This is a single paired development run. Treat the measurements as descriptive evidence for the optimization loop, not as a generalized winner claim.
