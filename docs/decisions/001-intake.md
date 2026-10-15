# Decision · immutable readings and durable replay binding

[Decisions](README.md)

A researcher must not overwrite earlier observations because a client retried a request. Store append-only observations with an exact identity and bind an idempotency key to canonical intent. Same key/content returns the original result; changed content or an existing identity under a new key conflicts.

Canonical numeric values make 0, 0.0 and -0.0 agree in memory and SQLite. Station text and identifiers remain exact. A write transaction installs the reading, binding and pending event together. Uniqueness and immediate transactions serialise competing SQLite writes; the shared memory adapter uses a lock.

An update endpoint would make corrections convenient but alter history and concurrency requirements. Corrections can instead become explicit linked observations in a future requirement. Key expiration and authenticated tenant namespaces are not implemented; this teaching application retains globally scoped bindings indefinitely.
