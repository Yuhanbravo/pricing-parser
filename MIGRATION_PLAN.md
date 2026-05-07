# Migration Plan

## Objective

Keep the valuation parser on a controlled migration path from adapter-specific parsing toward a more shared, mapping-driven, and workbook-aligned parsing pipeline without breaking the current verified route and export contract.

## Migration Baseline

- Phase 1 established the repository boundary and the mapping-driven routing skeleton.
- Phase 2 closed the minimum end-to-end loop for `greatwall` and `xyzc` with standardized CSV exports.
- Phase 3 converged review rules and summary statistics, aligned output schemas more closely to the expected workbook, and added workbook export.
- Phase 4 expanded verified adapter coverage beyond the initial two-sample path and hardened batch execution against more custodian layouts.
- Phase 5 validated the full 11-file controlled raw set, kept the strict-default unresolved fixture visible as a routing failure, and promoted `3102*` derivative-subject detection into shared review-item behavior.

## Current State After Phase 5

- Verified adapters: `citics`, `cmsc`, `csc`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Verified outputs: `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and a date-derived workbook `估值表解析_output_<date>.xlsx`.
- Latest bounded evidence from the strict-default `output/` run: 11 processed files, 10 successful routes, 1 routing failure, 1022 subject rows, 182 position rows, 238 review items, and 0 normalization issues.
- Current review contract keeps `3102*` derivative subjects in `valuation_subjects` and `review_items`; they are not promoted into `valuation_positions`.
- Current summary contract now includes explicit indexes for unrouted objects and review entrypoints, and the strict-default baseline compares full workbook sheet contents.
- Canonical `.xlsx` mapping and core non-derivative position-review entrypoints both have repository regression coverage, with dedicated fixtures for `hk_equity`, `a_share`, and `fund_or_etf`.
- Remaining work is no longer about proving the pipeline exists; it is about contract stabilization, terminology convergence, and controlled fixture governance.

## Planned Next Phase

### Phase 6.1: Artifact Contract Stabilization

- Keep workbook export naming aligned with the input date as `估值表解析_output_<date>.xlsx` and prevent regressions back to historical artifact names.
- Keep regression tests around review-item detection, normalization, workbook export naming, and add new asset-class-specific review paths only when they go beyond the currently covered `hk_equity`, `a_share`, and `fund_or_etf` fixtures.
- Keep documentation aligned with the actual bounded run outputs rather than with historical phase labels.

### Phase 6.2: Output Vocabulary Convergence

- Refine `asset_type` values so they align better with downstream business terminology.
- Review subject, position, and review-item field semantics against the expected workbook and keep the external export contract stable where possible.
- Document any intentionally deferred vocabulary mismatches before introducing new output columns.

### Phase 6.3: Fixture Governance And Incremental Coverage

- Revisit which raw fixtures must remain in Git and which should be reduced to minimal expected artifacts or external local samples.
- Add new adapter coverage only when the new sample introduces layout variation that is not already exercised by the current verified set.

## Non-Goals

- No production reconciliation workflow.
- No AI-based routing or rule guessing.
- No expansion into pricing enrichment, market data completion, or downstream portfolio analytics.
- No bulk raw-sample ingestion into Git.

## Risks

- New custodians may introduce layout differences that stress current shared logic.
- Output vocabulary or artifact-name changes can break downstream expectations if introduced without staged validation.
- The current fixture set is broader than before, but it can still create false confidence if new behavior is validated only against the existing 11 files.

## Exit Criteria For The Next Migration Step

- Workbook artifact naming remains aligned with the input date as `估值表解析_output_<date>.xlsx` and is covered by regression tests.
- Review-item generation keeps dedicated regression coverage beyond the current derivative-subject rule, including core non-derivative review paths for `hk_equity`, `a_share`, and `fund_or_etf`.
- `asset_type` terminology has a documented target mapping and at least the currently verified samples conform to it.
- Status and handoff documents are refreshed again after the next bounded phase completes.