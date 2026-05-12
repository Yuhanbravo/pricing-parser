# data_samples

`data_samples/` is a controlled fixture area, not the default home for day-to-day raw sample files.

## Policy

- New raw `.xls/.xlsx/.csv` valuation samples should stay outside the repository by default.
- Only intentionally curated,脱敏 and minimal fixtures may remain in Git when they are necessary for tests or expected-output comparison.
- Generated outputs should not be written back into this directory unless they are explicitly maintained expected artifacts.

## Suggested Layout

- `raw/`: historical or explicitly retained minimal fixtures only.
- `mapping/`: mapping format examples and README-style guidance.
- `expected/`: strict-default acceptance artifacts used to lock routing, CSV exports, markdown summary, and workbook-content regression behavior.

## Maintenance Rule

Before adding any new sample here, document why it must stay in Git and why a smaller or external local sample is insufficient.
