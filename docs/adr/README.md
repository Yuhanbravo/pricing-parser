# ADR 决策记录

`docs/adr/` 是本仓库的轻量级 Architecture / Owner Decision Record 层，用于记录 owner 已确认或正在讨论的项目级决策。ADR 文档是人机共读文档，中文为主，必要时保留英文术语辅助对齐。

## 目的

ADR 用于帮助 owner、developer、reviewer、intern 和 AI agent 区分：

- 哪些事项已经由 owner 正式决定；
- 哪些内容仍只是 roadmap planning；
- 哪些材料是历史 execution record；
- 哪些未来变更在实现前需要 owner decision。

ADR 是 formal owner decision record。它记录重要决策、被拒绝的替代方案、被推迟的事项，以及被后续决策取代的历史结论。

## 与既有文档的关系

ADR 不替代以下文档：

- [`README.md`](../../README.md)：稳定项目说明、工作区边界、安装运行方式、样本策略、PR 协作约定和文档入口。
- [`docs/status.md`](../status.md)：当前状态、支持范围、已知缺口和下一步建议的 SSOT。
- [`docs/roadmap.md`](../roadmap.md)：多轮路线图、阶段排序和未来工作拆分。
- [`docs/HANDOFF.md`](../HANDOFF.md)：交接事实和接手上下文。
- [`MIGRATION_PLAN.md`](../../MIGRATION_PLAN.md)：迁移路径与计划中的收敛工作。
- [`tasks/`](../../tasks/)：任务包、execution report、review notes 和历史 audit trail。

ADR 只记录 owner decision 本身及其直接影响，不复制 current status snapshot，不复制长篇 roadmap，也不替代 task report。

## 状态值

ADR 必须使用以下状态之一：

- `Proposed`：讨论草案，尚未被 owner 接受。
- `Accepted`：owner 已接受，可作为实现指导。
- `Rejected`：已明确拒绝，保留用于追溯。
- `Superseded`：已被后续 ADR 取代。
- `Deferred`：暂缓决定，后续再通过 ADR 或任务继续推进。

只有 `Accepted` ADR 可以作为 implementation guidance。`Proposed` ADR 只是 discussion draft，不能作为 runtime behavior、output contract、baseline 或 sample policy 变更的权威依据。

## 命名约定

ADR 文件使用以下命名格式：

```text
0001-short-kebab-case-title.md
```

编号 append-only。历史 ADR 不重排、不复用编号、不因后续新增或删除而 renumber。

## 适用范围

适合写入 ADR 的事项包括：

- product boundary decisions；
- architecture decisions；
- output-contract decisions；
- sample / fixture governance decisions；
- owner-approved semantic decisions。

## 非目标

ADR 不用于：

- 存放当前状态快照；
- 复制长篇 roadmap text；
- 变成 task report 或 execution report；
- 隐藏 runtime behavior change；
- 绕过正常任务包、PR review、validation 和 baseline 管理。
