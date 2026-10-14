# Answer notes · Archive shelf

[Prompts](INTERVIEW.md)

SnapshotSource returns an immutable tuple of nonblank string titles. An empty tuple is valid. TitleArchive preserves that contract; DriftingArchive matches the signature but breaks stability. The inspector samples two reads, not all possible behaviour.

Do not special-case the wrapper in inspect_snapshot. Copy the source projection into a tuple. Reject blank prefixes at construction and preserve stable ordered titles.

A useful answer connects a concrete change pressure to a consumer requirement, points to source and behavioural evidence, and states the limits. Revisit the lesson if you can only recite the principle’s definition.
