# Own supplier contracts and acknowledgement semantics

[Foundation](../README.md) · [Architecture](../../../docs/ARCHITECTURE.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

## Problem and reasoning

Saving an observation and producing a receipt have independent acknowledgements. Constructor injection alone does not decide what a failed supplier call means or who defines its guarantees.

Policy imports its own writer/queue/sink requirements. Composition selects SQLite and a durable local idempotent sink. Lost commit acknowledgement can reconcile via request replay; lost queue acknowledgement can retry the same event without another local preview.

Read [policy.py](../../../src/solid_workbook/backend/policy.py) and [sqlite_store.py](../../../src/solid_workbook/backend/sqlite_store.py), then find the corresponding behaviour in [the backend tests](../../../tests/test_backend.py). Run the API walkthrough and explain one request before changing code.

## Levels of thinking

Foundation identifies a useful boundary. Feature ownership retains correct outcomes when operations fail or suppliers change. System ownership defines durable identity, concurrency, compatibility and migration semantics. The [decisions](../../../docs/decisions/README.md) record both chosen behaviour and its limits.

The backend is a local reference implementation with explicit limits. Do not claim that more protocols establish seniority or that passing tests prove every implementation/input. State the actual promise and evidence.
