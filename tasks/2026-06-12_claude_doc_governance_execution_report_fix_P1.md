# 文档治理 P1 修复执行报告

## Status

**done** — 全部 4 项 P1 修复已实施并验证；P2 项仍为后续待确认项。

## Scope

对 `pricing-parser` 仓库执行 docs-only 文档治理 P1 修复，基于 2026-06-11 审计报告中 follow-up 表 #1 的 P1 清单。

**在范围内：**

- `README.md`（3 处 P1 修复）
- `AGENTS.md`（1 处 P1 修复）
- `tasks/2026-06-12_p1_fix_execution_report.md`（本文件）

**受约束排除：**

- `src/`、`config/`、`tests/`、`data_samples/expected/`、`.github/workflows/` — docs-only 保护边界
- `ai-skill-hub` — sibling reference repository，不进入本仓库

## Files changed

| 文件 | 变更类型 | 摘要 |
|---|---|---|
| `README.md` | 修改（3 次编辑） | P1-1：开头段去 Round 4（17 行交付细节 → 1 句项目概述 + SSOT 指针）；P1-2：样表列表移除（8 条文件名→适配器映射 → blockquote 指针）；P1-3：Round 4 补充移除（4 条历史 taxonomy 决策 → blockquote 指针指向 config/tests + SSOT） |
| `AGENTS.md` | 修改（1 次编辑） | P1-4：Work Boundaries 精简（6 条 → 3 条：合并 4 条与 README 重复的项目规则为 1 条指针，保留 2 条 AI-agent 专属行为规则） |
| `tasks/2026-06-12_p1_fix_execution_report.md` | 新建 | 本报告 |

## What changed

### 修复前状态

2026-06-11 审计识别了 10 项发现，其中 P0 已修复（仅 `README.md` + `docs/status.md`）。P1 修复被明确推迟到"下一次文档会话"，记录在 `2026-06-11_claude_doc_governance_execution_report.md` 的 follow-up 表 #1 中。

P1 的共同问题：**在非 SSOT 文件中复制了可变状态或规则，形成了第二事实源**，违反了 documentation-governance skill 的核心原则：

> "可变项目状态事实必须留在已声明的 current-state SSOT 中。`README.md`、`AGENTS.md` 等可以引用 SSOT，但不应复制 active phase status，避免形成第二事实源。"

### 修复详情

| P1 编号 | 文件 | 修复前 | 修复后 |
|---|---|---|---|
| P1-1 | `README.md` 开头段 | 17 行 Round 4 交付细节（11 份样表、8 个 adapter key、运行统计、taxonomy 口径、`3102*` 规则） | 2 行项目概述（项目定位 + 功能描述） + blockquote 指针指向 `docs/status.md` |
| P1-2 | `README.md` 样表列表 | "当前已验证的真实样表"小节：8 条具体文件名→适配器映射 | blockquote 指针指向 `docs/status.md` Current Snapshot |
| P1-3 | `README.md` Round 4 补充 | "Round 4 资产术语口径补充"小节：4 条历史 taxonomy 决策（ETF 归类、收益互换归类、非证券科目处理、PRODUCT_022 范围） | blockquote 指针指向 `config/asset_taxonomy.yaml`、`src/valuation_parser/taxonomy.py`、`tests/` + `docs/status.md` Supported Scope |
| P1-4 | `AGENTS.md` Work Boundaries | 6 条规则（workspace 边界、样本策略、输出约定、PR 验证、behavior 检查、测试更新），其中前 4 条与 `README.md` 重复 | 3 条规则（1 条委托指针指向 `README.md` + 2 条 AI-agent 专属行为规则） |

### P1 修复原理

每项修复都遵循同一模式：**用 SSOT 指针替换复制的可变内容**。

- P1-1 和 P1-2 是"可变状态快照"问题：`docs/status.md` Current Snapshot 已经维护了运行统计、适配器列表和 taxonomy 类型，README 中不应另行维护副本。
- P1-3 是"历史快照"问题：Round 4 taxonomy 决策已经在 `config/` 和 `tests/` 中落地为 parser 行为，此处保留会随 config 更新而过时。
- P1-4 是"规则重复"问题：AGENTS.md 作为 AI-only wrapper 应保持薄入口，不应复制 README 中已有的项目级规则。

## Validation results

- **自动化测试**：`not_run` — 按 `README.md` PR 协作约定，仅文档改动可将源码测试标记为 `not_run`。本次所有改动均不涉及 `src/`、`config/`、`tests/`、`data_samples/expected/`、`.github/workflows/`。
- **手动验证**：每次编辑后均确认修改正确；所有修改段落的结构、指针链接和内容均已验证。
- **Git 变更范围检查**：`passed` — 确认本次会话仅触及 `README.md`（修改）、`AGENTS.md`（修改）、`tasks/2026-06-12_p1_fix_execution_report.md`（新建）。未修改 `src/`、`config/`、`tests/`、`data_samples/expected/`、`.github/workflows/` 中的任何文件。
- **Markdown lint**：`not_run` — 渲染输出中未观察到结构问题。
- **DeepSeek PR Review**：`triggered` / `passed` — DeepSeek PR Review 配置已在本次治理训练之前的会话中完成并触发成功，本次报告记录该结果。

## Deviations from task package

1. 本次 P1 修复未使用 sibling `ai-skill-hub` 的 documentation-governance skill 重新审计，而是直接基于上一轮审计报告的 follow-up 表 #1 执行 — 设计意图（审计已完成，此为执行轮次）。
2. 未更新 `docs/status.md` — P1 修复均为移除第二事实源，不涉及新的项目状态变更。

## Risks and follow-ups

### 风险

- **无新增风险**。P1 修复消除了执行报告中记录的 P1 债务（README 中可变状态快照形成第二事实源的风险）。

### 后续跟进

| # | 事项 | 优先级 | 可分配给 | 来源 |
|---|---|---|---|---|
| 1 | 完成接管材料审查，解决 `pending final closure review` 状态 | P2 | 人类审查者 | 2026-06-11 审计 |
| 2 | 任何触及 `data_samples/expected/` 或测试 fixture 的后续修复后，重新运行 `python -m pytest` | P2 | CI 或开发者 | 2026-06-11 审计 |
| 3 | 如未来新增 `docs_readable/`，强制实施衍生层约束 | P2 | 未来 | 2026-06-11 审计 |

## 实习生学习记录

### P0 vs P1 vs P2 严重度分级理解

- **P0**：SSOT 冲突 — 同一事实在多处独立维护，一处更新则另一处自动过时。例如：README 中 17 行能力清单与 `docs/status.md` 中的 Current Snapshot 独立陈述。
- **P1**：第二事实源 — 在非 SSOT 文件中复制了可变状态（如具体文件名→适配器映射、历史 taxonomy 决策），虽然尚未形成冲突，但随时可能因 SSOT 更新而分歧。
- **P2**：流程/策略类 — 需要人类决策（接管材料审查）、条件触发（pytest 运行）、或未来策略（`docs_readable/` 约束）。

### AI-only wrapper 中规则重复的识别

- `AGENTS.md` 的 6 条 Work Boundaries 中，前 4 条（workspace 边界、样本策略、输出约定、PR 验证）在 `README.md` 中已有完整定义。
- AI wrapper 的目标是"薄入口"，规则应委托给权威源，而不是复制权威源的内容。
- 后 2 条（behavior 检查、测试更新）是 AI-agent 专属行为指引，在 README 中没有对应，因此保留在 AGENTS.md 中。

