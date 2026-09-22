# Benchmark Methodology

## Objective

The benchmark program evaluates Agent-Workflow as an engineering system, not only as a prompting technique.

The primary question is whether durable lifecycle control, orchestration, evidence collection, recovery, and review improve useful software-engineering outcomes enough to justify their additional time and token cost.

## Paired design

Where possible, benchmark runs use paired arms against the same frozen task fixture and requirements.

A result record should preserve:

- benchmark and treatment identifiers;
- exact source revisions;
- model and reasoning configuration;
- executor/runtime identity;
- starting fixture identity;
- final software trees;
- machine scores and eligibility state;
- wall time, executor-active time, and host overhead;
- provider token telemetry;
- repetition count and pairing metadata;
- deterministic test/evidence results;
- sanitized provenance.

## Finished software is evidence

The final project from each treatment is part of the benchmark evidence. Public readers should be able to compare:

- requirements implemented;
- correctness and tests;
- architecture and maintainability;
- unnecessary complexity;
- repair work;
- visible feature quality;
- whether additional orchestration cost corresponds to a materially different result.

Metrics without the produced software are insufficient for the public case study.

## Development vs qualified claims

A one-repetition development run is descriptive and diagnostic. It can identify likely overhead sources and generate hypotheses, but it does not justify a generalized performance claim.

Stronger claims require an appropriately repeated and reviewed cohort with the same treatment definition and controlled environment.

## BM3

BM3 compares:

- `structured-direct/v1`: structured workflow instructions executed directly through Codex;
- `agent-workflow-full/v1`: the same structured workflow discipline executed through Agent-Workflow.

This removes a major Round 2 confound: raw prompting versus structured workflow prompting.

BM3 records granular timing and machine quality so overhead can be separated into coding-model work versus Agent-Workflow host/lifecycle work.

TypeSafe/Jev routing qualification is performed before paired execution and is not part of either treatment. BM3 asserts that paired execution emits no additional semantic-routing calls.

## BM4

BM4 is intended to preserve the BM3 task/control design as closely as practical while replacing the BM3 Agent-Workflow candidate with an optimized implementation.

The optimization phase should be driven by BM3 evidence, especially:

- duplicated context;
- unnecessary repeated prompt/state construction;
- redundant evidence serialization;
- avoidable general-LLM decisions;
- repeated verification/review context;
- excess executor-active work;
- excess host/lifecycle overhead.

BM4 should include an optimization ledger mapping each change to the BM3 observation that motivated it and the metric it is expected to affect.

## Interpretation

The benchmark is designed to answer several questions independently:

1. Did quality change?
2. Did executor-active time change?
3. Did Agent-Workflow host overhead change?
4. Did total, cached, uncached, output, or reasoning tokens change?
5. Did reliability/evidence/recovery behavior change?
6. Did optimization reduce waste without reducing software quality?

No single metric is sufficient by itself.
