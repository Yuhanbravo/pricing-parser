---
name: acceptance-baseline-refresh
description: "Project-local experimental workflow for rerun, diff judgment, baseline refresh, and contract-sync after controlled parser changes."
status: experimental
scope: pricing_parser only
---

# Acceptance Baseline Refresh

## When To Use

在以下场景使用：

- 解析输出字段发生了受控变化
- `parse_summary.md` 的统计口径发生了明确调整
- `data_samples/expected/` 需要和当前已验证契约重新对齐
- 你需要留下“为什么可以刷新 baseline”的判断依据

不要在以下场景使用：

- 未先完成范围内代码实现与最小验证
- 尚不确定差异是预期变化还是潜在回归
- 想用 baseline 覆盖来掩盖测试失败

## Inputs

- 当前 task package 或等价范围说明
- 受控重跑入口，例如 `data_samples/raw/`
- 当前 baseline 目录，例如 `data_samples/expected/`
- 临时输出目录，例如 `tmp/<run_name>/current/`
- 已通过的最小验证结果，例如 smoke 或 focused tests

## Outputs

- 差异分类结论
- 是否刷新 baseline 的明确决定
- 刷新后的 expected 文件集合
- baseline refresh 报告
- 与本轮契约相关的 README / HANDOFF / status 同步结果

## Execution Steps

1. 先确认边界。
   只在 task package 已授权、并且已有最小验证通过的前提下开始 baseline refresh。

2. 进行受控重跑。
   使用固定输入集、固定 mapping、固定输出目录生成新的 CSV / Markdown / workbook 产物。

3. 对比 baseline。
   对 `data_samples/expected/` 中受影响文件逐一比较，记录新增字段、统计值变化、展示口径变化与纯格式变化。

4. 做差异判定。
   把差异分成三类：
   - 预期契约更新
   - 潜在回归
   - 待确认但暂不刷新

5. 只刷新被判定为“预期契约更新”的文件。
   不允许因为有 diff 就整体覆盖 expected 目录。

6. 做刷新后验证。
   至少确认刷新后的 expected 文件与受控重跑结果一致，并补充必要 smoke / acceptance 验证。

7. 同步说明文档。
   把 baseline refresh 事实同步到项目状态文档和 execution report，而不是只停留在命令输出里。

## Constraints

- 不替代 parser 实现或测试。
- 不改变 task package 的范围。
- 不把未确认差异直接写进 expected baseline。
- 不把实验 skill 输出伪装成正式 canonical governance。
- 不借 baseline refresh 处理 `PRODUCT_022`、adapter 扩张或 routing 改写等范围外事项。

## Acceptance Criteria

满足以下条件时，才可把一次 baseline refresh 判定为完成：

- 进入 refresh 前，至少有一组与本轮改动直接相关的 focused tests 或 smoke tests 已通过。
- 受控重跑入口、baseline 目录、临时输出目录在报告中写清楚。
- 差异已被明确分类为：`预期契约更新`、`潜在回归` 或 `待确认`。
- 只有被判定为 `预期契约更新` 的 expected 文件被刷新。
- 刷新后，至少完成一次“expected 与受控输出一致”的验证。
- baseline refresh 的结果已同步进任务报告或状态文档，而不只是停留在临时命令输出中。

## Boundaries With Other Workflows

### With `workflow-bootstrap`

- `workflow-bootstrap` 负责角色链和流程壳层，例如 Drafter / Reviewer / Implementer / Reporter / Final Reviewer。
- 本 skill 只负责其中“baseline refresh judgment”这一段受控流程。
- 本 skill 不定义角色职责，也不替代 task package 编写、预审查或最终复核。

### With `chatgpt-handoff-pilot`

- `chatgpt-handoff-pilot` 负责 task package、bounded execution 和 execution report 的协议化组织。
- 本 skill 只补充“当 expected baseline 需要刷新时，如何先判断、再刷新、再留痕”。
- 本 skill 不能绕过 task package 授权，也不能单独批准范围扩大。

## Recommended Report Structure

建议至少记录以下字段：

- rerun entry
- baseline location
- temp output location
- focused tests run first
- diff summary by artifact
- refresh approved / rejected decision per artifact
- post-refresh validation
- documentation sync status

## Round 4 Trial Notes

本轮实际试跑结论：

- `parse_summary.md` 中 `Review flagged subjects` 从 `238` 增至 `525` 是预期契约更新。
- `Review items exported` 保持 `238`，说明 subject-level review 覆盖扩大，但 review item 导出边界未被放宽。
- `Supported asset types` 从旧 internal keys 改为 taxonomy display names，是预期展示口径更新。
- `valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv` 新增 taxonomy 字段，是预期 schema 更新。
- 在后续 swap-margin taxonomy 修复的 follow-up 复核中，文本 expected baseline 已与当前 rerun 输出保持一致，因此结论是“无需再次刷新，只需补充证据链说明”。