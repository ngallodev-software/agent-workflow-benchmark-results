Review the supplied Change Window Planner implementation using only the frozen task,
source files, and deterministic probe evidence in the evaluation context. Return one JSON
object with numeric 0..10 fields: correctness, robustness, accessibility_ui,
task_completeness, engineering_quality, plus a concise findings array. Do not compare this
candidate with another implementation. Do not claim behavior that is not supported by the
provided source or deterministic evidence.

This probe is OPTIONAL in bundle v1 and is not connected to scoring dimensions by default.
To use it, add components referencing /payload/<field> to bundle.json.
