# Routing Semantic v1 — Methodology Boundary

The study uses a frozen 120-case public-safe corpus and a separately constructed blinded oracle.

## Separation of inference and ground truth

The inference runner cannot accept an oracle path. All 120 semantic/control cases completed before the frozen oracle was loaded for reporting.

Agreement between candidate and control is not treated as correctness. Correctness is defined only by the separately frozen oracle.

## Oracle construction

The blinded oracle-authoring view withheld:

- corpus construction tags;
- deterministic-control outputs;
- TypeSafe/Jev outputs;
- comparison results.

A and B labeled independently. A/B disagreements went to a separately blinded C pass. Two-of-three majority resolved ordinary disputes; genuine three-way conflicts required recorded human resolution under the frozen rubric.

The final oracle was frozen before P2 inference.

## Statistical/sample policy

All three seams have **n=120** oracle-eligible outcomes in the published study.

The frozen study policy uses:

- deterministic paired bootstrap intervals;
- p90 only when n >= 20;
- p95 only when n >= 40;
- ECE publication only when n >= 100;
- explicit exclusions rather than silent denominator changes;
- request-level accounting that counts one batched provider request once.

## Publication boundary

The private frozen oracle contains richer adjudication provenance than the public evidence needs.

P3 therefore publishes a redacted oracle projection containing final labels and per-seam resolution status/method, while removing private adjudicator identities, individual A/B/C votes, pass provenance, human-resolution rationale/participants, and private reasoning-summary artifacts.

The P3 verification record is published under [`../results/verification.json`](../results/verification.json).

## Known methodological correction

The authoritative v1 adjudication passes preserved labels but no structured per-decision justification. A later private-log audit found contemporaneous provider reasoning summaries, but those summaries were not available to the original human-resolution workflow and were not retrofitted into the frozen oracle.

Future cohorts will use a new versioned structured-rationale contract rather than modifying v1.
