# Decision · pending intent and idempotent local effect

[Decisions](README.md)

Accepting an observation and producing a receipt are different acknowledgements. Commit pending intent with the observation, then process one event explicitly through a sink port. A sink result precedes queue acknowledgement, so failure between those operations can require a retry.

The bundled sink stores event identity/content and its receipt in SQLite. Exact replay returns that receipt; changed content conflicts. This demonstrates durable idempotency of a local effect, including after a restart. It does not prove exactly-once email or other external delivery.

We could combine preview creation and queue acknowledgement in one local transaction, but keeping them separate exposes the supplier boundary that matters when a provider is external. We do not add worker leases here: duplicate attempts are expected and the local sink deduplicates them. Adding a non-idempotent provider without a contract change would be incorrect.

The first pending event can block later work if it repeatedly fails. Backoff, attempt limits, dead-letter handling and autonomous scheduling are future policies. Processing remains an explicit local API operation.
