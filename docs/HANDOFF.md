# Project Handoff

This file is the single source of truth for project handoff.

## Current Status

- Current phase: Phase 5 delivery completed.
- Latest bounded delivery extended the verified path to the full 11-file controlled raw set, preserved zero routing failures, and refreshed derivative-subject review handling.
- Verified adapters in the current run: `citics`, `cmsc`, `csc`, `generic`, `greatwall`, `gtja`, `guosen`, `orient`, `xyzc`.
- Latest validated outputs were generated under `output_phase5/`, including `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and `phase3_outputs.xlsx`.

## What Was Delivered In Phase 5

- Full-run validation now covers all 11 controlled raw fixtures in `data_samples/raw/`.
- The verified adapter path now includes `citics`, `cmsc`, `csc`, `generic`, `greatwall`, `gtja`, `guosen`, `orient`, and `xyzc`.
- Shared review logic now explicitly flags `3102*` derivative subjects as review items.
- Output artifacts were regenerated under `output_phase5/`; the workbook export still uses the legacy filename `phase3_outputs.xlsx` for compatibility.

## Hard Boundaries

- The project remains a parser and normalization tool, not a reconciliation system, analytics platform, or workbook beautification project.
- Routing must continue to depend on explicit mapping plus deterministic file and sheet signals; do not replace mapping-driven routing with model inference.
- Raw sample files are still controlled assets. New raw `.xls` or `.xlsx` samples should not be committed by default.
- `ai_skill_hub` stays a separate sibling repository and is not part of this repository's runtime or packaging boundary.

## Verified Scope

- Verified input coverage in code now spans the current 11-file fixture set under `data_samples/raw/`.
- Verified output artifacts for the latest run cover routing results, standardized subjects, standardized positions, review items, markdown summary, and workbook export.
- Latest parse summary numbers: 11 processed files, 11 successful routes, 1113 subject rows, 202 position rows, 253 review items, and 0 normalization issues.
- Current project dependencies remain minimal: `openpyxl`, `xlrd`, and `PyYAML`, with `pytest` for development validation.

## Known Gaps

- `phase3_outputs.xlsx` is still the workbook export name, so artifact naming remains historically coupled to an older phase label.
- `asset_type` remains technically usable but is not yet fully aligned with the target workbook's preferred business terminology.
- Review rules are broader now, but additional asset-class coverage and more edge-case regression fixtures are still needed.
- The repository still has no `docs_readable/` derivative layer; if one is introduced, it must not become a second source of truth.

## Recommended Next Steps

1. Decide whether the workbook artifact should keep the legacy `phase3_outputs.xlsx` name or move to a neutral name with compatibility handling.
2. Refine `asset_type` vocabulary to match the expected workbook's business-facing terminology.
3. Add regression tests for review-item generation and workbook-export structure beyond the current derivative-subject rule.
4. Decide which current repository sample assets remain in Git and which should be reduced to minimal fixtures only.

## Practical Takeover Notes

- Start from `docs/status.md` when you need the current snapshot of phase, scope, and risks.
- Use `MIGRATION_PLAN.md` for planned convergence work and deferred items; do not overload this handoff file with implementation scheduling.
- If you change parser behavior, regenerate outputs in an ignored output directory and verify that workbook and CSV artifacts remain mutually consistent.