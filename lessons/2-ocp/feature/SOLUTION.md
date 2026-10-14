# Solution notes · text v2

[Exercise](EXERCISE.md)

The exercise is not implemented. Create a renderer for the v2 fields and register `Schema("text", 2)` beside v1. Map the validated fields into a reading value before formatting; do not reinterpret v1 keys as aliases unless the schema explicitly promises that.

Use an exact v2 registration so the batch loop remains unchanged. Include a valid v2 fixture with `station_id` and `temperature_kelvin`, then retain the bundled legacy-shaped future row as a rejection case. Compare unrelated rows before and after composition.

A new registration makes unsupported data interpretable, not automatically valid. Preserve envelope identity rules and test that a prior unsupported envelope still claims its identity. Discuss a real migration plan separately from rendering support; this local registry does not rewrite or durably reconcile saved records.
