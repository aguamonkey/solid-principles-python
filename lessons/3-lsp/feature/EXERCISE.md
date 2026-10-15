# Exercise · selected catalogue

[Lab](README.md) · [Solution](SOLUTION.md)

Add a wrapper that selects a validated set of exact identities from another catalogue while preserving source order and initial unavailability. Unknown requested identities must not fabricate entries. An empty selection is valid available content.

Copy selected values so a later source mutation cannot alter the wrapper’s previously returned projection. Apply the same contract cases to a valid wrapped source. Do not change the inspector to recognise your class. Explain why wrapping an unstable source does not automatically make future reads stable. The wrapper is not implemented.
