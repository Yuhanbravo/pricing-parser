from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook

from valuation_parser.models import PositionRecord, ReviewItem, RouteDecision, SubjectRecord

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
    "broker",
    "sheet_name",
    "valuation_date",
    "raw_row_index",
    "subject_code",
    "subject_name",
    "parent_subject_code",
    "subject_level",
    "root_subject_code",
    "root_subject_name",
    "is_leaf",
    "is_position_candidate",
    "quantity",
    "unit_cost",
    "cost",
    "cost_pct_nav",
    "market_price",
    "market_value",
    "market_value_pct_nav",
    "pnl",
    "suspension_info",
    "raw_text",
]

POSITION_FIELDS = [
    "broker",
    "sheet_name",
    "valuation_date",
    "raw_row_index",
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
    "suspension_info",
    "review_flag",
    "review_note",
]

REVIEW_FIELDS = [
    "broker",
    "valuation_date",
    "raw_row_index",
    "subject_code",
    "subject_name",
    "quantity",
    "cost",
    "market_value",
    "pnl",
    "review_reason",
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


def write_review_items(path: Path, review_items: list[ReviewItem]) -> None:
    rows = [review_item.to_row() for review_item in review_items]
    _write_csv(path, REVIEW_FIELDS, rows)


def write_summary(path: Path, *, files_processed: int, routes: list[RouteDecision], subjects: list[SubjectRecord], positions: list[PositionRecord], review_items: list[ReviewItem]) -> None:
    success_count = sum(1 for route in routes if route.route_status == "success")
    failure_count = sum(1 for route in routes if route.route_status != "success")
    manual_override_count = sum(1 for route in routes if route.route_source == "manual_override")
    review_count = sum(1 for position in positions if position.review_flag)
    review_item_count = len(review_items)
    normalization_issue_count = sum(1 for position in positions if position.review_flag in {"missing_code", "unknown_exchange", "unknown_asset_type"})
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
            f"- Review items exported: {review_item_count}",
            f"- Normalization issues: {normalization_issue_count}",
        ]
    )
    path.write_text(content + "\n", encoding="utf-8")


def write_excel_workbook(
    path: Path,
    *,
    routes: list[RouteDecision],
    subjects: list[SubjectRecord],
    positions: list[PositionRecord],
    review_items: list[ReviewItem],
) -> None:
    workbook = Workbook()
    workbook.remove(workbook.active)

    _write_sheet(workbook, "routing_results", ROUTING_FIELDS, [route.to_row() for route in routes])
    _write_sheet(workbook, "valuation_subjects", SUBJECT_FIELDS, [subject.to_row() for subject in subjects])
    _write_sheet(workbook, "valuation_positions", POSITION_FIELDS, [position.to_row() for position in positions])
    _write_sheet(workbook, "review_items", REVIEW_FIELDS, [item.to_row() for item in review_items])

    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object | None]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _write_sheet(workbook: Workbook, title: str, fieldnames: list[str], rows: list[dict[str, object | None]]) -> None:
    worksheet = workbook.create_sheet(title=title)
    worksheet.append(fieldnames)
    for row in rows:
        worksheet.append([row.get(field) for field in fieldnames])
