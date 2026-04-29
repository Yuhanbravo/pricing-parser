from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from pathlib import Path
import re

from valuation_parser.models import ParseArtifacts, PositionRecord, ReviewItem, RouteDecision, SubjectRecord
from valuation_parser.normalizers import REVIEW_FLAG_VALUE, derive_broker_name, infer_asset_type, normalize_security_code, resolve_review_flag


class BaseValuationAdapter(ABC):
    key = "base"

    @abstractmethod
    def parse(self, source_file: Path, route: RouteDecision) -> ParseArtifacts:
        raise NotImplementedError


def annotate_subject_hierarchy(subjects: list[SubjectRecord]) -> list[SubjectRecord]:
    codes = [subject.subject_code for subject in subjects if subject.subject_code]
    annotated: list[SubjectRecord] = []
    for subject in subjects:
        code = subject.subject_code
        parent_code = _find_parent_code(code, codes)
        is_leaf = not any(other_code and code and other_code != code and other_code.startswith(code) for other_code in codes)
        subject_level = _infer_subject_level(code)
        root_subject_code = _find_root_subject_code(code, codes)
        root_subject_name = next((candidate.subject_name for candidate in subjects if candidate.subject_code == root_subject_code), None)
        is_position_candidate = _is_position_subject(subject, is_leaf=is_leaf)
        annotated.append(
            replace(
                subject,
                parent_subject_code=parent_code,
                subject_level=subject_level,
                root_subject_code=root_subject_code,
                root_subject_name=root_subject_name,
                is_leaf=is_leaf,
                is_position_candidate=is_position_candidate,
            )
        )
    return annotated


def build_positions_and_review_items(subjects: list[SubjectRecord]) -> tuple[list[SubjectRecord], list[PositionRecord], list[ReviewItem]]:
    flagged_subjects: list[SubjectRecord] = []
    positions: list[PositionRecord] = []
    review_items: list[ReviewItem] = []
    for subject in subjects:
        review_reason = _determine_review_reason(subject)
        subject_review_flag = REVIEW_FLAG_VALUE if review_reason else None
        if review_reason:
            review_items.append(
                ReviewItem(
                    source_file=subject.source_file,
                    broker=subject.broker,
                    valuation_date=subject.valuation_date,
                    raw_row_index=subject.raw_row_index,
                    subject_code=subject.subject_code,
                    subject_name=subject.subject_name,
                    quantity=subject.quantity,
                    cost=subject.cost,
                    market_value=subject.market_value,
                    pnl=subject.pnl,
                    review_reason=review_reason,
                )
            )

        instrument_code_raw = _extract_instrument_code(subject.subject_code)
        if not _should_emit_position(subject, review_reason, instrument_code_raw):
            flagged_subjects.append(replace(subject, review_flag=subject_review_flag))
            continue
        instrument_code_std, exchange, normalization_flag = normalize_security_code(instrument_code_raw)
        asset_type = infer_asset_type(instrument_code_raw, exchange)
        review_flag = resolve_review_flag(normalization_flag, asset_type, review_reason)
        flagged_subjects.append(replace(subject, review_flag=review_flag))
        positions.append(
            PositionRecord(
                source_file=subject.source_file,
                broker=subject.broker,
                sheet_name=subject.sheet_name,
                valuation_date=subject.valuation_date,
                product_id=subject.product_id,
                association_code=subject.association_code,
                custodian_id=subject.custodian_id,
                custodian_name=subject.custodian_name,
                adapter_key=subject.adapter_key,
                route_source=subject.route_source,
                instrument_name=subject.subject_name,
                instrument_code_raw=instrument_code_raw,
                instrument_code_std=instrument_code_std,
                exchange=exchange,
                asset_type=asset_type,
                quantity=subject.quantity,
                unit_cost=subject.unit_cost,
                cost=subject.cost,
                market_price=subject.market_price,
                market_value=subject.market_value,
                unrealized_pnl=subject.pnl,
                subject_code=subject.subject_code,
                subject_name=subject.subject_name,
                raw_row_index=subject.raw_row_index,
                suspension_info=_normalize_position_suspension_info(subject.suspension_info),
                review_flag=review_flag,
                review_note=_build_review_note(review_flag, review_reason),
            )
        )
    return flagged_subjects, positions, review_items


def enrich_subject_record(subject: SubjectRecord) -> SubjectRecord:
    broker = derive_broker_name(subject.custodian_name, subject.adapter_key)
    return replace(subject, broker=broker)


def _find_parent_code(code: str | None, codes: list[str | None]) -> str | None:
    if not code:
        return None
    candidates = [candidate for candidate in codes if candidate and candidate != code and code.startswith(candidate)]
    if not candidates:
        return None
    return max(candidates, key=len)


def _find_root_subject_code(code: str | None, codes: list[str | None]) -> str | None:
    if not code:
        return None
    candidates = [candidate for candidate in codes if candidate and code.startswith(candidate)]
    if not candidates:
        return None
    return min(candidates, key=len)


def _infer_subject_level(code: str | None) -> int | None:
    if not code:
        return None
    if re.fullmatch(r"\d{4}", code):
        return 1
    if re.fullmatch(r"\d{6}|\d{4}[A-Z]\d{2}", code):
        return 2
    if re.fullmatch(r"\d{8}|\d{6}[A-Z]\d{2}", code):
        return 3
    return 4


def _is_position_subject(subject: SubjectRecord, *, is_leaf: bool | None = None) -> bool:
    leaf_flag = subject.is_leaf if is_leaf is None else is_leaf
    instrument_code = _extract_instrument_code(subject.subject_code)
    return bool(
        leaf_flag
        and subject.quantity not in (None, 0)
        and (subject.unit_cost is not None or subject.cost is not None)
        and (subject.market_price is not None or subject.market_value is not None)
        and subject.subject_code
        and instrument_code is not None
    )


def _should_emit_position(
    subject: SubjectRecord,
    review_reason: str | None,
    instrument_code_raw: str | None,
) -> bool:
    if subject.is_position_candidate:
        return True

    if not review_reason or not subject.is_leaf or not subject.subject_code:
        return False

    return bool(
        instrument_code_raw is not None
        or subject.quantity not in (None, 0)
        or subject.cost is not None
        or subject.market_price is not None
        or subject.market_value is not None
    )


def _extract_instrument_code(subject_code: str | None) -> str | None:
    if not subject_code:
        return None
    normalized = subject_code.strip().upper()
    normalized = re.sub(r"[._\- ](?:SH|SZ|HK|HG|CFX)$", "", normalized)

    embedded_match = re.search(r"[A-Z]{1,2}(\d{5,6})$", normalized)
    if embedded_match:
        return embedded_match.group(1)

    separated_match = re.search(r"(?:^|[._\- ])(\d{4,6})$", normalized)
    if separated_match:
        return separated_match.group(1)

    plain_match = re.search(r"(\d{6})$", normalized)
    if plain_match:
        return plain_match.group(1)

    return None


def _determine_review_reason(subject: SubjectRecord) -> str | None:
    if _is_derivative_subject(subject.subject_code):
        return "衍生工具科目，需单独建模或排除"
    if _is_valuation_gain_summary(subject):
        return "估值增值汇总行，通常不作为持仓叶子"
    if subject.is_leaf and subject.quantity not in (None, 0) and subject.market_price is None:
        return "叶子行存在数量但缺少市价"
    if subject.is_leaf and subject.market_price is not None and subject.quantity in (None, 0):
        return "叶子行存在市价但缺少数量"
    return None


def _is_valuation_gain_summary(subject: SubjectRecord) -> bool:
    return bool(
        subject.subject_code
        and subject.subject_code.endswith("99")
        and subject.quantity in (None, 0)
        and "估值增值" in (subject.subject_name or "")
    )


def _is_derivative_subject(subject_code: str | None) -> bool:
    if not subject_code:
        return False
    return subject_code.strip().upper().startswith("3102")


def _normalize_position_suspension_info(suspension_info: str | None) -> str | None:
    if not suspension_info:
        return None
    normalized = suspension_info.strip()
    if normalized in {"【正常交易】", "(正常交易)", "（正常交易）", "[正常交易]"}:
        return "正常交易"
    return normalized


def _build_review_note(review_flag: str | None, review_reason: str | None) -> str | None:
    notes: list[str] = []
    if review_flag == "missing_code":
        notes.append("缺少可标准化的证券代码")
    elif review_flag == "unknown_exchange":
        notes.append("无法根据证券代码识别交易所")
    elif review_flag == "unknown_asset_type":
        notes.append("无法推断资产类型")

    if review_reason:
        notes.append(review_reason)

    if not notes:
        return None
    return "；".join(notes)
