# Solution notes · selection

[Exercise](EXERCISE.md)

The exercise is not implemented. Validate requested identity strings at construction. Propagate initial unavailable; for success, filter in source order and create copied CatalogueCard values. Return a tuple of those values. Use shared cases for order, empty selection, exact matching, prior projection retention and unavailability.

Copying protects older projections from alias mutation. It cannot stop a changing supplier from returning different future content, so the source must still honour the required stability promise or the wrapper must define an explicit capture-at-construction contract instead.
