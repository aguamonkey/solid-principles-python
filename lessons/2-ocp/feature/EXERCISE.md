# Exercise · support text v2 without guessing

[Lab](README.md) · [Solution notes](SOLUTION.md)

Add a text v2 registration whose payload requires `station_id` and numeric `temperature_kelvin`. Use the same reading domain for finite nonnegative kelvin, then produce a nonblank text preview. Keep text v1 unchanged.

Add the registration at composition without editing the batch loop or adding a version branch there. Test coexistence of v1/v2, correct v2 input, invalid v2 input, booleans, duplicate composition and unchanged outcomes for unrelated records.

The bundled future row currently contains v1-shaped fields tagged as v2. Leave that row unchanged: after installing your v2 adapter, it should move from unsupported to rejected. Add a separate valid v2 record to prove actual new support. An unsupported schema never promised a valid payload.

Run the README checks and `ocp-lab`. Explain why exact version lookup protects payload meaning, and why new support can reveal existing damage. This exercise is intentionally not implemented.
