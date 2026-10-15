# Foundation → reliable feature → system contracts

[Repository](../README.md) · [Python orientation](PYTHON_START.md) · [Interview practice](INTERVIEW_PREP.md)

Pick one principle at a time. Read for ten minutes, run its example for ten, then explain it aloud for ten. Attempt coding exercises in a separate session, before opening their solution notes.

| Principle | Start | Explore failure or change | Follow into the backend |
| --- | --- | --- | --- |
| SRP | [Foundation](../lessons/1-srp/README.md) | [Recovery lab](../lessons/1-srp/feature/README.md) | [Intake ownership](../lessons/1-srp/system/README.md) |
| OCP | [Foundation](../lessons/2-ocp/README.md) | [Compatibility lab](../lessons/2-ocp/feature/README.md) | [Export extension](../lessons/2-ocp/system/README.md) |
| LSP | [Foundation](../lessons/3-lsp/README.md) | [Catalogue lab](../lessons/3-lsp/feature/README.md) | [Repository contracts](../lessons/3-lsp/system/README.md) |
| ISP | [Foundation](../lessons/4-isp/README.md) | [Bounded reader workflow](../lessons/4-isp/system/README.md) | [Port ownership](../lessons/4-isp/system/README.md) |
| DIP | [Foundation](../lessons/5-dip/README.md) | [Processing outcomes](../lessons/5-dip/system/README.md) | [Composition and durable intent](../lessons/5-dip/system/README.md) |

These describe increasing responsibility, not automatic job titles. Foundation asks whether a boundary helps. Feature ownership asks what happens when something fails. System ownership defines identity, concurrency, persistence and migration promises, then tests their practical limits.

After a session, write: what changed, what stayed stable, and what risk remains? Revisit without notes. Compare the same question in Swift or TypeScript after recall, rather than translating classes mechanically.

For a recruiter walkthrough, run the API, demonstrate an exact replay and a conflict, then show one transaction test and one shared adapter contract. Explain why a real email supplier would require a separate idempotency agreement.
