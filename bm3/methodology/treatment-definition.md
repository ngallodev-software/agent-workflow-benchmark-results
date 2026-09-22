# BM3 treatment definition

BM3 uses a paired design over the same frozen task fixture and three phases: analyze/plan, implement, and verify/repair.

## Control — `structured-direct/v1`

The control runs each structured phase prompt directly through Codex. It includes canonical task prompts, the benchmark-neutral safety envelope, requirements traceability, bounded plan-before-edit discipline, writable-scope/non-target checks, acceptance-first verification, phase-completion evidence, self-review, and drift audit.

## Candidate — `agent-workflow-full/v1`

The candidate receives the same structured phase prompts and discipline, but executes through Agent-Workflow. It additionally uses Agent Run lifecycle management, durable execution state, completion evidence, and sealing.

The effective prompt artifacts differ only in arm/treatment identity. Model (`gpt-5.6-luna`), reasoning effort (`high`), executor family, fixture, task prompt, and paired start are held constant.

## TypeSafe/Jev

TypeSafe/Jev semantic routing was exercised before paired execution as a qualification/calibration check in `comparative` mode. It was explicitly not part of either treatment. Three qualification calls were recorded; the treatment definition states that paired execution includes no semantic routing treatment.

## Claim level

This run uses one repetition under `comparative-development/v1`. Winner policy is disabled and would in any event require at least 10 eligible pairs. BM3 therefore supports diagnosis and optimization hypotheses, not a generalized winner claim.
