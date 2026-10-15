# A practical senior-level rehearsal

[Architecture](ARCHITECTURE.md) · [Decisions](decisions/README.md) · [Answer notes](INTERVIEW_NOTES.md)

Start with five minutes: demonstrate intake, replay, conflict, export and receipt processing. Then choose one of these questions and explain the evidence before reading notes.

1. Where would a new station display rule belong, and where would an intake invariant belong?
2. Add an export recipe. What code should remain unchanged, and when could changing that policy be justified?
3. What must a replacement repository preserve beyond method signatures?
4. Why does the export consumer not need a writer or receipt sink?
5. Why is injecting a concrete database not the whole DIP story?
6. What happens if the process loses acknowledgement after accepting a reading?
7. Why commit the reading, request key and outbox event together?
8. Does an outbox establish exactly-once delivery? Show the gap.
9. How does a request retry differ from a receipt retry?
10. What guarantees does cursor paging provide when new readings arrive?
11. Why are these HTTP endpoints synchronous? How would an async store change the choice?
12. What would you change before adding tenants, a network sender or a background worker?

For each answer give a problem, decision, test and tradeoff. Point to actual source and evidence rather than counting protocols. A useful exercise is to defend an alternative you did not choose, such as a simpler whole-document export or a different duplicate policy.
