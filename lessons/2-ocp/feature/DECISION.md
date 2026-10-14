# Decision · exact schema lookup and per-record recovery

[Lab](README.md)

## Pressure

A workbook release can recognise some export recipes while an extension introduces another format or payload meaning. One unknown or damaged record should not prevent familiar previews from being useful.

## Decision

Capture registrations keyed by exact format/version at composition. The batch policy validates envelopes and identity, then invokes only an exact renderer. Renderers own payload rules. Return ready, unsupported and rejected separately, preserving order and copying accepted projections.

First valid envelope wins its identity even when unsupported or damaged. This avoids registry installation silently changing which duplicate is considered authoritative. It also means a damaged earlier record blocks a later duplicate; that is a chosen policy, not automatic repair.

## Alternatives

- Fall back from v2 to v1: risks interpreting changed meaning as familiar data.
- Add format branches to the batch loop: couples a stable recovery algorithm to every renderer release.
- Fail the entire list: simpler and possibly appropriate for an atomic operation, but hides useful independent previews in this screenless study lab.
- Last duplicate wins: a different reconciliation policy with its own ordering and compatibility consequences.
- Deeply sandbox extension code: a much larger runtime boundary; typed callables and frozen values do not provide that isolation.

## Consequences

Adding a registration changes only records with that exact key unless the identity policy links them. Successful previewing has no delivery side effects. A production workflow needs bounded inputs, diagnostics, durable schema handling and explicit rollout requirements. Interfaces and registration do not establish those guarantees.
