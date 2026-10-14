from ..srp import Reading, decode_reading


def decode_snapshot(raw: object) -> Reading | None:
    return None if raw is None else decode_reading(raw)


def decode_acknowledgement(raw: object, station: str) -> Reading:
    reading = decode_reading(raw)
    if reading.station != station:
        raise ValueError("Acknowledgement identifies a different station")
    return reading
