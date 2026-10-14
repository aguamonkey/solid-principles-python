import unittest
from unittest.mock import Mock

from solid_workbook.reading_desk.adapters import (
    MemorySnapshots,
    SampleReadingSource,
    SourceMode,
)
from solid_workbook.reading_desk.decoding import decode_snapshot
from solid_workbook.reading_desk.edit_rules import parse_edit
from solid_workbook.reading_desk.policy import Notice, ReadingDesk
from solid_workbook.reading_desk.presentation import render_state
from solid_workbook.srp import Reading


class ReadingDeskTests(unittest.TestCase):
    def setUp(self):
        self.source = SampleReadingSource()
        self.snapshots = MemorySnapshots()
        self.desk = ReadingDesk(self.source, self.snapshots)

    def test_successful_load_publishes_and_snapshots(self):
        state = self.desk.refresh()
        self.assertEqual(state.notice, Notice.LOADED)
        self.assertEqual(state.reading, self.source.reading)
        self.assertEqual(self.snapshots.latest, state.reading)

    def test_failed_first_load_remains_empty_without_snapshot_write(self):
        self.source.mode = SourceMode.OFFLINE
        self.assertEqual(self.desk.refresh().notice, Notice.SOURCE_UNAVAILABLE)
        self.assertIsNone(self.desk.state.reading)
        self.assertEqual(self.snapshots.writes, 0)

    def test_offline_refresh_retains_confirmed_reading_and_snapshot(self):
        before = self.desk.refresh().reading
        writes = self.snapshots.writes
        self.source.mode = SourceMode.OFFLINE
        self.assertEqual(self.desk.refresh().reading, before)
        self.assertEqual(self.snapshots.latest, before)
        self.assertEqual(self.snapshots.writes, writes)

    def test_malformed_refresh_retains_confirmed_reading(self):
        before = self.desk.refresh().reading
        self.source.mode = SourceMode.MALFORMED
        state = self.desk.refresh()
        self.assertEqual(state.notice, Notice.SOURCE_INVALID)
        self.assertEqual(state.reading, before)
        self.assertEqual(self.snapshots.writes, 1)

    def test_successful_empty_result_clears_visible_reading_and_snapshot(self):
        self.desk.refresh()
        self.source.reading = None
        self.assertEqual(self.desk.refresh().notice, Notice.EMPTY)
        self.assertIsNone(self.desk.state.reading)
        self.assertIsNone(self.snapshots.latest)

    def test_recovery_replaces_reading_and_clears_failure_notice(self):
        self.desk.refresh()
        self.source.mode = SourceMode.OFFLINE
        self.desk.refresh()
        self.source.mode = SourceMode.AVAILABLE
        self.source.reading = Reading("South ridge", 290)
        state = self.desk.refresh()
        self.assertEqual(state.notice, Notice.LOADED)
        self.assertEqual(state.reading.station, "South ridge")

    def test_edit_without_reading_never_calls_source(self):
        self.assertEqual(self.desk.edit("282").notice, Notice.NO_READING)
        self.assertEqual(self.source.updates, 0)

    def test_invalid_edits_never_call_update_or_write_snapshot(self):
        before = self.desk.refresh().reading
        for text in ["", "warm", "-1", "NaN", "Infinity", "1e999"]:
            with self.subTest(text=text):
                self.assertEqual(self.desk.edit(text).notice, Notice.EDIT_INVALID)
                self.assertEqual(self.desk.state.reading, before)
        self.assertEqual(self.source.updates, 0)
        self.assertEqual(self.snapshots.writes, 1)

    def test_valid_edit_preserves_station_and_publishes_acknowledgement(self):
        self.desk.refresh()
        state = self.desk.edit("282.5")
        self.assertEqual(state.reading, Reading("North ridge", 282.5))
        self.assertEqual(self.snapshots.latest, state.reading)
        self.assertEqual(self.source.updates, 1)

    def test_supplier_normalisation_is_allowed_for_same_station(self):
        source = Mock()
        source.fetch.return_value = {"station": "A", "kelvin": 281}
        source.update.return_value = {"station": "A", "kelvin": 282.0}
        desk = ReadingDesk(source, self.snapshots)
        desk.refresh()
        self.assertEqual(desk.edit("282.04").reading, Reading("A", 282.0))
        source.update.assert_called_once_with(Reading("A", 282.04))

    def test_wrong_station_ack_retains_previous_visible_reading(self):
        before = self.desk.refresh().reading
        self.source.mode = SourceMode.WRONG_STATION_ACK
        self.assertEqual(self.desk.edit("282").notice, Notice.ACK_INVALID)
        self.assertEqual(self.desk.state.reading, before)
        self.assertEqual(self.snapshots.writes, 1)
        self.assertEqual(self.source.reading.kelvin, 282)

    def test_malformed_ack_is_not_published(self):
        source = Mock()
        source.fetch.return_value = {"station": "A", "kelvin": 281}
        desk = ReadingDesk(source, self.snapshots)
        desk.refresh()
        for value in [
            None,
            {},
            {"station": "A", "kelvin": True},
            {"station": "A", "kelvin": float("nan")},
        ]:
            source.update.return_value = value
            self.assertEqual(desk.edit("282").notice, Notice.ACK_INVALID)
            self.assertEqual(desk.state.reading, Reading("A", 281))
        self.assertEqual(self.snapshots.writes, 1)

    def test_update_failure_before_commit_retains_confirmed_data(self):
        before = self.desk.refresh().reading
        self.source.mode = SourceMode.OFFLINE
        self.assertEqual(self.desk.edit("282").notice, Notice.UPDATE_UNCONFIRMED)
        self.assertEqual(self.desk.state.reading, before)
        self.assertEqual(self.source.reading, before)

    def test_lost_update_ack_can_commit_and_refresh_reconciles(self):
        before = self.desk.refresh().reading
        self.source.mode = SourceMode.LOST_UPDATE_ACK
        self.assertEqual(self.desk.edit("282").notice, Notice.UPDATE_UNCONFIRMED)
        self.assertEqual(self.desk.state.reading, before)
        self.assertEqual(self.source.reading, Reading("North ridge", 282))
        self.source.mode = SourceMode.AVAILABLE
        self.assertEqual(self.desk.refresh().reading, self.source.reading)
        self.assertEqual(self.desk.state.notice, Notice.LOADED)

    def test_snapshot_failure_keeps_confirmed_source_result(self):
        self.desk.refresh()
        old_snapshot = self.snapshots.latest
        self.snapshots.fail = True
        state = self.desk.edit("282")
        self.assertEqual(state.notice, Notice.SNAPSHOT_UNCONFIRMED)
        self.assertEqual(state.reading, Reading("North ridge", 282))
        self.assertEqual(self.snapshots.latest, old_snapshot)
        self.assertEqual(self.source.reading, state.reading)

    def test_snapshot_can_write_then_raise_without_reverting_source(self):
        class LostAck:
            def __init__(self):
                self.latest = None

            def save(self, reading):
                self.latest = reading
                raise OSError("Lost ack")

        store = LostAck()
        desk = ReadingDesk(self.source, store)
        state = desk.refresh()
        self.assertEqual(state.notice, Notice.SNAPSHOT_UNCONFIRMED)
        self.assertEqual(store.latest, state.reading)

    def test_empty_source_stays_empty_even_if_snapshot_clear_fails(self):
        self.desk.refresh()
        self.source.reading = None
        self.snapshots.fail = True
        state = self.desk.refresh()
        self.assertIsNone(state.reading)
        self.assertEqual(state.notice, Notice.SNAPSHOT_UNCONFIRMED)
        self.assertIsNotNone(self.snapshots.latest)

    def test_rendering_does_not_call_source_or_snapshot(self):
        state = self.desk.refresh()
        writes = self.snapshots.writes
        self.assertIn("281.25 K", render_state(state))
        self.assertEqual(self.snapshots.writes, writes)
        self.assertEqual(self.source.updates, 0)

    def test_form_parser_does_not_redefine_numeric_source_decoder(self):
        self.assertEqual(parse_edit(Reading("A", 281), "282"), Reading("A", 282))
        with self.assertRaises(ValueError):
            decode_snapshot({"station": "A", "kelvin": "282"})
        self.assertEqual(
            decode_snapshot({"station": "A", "kelvin": 400}), Reading("A", 400)
        )

    def test_snapshot_is_not_read_to_bootstrap_a_new_desk(self):
        self.snapshots.latest = Reading("Old", 280)
        self.assertIsNone(ReadingDesk(self.source, self.snapshots).state.reading)


if __name__ == "__main__":
    unittest.main()
