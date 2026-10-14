import json
import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import Mock

from solid_workbook.export_lab.batch import Outcome, preview_batch
from solid_workbook.export_lab.composition import (
    JSON_V1,
    TEXT_V1,
    compose_exports,
    sample_batch,
)
from solid_workbook.export_lab.registry import (
    ExportPreview,
    Registration,
    Schema,
    VersionedExports,
)


def record(**changes):
    return {
        "id": "one",
        "format": "text",
        "version": 1,
        "payload": {"station": "A", "kelvin": 281},
        **changes,
    }


class ExportLabTests(unittest.TestCase):
    def test_outcomes_preserve_record_order(self):
        rows = preview_batch(sample_batch(), compose_exports(False))
        self.assertEqual([row.index for row in rows], [0, 1, 2, 3, 4])
        self.assertEqual(
            [row.outcome for row in rows],
            [
                Outcome.READY,
                Outcome.UNSUPPORTED,
                Outcome.UNSUPPORTED,
                Outcome.REJECTED,
                Outcome.REJECTED,
            ],
        )

    def test_new_registration_changes_only_its_own_record(self):
        batch = sample_batch()
        before, after = (
            preview_batch(batch, compose_exports(False)),
            preview_batch(batch, compose_exports(True)),
        )
        for index in [0, 2, 3, 4]:
            self.assertEqual(before[index], after[index])
        self.assertEqual(after[1].outcome, Outcome.READY)
        self.assertEqual(
            json.loads(after[1].preview.body), {"station": "South ridge", "kelvin": 290}
        )

    def test_test_only_registration_uses_unchanged_batch_loop(self):
        registry = VersionedExports(
            [
                Registration(
                    Schema("test", 1), lambda raw: ExportPreview("Test", "Local output")
                )
            ]
        )
        row = preview_batch([record(format="test")], registry)[0]
        self.assertEqual(row.outcome, Outcome.READY)
        self.assertEqual(row.preview.body, "Local output")

    def test_duplicate_schema_rejects_composition(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            VersionedExports([TEXT_V1, TEXT_V1])

    def test_versions_require_actual_positive_integers(self):
        for version in [True, False, 1.0, 0, -1, "1", None]:
            with self.subTest(version=version), self.assertRaises(ValueError):
                Schema("text", version)
        self.assertEqual(Schema("text", 10**100).version, 10**100)

    def test_format_keys_must_be_nonblank_strings(self):
        for key in [None, 1, ""]:
            with self.assertRaises(ValueError):
                Schema(key, 1)
        with self.assertRaises(ValueError):
            Schema(" ", 1)

    def test_registration_collection_mutation_does_not_add_support(self):
        registrations = [TEXT_V1]
        registry = VersionedExports(registrations)
        registrations.append(JSON_V1)
        self.assertIsNone(registry.renderer(Schema("json", 1)))

    def test_distinct_versions_can_coexist(self):
        registry = VersionedExports(
            [
                TEXT_V1,
                Registration(
                    Schema("text", 2),
                    lambda raw: ExportPreview("V2", "Different meaning"),
                ),
            ]
        )
        rows = preview_batch([record(), record(id="two", version=2)], registry)
        self.assertEqual([row.preview.label for row in rows], ["Text v1", "V2"])

    def test_future_version_never_falls_back(self):
        render = Mock(return_value=ExportPreview("Test", "Body"))
        registry = VersionedExports([Registration(Schema("text", 1), render)])
        self.assertEqual(
            preview_batch([record(version=2)], registry)[0].outcome, Outcome.UNSUPPORTED
        )
        render.assert_not_called()

    def test_unknown_format_does_not_decode_damaged_payload(self):
        row = preview_batch(
            [record(format="future", payload=None)], compose_exports(False)
        )[0]
        self.assertEqual(row.outcome, Outcome.UNSUPPORTED)

    def test_lookup_is_exact_and_case_sensitive(self):
        for key in ["Text", " text", "text "]:
            self.assertEqual(
                preview_batch([record(format=key)], compose_exports(False))[0].outcome,
                Outcome.UNSUPPORTED,
            )

    def test_invalid_envelopes_are_rejected_without_claiming_identity(self):
        for value in [
            None,
            [],
            {},
            record(id=" "),
            record(format=None),
            record(version=True),
            record(version=1.0),
        ]:
            rows = preview_batch([value, record()], compose_exports(False))
            self.assertEqual(rows[0].reason, "Invalid envelope")
            self.assertEqual(rows[1].outcome, Outcome.READY)

    def test_unsupported_record_still_claims_valid_identity(self):
        rows = preview_batch(
            [record(format="future"), record()], compose_exports(False)
        )
        self.assertEqual(rows[1].reason, "Duplicate identity")

    def test_damaged_known_payload_claims_valid_identity(self):
        rows = preview_batch([record(payload=None), record()], compose_exports(False))
        self.assertEqual(rows[0].outcome, Outcome.REJECTED)
        self.assertEqual(rows[1].reason, "Duplicate identity")

    def test_damaged_record_does_not_hide_later_valid_preview(self):
        rows = preview_batch(
            [record(payload=None), record(id="two")], compose_exports(False)
        )
        self.assertEqual(rows[1].outcome, Outcome.READY)

    def test_payload_rules_reject_booleans_strings_and_nonfinite_kelvin(self):
        for value in [True, "281", -1, float("nan"), float("inf"), 10**400]:
            row = preview_batch(
                [record(payload={"station": "A", "kelvin": value})],
                compose_exports(False),
            )[0]
            self.assertEqual(row.outcome, Outcome.REJECTED)

    def test_renderer_exception_is_contained_to_its_record(self):
        def broken(raw):
            raise RuntimeError("Private supplier details")

        rows = preview_batch(
            [record(format="broken"), record(id="two")],
            VersionedExports([TEXT_V1, Registration(Schema("broken", 1), broken)]),
        )
        self.assertEqual(rows[0].reason, "Invalid payload or preview")
        self.assertEqual(rows[1].outcome, Outcome.READY)

    def test_preview_fields_require_nonblank_strings(self):
        for label, body in [("", "Body"), ("Label", " "), (1, "Body"), ("Label", None)]:
            with self.assertRaises(ValueError):
                ExportPreview(label, body)

    def test_preview_output_is_copied_and_frozen(self):
        value = ExportPreview("Test", "Original")
        registry = VersionedExports(
            [Registration(Schema("text", 1), lambda raw: value)]
        )
        row = preview_batch([record()], registry)[0]
        object.__setattr__(value, "body", "Changed")
        self.assertEqual(row.preview.body, "Original")
        with self.assertRaises(FrozenInstanceError):
            row.preview.body = "Change"

    def test_invalid_renderer_output_is_rejected(self):
        registry = VersionedExports(
            [Registration(Schema("text", 1), lambda raw: {"body": "Wrong type"})]
        )
        self.assertEqual(
            preview_batch([record()], registry)[0].outcome, Outcome.REJECTED
        )

    def test_batch_does_not_mutate_the_input(self):
        batch = sample_batch()
        before = json.dumps(batch, sort_keys=True)
        preview_batch(batch, compose_exports(True))
        self.assertEqual(json.dumps(batch, sort_keys=True), before)

    def test_document_boundary_distinguishes_empty_from_non_list(self):
        self.assertEqual(preview_batch([], compose_exports(False)), ())
        for value in [None, {}, (), "[]"]:
            with self.assertRaises(ValueError):
                preview_batch(value, compose_exports(False))


if __name__ == "__main__":
    unittest.main()
