from __future__ import annotations

from valuation_parser.adapters.cmsc import CmscValuationAdapter
from valuation_parser.adapters.citics import CiticsValuationAdapter
from valuation_parser.adapters.csc import CscValuationAdapter
from valuation_parser.adapters.generic import GenericValuationAdapter
from valuation_parser.adapters.greatwall import GreatwallValuationAdapter
from valuation_parser.adapters.gtja import GtjaValuationAdapter
from valuation_parser.adapters.guosen import GuosenValuationAdapter
from valuation_parser.adapters.orient import OrientValuationAdapter
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
    registry["cmsc"] = CmscValuationAdapter()
    registry["citics"] = CiticsValuationAdapter()
    registry["csc"] = CscValuationAdapter()
    registry["generic"] = GenericValuationAdapter()
    registry["greatwall"] = GreatwallValuationAdapter()
    registry["gtja"] = GtjaValuationAdapter()
    registry["guosen"] = GuosenValuationAdapter()
    registry["orient"] = OrientValuationAdapter()
    registry["xyzc"] = XyzcValuationAdapter()
    return registry


def get_adapter(adapter_key: str, registry: dict[str, BaseValuationAdapter] | None = None) -> BaseValuationAdapter:
    active_registry = registry or build_registry()
    if adapter_key not in active_registry:
        raise KeyError(f"Unsupported adapter_key: {adapter_key}")
    return active_registry[adapter_key]
