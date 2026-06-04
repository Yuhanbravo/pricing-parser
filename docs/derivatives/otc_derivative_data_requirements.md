# OTC Derivative Data Requirements

## What The Valuation Table Usually Gives

- subject code
- subject name
- market value or fair value balance
- valuation appreciation or depreciation
- partial cost or margin information
- occasional contract-like wording

## What Is Commonly Missing

- stable contract identifier
- counterparty
- notional amount
- trade direction
- underlying composition
- delta or equivalent exposure
- valuation methodology details
- maturity schedule

## Supplemental Data Likely Needed Later

- broker swap ledger
- OTC contract register
- trade confirmations
- derivative valuation detail files
- underlying basket lists
- margin statements
- counterparty daily reports

## Design Consequence

Round 5C and Round 5D should explicitly separate valuation-table recognition from full lookthrough. Round 5A only records the input requirements for that later work.
