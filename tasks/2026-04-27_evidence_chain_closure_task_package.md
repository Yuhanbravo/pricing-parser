# Task Package: Evidence Chain Closure

## Task Identification

- Name: Round 3 / Evidence Chain Closure
- Phase: Phase 3 review closure
- Submitted By: Copilot planner
- Date: 2026-04-27
- Upstream Need Review: [tasks/2026-04-27_evidence_chain_closure_need_review.md](d:\DUKE\hxhy\pricing_parser\tasks\2026-04-27_evidence_chain_closure_need_review.md)

## 1. Background

第一轮已经完成估值表解析器的可运行骨架，建立了 `cli / pipeline / routing / mapping_loader / product_identity / normalizers / exporters / adapters` 等模块，并能在脱敏样本上端到端跑通。但第一轮的主要问题不是“不能运行”，而是“外部契约没有收口”，包括 trace 字段未真实导出、mapping 校验不严格、generic fallback 误记成功，以及 docs / expected / outputs 口径分叉。

第二轮围绕这些核心契约问题做了集中修复，已基本打掉最关键的 P0：subjects / positions 的 trace 字段已真实导出，`mapping_loader` 已在加载期拒绝未知 `adapter_key`，strict-default 路径下未命中 mapping 的样本不再被静默记为成功路由，`review_flag / review_items / parse_summary` 的职责也开始收紧。第二轮复审结论不是“可以直接并主线”，而是“基本通过但仍需修正，建议再修一轮”。

第三轮因此不再扩展解析能力，也不重构架构，而是专门收口 docs / expected / outputs / tests / summary / tag 这条证据链，使当前节点成为一个可验收、可复审、可接手、可做 merge 决策的稳定候选点。

## 2. Goal

本轮目标是统一 docs / expected / outputs / tests / summary / tag 的证据链，使仓库中的文档、基线、测试和当前输出能够共同证明同一套 strict-default 外部契约。

本轮完成后，应满足以下高层结果：

- `README / HANDOFF / status` 对当前状态的描述一致。
- `data_samples/expected/` 对当前严格路由路径形成可审阅的 acceptance baseline。
- `.xlsx` mapping 回归不再只靠手工 smoke，而有仓库内自动化测试支撑。
- `parse_summary.md` 对路由失败、fallback 条件和 review 入口的说明足够清晰。
- 历史产物不会再与当前契约并列误导接手人。
- tag 决策条件与建议名称被显式记录。

## 3. Scope

本轮只允许在“证据链收口”边界内执行，不扩功能、不改算法。

### Allowed Changes

- 更新状态类文档中的统计数字、当前阶段描述和边界说明。
- 补齐或整理 `data_samples/expected/` 下的当前 acceptance baseline。
- 为 `.xlsx` mapping 增加自动化测试。
- 调整 `parse_summary.md` 相关导出或测试，使 summary 能说明：
  - routing success
  - routing failure
  - fallback 的启用条件
  - review 入口
  - flagged subjects / positions / review items 的关系
- 对历史输出、过期治理报告或旧 baseline 增加历史标注或清理策略说明。
- 在 handoff / status / execution report 中补充 tag 建议。

### Bounded Execution Focus

- 优先修正文档数字漂移，尤其当前 `238 review items` 与主文档仍写 `242` 的显性不一致。
- 优先补齐 strict-default 路径的 acceptance evidence，而不是重新定义功能目标。
- 若 summary 口径确实需要代码配合，只允许改动最接近控制 summary 输出的局部实现，不得扩展到新的功能切片。

## 4. Explicit Non-goals

本轮明确不做以下事项：

- 不新增托管机构 adapter。
- 不新增资产类型解析。
- 不修改核心解析算法、主路由策略或脱敏逻辑。
- 不引入 Wind、Oracle、生产系统或真实敏感数据。
- 不做大规模重构。
- 不引入新的复杂依赖。
- 不把 bundle 文件作为本轮常规源码资产提交。
- 不把 unrelated cleanup 混入本轮交付。
- 不把第三轮包装成“功能升级轮”或“生产接入轮”。

## 5. Target Files

### Primary Docs

- [README.md](d:\DUKE\hxhy\pricing_parser\README.md)
- [docs/HANDOFF.md](d:\DUKE\hxhy\pricing_parser\docs\HANDOFF.md)
- [docs/status.md](d:\DUKE\hxhy\pricing_parser\docs\status.md)

### Expected Baseline And Historical Evidence

- [data_samples/expected/parse_summary.md](d:\DUKE\hxhy\pricing_parser\data_samples\expected\parse_summary.md)
- `data_samples/expected/` 下与以下交付物对应的 baseline 文件：
  - `routing_results.csv`
  - `valuation_subjects.csv`
  - `valuation_positions.csv`
  - `parse_summary.md`
  - workbook 结构说明
- 与历史产物标注有关的文档或说明文件

### Tests

- `tests/` 下与以下契约相关的测试文件：
  - smoke / exporter / summary 契约
  - mapping loader
  - `.xlsx` mapping 自动化回归

### Only If Summary Wording Requires Code Changes

- `src/valuation_parser/exporters.py`
- `src/valuation_parser/pipeline.py`

### Process Files

- [tasks/2026-04-27_evidence_chain_closure_need_review.md](d:\DUKE\hxhy\pricing_parser\tasks\2026-04-27_evidence_chain_closure_need_review.md)
- [tasks/2026-04-27_evidence_chain_closure_task_package.md](d:\DUKE\hxhy\pricing_parser\tasks\2026-04-27_evidence_chain_closure_task_package.md)
- `tasks/2026-04-27_evidence_chain_closure_execution_report.md`
- `tasks/2026-04-27_evidence_chain_closure_ai_review_report.md`

## 6. Acceptance Criteria

本轮至少需要满足以下可验证标准：

1. [README.md](d:\DUKE\hxhy\pricing_parser\README.md)、[docs/HANDOFF.md](d:\DUKE\hxhy\pricing_parser\docs\HANDOFF.md)、[docs/status.md](d:\DUKE\hxhy\pricing_parser\docs\status.md) 中的统计数字与当前 strict-default 实跑结果一致。
2. `data_samples/expected/` 对当前关键交付物形成 acceptance baseline，至少覆盖：
   - `routing_results.csv`
   - `valuation_subjects.csv`
   - `valuation_positions.csv`
   - `parse_summary.md`
   - workbook 结构说明
3. `.xlsx` mapping 已有仓库内自动化测试，不再只依赖手工 smoke。
4. `parse_summary.md` 或其对应契约测试能够明确说明：
   - 未路由样本
   - routing failure
   - generic fallback 仅在显式启用时生效
   - review 入口
   - flagged subjects / positions / review items 的关系
5. 历史产物不再与当前契约并列混淆；若保留历史材料，必须有明确历史标注。
6. tag 策略已有明确书面建议，包括建议名称和建议在何种条件下打 tag。
7. 测试通过；若环境问题导致部分测试无法完成，阻塞原因与受影响范围必须被写入 execution report。
8. 本轮 diff 仅覆盖授权范围，不混入新 adapter、新算法或无关清理。

### Completion Threshold

- 若以上标准全部满足，可判定为“可进入并主线前复审”。
- 若只剩 1 到 2 个轻微证据漂移，则判定为“仍需小修”。
- 若 docs / expected / outputs / tests 仍不能互相印证，或本轮扩展了无关功能，则判定为未按任务包执行。

## 7. Execution Report Requirements

执行完成后必须生成：`tasks/2026-04-27_evidence_chain_closure_execution_report.md`。

execution report 至少需要包含以下章节：

1. `Scope Restatement`
   - 复述本轮只做证据链收口。
2. `Files Changed`
   - 逐个列出改动文件及其作用。
3. `Changes Made`
   - 按本 task package 的验收项逐条说明完成情况。
4. `Validation`
   - 列出实际运行命令、结果、失败原因和环境阻塞。
5. `Boundaries Kept`
   - 说明本轮明确没做哪些事情。
6. `Remaining Issues`
   - 记录尚未解决的问题、风险和待确认项。
7. `Tag Recommendation`
   - 说明是否建议打 tag，以及建议 tag 名称。
8. `Commit Summary`
   - 列出本轮 commit hash 和 commit message；若尚未提交，也要明确写明未提交状态。

execution report 还必须满足以下要求：

- 明确记录测试是否全部通过。
- 若存在环境阻塞，必须区分“环境导致未验证”与“代码断言失败”。
- 明确说明本轮是否仍存在阻碍进入并主线前复审的问题。

## Constraints

- 执行侧必须先复述本轮目标、边界、明确不做事项和预计修改文件，再开始施工。
- 执行侧必须保持 bounded execution，不得把额外发现的问题混入本轮交付。
- 当发现范围外问题时，只允许在 execution report 中记录为风险或待确认项。
- 如需更新 handoff 文档，应继续遵守 [docs/HANDOFF.md](d:\DUKE\hxhy\pricing_parser\docs\HANDOFF.md) 作为 handoff 单一主文档的原则。

## Supporting Context

- Project brief: [估值表解析器项目任务书.md](d:\DUKE\hxhy\pricing_parser\估值表解析器项目任务书.md)
- Round 1 review summary: [任务书集合/pricing_parser第一轮审查结论摘要.md](d:\DUKE\hxhy\pricing_parser\任务书集合\pricing_parser第一轮审查结论摘要.md)
- Round 2 review summary: [任务书集合/pricing_parser第二轮审查结论摘要.md](d:\DUKE\hxhy\pricing_parser\任务书集合\pricing_parser第二轮审查结论摘要.md)
- Handoff pilot instructions: [任务书集合/估值表解析器第三轮证据链收口_Handoff流程试跑说明.md](d:\DUKE\hxhy\pricing_parser\任务书集合\估值表解析器第三轮证据链收口_Handoff流程试跑说明.md)

## Expected Output

- A bounded implementation aligned to this task package.
- A structured execution report.
- A code and docs diff limited to evidence-chain closure scope.