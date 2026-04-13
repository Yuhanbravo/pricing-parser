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


def test_pipeline_writes_non_empty_outputs_for_greatwall_sample(tmp_path: Path) -> None:
    sample_file = Path("data_samples/raw/证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx")
    output_dir = tmp_path / "output"

    outputs = run_pipeline(sample_file, Path("产品与托管机构映射表.csv"), output_dir)

    subjects_content = outputs["valuation_subjects"].read_text(encoding="utf-8-sig")
    positions_content = outputs["valuation_positions"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "11028101H02208" in subjects_content
    assert "02208.HK" in positions_content
    assert "Subject rows exported: 48" in summary_content
    assert "Position rows exported: 2" in summary_content


def test_pipeline_writes_non_empty_outputs_for_xyzc_sample(tmp_path: Path) -> None:
    sample_file = Path("data_samples/raw/20250327_PRODUCT_002_证券投资基金估值表.xls")
    output_dir = tmp_path / "output"

    outputs = run_pipeline(sample_file, Path("产品与托管机构映射表.csv"), output_dir)

    routing_content = outputs["routing_results"].read_text(encoding="utf-8-sig")
    subjects_content = outputs["valuation_subjects"].read_text(encoding="utf-8-sig")
    positions_content = outputs["valuation_positions"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "xyzc" in routing_content
    assert "11020101600309" in subjects_content
    assert "600309.SH" in positions_content
    assert "00700.HK" in positions_content
    assert "Position rows exported: " in summary_content