# BM3 task-source provenance

BM3 recorded the task prompt digest:

`aeb436c39c62b4767d81938d547d3ae3ae71b0c2f65442d13f76ac1948b94b7d`

The last public `agent-workflow-benchmark` commit before the BM3 run began was:

`76f6005845a17dc9d36da1c67cede4a5a9e3d5cb` (2026-09-22T15:54:46Z)

Reconstructing the canonical task plus all three phase prompt files from that revision produces the exact BM3 task prompt digest above. Those four files are therefore cryptographically matched to the task inputs recorded by the BM3 run.

The workflow profile, scoring contract, visual rubric, and visual runtime lock in this directory are copied from the same pre-run benchmark revision so the published task is self-contained. BM3 did not record the installed benchmark package's repository commit SHA, so these supporting files are identified as same-revision source assets rather than independently sealed installed-source provenance.
