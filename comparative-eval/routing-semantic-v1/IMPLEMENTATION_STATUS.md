# Routing Semantic v1 — Implementation Status

**Current state:** implementation merged; 120-case inference corpus frozen; independent oracle and live study not yet complete.

## Evidence pipeline

~~~mermaid
flowchart LR
    A[Frozen public-safe corpus] --> B[Inference run]
    B --> C[Deterministic control]
    B --> D[One batched TypeSafe/Jev request]
    D --> D1[Choice]
    D --> D2[Noul]
    D --> D3[Score]
    C --> E[Three neutral decision observations]
    D1 --> E
    D2 --> E
    D3 --> E
    D --> F[One request-level evidence record]
    G[Separate frozen blinded oracle] --> H[Post-inference oracle join]
    E --> H
    H --> I[Correctness / calibration / disagreement]
    F --> J[Latency / usage / reliability]
    I --> K[Public study report]
    J --> K
~~~

## Implemented and merged

- agent-workflow-comparative-eval 0.2.0 preregistered routing-semantic-v1 study specification;
- separate inference-case and oracle contracts;
- lossless Choice/Noul/Score evidence persistence;
- provider-request deduplication for batched calls;
- explicit exclusion records and sample eligibility;
- Agent-Workflow 0.11.10 lossless semantic evidence path and agent-workflow-benchmark 0.4.0 run/report/publication command lane;
- public-safe publication manifest and Markdown report generation.

## Completed empirical prerequisites

- routing-semantic-v1 study specification is frozen at version 1.1.0;
- routing-semantic-corpus-v1.0.0 contains 120 public-safe cases;
- every case is eligible for all three routing seams;
- benchmark tooling exports a blinded oracle-authoring view with construction tags and treatment outputs removed.

## Intentionally incomplete

- the independent blinded oracle has not been adjudicated/frozen;
- no live TypeSafe/Jev comparative inference run has been executed on the frozen corpus;
- the full study has not been run;
- no Jev effectiveness claim is currently supported.

The eventual result remains publishable even if the semantic candidate is equal to or worse than deterministic control. Evidence quality, not a favorable outcome, is the gate.
