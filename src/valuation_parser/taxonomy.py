from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re

import yaml


@dataclass(frozen=True)
class AssetTaxonomyEntry:
    key: str
    display_name: str
    asset_class_l1: str
    asset_class_l2: str
    include_in_positions: bool
    # YAML keeps this as 0/1 for readability, but the loader normalizes it to
    # the runtime review_flag representation ("0"/"1") used by merge logic.
    default_review_flag: str | None = None
    default_review_category: str | None = None


@dataclass(frozen=True)
class TaxonomyFields:
    asset_type_internal: str
    asset_type_display: str
    asset_class_l1: str
    asset_class_l2: str
    include_in_positions: bool
    default_review_flag: str | None = None
    review_category: str | None = None


class AssetTaxonomy:
    def __init__(self, entries: dict[str, AssetTaxonomyEntry]) -> None:
        self._entries = entries

    def resolve(self, key: str | None) -> TaxonomyFields:
        entry = self._entries.get(key or "", self._entries["unknown"])
        return TaxonomyFields(
            asset_type_internal=entry.key,
            asset_type_display=entry.display_name,
            asset_class_l1=entry.asset_class_l1,
            asset_class_l2=entry.asset_class_l2,
            include_in_positions=entry.include_in_positions,
            default_review_flag=entry.default_review_flag,
            review_category=entry.default_review_category,
        )


LEGACY_ASSET_TYPE_MAP = {
    "a_share": "equity_a_share",
    "hk_equity": "equity_hk",
    "fund_or_etf": "fund_exchange_traded",
}


def load_asset_taxonomy(config_path: Path | None = None) -> AssetTaxonomy:
    return _load_asset_taxonomy_cached(config_path or _default_config_path())


@lru_cache(maxsize=2)
def _load_asset_taxonomy_cached(config_path: Path) -> AssetTaxonomy:
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    entries: dict[str, AssetTaxonomyEntry] = {}
    for key, item in (data.get("asset_types") or {}).items():
        if not isinstance(item, dict):
            continue
        review_flag = item.get("default_review_flag")
        entries[key] = AssetTaxonomyEntry(
            key=key,
            display_name=str(item.get("display_name") or key),
            asset_class_l1=str(item.get("asset_class_l1") or "未识别"),
            asset_class_l2=str(item.get("asset_class_l2") or "未识别"),
            include_in_positions=bool(item.get("include_in_positions")),
            # Normalize YAML ints to the existing string-based review flag
            # contract so taxonomy defaults and exporter flags compare cleanly.
            default_review_flag=str(review_flag) if review_flag in {0, 1, "0", "1"} else None,
            default_review_category=_clean_text(item.get("default_review_category")),
        )

    if "unknown" not in entries:
        raise ValueError("asset taxonomy config must define unknown")
    return AssetTaxonomy(entries)


def classify_position_taxonomy(
    *,
    asset_type: str | None,
    instrument_code_raw: str | None,
    exchange: str | None,
    subject_code: str | None,
    subject_name: str | None,
    review_reason: str | None = None,
    taxonomy: AssetTaxonomy | None = None,
) -> TaxonomyFields:
    resolved_taxonomy = taxonomy or load_asset_taxonomy()
    taxonomy_key = _select_taxonomy_key(
        asset_type=asset_type,
        instrument_code_raw=instrument_code_raw,
        exchange=exchange,
        subject_code=subject_code,
        subject_name=subject_name,
        review_reason=review_reason,
    )
    return resolved_taxonomy.resolve(taxonomy_key)


def classify_subject_taxonomy(
    *,
    subject_code: str | None,
    subject_name: str | None,
    asset_type: str | None = None,
    review_reason: str | None = None,
    taxonomy: AssetTaxonomy | None = None,
) -> TaxonomyFields:
    resolved_taxonomy = taxonomy or load_asset_taxonomy()
    taxonomy_key = _select_taxonomy_key(
        asset_type=asset_type,
        instrument_code_raw=None,
        exchange=None,
        subject_code=subject_code,
        subject_name=subject_name,
        review_reason=review_reason,
    )
    return resolved_taxonomy.resolve(taxonomy_key)


def _select_taxonomy_key(
    *,
    asset_type: str | None,
    instrument_code_raw: str | None,
    exchange: str | None,
    subject_code: str | None,
    subject_name: str | None,
    review_reason: str | None,
) -> str:
    normalized_subject_code = (subject_code or "").strip().upper()
    normalized_subject_name = (subject_name or "").strip()
    normalized_review_reason = (review_reason or "").strip()
    digits = re.sub(r"\D", "", instrument_code_raw or "")
    has_swap_name = "收益互换" in normalized_subject_name
    has_margin_name = "保证金" in normalized_subject_name

    if has_swap_name and has_margin_name and not normalized_subject_code.startswith("3102"):
        return "margin_deposit"

    if normalized_subject_code.startswith("3102") or "衍生工具" in normalized_review_reason or has_swap_name:
        return "derivative_swap"

    if asset_type == "a_share" and exchange == "SH" and digits.startswith("689"):
        return "cdr"
    if asset_type == "a_share" and exchange == "SH" and digits.startswith("688"):
        return "equity_star"

    mapped_legacy = LEGACY_ASSET_TYPE_MAP.get(asset_type or "")
    if mapped_legacy:
        return mapped_legacy

    if normalized_subject_code.startswith("1002") or any(token in normalized_subject_name for token in ("银行存款", "存款", "活期存款", "定期存款")):
        return "cash_deposit"
    if normalized_subject_code.startswith("1031") or has_margin_name:
        return "margin_deposit"
    if normalized_subject_code.startswith("1021") or "清算款" in normalized_subject_name:
        return "clearing_balance"
    if normalized_subject_code.startswith("2221") or "应交税费" in normalized_subject_name or "税费" in normalized_subject_name:
        return "tax_payable"
    if normalized_subject_code.startswith("2203") or normalized_subject_code.startswith("2202") or "应付款" in normalized_subject_name:
        return "payable"

    return "unknown"


def _default_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "asset_taxonomy.yaml"


def _clean_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None