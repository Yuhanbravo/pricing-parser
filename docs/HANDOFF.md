# Project Handoff

This file is the single source of truth for project handoff.

## Update Log

- 2026-05-14: Synchronized Round 4 asset taxonomy closure facts, refreshed expected-baseline references, and kept `PRODUCT_022` / project-local experiment skill boundaries explicit. Environment blockers: none.

## Current Status

- Current phase: Round 4 asset taxonomy closure on top of the existing Phase 5 delivery baseline.
- Latest bounded delivery reran the full 11-file controlled raw set under strict default routing, refreshed `data_samples/expected/`, and kept unresolved files out of implicit generic-fallback success paths.
- Verified adapters hit in the current run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Latest validated outputs were generated under `output/`, including `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and the date-derived workbook `估值表解析_output_<date>.xlsx`.

## What Was Refreshed In The Contract-Alignment Pass

- Full-run validation continues to use all 11 controlled raw fixtures in `data_samples/raw/`.
- `valuation_subjects` and `valuation_positions` exports now retain trace columns needed for handoff and audit: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.
- Round 4 taxonomy exports now retain `asset_type_internal`, `asset_type_display`, `asset_class_l1`, and `asset_class_l2` across subjects, positions, and review items; subjects and review items also retain `review_category`.
- `routing_results` now exports canonical `custodian_name_chinese` values, so alias forms such as `国泰` are normalized to `国泰海通证券股份有限公司` in downstream artifacts.
- `valuation_positions` now normalizes the routine suspension marker to plain `正常交易`, so downstream consumers no longer need to strip bracketed variants.
- Mapping validation now rejects unknown `adapter_key` values at load time instead of deferring the error to runtime routing.
- `parse_summary.md` now uses taxonomy display names instead of legacy internal keys and appends an `Asset Type Coverage` table.
- Output artifacts were regenerated under `output/`, and `data_samples/expected/valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, and `parse_summary.md` were refreshed from the controlled rerun.
- The workbook export name remains derived from the input date as `估值表解析_output_<date>.xlsx`.

## Hard Boundaries

- The project remains a parser and normalization tool, not a reconciliation system, analytics platform, or workbook beautification project.
- Routing must continue to depend on explicit mapping plus deterministic file and sheet signals; do not replace mapping-driven routing with model inference.
- Raw sample files are still controlled assets. New raw `.xls` or `.xlsx` samples should not be committed by default.
- `ai_skill_hub` stays a separate sibling repository and is not part of this repository's runtime or packaging boundary.
- `PRODUCT_022` remains intentionally unresolved under the strict-default path; Round 4 does not add mapping coverage or a dedicated adapter for it.
- The project-local `skill_experiments/acceptance-baseline-refresh/` assets are experimental only and do not promote this workflow into `ai-skill-hub`.

## Verified Scope

- Verified input coverage in code now spans the current 11-file fixture set under `data_samples/raw/`.
- Verified output artifacts for the latest run cover routing results, standardized subjects, standardized positions, review items, markdown summary, and workbook export.
- The markdown summary now includes supported and unsupported asset-type coverage using taxonomy display names, so handoff readers can quickly see whether the current run stayed within the parser's known asset scope.
- Latest parse summary numbers: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 525 review-flagged subjects, 238 review items, and 0 normalization issues.
- Current supported display asset types are `A股股票`, `场内基金/ETF`, `存托凭证`, `港股`, and `科创板股票`.
- Current non-position taxonomy categories such as `收益互换`, `现金及存款`, `保证金`, `证券清算款`, `应付款项`, and `应交税费` remain visible in subjects and summary coverage, but they do not enter `valuation_positions.csv`.
- The unresolved sample is `估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx`; it only routes through `generic` when `--allow-generic-fallback` is explicitly enabled.
- Current project dependencies remain minimal: `openpyxl`, `xlrd`, and `PyYAML`, with `pytest` for development validation.

## Known Gaps


## Recommended Next Steps

1. Decide whether the generated workbook `估值表解析_output_<date>.xlsx` should also have a separately maintained acceptance artifact.
2. Decide whether `PRODUCT_022` should remain an intentional strict-default failure fixture or be replaced by another controlled sample from the same custodian path in a later round.
3. Add regression tests for review-item generation and workbook-export structure beyond the current derivative-subject rule.
4. Evaluate whether the workbook summary should expose more taxonomy columns or a dedicated acceptance baseline in a later round.

## Practical Takeover Notes

- Start from `docs/status.md` when you need the current snapshot of phase, scope, and risks.
- Use `MIGRATION_PLAN.md` for planned convergence work and deferred items; do not overload this handoff file with implementation scheduling.
- If you change parser behavior, rerun `data_samples/raw/` and regenerate outputs in an ignored output directory such as `output/`, then verify that workbook and CSV artifacts remain mutually consistent.