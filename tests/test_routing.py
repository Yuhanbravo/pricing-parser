from valuation_parser.models import MappingRecord, ProductIdentity
from valuation_parser.routing import route_identity


def test_route_prefers_exact_match() -> None:
    mappings = [
        MappingRecord(
            product_id="PRODUCT_001",
            association_code="XXX001",
            custodian_id="CUSTODIAN_007",
            custodian_name="CUSTODIAN_GROUP_007",
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
