# Routing Semantic v1 — Publication Status

**Current state:** P0A–P3 complete; sanitized public evidence verified and published.

## Frozen identities

- study: `routing-semantic-v1`;
- study version: `1.1.0`;
- dataset: `routing-semantic-corpus-v1.0.0`;
- cases: **120**;
- corpus SHA-256: `e4b33df3b3752b32cdb362833765cc8f0c9cc024473071209563d73284011280`;
- oracle: `routing-semantic-oracle-v1.0.0`;
- question set: `routing/v2`;
- projector: `routing-state/v2`.

## Completed evidence pipeline

~~~mermaid
flowchart LR
    A[Frozen 120-case corpus] --> B[P2 inference]
    B --> C[Deterministic control]
    B --> D[One TypeSafe/Jev request per case]
    D --> E[Three per-seam observations]
    F[Separately frozen oracle] --> G[Post-inference join]
    E --> G
    G --> H[Correctness / calibration / disagreement]
    D --> I[Request-level latency / tokens / reliability]
    H --> J[P2 report]
    I --> J
    J --> K[P3 redacted public projection]
    K --> L[Independent publication verification]
~~~

P2 completed with:

- 120 cases;
- 360 observations;
- 120 provider requests;
- 360 oracle outcomes;
- 0 exclusions;
- oracle absent during inference.

P3 independently verified the exact public file boundary, manifest integrity, privacy contracts, public-oracle projection, full-study sample identity, and absence of private A/B/C votes, human-resolution rationale/participant identity, and private reasoning summaries.

## Published result

See [`results/README.md`](results/README.md).

Headline seam-level evidence:

| Seam | Candidate | Control | Paired result |
| --- | ---: | ---: | --- |
| Interaction required | 91.67% accuracy | 71.67% | +20.0 pp; 95% interval +10.83 to +29.17 pp |
| Task class | 81.67% accuracy | 52.50% | +29.17 pp; 95% interval +20.0 to +38.33 pp |
| Semantic risk | MAE 0.28975 | MAE 0.29167 | difference -0.001917; 95% interval -0.101917 to +0.092917 |

The first two seams show higher semantic-candidate accuracy in this frozen cohort. Semantic-risk ordinal error is approximately unchanged at the resolution of this study.

## Claim boundary

This study supports bounded seam-specific claims for the frozen corpus. It does not establish:

- a general winner across all routing behavior;
- downstream causal improvement in software quality;
- a provider-cost advantage;
- validity outside the frozen corpus/runtime without replication.

The v1 oracle remains immutable. A future version will require structured adjudicator justifications and explicit aggregate-session usage provenance.
