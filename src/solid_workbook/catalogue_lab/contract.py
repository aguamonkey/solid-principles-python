from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class EntryView(Protocol):
    @property
    def identity(self) -> str: ...
    @property
    def title(self) -> str: ...


@dataclass(frozen=True)
class CatalogueCard:
    identity: str
    title: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.identity, str)
            or not self.identity.strip()
            or not isinstance(self.title, str)
            or not self.title.strip()
        ):
            raise ValueError("Catalogue identity and title must be nonblank strings")


@dataclass(frozen=True)
class Available:
    entries: tuple[EntryView, ...]


@dataclass(frozen=True)
class Unavailable:
    reason: str


Snapshot = Available | Unavailable


class Catalogue(Protocol):
    def snapshot(self) -> Snapshot: ...


class Outcome(Enum):
    PASSED = "passed"
    UNAVAILABLE = "unavailable"
    VIOLATION = "violation"


@dataclass(frozen=True)
class Report:
    outcome: Outcome
    message: str
    before: tuple[CatalogueCard, ...] | None = None
    after: tuple[CatalogueCard, ...] | None = None


def copy_entries(values: object) -> tuple[CatalogueCard, ...]:
    if not isinstance(values, tuple):
        raise ValueError("Snapshot entries must be a tuple")
    cards: list[CatalogueCard] = []
    seen: set[str] = set()
    for entry in values:
        card = CatalogueCard(entry.identity, entry.title)
        if card.identity in seen:
            raise ValueError("Duplicate catalogue identity")
        seen.add(card.identity)
        cards.append(card)
    return tuple(cards)


def inspect_catalogue(source: Catalogue) -> Report:
    before: tuple[CatalogueCard, ...] | None = None
    after: tuple[CatalogueCard, ...] | None = None
    try:
        first = source.snapshot()
        if isinstance(first, Unavailable):
            if not isinstance(first.reason, str) or not first.reason.strip():
                raise ValueError("Unavailability requires a useful reason")
            return Report(Outcome.UNAVAILABLE, first.reason)
        if not isinstance(first, Available):
            raise ValueError("Unknown snapshot outcome")
        before = copy_entries(first.entries)
        second = source.snapshot()
        if copy_entries(first.entries) != before:
            return Report(
                Outcome.VIOLATION,
                "Earlier snapshot changed after another read.",
                before,
            )
        if not isinstance(second, Available):
            return Report(
                Outcome.VIOLATION,
                "A successful snapshot must remain available.",
                before,
            )
        after = copy_entries(second.entries)
        if after != before:
            return Report(
                Outcome.VIOLATION,
                "Repeated snapshots changed ordered content.",
                before,
                after,
            )
        return Report(
            Outcome.PASSED,
            "Stable content and retained snapshot honoured.",
            before,
            after,
        )
    except Exception:
        return Report(
            Outcome.VIOLATION,
            "Supplier threw or returned invalid snapshot data.",
            before,
            after,
        )
