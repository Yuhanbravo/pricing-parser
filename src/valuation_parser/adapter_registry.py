from __future__ import annotations

from valuation_parser.adapters.greatwall import GreatwallValuationAdapter
from valuation_parser.adapters.xyzc import XyzcValuationAdapter
from valuation_parser.adapters.base import BaseValuationAdapter
from valuation_parser.adapters.placeholder import PlaceholderValuationAdapter

SUPPORTED_ADAPTERS = {
    "generic",
    "xyzc",
    "cmsc",
    "citics",
    "orient",
    "csc",
    "gtja",
    "guosen",
    "greatwall",
}


def build_registry() -> dict[str, BaseValuationAdapter]:
    registry = {key: PlaceholderValuationAdapter(key) for key in sorted(SUPPORTED_ADAPTERS)}
    registry["greatwall"] = GreatwallValuationAdapter()
    registry["xyzc"] = XyzcValuationAdapter()
    return registry


def get_adapter(adapter_key: str, registry: dict[str, BaseValuationAdapter] | None = None) -> BaseValuationAdapter:
    active_registry = registry or build_registry()
    if adapter_key not in active_registry:
        raise KeyError(f"Unsupported adapter_key: {adapter_key}")
    return active_registry[adapter_key]
