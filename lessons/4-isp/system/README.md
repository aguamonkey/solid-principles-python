# Let each consumer request its actual operations

[Foundation](../README.md) · [Architecture](../../../docs/ARCHITECTURE.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

## Problem and reasoning

An exporter reads a bounded page. It should not need to append observations, acknowledge receipts or even look up a single identity just to satisfy a broad store interface.

ReadingPager supplies page, ReadingLookup supplies get, and ReadingReader composes both for the HTTP layer. Export policy requests only ReadingPager. The writer, queue and sink remain separate; the queue retains its two related processing operations.

Read [ports.py](../../../src/solid_workbook/backend/ports.py) and [exports.py](../../../src/solid_workbook/backend/exports.py), then find the corresponding behaviour in [the backend tests](../../../tests/test_backend.py). Run the API walkthrough and explain one request before changing code.

## Levels of thinking

Foundation identifies a useful boundary. Feature ownership retains correct outcomes when operations fail or suppliers change. System ownership defines durable identity, concurrency, compatibility and migration semantics. The [decisions](../../../docs/decisions/README.md) record both chosen behaviour and its limits.

The backend is a local reference implementation with explicit limits. Do not claim that more protocols establish seniority or that passing tests prove every implementation/input. State the actual promise and evidence.
