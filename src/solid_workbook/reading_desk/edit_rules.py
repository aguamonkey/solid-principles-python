from ..srp import Reading


def parse_edit(current: Reading, kelvin_text: str) -> Reading:
    # Form input is text; source payloads have their own runtime decoder.
    try:
        value = float(kelvin_text)
    except (ValueError, OverflowError) as error:
        raise ValueError("Enter a numeric temperature") from error
    return Reading(current.station, value)
