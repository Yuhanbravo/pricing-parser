# Repository AI Initialization Scan

## Scan Summary

1. Root structure includes `src/`, `tests/`, `config/`, `data_samples/`, `docs/`, `tasks/`, and `skill_experiments/`.
2. Python package lives under `src/valuation_parser/`; `pyproject.toml` names the project `valuation-parser`.
3. CLI entry point is `valuation-parser = valuation_parser.cli:main`.
4. Core modules include `cli.py`, `pipeline.py`, `routing.py`, `mapping_loader.py`, `product_identity.py`, `exporters.py`, `taxonomy.py`, and `normalizers.py`.
5. Adapter modules live under `src/valuation_parser/adapters/` and include custodian-specific adapters plus `generic`.
6. Configuration lives under `config/`, especially `asset_taxonomy.yaml`, `code_rules.yaml`, and `config/adapters/*.yaml`.
7. Tests live under `tests/` and cover routing, mapping, identity, adapters, taxonomy, exports, review items, smoke, and acceptance baseline behavior.
8. Install command is `python -m pip install -e .[dev]`.
9. Test command is `python -m pytest`.
10. Runtime examples and data policy are already documented in `README.md`.
11. Current project state and known gaps are already documented in `docs/status.md`.
12. Existing project guidance includes `README.md`, `docs/status.md`, `docs/HANDOFF.md`, `MIGRATION_PLAN.md`, `单项目 Commit Convention（轻量版）.md`, and `Git与Bundle开发协作规范_实习生版.md`.
13. `tasks/` already contains task packages, review notes, and execution reports, but did not yet have a directory-level README.
14. `AGENTS.md` and `.github/copilot-instructions.md` were not present before this initialization.
15. Main risks are historical snapshots being mistaken for current contracts, large reference assets being over-scanned, and new AI entries duplicating canonical documentation.

## Minimal Supplemental Information Gaps

- Confirm the team's preferred PR branch naming pattern.
- Confirm whether GitHub Actions or another CI runner is authoritative.
- Confirm whether `python -m pytest` is the required PR validation command or only the local default.
- Confirm whether future ai-skill-hub workflow references should point to a sibling repo path, bundle artifact, or published package.

## Canonical Source Map

- Project scope and run commands: `README.md`
- Current status and known gaps: `docs/status.md`
- Dependencies and test configuration: `pyproject.toml`
- Parser behavior: `src/valuation_parser/`
- Parser rules and taxonomy: `config/`
- Executable contract: `tests/`
- Task package and execution report trail: `tasks/`

## Recommended Minimal Entry Files

- `AGENTS.md`: project-side thin entry with canonical backreferences.
- `.github/copilot-instructions.md`: Copilot-specific thin adapter.
- `tasks/README.md`: directory convention for task packages and execution reports.

Do not expand these files into a second project rulebook.
