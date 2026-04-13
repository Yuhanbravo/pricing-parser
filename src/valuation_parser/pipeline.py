from __future__ import annotations

from pathlib import Path

from valuation_parser.adapter_registry import build_registry, get_adapter
from valuation_parser.exporters import write_positions, write_routing_results, write_subjects, write_summary
from valuation_parser.mapping_loader import load_mapping
from valuation_parser.models import ParseArtifacts
from valuation_parser.product_identity import extract_product_identity, preview_workbook
from valuation_parser.routing import route_identity

SUPPORTED_INPUT_EXTENSIONS = {".csv", ".xls", ".xlsx"}


def run_pipeline(
    input_path: str | Path,
    mapping_path: str | Path,
    output_dir: str | Path,
    *,
    summary_path: str | Path | None = None,
    adapter_override: str | None = None,
    fail_on_routing_error: bool = False,
    include_inactive_mapping: bool = False,
) -> dict[str, Path]:
    input_root = Path(input_path)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    mapping = load_mapping(mapping_path, include_inactive=include_inactive_mapping)
    registry = build_registry()

    source_files = list(_iter_input_files(input_root))
    artifacts: list[ParseArtifacts] = []

    for source_file in source_files:
        preview = preview_workbook(source_file)
        identity = extract_product_identity(source_file, preview=preview)
        route = route_identity(str(source_file), identity, mapping, adapter_override=adapter_override)
        if route.route_status != "success":
            artifacts.append(ParseArtifacts(route=route))
            if fail_on_routing_error:
                raise RuntimeError(f"Routing failed for {source_file}: {route.route_message}")
            continue

        adapter = get_adapter(route.adapter_key or "generic", registry)
        artifacts.append(adapter.parse(source_file, route))

    routing_path = output_root / "routing_results.csv"
    subjects_path = output_root / "valuation_subjects.csv"
    positions_path = output_root / "valuation_positions.csv"
    summary_output = Path(summary_path) if summary_path else output_root / "parse_summary.md"

    routes = [artifact.route for artifact in artifacts]
    subjects = [subject for artifact in artifacts for subject in artifact.subjects]
    positions = [position for artifact in artifacts for position in artifact.positions]

    write_routing_results(routing_path, routes)
    write_subjects(subjects_path, subjects)
    write_positions(positions_path, positions)
    write_summary(summary_output, files_processed=len(source_files), routes=routes, subjects=subjects, positions=positions)

    return {
        "routing_results": routing_path,
        "valuation_subjects": subjects_path,
        "valuation_positions": positions_path,
        "parse_summary": summary_output,
    }


def _iter_input_files(input_root: Path):
    if input_root.is_file():
        if input_root.suffix.lower() in SUPPORTED_INPUT_EXTENSIONS:
            yield input_root
        return

    for candidate in sorted(input_root.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_INPUT_EXTENSIONS:
            yield candidate
