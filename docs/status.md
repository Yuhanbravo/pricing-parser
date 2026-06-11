# Project Status

## Current Phase

- Current milestone: Round 4 asset taxonomy closure on top of the Phase 5 delivery baseline.
- Latest bounded delivery verified the full `data_samples/raw/` set end to end under strict default routing, refreshed `data_samples/expected/`, and retained 1 routing failure instead of silent generic fallback success.
- Latest review-rule update still forces `3102*` derivative subjects into `review_items`, and those rows are not promoted into `valuation_positions`.
- Latest project-level AI collaboration refresh added thin Codex/Copilot entrypoints and task package conventions without changing parser behavior.
- DeepSeek PR Review configuration has been completed.
- First-round handoff material refresh has been completed; pending final closure review.
- Current priority is docs-only governance training (audit → report → fix); parser behavior is intentionally frozen during this phase. Feature iteration on workbook baseline and export consistency is deferred until documentation structure is confirmed.
- Claude Code initialization is limited to a thin `CLAUDE.md` entrypoint and does not change parser behavior.

## Current Snapshot

- Routing, parsing, normalization, and export are working end to end on the full 11-file controlled raw set, with one sample intentionally left unresolved by default because it has no active mapping match.
- The authoritative strict-default baseline lives under `data_samples/expected/`; ad hoc reruns may also generate artifacts in ignored directories such as `output/`.
- Latest parse summary reports: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 508 review-flagged subjects, 238 review items, and 0 normalization issues.
- Latest parse summary now reports supported and unsupported asset-type coverage using taxonomy display names, plus explicit `Asset Type Coverage`, `Unrecognized Object Index`, and `Review Entry Index` sections.
- `review_flag` marks whether a subject or position needs manual review; `review_note` carries the row-level reason; `review_items.csv` is the run-level review queue.
- Review entry grouping is regression-covered when `subject_name` and `instrument_name` differ, so index and summary views stay aligned for the same logical item.
- Adapters hit in the latest run: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Subjects and positions exports now preserve the trace fields required for audit and downstream reconciliation: `source_file`, `product_id`, `association_code`, `custodian_id`, `custodian_name`, `adapter_key`, and `route_source`.
- Subjects, positions, and review items now also preserve Round 4 taxonomy fields: `asset_type_internal`, `asset_type_display`, `asset_class_l1`, and `asset_class_l2`; subjects and review items additionally carry `review_category`.
- Routing results now normalize `custodian_name_chinese` to a canonical display name, so aliases like `国泰` are exported as `国泰海通证券股份有限公司`.
- Position exports now normalize the routine suspension marker to plain `正常交易`, avoiding bracketed formatting drift in downstream sheets.
- The strict-default acceptance baseline is maintained under `data_samples/expected/`, including routing/subjects/positions/review CSVs, parse summary, and a full workbook-content baseline; the baseline was refreshed from a controlled rerun and verified against the Round 4 taxonomy contract.
- Canonical `.xlsx` mapping is regression-covered inside the repository at both the loader and pipeline layers.
- AI collaboration entrypoints are now in place: `AGENTS.md` for project-level agent orientation, `.github/copilot-instructions.md` for Copilot-specific guidance, `CLAUDE.md` for Claude Code orientation, and `tasks/README.md` for bounded task package / execution report conventions.
- `ai-skill-hub` is used only as a sibling reference repository; its files are not committed into this repository.

## Supported Scope

- Supported routing inputs: filename, sheet preview, header preview, mapping-table lookup, and optional manual adapter override.
- Supported workbook types in code: `.xls`, `.xlsx`, `.csv` for preview and routing; parsing is verified across the current 11-file raw fixture set.
- Verified adapters in the current bounded path are `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, and `xyzc`; `generic` remains available only through explicit override or explicit fallback enablement.
- Shared review logic includes derivative-subject handling for `3102*` codes; derivative review stays at the subject/review-item layer rather than creating synthetic position rows.
- Current position-export taxonomy types are `A股股票`, `场内基金/ETF`, `存托凭证`, `港股`, and `科创板股票`.
- Current subject / summary taxonomy coverage additionally includes non-position classes such as `收益互换`, `现金及存款`, `保证金`, `证券清算款`, `应付款项`, and `应交税费`.
- Review-entry deduplication is covered when `subject_name` and `instrument_name` differ, preventing split groups in the index and summary views.

## Repository Rules

> Repository-level rules (workspace boundaries, sample policy, output conventions, and thin-entry rules for AI files) are defined in **[README.md](../README.md)**. This section intentionally defers to README.md as the single source; do not duplicate rules here.

## Known Gaps

- Workbook export naming is now derived from the input date as `估值表解析_output_<date>.xlsx`, removing both the historical Phase 3 label and the old expected-baseline filename from current outputs.
- Shared review logic now has dedicated non-derivative regression coverage for the core supported asset classes `hk_equity`, `a_share`, and `fund_or_etf`; future fixture growth should track genuinely new asset classes or review reasons.
- `review_flag` now uses the binary value `1` to mark every subject or position that requires manual review, leaving clean rows blank; `review_note` and `review_items.csv` remain the authoritative place for the concrete review reason.
- `PRODUCT_022` remains outside the current bounded scope: it is still an intentional strict-default routing failure unless `--allow-generic-fallback` is explicitly enabled.
- The repository does not currently use a `docs_readable/` derivative layer; if one is added later, it must remain non-authoritative.
- Historical materials referenced by older review notes, such as `output_phase*` and `docs/documentation_governance_report.*`, should be treated as legacy snapshots rather than current contract artifacts and should only be retained with an explicit historical label.

## Recommended Next Steps

1. Once documentation structure is stable, resume feature planning: workbook baseline maintenance, export consistency checks, and review-item regression expansion.
2. Decide whether the generated workbook `估值表解析_output_<date>.xlsx` should also have a separately maintained acceptance baseline.
3. Decide how to handle the remaining unmapped `PRODUCT_022` sample: fill the mapping gap, add a dedicated adapter route, or keep it as an explicit failure fixture.
4. Add regression checks for review-item generation and workbook-export consistency beyond the current `3102*` rule and existing non-derivative fixtures.
5. Confirm the team's authoritative PR validation command and branch naming convention, then document it in the existing thin entry / canonical-source structure without creating a second rulebook.
