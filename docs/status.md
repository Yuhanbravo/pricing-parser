# Project Status

## Current Phase

- Current milestone: Round 4 asset taxonomy closure on top of the Phase 5 delivery baseline.
- Latest bounded delivery verified the full `data_samples/raw/` set end to end under strict default routing, refreshed `data_samples/expected/`, and retained 1 routing failure instead of silent generic fallback success.
- Latest review-rule update still forces `3102*` derivative subjects into `review_items`, and matching subject / position rows carry `review_flag` as the manual-review entrypoint.

## Current Snapshot

- Routing, parsing, normalization, and export are working end to end on the full 11-file controlled raw set, with one sample intentionally left unresolved by default because it has no active mapping match.
- Latest validated outputs were generated under `output/` and include `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and a date-derived workbook export `估值表解析_output_<date>.xlsx`.
- Latest parse summary reports: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 525 review-flagged subjects, 238 review items, and 0 normalization issues.
- Latest parse summary now reports supported and unsupported asset-type coverage using taxonomy display names for the current run.
- Adapters hit in the latest run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Subjects and positions exports now preserve the trace fields required for audit and downstream reconciliation: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.
- Subjects, positions, and review items now also preserve Round 4 taxonomy fields: `asset_type_internal`, `asset_type_display`, `asset_class_l1`, and `asset_class_l2`; subjects and review items additionally carry `review_category`.
- Routing results now normalize `custodian_name_chinese` to a canonical display name, so aliases like `国泰` are exported as `国泰海通证券股份有限公司`.
- Position exports now normalize the routine suspension marker to plain `正常交易`, avoiding bracketed formatting drift in downstream sheets.
- `data_samples/expected/valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, and `parse_summary.md` were refreshed from a controlled rerun and verified against the generated outputs.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping-table lookup, and optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; parsing is verified across the current 11-file raw fixture set.
- Verified adapters in the current bounded path are `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, and `xyzc`; `generic` remains available only through explicit override or explicit fallback enablement.
- Shared review logic includes derivative-subject handling for `3102*` codes in addition to the existing position-derived review flow.
- Current position-export taxonomy types are `A股股票`, `场内基金/ETF`, `存托凭证`, `港股`, and `科创板股票`.
- Current subject / summary taxonomy coverage additionally includes non-position classes such as `收益互换`, `现金及存款`, `保证金`, `证券清算款`, `应付款项`, and `应交税费`.

## Repository Rules

- This repository stores project code, tests, configs, and project-facing documentation only.
- `ai_skill_hub` must remain a separate sibling repository imported via Git bundle.
- New raw `.xls`, `.xlsx`, and `.csv` samples are not committed by default.
- Generated outputs belong in ignored directories such as `output/` or `tmp/`.

## Known Gaps

- Workbook export naming is now derived from the input date as `估值表解析_output_<date>.xlsx`, removing both the historical Phase 3 label and the old expected-baseline filename from current outputs.
- Shared review logic is broader now, but more regression coverage is still needed for additional asset classes and review reasons beyond the current fixture set.
- `review_flag` now uses the binary value `1` to mark every subject or position that requires manual review, leaving clean rows blank; `review_note` and `review_items.csv` remain the authoritative place for the concrete review reason.
- `PRODUCT_022` remains outside the current bounded scope: it is still an intentional strict-default routing failure unless `--allow-generic-fallback` is explicitly enabled.
- The repository does not currently use a `docs_readable/` derivative layer; if one is added later, it must remain non-authoritative.

## Recommended Next Steps

1. Decide whether the generated workbook `估值表解析_output_<date>.xlsx` should also have a separately maintained acceptance baseline.
2. Decide whether the remaining unmapped `PRODUCT_022` sample should stay as an explicit failure fixture or be replaced by another controlled sample in a later round.
3. Add regression checks for review-item generation and workbook-export consistency beyond the current `3102*` rule.
4. Evaluate whether the workbook summary should expose a richer taxonomy view or a separately maintained workbook baseline in a later round.
