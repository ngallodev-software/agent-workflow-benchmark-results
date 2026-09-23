# Scoring bundles

Post-seal scoring material lives here, separate from benchmark execution artifacts.

- `bm6-universal-scoring-bundle-v1.zip` — BM6 Change Window Planner universal scoring bundle v1.
  It was created only after the BM6 execution seal existed and contains the deterministic
  evaluator, TypeSafe batch configuration, optional LLM review prompt, frozen task text,
  expected fixture data, and generic `score.py` entrypoint.
- Verify the archive against `bm6-universal-scoring-bundle-v1.zip.sha256` before use.

Unpack the archive outside sealed worktrees and run:

```bash
agent-workflow benchmark scoring-bundle-validate /path/to/bm6-universal-scoring-bundle-v1
agent-workflow benchmark score RUN_PLAN.json \
  --scoring-bundle /path/to/bm6-universal-scoring-bundle-v1
```
