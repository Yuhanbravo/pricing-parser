# Documentation Governance Report

Historical note: this report records a 2026-04-16 audit snapshot. It is kept for traceability, but the current parser contract is defined by `README.md`, `docs/HANDOFF.md`, `docs/status.md`, `data_samples/expected/`, and the latest strict-default output evidence.

- Date: 2026-04-16
- Mode: `audit -> report -> fix`
- Project root: `pricing_parser`
- Requested config path: `pricing_parser/config`
- Config resolution: no documentation-specific governance config was found under `config/`; this run used the `documentation-governance` skill defaults plus repository structure and current project artifacts as context.

## Scan Scope

- Root docs scanned: `README.md`, `MIGRATION_PLAN.md`
- Project docs scanned: `docs/status.md`, `docs/HANDOFF.md`
- Sample-policy docs scanned: `data_samples/README.md`
- Repository markdown inventory reviewed for phase drift, duplicate topics, naming issues, and missing readable-layer boundaries.

## Findings

### High Priority

1. Core status documents were stale against the current project phase.
   - `README.md` still described the project as Phase 2.
   - `docs/status.md` and `docs/HANDOFF.md` still described the project as Phase 3.
   - `MIGRATION_PLAN.md` still treated Phase 3 as the current state.

2. Project capability statements understated current verified coverage.
   - The repository now has validated Phase 5 coverage across 11 controlled raw files and 9 adapter keys.
   - Shared review behavior now includes `3102*` derivative-subject review-item generation.

### Medium Priority

1. Workbook artifact naming is historically misleading.
   - The current workbook artifact is still written as `phase3_outputs.xlsx` even when generated under `output_phase5/`.
   - This is not a runtime error, but it needs to be documented until a compatibility-safe rename is planned.

2. No documentation-specific config exists under the requested config path.
   - `pricing_parser/config/` contains runtime parser configuration, not documentation governance rules.

### Low Priority

1. No `docs_readable/` layer exists in this repository.
   - No dual-layer conflict was detected in this audit.
   - If a readable derivative layer is introduced later, it should remain non-authoritative.

2. No urgent duplicate-topic conflict was found among the current project markdown files.
   - The dominant governance problem was stale phase narration, not duplicate ownership.

## Single Source Of Truth Used For This Update

- `output_phase5/parse_summary.md`
- Current adapter registry and pipeline behavior
- Current Phase 5 tests, including full-run smoke and derivative review-item regression

## Fixes Applied

- Updated `README.md` to reflect Phase 5 scope, verified adapters, current outputs, and next steps.
- Updated `docs/status.md` to reflect the current run statistics and current review-rule scope.
- Updated `docs/HANDOFF.md` to align takeover guidance with Phase 5 outputs and known gaps.
- Updated `MIGRATION_PLAN.md` so the migration baseline and next-phase planning no longer stop at Phase 3.
- Added this governance report and a JSON mirror for machine-readable tracking.

## Residual Risks

- Future artifact renaming may break downstream consumers if the workbook filename changes without compatibility handling.
- Additional asset classes may still expose review-rule gaps that are not covered by the current fixture set.
- Documentation can drift again unless status and handoff files are refreshed as part of each bounded delivery.