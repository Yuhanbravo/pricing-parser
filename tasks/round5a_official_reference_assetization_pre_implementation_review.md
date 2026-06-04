# Round 5A Official Reference Assetization Pre-Implementation Review

## Reviewer Role

本文件是 `workflow-bootstrap` 角色链中的 Reviewer 阶段产物。

本阶段职责是对 `tasks/round5a_official_reference_assetization_task_package.md` 做 implementation 前 safety gate 审查，确认边界是否清晰、是否存在范围漂移、以及验收是否具备可验证性。

本文件不新增需求，不进入实现，不替代 task package。

## Review Target

- Reviewed task package: `tasks/round5a_official_reference_assetization_task_package.md`
- Review focus: scope safety, protocol boundary, acceptance verifiability

## Review Summary

审查结论：`Pass with boundary reminders`

判断依据：当前 task package 已具备进入 Implementer 阶段的最小条件，尤其对以下四条高风险越界点写得足够明确：

- 不改 parser 逻辑
- 不改 adapters
- 不刷新 baseline
- 不改输出契约

未发现阻止进入实现的 P0/P1 级范围错误。

需要强调的是，Implementer 仍必须严格按 task package 执行，不得把本 Reviewer 文档中的提醒理解为新增授权。

## Safety Gate Checks

### 1. 是否明确禁止修改 parser 逻辑

结论：`明确，可通过`

检查结果：

- Scope 已写明本轮只做 `reference/data/documentation` 资产化，不改 parser runtime 行为。
- Non-goals 已明确“不修改 `src/` 下 parser 核心逻辑”。
- Acceptance Criteria 第 12 条再次要求本轮改动不得进入 `src/` 主解析逻辑。

Reviewer 判断：

- 当前任务包已把 parser 运行时改动排除在外。
- 即使后续需要说明字段分层、映射设计或衍生品支线，也只能停留在 reference/design 层，不得借机进入实现层。

边界提醒：

- 若施工中发现某个 reference 资产设计需要代码配合，默认应记录到 Round 5B 或后续轮次，不在本轮落地。

### 2. 是否明确禁止修改 adapters

结论：`明确，可通过`

检查结果：

- Non-goals 已明确“不修改 adapters”与“不新增 adapter”。
- Acceptance Criteria 第 12 条再次将 adapter 排除在允许改动之外。

Reviewer 判断：

- 当前 task package 没有给 adapter 修订、补 mapping 或接入新样本留下隐性口子。

边界提醒：

- 不得因为官方文档中出现新的科目或衍生品表述，就顺手扩展 adapter 识别逻辑。

### 3. 是否明确禁止刷新 baseline

结论：`明确，可通过`

检查结果：

- Non-goals 已明确“不刷新 `data_samples/expected/` baseline”。
- Acceptance Criteria 第 12 条再次要求不得进入 expected baseline refresh。
- Validation Requirements 要求跑 `pytest -q`，但没有把 baseline refresh 作为本轮验证动作。

Reviewer 判断：

- 当前任务包已把 baseline 维持为只读证据面，符合“reference-only round”的边界。

边界提醒：

- 本轮验证可以证明“未破坏现状”，但不能把“需要新 baseline 才能通过”的实现混进来。

### 4. 是否明确禁止修改输出契约

结论：`明确，可通过`

检查结果：

- Non-goals 已明确“不修改 `valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv` 现有 runtime 输出字段”。
- Goal 和 Acceptance Criteria 都把标准会计科目层定位为 design/reference 资产，而不是本轮输出字段接入。

Reviewer 判断：

- 当前任务包已将“标准会计科目层设计”与“parser 输出契约变更”清楚拆开。
- 这能有效防止 Implementer 在 Round 5A 提前加入 `account_code_std` 等 runtime 字段。

边界提醒：

- 任何 `subjects / positions / review_items / summary` 的运行时字段改动都应延后到 Round 5B 再单独立项。

### 5. 是否把官方口径误写成 runtime 配置替代品

结论：`未误写，可通过`

检查结果：

- Non-goals 已明确“不把官方参考文件直接作为 parser runtime 配置”。
- Acceptance Criteria 第 10 条明确官方口径是标准化底座，不直接替代 Round 4 展示分类。

Reviewer 判断：

- 当前任务包保持了“官方标准科目层”和“现有 taxonomy 展示层”的分层关系。
- 这与上游第五轮任务书要求一致，没有把 reference 资产误写成配置覆盖层。

边界提醒：

- `docs/reference/` 与 `data/reference/` 下的资产只提供设计和抽取依据，不应在本轮被 parser 直接读取。

### 6. 是否存在会引起实施歧义的轻微点

结论：`有轻微提醒，但不构成阻塞`

检查结果：

- Allowed Changes 中已注明 Markdown 转换“已经完成”，且当前文件位置写在 `任务书集合/` 下。
- 但 Target Files 与 Acceptance Criteria 仍把正式交付位置定义为 `docs/reference/markdown/`。

Reviewer 判断：

- 这更像是当前实施状态说明，不是范围错误。
- 但 Implementer 在开工时应把“已有 Markdown 是否直接迁移为正式交付物”与“是否保留 `任务书集合/` 中的历史工作稿”处理清楚，并在 execution report 里写明。

边界提醒：

- 不要因为已有工作稿存在，就跳过 manifest、正式目录落盘和可复核性说明。

## Additional Reviewer Notes

### Scope clarity

当前 task package 已具备 bounded execution 所需的最小字段：

- Goal
- Scope
- Explicit Non-goals
- Target Files
- Acceptance Criteria
- Validation Requirements
- Execution Report Requirements

因此，Reviewer 不要求回退 Drafter 重写任务包。

### Residual risks

以下风险尚未构成阻塞，但实施时应保持警惕：

1. 已完成的 Markdown 工作稿若不落到 task package 约定目录，后续 evidence chain 会分叉。
2. `data/reference/` 与 `docs/reference/` 资产较多，Implementer 应坚持先做最小必需集，不要追求一次性全量抽取。
3. OTC derivative 文档容易诱发实现冲动，本轮必须停留在 design/reference 层。

## Reviewer Decision

Reviewer decision: `Pass`

允许进入 Implementer 阶段，前提如下：

1. 严格遵守 task package 中已列明的 Non-goals。
2. 不以 reference assetization 为名义修改 parser 逻辑、adapters、routing 或输出契约。
3. 不刷新 expected baseline。
4. 已有 Markdown 工作稿必须在实施中被明确纳入正式交付路径或在 execution report 中解释其关系。
5. 实施完成后必须用验证结果和 execution report 证明边界被遵守，而不是只凭文件新增数量。

## Handoff To Implementer

Implementer 应基于已审 task package 做 bounded execution。

本 Reviewer 文件只确认“可以开始做”，不增加任何超出 task package 的新授权。