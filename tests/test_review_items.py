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

    positions, review_items = build_positions_and_review_items([derivative_subject, non_derivative_subject])

    assert len(positions) == 2
    assert any(item.subject_code == "3102A101000002" for item in review_items)
    assert any(item.review_reason == "衍生工具科目，需单独建模或排除" for item in review_items)
    assert all(item.subject_code != "600000" for item in review_items)
