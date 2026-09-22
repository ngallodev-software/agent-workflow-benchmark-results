# Agent-Workflow Benchmark Results

Public, reproducible benchmark results for [Agent-Workflow](https://github.com/ngallodev-software/agent-workflow).

This repository stores **results and finished software**, not the benchmark harness itself. The harness lives in [agent-workflow-benchmark](https://github.com/ngallodev-software/agent-workflow-benchmark).

## Purpose

The benchmark program measures whether Agent-Workflow's lifecycle, orchestration, evidence, review, and recovery mechanisms justify their runtime and token cost. Each published benchmark preserves enough public evidence to inspect the treatment design, finished software, machine scoring, timing, token usage, and limitations.

The intended engineering loop is:

```text
instrument -> benchmark -> diagnose -> optimize -> re-benchmark
```

## Published / planned studies

| Study | Comparison | Status | Purpose |
| --- | --- | --- | --- |
| Round 2 | `raw-direct/v1` vs `agent-workflow-full/v1` | Historical development smoke | Establish initial wall-time/token overhead |
| BM3 | `structured-direct/v1` vs `agent-workflow-full/v1` | Running / pending publication | Isolate lifecycle/orchestration overhead from structured prompt discipline |
| BM4 | structured-direct vs optimized Agent-Workflow | Planned | Measure the effect of targeted waste reduction discovered from BM3 |

## Repository layout

```text
historical/round2/    sanitized historical baseline
bm3/                  BM3 task, outputs, metrics, analysis
bm4/                  optimization ledger and future BM4 results
schema/               public result metadata schema
```

For completed studies, both treatment outputs are stored as ordinary source trees so readers can inspect the actual software produced rather than relying only on reported metrics.

See [METHODOLOGY.md](METHODOLOGY.md) and [EVIDENCE_POLICY.md](EVIDENCE_POLICY.md).

## Claim discipline

Development runs are descriptive. A single paired run does not establish a generalized winner or treatment effect. Published summaries must identify sample size, treatment identity, environment, scoring eligibility, and known limitations.
