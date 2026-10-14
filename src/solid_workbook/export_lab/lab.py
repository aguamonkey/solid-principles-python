from .batch import preview_batch
from .composition import compose_exports, sample_batch


def run_lab() -> None:
    batch = sample_batch()
    print("EXPORT BENCH / VERSIONED COMPATIBILITY LAB")
    for include_json in (False, True):
        print("\nJSON extension:", "included" if include_json else "absent")
        for row in preview_batch(batch, compose_exports(include_json)):
            detail = row.preview.body if row.preview else row.reason
            print(f"{row.index + 1:02} {row.identity}: {row.outcome.value} | {detail}")
    print("\nJSON changes its own record; other outcomes stay unchanged.")
    print("Local previews only. No files are written and no services are contacted.")
