from valuation_parser.adapters.base import build_positions_and_review_items
from valuation_parser.models import SubjectRecord


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
