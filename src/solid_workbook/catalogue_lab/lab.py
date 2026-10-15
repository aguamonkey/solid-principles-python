from .contract import Available, Catalogue, CatalogueCard, inspect_catalogue
from .sources import (
    AliasingCatalogue,
    DriftingCatalogue,
    FixedCatalogue,
    OfflineCatalogue,
)


def naive_equal_reads(source: Catalogue) -> bool:
    """Deliberate comparison trap: holding aliases can hide a changed old snapshot."""
    first, second = source.snapshot(), source.snapshot()
    return (
        isinstance(first, Available)
        and isinstance(second, Available)
        and first.entries == second.entries
    )


def run_lab() -> None:
    sources: tuple[tuple[str, Catalogue], ...] = (
        (
            "Fixed catalogue",
            FixedCatalogue((CatalogueCard("field-notes", "Field notes"),)),
        ),
        ("Empty catalogue", FixedCatalogue(())),
        ("Offline catalogue", OfflineCatalogue()),
        ("Drifting catalogue", DriftingCatalogue()),
        ("Aliasing catalogue", AliasingCatalogue()),
    )
    print("ARCHIVE SHELF / CATALOGUE CONTRACT LAB")
    for name, source in sources:
        report = inspect_catalogue(source)
        print(f"{name}: {report.outcome.value} | {report.message}")
        if report.before is not None:
            print("  Captured before:", tuple(card.title for card in report.before))
    print("Naive alias comparison:", naive_equal_reads(AliasingCatalogue()))
    print("Fresh fixtures for each comparison. A matching protocol is not proof.")
