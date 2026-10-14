# Open/Closed · Export bench

[Repository](../../README.md) · [Exercise](EXERCISE.md) · [Solution notes](SOLUTION.md) · [Interview](INTERVIEW.md) · [Compatibility lab](feature/README.md)

A registry accepts formatter implementations; export lookup does not branch on concrete format names.

## Before: the change pressure

An exporter with a growing if/elif or match over every format needs editing for each supplier. This describes the coupled design to reason about; it is not a hidden working service.

## After: follow the actual source

Read [ocp.py](../../src/solid_workbook/ocp.py) and the [contract tests](../../tests/test_workbook.py).

Formatter is a structural protocol. A test-only object with format() extends the same registry. Duplicate/blank registration fails, lookup is exact and unknown formats fail. Formatter objects may still hold mutable state.

Run `PYTHONPATH=src python -m solid_workbook ocp`. The CLI is composition, not the domain policy. Output is a local demonstration, not a network or persistence acknowledgement.

## Explain the decision

State the consumer’s promise, point to its implementation, then name the test that demonstrates it. Try the exercise before reading solution notes.

## Progression and limits

This is a runnable foundation with behavioural tests. The separate [compatibility lab](feature/README.md) adds exact format/version registrations, identity policy and independent record recovery. A later feature stage can add failure recovery and more consumers; a system stage can define migration, versioning, concurrency and durable supplier contracts. Those advanced stages are not implemented by this initial milestone.

No number of traits, protocols, files or classes proves SOLID. The chosen change pressure and consumer behaviour justify the boundary. These trusted, synchronous examples cannot establish universal substitutability or production safety.
