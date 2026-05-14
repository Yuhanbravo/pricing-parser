# Round 4 Asset Taxonomy Execution Report

## Role

本文件对应 `workflow-bootstrap` 角色链中的 Reporter 阶段产物，用于回传 Round 4 资产术语收敛的实际执行情况。

## Scope Confirmation

本轮执行保持在 `tasks/round4_asset_taxonomy_task_package.md` 的授权范围内：

- 引入并集成 taxonomy 配置层
- 将 taxonomy 字段透传到 subjects / positions / review_items / summary
- 刷新 expected baseline
- 同步 README / HANDOFF / status
- 新增项目本地 experiment skill 文档资产

本轮未做：

- 未新增 adapter
- 未改变 routing 逻辑
- 未处理 `PRODUCT_022`
- 未引入新样本
- 未把 experiment skill 提交到 `ai-skill-hub`

## Modified Areas

### Configuration and taxonomy wiring

- `config/asset_taxonomy.yaml`
- `src/valuation_parser/taxonomy.py`
- `src/valuation_parser/models.py`
- `src/valuation_parser/exporters.py`
- `src/valuation_parser/pipeline.py`

作用：引入轻量 taxonomy 配置层，并把统一术语字段落到导出与 summary 路径中。

### Tests

- `tests/test_smoke.py`

作用：在 Round 4 summary / schema 契约变化后，同步调整 smoke 断言，避免旧 header 与旧 summary 字符串造成假失败。

### Expected baseline

- `data_samples/expected/valuation_subjects.csv`
- `data_samples/expected/valuation_positions.csv`
- `data_samples/expected/review_items.csv`
- `data_samples/expected/parse_summary.md`

作用：将受控重跑后的 Round 4 契约结果固化为 acceptance baseline。

### Documentation

- `README.md`
- `docs/HANDOFF.md`
- `docs/status.md`

作用：同步 Round 4 taxonomy 字段、summary 口径、review 统计、baseline refresh 与 scope boundary。

### Workflow / experiment artifacts

- `skill_experiments/acceptance-baseline-refresh/`
- `tasks/round4_acceptance_baseline_refresh_report.md`
- `tasks/round4_asset_taxonomy_execution_report.md`
- `tasks/round4_asset_taxonomy_final_review.md`

作用：补齐本轮 workflow-bootstrap 与项目本地 baseline refresh 试跑留痕。

## Acceptance Items Completed

已完成的验收项：

1. taxonomy 配置文件已存在，并仅承载术语映射与展示口径。
2. 旧 `asset_type` 字段保留。
3. subjects / positions / review_items 已补入 Round 4 taxonomy 字段。
4. `review_category` 与 `review_note` 继续保留在 review 口径中，没有被 taxonomy 吸收。
5. `parse_summary.md` 使用 display-name 口径展示资产类型，并新增 `Asset Type Coverage`。
6. ETF / 场内基金按基金类口径输出。
7. 收益互换进入 review 口径但不进入 positions。
8. 现金、保证金、清算款、负债类项目保留在 subjects / summary，不进入 positions。
9. expected baseline 已在 rerun + diff judgment 后刷新。
10. README / HANDOFF / status 已同步。
11. 项目本地 experiment skill 已补齐，但未进入 `ai-skill-hub`。

## Validation Run In This Closure Phase

### Smoke validation

- Reran `tests/test_smoke.py -vv`
- Result: `6 passed`

### Baseline consistency validation

- Compared refreshed expected files against `tmp/round4_baseline_refresh/current/`
- Result: `valuation_subjects.csv`, `valuation_positions.csv`, `review_items.csv`, and `parse_summary.md` all matched the controlled rerun outputs

### Documentation validation

- Verified that stale `242 review items` / old asset-type wording no longer remained in the updated docs
- Confirmed touched markdown files had no editor-reported errors

## Current Verified Output Facts

- Processed files: `11`
- Successful routes: `10`
- Routing failures: `1`
- Subject rows exported: `1022`
- Position rows exported: `182`
- Review flagged subjects: `525`
- Review items exported: `238`
- Normalization issues: `0`
- Supported display asset types: `A股股票`, `场内基金/ETF`, `存托凭证`, `港股`, `科创板股票`

## Residual Risks

1. Workbook export still lacks a separately maintained acceptance baseline.
2. Additional regression coverage is still desirable for review-item generation beyond the current fixture set.
3. `PRODUCT_022` remains intentionally unresolved in the strict-default path and should not be mistaken for an unreviewed defect in this round.

## Reporter Conclusion

Round 4 asset taxonomy closure is complete at the repository-contract level: code, smoke validation, expected baseline, docs, and workflow artifacts are now aligned.