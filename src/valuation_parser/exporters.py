from __future__ import annotations

import csv
from collections import Counter
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
    "source_file",
    "broker",
    "sheet_name",
    "valuation_date",
    "product_id",
    "association_code",
    "custodian_id",
    "custodian_name",
    "adapter_key",
    "route_source",
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
    "review_flag",
    "raw_text",
]

POSITION_FIELDS = [
    "source_file",
    "broker",
    "sheet_name",
    "valuation_date",
    "product_id",
    "association_code",
    "custodian_id",
    "custodian_name",
    "adapter_key",
    "route_source",
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
    "source_file",
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
    generic_fallback_count = sum(1 for route in routes if route.route_source == "layout_fallback(generic)")
    flagged_subject_count = sum(1 for subject in subjects if subject.review_flag)
    flagged_position_count = sum(1 for position in positions if position.review_flag)
    review_item_count = len(review_items)
    normalization_issue_count = sum(1 for position in positions if _has_normalization_issue(position.review_note))
    adapter_keys = sorted({route.adapter_key for route in routes if route.adapter_key})
    supported_asset_types = sorted({position.asset_type for position in positions if position.asset_type})
    unsupported_asset_types = ["unknown_asset_type"] if any(_has_unknown_asset_type(position.review_note) for position in positions) else []
    unrouted_files = sorted({Path(route.source_file).name for route in routes if route.route_status != "success"})
    unrouted_lines = _build_unrecognized_object_lines(routes)
    review_lines = _build_review_summary_lines(review_items=review_items, positions=positions)
    review_index_lines = _build_review_index_lines(review_items=review_items, positions=positions)

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
            f"- Review flagged subjects: {flagged_subject_count}",
            f"- Review flagged positions: {flagged_position_count}",
            f"- Review items exported: {review_item_count}",
            f"- Normalization issues: {normalization_issue_count}",
            f"- Unrouted files: {', '.join(unrouted_files) if unrouted_files else 'none'}",
            f"- Generic fallback routes used: {generic_fallback_count}",
            "- Fallback note: generic fallback runs only when --allow-generic-fallback is explicitly enabled.",
            "- Review entrypoint: first inspect the Review Entry Index below, then open valuation_subjects.csv / valuation_positions.csv rows with review_flag=1 and use review_items.csv.review_reason / valuation_positions.csv.review_note for concrete reasons.",
            f"- Supported asset types: {', '.join(supported_asset_types) if supported_asset_types else 'none'}",
            f"- Unsupported asset types: {', '.join(unsupported_asset_types) if unsupported_asset_types else 'none'}",
            "",
            "## Unrouted File Details",
            *([f"- {source_file}" for source_file in unrouted_files] or ["- none"]),
            "",
            "## Unrecognized Object Index",
            *unrouted_lines,
            "",
            "## Review Entry Index",
            *review_index_lines,
            "",
            "## Review Queue By Source File",
            *review_lines,
        ]
    )
    path.write_text(content + "\n", encoding="utf-8")


def _build_unrecognized_object_lines(routes: list[RouteDecision]) -> list[str]:
    failed_routes = [route for route in routes if route.route_status != "success"]
    if not failed_routes:
        return ["- none"]

    lines: list[str] = []
    for route in sorted(failed_routes, key=lambda item: Path(item.source_file).name):
        lines.append(
            "- "
            f"source_file={Path(route.source_file).name}; "
            f"product_id={route.product_id or 'none'}; "
            f"association_code={route.association_code or 'none'}; "
            f"route_message={route.route_message or 'none'}"
        )
    return lines


def _build_review_index_lines(*, review_items: list[ReviewItem], positions: list[PositionRecord]) -> list[str]:
    review_entries: dict[tuple[str, int | None, str | None, str | None], dict[str, object]] = {}

    for review_item in review_items:
        source_file = Path(review_item.source_file).name if review_item.source_file else "unknown"
        key = (source_file, review_item.raw_row_index, review_item.subject_code, review_item.subject_name)
        entry = review_entries.setdefault(
            key,
            {
                "entrypoints": set(),
                "reasons": set(),
            },
        )
        entry["entrypoints"].add("subject")
        entry["reasons"].update(_split_review_reasons(review_item.review_reason))

    for position in positions:
        if not position.review_note:
            continue
        source_file = Path(position.source_file).name
        key = (source_file, position.raw_row_index, position.subject_code, position.subject_name or position.instrument_name)
        entry = review_entries.setdefault(
            key,
            {
                "entrypoints": set(),
                "reasons": set(),
            },
        )
        entry["entrypoints"].add("position")
        entry["reasons"].update(_split_review_reasons(position.review_note))

    if not review_entries:
        return ["- none"]

    lines: list[str] = []
    for (source_file, raw_row_index, subject_code, subject_name), payload in sorted(review_entries.items()):
        entrypoints = "+".join(sorted(payload["entrypoints"]))
        reasons = "；".join(sorted(payload["reasons"])) or "none"
        lines.append(
            "- "
            f"source_file={source_file}; "
            f"raw_row_index={raw_row_index if raw_row_index is not None else 'none'}; "
            f"subject_code={subject_code or 'none'}; "
            f"subject_name={subject_name or 'none'}; "
            f"entrypoint={entrypoints}; "
            f"reasons={reasons}"
        )
    return lines


def _build_review_summary_lines(*, review_items: list[ReviewItem], positions: list[PositionRecord]) -> list[str]:
    review_entries: dict[tuple[str, int | None, str | None, str | None], set[str]] = {}

    for review_item in review_items:
        source_file = Path(review_item.source_file).name if review_item.source_file else "unknown"
        key = (source_file, review_item.raw_row_index, review_item.subject_code, review_item.subject_name)
        reasons = review_entries.setdefault(key, set())
        reasons.update(_split_review_reasons(review_item.review_reason))

    for position in positions:
        if not position.review_note:
            continue
        source_file = Path(position.source_file).name
        key = (source_file, position.raw_row_index, position.subject_code, position.instrument_name)
        reasons = review_entries.setdefault(key, set())
        reasons.update(_split_review_reasons(position.review_note))

    if not review_entries:
        return ["- none"]

    summary_lines: list[str] = []
    source_files = sorted({entry_key[0] for entry_key in review_entries})
    for source_file in source_files:
        entries_for_file = [reasons for entry_key, reasons in review_entries.items() if entry_key[0] == source_file]
        reason_counter: Counter[str] = Counter(
            reason
            for reasons in entries_for_file
            for reason in reasons
        )
        top_reasons = ", ".join(
            f"{reason} ({count})"
            for reason, count in sorted(reason_counter.items(), key=lambda item: (-item[1], item[0]))[:3]
        )
        summary_lines.append(
            f"- {source_file}: {len(entries_for_file)} review entries; top reasons: {top_reasons or 'none'}"
        )
    return summary_lines


def _split_review_reasons(review_text: str | None) -> list[str]:
    if not review_text:
        return []
    return [part.strip() for part in review_text.split("；") if part.strip()]


def _has_normalization_issue(review_note: str | None) -> bool:
    if not review_note:
        return False
    return any(
        marker in review_note
        for marker in (
            "缺少可标准化的证券代码",
            "无法根据证券代码识别交易所",
            "无法推断资产类型",
        )
    )


def _has_unknown_asset_type(review_note: str | None) -> bool:
    return bool(review_note and "无法推断资产类型" in review_note)


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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_sheet(workbook: Workbook, title: str, fieldnames: list[str], rows: list[dict[str, object | None]]) -> None:
    worksheet = workbook.create_sheet(title=title)
    worksheet.append(fieldnames)
    for row in rows:
        worksheet.append([row.get(field) for field in fieldnames])
