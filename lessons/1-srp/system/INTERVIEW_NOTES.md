# Answer notes

[Prompts](INTERVIEW.md)

Trace an intake through its strict request model, Observation, record_observation, ReadingWriter and SQLite transaction. HTTP never implements the SQL transaction; policy never chooses a concrete connection.

Register a display renderer. Convert only the projection, preserve the underlying observation and add a test against the same repository before/after export. Do not redefine Observation.kelvin or mutate history.

Discuss the actual mechanism and its limits. The backend decisions separate policy guarantees from the extra contracts that public deployment or remote suppliers would require.
