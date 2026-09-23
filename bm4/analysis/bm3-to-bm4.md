# BM3 → BM4 optimization analysis

## Scope and interpretation

BM3 and BM4 use the same Priority Picker v2 task, fixture digest, task-prompt digest, structured-direct control design, and paired treatment structure. BM3 used `gpt-5.6-luna`; BM4 used `gpt-6-luna` at high reasoning effort. Therefore, absolute BM3-to-BM4 time and token values are not a same-model comparison.

The useful cross-study signal is the **within-study candidate premium relative to that study's own structured-direct control**. Even that normalized contrast should be treated as descriptive rather than a clean causal estimate because the model changed.

BM4 is a single paired development run (`n=1`). Both BM4 arms are machine-score eligible, but human visual review is incomplete, the sandbox is not publication-verified, and the visual runtime is development-verified rather than publication-verified. No generalized winner claim is supported.

## BM4 within-study result

| Metric | Structured direct | Agent-Workflow optimized | Candidate delta | Candidate premium |
| --- | ---: | ---: | ---: | ---: |
| Machine score | 79.5 | 86.0 | +6.5 | +8.2% |
| Task wall time | 754.186 s | 1,182.853 s | +428.667 s | +56.8% |
| Executor active | 754.074 s | 1,128.800 s | +374.727 s | +49.7% |
| Measured host overhead | 0.112 s | 54.053 s | +53.941 s | — |
| Provider tokens | 1,678,393 | 4,309,050 | +2,630,657 | +156.7% |
| Input tokens | 1,642,042 | 4,258,210 | +2,616,168 | +159.3% |
| Cached input tokens | 1,403,392 | 3,998,208 | +2,594,816 | +184.9% |
| Uncached input tokens | 238,650 | 260,002 | +21,352 | +8.9% |
| Output tokens | 36,351 | 50,840 | +14,489 | +39.9% |
| Reasoning output tokens | 12,442 | 20,723 | +8,281 | +66.6% |

The optimized Agent-Workflow arm preserved a higher frozen machine score while both arms satisfied required machine-score guardrails. The +6.5-point difference came from +3 hidden-functional points, +1.5 accessibility/UI points, and +2 engineering-quality points.

The machine score is not a human product-quality rating. Both implementations retained UI defects. The optimized arm earned 4.0/10 accessibility/UI points versus 2.5/10 for direct execution.

## Normalized BM3 → BM4 change

| Within-study candidate premium | BM3 | BM4 | Descriptive change |
| --- | ---: | ---: | ---: |
| Task wall time | +171.1% | +56.8% | -114.3 pp |
| Executor active time | +167.8% | +49.7% | -118.1 pp |
| Provider tokens | +243.4% | +156.7% | -86.6 pp |
| Cached input | +280.9% | +184.9% | -96.0 pp |
| Uncached input | +71.2% | +8.9% | -62.3 pp |
| Output tokens | +85.5% | +39.9% | -45.7 pp |
| Reasoning output | +243.3% | +66.6% | -176.8 pp |
| Machine-score delta | +4.0 pts | +6.5 pts | +2.5 pts |

These normalized contrasts are the strongest evidence that the BM4 optimization direction was productive. They do **not** establish that OPT-001–007 alone caused the cross-study change because the underlying model changed.

The most notable input result is the uncached-input premium: BM4 candidate uncached input was only 8.9% above its control, compared with 71.2% in BM3. At the same time, BM4 still carried a 184.9% cached-input premium. The remaining token amplification is therefore dominated by cached context associated with the execution/tool loop rather than a large amount of new uncached instruction text.

## Phase behavior

| Phase | BM3 direct | BM3 workflow | BM3 premium | BM4 direct | BM4 optimized | BM4 premium |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Analyze / plan | 72.571 s | 272.984 s | +276.2% | 71.334 s | 139.560 s | +95.6% |
| Implement | 278.492 s | 903.977 s | +224.6% | 548.878 s | 631.960 s | +15.1% |
| Verify / repair | 195.695 s | 305.301 s | +56.0% | 133.974 s | 411.333 s | +207.0% |

The implementation phase shows the clearest improvement in the normalized contrast: its workflow premium fell from +224.6% in BM3 to +15.1% in BM4.

Verification is now the dominant regression. The optimized candidate spent 411.333 seconds in verify/repair versus 133.974 seconds for direct execution, a +277.359-second / +207.0% premium. Further optimization should target verification/review loops before additional prompt-size micro-optimization.

## Amplification telemetry

BM4 added direct instrumentation that BM3 did not have:

| Metric | Structured direct | Agent-Workflow optimized | Delta |
| --- | ---: | ---: | ---: |
| Model turns | 3 | 3 | 0 |
| Tool calls | 42 | 77 | +35 |
| Command executions | 42 | 77 | +35 |
| Launch-prompt bytes | 14,004 | 19,138 | +5,134 |
| Injected executor-context bytes | 0 | 5,107 | +5,107 |
| Estimated injected executor-context tokens | 0 | 1,277 | +1,277 |

The workflow treatment did not add model turns beyond the three benchmark phases, but it caused 35 additional tool/command interactions. That is a more plausible remaining amplification target than the compact executor-context projection itself: the measured injected projection was only 5,107 bytes / about 1,277 diagnostic tokens across the run.

Measured host overhead accounts for about 12.6% of the BM4 wall-time delta (53.941 of 428.667 seconds). Executor-active time accounts for the large majority of the remaining delta. This is consistent with BM3's conclusion that model/tool-path behavior matters more than ordinary Python lifecycle bookkeeping, although host overhead is now a larger share than BM3's roughly 2%.

## Visual and benchmark-integrity result

BM4 repaired the missing-visual-evidence problem that invalidated BM3. Both arms now pass the required visual-capture guardrail with a development-verified runtime and are machine-score eligible.

During evidence collection, the original visual evaluator was found to incorrectly convert solution/UI defects into benchmark harness failures and to require an undocumented hard-coded `title` sort option. The evaluator correction was applied only to visual capture after model execution. The public correction receipt records `model_execution_modified: false` and both evaluator hashes.

The corrected visual evidence shows real application deficiencies rather than hiding them:

- structured direct rendered zero priority items because of JavaScript/application failures and earned 2.5/10 accessibility/UI points;
- Agent-Workflow optimized rendered six items and earned 4.0/10 accessibility/UI points, but still failed several interaction checks.

## Source provenance

BM4 captured exact installed source revisions for:

- Agent-Workflow: `63627e6ec73fa62c18da64ffc38c5189cced6458`;
- agent-workflow-benchmark: `00553a491d68a23d05ea1a316852be04c44c3912`;
- comparative-eval: `6cd93bdb8c61eda795f6a11640aa1f652a640a9d`;
- spec-contracts: `0fb24cc848e9c3a87652caceb2f1c9d62a499b09`.

TypeSafe SDK 0.6.0 was versioned but its source revision was unavailable in the captured environment evidence.

## Next optimization target

BM4 supports continuing the optimization program, but it changes the priority order:

1. attack verify/repair amplification and repeated tool loops;
2. retain the compact context projection and host-owned deterministic gates;
3. instrument verification-cache hit/miss and repeated command equivalence at phase granularity;
4. preserve the new visual/evidence completion gates;
5. add publication-grade isolation/runtime provenance only when making publication-grade claims.

The current evidence supports saying that Agent-Workflow's normalized overhead was substantially lower in BM4 while retaining a higher machine score. It does not support claiming that Agent-Workflow is faster than direct execution, that the optimization effect is model-independent, or that BM4 establishes a generalized winner.
