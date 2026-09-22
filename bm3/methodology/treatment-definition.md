# BM3 Treatment Definition

## Control

`structured-direct/v1`

The structured benchmark workflow profile is executed directly through Codex CLI without Agent-Workflow lifecycle execution.

## Candidate

`agent-workflow-full/v1`

The same structured benchmark workflow profile is executed through the real Agent-Workflow lifecycle, durable execution, evidence, and review infrastructure.

## Semantic qualification

TypeSafe/Jev routing qualification is performed separately before paired execution through the real Agent-Workflow routing boundary.

It is diagnostic evidence, not a benchmark treatment.

The paired run must report:

```text
treatment_additional_records = 0
```

Any semantic-routing calls during paired execution invalidate the intended treatment identity.
