from valuation_parser.models import MappingRecord, ProductIdentity
from valuation_parser.routing import route_identity


def test_route_prefers_exact_match() -> None:
    mappings = [
        MappingRecord(
            product_id="PRODUCT_001",
            association_code="XXX001",
            custodian_id="CUSTODIAN_007",
            custodian_name="CUSTODIAN_GROUP_007",
            true_custodian_name="国信证券股份有限公司",
            adapter_key="guosen",
        )
    ]

    route = route_identity(
        source_file="sample.xlsx",
        identity=ProductIdentity(product_id="PRODUCT_001", association_code="XXX001", route_message="ok"),
        mappings=mappings,
    )

    assert route.route_status == "success"
    assert route.adapter_key == "guosen"
    assert route.route_source == "mapping(product_id+association_code)"


def test_route_can_fallback_to_true_custodian_name_alias() -> None:
    mappings = [
        MappingRecord(
            product_id="PRODUCT_012",
            association_code="XXX012",
            custodian_id="CUSTODIAN_006",
            custodian_name="CUSTODIAN_GROUP_006",
            true_custodian_name="国泰海通证券股份有限公司",
            adapter_key="gtja",
        )
    ]

    route = route_identity(
        source_file="sample.xlsx",
        identity=ProductIdentity(custodian_name_chinese="国泰", route_message="resolved custodian_name_chinese only"),
        mappings=mappings,
    )

    assert route.route_status == "success"
    assert route.adapter_key == "gtja"
    assert route.route_source == "mapping(custodian_name_chinese)"
    assert route.custodian_name_chinese == "国泰海通证券股份有限公司"


def test_route_reports_attempted_strategies_when_mapping_is_missing() -> None:
    route = route_identity(
        source_file="sample.xlsx",
        identity=ProductIdentity(product_id="PRODUCT_022", association_code="XXX022", route_message="resolved product_id and association_code"),
        mappings=[],
    )

    assert route.route_status == "failed"
    assert "PRODUCT_022" in route.route_message
    assert "XXX022" in route.route_message
    assert "mapping(product_id+association_code)" in route.route_message
    assert "mapping(product_id)" in route.route_message
    assert "mapping(association_code)" in route.route_message
