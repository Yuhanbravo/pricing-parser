# Project Status

## Current Phase

- Current milestone: Phase 2 completed, preparing for Phase 3 rule convergence.
- Real adapters implemented: `greatwall`, `xyzc`.
- Placeholder adapters remain for unsupported custodians.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping table lookup, optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; real parsing currently verified on one `greatwall` sample and one `xyzc` sample.
- Current standardized position coverage: A-share and HK equity style codes present in the two verified samples.

## Repository Rules

- This repository stores project code, tests, configs, and project-facing documentation only.
- `ai_skill_hub` must remain a separate sibling repository imported via Git bundle.
- New raw `.xls/.xlsx/.csv` samples are not committed by default.
- Generated outputs belong in ignored directories such as `output/` or `tmp/`.

## Known Gaps

- Shared parsing helpers are still duplicated across the two real adapters.
- `normalize_security_code` and `asset_type` inference are still minimal.
- `review_flag` currently needs Phase 3 convergence into shared rules.
- Some historical sample files still exist in the repository and should be revisited under the new sample-data policy.

## Recommended Next Steps

1. Freeze the target output schema against the expected workbook in `data_samples/expected/`.
2. Extract shared subject and position parsing helpers into the common adapter layer.
3. Expand normalization and review rules with regression tests.
4. Revisit tracked sample files and decide which fixtures remain in Git.
