from valuation_parser.taxonomy import classify_position_taxonomy, classify_subject_taxonomy, load_asset_taxonomy


def test_load_asset_taxonomy_reads_expected_entries() -> None:
    taxonomy = load_asset_taxonomy()

    known = taxonomy.resolve("fund_exchange_traded")
    unknown = taxonomy.resolve(None)

    assert known.asset_type_display == "场内基金/ETF"
    assert known.asset_class_l1 == "基金类"
    assert known.include_in_positions is True
    assert unknown.asset_type_internal == "unknown"
    assert unknown.review_category == "unknown_subject"


def test_classify_position_taxonomy_maps_legacy_asset_types() -> None:
    hk_equity = classify_position_taxonomy(
        asset_type="hk_equity",
        instrument_code_raw="700",
        exchange="HK",
        subject_code="11028101H00700",
        subject_name="腾讯控股",
    )
    etf = classify_position_taxonomy(
        asset_type="fund_or_etf",
        instrument_code_raw="510300",
        exchange="SH",
        subject_code="11020101510300",
        subject_name="沪深300ETF",
    )

    assert hk_equity.asset_type_internal == "equity_hk"
    assert hk_equity.asset_type_display == "港股"
    assert etf.asset_type_internal == "fund_exchange_traded"
    assert etf.asset_class_l1 == "基金类"


def test_classify_position_taxonomy_splits_star_and_cdr() -> None:
    star = classify_position_taxonomy(
        asset_type="a_share",
        instrument_code_raw="688981",
        exchange="SH",
        subject_code="11020101688981",
        subject_name="中芯国际",
    )
    cdr = classify_position_taxonomy(
        asset_type="a_share",
        instrument_code_raw="689009",
        exchange="SH",
        subject_code="11020101689009",
        subject_name="九号公司存托凭证",
    )

    assert star.asset_type_internal == "equity_star"
    assert cdr.asset_type_internal == "cdr"


def test_classify_subject_taxonomy_marks_derivative_and_unknown() -> None:
    derivative = classify_subject_taxonomy(
        subject_code="3102A101000002",
        subject_name="收益互换",
        review_reason="衍生工具科目，需单独建模或排除",
    )
    unknown = classify_subject_taxonomy(
        subject_code="999999",
        subject_name="未知科目",
    )

    assert derivative.asset_type_internal == "derivative_swap"
    assert derivative.review_category == "derivative_review"
    assert derivative.include_in_positions is False
    assert unknown.asset_type_internal == "unknown"
    assert unknown.review_category == "unknown_subject"


def test_classify_subject_taxonomy_marks_balance_sheet_items() -> None:
    cash = classify_subject_taxonomy(subject_code="100201", subject_name="银行存款")
    margin = classify_subject_taxonomy(subject_code="103103", subject_name="存出保证金")
    clearing = classify_subject_taxonomy(subject_code="102101", subject_name="证券清算款")
    payable = classify_subject_taxonomy(subject_code="220201", subject_name="应付款项")
    tax = classify_subject_taxonomy(subject_code="222101", subject_name="应交税费")

    assert cash.asset_type_internal == "cash_deposit"
    assert margin.asset_type_internal == "margin_deposit"
    assert clearing.asset_type_internal == "clearing_balance"
    assert payable.asset_type_internal == "payable"
    assert tax.asset_type_internal == "tax_payable"