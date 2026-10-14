# Interview · reading ownership and failure recovery

[Lab](README.md) · [Answer notes](INTERVIEW_NOTES.md)

1. Why does one desk policy own both refresh and edit operations?
2. Why keep form parsing separate from source decoding?
3. How does a confirmed empty result differ from a failed refresh?
4. Why verify station identity in the update acknowledgement?
5. What does the caller know after an update exception?
6. Why publish before writing the snapshot?
7. What would adding asynchronous suppliers require?
8. How do Python protocols differ from runtime validation?

For a short rehearsal: run the lost-acknowledgement example and explain which value is visible before and after reconciliation. Point to one test and one limitation.
