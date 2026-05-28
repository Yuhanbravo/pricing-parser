# Accounting Subjects Mapping Design

## Design Goal

Round 5A defines the standard accounting subject layer as a reference and design layer. It does not wire the layer into parser runtime yet.

## Required Field Order

The intended field layering remains:

1. `subject_code` and `subject_name`
2. `account_code_std`, `account_name_std`, `account_class_std`
3. `asset_type_internal`, `asset_class_l1`, `asset_class_l2`
4. `asset_type_display`

## Design Rules

### Rule 1: Raw valuation subjects remain traceable

The parser must continue to preserve raw subject information from the custodian valuation statement.

### Rule 2: Standard accounting subjects are a normalization base

The official-accounting layer improves standardization, audit traceability, and later rule design. It is not a direct replacement for the Round 4 taxonomy layer.

### Rule 3: Asset taxonomy still controls position inclusion

Whether a row enters ordinary `valuation_positions.csv` remains a taxonomy and business-rule question, not a direct consequence of being a standard accounting subject.

Examples:

- 1031 存出保证金: standard subject yes, ordinary position no
- 3003 证券清算款: standard subject yes, ordinary position no
- 2203/2206/2207/2208/2221: standard subject yes, ordinary position no
- 1102/1103/1104/1105: standard subject yes, may map onward to ordinary investment displays depending on taxonomy

### Rule 4: Derivative-related entries branch out

Derivative-related entries should flow to a future OTC derivative subsystem or review queue when the valuation table does not provide enough contract-level detail.

## Deferred Runtime Work

The following is intentionally deferred to Round 5B or later:

- runtime addition of `account_code_std` or similar output columns
- parser-side mapping execution
- widening existing CSV export contracts
- automatic valuation-method logic
- OTC lookthrough implementation
