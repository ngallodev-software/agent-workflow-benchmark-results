# BM3 — Structured Direct vs Agent-Workflow Full

**Status: running; public result pending.**

BM3 compares:

- `structured-direct/v1`
- `agent-workflow-full/v1`

Both arms receive the same structured workflow discipline. Only the candidate executes through Agent-Workflow lifecycle/orchestration/evidence mechanisms.

This study is intended to separate structured-prompt effects from lifecycle/orchestration overhead and to pair time/token evidence with machine-quality scoring.

## Publication layout

When the current run is complete, this directory will contain:

```text
bm3/
├── result.json
├── methodology/
│   ├── environment.json
│   └── treatment-definition.md
├── task/
│   ├── benchmark-spec.json
│   └── starting-fixture/
├── structured-direct/
│   ├── final-project/
│   ├── score.json
│   ├── timing.json
│   └── usage.json
├── agent-workflow/
│   ├── final-project/
│   ├── score.json
│   ├── timing.json
│   └── usage.json
└── analysis/
    ├── comparison.md
    └── optimization-opportunities.md
```

Raw TypeSafe/Jev audit payloads remain private. Public semantic evidence will contain only sanitized aggregate/calibration/provenance fields.

A one-repetition BM3 run remains a development result, not a generalized treatment-effect claim.
