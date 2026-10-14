# Solution notes · edit ceiling

[Exercise](EXERCISE.md)

The exercise is not implemented. Add the upper bound after parsing the text into a valid reading in `parse_edit`. Raise the existing validation failure for values above 350 K. Let the desk’s existing edit-invalid branch retain data and avoid the supplier call.

Use a source fixture returning 400 K to demonstrate that source decoding is unchanged. Capture update and snapshot counts before the rejected edit and compare afterwards. Then submit 350 K and verify publication and storage of the acknowledged value.

Do not add the editing ceiling to `Reading.__post_init__`: that would redefine every constructed reading, including source data. Explain separately whether a supplier is allowed to normalise an acknowledgement above the requested bound; the reference contract permits source normalisation and validates acknowledgements against the source domain.
