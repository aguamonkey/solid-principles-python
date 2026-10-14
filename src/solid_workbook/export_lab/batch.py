from dataclasses import dataclass
from enum import Enum

from .registry import ExportPreview, Schema, VersionedExports


class Outcome(Enum):
    READY = "ready"
    UNSUPPORTED = "unsupported"
    REJECTED = "rejected"


@dataclass(frozen=True)
class PreviewRow:
    index: int
    identity: str | None
    schema: Schema | None
    outcome: Outcome
    reason: str
    preview: ExportPreview | None = None


def preview_batch(raw: object, registry: VersionedExports) -> tuple[PreviewRow, ...]:
    if not isinstance(raw, list):
        raise ValueError("Expected an already-parsed export list")
    rows: list[PreviewRow] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("id"), str)
            or not item["id"].strip()
        ):
            rows.append(
                PreviewRow(index, None, None, Outcome.REJECTED, "Invalid envelope")
            )
            continue
        identity = item["id"]
        try:
            key, version = item.get("format"), item.get("version")
            if not isinstance(key, str) or not isinstance(version, int):
                raise ValueError("Invalid schema fields")
            schema = Schema(key, version)
        except ValueError:
            rows.append(
                PreviewRow(index, identity, None, Outcome.REJECTED, "Invalid envelope")
            )
            continue
        if identity in seen:
            rows.append(
                PreviewRow(
                    index, identity, schema, Outcome.REJECTED, "Duplicate identity"
                )
            )
            continue
        seen.add(identity)
        renderer = registry.renderer(schema)
        if renderer is None:
            rows.append(
                PreviewRow(
                    index,
                    identity,
                    schema,
                    Outcome.UNSUPPORTED,
                    "No exact schema registration",
                )
            )
            continue
        try:
            value = renderer(item.get("payload"))
            if not isinstance(value, ExportPreview):
                raise ValueError("Invalid preview type")
            preview = ExportPreview(value.label, value.body)
        except Exception:
            rows.append(
                PreviewRow(
                    index,
                    identity,
                    schema,
                    Outcome.REJECTED,
                    "Invalid payload or preview",
                )
            )
            continue
        rows.append(
            PreviewRow(
                index, identity, schema, Outcome.READY, "Preview available", preview
            )
        )
    return tuple(rows)
