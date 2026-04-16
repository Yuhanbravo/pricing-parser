from pathlib import Path

from valuation_parser.pipeline import run_pipeline


def test_pipeline_writes_phase0_outputs(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    sample_file = raw_dir / "2025-03-27_PRODUCT_001估值表.csv"
    sample_file.write_text("header,value\nproduct,PRODUCT_001\n", encoding="utf-8-sig")

    mapping_path = tmp_path / "mapping.csv"
    mapping_path.write_text(
        "fake_custodian_id,fake_custodian_name,true_custodian_name,product_count,fake_product_ids,fake_association_codes\n"
        "CUSTODIAN_007,CUSTODIAN_GROUP_007,国信证券股份有限公司,1,PRODUCT_001,XXX001\n",
        encoding="utf-8-sig",
    )

    output_dir = tmp_path / "output"
    outputs = run_pipeline(raw_dir, mapping_path, output_dir)

    routing_csv = outputs["routing_results"]
    assert routing_csv.exists()
    content = routing_csv.read_text(encoding="utf-8-sig")
    assert "CUSTODIAN_007" in content
    assert "guosen" in content
    assert outputs["parse_summary"].exists()
    assert outputs["phase3_workbook"].exists()


def test_pipeline_writes_non_empty_outputs_for_greatwall_sample(tmp_path: Path) -> None:
    sample_file = Path("data_samples/raw/证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx")
    output_dir = tmp_path / "output"

    outputs = run_pipeline(sample_file, Path("产品与托管机构映射表.csv"), output_dir)

    subjects_content = outputs["valuation_subjects"].read_text(encoding="utf-8-sig")
    positions_content = outputs["valuation_positions"].read_text(encoding="utf-8-sig")
    review_content = outputs["review_items"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "broker,sheet_name,valuation_date,raw_row_index,subject_code" in subjects_content
    assert "11028101H02208" in subjects_content
    assert "02208.HK" in positions_content
    assert "review_reason" in review_content
    assert "Subject rows exported: 48" in summary_content
    assert "Position rows exported: 2" in summary_content
    assert "Review items exported:" in summary_content
    assert outputs["phase3_workbook"].exists()


def test_pipeline_writes_non_empty_outputs_for_xyzc_sample(tmp_path: Path) -> None:
    sample_file = Path("data_samples/raw/20250327_PRODUCT_002_证券投资基金估值表.xls")
    output_dir = tmp_path / "output"

    outputs = run_pipeline(sample_file, Path("产品与托管机构映射表.csv"), output_dir)

    routing_content = outputs["routing_results"].read_text(encoding="utf-8-sig")
    subjects_content = outputs["valuation_subjects"].read_text(encoding="utf-8-sig")
    positions_content = outputs["valuation_positions"].read_text(encoding="utf-8-sig")
    review_content = outputs["review_items"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "xyzc" in routing_content
    assert "broker,sheet_name,valuation_date,raw_row_index,subject_code" in subjects_content
    assert "11020101600309" in subjects_content
    assert "600309.SH" in positions_content
    assert "00700.HK" in positions_content
    assert "review_reason" in review_content
    assert "Position rows exported: " in summary_content
    assert "Review items exported:" in summary_content
    assert outputs["phase3_workbook"].exists()


def test_pipeline_writes_non_empty_outputs_for_phase4_samples(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    sample_names = [
        "PRODUCT_006_资产估值表_20250327.xls",
        "PRODUCT_010_证券投资基金估值表_2025-03-27.xls",
        "PRODUCT_012_估值表_20250327.xls",
    ]
    for sample_name in sample_names:
        source = Path("data_samples/raw") / sample_name
        (raw_dir / sample_name).write_bytes(source.read_bytes())

    output_dir = tmp_path / "output"
    outputs = run_pipeline(raw_dir, Path("产品与托管机构映射表.csv"), output_dir)

    routing_content = outputs["routing_results"].read_text(encoding="utf-8-sig")
    positions_content = outputs["valuation_positions"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "citics" in routing_content
    assert "orient" in routing_content
    assert "gtja" in routing_content
    assert "600036.SH" in positions_content
    assert "00700.HK" in positions_content
    assert "000333.SZ" in positions_content
    assert "Processed files: 3" in summary_content


def test_pipeline_writes_non_empty_outputs_for_full_phase5_raw_set(tmp_path: Path) -> None:
    output_dir = tmp_path / "output_phase5"

    outputs = run_pipeline(Path("data_samples/raw"), Path("产品与托管机构映射表.csv"), output_dir)

    routing_content = outputs["routing_results"].read_text(encoding="utf-8-sig")
    positions_content = outputs["valuation_positions"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "guosen" in routing_content
    assert "cmsc" in routing_content
    assert "csc" in routing_content
    assert "layout_fallback(generic)" in routing_content
    assert "688617.SH" in positions_content
    assert "600309.SH" in positions_content
    assert "002475.SZ" in positions_content
    assert "Processed files: 11" in summary_content
    assert "Routing failures: 0" in summary_content