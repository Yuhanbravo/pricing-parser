from valuation_parser.product_identity import extract_product_identity


def test_extract_product_identity_from_multiple_filename_variants() -> None:
    first = extract_product_identity("2025-03-27_PRODUCT_001估值表.xlsx")
    second = extract_product_identity("估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx")
    third = extract_product_identity("PRODUCT_008委托资产资产估值表20250327.xls")

    assert first.product_id == "PRODUCT_001"
    assert second.product_id == "PRODUCT_022"
    assert second.association_code == "XXX022"
    assert third.product_id == "PRODUCT_008"
