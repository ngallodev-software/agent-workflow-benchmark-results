# Comparative Decision Study Report

- **Study:** routing-semantic-v1 / 1.1.0
- **Oracle:** routing-semantic-oracle-v1.0.0
- **Study sample eligible:** yes
- **Provider requests:** 120

## Per-seam results

| Seam | n | Candidate metric | Control metric | Calibration |
| --- | ---: | --- | --- | --- |
| routing.interaction-required/v1 | 120 | accuracy=0.917 | accuracy=0.717 | eligible |
| routing.semantic-risk/v1 | 120 | MAE=0.290 | MAE=0.292 | eligible; normalized 1/120, max mass Δ=0.01 |
| routing.task-class/v1 | 120 | accuracy=0.817 | accuracy=0.525 | eligible; normalized 1/120, max mass Δ=0.01 |

## Interpretation boundary

Agreement is not correctness; correctness in this report comes only from the separately frozen oracle. Provider latency/token evidence is counted once per batched request rather than once per decision seam.

For Choice/Score calibration, finite nonnegative provider probability masses are normalized to unit sum only in the derived calibration calculation when needed; persisted raw evidence is unchanged and the per-seam table reports normalization use.

A non-eligible development sample is useful for instrumentation validation but is not a generalized effectiveness claim.
