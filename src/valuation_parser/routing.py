from __future__ import annotations

from valuation_parser.models import MappingRecord, ProductIdentity, RouteDecision


def route_identity(
    source_file: str,
    identity: ProductIdentity,
    mappings: list[MappingRecord],
    adapter_override: str | None = None,
) -> RouteDecision:
    attempts: list[str] = []
    if adapter_override:
        return RouteDecision(
            source_file=source_file,
            product_id=identity.product_id,
            association_code=identity.association_code,
            custodian_name_chinese=identity.custodian_name_chinese,
            custodian_id=None,
            custodian_name=None,
            adapter_key=adapter_override,
            route_source="manual_override",
            route_status="success",
            route_message=f"manual adapter override applied: {adapter_override}",
        )

    if identity.product_id and identity.association_code:
        attempts.append("mapping(product_id+association_code)")
        match = _match_exact(identity.product_id, identity.association_code, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(product_id+association_code)")

    if identity.product_id:
        attempts.append("mapping(product_id)")
        match = _match_product(identity.product_id, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(product_id)")

    if identity.association_code:
        attempts.append("mapping(association_code)")
        match = _match_association(identity.association_code, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(association_code)")

    if identity.custodian_name_chinese:
        attempts.append("mapping(custodian_name_chinese)")
        match = _match_custodian_name(identity.custodian_name_chinese, mappings)
        if match is not None:
            return _success_decision(source_file, identity, match, "mapping(custodian_name_chinese)")

    detail = _build_failure_message(identity, attempts)

    return RouteDecision(
        source_file=source_file,
        product_id=identity.product_id,
        association_code=identity.association_code,
        custodian_name_chinese=identity.custodian_name_chinese,
        custodian_id=None,
        custodian_name=None,
        adapter_key=None,
        route_source="unresolved",
        route_status="failed",
        route_message=detail,
    )


def _build_failure_message(identity: ProductIdentity, attempts: list[str]) -> str:
    resolved_parts = []
    if identity.product_id:
        resolved_parts.append(f"product_id={identity.product_id}")
    if identity.association_code:
        resolved_parts.append(f"association_code={identity.association_code}")
    if identity.custodian_name_chinese:
        resolved_parts.append(f"custodian_name_chinese={identity.custodian_name_chinese}")

    if not resolved_parts:
        return identity.route_message

    attempt_text = ", ".join(attempts) if attempts else "no routing strategy attempted"
    resolved_text = ", ".join(resolved_parts)
    return f"identity resolved ({resolved_text}) but no active mapping matched; tried {attempt_text}"


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


def _match_custodian_name(custodian_name_chinese: str, mappings: list[MappingRecord]) -> MappingRecord | None:
    canonical_name = _normalize_custodian_name(custodian_name_chinese)
    for mapping in mappings:
        if _normalize_custodian_name(mapping.true_custodian_name) == canonical_name:
            return mapping
    return None


def _normalize_custodian_name(name: str | None) -> str | None:
    if not name:
        return None
    if "国泰" in name:
        return "国泰海通证券股份有限公司"
    return name.strip()


def _success_decision(
    source_file: str,
    identity: ProductIdentity,
    mapping: MappingRecord,
    route_source: str,
) -> RouteDecision:
    canonical_custodian_name_chinese = _normalize_custodian_name(mapping.true_custodian_name) or _normalize_custodian_name(identity.custodian_name_chinese)
    return RouteDecision(
        source_file=source_file,
        product_id=identity.product_id,
        association_code=identity.association_code,
        custodian_name_chinese=canonical_custodian_name_chinese,
        custodian_id=mapping.custodian_id,
        custodian_name=mapping.custodian_name,
        adapter_key=mapping.adapter_key,
        route_source=route_source,
        route_status="success",
        route_message=f"matched {mapping.custodian_id} via {route_source}",
    )
