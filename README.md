<p align="center">
  <a href="https://ngallodev-software.uk/" title="Nate G. / ngallodev-software portfolio">
    <img src="https://ngallodev-software.uk/icon-husky-r1-192.png" width="88" alt="Nate G. portfolio husky mark">
  </a>
</p>

<h1 align="center">Agent-Workflow Benchmark Results</h1>

<p align="center"><strong>Public, sanitized evidence and finished software from Agent-Workflow benchmark and semantic-decision studies.</strong></p>

<p align="center">
  <a href="https://ngallodev-software.uk/projects/agent-workflow">Agent-Workflow case study</a> ·
  <a href="https://jevhunt.com/projects/ngallodev-software/agent-workflow-benchmark-results/">JevHunt listing</a> ·
  <a href="https://github.com/ngallodev-software/agent-workflow-benchmark">Benchmark harness</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/evidence-public%20and%20sanitized-blue" alt="">
  <img src="https://img.shields.io/badge/research-inspectable%20artifacts-2ea44f" alt="">
  <img src="https://img.shields.io/badge/license-Apache--2.0-green" alt="">
</p>

## Summary

> **Evidence & chronology:** this repository is part of the wider Agent-Workflow engineering ecosystem. A private `agent-workflow-lab-notebook` preserves dated decisions, failures, corrections, and evidence lineage; public README and portfolio claims are curated from public artifacts and reviewed notebook history. JevHunt is an independent discovery/indexing surface, not an endorsement or independent validation.

- **What it is:** the public evidence repository for completed Agent-Workflow benchmark studies and the software each arm produced.
- **What to look at:** paired scores, wall time, provider-token usage, treatment identity, eligibility, finished outputs, and study-specific limitations.
- **How to read it:** these are inspectable development observations, not a leaderboard or generalized causal result.
- **Current signal:** BM5 used less wall time and fewer provider tokens in its single eligible pair while also receiving a lower machine score, making the tradeoff visible rather than hiding it.

Public benchmark evidence and finished software for
[Agent-Workflow](https://github.com/ngallodev-software/agent-workflow).

This repository stores **results and finished software**, not the benchmark
harness itself. The harness and scoring implementation live in
[agent-workflow-benchmark](https://github.com/ngallodev-software/agent-workflow-benchmark).

Read these results as inspectable development evidence, not as a leaderboard.
The repository publishes treatment identity, sample size, eligibility, scoring
evidence, timing/token measurements, finished outputs, and known limitations so
individual claims can be checked against the underlying artifacts.

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
| BM3 | `structured-direct/v1` vs `agent-workflow-full/v1` | Execution complete; visual/human review pending | Isolate lifecycle/orchestration overhead from structured prompt discipline |
| BM4 | `structured-direct/v1` vs `agent-workflow-bm4/v1` | One eligible pair; descriptive development result | Measure early context/execution optimization effects |
| BM5 | `structured-direct/v1` vs `agent-workflow-bm5/v1` | One eligible pair; awaiting human review | Measure steering-first lifecycle and later execution/context optimizations |
| Routing semantic v1 | deterministic routing control vs bounded TypeSafe/Jev evidence | **Complete; 120-case P3-verified public result** | Measure correctness, calibration, reliability, and request overhead for the three live routing seams |

## Current paired measurements

These are single-pair development observations, not generalized effects. BM3's machine score delta is descriptive only because visual-capture evidence is missing; BM5 has zero human-complete pairs and awaits review. Cost evidence is unavailable for BM5.

| Study | Machine score delta | Wall-time delta | Provider-token delta | Eligibility / qualification |
| --- | ---: | ---: | ---: | --- |
| BM3 | +4.0 | +935.505 s | +2,345,986 | 0 eligible pairs (missing required visual evidence); TypeSafe qualification 3/3 successful |
| BM4 | +6.5 | +428.667 s | +2,630,657 | 1 eligible pair; TypeSafe qualification 3/3 route matches |
| BM5 | -2.5 (82.5 vs 80.0) | -185.003 s | -235,308 | 1 eligible pair, 0 human-complete; awaiting human review; TypeSafe qualification 3/3 route matches |

BM5's supplementary product score was 79.5 direct vs 77.5 Agent-Workflow (-2.0). The paired Agent-Workflow arm used 185.003 fewer wall-clock seconds and 235,308 fewer provider tokens, while scoring 2.5 fewer machine points. Time savings were concentrated in implementation (456.8 s vs 772.5 s); analyze-plan and verify-repair were slower. These results suggest a possible efficiency/quality tradeoff worth repeating, not a winner or a causal estimate. See each study README for its full metric table and evidence limits.

## How Jev/TypeSafe appears in these studies

Agent-Workflow uses the TypeSafe SDK `system_one` interface with bounded `Choice`, `Noul`, and `Score` questions. The benchmark runners make one pre-treatment routing-qualification call for each of the three phase contexts. They publish sanitized summaries and keep raw request/response audits private. Qualification is outside both paired arms, so none of the reported score, timing, or token deltas measures the effect or cost of TypeSafe routing.

```mermaid
flowchart LR
    A[Three phase contexts] --> B[TypeSafe route qualification]
    B --> C[Sanitized diagnostic summary]
    B -. excluded from treatment .-> D[Structured-direct arm]
    B -. excluded from treatment .-> E[Agent-Workflow arm]
    D --> F[Machine score, time, usage]
    E --> F
    G[Optional BM4 advisory source review] --> H[Supplementary review only]
    F --> I[Result plus eligibility and human-review gates]
    H --> I
```

The qualification evidence records three successes for each study: BM3 had one task-class disagreement under shadow disposition and semantic-risk uncertainty fallback in all three phases; BM4 and BM5 matched deterministic route recommendations in all three phases. BM4 also contains separate advisory TypeSafe source-review experiments; these do not affect its benchmark score or eligibility. The completed routing-semantic-v1 decision study shows higher TypeSafe/Jev candidate accuracy on task-class and interaction-required routing decisions in its frozen 120-case corpus, while semantic-risk ordinal error is approximately unchanged. This bounded decision evidence does not establish downstream product-quality improvement or an execution-cost advantage.

Official background: [Jev/System One announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [System One](https://docs.typesafe.ai/concepts/system-one.md), [state](https://docs.typesafe.ai/concepts/state.md), [Choice](https://docs.typesafe.ai/primitives/choice.md), [Noul](https://docs.typesafe.ai/primitives/noul.md), [Score](https://docs.typesafe.ai/primitives/score.md), and [Python SDK](https://docs.typesafe.ai/sdk/python.md).

## Repository layout

```text
historical/round2/    sanitized historical baseline
bm3/                  BM3 task, outputs, metrics, analysis, qualification evidence
bm4/                  BM4 task, outputs, metrics, analysis, qualification evidence
bm5/                  BM5 task, outputs, metrics, analysis, qualification evidence
comparative-eval/      bounded decision-study methodology, status, and future results
schema/               public result metadata schema
```

For completed studies, both treatment outputs are stored as ordinary source trees so readers can inspect the actual software produced rather than relying only on reported metrics.

See [METHODOLOGY.md](METHODOLOGY.md) and [EVIDENCE_POLICY.md](EVIDENCE_POLICY.md).

## Claim discipline

Development runs are descriptive. A single paired run does not establish a generalized winner or treatment effect. Published summaries must identify sample size, treatment identity, environment, scoring eligibility, and known limitations.


## Comparative decision-study program

A separate public-evidence lane now exists under [comparative-eval/](comparative-eval/), backed by the merged Agent-Workflow 0.11.10 / benchmark 0.4.0 / comparative-eval 0.2.0 study stack. It is intentionally distinct from BM3–BM5: those studies evaluate workflow/lifecycle treatments, while routing-semantic-v1 evaluates bounded semantic decisions against independently frozen labels.

The routing-semantic-v1 subtree now contains the completed, P3-verified public result. See [the published result](comparative-eval/routing-semantic-v1/results/README.md), [implementation/publication status](comparative-eval/routing-semantic-v1/IMPLEMENTATION_STATUS.md), and [publication integrity record](comparative-eval/routing-semantic-v1/results/PUBLICATION-INTEGRITY.md).

In the frozen 120-case cohort, candidate accuracy was 91.67% vs 71.67% for interaction-required and 81.67% vs 52.50% for task class. Semantic-risk MAE was 0.28975 vs 0.29167, with the paired interval spanning zero. These are seam-specific study results, not a general leaderboard or downstream causal claim.
