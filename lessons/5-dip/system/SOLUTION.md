# Solution notes

[Exercise](EXERCISE.md)

Inject the fixture at create_app or process_receipt. Preserve event identity/content across retries. Do not delete the accepted reading or claim rollback. For a real remote provider, require its documented idempotency/retention contract before treating it as substitutable.

These are review notes, not an implemented exercise. Explain one practical limitation and where a new requirement would legitimately change the chosen contract.
