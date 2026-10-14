from dataclasses import dataclass
from enum import Enum

from ..srp import Reading
from .decoding import decode_acknowledgement, decode_snapshot
from .edit_rules import parse_edit
from .ports import ReadingSource, SnapshotWriter


class Notice(Enum):
    IDLE = "idle"
    LOADED = "loaded"
    EMPTY = "empty"
    SOURCE_UNAVAILABLE = "source-unavailable"
    SOURCE_INVALID = "source-invalid"
    NO_READING = "no-reading"
    EDIT_INVALID = "edit-invalid"
    UPDATE_UNCONFIRMED = "update-unconfirmed"
    ACK_INVALID = "ack-invalid"
    SNAPSHOT_UNCONFIRMED = "snapshot-unconfirmed"


@dataclass(frozen=True)
class DeskState:
    reading: Reading | None = None
    notice: Notice = Notice.IDLE


class ReadingDesk:
    """Own synchronous publication and retention, not transport or display."""

    def __init__(self, source: ReadingSource, snapshots: SnapshotWriter) -> None:
        self._source = source
        self._snapshots = snapshots
        self._state = DeskState()

    @property
    def state(self) -> DeskState:
        return self._state

    def _retain(self, notice: Notice) -> DeskState:
        self._state = DeskState(self._state.reading, notice)
        return self._state

    def _publish(self, reading: Reading | None) -> DeskState:
        self._state = DeskState(
            reading, Notice.EMPTY if reading is None else Notice.LOADED
        )
        try:
            self._snapshots.save(reading)
        except Exception:
            # Keep the confirmed source result; snapshot failure is a separate fact.
            self._retain(Notice.SNAPSHOT_UNCONFIRMED)
        return self._state

    def refresh(self) -> DeskState:
        try:
            raw = self._source.fetch()
        except Exception:
            return self._retain(Notice.SOURCE_UNAVAILABLE)
        try:
            reading = decode_snapshot(raw)
        except (ValueError, OverflowError):
            return self._retain(Notice.SOURCE_INVALID)
        return self._publish(reading)

    def edit(self, kelvin_text: str) -> DeskState:
        current = self._state.reading
        if current is None:
            return self._retain(Notice.NO_READING)
        try:
            edited = parse_edit(current, kelvin_text)
        except (ValueError, OverflowError):
            return self._retain(Notice.EDIT_INVALID)
        try:
            raw = self._source.update(edited)
        except Exception:
            # Supplier may have committed before losing its acknowledgement.
            return self._retain(Notice.UPDATE_UNCONFIRMED)
        try:
            acknowledged = decode_acknowledgement(raw, current.station)
        except (ValueError, OverflowError):
            return self._retain(Notice.ACK_INVALID)
        return self._publish(acknowledged)
