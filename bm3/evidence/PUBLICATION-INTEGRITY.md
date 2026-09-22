# BM3 publication integrity

The public BM3 package contained 38 publishable files covering:

- the starting fixture and benchmark specification;
- both completed software trees;
- per-arm machine score, timing, and usage summaries;
- sanitized TypeSafe qualification evidence.

All 38 files were imported into this repository from their exact base64 payloads. After publication, every destination Git blob ID was compared with a Git blob created from the corresponding package payload. Result: **38/38 matched, 0 mismatches**.

The canonical task and three phase prompts were reconstructed from the last public benchmark source revision before execution, `76f6005845a17dc9d36da1c67cede4a5a9e3d5cb`. Their canonical bundle SHA-256 is:

`aeb436c39c62b4767d81938d547d3ae3ae71b0c2f65442d13f76ac1948b94b7d`

That exactly matches the task prompt digest recorded by BM3. See `../task/SOURCE-PROVENANCE.md`.

Raw private evidence and raw TypeSafe audit logs remain intentionally unpublished, as documented in the BM3 result metadata.
