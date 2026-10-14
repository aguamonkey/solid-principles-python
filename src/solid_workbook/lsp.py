"""Archive shelf: snapshots promise stable, immutable, nonblank titles."""

from typing import Protocol


class SnapshotSource(Protocol):
    def snapshot(self) -> tuple[str, ...]: ...


class TitleArchive:
    def __init__(self, titles: tuple[str, ...]) -> None:
        if any(not isinstance(title, str) or not title.strip() for title in titles):
            raise ValueError("Titles must be nonblank strings")
        self._titles = tuple(titles)

    def snapshot(self) -> tuple[str, ...]:
        return self._titles


class DriftingArchive:
    """Deliberate violation: the structural signature hides unstable content."""

    def __init__(self) -> None:
        self._revision = 0

    def snapshot(self) -> tuple[str, ...]:
        self._revision += 1
        return (f"Revision {self._revision}",)


def inspect_snapshot(source: SnapshotSource) -> bool:
    first, second = source.snapshot(), source.snapshot()
    return (
        isinstance(first, tuple)
        and isinstance(second, tuple)
        and all(isinstance(title, str) and bool(title.strip()) for title in first)
        and first == second
    )
