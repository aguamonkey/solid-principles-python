# Answer notes

[Prompts](INTERVIEW.md)

Policy imports its own writer/queue/sink requirements. Composition selects SQLite and a durable local idempotent sink. Lost commit acknowledgement can reconcile via request replay; lost queue acknowledgement can retry the same event without another local preview.

Inject the fixture at create_app or process_receipt. Preserve event identity/content across retries. Do not delete the accepted reading or claim rollback. For a real remote provider, require its documented idempotency/retention contract before treating it as substitutable.

Discuss the actual mechanism and its limits. The backend decisions separate policy guarantees from the extra contracts that public deployment or remote suppliers would require.
