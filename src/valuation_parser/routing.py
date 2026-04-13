from __future__ import annotations

from valuation_parser.models import MappingRecord, ProductIdentity, RouteDecision


def route_identity(
    source_file: str,
    identity: ProductIdentity,
    mappings: list[MappingRecord],
    adapter_override: str | None = None,
) -> RouteDecision:
    if adapter_override:
        return RouteDecision(
            source_file=source_file,
            product_id=identity.product_id,
            association_code=identity.association_code,
            custodian_id=None,
            custodian_name=None,
            adapter_key=adapter_override,
            route_source="manual_override",
            route_status="success",
            route_message=f"manual adapter override applied: {adapter_override}",
        )

    if identity.product_id and identity.association_code:
        match = _match_exact(identity.product_id, identity.association_code, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(product_id+association_code)")

    if identity.product_id:
        match = _match_product(identity.product_id, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(product_id)")

    if identity.association_code:
        match = _match_association(identity.association_code, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(association_code)")

    return RouteDecision(
        source_file=source_file,
        product_id=identity.product_id,
        association_code=identity.association_code,
        custodian_id=None,
        custodian_name=None,
        adapter_key=None,
        route_source="unresolved",
        route_status="failed",
        route_message=identity.route_message,
    )


def _match_exact(product_id: str, association_code: str, mappings: list[MappingRecord]) -> MappingRecord | None:
    for mapping in mappings:
        if mapping.product_id == product_id and mapping.association_code == association_code:
            return mapping
    return None


def _match_product(product_id: str, mappings: list[MappingRecord]) -> MappingRecord | None:
    for mapping in mappings:
        if mapping.product_id == product_id:
            return mapping
    return None


def _match_association(association_code: str, mappings: list[MappingRecord]) -> MappingRecord | None:
    for mapping in mappings:
        if mapping.association_code == association_code:
            return mapping
    return None


def _success_decision(
    source_file: str,
    identity: ProductIdentity,
    mapping: MappingRecord,
    route_source: str,
) -> RouteDecision:
    return RouteDecision(
        source_file=source_file,
        product_id=identity.product_id,
        association_code=identity.association_code,
        custodian_id=mapping.custodian_id,
        custodian_name=mapping.custodian_name,
        adapter_key=mapping.adapter_key,
        route_source=route_source,
        route_status="success",
        route_message=f"matched {mapping.custodian_id} via {route_source}",
    )
