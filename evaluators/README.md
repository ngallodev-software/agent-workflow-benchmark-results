# Evaluators

Task-specific post-seal evaluator artifacts live here.

The generic scoring engine, scoring-bundle schema, TypeSafe/LLM probe support, and
bundle tooling live in `agent-workflow-benchmark`. This directory contains only
benchmark-specific evaluator material that must not be present during agent execution.

Evaluator bundles are organized by benchmark and evaluator version:

```text
evaluators/
  bm6/
    v1/
```

A task-specific evaluator should be added only after the corresponding execution
has been sealed.
