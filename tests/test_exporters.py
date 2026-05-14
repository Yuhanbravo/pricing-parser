from pathlib import Path

from valuation_parser.exporters import write_positions, write_subjects, write_summary
from valuation_parser.models import PositionRecord, ReviewItem, RouteDecision, SubjectRecord


def test_write_summary_reports_flagged_subjects_and_positions_separately(tmp_path: Path) -> None:
    summary_path = tmp_path / "parse_summary.md"
    route = RouteDecision(
        source_file="sample.xlsx",
        product_id="PRODUCT_023",
        association_code="XXX023",
        custodian_name_chinese="长城证券",
        custodian_id="CUSTODIAN_023",
        custodian_name="长城证券股份有限公司",
        route_status="success",
        route_source="mapping(product_id)",
        adapter_key="greatwall",
        route_message="",
    )
    flagged_subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        sheet_name="估值表",
        valuation_date="2025-03-27",
        subject_code="3102A101000002",
        subject_name="场外期权",
        is_leaf=True,
        is_position_candidate=True,
        review_flag="1",
    )
    clean_subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        sheet_name="估值表",
        valuation_date="2025-03-27",
        subject_code="1102",
        subject_name="股票投资",
    )
    flagged_position = PositionRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        sheet_name="估值表",
        valuation_date="2025-03-27",
        instrument_name="场外期权",
        subject_code="3102A101000002",
        subject_name="场外期权",
        review_flag="1",
    )
    review_item = ReviewItem(
        broker="测试券商",
        valuation_date="2025-03-27",
        raw_row_index=1,
        subject_code="3102A101000002",
        subject_name="场外期权",
        review_reason="衍生工具科目，需单独建模或排除",
    )

    write_summary(
        summary_path,
        files_processed=1,
        routes=[route],
        subjects=[flagged_subject, clean_subject],
        positions=[flagged_position],
        review_items=[review_item],
    )

    content = summary_path.read_text(encoding="utf-8")

    assert "Review flagged subjects: 1" in content
    assert "Review flagged positions: 1" in content


def test_write_subjects_and_positions_include_taxonomy_columns(tmp_path: Path) -> None:
    subjects_path = tmp_path / "valuation_subjects.csv"
    positions_path = tmp_path / "valuation_positions.csv"

    subject = SubjectRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        subject_code="100201",
        subject_name="银行存款",
        review_flag=None,
        asset_type_internal="cash_deposit",
        asset_type_display="现金及存款",
        asset_class_l1="现金类",
        asset_class_l2="银行存款",
        review_category=None,
    )
    position = PositionRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        instrument_name="腾讯控股",
        instrument_code_raw="700",
        instrument_code_std="00700.HK",
        exchange="HK",
        asset_type="hk_equity",
        asset_type_internal="equity_hk",
        asset_type_display="港股",
        asset_class_l1="权益类",
        asset_class_l2="港股",
        subject_code="11028101H00700",
        subject_name="腾讯控股",
    )

    write_subjects(subjects_path, [subject])
    write_positions(positions_path, [position])

    subjects_content = subjects_path.read_text(encoding="utf-8-sig")
    positions_content = positions_path.read_text(encoding="utf-8-sig")

    assert "asset_type_internal,asset_type_display,asset_class_l1,asset_class_l2,review_category" in subjects_content
    assert "cash_deposit,现金及存款,现金类,银行存款," in subjects_content
    assert "asset_type,asset_type_internal,asset_type_display,asset_class_l1,asset_class_l2" in positions_content
    assert "hk_equity,equity_hk,港股,权益类,港股" in positions_content