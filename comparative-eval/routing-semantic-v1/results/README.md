# Routing Semantic v1 — Published Result

**Study:** `routing-semantic-v1` / 1.1.0  
**Dataset:** `routing-semantic-corpus-v1.0.0`  
**Frozen oracle:** `routing-semantic-oracle-v1.0.0`  
**Status:** eligible full-study evidence; P3 publication verification passed

## What was compared

The study compares Agent-Workflow's deterministic routing control with a bounded TypeSafe/Jev semantic-evidence candidate on three live routing seams:

- task class;
- interaction required;
- semantic risk.

The independent oracle was frozen before comparative inference. The inference runner did not receive the oracle; labels were joined only after all 120 cases completed.

## Full-study shape

| Measure | Value |
| --- | ---: |
| Frozen cases | 120 |
| Decision observations | 360 |
| Provider requests | 120 |
| Oracle outcomes | 360 |
| Exclusions | 0 |
| Oracle-eligible n per seam | 120 |

## Results

| Seam | Candidate | Deterministic control | Paired comparison |
| --- | ---: | ---: | --- |
| Interaction required | **91.67% accuracy** (110/120) | 71.67% (86/120) | +20.0 percentage points; 95% interval +10.83 to +29.17 |
| Task class | **81.67% accuracy** (98/120) | 52.50% (63/120) | +29.17 percentage points; 95% interval +20.0 to +38.33 |
| Semantic risk | MAE 0.28975 | MAE 0.29167 | candidate-control absolute-error difference -0.001917; 95% interval -0.101917 to +0.092917 |

The first two seams show materially higher candidate accuracy in this frozen cohort. The semantic-risk result does not show comparable separation: the observed MAEs are nearly identical and the paired interval spans both directions.

## Change analysis

### Interaction required

- beneficial changes: 30;
- harmful changes: 6;
- both correct: 80;
- both wrong: 4.

### Task class

- beneficial changes: 38;
- harmful changes: 3;
- changed but both wrong: 10;
- both correct: 60;
- both wrong: 19.

## Calibration

- interaction-required Brier: 0.07741;
- interaction-required ECE: 0.14942;
- task-class multiclass Brier: 0.27346;
- task-class log loss: 1.80242;
- semantic-risk multiclass Brier: 0.32484;
- semantic-risk log loss: 0.53531.

One probability vector out of 120 in each multiclass seam had total mass 0.99. The reporting layer preserved the raw evidence and normalized only the derived calibration copy. Maximum mass deviation was 0.01.

## Request-level evidence

- provider requests: 120;
- successful requests: 120;
- input tokens: 91,445;
- output tokens: 10,598;
- provider total tokens: 102,043;
- p50 request duration: 0.1468 s;
- p90: 0.1865 s;
- p95: 0.2206 s.

Provider cost evidence is incomplete and no cost conclusion is published.

## Interpretation boundary

This is a bounded study of three routing decisions, not a general benchmark of Agent-Workflow, Jev, or software-agent quality.

The results support seam-specific claims for this frozen corpus:

- the semantic candidate was more accurate on task-class and interaction-required classification;
- semantic-risk ordinal error was approximately unchanged at the resolution of this study;
- all 120 candidate provider requests succeeded;
- the report contains no evidence sufficient to claim a cost advantage.

The study does not establish downstream causal effects on software quality.

## Publication privacy

P3 publishes a redacted oracle projection rather than the private frozen oracle. It retains final labels and per-seam resolution status/method while removing:

- adjudicator identities;
- individual A/B/C votes;
- pass hashes and timestamps;
- human-resolution rationale;
- participant identities;
- private Inspect reasoning summaries.

See `verification.json` and `PUBLICATION-INTEGRITY.md`.

## Exact evidence bundle

The exact verified P3 tree is stored as base64 parts under `bundle/`.

Reconstruct it with:

~~~bash
cat bundle/parts/part-*.b64 | tr -d '\n' | base64 -d > routing-semantic-v1-p3-public.tar.gz
sha256sum -c bundle/routing-semantic-v1-p3-public.tar.gz.sha256
tar -xzf routing-semantic-v1-p3-public.tar.gz
~~~

The expected archive SHA-256 is:

`b07c3899dfa6c504a919e6eb425f2e561267bc994ee86ce880972ae8b84abad2`

The archive contains the public corpus, public oracle projection, full neutral observation/request/outcome evidence, report, study specification, publication manifest, and SHA manifest.
