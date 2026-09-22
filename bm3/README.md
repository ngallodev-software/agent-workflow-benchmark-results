# BM3 — Structured Direct vs Agent-Workflow Full

**Status: execution complete; report awaiting human visual review.**

BM3 compares `structured-direct/v1` with `agent-workflow-full/v1` on the same frozen Priority Picker v2 task, model, reasoning setting, starting fixture, structured phase prompts, and paired start. The candidate differs by executing through Agent-Workflow lifecycle, durable state, completion evidence, and sealing.

This is a one-pair development result (`n=1`). It is descriptive, not a generalized treatment-effect claim.

## Result at a glance

| Metric | Structured direct | Agent-Workflow full | Candidate delta |
| --- | ---: | ---: | ---: |
| Machine score | 75 | 79 | +4 |
| Task wall time | 546.758 s | 1482.263 s | +935.505 s (+171.1%) |
| Provider tokens | 963,980 | 3,309,966 | +2,345,986 (+243.4%) |
| Cached input tokens | 789,504 | 3,007,488 | +2,217,984 |
| Uncached input tokens | 148,085 | 253,514 | +105,429 (+71.2%) |
| Output tokens | 26,391 | 48,964 | +22,573 (+85.5%) |
| Local API-equivalent estimate | $0.0771 | $0.1696 | +$0.0925 (+120.1%) |

Both arms are formally **invalid for eligible machine/composite comparison** because required visual-capture evidence is missing. The observed machine scores remain useful descriptive evidence under the benchmark contract. Human visual review is also incomplete, so no composite score or winner is reported.

## What BM3 isolates

The effective benchmark prompt files are identical between arms except for arm/treatment identity. Both receive the same requirements traceability, plan-before-edit, scope control, acceptance-first verification, phase evidence, self-review, and drift-audit instructions. This removes the Round 2 raw-prompt-versus-structured-workflow confound.

## Primary finding for BM4

Only about **18.9 seconds** of the 935.5-second wall-time delta is measured Agent-Workflow host overhead. Approximately **916.6 seconds (~98%)** is additional executor-active time. Likewise, **94.5% of the extra provider tokens are cached-input tokens**.

The optimization target is therefore primarily the context/execution behavior induced by the workflow layer—replayed context, repeated state/instruction material, redundant verification/review work, and excess model-active turns—not Python bookkeeping alone.

See `analysis/comparison.md` and `analysis/optimization-opportunities.md`.
