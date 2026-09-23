# BM4 Post-run Analysis Manifest

The generated `PUBLICATION-MANIFEST.json` remains unchanged and continues to describe the original 62-file BM4 publication package produced by the benchmark finalizer.

The following interpretation artifacts were added afterward and are intentionally tracked separately so the generated evidence package remains immutable:

| Path | Git blob SHA |
| --- | --- |
| `analysis/bm3-to-bm4.md` | `24dc4121db3ea28a77d92b0074a75972adb4313c` |
| `optimization-results.md` | `26ee1f751b132f2be96efd17a8ebba71fc0637c0` |
| `portfolio-summary.md` | `7ae6b372e15d5e3e29f8a6a5ea2e463145c26a58` |
| `analysis/official-scoring-matrix.md` | `9a0c65bf99e4f660ae75fd6919d1e67da9ce7e05` |
| `analysis/end-to-end-product-rubric.md` | `a556709b88e3d28487b2546410b44225c0bf96b7` |
| `analysis/end-to-end-product-score.json` | `44bdb37bcb4ca65aa7d1da6848292d79201b0b65` |

These files interpret the frozen BM3/BM4 evidence; they do not modify benchmark execution, the official frozen score, visual evidence, or the original BM4 publication manifest.

The supplementary end-to-end product score is explicitly post-hoc and non-official. It exists as a product-completeness lens and future rubric-design input; it does not replace the official BM4 machine score.
