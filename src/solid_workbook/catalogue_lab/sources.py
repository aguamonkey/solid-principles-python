from collections.abc import Iterable
from dataclasses import dataclass

from .contract import (
    Available,
    CatalogueCard,
    EntryView,
    Snapshot,
    Unavailable,
    copy_entries,
)


class FixedCatalogue:
    def __init__(self, entries: Iterable[EntryView]) -> None:
        self._entries = copy_entries(tuple(entries))

    def snapshot(self) -> Snapshot:
        return Available(self._entries)


class OfflineCatalogue:
    def snapshot(self) -> Snapshot:
        return Unavailable("Catalogue is unavailable in this local fixture.")


class DriftingCatalogue:
    def __init__(self) -> None:
        self._revision = 0

    def snapshot(self) -> Snapshot:
        self._revision += 1
        return Available((CatalogueCard("field-notes", f"Revision {self._revision}"),))


@dataclass
class MutableCard:
    # Mutable attributes structurally satisfy EntryView's read-only properties.
    identity: str
    title: str


class AliasingCatalogue:
    def __init__(self) -> None:
        self._card = MutableCard("field-notes", "Original title")
        self._reads = 0

    def snapshot(self) -> Snapshot:
        self._reads += 1
        if self._reads == 2:
            self._card.title = "Changed title"
        return Available((self._card,))
