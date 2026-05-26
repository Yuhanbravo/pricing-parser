# Round 4 Acceptance Baseline Refresh Report

## Purpose

本报告记录 Round 4 资产术语收敛完成后的 baseline refresh 过程，说明本轮 expected baseline 为什么可以刷新、刷新了哪些文件、以及哪些边界没有被顺手扩大。

## Rerun Inputs

- Controlled input set: `data_samples/raw/`
- Baseline directory: `data_samples/expected/`
- Temporary rerun output: `tmp/round4_baseline_refresh/current/`
- Pipeline entry used for rerun: `src/valuation_parser/pipeline.py`

## Files Evaluated

- `valuation_subjects.csv`
- `valuation_positions.csv`
- `review_items.csv`
- `parse_summary.md`

## Diff Judgment

### 1. `valuation_subjects.csv`

结论：`refresh approved`

原因：subjects 导出新增 taxonomy 字段：

- `asset_type_internal`
- `asset_type_display`
- `asset_class_l1`
- `asset_class_l2`
- `review_category`

这属于 Round 4 task package 明确授权的 schema 更新，不是回归。

### 2. `valuation_positions.csv`

结论：`refresh approved`

原因：positions 导出新增 taxonomy 字段：

- `asset_type_internal`
- `asset_type_display`
- `asset_class_l1`
- `asset_class_l2`

同时，非证券持仓类 taxonomy 项目没有被错误扩张进 positions，符合 Round 4 边界。

### 3. `review_items.csv`

结论：`refresh approved`

原因：review items 导出新增 taxonomy 字段，并继续保留 `review_category` / `review_note` 作为 review 口径主字段，符合“taxonomy 与 review 分离”的任务要求。

### 4. `parse_summary.md`

结论：`refresh approved`

关键差异：

- `Review flagged subjects: 238` -> `525`
- `Review items exported: 238` -> `238`（保持不变）
- `Supported asset types: a_share, fund_or_etf, hk_equity` -> `Supported asset types: A股股票, 场内基金/ETF, 存托凭证, 港股, 科创板股票`
- 新增 `## Asset Type Coverage` 表格

判定理由：

- `Review flagged subjects` 增加是 subject-level taxonomy / review 覆盖面扩大的预期结果。
- `Review items exported` 保持不变，说明本轮没有把 review item 导出边界意外放宽。
- 资产类型展示从 internal keys 切换到 display names 是 Round 4 summary 统一展示口径的目标之一。

## Refresh Decision

本轮对以上四个 expected 文件全部执行刷新。

刷新后执行了一致性验证，确认 `data_samples/expected/` 中的四个文件与 `tmp/round4_baseline_refresh/current/` 中对应文件逐一一致。

## Boundaries Preserved

- 未处理 `PRODUCT_022`
- 未新增 adapter
- 未改 routing 逻辑
- 未把收益互换、现金及存款、保证金、清算款等项目错误导入 `valuation_positions.csv`
- 未把实验 skill 同步到 `ai-skill-hub`

## Documentation Sync

baseline refresh 完成后，同步更新了：

- `README.md`
- `docs/HANDOFF.md`
- `docs/status.md`

同步内容包括：

- Round 4 taxonomy 字段与展示口径
- `525` review-flagged subjects / `238` review items 的当前契约事实
- `PRODUCT_022` 仍不在本轮范围内
- 项目本地 experiment skill 的边界说明

> **Note**: 上述 `525` 为本轮初始 baseline refresh 时的计数。后续 swap-margin taxonomy 修复后重新验证，accepted baseline 已更新为 `508`。详见下方 Follow-up 节。

## Outcome

本轮 baseline refresh 判定为：`accepted and synchronized`

## Follow-up: Swap Margin Taxonomy Verification

在后续修复“`收益互换` + `保证金` 科目应归入 `margin_deposit`，而非 `derivative_swap`”之后，又按同一实验流程追加执行了一次 follow-up 验证。

### Follow-up Inputs

- Controlled input set: `data_samples/raw/`
- Baseline directory: `data_samples/expected/`
- Temporary rerun output: `tmp/round4_swap_margin_refresh/current/`
- Focused validations run first:
	- `tests/test_asset_taxonomy.py`
	- `tests/test_acceptance_baseline.py`

### Follow-up Validation Result

结论：`focused tests passed before rerun`

说明：在进入 follow-up rerun 之前，focused tests 已通过，确认当前 taxonomy 行为与 acceptance baseline 测试契约一致。

### Follow-up Diff Judgment

本次 follow-up 复跑后，以下文本基线文件与当前 rerun 输出逐一一致：

- `routing_results.csv`
- `valuation_subjects.csv`
- `valuation_positions.csv`
- `review_items.csv`
- `parse_summary.md`

结论：`no additional text baseline refresh required`

原因：此前针对 swap-margin taxonomy 修复而执行的 baseline refresh 已经把当前受控契约同步进 `data_samples/expected/`；本次 follow-up 只是复核同步状态，而不是产生新的契约变化。

### Workbook Note

本次 ad hoc workbook 逐行读取比较在脚本中遇到一次 `EOFError`，因此没有把该次脚本结果单独作为 follow-up 判定依据。

本次 follow-up 对 workbook 的接受性判断仍以已通过的 `tests/test_acceptance_baseline.py` 为准；该测试包含 workbook baseline 比较，因此足以支持“当前 expected baseline 已与现行 taxonomy 修复同步”的结论。

### Follow-up Outcome

本次 follow-up 判定为：`already synchronized; no further refresh performed`

这意味着：

- 本次没有新增 expected 文件刷新
- 本次没有新增 README / HANDOFF / status 同步动作
- 本次 follow-up 的主要价值是补充证据链，确认当前 baseline 仍与修复后的输出一致