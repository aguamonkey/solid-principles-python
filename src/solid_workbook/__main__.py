"""Composition and repeatable local demonstrations; no network or disk writes."""

import argparse

from . import dip, isp, lsp, ocp, srp
from .catalogue_lab.lab import run_lab as run_catalogue_lab
from .export_lab.lab import run_lab as run_export_lab
from .reading_desk.lab import run_lab


class LocalReports:
    def __init__(self) -> None:
        self.reports: list[str] = []

    def save(self, report: str) -> None:
        self.reports.append(report)


class LocalNotifier:
    def notify(self, report: str) -> str:
        return f"Local preview: {report}"


def run(principle: str) -> None:
    if principle == "lsp-lab":
        run_catalogue_lab()
        return
    if principle == "ocp-lab":
        run_export_lab()
        return
    if principle == "srp-lab":
        run_lab()
        return
    if principle in ("all", "srp"):
        notebook = isp.MemoryNotebook()
        reading = srp.record_reading(
            {"station": "North ridge", "kelvin": 281.25}, notebook
        )
        print("SRP /", srp.render_reading(reading))
    if principle in ("all", "ocp"):
        registry = ocp.ExportRegistry()
        registry.register("json", ocp.JsonFormatter())
        print("OCP /", registry.export("json", srp.Reading("North ridge", 281.25)))
    if principle in ("all", "lsp"):
        print(
            "LSP / stable:",
            lsp.inspect_snapshot(lsp.TitleArchive(("Field notes",))),
            "drifting:",
            lsp.inspect_snapshot(lsp.DriftingArchive()),
        )
    if principle in ("all", "isp"):
        notebook = isp.MemoryNotebook()
        notebook.append(srp.Reading("North ridge", 281.25))
        print("ISP /", isp.station_summary(notebook))
    if principle in ("all", "dip"):
        result = dip.publish("North ridge report", LocalReports(), LocalNotifier())
        print("DIP /", result.kind.value, result.receipt)


def main() -> None:
    parser = argparse.ArgumentParser(description="SOLID Python study labs")
    parser.add_argument(
        "principle",
        nargs="?",
        default="all",
        choices=(
            "all",
            "srp",
            "ocp",
            "lsp",
            "isp",
            "dip",
            "srp-lab",
            "ocp-lab",
            "lsp-lab",
        ),
    )
    run(parser.parse_args().principle)


if __name__ == "__main__":
    main()
