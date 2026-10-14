# Field notebook · reliable reading recovery

[Foundation](../README.md) · [Decision](DECISION.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

A reading desk refreshes a station’s temperature, accepts a text edit and writes a local snapshot. These operations can fail at different boundaries. Useful confirmed data should remain visible, and a confirmed supplier result should not disappear because snapshot storage failed.

Run from the repository root:

```bash
PYTHONPATH=src python -m solid_workbook srp-lab
```

The deterministic walkthrough loads, refreshes offline, recovers, rejects a bad edit, loses an update acknowledgement, reconciles through refresh and demonstrates snapshot failure/recovery. No network or disk storage is used.

## Ownership map

| Change | Owner |
| --- | --- |
| Shape and meaning of supplied numeric data | `decoding.py` and the foundation `Reading` value |
| Rules for a text edit | `edit_rules.py` |
| Fetch/update transport | `ReadingSource` implementation |
| Retention, acknowledgement and publication | `ReadingDesk` |
| Snapshot destination | `SnapshotWriter` implementation |
| Words and formatting shown to the learner | `presentation.py` |
| Selection of the local suppliers | `lab.py` |

Multiple related operations can belong to one policy. Refreshing, editing, retaining and publishing are one desk’s state-transition responsibility. SRP does not require one method per class.

## Behavioural contract

- Source readings require nonblank station identity and finite nonnegative numeric kelvin. Booleans and numeric strings from the source are invalid. `None` is a confirmed empty result.
- Text edits are parsed separately, retain the current station identity, and are validated before updating the source. Editing without a loaded reading does not call it.
- Failed or malformed refreshes retain the last confirmed reading and do not write a snapshot. A successful empty refresh clears the visible reading and asks the snapshot writer to clear it.
- Updates may normalise temperature. An acknowledgement must still identify the same exact station; malformed, empty or wrong-station acknowledgements are not published.
- An update exception yields **unconfirmed**, preserving the previous confirmed reading. The supplier may already have committed. A successful refresh can reconcile the desk with that supplier state.
- Confirmed source results are published before snapshot writing. If that write fails, the source result remains visible with a snapshot-specific notice. The snapshot might have changed before its acknowledgement failed.
- Success clears an earlier notice. State and readings are frozen value objects, with no ordinary field reassignment.

## Follow the actual source

1. [ports.py](../../../src/solid_workbook/reading_desk/ports.py): source and snapshot requirements.
2. [decoding.py](../../../src/solid_workbook/reading_desk/decoding.py): supplied data and acknowledgement identity.
3. [edit_rules.py](../../../src/solid_workbook/reading_desk/edit_rules.py): text input policy.
4. [policy.py](../../../src/solid_workbook/reading_desk/policy.py): synchronous state transitions and failure retention.
5. [presentation.py](../../../src/solid_workbook/reading_desk/presentation.py): labels and value formatting.
6. [adapters.py](../../../src/solid_workbook/reading_desk/adapters.py): deterministic supplier modes and memory snapshots.
7. [lab.py](../../../src/solid_workbook/reading_desk/lab.py): composition and walkthrough.
8. [Tests](../../../tests/test_reading_desk.py): twenty behavioural cases; the original foundation tests remain.

## Limits

The snapshot port is write-only. The desk does not bootstrap from stored values or implement cache freshness. Memory snapshots and the supplier last only for this process. Methods are synchronous and the desk is not thread-safe or reentrant; there is no cancellation, request generation guard or concurrency control.

Python protocols support static checks but do not enforce implementations at runtime. Broad supplier exceptions become boundary notices; a production service needs suitable diagnostics without exposing raw errors to users. These examples do not provide retries, durable identity or transactional coordination. A refresh observes current supplier state, not proof that a particular earlier write caused it.

The source decoder keeps its numeric domain independent of future stricter editing rules. Try the [edit-limit exercise](EXERCISE.md) before reading the solution. The foundation’s station-name exercise remains separate and unimplemented.
