# Catalogue contracts · structure is not behaviour

[Foundation](../README.md) · [Exercise](EXERCISE.md) · [Solution](SOLUTION.md) · [Interview](INTERVIEW.md) · [Decision](DECISION.md)

Run `PYTHONPATH=src python -m solid_workbook lsp-lab`. A fixed and an empty catalogue pass. An initially unavailable catalogue is permitted. Drifting and aliasing catalogues violate the same caller’s contract.

A successful snapshot promises ordered, uniquely identified, nonblank entries; later sampled reads must succeed with the same content and must not mutate earlier returned snapshots. Initial unavailable is allowed with a useful reason. This contract deliberately excludes changing live catalogues. The backend reader has a different append-only paging contract.

[EntryView](../../../src/solid_workbook/catalogue_lab/contract.py) has read-only properties, but a mutable dataclass can structurally satisfy them. A tuple also does not freeze its contained objects. The naive equality comparison can therefore pass when both reads alias an object that changed.

The inspector copies value evidence before the next supplier call and checks both the retained prior output and newly returned output. See [sources](../../../src/solid_workbook/catalogue_lab/sources.py), [composition](../../../src/solid_workbook/catalogue_lab/lab.py) and the [22 contract tests](../../../tests/test_catalogue_lab.py).

Two reads provide sampled evidence, not a universal proof. Hidden state, transient mutations between observations, malicious properties and nontermination are outside the inspector’s guarantees. It does not restore a mutated source or provide concurrency isolation. Fresh fixtures matter when comparing naive and guarded inspection.
