# Expected Baseline

This directory stores the current strict-default acceptance baseline for the evidence-chain closure round.

## Authoritative Files

- `routing_results.csv`: expected routing contract for the controlled 11-file run.
- `valuation_subjects.csv`: expected subjects export contract, including trace columns.
- `valuation_positions.csv`: expected positions export contract, including trace columns and review fields.
- `review_items.csv`: expected manual-review item export for the same run.
- `parse_summary.md`: expected markdown summary for the strict-default path.
- `估值表解析_output_2025-03-27.xlsx`: workbook baseline for the same run.

## Workbook Baseline

The expected workbook is checked as a full sheet-content baseline for the same strict-default run and should contain these sheets:

- `routing_results`
- `valuation_subjects`
- `valuation_positions`
- `review_items`

## Scope Note

This directory is the current baseline for evidence-chain verification. Historical output references such as `output_phase1/` may still appear in older review notes, but they are legacy snapshots rather than active external contract artifacts.

The paired markdown summary is also part of the active contract and is expected to expose both `Unrecognized Object Index` and `Review Entry Index` so reviewers can locate unresolved files and reviewable rows without rerunning the parser.