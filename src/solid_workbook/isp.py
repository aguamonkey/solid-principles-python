"""Station board: a reader does not need append operations."""

from typing import Protocol

from .srp import Reading, ReadingAppender


class ReadingReader(Protocol):
    def readings(self) -> tuple[Reading, ...]: ...


class NotebookPort(ReadingReader, ReadingAppender, Protocol):
    """A use case needing both operations can compose both requirements."""


class MemoryNotebook:
    def __init__(self) -> None:
        self._readings: list[Reading] = []

    def append(self, reading: Reading) -> None:
        self._readings.append(reading)

    def readings(self) -> tuple[Reading, ...]:
        return tuple(self._readings)


def station_summary(reader: ReadingReader) -> dict[str, int]:
    counts: dict[str, int] = {}
    for reading in reader.readings():
        counts[reading.station] = counts.get(reading.station, 0) + 1
    return counts
