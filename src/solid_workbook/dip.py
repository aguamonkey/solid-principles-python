"""Publication policy owns its contracts; composition supplies implementations."""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ReportArchive(Protocol):
    def save(self, report: str) -> None: ...


class ReportNotifier(Protocol):
    def notify(self, report: str) -> str: ...


class PublicationKind(Enum):
    INVALID = "invalid"
    STORE_UNCONFIRMED = "store-unconfirmed"
    NOTIFY_UNCONFIRMED = "notify-unconfirmed"
    CONFIRMED = "confirmed"


@dataclass(frozen=True)
class Publication:
    kind: PublicationKind
    receipt: str | None = None


def publish(
    report: str, archive: ReportArchive, notifier: ReportNotifier
) -> Publication:
    if not report.strip():
        return Publication(PublicationKind.INVALID)
    try:
        archive.save(report)
    except Exception:
        return Publication(PublicationKind.STORE_UNCONFIRMED)
    try:
        receipt = notifier.notify(report)
    except Exception:
        return Publication(PublicationKind.NOTIFY_UNCONFIRMED)
    return Publication(PublicationKind.CONFIRMED, receipt)
