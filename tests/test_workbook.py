import unittest

from solid_workbook import dip, isp, lsp, ocp, srp


class WorkbookTests(unittest.TestCase):
    def test_invalid_readings_do_not_write(self):
        notebook = isp.MemoryNotebook()
        for raw in [
            {"station": "A", "kelvin": 10**400},
            None,
            {},
            {"station": "A", "kelvin": True},
            {"station": " ", "kelvin": 1},
            {"station": "A", "kelvin": -1},
            {"station": "A", "kelvin": float("inf")},
            {"station": "A", "kelvin": float("nan")},
        ]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                srp.record_reading(raw, notebook)
        self.assertEqual(notebook.readings(), ())

    def test_zero_kelvin_is_valid(self):
        self.assertEqual(
            srp.decode_reading({"station": "A", "kelvin": 0}), srp.Reading("A", 0)
        )

    def test_input_mutation_does_not_change_saved_reading(self):
        notebook = isp.MemoryNotebook()
        raw = {"station": "A", "kelvin": 281.0}
        reading = srp.record_reading(raw, notebook)
        raw["kelvin"] = 1
        self.assertEqual(notebook.readings(), (reading,))
        self.assertEqual(reading.kelvin, 281.0)

    def test_formatting_does_not_write(self):
        notebook = isp.MemoryNotebook()
        self.assertEqual(srp.render_reading(srp.Reading("A", 281)), "A: 281.00 K")
        self.assertEqual(notebook.readings(), ())

    def test_test_only_format_extends_same_exporter(self):
        class Tsv:
            def format(self, reading):
                return f"{reading.station}\t{reading.kelvin}"

        registry = ocp.ExportRegistry()
        registry.register("tsv", Tsv())
        self.assertEqual(registry.export("tsv", srp.Reading("A", 281)), "A\t281")

    def test_duplicate_and_blank_keys_fail(self):
        registry = ocp.ExportRegistry()
        registry.register("text", ocp.TextFormatter())
        for key in ["text", " "]:
            with self.assertRaises(ValueError):
                registry.register(key, ocp.JsonFormatter())
        self.assertEqual(registry.export("text", srp.Reading("A", 1)), "A: 1.00 K")

    def test_unknown_format_does_not_guess(self):
        registry = ocp.ExportRegistry()
        registry.register("text", ocp.TextFormatter())
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            registry.export("Text", srp.Reading("A", 1))

    def test_snapshot_contract_uses_minimal_fixture(self):
        class Fixture:
            def snapshot(self):
                return ("One", "Two")

        for source in [Fixture(), lsp.TitleArchive(("One",)), lsp.TitleArchive(())]:
            self.assertTrue(lsp.inspect_snapshot(source))

    def test_drifting_snapshot_violates_contract(self):
        self.assertFalse(lsp.inspect_snapshot(lsp.DriftingArchive()))

    def test_blank_snapshot_titles_fail(self):
        with self.assertRaises(ValueError):
            lsp.TitleArchive((" ",))

        class Broken:
            def snapshot(self):
                return ("",)

        self.assertFalse(lsp.inspect_snapshot(Broken()))

    def test_read_only_fixture_needs_no_append(self):
        class Reader:
            def readings(self):
                return (srp.Reading("A", 1), srp.Reading("A", 2), srp.Reading("B", 3))

        self.assertEqual(isp.station_summary(Reader()), {"A": 2, "B": 1})

    def test_notebook_snapshots_do_not_grow_after_append(self):
        notebook = isp.MemoryNotebook()
        notebook.append(srp.Reading("A", 1))
        snapshot = notebook.readings()
        notebook.append(srp.Reading("B", 2))
        self.assertEqual(len(snapshot), 1)
        self.assertEqual(len(notebook.readings()), 2)

    def test_invalid_publication_calls_neither_dependency(self):
        class Trap:
            def save(self, report):
                self.fail()

            def notify(self, report):
                self.fail()

            def fail(self):
                raise AssertionError("Unexpected dependency call")

        self.assertEqual(
            dip.publish(" ", Trap(), Trap()).kind, dip.PublicationKind.INVALID
        )

    def test_publication_calls_archive_before_notifier(self):
        events = []

        class Archive:
            def save(self, report):
                events.append("save")

        class Notifier:
            def notify(self, report):
                events.append("notify")
                return "Preview"

        self.assertEqual(
            dip.publish("Report", Archive(), Notifier()).receipt, "Preview"
        )
        self.assertEqual(events, ["save", "notify"])

    def test_storage_failure_does_not_notify(self):
        class Archive:
            def save(self, report):
                raise OSError("Offline")

        class Notifier:
            def notify(self, report):
                raise AssertionError("Unexpected notify")

        self.assertEqual(
            dip.publish("Report", Archive(), Notifier()).kind,
            dip.PublicationKind.STORE_UNCONFIRMED,
        )

    def test_notification_failure_retains_saved_report(self):
        saved = []

        class Archive:
            def save(self, report):
                saved.append(report)

        class Notifier:
            def notify(self, report):
                raise OSError("No acknowledgement")

        self.assertEqual(
            dip.publish("Report", Archive(), Notifier()).kind,
            dip.PublicationKind.NOTIFY_UNCONFIRMED,
        )
        self.assertEqual(saved, ["Report"])

    def test_storage_can_commit_then_throw(self):
        saved = []

        class Archive:
            def save(self, report):
                saved.append(report)
                raise OSError("Acknowledgement lost")

        class Notifier:
            def notify(self, report):
                raise AssertionError("Unexpected notify")

        result = dip.publish("Report", Archive(), Notifier())
        self.assertEqual(result.kind, dip.PublicationKind.STORE_UNCONFIRMED)
        self.assertEqual(saved, ["Report"])


if __name__ == "__main__":
    unittest.main()
