# BM4 Optimization Results Addendum

This file records observed BM4 outcomes against the pre-run `optimization-ledger.md`. The original ledger is retained unchanged as the frozen optimization plan.

BM4 used `gpt-6-luna` at high reasoning effort; BM3 used `gpt-5.6-luna`. Cross-study absolute values are therefore not directly comparable. Results below emphasize the within-BM4 treatment/control contrast and use BM3 only as descriptive context.

| ID | Outcome | BM4 evidence | Assessment |
| --- | --- | --- | --- |
| OPT-001 | Compact context projection was exercised. | Candidate injected executor context totaled 5,107 bytes / ~1,277 diagnostic tokens. Candidate launch prompts totaled 19,138 bytes vs 14,004 direct (+5,134 bytes). Cached-input premium nevertheless remained +184.9%. | **Implemented; partial objective.** Prompt/state injection is compact, but cached amplification remains large. |
| OPT-002 | Amplification telemetry is now observable and implementation-phase overhead is much smaller in the normalized contrast. | 3 model turns in both arms; 77 candidate vs 42 direct tool/command calls. Implementation wall premium was +15.1% in BM4 vs +224.6% in BM3. | **Implemented; strong signal.** Remaining loop count is now measurable. |
| OPT-003 | Model/executor-active work remains the primary overhead source. | Candidate-minus-control wall delta: +428.667s. Executor-active delta: +374.727s. Host-overhead delta: +53.941s. Host overhead explains ~12.6% of wall delta. | **Validated priority.** Continue optimizing the model/tool path before host micro-optimization. |
| OPT-004 | Durable evidence was separated from compact executor context. | Only ~1,277 estimated executor-context tokens were injected while full receipts, visual evidence, hashes, and consolidated artifacts remained durable outside the model-facing projection. | **Implemented.** Individual causal contribution is not isolated. |
| OPT-005 | Deterministic host gates did not add extra model turns. | Both arms used 3 model turns. Required paired identity, scope, assistance, visual, provider-usage, and harness-integrity guardrails passed. | **Implemented.** Tool/command count is still high and is the next amplification target. |
| OPT-006 | Verification reuse did not deliver the desired end-to-end verify/repair reduction in this run. | Verify/repair: 411.333s candidate vs 133.974s direct, +277.359s / +207.0%. | **Target not achieved.** Highest-priority follow-up; add phase-level verification-cache hit/miss and repeated-command telemetry. |
| OPT-007 | Lifecycle-specific prompt duplication was bounded. | Candidate launch-prompt total was 19,138 bytes vs 14,004 direct (+36.7%) with no extra model turns. | **Implemented; partial objective.** Overall cached-input premium shows prompt size alone is not the remaining bottleneck. |
| OPT-008 | Exact source provenance improved materially. | Exact source SHAs captured for Agent-Workflow, benchmark, comparative-eval, and spec-contracts. TypeSafe SDK 0.6.0 source SHA remained unavailable. | **Mostly complete.** Close the TypeSafe source-provenance gap before publication-grade claims. |
| OPT-009 | Execution completion and evidence completion are now operationally separated and recoverable. | Model execution remained preserved through visual-runtime/harness recovery; corrected visual evidence made both arms machine-score eligible. Visual correction receipt records `model_execution_modified: false`. | **Completed during BM4 hardening.** Keep this behavior in future runners. |

## Aggregate outcome

Within BM4, Agent-Workflow optimized scored 86.0 versus 79.5 structured direct while carrying a +56.8% wall-time premium and +156.7% provider-token premium.

Relative to each study's own control, BM3's full workflow had +171.1% wall and +243.4% provider-token premiums. The normalized premiums are therefore substantially smaller in BM4, but the model changed between studies and the result is `n=1`; treat this as descriptive evidence, not a causal or generalized treatment-effect estimate.

The most important remaining inefficiency is verify/repair. The most encouraging signal is that implementation-phase wall premium fell to +15.1% while the compact context projection remained small and machine quality did not regress.
