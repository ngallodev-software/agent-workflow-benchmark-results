# BM4 Post-run Analysis Manifest

The generated `PUBLICATION-MANIFEST.json` remains unchanged and continues to describe the original 62-file BM4 publication package produced by the benchmark finalizer.

The following interpretation artifacts are tracked separately so the generated evidence package remains immutable:

| Path | Git blob SHA |
| --- | --- |
| `analysis/code-quality-review-gpt6-luna.md` | `7c8a284876bf6c8891ad8aba74468c394739c270` |
| `analysis/code-quality-review-typesafe.md` | `3d56a175071a06d7ea77a7769b790402604f10ed` |
| `analysis/code-quality-review-typesafe.json` | `723e8c4be1e4f76baf162a46712ca316d3256032` |
| `analysis/code-quality-review-typesafe-analysis.md` | `2f0d7673e0c453ecbf87f817cdd283d4bf792f1e` |
| `analysis/typesafe-request-response-review.md` | `1e3ca69dc12ace326b166c64d2026145e2b3a583` |
| `analysis/code-quality-review-typesafe-v2-full-tree.md` | `de0a8d3e74503524d3a3442008b015e97d5c8407` |
| `analysis/code-quality-review-typesafe-v2-full-tree.json` | `2c3ee581ac8d746d03bc5c0b2ae084c505687fd1` |
| `analysis/code-quality-review-typesafe-v2-matched-file.md` | `c3b713232f6c64d1d445dfd3a56508221364713e` |
| `analysis/code-quality-review-typesafe-v2-matched-file.json` | `b4f15e7bef7883ea81ebae5b63eb99f4a06d6086` |
| `analysis/code-quality-review-typesafe-v2-matched-file-reversed.md` | `e0052532d2716339a080c54dea4412b3a4707298` |
| `analysis/code-quality-review-typesafe-v2-matched-file-reversed.json` | `00e45ee90fee5c50c2fa8e75e469b9c2ef90ecdc` |
| `analysis/typesafe-deterministic-finding-checks.json` | `770dd7b72b1216ccd70dacb7067f7722312b8590` |
| `analysis/bm3-to-bm4.md` | `24dc4121db3ea28a77d92b0074a75972adb4313c` |
| `optimization-results.md` | `26ee1f751b132f2be96efd17a8ebba71fc0637c0` |
| `portfolio-summary.md` | `7ae6b372e15d5e3e29f8a6a5ea2e463145c26a58` |
| `analysis/official-scoring-matrix.md` | `9a0c65bf99e4f660ae75fd6919d1e67da9ce7e05` |
| `analysis/end-to-end-product-rubric.md` | `a556709b88e3d28487b2546410b44225c0bf96b7` |
| `analysis/end-to-end-product-score.json` | `44bdb37bcb4ca65aa7d1da6848292d79201b0b65` |

These files interpret the frozen BM4 evidence or document post-run code review; they do not modify benchmark execution, the official frozen score, visual evidence, or the original BM4 publication manifest.

The supplementary end-to-end product score is explicitly post-hoc and non-official; it does not replace the official BM4 machine score.

The full SDK DEBUG logs are excluded from this manifest and remain owner-only (`0600`) because they contain complete API request and response bodies, including submitted source code.
