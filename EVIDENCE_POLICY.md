# Public Evidence Policy

This repository is public. Only material suitable for public disclosure belongs here.

## Publish

Public benchmark records may include:

- frozen benchmark specifications and safe task instructions;
- sanitized starting fixtures;
- finished software produced by each treatment;
- source/tool/model/version identities;
- machine scoring and deterministic test evidence;
- wall-time and phase timing summaries;
- provider token counts;
- public-safe Agent-Workflow receipts;
- sanitized TypeSafe aggregate statistics;
- hashes of retained private evidence;
- methodology, limitations, and analysis.

## Keep private

Do not commit:

- `TYPESAFE_API_KEY` or any credential/token;
- Codex/OpenAI authentication/session material;
- raw `typesafe-api-audit.jsonl`;
- raw semantic request/response payloads containing projected task context;
- private filesystem paths when they reveal local/user information;
- secrets from provider logs;
- raw evidence archives before public-safety review;
- unrelated local repository or user data.

## Provenance for private evidence

When useful, the public manifest may record hashes of private artifacts without publishing their contents.

Example:

```json
{
  "private_evidence": {
    "raw_archive_sha256": "...",
    "typesafe_audit_sha256": "...",
    "published": false
  }
}
```

## Publication gate

Before publishing a completed benchmark:

1. inspect the evidence archive;
2. verify secret scanning passed;
3. extract only public-safe result fields;
4. copy final software trees;
5. remove local paths and credentials;
6. record source revisions and hashes;
7. document claim level and limitations;
8. verify the public tree independently.
