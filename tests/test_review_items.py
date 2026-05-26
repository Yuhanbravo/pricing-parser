import pytest

from valuation_parser.adapters.base import build_positions_and_review_items
from valuation_parser.models import SubjectRecord


@pytest.fixture(params=[
    {
        "subject": SubjectRecord(
            source_file="sample.xlsx",
            broker="测试券商",
            valuation_date="2025-03-27",
            subject_code="11028101H02899",
            subject_name="紫金矿业",
            quantity=None,
            unit_cost=17.14,
            cost=411464.85,
            market_price=16.67,
            market_value=400009.10,
            pnl=-11455.75,
            is_leaf=True,
            is_position_candidate=False,
        ),
        "asset_type": "hk_equity",
        "instrument_code_raw": "02899",
        "instrument_code_std": "02899.HK",
        "exchange": "HK",
        "review_reason": "叶子行存在市价但缺少数量",
    },
    {
        "subject": SubjectRecord(
            source_file="sample.xlsx",
            broker="测试券商",
            valuation_date="2025-03-27",
            subject_code="11020101600309",
            subject_name="万华化学",
            quantity=None,
            unit_cost=68.53,
            cost=1117039.0,
            market_price=75.04,
            market_value=1223155.0,
            pnl=-106116.0,
            is_leaf=True,
            is_position_candidate=False,
        ),
        "asset_type": "a_share",
        "instrument_code_raw": "600309",
        "instrument_code_std": "600309.SH",
        "exchange": "SH",
        "review_reason": "叶子行存在市价但缺少数量",
    },
    {
        "subject": SubjectRecord(
            source_file="sample.xlsx",
            broker="测试券商",
            valuation_date="2025-03-27",
            subject_code="11050201512000",
            subject_name="华宝中证全指证券公司ETF",
            quantity=70000.0,
            unit_cost=1.09,
            cost=76080.0,
            market_price=None,
            market_value=74130.0,
            pnl=-1950.0,
            is_leaf=True,
            is_position_candidate=True,
        ),
        "asset_type": "fund_or_etf",
        "instrument_code_raw": "512000",
        "instrument_code_std": "512000.SH",
        "exchange": "SH",
        "review_reason": "叶子行存在数量但缺少市价",
    },
])
def non_derivative_position_review_subject(request: pytest.FixtureRequest) -> dict[str, object]:
    return request.param


def test_build_positions_and_review_items_marks_derivative_subjects_for_review() -> None:
    derivative_subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        subject_code="3102A101000002",
        subject_name="中信证券20221024@场外期权",
        quantity=1,
        unit_cost=1.0,
        cost=1.0,
        market_price=1.0,
        market_value=1.0,
        pnl=0.0,
        is_leaf=True,
        is_position_candidate=True,
    )
    non_derivative_subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        subject_code="600000",
        subject_name="普通股票",
        quantity=1,
        unit_cost=1.0,
        cost=1.0,
        market_price=1.0,
        market_value=1.0,
        pnl=0.0,
        is_leaf=True,
        is_position_candidate=True,
    )

    subjects, positions, review_items = build_positions_and_review_items([derivative_subject, non_derivative_subject])

    assert len(subjects) == 2
    assert len(positions) == 1
    assert any(item.subject_code == "3102A101000002" for item in review_items)
    assert any(item.review_reason == "衍生工具科目，需单独建模或排除" for item in review_items)
    assert all(item.subject_code != "600000" for item in review_items)
    derivative_review_item = next(item for item in review_items if item.subject_code == "3102A101000002")
    non_derivative_position = next(position for position in positions if position.subject_code == "600000")
    derivative_subject_row = next(subject for subject in subjects if subject.subject_code == "3102A101000002")
    assert derivative_subject_row.review_flag == "1"
    assert derivative_subject_row.asset_type_internal == "derivative_swap"
    assert derivative_subject_row.review_category == "derivative_review"
    assert derivative_review_item.asset_type_internal == "derivative_swap"
    assert derivative_review_item.asset_type_display == "收益互换"
    assert derivative_review_item.review_category == "derivative_review"
    assert derivative_review_item.review_note == "衍生工具科目，需单独建模或排除"
    assert all(position.subject_code != "3102A101000002" for position in positions)
    assert non_derivative_position.review_flag is None
    assert non_derivative_position.asset_type_internal == "equity_a_share"
    assert non_derivative_position.asset_type_display == "A股股票"


def test_build_positions_and_review_items_does_not_flag_real_position_codes_ending_in_99() -> None:
    subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        subject_code="11028101H02899",
        subject_name="紫金矿业",
        quantity=24000,
        unit_cost=17.14,
        cost=411464.85,
        market_price=16.67,
        market_value=400009.10,
        pnl=-11455.75,
        suspension_info="【正常交易】",
        is_leaf=True,
        is_position_candidate=True,
    )

    subjects, positions, review_items = build_positions_and_review_items([subject])

    assert subjects[0].review_flag is None
    assert positions[0].review_flag is None
    assert positions[0].suspension_info == "正常交易"
    assert subjects[0].asset_type_internal == "equity_hk"
    assert positions[0].asset_type_internal == "equity_hk"
    assert review_items == []


def test_build_positions_and_review_items_marks_non_derivative_review_position(
    non_derivative_position_review_subject: dict[str, object],
) -> None:
    subject = non_derivative_position_review_subject["subject"]
    asset_type = non_derivative_position_review_subject["asset_type"]
    instrument_code_raw = non_derivative_position_review_subject["instrument_code_raw"]
    instrument_code_std = non_derivative_position_review_subject["instrument_code_std"]
    exchange = non_derivative_position_review_subject["exchange"]
    review_reason = non_derivative_position_review_subject["review_reason"]

    assert isinstance(subject, SubjectRecord)

    subjects, positions, review_items = build_positions_and_review_items([subject])

    assert subjects[0].review_flag == "1"
    assert len(positions) == 1
    assert positions[0].asset_type == asset_type
    assert positions[0].instrument_code_raw == instrument_code_raw
    assert positions[0].instrument_code_std == instrument_code_std
    assert positions[0].exchange == exchange
    assert positions[0].review_flag == "1"
    assert positions[0].review_note == review_reason
    assert review_items[0].review_reason == review_reason


def test_build_positions_and_review_items_preserves_normalization_reason_in_review_note() -> None:
    subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        subject_code="1102A1MISSING",
        subject_name="无代码资产",
        quantity=100.0,
        unit_cost=1.0,
        cost=100.0,
        market_price=1.2,
        market_value=120.0,
        pnl=20.0,
        is_leaf=True,
        is_position_candidate=True,
    )

    _, positions, _ = build_positions_and_review_items([subject])

    assert positions[0].review_flag == "1"
    assert positions[0].review_note == "缺少可标准化的证券代码"


def test_build_positions_and_review_items_does_not_promote_cash_review_rows_into_positions() -> None:
    subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        subject_code="10020101",
        subject_name="银行结算账户",
        quantity=0.0,
        cost=786526.32,
        market_price=0.0,
        market_value=786526.32,
        pnl=0.0,
        is_leaf=True,
        is_position_candidate=False,
    )

    subjects, positions, review_items = build_positions_and_review_items([subject])

    assert subjects[0].review_flag == "1"
    assert positions == []
    assert review_items[0].review_reason == "叶子行存在市价但缺少数量"


def test_build_positions_and_review_items_keeps_estimated_gain_summary_out_of_positions() -> None:
    subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        subject_code="11028199",
        subject_name="沪港通股票估增",
        quantity=0.0,
        cost=1198715.79,
        market_value=1198715.79,
        pnl=0.0,
        is_leaf=True,
        is_position_candidate=False,
    )

    subjects, positions, review_items = build_positions_and_review_items([subject])

    assert subjects[0].review_flag == "1"
    assert positions == []
    assert review_items[0].review_reason == "估值增值汇总行，通常不作为持仓叶子"
