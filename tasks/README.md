# Tasks Directory

`tasks/` stores bounded task packages, review notes, and execution reports for AI-assisted work. Historical files are audit trail, not automatically current project rules.

## File Names

Use descriptive names that are easy to sort and review:

- `<date>_<task-name>_task_package.md`
- `<date>_<task-name>_execution_report.md`
- `<date>_<task-name>_need_review.md` when human review is explicitly needed

Examples:

- `2026-06-04_repo_ai_entrypoints_minimal_bootstrap_task_package.md`
- `2026-06-04_repo_ai_entrypoints_minimal_bootstrap_execution_report.md`

## Task Package Minimum Fields

- Task name
- Goal
- Scope
- Non-goals
- Authorized modification paths
- Acceptance criteria
- Suggested validation commands

## Execution Report Minimum Fields

- Status: `done`, `partial`, or `blocked`
- Files changed
- What changed
- Validation results
- Deviations from the task package
- Risks and follow-ups

## Boundary

Keep workflow conventions here lightweight. Project facts belong in `README.md` and `docs/status.md`; code behavior belongs in `src/`, `config/`, and `tests/`.
