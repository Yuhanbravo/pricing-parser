# AI Agent Entry

This repository is a Python valuation statement parser. It is organized around mapping-driven routing, shared parsing/export logic, and custodian adapters.

## Read First

- `README.md`: project scope, workspace boundary, install/run commands, sample and data policy.
- `docs/status.md`: current supported scope, latest verified baseline, known gaps, recommended next steps.
- `pyproject.toml`: package metadata, dependencies, CLI entry point, pytest configuration.
- `config/`: adapter, taxonomy, and code normalization configuration.
- `tests/`: executable behavior contract.
- `tasks/README.md`: task package and execution report conventions.

## Minimal Commands

```powershell
python -m pip install -e .[dev]
python -m pytest
```

CLI usage is documented in `README.md`; prefer those examples over inventing new command shapes.

## Work Boundaries

- Repository-level rules (workspace boundaries, sample policy, output conventions, PR validation) are defined in `README.md`; this section covers AI-agent-specific behavior only.
- Before changing behavior, inspect the related module under `src/valuation_parser/` and the matching tests.
- If a task changes routing, adapter behavior, taxonomy, exports, or review logic, update focused tests with the change.

## Thin Entry Rule

This file is only an entry point. Do not turn it into a second rulebook. Put durable project facts in `README.md` or `docs/status.md`, executable contracts in `tests/`, and parser rules in `config/` or `src/valuation_parser/`.
