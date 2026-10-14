# Answer notes · export compatibility

[Prompts](INTERVIEW.md)

1. The loop owns envelopes, identity, lookup and record recovery. A renderer owns payload interpretation and composition chooses registrations. A new identity policy can still justify changing the loop.
2. A familiar format name does not establish familiar payload/output meaning. Exact version matching avoids accidentally reading a new schema as an old one.
3. `bool` subclasses `int`; `isinstance(True, int)` is true. This schema deliberately requires the actual integer type and a positive value.
4. Unsupported means no exact renderer is installed, so payload meaning is not judged. Rejected means the envelope, identity, known payload or renderer output violates a recognised rule.
5. First-valid-envelope identity is independent of registry support. The cost is that a damaged earlier record can block a later valid duplicate. That tradeoff must be explicit.
6. The proxy prevents ordinary mapping writes and captured entries do not track later list edits. Renderer functions can still capture mutable state; frozen output objects are not a general purity guarantee.
7. An operation requiring atomic all-or-nothing effects may need whole-document failure. Independent previews can benefit from partial recovery without claiming delivery success.
8. Installing a renderer makes payload validation possible. An unknown schema was never evidence that its payload was valid, so new support can reveal existing damage.
