from typing import Protocol

from ..srp import Reading


class ReadingSource(Protocol):
    def fetch(self) -> object: ...
    def update(self, reading: Reading) -> object: ...


class SnapshotWriter(Protocol):
    def save(self, reading: Reading | None) -> None: ...
