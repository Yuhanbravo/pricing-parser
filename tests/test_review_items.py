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
    assert len(positions) == 2
    assert any(item.subject_code == "3102A101000002" for item in review_items)
    assert any(item.review_reason == "衍生工具科目，需单独建模或排除" for item in review_items)
    assert all(item.subject_code != "600000" for item in review_items)
    derivative_position = next(position for position in positions if position.subject_code == "3102A101000002")
    non_derivative_position = next(position for position in positions if position.subject_code == "600000")
    derivative_subject_row = next(subject for subject in subjects if subject.subject_code == "3102A101000002")
    assert derivative_position.review_flag == "1"
    assert derivative_position.review_note == "衍生工具科目，需单独建模或排除"
    assert derivative_subject_row.review_flag == "1"
    assert non_derivative_position.review_flag is None


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
    assert review_items == []


def test_build_positions_and_review_items_emits_review_candidate_as_position() -> None:
    subject = SubjectRecord(
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
    )

    subjects, positions, review_items = build_positions_and_review_items([subject])

    assert subjects[0].review_flag == "1"
    assert len(positions) == 1
    assert positions[0].instrument_code_raw == "02899"
    assert positions[0].review_flag == "1"
    assert positions[0].review_note == "叶子行存在市价但缺少数量"
    assert review_items[0].review_reason == "叶子行存在市价但缺少数量"


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
