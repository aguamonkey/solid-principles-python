# Export bench · extension and compatibility

[Foundation](../README.md) · [Decision](DECISION.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

A saved export list contains a supported text record, a JSON extension, a future version, a malformed reading and a duplicate identity. The caller should preserve useful previews without guessing what an unsupported schema means.

```bash
PYTHONPATH=src python -m solid_workbook ocp-lab
```

The walkthrough processes the same bundled list twice: first with text v1, then with JSON v1 added at composition. Only the JSON record becomes ready. No files are written and no service is contacted.

## Progression

| Scope | Question | Evidence |
| --- | --- | --- |
| Foundation | Can a new formatter use the same lookup? | Original formatter protocol and test-only implementation |
| Reliable feature | Can one damaged record leave useful previews readable? | Per-record outcomes, copied projections and ordered results |
| System contracts | Which schema meanings can this release interpret? | Exact format/version registrations and compatibility cases |

Versioned compatibility is one system concern, not a complete migration or durable export system.

## Contract

- Input is an already-parsed list. Empty lists succeed; other document types fail before record processing.
- Envelopes need a nonblank string identity and format plus an actual positive integer version. `True`, `False`, floats and strings are invalid versions. Python integers are unbounded; this lab does not impose a JavaScript safe-integer limit.
- Identity and lookup are exact and case-sensitive. Keys are not trimmed or normalised.
- The first valid envelope claims its identity, including when its schema is unsupported or payload is damaged. Later duplicates are rejected. An invalid envelope does not claim identity.
- Lookup requires the exact format/version pair. Unknown formats or versions are unsupported and do not decode the payload or fall back to another version.
- Registered renderers own payload meaning. A known bad payload, renderer exception or invalid preview is rejected independently of later records.
- Preview labels and bodies must be nonblank strings. Accepted projections are copied into frozen dataclasses, and the report preserves input order.
- Registration finishes at construction. Duplicate schema keys fail composition. The mapping captures its own entries and exposes lookup without a registration mutation API.

Text v1 and JSON v1 both expect `station` and numeric `kelvin`, validated through the foundation reading decoder. Their version describes the registered input/output recipe’s meaning; it is not inferred from a payload or chosen by a fallback.

## Read the actual source

1. [registry.py](../../../src/solid_workbook/export_lab/registry.py): schema keys, preview domain and captured registrations.
2. [batch.py](../../../src/solid_workbook/export_lab/batch.py): envelope, identity and recovery policies.
3. [composition.py](../../../src/solid_workbook/export_lab/composition.py): text/JSON adapters and sample records.
4. [lab.py](../../../src/solid_workbook/export_lab/lab.py): composition comparison using one algorithm.
5. [Tests](../../../tests/test_export_lab.py): twenty-two extension and compatibility cases.

## Where can changes belong?

A new format/version changes its renderer and composition. It does not add a concrete-format branch to the batch loop. A new document-wide identity policy could legitimately change that loop. OCP closes selected boundaries against a stated change pressure, not every future change.

The bundled input remains available when a new registry is composed. The lab previews only; it has no file delivery, durable unsupported-payload store, input size limits, streaming, retry or cross-batch identity reconciliation. Adapters are trusted synchronous functions; a nonterminating renderer cannot be interrupted here.

A mapping proxy prevents ordinary registry writes, but renderers can capture mutable state. Frozen dataclasses prevent ordinary field assignment, not deliberate bypass or every possible side effect. Runtime validation and tests complement static annotations; none establish a plugin sandbox or universal SOLID compliance.

Try the [text v2 exercise](EXERCISE.md). The foundation’s CSV exercise remains separate and unimplemented.
