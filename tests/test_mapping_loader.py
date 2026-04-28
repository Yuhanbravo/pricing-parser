from pathlib import Path

from openpyxl import Workbook
import pytest

from valuation_parser.mapping_loader import load_mapping
from valuation_parser.pipeline import run_pipeline


def test_load_compact_mapping_csv(tmp_path: Path) -> None:
    mapping_path = tmp_path / "mapping.csv"
    mapping_path.write_text(
        "fake_custodian_id,fake_custodian_name,true_custodian_name,product_count,fake_product_ids,fake_association_codes\n"
        "CUSTODIAN_007,CUSTODIAN_GROUP_007,国信证券股份有限公司,1,PRODUCT_001,XXX001\n",
        encoding="utf-8-sig",
    )

    records = load_mapping(mapping_path)

    assert len(records) == 1
    assert records[0].product_id == "PRODUCT_001"
    assert records[0].association_code == "XXX001"
    assert records[0].adapter_key == "guosen"
    assert records[0].true_custodian_name == "国信证券股份有限公司"


def test_load_mapping_rejects_unregistered_adapter_key(tmp_path: Path) -> None:
    mapping_path = tmp_path / "mapping.csv"
    mapping_path.write_text(
        "product_id,association_code,custodian_id,custodian_name,adapter_key\n"
        "PRODUCT_001,XXX001,CUSTODIAN_001,CUSTODIAN_GROUP_001,not_registered\n",
        encoding="utf-8-sig",
    )

    with pytest.raises(ValueError, match="Unsupported adapter_key"):
        load_mapping(mapping_path)


def test_load_canonical_mapping_xlsx(tmp_path: Path) -> None:
    mapping_path = tmp_path / "mapping.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "mapping"
    worksheet.append(["product_id", "association_code", "custodian_id", "custodian_name", "adapter_key", "is_active", "note"])
    worksheet.append(["PRODUCT_023", "XXX023", "CUSTODIAN_023", "长城证券股份有限公司", "greatwall", "true", "xlsx regression"])
    workbook.save(mapping_path)

    records = load_mapping(mapping_path)

    assert len(records) == 1
    assert records[0].product_id == "PRODUCT_023"
    assert records[0].association_code == "XXX023"
    assert records[0].custodian_id == "CUSTODIAN_023"
    assert records[0].adapter_key == "greatwall"
    assert records[0].note == "xlsx regression"


def test_pipeline_accepts_canonical_mapping_xlsx(tmp_path: Path) -> None:
    mapping_path = tmp_path / "mapping.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "mapping"
    worksheet.append(["product_id", "association_code", "custodian_id", "custodian_name", "adapter_key", "is_active", "note"])
    worksheet.append(["PRODUCT_023", "XXX023", "CUSTODIAN_023", "长城证券股份有限公司", "greatwall", "true", "xlsx pipeline regression"])
    workbook.save(mapping_path)

    output_dir = tmp_path / "output"
    outputs = run_pipeline(Path("data_samples/raw/证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx"), mapping_path, output_dir)

    routing_content = outputs["routing_results"].read_text(encoding="utf-8-sig")
    summary_content = outputs["parse_summary"].read_text(encoding="utf-8")

    assert "greatwall" in routing_content
    assert "Routing failures: 0" in summary_content
    assert "Unrouted files: none" in summary_content
