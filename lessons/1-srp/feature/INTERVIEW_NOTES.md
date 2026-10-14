# Answer notes · reading recovery

[Prompts](INTERVIEW.md)

1. Both operations participate in one state-publication policy: validate, confirm, retain useful data and publish outcomes. The boundary follows reasons to change, not method count.
2. Text input and numeric supplied data have different representations and can have different rules. A new editing ceiling must not make existing source readings unreadable.
3. Empty success confirms there is no current reading and requests snapshot clearing. Failure leaves the last confirmed value useful and does not invent a new snapshot.
4. A structurally valid response can belong to a different station. Publishing it would misattribute an acknowledgement; valid source normalisation of temperature remains allowed.
5. The update is unconfirmed. The supplier may have changed already. Retaining confirmed data and refreshing later is reconciliation, not guaranteed rollback or safe automatic retry.
6. Snapshot writing is auxiliary to the confirmed source result. Its failure produces a separate notice; it must not hide that result or claim the supplier update failed.
7. Define request lifetimes, ordering, obsolete-result guards and cancellation semantics. The synchronous desk supplies none of those guarantees and is not a concurrent actor.
8. Protocols describe members for static analysis. They do not validate unknown payloads or prove correct behaviour of suppliers. Explicit decoders and behavioural tests address separate requirements.
