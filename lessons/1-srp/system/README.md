# Ownership under a real intake request

[Foundation](../README.md) · [Architecture](../../../docs/ARCHITECTURE.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

## Problem and reasoning

HTTP parsing, observation invariants, acceptance policy, persistence and response presentation can change for different reasons. A controller that does all five would make a transport change disturb transaction policy.

Trace an intake through its strict request model, Observation, record_observation, ReadingWriter and SQLite transaction. HTTP never implements the SQL transaction; policy never chooses a concrete connection.

Read [http.py](../../../src/solid_workbook/backend/http.py) and [policy.py](../../../src/solid_workbook/backend/policy.py), then find the corresponding behaviour in [the backend tests](../../../tests/test_backend.py). Run the API walkthrough and explain one request before changing code.

## Levels of thinking

Foundation identifies a useful boundary. Feature ownership retains correct outcomes when operations fail or suppliers change. System ownership defines durable identity, concurrency, compatibility and migration semantics. The [decisions](../../../docs/decisions/README.md) record both chosen behaviour and its limits.

The backend is a local reference implementation with explicit limits. Do not claim that more protocols establish seniority or that passing tests prove every implementation/input. State the actual promise and evidence.
