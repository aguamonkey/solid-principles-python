from .adapters import MemorySnapshots, SampleReadingSource, SourceMode
from .policy import ReadingDesk
from .presentation import render_state


def run_lab() -> None:
    source, snapshots = SampleReadingSource(), MemorySnapshots()
    desk = ReadingDesk(source, snapshots)
    print("FIELD NOTEBOOK / SRP RECOVERY LAB")
    print("01 Load:", render_state(desk.refresh()))
    source.mode = SourceMode.OFFLINE
    print("02 Offline refresh:", render_state(desk.refresh()))
    source.mode = SourceMode.AVAILABLE
    print("03 Recover:", render_state(desk.refresh()))
    print("04 Invalid edit:", render_state(desk.edit("warm")))
    source.mode = SourceMode.LOST_UPDATE_ACK
    print("05 Lost update acknowledgement:", render_state(desk.edit("282")))
    source.mode = SourceMode.AVAILABLE
    print("06 Reconcile:", render_state(desk.refresh()))
    snapshots.fail = True
    print("07 Snapshot failure:", render_state(desk.edit("283")))
    snapshots.fail = False
    print("08 Recover snapshot:", render_state(desk.refresh()))
    print(f"Source updates: {source.updates}; snapshot writes: {snapshots.writes}")
    print("Local memory only. No network, disk storage or asynchronous requests.")
