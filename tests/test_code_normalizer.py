from valuation_parser.normalizers import derive_broker_name, infer_asset_type, normalize_security_code, resolve_review_flag


def test_normalize_security_code_variants() -> None:
    assert normalize_security_code("600109") == ("600109.SH", "SH", None)
    assert normalize_security_code("000560") == ("000560.SZ", "SZ", None)
    assert normalize_security_code("511360") == ("511360.SH", "SH", None)
    assert normalize_security_code("9926") == ("09926.HK", "HK", None)
    assert normalize_security_code("09926") == ("09926.HK", "HK", None)


def test_infer_asset_type_variants() -> None:
    assert infer_asset_type("600109", "SH") == "a_share"
    assert infer_asset_type("000560", "SZ") == "a_share"
    assert infer_asset_type("511360", "SH") == "fund_or_etf"
    assert infer_asset_type("09926", "HK") == "hk_equity"
    assert infer_asset_type("ABC", None) is None


def test_resolve_review_flag_prefers_normalization_error() -> None:
    assert resolve_review_flag("missing_code", None) == "missing_code"
    assert resolve_review_flag(None, None) == "unknown_asset_type"
    assert resolve_review_flag(None, "a_share", "叶子行存在数量但缺少市价") == "manual_review_required"
    assert resolve_review_flag(None, "a_share") is None


def test_derive_broker_name_prefers_custodian_name() -> None:
    assert derive_broker_name("长江证券", "xyzc") == "长江证券"
    assert derive_broker_name(None, "xyzc") == "xyzc"
    assert derive_broker_name(None, None) is None
