import json

from ..srp import decode_reading, render_reading
from .registry import ExportPreview, Registration, Schema, VersionedExports


def render_text_v1(raw: object) -> ExportPreview:
    return ExportPreview("Text v1", render_reading(decode_reading(raw)))


def render_json_v1(raw: object) -> ExportPreview:
    reading = decode_reading(raw)
    body = json.dumps(
        {"station": reading.station, "kelvin": reading.kelvin}, sort_keys=True
    )
    return ExportPreview("JSON v1", body)


TEXT_V1 = Registration(Schema("text", 1), render_text_v1)
JSON_V1 = Registration(Schema("json", 1), render_json_v1)


def compose_exports(include_json: bool) -> VersionedExports:
    return VersionedExports([TEXT_V1, JSON_V1] if include_json else [TEXT_V1])


def sample_batch() -> list[object]:
    return [
        {
            "id": "north",
            "format": "text",
            "version": 1,
            "payload": {"station": "North ridge", "kelvin": 281.25},
        },
        {
            "id": "south",
            "format": "json",
            "version": 1,
            "payload": {"station": "South ridge", "kelvin": 290},
        },
        {
            "id": "future",
            "format": "text",
            "version": 2,
            "payload": {"station": "Future ridge", "kelvin": 280},
        },
        {
            "id": "damaged",
            "format": "text",
            "version": 1,
            "payload": {"station": "Broken ridge", "kelvin": "warm"},
        },
        {
            "id": "north",
            "format": "text",
            "version": 1,
            "payload": {"station": "Duplicate", "kelvin": 281},
        },
    ]
