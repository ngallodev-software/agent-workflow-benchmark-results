# BM4 TypeSafe request and response review

## Scope

This review examines the original 56-question Score request, two controlled v2 variants, one candidate-order reversal, and a focused Noul batch against four deterministic-review concerns. TypeSafe is supplemental evidence. The deterministic code review remains the primary report; its score and findings are not computed from TypeSafe probabilities.

## What worked

- The original request used one `system_one` call for seven matched file pairs and 56 independent Score judgments. Those questions shared the same requirements and source state, so batching them avoided repeating the large context.
- The v2 rubric states the file role, asks for independent evaluation against the requirements, discourages complexity rewards, and scopes responsibility to the file. That is a useful improvement over generic anchors.
- The Noul follow-up asked four narrow yes/no questions against exact file excerpts. This tests a second TypeSafe primitive against specific deterministic findings instead of asking it for another general code-quality score.
- The receipts preserve request hashes, source hashes, score distributions, confidence, token usage, and the deterministic review hash. SDK DEBUG logs captured full HTTP bodies in a private file.

## What the experiments found

| Variant | Context | Candidate presentation | Requests | Input / output tokens | Structured Direct average | Optimized average |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| v1 generic rubric | Full tree | Balanced by file | 1 | 29,637 / 1,166 | 64.05% | 56.79% |
| v2 role-anchored rubric | Full tree | Balanced by file | 1 | 32,511 / 1,166 | 65.77% | 58.25% |
| v2 role-anchored rubric | One matched file pair per request | Balanced by file | 7 | 38,295 / 1,190 | 63.25% | 58.80% |
| v2 role-anchored rubric | One matched file pair per request | Reversed for every pair | 7 | 38,372 / 1,190 | 55.67% | 59.72% |

Changing the rubric from v1 to v2 shifted file scores by a mean absolute 7.80 percentage points. Switching v2 from full-tree to matched-file context shifted scores by 6.59 points on average, with a 13.91 point maximum. Reversing the two candidates in matched-file requests shifted scores by 7.32 points on average, with a 22.86 point maximum. The aggregate ranking also reversed: v2 matched-file balanced favored Structured Direct by 4.45 points, while reversed order favored Optimized by 4.05 points.

These single-run comparisons show sensitivity to prompt and request context. The reversed run changes candidate placement and also uses new model responses, so it is evidence of instability, not a precise causal estimate of position bias. No TypeSafe aggregate should be presented as a reliable winner ranking from these runs.

The Noul batch returned yes probabilities of 0.51 for the withdrawn control status claim, 0.31 for the candidate's missing direct range validation, 0.92 for the candidate sort-tie concern, and 0.85 for the server error-mapping concern. The first two source checks do not support using Noul as a truth oracle: inspection shows the status tuple compares by equality without hashing, while `calculate_priority` contains no 1–5 bounds check. The latter two probabilities corroborate the cited source, but still do not prove severity. Noul returns probabilities without a rationale, so a reviewer must inspect the cited code.

One v2 full-tree response had a TypeSafe scalar score of 3.44 while its probability-weighted expectation was 3.40. The receipt preserves both values and flags the discrepancy. The captured response was reused from the protected SDK log; no duplicate API request was made to recover it.

## Recommended request pattern

1. Keep deterministic review and scoring first. Pass its saved Markdown into the benchmark command; the combined report preserves it as the first section.
2. Use one batched full-tree Score request for the broad advisory pass. Include the task, matched source files, explicit roles, a shared behavior-based rubric, and instructions not to claim tests were run.
3. Use matched-file requests selectively when a finding depends on one file pair. Avoid repeating the full task text when a concise requirement reference is sufficient; the seven matched-file requests used about 18% more input tokens than the one-call full-tree variant.
4. Use Noul for narrowly stated concerns with exact source excerpts and line references. Preserve probabilities and disagreement; do not use a low probability to delete a deterministic finding.
5. If a score ranking matters, check order and paraphrase sensitivity across multiple runs and compare against independent adjudicated reviews. These experiments are not enough to calibrate a production threshold.

## Receipts and raw logs

- `code-quality-review-typesafe.json` — original Score receipt with the deterministic-review hash and TypeSafe finding-check reference.
- `code-quality-review-typesafe-v2-full-tree.json` — role-anchored full-tree receipt; response was replayed from the logged API response after local validation exposed the rounded-value discrepancy.
- `code-quality-review-typesafe-v2-matched-file.json` and `code-quality-review-typesafe-v2-matched-file-reversed.json` — per-file context and order-sensitivity receipts.
- `typesafe-deterministic-finding-checks.json` — Noul request and response receipt.
- `typesafe-sdk-debug.log` and `typesafe-sdk-debug-followup.log` — private raw HTTP logs containing BM4 source and complete bodies; do not publish them.
