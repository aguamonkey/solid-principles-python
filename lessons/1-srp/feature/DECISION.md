# Decision · keep confirmed data through boundary failures

[Lab](README.md)

## Pressure

A transient refresh failure should not erase a useful temperature. Snapshot storage failure should not redefine a supplier’s acknowledged update as failed. A thrown update also cannot prove that no write occurred.

## Decision

Keep source decoding, text-edit validation, transport, state publication, snapshot writing and presentation separate. `ReadingDesk` orchestrates one coherent publication policy through typed protocols. It retains confirmed data on failed refresh/update acknowledgement and publishes a valid source result before attempting its snapshot.

Use explicit notice variants, not a single boolean. A successful empty source result is different from a failed request. Snapshot failure is different from source failure. A supplier can commit before losing acknowledgement; the demonstration reconciles by reading its current value again.

## Alternatives

- One component/function doing transport, parsing and output: fewer files initially, but independent rule and display changes share the same owner.
- Clear data on every refresh error: hides information that remains useful to this consumer.
- Write snapshot before publishing: lets an auxiliary failure suppress a valid source result.
- Reuse source decoding as all form validation: a stricter edit rule could reject historical source data that still needs to be read.
- Add asynchronous cancellation now: a different concurrency pressure, not required by this synchronous walkthrough. Future work must define ordering and obsolete-result guards explicitly.

## Consequences

The caller can distinguish confirmed data from uncertain side effects. State notices do not establish rollback, durable storage or retry safety. Supplier exceptions are contained at their own boundary, while production diagnostic policy remains separate. Small protocols aid test fixtures, but behaviour still needs tests.
