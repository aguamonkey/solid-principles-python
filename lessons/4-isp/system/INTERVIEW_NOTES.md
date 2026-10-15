# Answer notes

[Prompts](INTERVIEW.md)

ReadingPager supplies page, ReadingLookup supplies get, and ReadingReader composes both for the HTTP layer. Export policy requests only ReadingPager. The writer, queue and sink remain separate; the queue retains its two related processing operations.

Type the consumer against the pager requirement and compute from the supplied immutable page. Do not import SqliteNotebook or require unused write stubs. Keep both queue operations together because process_receipt genuinely needs both.

Discuss the actual mechanism and its limits. The backend decisions separate policy guarantees from the extra contracts that public deployment or remote suppliers would require.
