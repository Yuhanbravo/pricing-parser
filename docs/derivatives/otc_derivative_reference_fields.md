# OTC Derivative Reference Fields

## Contract-Level Candidate Fields

- `source_file`
- `product_id`
- `subject_code`
- `subject_name`
- `account_code_std`
- `account_name_std`
- `derivative_type`
- `contract_name`
- `contract_id`
- `counterparty`
- `trade_direction`
- `notional_amount`
- `market_value`
- `cost`
- `valuation_appreciation`
- `margin_amount`
- `settlement_amount`
- `maturity_date`
- `valuation_method_hint`
- `review_flag`
- `review_category`
- `review_note`

## Underlying-Exposure Candidate Fields

- `contract_id`
- `underlying_type`
- `underlying_code`
- `underlying_name`
- `underlying_market`
- `underlying_quantity`
- `underlying_price`
- `notional_exposure`
- `delta_adjusted_exposure`
- `long_short`
- `lookthrough_confidence`

## Availability Constraint

The valuation table alone often exposes only partial information such as subject names, market value, valuation appreciation, or margin-like balances. Round 5A therefore treats many fields as review-driven or supplemental-data-driven rather than guaranteed parser outputs.
