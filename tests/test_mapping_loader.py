from pathlib import Path

from valuation_parser.mapping_loader import load_mapping


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
