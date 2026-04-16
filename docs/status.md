# Project Status

## Current Phase

- Current milestone: Phase 3 delivery completed.
- Real adapters implemented and verified in the latest run: `greatwall`, `xyzc`.
- Placeholder adapters still remain for unsupported custodians.

## Current Snapshot

- Routing, parsing, normalization, and export are working end to end on the two verified real samples.
- Phase 3 outputs now include `review_items.csv` and `phase3_outputs.xlsx` in addition to the standard CSV and markdown exports.
- Latest parse summary reports: 2 processed files, 2 successful routes, 184 subject rows, 19 position rows, 8 review items, and 0 normalization issues.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping-table lookup, and optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; real parsing is currently verified on one `greatwall` sample and one `xyzc` sample.
- Current standardized position coverage includes the equity-style and derivative rows surfaced by the two verified samples.

## Repository Rules

- This repository stores project code, tests, configs, and project-facing documentation only.
- `ai_skill_hub` must remain a separate sibling repository imported via Git bundle.
- New raw `.xls`, `.xlsx`, and `.csv` samples are not committed by default.
- Generated outputs belong in ignored directories such as `output/` or `tmp/`.

## Known Gaps

- Additional raw sample formats still need explicit verification before they can be considered supported.
- `asset_type` terminology still needs refinement to match downstream workbook language more closely.
- Shared review logic exists now, but broader regression coverage is still needed for more asset classes and edge cases.
- Some historical sample files still exist in the repository and should be revisited under the sample-data policy.

## Recommended Next Steps

1. Expand coverage to more verified custodian samples before onboarding the next real adapter.
2. Tighten `asset_type` naming against the expected workbook vocabulary.
3. Add regression checks for review-item generation and workbook-export consistency.
4. Revisit tracked sample files and decide which fixtures remain in Git.
