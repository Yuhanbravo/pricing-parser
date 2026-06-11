# 文档治理执行报告

## Status

**partial** — P0 修复已实施并验证；P1/P2 修复待用户确认后执行。

## Scope

对 `pricing-parser` 仓库执行 docs-only 文档治理审计与 P0 修复轮次，使用 sibling repository `ai-skill-hub` 中的 `documentation-governance` skill。

**在范围内：**

- `CLAUDE.md`
- `README.md`
- `docs/status.md`
- `tasks/2026-06-11_claude_doc_governance_execution_report.md`（本文件）

**受约束排除：**

- `AGENTS.md` — 审计未发现问题
- `.github/copilot-instructions.md` — 审计未发现问题
- `tasks/README.md` — 审计未发现问题
- `src/`、`config/`、`tests/`、`data_samples/expected/`、`.github/workflows/` — docs-only 保护边界

## Files changed

| 文件 | 变更类型 | 摘要 |
|---|---|---|
| `CLAUDE.md` | 新建 | 本次会话新增的 Claude Code 项目薄入口。委托 `AGENTS.md` 作为主入口，仅保留 Claude Code 专用说明：保持薄层、不复制 `docs/status.md` 可变状态、不扩展为第二规则库、docs-only 任务不修改 `src/`/`config/`/`tests/`/`.github/workflows/`/`data_samples/expected/` |
| `README.md` | 修改（3 次编辑） | P0-1：精简"当前能力"（17 行详细清单 → 4 行能力概述 + SSOT 指针）；P0-2：替换"下一步建议"（4 条编号建议 → 单行指针指向 `docs/status.md`）；新增"文档分类与事实源"小节，位于"样本与数据策略"与"状态文档"之间 |
| `docs/status.md` | 修改（3 次编辑） | P0-3：替换"Repository Rules"（5 条规则清单 → 单行指针指向 `README.md`）；Current Phase 更新（DeepSeek PR Review、接管材料刷新、文档治理优先级、Claude Code 薄入口）；Current Snapshot 补充（`CLAUDE.md` 入口、`ai-skill-hub` sibling 边界）；Recommended Next Steps 重排序（文档治理优先 → 功能迭代后置） |
| `tasks/2026-06-11_claude_doc_governance_execution_report.md` | 新建 | 本报告 |

## What changed

### 审计阶段（只读）

1. 从 sibling repo 读取并确认 `documentation-governance` skill 定义：
   - `SKILL.md` — 执行导向的规范规则集
   - `README.md` — 面向人类的说明与快速上手
   - `prompts/reusable_prompts.md` — 可复用 prompt 模板，含 Mutable Status SSOT Check（模板 3）

2. 扫描 6 个 markdown 文件：`README.md`、`docs/status.md`、`AGENTS.md`、`.github/copilot-instructions.md`、`tasks/README.md`、`CLAUDE.md`。

3. 按受众模型对每个文件分类：
   - `README.md` → human_ai_shared
   - `docs/status.md` → human_primary_archive（事实上的 human_ai_shared）
   - `AGENTS.md` → ai_only_wrapper
   - `.github/copilot-instructions.md` → ai_only_wrapper
   - `CLAUDE.md` → ai_only_wrapper
   - `tasks/README.md` → human_ai_shared

4. 共识别 10 项发现，按 P0/P1/P2 严重度分级。核心发现：
   - **P0-1**：README"当前能力"包含 17 条可变状态事实（适配器列表、运行统计、taxonomy 类型），与 `docs/status.md` 重复
   - **P0-2**：README"下一步建议"与 `docs/status.md` Recommended Next Steps 几乎逐条对应
   - **P0-3**：Repository Rules 在 README、`docs/status.md`、`AGENTS.md` 三处独立陈述
   - AI wrapper 文件（AGENTS、copilot-instructions、CLAUDE）状态健康 — 均保持薄入口

### 修复阶段（仅 P0，仅 README.md + docs/status.md）

| P0 编号 | 文件 | 修复前 | 修复后 |
|---|---|---|---|
| P0-1 | `README.md` | 17 行详细能力清单（含具体 adapter key、运行数量、taxonomy 类型） | 4 行能力概述 + blockquote 指针指向 `docs/status.md` |
| P0-2 | `README.md` | 4 条编号下一步建议 | 单行 blockquote 指针指向 `docs/status.md` |
| P0-3 | `docs/status.md` | 5 条规则清单，与 README 重复 | 单行 blockquote 指针指向 `README.md`（声明为 repository rules 的 SSOT） |

`docs/status.md` 额外更新：

- Current Phase：+4 条（DeepSeek PR Review 已完成、接管材料刷新已完成/待关闭、文档治理优先级、Claude Code 薄入口）
- Current Snapshot：`CLAUDE.md` 纳入 AI 入口列表；新增 `ai-skill-hub` sibling 边界说明
- Recommended Next Steps：+2 条新项（先完成文档治理审计、文档结构稳定后再恢复功能规划）；原 4 条顺延为 #3–#6

### CLAUDE.md 新建

在仓库根目录新建 `CLAUDE.md` 作为 Claude Code 专用项目入口（ai_only_wrapper）。内容设计遵循薄入口原则：

- 委托 `AGENTS.md` 作为主入口（首行 `@AGENTS.md`），不重复其内容
- 列出 Claude Code 专用说明：保持文件精简、不复制 `docs/status.md` 可变状态、不扩展为第二规则库
- 声明可读路径：`README.md`（稳定约定）、`docs/status.md`（可变状态 SSOT）、`tasks/README.md`（任务包约定）
- 声明 docs-only 任务保护边界：`src/`、`config/`、`tests/`、`.github/workflows/`、`data_samples/expected/` 不受文档任务修改
- 声明 sibling `ai-skill-hub` 仅作参考，不进入本仓库

### README.md 新增小节

"文档分类与事实源"（15 行）记录分类框架：
- AI-only wrapper（`AGENTS.md`、`.github/copilot-instructions.md`、`CLAUDE.md`）
- Human-AI shared（`README.md`）
- Current-state SSOT（`docs/status.md`）
- Task records（`tasks/` — 审计留痕，不是规则中心）
- 关键边界：SSOT 唯一性、历史文档不反向覆盖当前状态、AI 入口保持薄层、`ai-skill-hub` 为 sibling reference

## Validation results

- **自动化测试**：`not_run` — 按 `README.md` PR 协作约定，仅文档改动可将源码测试标记为 `not_run`，并说明原因。本次所有改动均不涉及 `src/`、`config/`、`tests/`、`data_samples/expected/`。
- **手动验证**：每次编辑后均使用 Read 工具回读确认；所有修改段落的结构、指针链接和内容均已验证正确。
- **Git 变更范围检查**：`passed` — 使用 `git status` 与 `git diff --name-only` 确认本次会话仅触及以下文件：`CLAUDE.md`（新建）、`README.md`（修改）、`docs/status.md`（修改）、`tasks/2026-06-11_claude_doc_governance_execution_report.md`（新建）。未修改 `src/`、`config/`、`tests/`、`data_samples/expected/`、`.github/workflows/` 中的任何文件，也未提交 `output/`、`tmp/` 或 raw 样本等产物。
- **Markdown lint**：`not_run` — 渲染输出中未观察到结构问题。
- **DeepSeek PR Review**：`triggered` / `passed` — DeepSeek PR Review 配置已在本次治理训练之前的会话中完成并触发成功，本次报告记录该结果。本次 docs-only 变更集未修改 parser 行为、路由、适配器、taxonomy、导出或 review 逻辑。

## Deviations from task package

1. 审计报告中的 P1/P2 项未执行 — 设计意图（用户确认仅 P0 范围）。
2. `docs/status.md` 的 Current Phase / Current Snapshot / Next Steps 更新超出了原始 P0 清单 — 由用户在后续指令中追加。

## Risks and follow-ups

### 风险

- **P1 债务**：`README.md` 中"当前已验证的真实样表"和"Round 4 资产术语口径补充"子节仍保留为可变状态快照。如果 `docs/status.md` 更新而 README 未同步，这些段落将过时并形成第二（分歧）事实源。
- **语言不一致**：`docs/status.md` 使用英文，`README.md` 使用中文。当前不构成冲突，但未来贡献者入职时需注意。
- **接管材料关闭状态**：`docs/status.md` 中标注接管材料刷新为 `pending final closure review`。如该审查未执行，状态文件将长期保留未决声明。

### 后续跟进

| # | 事项 | 优先级 | 可分配给 |
|---|---|---|---|
| 1 | 执行 P1 修复（README 样表列表移除、Round 4 补充移除、开头段去 Round 4、AGENTS.md Work Boundaries 精简） | P1 | 下一次文档会话 |
| 2 | 完成接管材料审查，解决 `pending final closure review` 状态 | P2 | 人类审查者 |
| 3 | 任何触及 `data_samples/expected/` 或测试 fixture 的后续 P1/P2 修复后，重新运行 `python -m pytest` | P2 | CI 或开发者 |
| 4 | 如未来新增 `docs_readable/`，强制实施衍生层约束 | P2 | 未来 |

## 实习生学习记录

### Claude Code CLI 基本用法

- Claude Code 在会话启动时从 `CLAUDE.md`（如存在）和 `AGENTS.md` 读取项目上下文。
- Read 工具可以访问 sibling 目录（如 `../ai-skill-hub/`）— 确认 sibling repo 读取成功。
- Edit 工具要求精确字符串匹配；从 Read 输出构造 `old_string` 时必须去除行号前缀。

### 文档分类学习

- **AI-only wrapper**：如 `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md`。这类文件应仅包含稳定的指针引用和工作边界 — 不含可变项目状态，不复制规则。
- **Human-AI shared**：`README.md` — 稳定的入门内容（安装、运行、结构、约定）。可包含简要能力概述，但详细内容必须链接到 SSOT。
- **Human-primary archive / SSOT**：`docs/status.md` — 当前阶段、快照、支持范围、已知缺口和下一步建议的唯一事实源。所有其他文件必须引用而非复制此文件中的可变事实。
- **Task records**：`tasks/` — 执行报告和任务包是历史审计记录，不是活跃的规则中心。

### AI-only / human-ai shared / human-primary 三类文档的区别

| 维度 | AI-only wrapper | Human-AI shared | Human-primary SSOT |
|---|---|---|---|
| 主要受众 | AI 代理（Codex、Copilot、Claude） | 两者 | 人类审查者与决策者 |
| 内容类型 | 指针、边界、工具专用提示 | 稳定说明、约定、命令 | 当前状态、指标、决策、缺口 |
| 可变事实？ | 从不 | 仅稳定摘要 + 链接 | 是 — 这是 SSOT |
| 示例 | `AGENTS.md` | `README.md` | `docs/status.md` |
| 如果变长了…… | 可能已变成第二规则库 — 应精简 | 可能在复制 SSOT — 应改为链接 | 可能需要拆分为子文档 |

### Sibling repository 读取结果

- **状态**：成功。
- **路径**：`D:\dev\pricing_parser\ai-skill-hub\skills\documentation-governance\`
- **已读文件**：`SKILL.md`（124 行）、`README.md`（139 行）、`prompts/reusable_prompts.md`（92 行）。
- **结果**：三个文件均成功加载到上下文中，并用于驱动审计方法论。未将任何文件从 `ai-skill-hub` 复制到 `pricing-parser` 仓库。

### 开放问题

1.是否应将 `CLAUDE.md` 加入 `README.md` 的项目结构树中（当前仅列出了 `AGENTS.md`）？
