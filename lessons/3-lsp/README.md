# Liskov Substitution · Archive shelf

[Repository](../../README.md) · [Exercise](EXERCISE.md) · [Solution notes](SOLUTION.md) · [Interview](INTERVIEW.md)

A snapshot source promises stable content, not merely a matching method signature.

## Before: the change pressure

A replacement returning a new revision on every read breaks a client that expects a fixed snapshot. This describes the coupled design to reason about; it is not a hidden working service.

## After: follow the actual source

Read [lsp.py](../../src/solid_workbook/lsp.py) and the [contract tests](../../tests/test_workbook.py).

SnapshotSource returns an immutable tuple of nonblank string titles. An empty tuple is valid. TitleArchive preserves that contract; DriftingArchive matches the signature but breaks stability. The inspector samples two reads, not all possible behaviour.

Run `PYTHONPATH=src python -m solid_workbook lsp`. The CLI is composition, not the domain policy. Output is a local demonstration, not a network or persistence acknowledgement.

## Explain the decision

State the consumer’s promise, point to its implementation, then name the test that demonstrates it. Try the exercise before reading solution notes.

## Progression and limits

This is a runnable foundation with behavioural tests. A later feature stage can add failure recovery and more consumers; a system stage can define migration, versioning, concurrency and durable supplier contracts. Those advanced stages are not implemented by this initial milestone.

No number of traits, protocols, files or classes proves SOLID. The chosen change pressure and consumer behaviour justify the boundary. These trusted, synchronous examples cannot establish universal substitutability or production safety.
