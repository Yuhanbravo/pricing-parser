# Project Status

## Current Phase

- Current milestone: Phase 5 delivery completed.
- Latest bounded delivery verified the full `data_samples/raw/` set end to end with zero routing failures.
- Latest review-rule update now forces `3102*` derivative subjects into `review_items`.

## Current Snapshot

- Routing, parsing, normalization, and export are working end to end on the full 11-file controlled raw set.
- Latest validated outputs were generated under `output_phase5/` and include `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and workbook export `phase3_outputs.xlsx`.
- Latest parse summary reports: 11 processed files, 11 successful routes, 1113 subject rows, 202 position rows, 253 review items, and 0 normalization issues.
- Adapters present in the latest run: `citics`, `cmsc`, `csc`, `generic`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping-table lookup, and optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; parsing is now verified across the current 11-file raw fixture set.
- Verified adapters in the current bounded path are `citics`, `cmsc`, `csc`, `generic`, `greatwall`, `gtja`, `guosen`, `orient`, and `xyzc`.
- Shared review logic includes derivative-subject handling for `3102*` codes in addition to the existing position-derived review flow.

## Repository Rules

- This repository stores project code, tests, configs, and project-facing documentation only.
- `ai_skill_hub` must remain a separate sibling repository imported via Git bundle.
- New raw `.xls`, `.xlsx`, and `.csv` samples are not committed by default.
- Generated outputs belong in ignored directories such as `output/` or `tmp/`.

## Known Gaps

- `phase3_outputs.xlsx` remains the workbook artifact name even in `output_phase5/`; this is now a documented compatibility holdover rather than a Phase 3-only artifact.
- `asset_type` terminology still needs refinement to match downstream workbook language more closely.
- Shared review logic is broader now, but more regression coverage is still needed for additional asset classes and review reasons beyond the current fixture set.
- The repository does not currently use a `docs_readable/` derivative layer; if one is added later, it must remain non-authoritative.

## Recommended Next Steps

1. Decide whether to keep or rename `phase3_outputs.xlsx`, and if renaming is desired, do it with an explicit compatibility plan.
2. Tighten `asset_type` naming against the expected workbook vocabulary.
3. Add regression checks for review-item generation and workbook-export consistency beyond the current `3102*` rule.
4. Revisit tracked sample files and decide which fixtures remain in Git.
