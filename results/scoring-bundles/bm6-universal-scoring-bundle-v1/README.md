# BM6 universal post-seal scoring bundle v1

This bundle was created after the BM6 Change Window Planner execution was sealed.
It contains the task-specific evaluator material that was intentionally absent during execution.

## Default weighting

The bundle's default 100-point machine score uses approximately:

- 82.5 points maximum from deterministic checks.
- 17.5 points maximum from one five-question TypeSafe batch per arm.
- 0 points from the included optional LLM probe unless you explicitly wire it into bundle.json.

The TypeSafe probe is independent and anchor-based. Each candidate is evaluated against the
same fixed task and deterministic evidence; the other candidate is never included in the request.

## Universal JSON controls

Edit `bundle.json` to add/change:

- `parameters`: arbitrary JSON; scalar values are also available as `{param_NAME}` to commands.
- `probes`: deterministic commands, additional `typesafe-batch` calls, or `llm-command` calls.
- TypeSafe questions and criteria.
- LLM argv, prompt file, response mode, and bounded context.
- source globs, bundle context files, prior probe outputs, file/byte limits.
- scoring weights and JSON Pointer mappings.

Additional TypeSafe calls are simply additional `typesafe-batch` probe entries.
An expensive probe is cached by bundle digest + sealed worktree digest, so multiple dimensions
can reuse one response.

## Use

Requires `agent-workflow-benchmark==0.3.9` and `typesafe-sdk==0.6.0`.

Validate:

    agent-workflow benchmark scoring-bundle-validate /path/to/bm6-universal-scoring-bundle-v1

Score the already-sealed run:

    agent-workflow benchmark score RUN_PLAN.json \
      --scoring-bundle /path/to/bm6-universal-scoring-bundle-v1

The benchmark re-verifies the execution seal after probes complete and before committing the
machine-score summary.

## Optional LLM probe

`optional-llm-deep-review` is configured for Codex/GPT-6 Luna but is not part of the default
score. This lets you inspect or later incorporate an LLM judgment without silently changing
the initial rubric.
