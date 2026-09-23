# BM5 treatment definition

BM5 compares the same structured task, phase prompts, fixture, model, reasoning effort, and paired schedule under two execution treatments.

- Control: structured-direct/v1 via direct-executor.
- Candidate: agent-workflow-bm5/v1 via agent-workflow.

The candidate adds the Agent-Workflow lifecycle plus the optimizations declared in the frozen benchmark specification: compact executor-context projection (OPT-001/004/007), host-owned deterministic gates (OPT-005), a single `agent finish` closeout transaction (OPT-010/011), host-derived acceptance criteria (OPT-012), steering-first exceptional worker protocol (OPT-013), per-command/cache amplification telemetry (OPT-014), and conditional verify/repair model invocation (OPT-015). This n=1 development result is descriptive rather than a generalized treatment-effect claim.
