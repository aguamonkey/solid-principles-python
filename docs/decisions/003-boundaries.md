# Decision · explicit ports and synchronous storage

[Decisions](README.md)

Use separate reader, writer, queue and sink contracts, with operations grouped around consumers. A broad concrete store can fulfil several ports without widening each client. Export uses only a reader; receipt processing uses only queue and sink.

Composition selects memory or SQLite outside policy. The same behavioural contract suite runs against both repositories and sinks; protocol conformance alone is insufficient. The catalogue lab separately demonstrates why a stable snapshot contract is stronger than a live repository read.

SQLite is synchronous and endpoints use ordinary def functions. Each adapter operation opens/closes its connection on one thread; write transactions are explicit. Async endpoints, an ORM or a service container would add mechanisms without resolving an existing requirement in this bounded reference workflow.

The initial schema is version 1. Unknown versions are refused, and initial DDL is transactional. There is no downgrade or general migration framework. A new schema needs an explicit migration and recovery plan rather than silently rerunning CREATE statements.
