# Project Handoff

This file is the single source of truth for project handoff.

## Current Status

- Current phase: Phase 3 delivery completed.
- Latest bounded delivery completed the shared review-rule convergence, summary-stat alignment, expected-workbook schema alignment, and multi-sheet Excel export.
- Real adapters verified in the current run: `greatwall`, `xyzc`.
- Latest validated outputs were generated under `output_phase3/`, including `routing_results.csv`, `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, `parse_summary.md`, and `phase3_outputs.xlsx`.

## What Was Delivered In Phase 3

- Shared review logic was expanded into common behavior instead of remaining adapter-only logic.
- Summary statistics now include review-item counts and normalization totals in the exported markdown summary.
- Output schemas were aligned more closely to the expected workbook shape used for downstream review.
- A multi-sheet Excel workbook export was added so the Phase 3 CSV outputs can also be reviewed in a single file.

## Hard Boundaries

- The project remains a parser and normalization tool, not a reconciliation system, analytics platform, or workbook beautification project.
- Routing must continue to depend on explicit mapping plus deterministic file and sheet signals; do not replace mapping-driven routing with model inference.
- Raw sample files are still controlled assets. New raw `.xls` or `.xlsx` samples should not be committed by default.
- `ai_skill_hub` stays a separate sibling repository and is not part of this repository's runtime or packaging boundary.

## Verified Scope

- Verified input coverage in code remains centered on the two real samples currently used for `greatwall` and `xyzc`.
- Verified output artifacts for the latest run cover routing results, standardized subjects, standardized positions, review items, markdown summary, and workbook export.
- Current project dependencies remain minimal: `openpyxl`, `xlrd`, and `PyYAML`, with `pytest` for development validation.

## Known Gaps

- Unsupported raw sample formats still exist outside the verified Phase 3 path and may fail without adapter-specific follow-up.
- `asset_type` remains technically usable but is not yet fully aligned with the target workbook's preferred business terminology.
- Review rules are broader than Phase 2, but additional asset-class coverage and more edge-case regression fixtures are still needed.
- Placeholder adapters still exist for unsupported custodians and should not be presented as production-ready parsing support.

## Recommended Next Steps

1. Expand verified sample coverage beyond the current two real adapters before adding more shared rule complexity.
2. Refine `asset_type` vocabulary to match the expected workbook's business-facing terminology.
3. Add regression tests for review-item generation and workbook-export structure.
4. Decide which current repository sample assets remain in Git and which should be reduced to minimal fixtures only.

## Practical Takeover Notes

- Start from `docs/status.md` when you need the current snapshot of phase, scope, and risks.
- Use `MIGRATION_PLAN.md` for planned convergence work and deferred items; do not overload this handoff file with implementation scheduling.
- If you change parser behavior, regenerate Phase outputs in an ignored output directory and verify that workbook and CSV artifacts remain mutually consistent.