# Round 4 Asset Taxonomy Pre-Implementation Review

## Reviewer Role

本文件是 `workflow-bootstrap` 角色链中的 Reviewer 阶段产物。

本阶段职责是对 `tasks/round4_asset_taxonomy_task_package.md` 做 implementation 前 safety gate 审查，确认边界是否清晰、是否存在范围漂移、以及验收是否具备可验证性。

本文件不新增需求，不进入实现，不替代 task package。

## Review Target

- Reviewed task package: `tasks/round4_asset_taxonomy_task_package.md`
- Review focus: scope safety, protocol boundary, acceptance verifiability

## Review Summary

审查结论：`Pass with boundary reminders`

判断依据：当前 task package 已基本满足进入 Implementer 阶段的最小条件，目标、范围、非目标、目标文件、验收标准与测试要求均已明确，且核心边界与 Round 4 任务书保持一致。未发现阻止进入实现的 P0/P1 级范围错误。

需要强调的是，Implementer 仍必须严格按 task package 执行，不得把下列提醒理解为新增授权。

## Safety Gate Checks

### 1. Taxonomy 与 review 逻辑是否混在一起

结论：`基本未混入，可通过`

检查结果：

- task package 已明确要求 taxonomy 字段与 `review_flag` / `review_note` / `review_category` 分离。
- 验收标准中已单列 `review_items.csv` 的 review 字段要求，并强调 review 分类与资产分类分离。
- 测试要求中也包含了 review 分离测试，能对该边界形成验证支撑。

Reviewer 判断：

- 当前任务包没有把“是否需要复核”重新编码进 `asset_type_internal` 或其它 taxonomy 字段。
- 当前表述仍允许在 subjects / review_items 中保留 `review_category`，这与 Round 4 任务书一致，不构成混用。

边界提醒：

- Implementer 不得借由 taxonomy 配置去吸收 review 规则主体。
- `config/asset_taxonomy.yaml` 只能承载术语映射与展示口径，不应成为 review 规则主载体。

### 2. 是否误伤旧 `asset_type` 字段

结论：`未误伤，可通过`

检查结果：

- Scope 已明确“保留现有 `asset_type` 字段，同时新增稳定 taxonomy 字段”。
- Acceptance Criteria 第 2 条明确要求保留旧字段，且不得删除或静默改写语义。

Reviewer 判断：

- 当前 task package 对旧字段采取兼容保留策略，符合 Round 4 任务书要求。
- 未出现要求替换、重命名、移除旧 `asset_type` 的语句。

边界提醒：

- Implementer 可以补充新字段，但不得把下游现有依赖旧 `asset_type` 的行为直接改写为只认新字段。

### 3. 是否扩大到 adapter 或 routing

结论：`边界总体清晰，可通过`

检查结果：

- Non-goals 已明确不新增 adapter、不改变 routing 逻辑、不改变核心持仓识别规则。
- Acceptance Criteria 也要求本轮实际改动不得扩展到 adapter、新样本接入或 routing 逻辑修改。
- Target Files 虽允许触达 `src/valuation_parser/` 相关模块，但限定为 taxonomy 加载、字段透传、summary 输出、review/export 流程直接相关模块。

Reviewer 判断：

- 当前任务包没有给 adapter 扩展、mapping 扩展或 routing 改写授权。
- 源码目录授权采用了“允许必要模块，但以 taxonomy 集成为限”的写法，边界足够，但执行时要防止借口式扩张。

边界提醒：

- 若实现过程中发现某个 taxonomy 需求需要改 routing、改 adapter、改识别规则，默认应停止扩展并记录为 follow-up，而不是顺手纳入本轮。

### 4. 是否把 `PRODUCT_022` 混进本轮

结论：`未混入，可通过`

检查结果：

- Non-goals 已明确“不处理 `PRODUCT_022`”。
- Acceptance Criteria 第 14 条也再次要求本轮实际改动不得扩展到 `PRODUCT_022` 处理。

Reviewer 判断：

- 当前 task package 仅把 `PRODUCT_022` 作为排除项处理，没有把它作为验收对象、实现目标或测试样本扩展目标。
- 这与 Round 4 任务书中的人工裁决一致。

边界提醒：

- Implementer 不得为消除单个 routing failure 而新增 mapping、adapter 或 fallback 特判来触碰 `PRODUCT_022`。

### 5. 验收是否能通过测试和 baseline 刷新证明

结论：`可证明，但需要严格按 task package 执行`

检查结果：

- Acceptance Criteria 已将输出字段、summary 口径、known business rules、expected baseline、文档同步和边界约束写成可检查项。
- Test Requirements 已覆盖 taxonomy 配置加载、known mapping、unknown fallback、exporter 字段、summary 展示、review 分离、smoke / acceptance。
- Scope 已要求 baseline 刷新前先完成重跑和 diff 判定。

Reviewer 判断：

- 现有 task package 具备“通过测试 + baseline refresh + 文档同步”来证明完成度的条件。
- 其中最关键的证据链是：重跑输出 -> diff 判定 -> expected baseline 刷新 -> smoke/acceptance 通过。

边界提醒：

- 若本轮只改代码但未同步 expected baseline、未记录 diff 判定、或未更新文档，则不应视为满足验收。

## Additional Reviewer Notes

### Scope clarity

当前 task package 结构完整，已具备 bounded execution 所需的最小字段：

- Goal
- Scope
- Non-goals
- Target Files
- Acceptance Criteria
- Test Requirements

因此，Reviewer 不要求回退 Drafter 重写任务包。

### Residual risks

以下是实现前仍需注意但尚未构成阻塞的风险：

1. `src/valuation_parser/` 目录授权较宽，Implementer 必须坚持“只改 taxonomy 集成直接相关模块”的最小改动原则。
2. workbook 相关基线若当前自动化覆盖不完整，执行报告中需要明确说明自动化验证范围和人工核对边界。
3. `review_category` 在 subjects / review_items 中的存在是允许的，但不得演变为 taxonomy 配置反向驱动 review 规则主体。

## Reviewer Decision

Reviewer decision: `Pass`

允许进入 Implementer 阶段，前提如下：

1. 严格遵守 task package 中已列明的 Non-goals。
2. 不以 taxonomy 集成为名义修改 adapter、routing 或核心持仓识别。
3. 不处理 `PRODUCT_022`。
4. 不删除或重定义旧 `asset_type`。
5. 实施完成后必须用测试、baseline refresh 报告和 execution report 证明验收，而不是只凭代码 diff。

## Handoff To Implementer

Implementer 应基于已审 task package 做 bounded execution。

本 Reviewer 文件只确认“可以开始做”，不增加任何超出 task package 的新授权。