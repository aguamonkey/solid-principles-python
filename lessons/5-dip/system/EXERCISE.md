# Exercise · Own supplier contracts and acknowledgement semantics

[Study](README.md) · [Solution notes](SOLUTION.md)

Replace the local receipt sink with a test-only failing sink, then recover using a sink that fulfils the same idempotency contract. Verify the reading stays accepted, pending intent remains during failure and processing eventually acknowledges.

Write the stable caller behaviour and one alternative first. Implement in your editor, add behavioural evidence and run the README checks. The exercise is not implemented in the reference branch.
