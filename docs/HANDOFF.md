# Project Handoff

This file is the single source of truth for project handoff.

## Update Log

- 2026-06-04: Ran project-level post-dev dual-refresh after AI entrypoint bootstrap; refreshed project status/handoff facts for thin Codex/Copilot entrypoints and task package conventions. Environment blockers: none; external sync and hook installation intentionally not performed.
- 2026-05-14: Synchronized Round 4 asset taxonomy closure facts, refreshed expected-baseline references, and kept `PRODUCT_022` / project-local experiment skill boundaries explicit. Environment blockers: none.

## Current Status

- Current phase: Round 4 asset taxonomy closure on top of the existing Phase 5 delivery baseline.
- Latest bounded delivery reran the full 11-file controlled raw set under strict default routing, refreshed `data_samples/expected/`, and kept unresolved files out of implicit generic-fallback success paths.
- Project-level AI collaboration entrypoints are now available: `AGENTS.md`, `.github/copilot-instructions.md`, and `tasks/README.md`. They are thin orientation files and should point back to existing canonical project sources instead of becoming a second rule set.
- Verified adapters hit in the current run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Latest validated strict-default baseline is stored under `data_samples/expected/`, including `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and the date-derived workbook `估值表解析_output_<date>.xlsx`; local reruns may still export into ignored directories such as `output/`, but those artifacts are not part of the tracked contract.

## What Was Refreshed In The Contract-Alignment Pass

- Full-run validation continues to use all 11 controlled raw fixtures in `data_samples/raw/`.
- `valuation_subjects` and `valuation_positions` exports now retain trace columns needed for handoff and audit: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.
- Round 4 taxonomy exports now retain `asset_type_internal`, `asset_type_display`, `asset_class_l1`, and `asset_class_l2` across subjects, positions, and review items; subjects and review items also retain `review_category`.
- `routing_results` now exports canonical `custodian_name_chinese` values, so alias forms such as `国泰` are normalized to `国泰海通证券股份有限公司` in downstream artifacts.
- `valuation_positions` now normalizes the routine suspension marker to plain `正常交易`, so downstream consumers no longer need to strip bracketed variants.
- `3102*` derivative subjects continue to produce review entries, but they stay in `valuation_subjects` and `review_items` instead of being promoted into `valuation_positions`.
- Mapping validation now rejects unknown `adapter_key` values at load time instead of deferring the error to runtime routing.
- `parse_summary.md` now uses taxonomy display names instead of legacy internal keys and appends an `Asset Type Coverage` table.
- Canonical `.xlsx` mapping loading is now covered by repository tests at both the loader layer and the pipeline layer.
- The tracked acceptance baseline was refreshed under `data_samples/expected/`; the workbook artifact continues to use the input-date-derived name `估值表解析_output_<date>.xlsx`, while ad hoc reruns should write to ignored directories such as `output/`.

## Hard Boundaries

- The project remains a parser and normalization tool, not a reconciliation system, analytics platform, or workbook beautification project.
- Routing must continue to depend on explicit mapping plus deterministic file and sheet signals; do not replace mapping-driven routing with model inference.
- Raw sample files are still controlled assets. New raw `.xls` or `.xlsx` samples should not be committed by default.
- `ai_skill_hub` stays a separate sibling repository and is not part of this repository's runtime or packaging boundary.
- `PRODUCT_022` remains intentionally unresolved under the strict-default path; Round 4 does not add mapping coverage or a dedicated adapter for it.
- The project-local `skill_experiments/acceptance-baseline-refresh/` assets are experimental only and do not promote this workflow into `ai-skill-hub`.
- Post-dev refresh for this repository is project-level only; use ai-skill-hub workflow guidance as a source, but do not perform system-level ai-skill-hub refresh, external sync, or hook installation from this project handoff.

## Verified Scope

- Verified input coverage in code now spans the current 11-file fixture set under `data_samples/raw/`.
- Verified output artifacts for the latest run cover routing results, standardized subjects, standardized positions, review items, markdown summary, and workbook export.
- The markdown summary now includes supported and unsupported asset-type coverage using taxonomy display names, and explicit `Unrecognized Object Index` and `Review Entry Index` sections, plus an `Asset Type Coverage` table, so handoff readers can move from counts to actionable review rows.
- Latest parse summary numbers: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 508 review-flagged subjects, 238 review items, and 0 normalization issues.
- Current supported display asset types are `A股股票`, `场内基金/ETF`, `存托凭证`, `港股`, and `科创板股票`.
- Current non-position taxonomy categories such as `收益互换`, `现金及存款`, `保证金`, `证券清算款`, `应付款项`, and `应交税费` remain visible in subjects and summary coverage, but they do not enter `valuation_positions.csv`.
- `review_flag` only marks whether a subject or position needs manual review; `review_note` carries the row-level reason; and `review_items.csv` is the run-level review queue export.
- The unresolved sample is `估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx`; it only routes through `generic` when `--allow-generic-fallback` is explicitly enabled.
- The strict-default acceptance baseline now lives under `data_samples/expected/`, including the expected routing CSV, subject CSV, position CSV, review-item CSV, parse summary, and workbook artifact; workbook validation now compares full sheet contents rather than only sheet headers.
- Current project dependencies remain minimal: `openpyxl`, `xlrd`, and `PyYAML`, with `pytest` for development validation.

## Known Gaps

- Historical materials referenced by older review notes, such as `output_phase*` and `docs/documentation_governance_report.*`, are not the authoritative current contract and should remain clearly treated as historical snapshots if retained locally for audit traceability.


## Recommended Next Steps

1. Decide whether the generated workbook `估值表解析_output_<date>.xlsx` should have a separately maintained acceptance artifact, or whether a business-readable workbook diff is also needed for review handoff.
2. Decide how to close the remaining routing gap for `PRODUCT_022`: add mapping coverage, add a dedicated adapter path, or keep it as an intentional failure fixture.
3. Add regression tests for review-item generation and workbook-export structure beyond the current derivative-subject rule and existing non-derivative asset-class fixtures.
4. Evaluate whether the workbook summary should expose more taxonomy columns or a dedicated acceptance baseline in a later round.
5. Confirm and document the authoritative PR validation command and branch naming convention in the existing thin-entry / canonical-source structure.

## Practical Takeover Notes

- Start from `docs/status.md` when you need the current snapshot of phase, scope, and risks.
- Use `AGENTS.md` for Codex/agent orientation, `.github/copilot-instructions.md` for Copilot-specific hints, and `tasks/README.md` for task package and execution report conventions.
- Use `MIGRATION_PLAN.md` for planned convergence work and deferred items; do not overload this handoff file with implementation scheduling.
- If you change parser behavior, rerun `data_samples/raw/` and regenerate outputs in an ignored output directory such as `output/`, then verify that workbook and CSV artifacts remain mutually consistent.
