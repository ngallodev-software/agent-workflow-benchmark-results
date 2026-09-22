# Round 2 — Historical Development Smoke

Round 2 compared `raw-direct/v1` with `agent-workflow-full/v1` in one paired execution-only development smoke.

It is retained because it established the initial performance problem that motivated BM3 and BM4.

## Observed result

Agent-Workflow consumed substantially more wall time and provider tokens in this run.

The largest wall-time penalty occurred during implementation, followed by analyze/plan. Verify/repair overhead was comparatively small.

Because Round 2 was execution-only and `n=1`, it does **not** establish whether the additional orchestration improved quality, reliability, autonomy, recovery, evidence quality, or review effectiveness.

BM3 was designed specifically to address part of that limitation by giving both treatments the same structured workflow discipline and adding machine-quality/timing observability.

See [summary.json](summary.json) for the exact sanitized numbers.
