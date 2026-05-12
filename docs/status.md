# Project Status

## Current Phase

- Current milestone: Phase 5 delivery with post-review derivative-exclusion refresh.
- Latest bounded delivery verified the full `data_samples/raw/` set end to end under strict default routing, resulting in 1 retained routing failure instead of silent generic fallback success.
- Latest review-rule update still forces `3102*` derivative subjects into `review_items`, but those rows are no longer promoted into `valuation_positions`.

## Current Snapshot

- Routing, parsing, normalization, and export are working end to end on the full 11-file controlled raw set, with one sample intentionally left unresolved by default because it has no active mapping match.
- The authoritative strict-default baseline lives under `data_samples/expected/`; ad hoc reruns may still be generated under ignored directories such as `output/`, with the same artifact set: `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and the date-derived workbook export `估值表解析_output_<date>.xlsx`.
- Latest parse summary reports: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 238 review items, and 0 normalization issues.
- `review_flag` only marks whether a subject or position needs manual review, `review_note` carries the row-level reason, and `review_items.csv` is the run-level review queue export; under the current strict-default evidence, `valuation_positions` has 0 `review_flag=1` rows, while active manual-review entrypoints in the bounded sample are `valuation_subjects` plus `review_items` and the position-review path itself is locked by dedicated non-derivative regression fixtures covering `hk_equity`, `a_share`, and `fund_or_etf`.
- Latest parse summary now also reports supported and unsupported asset-type coverage for the current run, plus explicit `Unrecognized Object Index` and `Review Entry Index` sections.
- Review entry grouping is regression-covered when `subject_name` and `instrument_name` differ, so `Review Entry Index` and `Review Queue By Source File` stay aligned for the same logical item.
- Adapters hit in the latest run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Subjects and positions exports now preserve the trace fields required for audit and downstream reconciliation: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.
- Routing results now normalize `custodian_name_chinese` to a canonical display name, so aliases like `国泰` are exported as `国泰海通证券股份有限公司`.
- Position exports now normalize the routine suspension marker to plain `正常交易`, avoiding bracketed formatting drift in downstream sheets.
- The strict-default acceptance baseline is maintained under `data_samples/expected/`, including routing/subjects/positions/review CSVs, summary evidence, and a full workbook-content baseline.
- Canonical `.xlsx` mapping is now regression-covered inside the repository at both the loader and pipeline layers.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping-table lookup, and optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; parsing is verified across the current 11-file raw fixture set.
- Verified adapters in the current bounded path are `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, and `xyzc`; `generic` remains available only through explicit override or explicit fallback enablement.
- Shared review logic includes derivative-subject handling for `3102*` codes, but derivative review stays at the subject/review-item layer rather than creating synthetic position rows.
- Review-entry deduplication now treats the position display name consistently across the index and summary views, preventing accidental split groups when a row's `subject_name` and `instrument_name` differ.

## Repository Rules

- This repository stores project code, tests, configs, and project-facing documentation only.
- `ai_skill_hub` must remain a separate sibling repository imported via Git bundle.
- New raw `.xls`, `.xlsx`, and `.csv` samples are not committed by default.
- Generated outputs belong in ignored directories such as `output/` or `tmp/`.

## Known Gaps

- Workbook export naming is now derived from the input date as `估值表解析_output_<date>.xlsx`, removing both the historical Phase 3 label and the old expected-baseline filename from current outputs.
- `asset_type` terminology still needs refinement to match downstream workbook language more closely.
- Shared review logic now has dedicated non-derivative regression coverage for the core supported asset classes `hk_equity`, `a_share`, and `fund_or_etf`; future fixture growth should track genuinely new asset classes or review reasons rather than duplicate the existing path.
- `review_flag` now uses the binary value `1` to mark every subject or position that requires manual review, leaving clean rows blank; `review_note` and `review_items.csv` remain the authoritative place for the concrete review reason.
- The repository does not currently use a `docs_readable/` derivative layer; if one is added later, it must remain non-authoritative.
- Historical materials referenced by older review notes, such as `output_phase*` and `docs/documentation_governance_report.*`, should be treated as legacy snapshots rather than current contract artifacts and should only be retained with an explicit historical label.

## Recommended Next Steps

1. Decide whether the generated workbook `估值表解析_output_<date>.xlsx` should also have a separately maintained acceptance baseline.
2. Decide how to handle the remaining unmapped `PRODUCT_022` sample in the default path: fill the mapping gap, add a dedicated adapter route, or keep it as an explicit failure fixture.
3. Tighten `asset_type` naming against the expected workbook vocabulary.
4. Keep extending review-item and workbook-export regression checks only when new review reasons or asset-class paths appear beyond the current `3102*` rule plus the covered `hk_equity` / `a_share` / `fund_or_etf` non-derivative fixtures.
5. If this round closes the remaining evidence drift, prefer `review-round1-baseline`, `review-round2-candidate`, and `review-round3-evidence-closed` for milestone tagging.
