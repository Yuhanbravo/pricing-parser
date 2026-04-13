from __future__ import annotations

import csv
from pathlib import Path

from valuation_parser.models import PositionRecord, RouteDecision, SubjectRecord

ROUTING_FIELDS = [
    "source_file",
    "product_id",
    "association_code",
    "custodian_name_chinese",
    "custodian_id",
    "custodian_name",
    "adapter_key",
    "route_source",
    "route_status",
    "route_message",
]

SUBJECT_FIELDS = [
    "source_file",
    "sheet_name",
    "valuation_date",
    "product_id",
    "association_code",
    "custodian_id",
    "custodian_name",
    "adapter_key",
    "route_source",
    "subject_code",
    "subject_name",
    "parent_subject_code",
    "subject_level",
    "is_leaf",
    "quantity",
    "unit_cost",
    "cost",
    "market_price",
    "market_value",
    "pnl",
    "raw_row_index",
    "raw_text",
]

POSITION_FIELDS = [
    "source_file",
    "sheet_name",
    "valuation_date",
    "product_id",
    "association_code",
    "custodian_id",
    "custodian_name",
    "adapter_key",
    "route_source",
    "instrument_name",
    "instrument_code_raw",
    "instrument_code_std",
    "exchange",
    "asset_type",
    "quantity",
    "unit_cost",
    "cost",
    "market_price",
    "market_value",
    "unrealized_pnl",
    "subject_code",
    "subject_name",
    "review_flag",
]


def write_routing_results(path: Path, routes: list[RouteDecision]) -> None:
    rows = [route.to_row() for route in routes]
    _write_csv(path, ROUTING_FIELDS, rows)


def write_subjects(path: Path, subjects: list[SubjectRecord]) -> None:
    rows = [subject.to_row() for subject in subjects]
    _write_csv(path, SUBJECT_FIELDS, rows)


def write_positions(path: Path, positions: list[PositionRecord]) -> None:
    rows = [position.to_row() for position in positions]
    _write_csv(path, POSITION_FIELDS, rows)


def write_summary(path: Path, *, files_processed: int, routes: list[RouteDecision], subjects: list[SubjectRecord], positions: list[PositionRecord]) -> None:
    success_count = sum(1 for route in routes if route.route_status == "success")
    failure_count = sum(1 for route in routes if route.route_status != "success")
    manual_override_count = sum(1 for route in routes if route.route_source == "manual_override")
    review_count = sum(1 for position in positions if position.review_flag)
    adapter_keys = sorted({route.adapter_key for route in routes if route.adapter_key})

    content = "\n".join(
        [
            "# Parse Summary",
            "",
            f"- Processed files: {files_processed}",
            f"- Successful routes: {success_count}",
            f"- Manual overrides: {manual_override_count}",
            f"- Routing failures: {failure_count}",
            f"- Supported adapters in run: {', '.join(adapter_keys) if adapter_keys else 'none'}",
            f"- Subject rows exported: {len(subjects)}",
            f"- Position rows exported: {len(positions)}",
            f"- Review flagged positions: {review_count}",
        ]
    )
    path.write_text(content + "\n", encoding="utf-8")


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object | None]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
