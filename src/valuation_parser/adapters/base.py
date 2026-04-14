from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from pathlib import Path
import re

from valuation_parser.models import ParseArtifacts, PositionRecord, ReviewItem, RouteDecision, SubjectRecord
from valuation_parser.normalizers import derive_broker_name, infer_asset_type, normalize_security_code, resolve_review_flag


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


def build_positions_and_review_items(subjects: list[SubjectRecord]) -> tuple[list[PositionRecord], list[ReviewItem]]:
    positions: list[PositionRecord] = []
    review_items: list[ReviewItem] = []
    for subject in subjects:
        review_reason = _determine_review_reason(subject)
        if review_reason:
            review_items.append(
                ReviewItem(
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

        if not subject.is_position_candidate:
            continue
        instrument_code_raw = _extract_instrument_code(subject.subject_code)
        instrument_code_std, exchange, normalization_flag = normalize_security_code(instrument_code_raw)
        asset_type = infer_asset_type(instrument_code_raw, exchange)
        review_flag = resolve_review_flag(normalization_flag, asset_type)
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
                suspension_info=subject.suspension_info,
                review_flag=review_flag,
                review_note=_build_review_note(review_flag),
            )
        )
    return positions, review_items


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
    return bool(
        leaf_flag
        and subject.quantity not in (None, 0)
        and subject.unit_cost is not None
        and subject.market_price is not None
        and subject.subject_code
        and re.search(r"[A-Z]\d{5}$|\d{6}$", subject.subject_code)
    )


def _extract_instrument_code(subject_code: str | None) -> str | None:
    if not subject_code:
        return None
    match = re.search(r"([A-Z]?)(\d{5,6})$", subject_code)
    if not match:
        return None
    return match.group(2)


def _determine_review_reason(subject: SubjectRecord) -> str | None:
    if subject.subject_code and subject.subject_code.endswith("99"):
        return "估值增值汇总行，通常不作为持仓叶子"
    if subject.is_leaf and subject.quantity not in (None, 0) and subject.market_price is None:
        return "叶子行存在数量但缺少市价"
    if subject.is_leaf and subject.market_price is not None and subject.quantity in (None, 0):
        return "叶子行存在市价但缺少数量"
    return None


def _build_review_note(review_flag: str | None) -> str | None:
    if review_flag == "missing_code":
        return "缺少可标准化的证券代码"
    if review_flag == "unknown_exchange":
        return "无法根据证券代码识别交易所"
    if review_flag == "unknown_asset_type":
        return "无法推断资产类型"
    return None
