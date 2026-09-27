# Comparative Decision Evidence

This subtree contains public evidence from bounded semantic-decision studies. It is separate from the BM3–BM6 lifecycle benchmark series.

## Routing semantic v1

`routing-semantic-v1` is now complete and has passed the P3 public-evidence verification boundary.

- study version: `1.1.0`;
- dataset: `routing-semantic-corpus-v1.0.0`;
- frozen cases: **120**;
- observations: **360**;
- provider requests: **120**;
- exclusions: **0**;
- oracle: `routing-semantic-oracle-v1.0.0`;
- inference completed without oracle access;
- sanitized public evidence verification: **pass**.

The study evaluates deterministic routing control against bounded TypeSafe/Jev semantic evidence on task class, interaction required, and semantic risk.

Read [the published result](routing-semantic-v1/results/README.md) for the seam-level findings, calibration/efficiency evidence, interpretation boundary, and publication-integrity record.

The result is intentionally not summarized as a single winner. In this frozen cohort the semantic candidate had higher accuracy on task class and interaction-required classification, while semantic-risk mean absolute error was approximately unchanged.
