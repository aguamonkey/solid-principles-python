# Single Responsibility · Field notebook

[Repository](../../README.md) · [Exercise](EXERCISE.md) · [Solution notes](SOLUTION.md) · [Interview](INTERVIEW.md) · [Recovery lab](feature/README.md)

Reading validation, report formatting and storage respond to different changes.

## Before: the change pressure

A function that decodes input, writes storage and assembles display text forces unrelated changes into one place. This describes the coupled design to reason about; it is not a hidden working service.

## After: follow the actual source

Read [srp.py](../../src/solid_workbook/srp.py) and the [contract tests](../../tests/test_workbook.py).

record_reading validates unknown input before calling a ReadingAppender. render_reading owns display. Frozen Reading values prevent ordinary field reassignment; protocols do not validate runtime input.

Run `PYTHONPATH=src python -m solid_workbook srp`. The CLI is composition, not the domain policy. Output is a local demonstration, not a network or persistence acknowledgement.

## Explain the decision

State the consumer’s promise, point to its implementation, then name the test that demonstrates it. Try the exercise before reading solution notes.

## Progression and limits

This is a runnable foundation with behavioural tests. The separate [recovery lab](feature/README.md) adds source failure retention, independent edit rules, acknowledgement checks and snapshot outcomes. Its edit-ceiling exercise differs from this foundation’s station-name exercise. A later feature stage can add failure recovery and more consumers; a system stage can define migration, versioning, concurrency and durable supplier contracts. Those advanced stages are not implemented by this initial milestone.

No number of traits, protocols, files or classes proves SOLID. The chosen change pressure and consumer behaviour justify the boundary. These trusted, synchronous examples cannot establish universal substitutability or production safety.
