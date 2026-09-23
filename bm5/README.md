# BM5 — Structured Direct vs Agent-Workflow Slimmed

**Status: development benchmark finalized; human visual review may remain pending.**

BM5 measures the same structured Priority Picker task with the frozen `agent-workflow-bm5/v1` treatment. The public benchmark specification names the candidate optimizations as compact executor-context projection (OPT-001/004/007), host-owned deterministic gates (OPT-005), a single `agent finish` closeout transaction (OPT-010/011), host-derived acceptance criteria (OPT-012), steering-first exceptional worker protocol (OPT-013), per-command/cache amplification telemetry (OPT-014), and conditional verify/repair model invocation (OPT-015). OPT-002/003/006 are not declared as enabled features in this BM5 specification.

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

## TypeSafe/Jev qualification

Before either arm ran, the benchmark made three TypeSafe qualification calls over analyze-plan, implement, and verify-repair context. All three route recommendations matched deterministic control. Semantic routing remained outside both treatments, so these calls do not account for BM5's observed time/token reductions or score regression. The public [qualification summary](evidence/typesafe-qualification-summary.json) records the sanitized results; the raw audit is not published.

BM5's measured pair had 80.0 vs 82.5 machine points (-2.5), 776.132 vs 961.135 seconds (-185.003 s), and 2,073,769 vs 2,309,077 provider tokens (-235,308). It had one eligible pair but no human-complete pair and is awaiting human review. No causal conclusion about TypeSafe is supported. See [Jev/System One](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [System One](https://docs.typesafe.ai/concepts/system-one.md), and the [Agent-Workflow TypeSafe boundary](https://github.com/ngallodev-software/agent-workflow#optional-bounded-semantic-decisions).

Raw TypeSafe audit records and the full evidence archive are intentionally not published. Their hashes are recorded in result.json.
