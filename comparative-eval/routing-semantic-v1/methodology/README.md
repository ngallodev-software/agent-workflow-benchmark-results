# Methodology Boundary

The final publication will include the frozen study specification, oracle protocol, exclusion/statistical policy, exact software/model/question/projector identities, and reproducibility instructions.

The inference runner cannot accept an oracle path. Oracle labels are joined only after semantic inference is complete. Agreement between candidate and control is not treated as correctness.

The preregistered corpus is now frozen at 120 shared cases (`routing-semantic-corpus-v1.0.0`), with all 120 marked oracle-eligible for each decision seam. p90 requires n >= 20, p95 requires n >= 40, and ECE publication requires n >= 100.


Oracle adjudicators receive a blinded authoring view containing request text, declared metadata, the frozen 1.1.0 taxonomy/rubric, and eligibility only. Corpus construction tags, deterministic outputs, Jev outputs, and comparison results are withheld. Two independent adjudicators label every seam; disagreements require a third independent label and recorded resolution under the frozen protocol before the oracle is hashed and frozen.
