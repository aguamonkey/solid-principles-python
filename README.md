# SOLID principles · Python

A workbook for explaining five design decisions through runnable local examples, behavioural tests and small changes. Start with one lesson, run it, and attempt its exercise before reading the solution.

| Lesson | Setting | Design question |
| --- | --- | --- |
| [01 · Single Responsibility](lessons/1-srp/README.md) | Field notebook | Where should this change belong? |
| [02 · Open/Closed](lessons/2-ocp/README.md) | Export bench | Which algorithm stays stable when another format is added? |
| [03 · Liskov Substitution](lessons/3-lsp/README.md) | Archive shelf | Does the replacement honour the caller’s promise? |
| [04 · Interface Segregation](lessons/4-isp/README.md) | Station board | Which operations does this consumer need? |
| [05 · Dependency Inversion](lessons/5-dip/README.md) | Publication desk | Can suppliers change independently of policy? |

## Run and verify

Use Python 3.11 or newer; check your interpreter version before creating the virtual environment. Runtime examples use only the standard library. Ruff and mypy are pinned development tools. CI checks Python 3.11 and 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
PYTHONPATH=src python -m solid_workbook all

ruff check .
ruff format --check .
mypy
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/check_docs.py
```

Replace `all` with `srp`, `ocp`, `lsp`, `isp` or `dip` to focus on one demonstration. Commands work from the repository root. Tests run separate fixtures without contacting services. There is no browser app in this initial milestone.

## How to study

Follow the [study path](docs/LEARNING_PATH.md). Each lesson links to actual source, tests, an exercise, separate solution notes and interview prompts. The settings use runtime input validation, frozen data and structural protocols rather than translating another language mechanically.

This initial foundation is deliberately smaller than the mature Swift/TypeScript workbooks. It does not yet include their interactive applications or advanced feature/system labs. The [progression](docs/LEARNING_PATH.md) identifies the next steps and keeps that scope visible.

## Cross-language practice

Compare one design question across [Swift](https://github.com/aguamonkey/SOLID-Principles-with-Swift), [TypeScript](https://github.com/aguamonkey/solid-principles-typescript), [Rust](https://github.com/aguamonkey/solid-principles-rust). First explain the promise, then explain how this language changes its implementation. Matching class names is not the study goal.

## Evidence and limits

Seventeen unittest cases cover runtime validation, extension, snapshot behaviour, read-only fixtures and partial publication failure. Strict mypy checks the source contracts; protocol annotations do not enforce those contracts at runtime.

The link checker covers local inline Markdown targets and excludes external URLs and heading fragments. It is not a full Markdown parser. These examples have no durable storage, network, authentication, asynchronous execution or exactly-once guarantees. Two snapshot samples do not prove behaviour for every future implementation. Rust Unavailable is permitted by the manifest contract; Python snapshot exceptions propagate. Those contracts are intentionally explicit.

[Contributing](CONTRIBUTING.md) · [MIT licence](LICENSE)
