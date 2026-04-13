from __future__ import annotations

import re


def normalize_security_code(raw_code: str | None) -> tuple[str | None, str | None, str | None]:
    if raw_code is None:
        return None, None, "missing_code"

    digits = re.sub(r"\D", "", raw_code).strip()
    if not digits:
        return None, None, "missing_code"

    if len(digits) == 5:
        return f"{digits.zfill(5)}.HK", "HK", None

    if len(digits) == 6:
        if digits[0] in {"5", "6", "9"}:
            return f"{digits}.SH", "SH", None
        if digits[0] in {"0", "1", "2", "3"}:
            return f"{digits}.SZ", "SZ", None

    return digits, None, "unknown_exchange"
