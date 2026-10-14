# Exercise · restrict edits without changing readable data

[Lab](README.md) · [Solution notes](SOLUTION.md)

The operator now permits edited temperatures up to **350 K**. The source can still contain older or exceptional readings above that value, and those readings must remain readable.

Change only the edit-policy boundary. Accept 0 K and 350 K; reject a text edit above 350 K before the supplier is called. Keep the existing nonnegative/finite rules. Do not change `Reading`, source decoding, transport or presentation to impose this editing ceiling.

Test that a supplied 400 K reading loads, a 351 K edit is rejected with no update or snapshot write, and a valid 350 K edit succeeds. Keep lost-acknowledgement and snapshot failure behaviour intact.

Run the README checks and the lab. Explain why input editing policy and readable source domain can differ. This exercise is intentionally not implemented.
