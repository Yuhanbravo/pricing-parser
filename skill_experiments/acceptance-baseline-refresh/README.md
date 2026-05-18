# Acceptance Baseline Refresh

本目录是 `pricing_parser` 仓库内的项目本地实验 skill，用于把受控样本 baseline 刷新流程固定为一条可复述、可审查、可留痕的工作线：

`重跑 -> 比对 -> 判定 -> 刷新 -> 同步文档`

它解决的问题不是“如何生成输出”，而是“当输出契约有意变化时，如何避免直接覆盖 expected baseline 并丢失判断过程”。

本轮 Round 4 中，这个实验 skill 用于辅助以下事项：

- 对 `data_samples/raw/` 的全量 11 份受控样表做一次受控重跑
- 比较新输出与既有 `data_samples/expected/` 的差异
- 判断差异是契约更新还是潜在回归
- 在确认是预期变化后刷新 `data_samples/expected/`
- 同步 `README.md`、`docs/HANDOFF.md`、`docs/status.md` 与任务报告

按 Round 4 任务书要求，这个实验 skill 需要至少覆盖：

- 何时使用 baseline refresh，而不是直接覆盖 expected
- baseline refresh 的输入、输出和约束
- refresh 前必须先有 focused validation
- refresh 后必须补报告与状态同步
- 与 `workflow-bootstrap`、`chatgpt-handoff-pilot` 的边界

边界：

- 这是项目内实验资产，不是正式 canonical skill。
- 本轮不把它同步到 `ai-skill-hub`。
- 本轮不把它放入 `.codex/skills/` 作为正式运行时入口。
- 它只补充 baseline refresh 的流程意识，不替代 `workflow-bootstrap` 或 `chatgpt-handoff-pilot`。

当前局限：

- 仍以文档化流程为主，没有额外自动化 orchestrator。
- workbook 目前只做结构与命名层面的说明，未建立单独 workbook acceptance baseline。
- 差异分类仍依赖实现者结合 task package 与 parse summary 做人工判断。

本轮补充结论：

- 在第一次 taxonomy baseline refresh 之后，后续 swap-margin taxonomy 修复又触发了一次 follow-up 复核。
- 该次 follow-up 表明文本 baseline 已经同步，无需再次刷新 expected。
- 这说明该实验 skill 不仅适用于“批准刷新”，也适用于“确认当前 baseline 已同步，因此拒绝无必要刷新”。

若后续要进入 `ai-skill-hub`，仍需补齐：

- 更清晰的适用边界与反例
- 更稳定的输入 / 输出模板
- 与 handoff / status / assessment 的协议衔接说明
- 跨项目复用所需的更通用示例