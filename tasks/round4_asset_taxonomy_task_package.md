# Round 4 Asset Taxonomy Task Package

## Goal

为估值表解析器新增一层轻量、可配置、可测试的资产术语层，使当前 Round 4 受控样本下的资产术语在以下输出之间保持一致：

- `valuation_subjects.csv`
- `valuation_positions.csv`
- `review_items.csv`
- `parse_summary.md`
- Excel workbook summary 相关输出
- `data_samples/expected/` acceptance baseline

本轮目标是术语收敛，不是重写解析器，也不是扩展新的产品覆盖面。

## Scope

本轮范围限定为以下内容：

1. 在项目内引入配置化资产术语映射文件：`config/asset_taxonomy.yaml`。
2. 保留现有 `asset_type` 字段，同时新增稳定 taxonomy 字段：
   - `asset_type_internal`
   - `asset_type_display`
   - `asset_class_l1`
   - `asset_class_l2`
3. 将新增 taxonomy 字段纳入以下输出：
   - `valuation_subjects.csv`
   - `valuation_positions.csv`
   - `review_items.csv`
4. 在 `valuation_subjects.csv` 和 `review_items.csv` 中明确保留或补充 `review_category`，并保持其与 taxonomy 字段分离。
5. 调整 `parse_summary.md` 的资产类型统计展示，统一使用 `asset_type_display` 作为展示口径。
6. 如当前 workbook 已包含 summary 相关输出，可在不改变复杂样式的前提下补入与 taxonomy 相关的最小必要字段。
7. 刷新 `data_samples/expected/` 中受影响的 acceptance baseline，并确保刷新前先完成重跑和 diff 判定。
8. 更新与本轮契约直接相关的项目文档，使 Round 4 的输出字段、业务口径与边界说明保持一致。
9. 在项目内新增 `acceptance-baseline-refresh` 实验 skill 文档资产，但仅限 `pricing_parser` 仓库内试作和留痕。

## Non-goals

以下事项明确不在本轮范围内：

- 不新增 adapter。
- 不处理 `PRODUCT_022`。
- 不新增新产品样本。
- 不改变 routing 逻辑。
- 不改变核心持仓识别规则。
- 不改金额、成本、市值、盈亏计算。
- 不改变当前 strict-default 行为。
- 不做生产数据库字段设计。
- 不做复杂行业分类、策略分类、交易所全量映射。
- 不把 review 逻辑和 asset taxonomy 混在一起。
- 不把项目内实验 skill 提交到 `ai-skill-hub`。
- 不把本轮扩展为新增 API、数据中心接入或其它新主题。

## Target Files

本轮允许触达的目标文件或目录如下：

### Configuration

- `config/asset_taxonomy.yaml`

### Source code

- `src/valuation_parser/` 下与 taxonomy 加载、字段透传、summary 输出、review/export 流程直接相关的模块
- `src/valuation_parser/exporters.py`
- `src/valuation_parser/pipeline.py`
- `src/valuation_parser/models.py`
- 其它仅在确有必要时与 taxonomy 集成直接相关的源文件

### Tests

- `tests/test_asset_taxonomy.py`
- `tests/test_exporters.py`
- `tests/test_review_items.py`
- `tests/test_smoke.py`
- 如已有更合适的同类测试文件，可在原文件中扩展而不是机械新增

### Expected baseline and outputs

- `data_samples/expected/valuation_subjects.csv`
- `data_samples/expected/valuation_positions.csv`
- `data_samples/expected/review_items.csv`
- `data_samples/expected/parse_summary.md`
- workbook baseline 或对应结构说明文件（如仓库当前已有）

### Documentation

- `README.md`
- `docs/HANDOFF.md`
- `docs/status.md`

### Workflow artifacts

- `tasks/round4_asset_taxonomy_pre_implementation_review.md`
- `tasks/round4_asset_taxonomy_execution_report.md`
- `tasks/round4_asset_taxonomy_final_review.md`
- `tasks/round4_acceptance_baseline_refresh_report.md`

### Project-local experiment

- `skill_experiments/acceptance-baseline-refresh/`

## Acceptance Criteria

本轮完成时，应同时满足以下验收条件：

1. 项目中存在 `config/asset_taxonomy.yaml`，且其职责仅限术语映射与展示口径，不承载 routing 或完整解析规则。
2. 现有 `asset_type` 字段被保留，未被删除或静默改写语义。
3. `valuation_positions.csv` 中新增 `asset_type_internal`、`asset_type_display`、`asset_class_l1`、`asset_class_l2` 字段，且正常证券持仓记录应尽量具备这些字段值。
4. `valuation_subjects.csv` 中新增 `asset_type_internal`、`asset_type_display`、`asset_class_l1`、`asset_class_l2`、`review_category` 字段，主要资产、负债与复核项应具备明确分类。
5. `review_items.csv` 中新增或保留 `asset_type_internal`、`asset_type_display`、`asset_class_l1`、`asset_class_l2`、`review_category`、`review_note`，并保持 review 分类与资产分类分离。
6. `parse_summary.md` 使用统一的 `asset_type_display` 展示资产分类统计，而不是混用旧口径。
7. ETF / 场内基金按基金类口径输出为 `fund_exchange_traded` / `场内基金/ETF`，不得在本轮按权益类口径落地。
8. 收益互换按 `derivative_swap` / `收益互换` 进入 review 口径，但不进入 `valuation_positions.csv`。
9. 现金、保证金、清算款保留在 subjects 或 summary 口径中，但不作为证券持仓进入 `valuation_positions.csv`。
10. 未识别或无法归类项存在 `unknown` fallback，并与 review 机制配合，而不是通过 taxonomy 掩盖问题。
11. `data_samples/expected/` 中受影响的 baseline 已同步刷新，且刷新建立在重跑与 diff 判定基础之上，而非直接覆盖。
12. `README.md`、`docs/HANDOFF.md`、`docs/status.md` 已同步更新本轮资产术语口径、边界说明与 baseline 状态。
13. 项目内实验 skill 目录已补齐到 `skill_experiments/acceptance-baseline-refresh/`，但未进入 `ai-skill-hub`。
14. 本轮实际改动未扩展到 adapter、新样本接入、`PRODUCT_022` 处理、routing 逻辑修改或核心算法变更。

## Test Requirements

本轮至少应补充或更新以下测试覆盖：

1. taxonomy 配置加载测试：验证 `config/asset_taxonomy.yaml` 可被正确读取并映射到程序使用的结构。
2. 已知 asset type 映射测试：覆盖当前受控样本中已出现的主要类型，例如 A 股、港股、科创板、存托凭证、场内基金/ETF、收益互换、现金及存款、保证金、清算款、应付款项、应交税费。
3. unknown fallback 测试：验证未识别类型不会导致 taxonomy 缺失，并能与 review 逻辑协同输出。
4. exporter 字段测试：验证 `valuation_positions.csv`、`valuation_subjects.csv`、`review_items.csv` 均包含本轮新增字段，且字段值符合口径约束。
5. summary 展示测试：验证 `parse_summary.md` 的资产类型统计统一使用 `asset_type_display`。
6. review 分离测试：验证 `review_category`、`review_flag`、`review_note` 与 taxonomy 字段职责分离，尤其是收益互换和 unknown 场景。
7. smoke / acceptance 测试：基于当前受控样本重跑后，输出与 `data_samples/expected/` 刷新后的基线一致。
8. 若 workbook baseline 当前受自动化覆盖，则应补充与 taxonomy 字段相关的最小必要断言；若未受自动化覆盖，应至少在本轮说明结构变化和人工核对范围。

## Boundary Notes

- 本任务包仅用于 Drafter 阶段收敛实施边界。
- 本任务包不包含实现步骤、代码方案、改动细节或执行结论。
- 进入实现前，必须先产出并通过 `round4_asset_taxonomy_pre_implementation_review.md` 的 Reviewer 审查。
