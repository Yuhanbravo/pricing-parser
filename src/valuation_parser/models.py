from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class WorkbookPreview:
    sheet_names: list[str] = field(default_factory=list)
    header_texts: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProductIdentity:
    product_id: str | None = None
    association_code: str | None = None
    custodian_name_chinese: str | None = None
    route_message: str = ""
    evidence: tuple[str, ...] = ()

    @property
    def is_resolved(self) -> bool:
        return bool(self.product_id or self.association_code)


@dataclass(frozen=True)
class MappingRecord:
    product_id: str | None
    association_code: str | None
    custodian_id: str
    custodian_name: str
    true_custodian_name: str | None
    adapter_key: str
    is_active: bool = True
    note: str | None = None


@dataclass(frozen=True)
class RouteDecision:
    source_file: str
    product_id: str | None
    association_code: str | None
    custodian_name_chinese: str | None
    custodian_id: str | None
    custodian_name: str | None
    adapter_key: str | None
    route_source: str
    route_status: str
    route_message: str

    def to_row(self) -> dict[str, str | None]:
        return asdict(self)


@dataclass(frozen=True)
class SubjectRecord:
    source_file: str
    broker: str | None = None
    sheet_name: str | None = None
    valuation_date: str | None = None
    product_id: str | None = None
    association_code: str | None = None
    custodian_id: str | None = None
    custodian_name: str | None = None
    adapter_key: str | None = None
    route_source: str | None = None
    subject_code: str | None = None
    subject_name: str | None = None
    parent_subject_code: str | None = None
    subject_level: int | None = None
    root_subject_code: str | None = None
    root_subject_name: str | None = None
    is_leaf: bool | None = None
    is_position_candidate: bool | None = None
    quantity: float | None = None
    unit_cost: float | None = None
    cost: float | None = None
    cost_pct_nav: float | None = None
    market_price: float | None = None
    market_value: float | None = None
    market_value_pct_nav: float | None = None
    pnl: float | None = None
    suspension_info: str | None = None
    review_flag: str | None = None
    raw_row_index: int | None = None
    raw_text: str | None = None

    def to_row(self) -> dict[str, object | None]:
        return asdict(self)


@dataclass(frozen=True)
class PositionRecord:
    source_file: str
    broker: str | None = None
    sheet_name: str | None = None
    valuation_date: str | None = None
    product_id: str | None = None
    association_code: str | None = None
    custodian_id: str | None = None
    custodian_name: str | None = None
    adapter_key: str | None = None
    route_source: str | None = None
    instrument_name: str | None = None
    instrument_code_raw: str | None = None
    instrument_code_std: str | None = None
    exchange: str | None = None
    asset_type: str | None = None
    quantity: float | None = None
    unit_cost: float | None = None
    cost: float | None = None
    market_price: float | None = None
    market_value: float | None = None
    unrealized_pnl: float | None = None
    subject_code: str | None = None
    subject_name: str | None = None
    raw_row_index: int | None = None
    suspension_info: str | None = None
    review_flag: str | None = None
    review_note: str | None = None

    def to_row(self) -> dict[str, object | None]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewItem:
    broker: str | None = None
    valuation_date: str | None = None
    raw_row_index: int | None = None
    subject_code: str | None = None
    subject_name: str | None = None
    quantity: float | None = None
    cost: float | None = None
    market_value: float | None = None
    pnl: float | None = None
    review_reason: str | None = None

    def to_row(self) -> dict[str, object | None]:
        return asdict(self)


@dataclass(frozen=True)
class ParseArtifacts:
    route: RouteDecision
    subjects: list[SubjectRecord] = field(default_factory=list)
    positions: list[PositionRecord] = field(default_factory=list)
    review_items: list[ReviewItem] = field(default_factory=list)
