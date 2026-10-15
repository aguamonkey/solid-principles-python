# Learn the Python while following one request

[Repository](../README.md) · [Learning path](LEARNING_PATH.md)

You do not need to know every Python feature before starting. Run one example, read its tests, then make a small change.

1. **Interpreter and virtual environment.** Confirm Python 3.11+. A virtual environment isolates this repo’s dependencies. Activate it before using the README commands. `PYTHONPATH=src` makes the local package importable without publishing it.
2. **Modules and imports.** A directory with `__init__.py` is a package here. `backend/domain.py` contains values; `backend/http.py` adapts them to HTTP. Follow an import to see which layer depends on which.
3. **Type hints.** `ReadingReader` describes operations a consumer needs. An object can satisfy it without inheriting from it. mypy checks that shape statically; it does not turn unknown JSON into trusted data.
4. **Dataclasses.** `Observation` is an immutable value with validation in `__post_init__`. `StoredReading` adds a database sequence. Read the canonical-zero test to see a domain rule rather than just syntax.
5. **Exceptions and explicit outcomes.** Invalid input, identity conflict and an unconfirmed side effect mean different things. Read one API test before following the corresponding branch.
6. **Context managers.** The SQLite adapter scopes connections and transactions. The rollback test injects a real database failure between operations, so its evidence goes beyond a mocked `save()` call.
7. **Synchronous and asynchronous code.** The database calls are synchronous. Follow the architecture explanation before trying to add `async` to functions.
8. **Tests.** `unittest` runs the behavioural suite. Contract mixins apply the same expectations to different adapters; `TestClient` exercises HTTP without requiring a separate running server.

First task: run `python -m solid_workbook srp` with `PYTHONPATH=src`, then explain why formatting does not write storage. Next, open the backend workbench and replay one request. The progression is understanding a boundary, observing its behaviour, changing it, and defending the tradeoff.
