# Interface Segregation · Station board

[Repository](../../README.md) · [Exercise](EXERCISE.md) · [Solution notes](SOLUTION.md) · [Interview](INTERVIEW.md)

The board reads entries. It should not require a recorder to supply or test that data.

## Before: the change pressure

Typing every consumer against a read-and-write manager makes read-only fixtures invent unsupported write methods. This describes the coupled design to reason about; it is not a hidden working service.

## After: follow the actual source

Read [isp.py](../../src/solid_workbook/isp.py) and the [contract tests](../../tests/test_workbook.py).

ReadingReader is a structural protocol for tuple snapshots. station_summary works with a fixture exposing only readings(). NotebookPort composes reading and appending for a consumer that really needs both. This is not authorisation.

Run `PYTHONPATH=src python -m solid_workbook isp`. The CLI is composition, not the domain policy. Output is a local demonstration, not a network or persistence acknowledgement.

## Explain the decision

State the consumer’s promise, point to its implementation, then name the test that demonstrates it. Try the exercise before reading solution notes.

## Progression and limits

This is a runnable foundation with behavioural tests. A later feature stage can add failure recovery and more consumers; a system stage can define migration, versioning, concurrency and durable supplier contracts. Those advanced stages are not implemented by this initial milestone.

No number of traits, protocols, files or classes proves SOLID. The chosen change pressure and consumer behaviour justify the boundary. These trusted, synchronous examples cannot establish universal substitutability or production safety.
