from collections.abc import Callable, Iterable
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class Schema:
    format: str
    version: int

    def __post_init__(self) -> None:
        if not isinstance(self.format, str) or not self.format.strip():
            raise ValueError("A format key is required")
        # bool is a subclass of int in Python; it is not a schema version.
        if type(self.version) is not int or self.version <= 0:
            raise ValueError("Version must be a positive integer")


@dataclass(frozen=True)
class ExportPreview:
    label: str
    body: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.label, str)
            or not self.label.strip()
            or not isinstance(self.body, str)
            or not self.body.strip()
        ):
            raise ValueError("Preview requires a useful label and body")


Renderer = Callable[[object], ExportPreview]


@dataclass(frozen=True)
class Registration:
    schema: Schema
    render: Renderer


class VersionedExports:
    def __init__(self, registrations: Iterable[Registration]) -> None:
        captured: dict[Schema, Renderer] = {}
        for registration in registrations:
            schema = Schema(registration.schema.format, registration.schema.version)
            if schema in captured:
                raise ValueError("Duplicate export schema")
            captured[schema] = registration.render
        self._renderers = MappingProxyType(captured)

    def renderer(self, schema: Schema) -> Renderer | None:
        return self._renderers.get(schema)
