# Answer notes

[Prompts](INTERVIEW.md)

The same StoreContract cases run against both adapters. They cover exact replay/conflict, canonical zero, ordered pages, cursor bounds, immutable projections and receipt acknowledgements. SQLite-only tests add transaction, restart and concurrency evidence.

An overwrite violates append-only identity even if every type annotation matches. Preserve key/content binding and original data. Do not special-case the adapter in the consumer or change the expected result just to make it pass.

Discuss the actual mechanism and its limits. The backend decisions separate policy guarantees from the extra contracts that public deployment or remote suppliers would require.
