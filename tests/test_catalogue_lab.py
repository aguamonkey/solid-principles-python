import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import Mock

from solid_workbook.catalogue_lab.contract import (
    Available,
    CatalogueCard,
    Outcome,
    Unavailable,
    copy_entries,
    inspect_catalogue,
)
from solid_workbook.catalogue_lab.lab import naive_equal_reads
from solid_workbook.catalogue_lab.sources import (
    AliasingCatalogue,
    DriftingCatalogue,
    FixedCatalogue,
    MutableCard,
    OfflineCatalogue,
)


class FreshCatalogue:
    def snapshot(self):
        return Available((CatalogueCard("one", "Field notes"),))


class CatalogueTests(unittest.TestCase):
    def test_same_caller_contract_for_independent_implementations(self):
        for factory in [
            lambda: FixedCatalogue((CatalogueCard("one", "Field notes"),)),
            FreshCatalogue,
        ]:
            with self.subTest(factory=factory):
                source = factory()
                self.assertEqual(inspect_catalogue(source).outcome, Outcome.PASSED)
                self.assertEqual(inspect_catalogue(source).outcome, Outcome.PASSED)

    def test_empty_success_is_a_valid_available_snapshot(self):
        report = inspect_catalogue(FixedCatalogue(()))
        self.assertEqual(report.outcome, Outcome.PASSED)
        self.assertEqual(report.before, ())

    def test_initial_unavailability_is_permitted(self):
        report = inspect_catalogue(OfflineCatalogue())
        self.assertEqual(report.outcome, Outcome.UNAVAILABLE)
        self.assertIsNone(report.before)

    def test_blank_unavailability_reason_is_a_violation(self):
        source = Mock()
        source.snapshot.return_value = Unavailable(" ")
        self.assertEqual(inspect_catalogue(source).outcome, Outcome.VIOLATION)

    def test_success_then_unavailability_breaks_stability_promise(self):
        source = Mock()
        source.snapshot.side_effect = [
            Available((CatalogueCard("one", "Title"),)),
            Unavailable("Offline"),
        ]
        report = inspect_catalogue(source)
        self.assertEqual(report.outcome, Outcome.VIOLATION)
        self.assertIn("remain available", report.message)

    def test_drifting_content_violates_protocol_promise(self):
        report = inspect_catalogue(DriftingCatalogue())
        self.assertEqual(report.outcome, Outcome.VIOLATION)
        self.assertEqual(report.before[0].title, "Revision 1")
        self.assertEqual(report.after[0].title, "Revision 2")

    def test_aliasing_is_detected_with_unmodified_evidence(self):
        report = inspect_catalogue(AliasingCatalogue())
        self.assertEqual(report.outcome, Outcome.VIOLATION)
        self.assertIn("Earlier snapshot changed", report.message)
        self.assertEqual(report.before[0].title, "Original title")

    def test_naive_comparison_can_falsely_pass_same_bad_behaviour(self):
        self.assertTrue(naive_equal_reads(AliasingCatalogue()))
        self.assertEqual(
            inspect_catalogue(AliasingCatalogue()).outcome, Outcome.VIOLATION
        )

    def test_fixed_constructor_copies_caller_owned_cards(self):
        card = MutableCard("one", "Original")
        source = FixedCatalogue((card,))
        card.title = "Changed outside"
        self.assertEqual(inspect_catalogue(source).before[0].title, "Original")

    def test_constructor_captures_input_collection(self):
        cards = [CatalogueCard("one", "Original")]
        source = FixedCatalogue(cards)
        cards.append(CatalogueCard("two", "Later"))
        self.assertEqual(len(inspect_catalogue(source).before), 1)

    def test_report_cards_prevent_ordinary_reassignment(self):
        report = inspect_catalogue(FreshCatalogue())
        with self.assertRaises(FrozenInstanceError):
            report.before[0].title = "Changed"

    def test_card_domain_requires_nonblank_string_fields(self):
        for identity, title in [
            ("", "Title"),
            ("one", " "),
            (None, "Title"),
            ("one", 1),
        ]:
            with self.assertRaises(ValueError):
                CatalogueCard(identity, title)

    def test_duplicate_identity_rejected_at_construction(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            FixedCatalogue(
                (CatalogueCard("one", "First"), CatalogueCard("one", "Second"))
            )

    def test_provider_duplicate_identity_is_a_violation(self):
        source = Mock()
        source.snapshot.return_value = Available(
            (CatalogueCard("one", "First"), CatalogueCard("one", "Second"))
        )
        self.assertEqual(inspect_catalogue(source).outcome, Outcome.VIOLATION)

    def test_order_is_part_of_snapshot_content(self):
        cards = (CatalogueCard("one", "First"), CatalogueCard("two", "Second"))
        source = Mock()
        source.snapshot.side_effect = [
            Available(cards),
            Available(tuple(reversed(cards))),
        ]
        self.assertEqual(inspect_catalogue(source).outcome, Outcome.VIOLATION)

    def test_identity_is_exact_without_case_or_space_normalisation(self):
        cards = (
            CatalogueCard("one", "First"),
            CatalogueCard("One", "Second"),
            CatalogueCard("one ", "Third"),
        )
        self.assertEqual(
            inspect_catalogue(FixedCatalogue(cards)).outcome, Outcome.PASSED
        )

    def test_unexpected_supplier_exception_is_a_violation(self):
        source = Mock()
        source.snapshot.side_effect = OSError("Private supplier details")
        report = inspect_catalogue(source)
        self.assertEqual(report.outcome, Outcome.VIOLATION)
        self.assertNotIn("Private supplier details", report.message)

    def test_second_read_exception_keeps_captured_evidence(self):
        source = Mock()
        source.snapshot.side_effect = [
            Available((CatalogueCard("one", "Title"),)),
            OSError("Offline"),
        ]
        report = inspect_catalogue(source)
        self.assertEqual(report.outcome, Outcome.VIOLATION)
        self.assertEqual(report.before[0].title, "Title")

    def test_unknown_outcome_is_a_violation(self):
        source = Mock()
        source.snapshot.return_value = {"entries": ()}
        self.assertEqual(inspect_catalogue(source).outcome, Outcome.VIOLATION)

    def test_tuple_container_required_even_if_list_values_look_valid(self):
        source = Mock()
        source.snapshot.return_value = Available([CatalogueCard("one", "Title")])
        self.assertEqual(inspect_catalogue(source).outcome, Outcome.VIOLATION)
        with self.assertRaises(ValueError):
            copy_entries([])

    def test_structurally_readable_mutable_card_can_be_copied(self):
        card = MutableCard("one", "Title")
        captured = copy_entries((card,))
        card.title = "Changed"
        self.assertEqual(captured, (CatalogueCard("one", "Title"),))

    def test_old_snapshot_change_is_detected_even_if_next_output_matches_baseline(self):
        card = MutableCard("one", "Original")

        class HiddenMutation:
            def __init__(self):
                self.reads = 0

            def snapshot(self):
                self.reads += 1
                if self.reads == 1:
                    return Available((card,))
                card.title = "Mutated old output"
                return Available((CatalogueCard("one", "Original"),))

        report = inspect_catalogue(HiddenMutation())
        self.assertEqual(report.outcome, Outcome.VIOLATION)
        self.assertIn("Earlier snapshot changed", report.message)
        self.assertEqual(report.before[0].title, "Original")


if __name__ == "__main__":
    unittest.main()
