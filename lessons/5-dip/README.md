# Dependency Inversion · Publication desk

[Repository](../../README.md) · [Exercise](EXERCISE.md) · [Solution notes](SOLUTION.md) · [Interview](INTERVIEW.md)

Publication policy owns archive and notifier contracts; the command-line composition chooses suppliers.

## Before: the change pressure

Constructing a concrete file store or network notifier inside policy couples use-case decisions to supplier details. This describes the coupled design to reason about; it is not a hidden working service.

## After: follow the actual source

Read [dip.py](../../src/solid_workbook/dip.py) and the [contract tests](../../tests/test_workbook.py).

publish accepts two protocols and returns explicit outcomes. Storage happens first; notification failure leaves the saved report intact. Exceptions are reported as unconfirmed because a supplier can perform an effect and then throw.

Run `PYTHONPATH=src python -m solid_workbook dip`. The CLI is composition, not the domain policy. Output is a local demonstration, not a network or persistence acknowledgement.

## Explain the decision

State the consumer’s promise, point to its implementation, then name the test that demonstrates it. Try the exercise before reading solution notes.

## Backend progression

Follow the [system study](system/README.md) into the working application, with source, tests, an exercise and interview prompts.

## Progression and limits

This is a runnable foundation with behavioural tests. A later feature stage can add failure recovery and more consumers; a system stage can define migration, versioning, concurrency and durable supplier contracts. The linked backend track now supplies the system-level example; broader production requirements remain explicit in its decisions.

No number of traits, protocols, files or classes proves SOLID. The chosen change pressure and consumer behaviour justify the boundary. These trusted, synchronous examples cannot establish universal substitutability or production safety.
