from valuation_parser.normalizers import normalize_security_code


def test_normalize_security_code_variants() -> None:
    assert normalize_security_code("600109") == ("600109.SH", "SH", None)
    assert normalize_security_code("000560") == ("000560.SZ", "SZ", None)
    assert normalize_security_code("9926") == ("9926", None, "unknown_exchange")
    assert normalize_security_code("09926") == ("09926.HK", "HK", None)
