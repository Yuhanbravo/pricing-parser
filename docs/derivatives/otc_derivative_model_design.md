# OTC Derivative Model Design

## Round 5A Position

OTC derivatives are not modeled as a small extension of ordinary security positions. They should become a separate subsystem.

## Why A Separate Subsystem Is Needed

Ordinary security-position outputs focus on securities such as stocks, bonds, and funds with familiar fields like code, quantity, cost, price, market value, and valuation appreciation.

Derivative workflows care about a different object model:

- contract identifier
- derivative type
- counterparty
- underlying asset
- notional amount
- trade direction
- margin
- fair value
- floating PnL
- maturity date
- valuation method hint

The two models overlap partially but are not interchangeable.

## Recommended Future Outputs

- `derivative_contracts.csv`
- `derivative_underlying_exposures.csv`
- `derivative_review_items.csv`

## Level Split

### Level 1

Recognize that a valuation-table subject belongs to an OTC derivative contract candidate.

### Level 2

Use supplemental ledgers or counterparty data to look through to underlying exposures.

Round 5A only prepares the design inputs for this split.
