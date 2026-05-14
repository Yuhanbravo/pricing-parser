# Development Notes

## Source

本实验 skill 来源于 Round 4 任务书中提出的 `acceptance-baseline-refresh` 草案，目标是把 baseline refresh 从“顺手覆盖 expected”提升为“有判断记录的受控刷新”。

## Why It Was Useful In Round 4

- Round 4 的契约变化不仅是字段追加，还包含 summary 统计口径变化。
- 如果没有单独的 diff judgment 步骤，`525` 与 `238` 这组看起来不一致的数字很容易被误判为 bug。
- 通过先重跑、再读 summary、再判定差异，能够证明这是 subject-level review 覆盖扩大，而不是 review item 误增。

## What Worked

- 先把受控重跑输出落到 `tmp/round4_baseline_refresh/current/`，便于与 `data_samples/expected/` 做定点比较。
- 先看 `parse_summary.md` 再决定是否刷新 CSV baseline，能快速识别这轮变化是否符合任务书边界。
- 刷新后做“expected 文件与受控输出一致性验证”，比只看 diff 更稳妥。

## What Is Still Immature

- 还没有统一的 diff 分类模板，当前主要靠报告文档描述。
- workbook 目前没有单独 acceptance baseline，因此 workbook 验证仍偏结构化说明。
- 还没有独立的自动化命令把“重跑 + diff 摘要 + 刷新建议”一次性串起来。

## If It Moves To ai-skill-hub Later

至少还需要补充：

- 更稳定的适用条件与反例
- 与 `chatgpt-handoff-pilot` 的 task package / execution report 衔接字段
- 更明确的风险分类模板
- 一个跨项目、非 parser 特定的 invocation 示例集