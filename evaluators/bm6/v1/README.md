# BM6 evaluator v1

Post-seal evaluator for the BM6 **Change Window Planner** run.

Files:

- `bm6-universal-scoring-bundle-v1.zip` — canonical scoring bundle.
- `bm6-universal-scoring-bundle-v1.zip.sha256` — archive checksum.

The bundle was created only after BM6 execution was sealed. It contains the
deterministic evaluator, batched TypeSafe scoring configuration, optional LLM
review prompt, frozen task text, expected fixture data, and generic `score.py`
entrypoint.

Validate after unpacking:

```bash
agent-workflow benchmark scoring-bundle-validate /path/to/bm6-universal-scoring-bundle-v1
```

Score the already-sealed run:

```bash
agent-workflow benchmark score RUN_PLAN.json \
  --scoring-bundle /path/to/bm6-universal-scoring-bundle-v1
```
