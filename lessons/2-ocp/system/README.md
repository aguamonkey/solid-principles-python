# Extend exports without editing lookup

[Foundation](../README.md) · [Architecture](../../../docs/ARCHITECTURE.md) · [Exercise](EXERCISE.md) · [Interview](INTERVIEW.md)

## Problem and reasoning

A consumer needs another representation of the same bounded data. The batch/repository policy should not grow concrete-format branches for every new renderer.

Exporters captures named renderers, export_page reads through a pager port, and HTTP selects a name. A test-only renderer uses the unchanged policy. The earlier CLI lab adds separate versioned payload-compatibility reasoning.

Read [exports.py](../../../src/solid_workbook/backend/exports.py) and [http.py](../../../src/solid_workbook/backend/http.py), then find the corresponding behaviour in [the backend tests](../../../tests/test_backend.py). Run the API walkthrough and explain one request before changing code.

## Levels of thinking

Foundation identifies a useful boundary. Feature ownership retains correct outcomes when operations fail or suppliers change. System ownership defines durable identity, concurrency, compatibility and migration semantics. The [decisions](../../../docs/decisions/README.md) record both chosen behaviour and its limits.

The backend is a local reference implementation with explicit limits. Do not claim that more protocols establish seniority or that passing tests prove every implementation/input. State the actual promise and evidence.
