from pathlib import Path

from valuation_parser.adapters.cmsc import CmscValuationAdapter
from valuation_parser.adapters.csc import CscValuationAdapter
from valuation_parser.adapters.generic import GenericValuationAdapter
from valuation_parser.adapters.guosen import GuosenValuationAdapter
from valuation_parser.adapters.xyzc import XyzcValuationAdapter
from valuation_parser.models import RouteDecision


def test_guosen_adapter_parses_sample_workbook() -> None:
    adapter = GuosenValuationAdapter()
    sample_file = Path("data_samples/raw/2025-03-27_PRODUCT_001估值表.xlsx")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_001",
        association_code="XXX001",
        custodian_name_chinese=None,
        custodian_id="CUSTODIAN_007",
        custodian_name="CUSTODIAN_GROUP_007",
        adapter_key="guosen",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_007 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 5
    assert any(position.instrument_code_std == "689009.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "00700.HK" for position in artifacts.positions)


def test_cmsc_adapter_parses_sample_workbook() -> None:
    adapter = CmscValuationAdapter()
    sample_file = Path("data_samples/raw/PRODUCT_008委托资产资产估值表20250327.xls")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_008",
        association_code="XXX008",
        custodian_name_chinese="招商证券",
        custodian_id="CUSTODIAN_002",
        custodian_name="CUSTODIAN_GROUP_002",
        adapter_key="cmsc",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_002 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 10
    assert any(position.instrument_code_std == "600309.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "00700.HK" for position in artifacts.positions)


def test_csc_adapter_parses_sample_workbook() -> None:
    adapter = CscValuationAdapter()
    sample_file = Path("data_samples/raw/估值表_PRODUCT_021_20250327.xls")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_021",
        association_code="XXX021",
        custodian_name_chinese="中信建投",
        custodian_id="CUSTODIAN_005",
        custodian_name="CUSTODIAN_GROUP_005",
        adapter_key="csc",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_005 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 4
    assert any(position.instrument_code_std == "00700.HK" for position in artifacts.positions)
    assert any(position.instrument_code_std == "002475.SZ" for position in artifacts.positions)


def test_xyzc_adapter_parses_csv_sample_workbook() -> None:
    adapter = XyzcValuationAdapter()
    sample_file = Path("data_samples/raw/20250327_PRODUCT_002_证券投资基金估值表.csv")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_002",
        association_code="XXX002",
        custodian_name_chinese="兴业证券",
        custodian_id="CUSTODIAN_001",
        custodian_name="CUSTODIAN_GROUP_001",
        adapter_key="xyzc",
        route_source="mapping(product_id)",
        route_status="success",
        route_message="matched CUSTODIAN_001 via mapping(product_id)",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert any(position.instrument_code_std == "600309.SH" for position in artifacts.positions)
    assert any(position.instrument_code_std == "00700.HK" for position in artifacts.positions)


def test_generic_adapter_can_parse_unmapped_standard_workbook() -> None:
    adapter = GenericValuationAdapter()
    sample_file = Path("data_samples/raw/估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx")
    route = RouteDecision(
        source_file=str(sample_file),
        product_id="PRODUCT_022",
        association_code="XXX022",
        custodian_name_chinese=None,
        custodian_id=None,
        custodian_name=None,
        adapter_key="generic",
        route_source="layout_fallback(generic)",
        route_status="success",
        route_message="fallback to generic tabular parser",
    )

    artifacts = adapter.parse(sample_file, route)

    assert len(artifacts.subjects) > 0
    assert len(artifacts.positions) >= 3
    assert any(position.instrument_code_std == "601058.SH" for position in artifacts.positions)