# Interview answer notes

[Prompts](INTERVIEW_PREP.md)

1. Presentation belongs to its renderer; a valid-observation invariant belongs to the domain. An editing restriction may differ from the readable source domain, as the SRP lab demonstrates.
2. Register a renderer without a concrete-format branch in the export policy. A new document-wide rule can legitimately change that policy; OCP is selective.
3. Preserve replay/conflict semantics, immutable projections, sequence order, cursor bounds and receipt behaviour. Shared tests compare memory and real SQLite, including the zero normalisation boundary.
4. Its workflow consumes a bounded page. Requiring writes would make read-only fixtures implement unrelated operations. Related reader operations remain together rather than following a one-method rule.
5. DIP concerns source dependency direction and abstraction ownership. Policy imports its own ports; composition imports implementations and chooses suppliers.
6. The client gets an unconfirmed storage outcome. Retrying the same key/content reconciles through the durable binding. A new key or changed content has different semantics.
7. A partial commit could lose notification intent or permit ambiguous retries. A real rollback test aborts outbox insertion and confirms that the reading and key did not escape.
8. Sender effect and queue acknowledgement remain separate. The local sink durably deduplicates event identity/content; an external provider needs an equivalent contract. Concurrent processors may observe one event.
9. Acceptance retries reuse a request key and immutable observation. Receipt retries reuse event identity/content. A stable request key alone does not deduplicate a remote sender’s effects. The processing endpoint advances pending work; it is not an idempotent replay API for a named event.
10. A cursor orders append-only traversal and avoids offset shifts; new appends can appear later. It does not freeze a dataset across requests. A repeatable export would need a high-water mark or snapshot policy.
11. SQLite calls block. FastAPI dispatches normal endpoints to a thread pool. Async syntax alone would not make those calls nonblocking; an async adapter requires deliberate lifecycle and concurrency choices.
12. Define tenant-scoped identity/permissions, provider idempotency, worker claiming, retry limits and poison-event recovery under their actual requirements. Also decide retention, backups and database migration. They are additional system contracts, not interfaces that can be added without policy decisions.
