from enum import Enum

from ..srp import Reading


class SourceMode(Enum):
    AVAILABLE = "available"
    OFFLINE = "offline"
    MALFORMED = "malformed"
    LOST_UPDATE_ACK = "lost-update-ack"
    WRONG_STATION_ACK = "wrong-station-ack"


class SampleReadingSource:
    def __init__(self) -> None:
        self.reading: Reading | None = Reading("North ridge", 281.25)
        self.mode = SourceMode.AVAILABLE
        self.updates = 0

    def fetch(self) -> object:
        if self.mode is SourceMode.OFFLINE:
            raise OSError("Sample source unavailable")
        if self.mode is SourceMode.MALFORMED:
            return {"station": "North ridge", "kelvin": "warm"}
        return self._payload(self.reading)

    def update(self, reading: Reading) -> object:
        if self.mode is SourceMode.OFFLINE:
            raise OSError("Sample source unavailable")
        self.updates += 1
        self.reading = reading
        if self.mode is SourceMode.LOST_UPDATE_ACK:
            raise OSError("Acknowledgement lost after update")
        if self.mode is SourceMode.WRONG_STATION_ACK:
            return {"station": "Other station", "kelvin": reading.kelvin}
        return self._payload(reading)

    @staticmethod
    def _payload(reading: Reading | None) -> object:
        return (
            None
            if reading is None
            else {"station": reading.station, "kelvin": reading.kelvin}
        )


class MemorySnapshots:
    def __init__(self) -> None:
        self.latest: Reading | None = None
        self.fail = False
        self.writes = 0

    def save(self, reading: Reading | None) -> None:
        if self.fail:
            raise OSError("Snapshot unavailable")
        self.latest = reading
        self.writes += 1
