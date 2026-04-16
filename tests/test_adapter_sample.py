from pathlib import Path

from valuation_parser.adapters.citics import CiticsValuationAdapter
from valuation_parser.adapters.greatwall import GreatwallValuationAdapter
from valuation_parser.adapters.gtja import GtjaValuationAdapter
from valuation_parser.adapters.orient import OrientValuationAdapter
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


def test_citics_adapter_parses_sample_workbook() -> None:
    adapter = CiticsValuationAdapter()
    sample_file = Path("data_samples/raw/PRODUCT_006_资产估值表_20250327.xls")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_006",
        association_code="XXX006",
        custodian_name_chinese="中信证券",
        custodian_id="CUSTODIAN_003",
        custodian_name="CUSTODIAN_GROUP_003",
        adapter_key="citics",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_003 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 10
    assert any(position.instrument_code_std == "600036.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "09926.HK" for position in artifacts.positions)
    assert any(position.instrument_code_std == "512000.SH" for position in artifacts.positions)
    assert artifacts.subjects[0].broker == "CUSTODIAN_GROUP_003"


def test_orient_adapter_parses_sample_workbook() -> None:
    adapter = OrientValuationAdapter()
    sample_file = Path("data_samples/raw/PRODUCT_010_证券投资基金估值表_2025-03-27.xls")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_010",
        association_code="XXX010",
        custodian_name_chinese="东方证券",
        custodian_id="CUSTODIAN_004",
        custodian_name="CUSTODIAN_GROUP_004",
        adapter_key="orient",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_004 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 8
    assert any(position.instrument_code_std == "601058.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "002475.SZ" for position in artifacts.positions)
    assert any(position.instrument_code_std == "00700.HK" for position in artifacts.positions)
    assert artifacts.subjects[0].broker == "CUSTODIAN_GROUP_004"


def test_gtja_adapter_parses_sample_workbook() -> None:
    adapter = GtjaValuationAdapter()
    sample_file = Path("data_samples/raw/PRODUCT_012_估值表_20250327.xls")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_012",
        association_code="XXX012",
        custodian_name_chinese="国泰",
        custodian_id="CUSTODIAN_006",
        custodian_name="CUSTODIAN_GROUP_006",
        adapter_key="gtja",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_006 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 6
    assert any(position.instrument_code_std == "605376.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "000333.SZ" for position in artifacts.positions)
    assert any(position.instrument_code_std == "600309.SH" for position in artifacts.positions)
    assert artifacts.subjects[0].broker == "CUSTODIAN_GROUP_006"
