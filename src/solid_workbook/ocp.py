"""Export bench: a registry extends formatting without editing lookup."""

import json
from typing import Protocol

from .srp import Reading


class Formatter(Protocol):
    def format(self, reading: Reading) -> str: ...


class TextFormatter:
    def format(self, reading: Reading) -> str:
        return f"{reading.station}: {reading.kelvin:.2f} K"


class JsonFormatter:
    def format(self, reading: Reading) -> str:
        return json.dumps(
            {"station": reading.station, "kelvin": reading.kelvin}, sort_keys=True
        )


class ExportRegistry:
    def __init__(self) -> None:
        self._formats: dict[str, Formatter] = {}

    def register(self, key: str, formatter: Formatter) -> None:
        if not key.strip() or key in self._formats:
            raise ValueError("Blank or duplicate format key")
        self._formats[key] = formatter

    def export(self, key: str, reading: Reading) -> str:
        try:
            formatter = self._formats[key]
        except KeyError as error:
            raise ValueError("Unsupported format") from error
        return formatter.format(reading)
