"""Field notebook: validation, formatting and storage change independently."""

from dataclasses import dataclass
from math import isfinite
from typing import Protocol


def _valid_kelvin(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return isfinite(value) and value >= 0
    except OverflowError:
        return False


@dataclass(frozen=True)
class Reading:
    station: str
    kelvin: float

    def __post_init__(self) -> None:
        if not isinstance(self.station, str) or not self.station.strip():
            raise ValueError("A station is required")
        if not _valid_kelvin(self.kelvin):
            raise ValueError("Temperature must be finite, nonnegative kelvin")


class ReadingAppender(Protocol):
    def append(self, reading: Reading) -> None: ...


def decode_reading(raw: object) -> Reading:
    if not isinstance(raw, dict):
        raise ValueError("Expected a reading object")
    station, kelvin = raw.get("station"), raw.get("kelvin")
    if (
        not isinstance(station, str)
        or isinstance(kelvin, bool)
        or not isinstance(kelvin, (int, float))
    ):
        raise ValueError("Invalid reading fields")
    try:
        temperature = float(kelvin)
    except OverflowError as error:
        raise ValueError("Temperature cannot be represented") from error
    return Reading(station, temperature)


def record_reading(raw: object, store: ReadingAppender) -> Reading:
    reading = decode_reading(raw)
    store.append(reading)
    return reading


def render_reading(reading: Reading) -> str:
    return f"{reading.station}: {reading.kelvin:.2f} K"
