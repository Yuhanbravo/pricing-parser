from pathlib import Path

from valuation_parser.adapters.greatwall import GreatwallValuationAdapter
from valuation_parser.adapters.xyzc import XyzcValuationAdapter
from valuation_parser.models import RouteDecision


def test_greatwall_adapter_parses_sample_workbook() -> None:
    adapter = GreatwallValuationAdapter()
    sample_file = Path("data_samples/raw/证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_023",
        association_code=None,
        custodian_name_chinese=None,
        custodian_id="CUSTODIAN_008",
        custodian_name="CUSTODIAN_GROUP_008",
        adapter_key="greatwall",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_008 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) == 2
    assert len(artifacts.review_items) >= 1
    assert artifacts.subjects[0].sheet_name == "Sheet1"
    assert any(position.instrument_code_std == "02208.HK" for position in artifacts.positions)
    assert all(position.review_flag is None for position in artifacts.positions)
    assert artifacts.subjects[0].broker == "CUSTODIAN_GROUP_008"


def test_xyzc_adapter_parses_sample_workbook() -> None:
    adapter = XyzcValuationAdapter()
    sample_file = Path("data_samples/raw/20250327_PRODUCT_002_证券投资基金估值表.xls")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_002",
        association_code="XXX002",
        custodian_name_chinese=None,
        custodian_id="CUSTODIAN_001",
        custodian_name="CUSTODIAN_GROUP_001",
        adapter_key="xyzc",
        route_source="mapping(product_id+association_code)",
        route_status="success",
        route_message="matched CUSTODIAN_001 via mapping(product_id+association_code)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 10
    assert len(artifacts.review_items) >= 1
    assert artifacts.subjects[0].sheet_name == "PRODUCT_002"
    assert any(position.instrument_code_std == "600309.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "00700.HK" for position in artifacts.positions)
    assert all(position.review_flag is None for position in artifacts.positions)
    assert artifacts.subjects[0].broker == "CUSTODIAN_GROUP_001"
