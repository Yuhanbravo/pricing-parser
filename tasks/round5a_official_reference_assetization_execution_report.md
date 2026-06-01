# Round 5A Official Reference Assetization Execution Report

## Scope Restatement

This round implemented only Round 5A official reference assetization.

Delivered scope:

- formal reference source assets
- formal Markdown reference assets
- structured accounting-subject reference CSVs
- OTC derivative design and reference CSVs
- reference and design documents
- this execution report

Out of scope and kept unchanged:

- parser runtime logic under `src/`
- adapters
- routing
- `PRODUCT_022`
- expected baseline refresh
- existing runtime output contracts

## Files Changed

### Submitted in git history

- `1d13a55` `docs(assetization): add round5a drafts`
	- `tasks/round5a_official_reference_assetization_task_package.md`
- `67ccf64` `docs(assetization): add round5a pre-implementation review materials`
	- `tasks/round5a_official_reference_assetization_pre_implementation_review.md`
- `bf2cfb0` `feat(reference): add round5a official reference assets`
	- `.gitignore`
	- `docs/reference/`
	- `docs/derivatives/`
	- `data/reference/`
- `58d3046` `docs(report): add round5a execution report`
	- `tasks/round5a_official_reference_assetization_execution_report.md`
- `4f6e30e` `refactor(report): refine execution report structure and wording`
    - `tasks/round5a_official_reference_assetization_execution_report.md`
- `47355bb` `docs(report): final review and polish for round5a execution report`
    - `tasks/round5a_official_reference_assetization_execution_report.md`

#### Non-delivery commit (3690f0c equivalent — see below)

- `3688f0c` `docs(task-package): Phase 5A - add official reference assetization task book with Round 5B/5C/5D design directions`
	- `任务书集合/pricing_parser第四轮审查结论摘要暨第五轮任务书.md`
	- **Status**: non-delivery. This file was introduced in a working-copy directory outside the formal Round 5A delivery paths (`docs/reference/`, `docs/derivatives/`, `data/reference/`, `tasks/`). The directory is now excluded by `.gitignore` and the file has been removed from tracking. See "Remaining Unsubmitted Working Tree Items" below for the rationale and resolution.

### Repo config

- `.gitignore`

### Reference assets

- `docs/reference/source/中国基金估值标准2018.pdf`
- `docs/reference/source/证券投资基金会计核算操作实务手册-20240530.docx`
- `docs/reference/markdown/中国基金估值标准2018.md`
- `docs/reference/markdown/证券投资基金会计核算操作实务手册-20240530.md`

### Reference docs

- `docs/reference/source_manifest.md`
- `docs/reference/official_valuation_references.md`
- `docs/reference/accounting_subjects_extraction_notes.md`
- `docs/reference/accounting_subjects_mapping_design.md`
- `docs/reference/official_reference_reusable_assets.md`

### OTC derivative docs

- `docs/derivatives/otc_derivative_model_design.md`
- `docs/derivatives/otc_derivative_reference_fields.md`
- `docs/derivatives/otc_derivative_review_rules.md`
- `docs/derivatives/otc_derivative_data_requirements.md`

### Structured reference CSVs

- `data/reference/accounting_subjects_raw.csv`
- `data/reference/accounting_subjects_normalized.csv`
- `data/reference/accounting_subject_mapping_review_queue.csv`
- `data/reference/accounting_subject_to_asset_taxonomy_design.csv`
- `data/reference/otc_derivative_subject_patterns.csv`
- `data/reference/otc_derivative_field_dictionary.csv`
- `data/reference/otc_derivative_review_rules.csv`

### Process files

- `tasks/round5a_official_reference_assetization_execution_report.md`

### Supporting delivery fixes

- Added a minimal `.gitignore` exception for `data/reference/*.csv` so the Round 5A structured reference CSV deliverables are not hidden by the repository-wide `*.csv` ignore rule.
- Added `任务书集合/` to `.gitignore` and removed it from tracking to keep historical working-copy materials outside the formal delivery surface.

## Reference Assets Added

### Source and Markdown assets

- Copied the existing working-copy source files into the formal Round 5A delivery path under `docs/reference/source/`.
- Copied the existing working-copy Markdown conversions into the formal Round 5A delivery path under `docs/reference/markdown/`.
- Preserved the historical working copies in `任务书集合/`; Round 5A formal delivery now lives under `docs/reference/`.

### Source manifest

- Added a manifest that records title, version, format, conversion method, public-reference positioning, and usage boundary for both sources.

### Structured accounting reference data

- Added a first-pass raw extraction table.
- Added a normalized standard-accounting table.
- Added a mapping review queue for unresolved or ambiguous cases.
- Added a draft standard-subject to existing asset-taxonomy design table.

### OTC derivative reference assets

- Added derivative subject-pattern candidates.
- Added a derivative field dictionary.
- Added derivative review-rule candidates.
- Added design notes that keep OTC derivatives as a future independent subsystem rather than ordinary positions.

## Validation

### Commands run

1. `git status --short`
2. `git diff --name-only`
3. `pytest -q`
4. `python -m pytest -q`
5. `Get-ChildItem -Recurse docs/reference,docs/derivatives,data/reference | Select-Object FullName`
6. `git status --short -- .gitignore docs/reference docs/derivatives data/reference tasks/round5a_official_reference_assetization_execution_report.md`

### Results

- `git status --short`: completed; showed the new Round 5A asset directories as untracked additions. The wider repository already had other untracked content outside this round.
- `git diff --name-only`: completed; produced no output because the Round 5A files are new untracked files rather than modifications to tracked files.
- `pytest -q`: passed in the `valuation-parser` environment. Result: `52 passed in 8.34s`.
- `python -m pytest -q`: environment blocked. The `python` executable was not available in the current shell.
- directory existence check: completed; confirmed the formal delivery paths under `docs/reference/`, `docs/derivatives/`, and `data/reference/` were created and populated.
- path-scoped `git status`: completed; confirmed `.gitignore`, `docs/reference/`, `docs/derivatives/`, `data/reference/`, and the execution report are the final bounded delivery surface for this round.

### Validation interpretation

The bounded execution stayed in the intended reference-only surface. Runtime-regression validation is now closed: `pytest -q` passed in the available project environment. The earlier `python -m pytest -q` attempt remains a shell-path limitation rather than a repository failure.

## Boundaries Kept

- No files under `src/` were modified.
- No adapter files were modified.
- No routing logic was touched.
- No baseline files under `data_samples/expected/` were refreshed.
- No runtime output columns were added to `valuation_subjects.csv`, `valuation_positions.csv`, or `review_items.csv`.
- No attempt was made to handle `PRODUCT_022`.
- No official reference file was wired into runtime configuration.

## Not Done

- No parser-side standard-accounting mapping was implemented.
- No runtime fields such as `account_code_std` or `account_name_std` were added to existing exports.
- No adapter or routing changes were made.
- No expected-baseline refresh was performed.
- No automatic valuation-method rules were implemented.
- No OTC derivative contract parsing or lookthrough output was implemented.

## Remaining Unsubmitted Working Tree Items

The repository still contains untracked working-copy materials outside the formal Round 5A delivery surface. These were intentionally kept outside the submitted Round 5A formal delivery path, which lives under `docs/reference/`, `docs/derivatives/`, and `data/reference/`.

- `scripts/`
- historical working-copy files under `任务书集合/`

### Resolution: 任务书集合/ directory

Commit `3688f0c` introduced `任务书集合/pricing_parser第四轮审查结论摘要暨第五轮任务书.md` into the branch diff. This file belongs to a historical working-copy directory that is outside the declared formal Round 5A delivery paths. Two steps were taken to resolve this:

1. **`.gitignore` exclusion**: The `任务书集合/` directory was added to `.gitignore` to prevent future accidental promotion of working-copy materials.
2. **Untracked**: All previously tracked files under `任务书集合/` were removed from Git tracking (`git rm --cached -r 任务书集合/`). The working copies remain on disk unchanged.

Commit `3688f0c` is retained in the git history for traceability but is explicitly marked as non-delivery in this report. No formal Round 5A deliverable depends on files under `任务书集合/`.

## Open Review Items

1. `1105 基金投资` versus `1105 交易性基金投资` was normalized to the current practice-manual naming, but this naming bridge remains explicitly documented.
2. `未分配利润` was captured as a concept-level normalized row, but its standard code was deferred in this first pass.
3. Generic derivative wording such as `衍生工具` or `收益互换` remains in review-oriented design assets rather than a forced standard runtime mapping.
4. The existing Markdown working copies were formalized by copying into `docs/reference/markdown/`; any later cleanup should preserve the formal location as the SSOT delivery path for Round 5A.
5. OCR noise remains in the 2018 guidebook Markdown and is documented rather than silently rewritten.

## Next Round Recommendations

### Round 5B

- Start with `valuation_subjects.csv` only.
- Add standard-accounting runtime fields behind the normalized/reference tables from this round.
- Keep mapping confidence and mapping-note fields explicit.
- Do not widen positions or review outputs until subject-layer integration is stable.

### Round 5C and Round 5D

- Treat OTC derivatives as a separate subsystem.
- Start with contract recognition and review-queue output before any lookthrough promise.
- Require supplemental data explicitly for counterparty, contract id, direction, notional, maturity, and underlying exposure.

## Commit Summary

- Drafter commit: `1d13a55` - `docs(assetization): add round5a drafts`
- Reviewer commit: `67ccf64` - `docs(assetization): add round5a pre-implementation review materials`
- Implementer commit: `bf2cfb0` - `feat(reference): add round5a official reference assets`
- Reporter commit: `58d3046` - `docs(report): add round5a execution report`
