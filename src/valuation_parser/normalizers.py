from __future__ import annotations

import re


def normalize_security_code(raw_code: str | None) -> tuple[str | None, str | None, str | None]:
    if raw_code is None:
        return None, None, "missing_code"

    digits = re.sub(r"\D", "", raw_code).strip()
    if not digits:
        return None, None, "missing_code"

    if len(digits) in {4, 5}:
        return f"{digits.zfill(5)}.HK", "HK", None

    if len(digits) == 6:
        if digits[0] in {"5", "6", "9"}:
            return f"{digits}.SH", "SH", None
        if digits[0] in {"0", "1", "2", "3"}:
            return f"{digits}.SZ", "SZ", None

    return digits, None, "unknown_exchange"


def infer_asset_type(raw_code: str | None, exchange: str | None) -> str | None:
    digits = re.sub(r"\D", "", raw_code or "").strip()

    if exchange == "HK":
        return "hk_equity"

    if exchange in {"SH", "SZ"}:
        if digits.startswith("5"):
            return "fund_or_etf"
        return "a_share"

    return None


def resolve_review_flag(normalization_flag: str | None, asset_type: str | None) -> str | None:
    if normalization_flag:
        return normalization_flag
    if asset_type is None:
        return "unknown_asset_type"
    return None


def derive_broker_name(custodian_name: str | None, adapter_key: str | None) -> str | None:
    if custodian_name:
        return custodian_name
    if adapter_key:
        return adapter_key
    return None
