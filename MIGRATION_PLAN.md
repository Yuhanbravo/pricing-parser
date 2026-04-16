# Migration Plan

## Objective

Keep the valuation parser on a controlled migration path from adapter-specific parsing toward a more shared, mapping-driven, and workbook-aligned parsing pipeline without breaking the current verified route and export contract.

## Migration Baseline

- Phase 1 established the repository boundary and the mapping-driven routing skeleton.
- Phase 2 closed the minimum end-to-end loop for `greatwall` and `xyzc` with standardized CSV exports.
- Phase 3 converged review rules and summary statistics, aligned output schemas more closely to the expected workbook, and added workbook export.

## Current State After Phase 3

- Verified adapters: `greatwall`, `xyzc`.
- Verified outputs: `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, `phase3_outputs.xlsx`.
- Remaining work is no longer about proving the pipeline exists; it is about coverage expansion, terminology convergence, and controlled hardening.

## Planned Next Phase

### Phase 4.1: Coverage Hardening

- Add more verified raw samples for existing and next-target custodians.
- Expand regression tests around review-item detection, normalization, and workbook export.
- Confirm that shared logic still behaves correctly across adapter-specific table shapes.

### Phase 4.2: Output Vocabulary Convergence

- Refine `asset_type` values so they align better with downstream business terminology.
- Review subject and position field semantics against the expected workbook and keep the external export contract stable where possible.
- Document any intentionally deferred vocabulary mismatches before introducing new output columns.

### Phase 4.3: Adapter Expansion

- Bring one additional real custodian adapter into the verified path using the current shared parsing and export skeleton.
- Avoid adapter onboarding that copies large blocks of parser logic without first evaluating whether the difference belongs in shared code.

## Non-Goals

- No production reconciliation workflow.
- No AI-based routing or rule guessing.
- No expansion into pricing enrichment, market data completion, or downstream portfolio analytics.
- No bulk raw-sample ingestion into Git.

## Risks

- New custodians may introduce layout differences that stress current shared logic.
- Output vocabulary changes can break downstream expectations if introduced without staged validation.
- Sample scarcity can create false confidence if new behavior is validated only on the current two real samples.

## Exit Criteria For The Next Migration Step

- At least one additional custodian path is verified with controlled fixtures or local samples.
- Review-item generation and workbook export have dedicated regression coverage.
- `asset_type` terminology has a documented target mapping and at least the currently verified samples conform to it.
- Status and handoff documents are refreshed again after the next bounded phase completes.