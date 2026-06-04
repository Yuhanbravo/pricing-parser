# Task Package: repo-ai-entrypoints-minimal-bootstrap

## Goal

Add minimal AI collaboration entry points for GitHub Copilot and Codex, while preserving existing repository documents as the canonical sources.

## Scope

- Add `AGENTS.md`.
- Add `.github/copilot-instructions.md`.
- Add `tasks/README.md`.
- Persist the repository AI initialization scan under `tasks/`.
- Produce an execution report after implementation.

## Non-goals

- Do not modify parser code.
- Do not modify adapter, routing, taxonomy, export, or review behavior.
- Do not rewrite `README.md` or `docs/status.md`.
- Do not copy ai-skill-hub workflow rules into this repository.
- Do not introduce a new governance system.

## Authorized Modification Paths

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `tasks/README.md`
- `tasks/2026-06-04_repo_ai_initialization_scan.md`
- `tasks/2026-06-04_repo_ai_entrypoints_minimal_bootstrap_task_package.md`
- `tasks/2026-06-04_repo_ai_entrypoints_minimal_bootstrap_execution_report.md`

## Acceptance Criteria

- `AGENTS.md` identifies the project and points to canonical source files.
- `.github/copilot-instructions.md` is Copilot-specific and does not duplicate project rules.
- `tasks/README.md` defines minimal task package and execution report conventions.
- The scan and task package are saved under `tasks/`.
- No files under `src/`, `config/`, `tests/`, or `data_samples/expected/` are changed.
- Validation results are recorded in the execution report.

## Suggested Validation Commands

```powershell
git status --short
python -m pytest
```

## Execution Report Format

- Status
- Files changed
- What changed
- Validation
- Deviations from task package
- Risks / follow-ups
