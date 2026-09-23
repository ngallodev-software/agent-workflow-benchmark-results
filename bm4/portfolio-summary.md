# BM4 Portfolio Evidence Summary

## Portfolio-safe headline

**Agent-Workflow optimization study (BM4):** on a paired development benchmark using GPT-6 Luna/high, the optimized Agent-Workflow treatment scored **86.0 vs 79.5** for the same structured-direct control task. It remained slower and more token-intensive than direct execution, but its within-run overhead was materially smaller than the normalized overhead observed in the prior BM3 study.

## Numbers safe to publish

| Metric | Structured direct | Agent-Workflow optimized | Candidate difference |
| --- | ---: | ---: | ---: |
| Frozen machine score | 79.5 | 86.0 | +6.5 pts |
| Task wall time | 754.2s | 1,182.9s | +56.8% |
| Provider tokens | 1.678M | 4.309M | +156.7% |
| Uncached input | 238,650 | 260,002 | +8.9% |
| Model turns | 3 | 3 | no increase |
| Tool / command calls | 42 | 77 | +35 |
| Injected Agent-Workflow context | 0 | ~1,277 est. tokens | +~1,277 |

Both arms were machine-score eligible under the development benchmark guardrails. Human visual review remains incomplete, so do not present a composite score or winner.

## Optimization-loop story

BM3 identified that Agent-Workflow's large overhead was mostly executor/model-active rather than Python bookkeeping and that cached-input growth dominated the token delta. That evidence drove OPT-001 through OPT-007: compact context projection, amplification instrumentation, durable-evidence separation, deterministic host gates, verification reuse, and reduced lifecycle prompt duplication.

BM4 shows three useful outcomes:

1. **Implementation-path overhead compressed sharply.** Implementation wall premium was +15.1% in BM4, versus +224.6% in BM3's normalized within-study comparison.
2. **Fresh context amplification became small.** Candidate uncached-input premium was only +8.9%, while the measured executor-context injection was ~1,277 diagnostic tokens across all three phases.
3. **The next bottleneck became visible.** Verify/repair was +207.0% slower than direct execution and the workflow made 77 tool/command calls vs 42 direct. The next optimization round should target verification/review loops and repeated commands.

## What not to claim

Do not claim:

- that BM4 proves Agent-Workflow is faster than direct execution — it was not;
- that BM4 proves a generalized winner — `n=1`, human review is incomplete, and the winner policy is not satisfied;
- that BM3→BM4 absolute time/token changes are directly comparable — BM3 used GPT-5.6 Luna and BM4 used GPT-6 Luna/high;
- that the benchmark is publication-grade — the runtime is development-verified and filesystem/oracle isolation is not publication-verified.

A defensible phrasing is:

> In a paired development benchmark, the optimized workflow preserved a higher frozen machine score while reducing the workflow's normalized wall-time premium from 171% in BM3 to 57% in BM4 and its provider-token premium from 243% to 157%. Because the benchmark model changed between rounds and each round used one pair, I treat this as engineering evidence for the optimization loop rather than a generalized performance claim.

## Evidence links to expose from the portfolio

The portfolio can link directly to:

- `bm4/result.json` — canonical machine-readable BM4 result;
- `bm4/analysis/bm3-to-bm4.md` — full optimization analysis;
- `bm4/optimization-results.md` — OPT-001–009 outcome map;
- `bm4/structured-direct/final-project/` — completed control implementation;
- `bm4/agent-workflow-optimized/final-project/` — completed optimized implementation;
- `bm4/structured-direct/visual/` and `bm4/agent-workflow-optimized/visual/` — visual evidence;
- `bm4/evidence/visual-harness-correction.json` — evidence that post-run visual-harness repair did not modify model execution;
- `bm4/PUBLICATION-MANIFEST.json` — original generated 62-file evidence-package integrity manifest.

The raw TypeSafe API audit and complete evidence archive should remain private. The public TypeSafe qualification summary is sufficient for portfolio evidence.


## Supplementary end-to-end product score

The official frozen BM4 score is intentionally retained as the primary benchmark score: **79.5 structured direct vs 86.0 Agent-Workflow optimized**.

A separate post-hoc product-completeness rubric was added after reviewing how the official 100-point contract distributes weight. The official contract assigns 70 points to Python/library correctness and robustness but only 10 points to the live browser UI. That means the structured-direct implementation can retain a relatively high official score even though its browser application renders zero backlog items.

Using only evidence already captured during BM4, the supplementary rubric scores:

- structured direct: **49 / 100**
- Agent-Workflow optimized: **79 / 100**
- supplementary difference: **+30 points**

The wider difference is primarily end-to-end integration, not a claim that the direct implementation never loads the JSON. Both implementations' Python/server paths load and validate the supplied fixture. The direct failure occurs in the browser integration path: JavaScript errors prevent any priority items from rendering. As a result, the populated data presentation cannot be meaningfully evaluated for that arm.

The supplementary 49/79 score is **not** the official BM4 machine score and must always be labeled post-hoc. It exists to make product completeness legible and to inform a better pre-registered rubric for future benchmark rounds.

See:

- `analysis/official-scoring-matrix.md`
- `analysis/end-to-end-product-rubric.md`
- `analysis/end-to-end-product-score.json`
