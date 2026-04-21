# Project Handoff

This file is the single source of truth for project handoff.

## Current Status

- Current phase: Phase 5 delivery with post-review contract alignment refresh.
- Latest bounded delivery reran the full 11-file controlled raw set under strict default routing, so unresolved files are no longer upgraded to successful generic fallback routes.
- Verified adapters hit in the current run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Latest validated outputs were generated under `output_phase6/`, including `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and `估值表解析_expected_output_2025-12-01.xlsx`.

## What Was Refreshed In The Contract-Alignment Pass

- Full-run validation continues to use all 11 controlled raw fixtures in `data_samples/raw/`.
- `valuation_subjects` and `valuation_positions` exports now retain trace columns needed for handoff and audit: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.
- `routing_results` now exports canonical `custodian_name_chinese` values, so alias forms such as `国泰` are normalized to `国泰海通证券股份有限公司` in downstream artifacts.
- `valuation_positions` now normalizes the routine suspension marker to plain `正常交易`, so downstream consumers no longer need to strip bracketed variants.
- Mapping validation now rejects unknown `adapter_key` values at load time instead of deferring the error to runtime routing.
- Output artifacts were regenerated under `output_phase6/`; the workbook export now uses the same filename as the expected workbook artifact: `估值表解析_expected_output_2025-12-01.xlsx`.

## Hard Boundaries

- The project remains a parser and normalization tool, not a reconciliation system, analytics platform, or workbook beautification project.
- Routing must continue to depend on explicit mapping plus deterministic file and sheet signals; do not replace mapping-driven routing with model inference.
- Raw sample files are still controlled assets. New raw `.xls` or `.xlsx` samples should not be committed by default.
- `ai_skill_hub` stays a separate sibling repository and is not part of this repository's runtime or packaging boundary.

## Verified Scope

- Verified input coverage in code now spans the current 11-file fixture set under `data_samples/raw/`.
- Verified output artifacts for the latest run cover routing results, standardized subjects, standardized positions, review items, markdown summary, and workbook export.
- The markdown summary now includes supported and unsupported asset-type coverage so handoff readers can quickly see whether the current run stayed within the parser's known asset scope.
- Latest parse summary numbers: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 242 review items, and 0 normalization issues.
- The unresolved sample is `估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx`; it only routes through `generic` when `--allow-generic-fallback` is explicitly enabled.
- Current project dependencies remain minimal: `openpyxl`, `xlrd`, and `PyYAML`, with `pytest` for development validation.

## Known Gaps


## Recommended Next Steps

1. Decide whether `data_samples/expected/估值表解析_expected_output_2025-12-01.xlsx` should remain parser-scoped or be expanded into a fuller acceptance artifact.
2. Decide how to close the remaining routing gap for `PRODUCT_022`: add mapping coverage, add a dedicated adapter path, or keep it as an intentional failure fixture.
3. Refine `asset_type` vocabulary to match the expected workbook's business-facing terminology.
4. Add regression tests for review-item generation and workbook-export structure beyond the current derivative-subject rule.

## Practical Takeover Notes

- Start from `docs/status.md` when you need the current snapshot of phase, scope, and risks.
- Use `MIGRATION_PLAN.md` for planned convergence work and deferred items; do not overload this handoff file with implementation scheduling.
- If you change parser behavior, rerun `data_samples/raw/` and regenerate outputs in an ignored output directory such as `output_phase6/`, then verify that workbook and CSV artifacts remain mutually consistent.