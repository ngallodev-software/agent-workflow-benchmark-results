# BM4 optimization opportunities derived from BM3

BM4 should preserve the BM3 control/task design and change the Agent-Workflow candidate only through evidence-backed waste reduction. Each optimization below should be recorded in an optimization ledger with before/after telemetry.

1. **Reduce replayed cached context.** The candidate added 2.218M cached-input tokens, 94.5% of the total-token delta. Inspect executor prompt/state assembly for material that is resent on every turn or phase but can be represented once, referenced by hash/path, summarized, or omitted after acknowledgement.

2. **Attack implementation-phase amplification first.** The implementation phase grew from 336,683 to 1,884,413 provider tokens and from 278.5s to 904.0s. Instrument turn counts, context size per turn, command/tool-loop count, and repeated instruction/state bytes so BM4 can attribute the reduction rather than only observe it.

3. **Separate durable evidence from model context.** Keep lifecycle receipts, provenance, patches, and deterministic state durable on the host, but do not automatically feed all of that evidence back into the model. Prefer stable identifiers, concise state projections, and deterministic retrieval only when required.

4. **Move deterministic decisions out of the model path.** Use ordinary code for schema validation, lifecycle transitions, policy gates, scope checks, completion predicates, artifact hashing, and evidence sealing. Use TypeSafe/Jev only for genuinely semantic bounded decisions where fuzzy evidence can change a policy outcome; BM3's semantic qualification showed the value of shadow/fallback handling without making semantic routing part of the treatment.

5. **Collapse redundant verification/review loops.** Preserve acceptance-first verification, but avoid asking the model to rediscover already-proven facts. Deterministic test results and unchanged hashes should satisfy corresponding gates directly; model review should focus on unresolved contradictions or semantic defects.

6. **Minimize per-phase instruction duplication.** BM3 proves the structured direct prompt itself can carry the required discipline. Agent-Workflow should inject only lifecycle-specific information that the direct prompt does not already contain.

7. **Instrument source provenance and visual completion.** BM3 captured installed package versions but not exact source-repository commit SHAs, and the execution-only readiness path later produced machine-score invalidation because visual evidence was missing. BM4 should record exact source revisions at run start and make the execution/report state machine explicitly distinguish `execution_complete` from `benchmark_complete`.

## BM4 success measures

Primary efficiency measures should include task wall time, executor-active time, measured host overhead, total/cached/uncached input, output/reasoning tokens, model turn count, and per-phase context bytes/tokens. Quality guardrails should preserve or improve eligible machine score and completed human visual review. A reduction should not be credited if it is achieved by weakening the structured task discipline, evidence durability, recovery semantics, or acceptance criteria.
