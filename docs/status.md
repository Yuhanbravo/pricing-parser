# Project Status

## Current Phase

- Current milestone: Phase 5 delivery with post-review contract alignment refresh.
- Latest bounded delivery verified the full `data_samples/raw/` set end to end under strict default routing, resulting in 1 retained routing failure instead of silent generic fallback success.
- Latest review-rule update still forces `3102*` derivative subjects into `review_items`, and matching position rows now carry `review_flag` as the manual-review entrypoint.

## Current Snapshot

- Routing, parsing, normalization, and export are working end to end on the full 11-file controlled raw set, with one sample intentionally left unresolved by default because it has no active mapping match.
- Latest validated outputs were generated under `output_phase6/` and include `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and workbook export `phase3_outputs.xlsx`.
- Latest parse summary reports: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 242 review items, and 0 normalization issues.
- Adapters hit in the latest run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Subjects and positions exports now preserve the trace fields required for audit and downstream reconciliation: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping-table lookup, and optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; parsing is verified across the current 11-file raw fixture set.
- Verified adapters in the current bounded path are `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, and `xyzc`; `generic` remains available only through explicit override or explicit fallback enablement.
- Shared review logic includes derivative-subject handling for `3102*` codes in addition to the existing position-derived review flow.

## Repository Rules

- This repository stores project code, tests, configs, and project-facing documentation only.
- `ai_skill_hub` must remain a separate sibling repository imported via Git bundle.
- New raw `.xls`, `.xlsx`, and `.csv` samples are not committed by default.
- Generated outputs belong in ignored directories such as `output/` or `tmp/`.

## Known Gaps

- `phase3_outputs.xlsx` remains the workbook artifact name even in `output_phase6/`; this is now a documented compatibility holdover rather than a Phase 3-only artifact.
- `asset_type` terminology still needs refinement to match downstream workbook language more closely.
- Shared review logic is broader now, but more regression coverage is still needed for additional asset classes and review reasons beyond the current fixture set.
- `review_flag` now marks every position that requires manual review, while `review_items.csv` remains the detailed queue explaining why each record needs attention.
- The repository does not currently use a `docs_readable/` derivative layer; if one is added later, it must remain non-authoritative.

## Recommended Next Steps

1. Decide whether to keep or rename `phase3_outputs.xlsx`, and if renaming is desired, do it with an explicit compatibility plan.
2. Decide how to handle the remaining unmapped `PRODUCT_022` sample in the default path: fill the mapping gap, add a dedicated adapter route, or keep it as an explicit failure fixture.
3. Tighten `asset_type` naming against the expected workbook vocabulary.
4. Add regression checks for review-item generation and workbook-export consistency beyond the current `3102*` rule.
