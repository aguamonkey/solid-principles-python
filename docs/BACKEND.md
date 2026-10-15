# Run the research workflow

[Repository](../README.md) · [Architecture](ARCHITECTURE.md) · [Decisions](decisions/README.md)

Start the server with the README command and open `/docs`. Expand an endpoint and use **Try it out**. All records use kelvin and an ASCII observation identity. Station names preserve their supplied text; whitespace-only names are rejected. Fields not in the request schema are rejected.

For a temporary in-memory run, use `--memory`. It cannot be combined with `--database`; state disappears when that process stops. The same HTTP contract suite runs with each adapter.

## One useful experiment

1. POST a reading with identity `ridge-001`, station `North ridge`, kelvin `281.25`, and `Idempotency-Key: ridge-001`.
2. Repeat it. Observe 200 replayed, the same sequence and one recorded observation.
3. Change the temperature under that key. Observe 409; GET the original to confirm it was retained.
4. GET a page or export it as JSON/text. Exports consume the same read-only projection, without a storage write or receipt call.
5. POST `/outbox/process`. It creates a durable local preview receipt and acknowledges the pending event. Call it again to see `empty`.
6. Restart the server using the same database path. The reading, key binding, queue and receipt still exist.

## HTTP contracts

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Process liveness; does not check the database |
| `GET /ready` | Perform a database read through the reader port |
| `POST /readings` | Atomic reading/key/outbox acceptance; 201 new or 200 replayed |
| `GET /readings/{identity}` | Read one immutable observation, or 404 |
| `GET /readings?after=0&limit=25` | Ascending sequence page, maximum 100 rows |
| `GET /export?format=json` | JSON or text export of one bounded page |
| `POST /outbox/process` | Process at most one pending receipt; 503 for unconfirmed boundaries |

Pages return `next_cursor` only when another row exists at query time. Exports return that value in `X-Next-Cursor`. New appends can become visible while traversing pages; this is not repeatable-read export of a frozen dataset. Cursors are nonnegative signed-64-bit integers so memory and SQLite enforce the same domain.

Keys are exact identifier strings, globally scoped in this single-user teaching application. They are retained indefinitely. A new key cannot overwrite or duplicate an existing reading identity. Numeric values are canonicalised so integer, floating and negative zero intents agree. No key expiration or cross-user namespace exists here.

Every HTTP response carries a generated `X-Request-ID`. Storage error responses include that identifier and a generic uncertainty message; server logs retain diagnostic information without intentionally logging request bodies.

## What the receipt represents

The default sink writes a local preview acknowledgement in the database. It is not an email delivery provider. It stores event identity/content and returns the previous receipt for an exact replay. Changed content under that event identity is rejected.

The outbox read, sink effect and queue acknowledgement are separate operations. Multiple processors can observe one event. The bundled sink’s idempotency makes those repeated attempts safe for this local effect. A network sender needs an equivalent durable provider contract; using the same Python protocol is not enough.

Each processing request is a worker tick, not an idempotent HTTP replay bound to a particular event. If an earlier queue acknowledgement committed before its response was lost, another tick can process the next event. Deduplication protects each event’s sink effect; it does not promise the same processing response on every call.

The earliest pending event is processed first. A permanently failing event can block later events. Retry scheduling, attempt limits and dead-letter handling would be separate policies, not cosmetic infrastructure changes.

## Troubleshooting

Use a new port if 8000 is occupied: `--port 8001`. Use a different `--database` path for an isolated dataset. Do not delete a dataset to resolve a retry conflict; inspect the original identity/key intent. A database with an unknown `user_version` is refused rather than silently downgraded. This version supports initial schema creation only, not a general migration framework.
