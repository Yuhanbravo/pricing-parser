from pathlib import Path

from valuation_parser.exporters import write_summary
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
    failed_route = RouteDecision(
        source_file="unmapped.xlsx",
        product_id="PRODUCT_022",
        association_code="XXX022",
        custodian_name_chinese=None,
        custodian_id=None,
        custodian_name=None,
        route_status="failed",
        route_source="mapping(product_id)",
        adapter_key=None,
        route_message="No active mapping record matched the extracted identity",
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
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        raw_row_index=1,
        subject_code="3102A101000002",
        subject_name="场外期权",
        review_reason="衍生工具科目，需单独建模或排除",
    )
    normalization_position = PositionRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        sheet_name="估值表",
        valuation_date="2025-03-27",
        instrument_name="无代码资产",
        subject_code="1102A199000001",
        subject_name="无代码资产",
        raw_row_index=2,
        review_flag="1",
        review_note="缺少可标准化的证券代码；叶子行存在数量但缺少市价",
    )

    write_summary(
        summary_path,
        files_processed=2,
        routes=[route, failed_route],
        subjects=[flagged_subject, clean_subject],
        positions=[flagged_position, normalization_position],
        review_items=[review_item],
    )

    content = summary_path.read_text(encoding="utf-8")

    assert "Processed files: 2" in content
    assert "Routing failures: 1" in content
    assert "Review flagged subjects: 1" in content
    assert "Review flagged positions: 2" in content
    assert "Unrouted files: unmapped.xlsx" in content
    assert "## Unrouted File Details" in content
    assert "- unmapped.xlsx" in content
    assert "## Unrecognized Object Index" in content
    assert "source_file=unmapped.xlsx; product_id=PRODUCT_022; association_code=XXX022; route_message=No active mapping record matched the extracted identity" in content
    assert "Generic fallback routes used: 0" in content
    assert "Fallback note: generic fallback runs only when --allow-generic-fallback is explicitly enabled." in content
    assert "Review entrypoint: first inspect the Review Entry Index below, then open valuation_subjects.csv / valuation_positions.csv rows with review_flag=1 and use review_items.csv.review_reason / valuation_positions.csv.review_note for concrete reasons." in content
    assert "## Review Entry Index" in content
    assert "source_file=sample.xlsx; raw_row_index=1; subject_code=3102A101000002; subject_name=场外期权; entrypoint=subject; reasons=衍生工具科目，需单独建模或排除" in content
    assert "source_file=sample.xlsx; raw_row_index=2; subject_code=1102A199000001; subject_name=无代码资产; entrypoint=position; reasons=叶子行存在数量但缺少市价；缺少可标准化的证券代码" in content
    assert "## Review Queue By Source File" in content
    assert "- sample.xlsx: 2 review entries; top reasons:" in content
    assert "缺少可标准化的证券代码 (1)" in content
    assert "叶子行存在数量但缺少市价 (1)" in content
    assert "衍生工具科目，需单独建模或排除 (1)" in content


def test_write_summary_deduplicates_review_entries_when_subject_and_instrument_names_differ(tmp_path: Path) -> None:
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
    review_item = ReviewItem(
        source_file="sample.xlsx",
        broker="测试券商",
        valuation_date="2025-03-27",
        raw_row_index=8,
        subject_code="1102.05.01.600000",
        subject_name="交易性金融资产",
        review_reason="人工复核科目映射",
    )
    flagged_position = PositionRecord(
        source_file="sample.xlsx",
        broker="测试券商",
        sheet_name="估值表",
        valuation_date="2025-03-27",
        instrument_name="浦发银行",
        subject_code="1102.05.01.600000",
        subject_name="交易性金融资产",
        raw_row_index=8,
        review_flag="1",
        review_note="缺少可标准化的证券代码",
    )

    write_summary(
        summary_path,
        files_processed=1,
        routes=[route],
        subjects=[],
        positions=[flagged_position],
        review_items=[review_item],
    )

    content = summary_path.read_text(encoding="utf-8")

    assert (
        "source_file=sample.xlsx; raw_row_index=8; subject_code=1102.05.01.600000; "
        "subject_name=交易性金融资产; entrypoint=position+subject; "
        "reasons=人工复核科目映射；缺少可标准化的证券代码"
    ) in content
    assert "- sample.xlsx: 1 review entries; top reasons:" in content
    assert "人工复核科目映射 (1)" in content
    assert "缺少可标准化的证券代码 (1)" in content