from ..srp import render_reading
from .policy import DeskState, Notice

MESSAGES = {
    Notice.IDLE: "No source request yet.",
    Notice.LOADED: "Source reading confirmed.",
    Notice.EMPTY: "Source confirmed an empty result.",
    Notice.SOURCE_UNAVAILABLE: "Refresh failed; last confirmed reading retained.",
    Notice.SOURCE_INVALID: "Invalid source data; last confirmed reading retained.",
    Notice.NO_READING: "Load a reading before editing.",
    Notice.EDIT_INVALID: "Invalid edit; source was not called.",
    Notice.UPDATE_UNCONFIRMED: "Update unconfirmed; refresh to reconcile.",
    Notice.ACK_INVALID: "Invalid acknowledgement; last confirmed reading retained.",
    Notice.SNAPSHOT_UNCONFIRMED: "Source confirmed; snapshot write is unconfirmed.",
}


def render_state(state: DeskState) -> str:
    value = render_reading(state.reading) if state.reading else "No reading"
    return f"{value} | {MESSAGES[state.notice]}"
