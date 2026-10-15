# Substitute storage while preserving promises

[Foundation](../README.md) · [Architecture](../../../docs/ARCHITECTURE.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

## Problem and reasoning

Matching get/record/page method names does not establish equivalent identity, paging or failure semantics. Memory and SQLite have different mechanisms and numeric limits.

The same StoreContract cases run against both adapters. They cover exact replay/conflict, canonical zero, ordered pages, cursor bounds, immutable projections and receipt acknowledgements. SQLite-only tests add transaction, restart and concurrency evidence.

Read [ports.py](../../../src/solid_workbook/backend/ports.py) and [sqlite_store.py](../../../src/solid_workbook/backend/sqlite_store.py), then find the corresponding behaviour in [the backend tests](../../../tests/test_backend.py). Run the API walkthrough and explain one request before changing code.

## Levels of thinking

Foundation identifies a useful boundary. Feature ownership retains correct outcomes when operations fail or suppliers change. System ownership defines durable identity, concurrency, compatibility and migration semantics. The [decisions](../../../docs/decisions/README.md) record both chosen behaviour and its limits.

The backend is a local reference implementation with explicit limits. Do not claim that more protocols establish seniority or that passing tests prove every implementation/input. State the actual promise and evidence.
