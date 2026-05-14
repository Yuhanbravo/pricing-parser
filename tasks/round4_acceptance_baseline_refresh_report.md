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

## Outcome

本轮 baseline refresh 判定为：`accepted and synchronized`