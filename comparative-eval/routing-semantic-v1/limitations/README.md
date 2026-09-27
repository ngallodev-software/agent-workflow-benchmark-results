# Routing Semantic v1 — Limitations

The study is complete and publication-eligible, but its claims remain bounded.

## Interpretation limitations

- The corpus contains 120 frozen public-safe routing cases; results do not automatically generalize to arbitrary production requests.
- The study evaluates three routing seams, not downstream software quality or end-to-end agent performance.
- Task-class and interaction-required results show clear candidate accuracy separation in this cohort; semantic-risk MAE does not.
- A single aggregate "winner" would obscure the heterogeneous seam-level result.

## Oracle-provenance limitation

The authoritative A/B/C pass contract retained labels but no structured per-decision adjudicator justification.

A later audit found provider reasoning summaries in retained private Inspect logs. They were supplementary execution evidence and were not exposed to the original human resolver. They were not retrofitted into the frozen oracle.

Future cohorts should require provider-neutral structured justifications and verify their persistence before real adjudication begins.

## Calibration/reporting limitation

One out of 120 probability vectors in each multiclass seam had total mass 0.99 rather than exactly 1.0. Raw evidence was preserved; only the derived calibration copy was normalized. The published report records this explicitly.

## Efficiency limitations

All 120 provider requests succeeded and token/latency evidence is complete at request level.

Provider cost evidence is incomplete, so no cost comparison is published.

## Publication/privacy limitation

The public oracle is a redacted projection of the private frozen oracle. It intentionally omits individual adjudicator votes, identities, human-resolution rationale/participants, and private reasoning summaries.

See [the publication-integrity note](../results/PUBLICATION-INTEGRITY.md).
