# Copilot Instructions

Use `AGENTS.md` as the project entry point. Treat `README.md`, `docs/status.md`, `pyproject.toml`, `config/`, and `tests/` as the canonical sources for current behavior.

When suggesting code:

- Follow the existing module boundaries under `src/valuation_parser/`.
- Prefer small, test-backed changes over broad rewrites.
- Read the nearest existing test before changing parser, routing, adapter, taxonomy, export, or review behavior.
- Follow the PR collaboration conventions in `README.md` before suggesting branch names, PR summaries, or validation notes.
- Do not generate real raw valuation samples or commit generated outputs.
- Do not copy ai-skill-hub workflow rules into this repository; link or reference them through task packages when needed.

This file is a Copilot adapter only. Keep project status, business rules, and workflow details in their canonical files.
