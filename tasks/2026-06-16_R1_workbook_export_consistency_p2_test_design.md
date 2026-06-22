# R1-P2 Workbook Export Consistency Regression Test Design

## Purpose

本文档基于 R1-P1 审计报告（`tasks/2026-06-16_R1_workbook_export_consistency_audit.md`）中的发现，设计 R1-P2 阶段的 workbook ↔ CSV 一致性回归测试。本文档仅做测试设计，不实现测试代码。所有测试实现应在 owner 确认 Decision Note 后进行。

## Preconditions

- Owner decision on workbook acceptance role：**confirmed** — 选项 B：Workbook 是 CSV 的 Excel 镜像 / 人工友好派生物，不作为独立权威产物
- Owner decision on baseline strategy：**confirmed** — 维持当前 sheet-content / structured read comparison 口径，不升级为二进制验收
- Owner decision on CSV vs workbook authority：**confirmed** — CSV 为语义权威；不一致视为 bug，修复优先回到 CSV、字段常量和 `to_row()` 数据源
- Owner decision on filename stability：**confirmed** — 保持当前日期派生文件名规则，R1-P2 纳入 regression test
- Owner decision on P2 direction：**confirmed** — 授权 R1-P2，仅新增 focused tests，不改 runtime、不刷新 baseline、不处理 R2/R3/R4
- No runtime behavior change expected：本轮仅新增测试，parser runtime 保持不变
- R1-P1 audit 已完成，审计报告和 decision note 已提交

## Proposed tests


### Test 1: Workbook sheet names match expected set

- **目标**：验证生成的 workbook 包含且仅包含 4 个预期 sheet
- **预期行为**：`workbook.sheetnames == ["routing_results", "valuation_subjects", "valuation_positions", "review_items"]`
- **输入**：取现有最小的成功样本（如 `证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx`），运行 `run_pipeline()` 生成 workbook
- **断言**：
  1. Workbook 的 sheet 名称集合为精确的 `{"routing_results", "valuation_subjects", "valuation_positions", "review_items"}`
  2. Sheet 顺序与预期一致
  3. 不存在额外的 sheet（如 openpyxl 默认的 "Sheet"）
- **风险**：低。当前 sheet 名称在 `write_excel_workbook()` 中硬编码，变更概率低。但如果将来新增 sheet 而未更新测试，测试会失败——这正是测试的目的。
- **建议实现位置**：`tests/test_workbook_consistency.py`（新建）新增 `test_write_excel_workbook_creates_expected_sheets`

### Test 2: Workbook headers match field constants

- **目标**：验证 workbook 各 sheet 的表头行与 `exporters.py` 中对应的 `*_FIELDS` 常量完全一致
- **预期行为**：
  - `routing_results` sheet 表头 = `ROUTING_FIELDS`
  - `valuation_subjects` sheet 表头 = `SUBJECT_FIELDS`
  - `valuation_positions` sheet 表头 = `POSITION_FIELDS`
  - `review_items` sheet 表头 = `REVIEW_FIELDS`
- **输入**：构造最小 in-memory 数据（每条 1 行），调用 `write_excel_workbook()` 生成 workbook
- **断言**：
  1. 每个 sheet 的第一行（表头）与对应 `*_FIELDS` 常量逐元素相等
  2. 表头列数与常量字段数一致
  3. 表头列顺序与常量完全一致
- **风险**：低。当前 `*_FIELDS` 常量同时被 CSV 和 workbook 使用，但 CSV 表头已有 smoke test 保护，workbook 表头没有独立测试。如果有人在 `_write_sheet` 中意外引入了列顺序变更，此测试可捕获。
- **建议实现位置**：`tests/test_workbook_consistency.py`（新建）新增 `test_write_excel_workbook_headers_match_field_constants`

### Test 3: Workbook row counts match CSV outputs

- **目标**：验证 workbook 各 sheet 的数据行数与对应 CSV 文件的数据行数一致
- **预期行为**：对任意输入，workbook 每个 sheet 的数据行数（不含表头）等于对应 CSV 文件的数据行数（不含表头）
- **输入**：使用与 `test_acceptance_baseline.py` 相同的全量 raw 集运行 `run_pipeline()`
- **断言**：
  1. `len(workbook["routing_results"]) - 1 == CSV routing_results 行数 - 1`
  2. `len(workbook["valuation_subjects"]) - 1 == CSV valuation_subjects 行数 - 1`
  3. `len(workbook["valuation_positions"]) - 1 == CSV valuation_positions 行数 - 1`
  4. `len(workbook["review_items"]) - 1 == CSV review_items 行数 - 1`
- **风险**：低。因数据同源（同一批 `routes`/`subjects`/`positions`/`review_items` 列表），行数理应天然一致。此测试主要防止未来的序列化错误（如 openpyxl 写入时意外跳过行）。
- **建议实现位置**：`tests/test_workbook_consistency.py`（新建）新增 `test_workbook_row_counts_match_csv`

### Test 4: Selected stable values match CSV outputs

- **目标**：抽样验证 workbook 中特定单元格的值与对应 CSV 文件中同位置的值一致
- **预期行为**：对同一行同一列，workbook 单元格值与 CSV 单元格值语义等价
- **输入**：使用全量 raw 集运行 `run_pipeline()`
- **抽样策略（deterministic sampling）**：
  1. **First / middle / last row**：每个 sheet 取首行（第 1 数据行）、中间行（`n_rows // 2`）、末行（最后 1 数据行），逐列比对 workbook 单元格与 CSV 单元格
  2. **已知空值行**：选取 `to_row()` 中已知会产生 `None` 值的行（如 review_items 中某些可选字段），验证跨格式空值等价（workbook `None` ↔ CSV `""`）
  3. **已知数值行**：选取包含典型数值字段的行（如 `valuation_positions` 中的持仓数量/金额列），验证数值跨格式一致性（处理 int/float 呈现差异）
  4. **Review edge case 行**：选取 review_items 中包含特殊标记或边界值的行（如 `status` 字段），验证字符串值跨格式精确匹配
- **断言**：
  1. 对每个抽样行，逐列比对 workbook 单元格与 CSV 单元格
  2. 字符串值：精确匹配
  3. 数值：转为 `float` 后比对（容差 `1e-9`）——处理 int/float 呈现差异
  4. 空值：`None`（workbook）与 `""`（CSV）视为等价
- **风险**：中。需要处理空值等价（`None` ↔ `""`）和数值类型差异（`int` vs `float`）。建议实现为专用比对函数 `_cell_values_equal(workbook_val, csv_val)`。
- **建议实现位置**：`tests/test_workbook_consistency.py`（新建）

### Test 5: Date-derived filename stability

- **目标**：验证 workbook 文件名对相同输入具有确定性
- **验证策略**：优先通过 public pipeline / generated output path 间接验证——即使用现有 raw 样本运行 `run_pipeline()`，断言 `outputs["output_workbook"].name` 对固定输入集返回固定文件名。此路径已在 `test_smoke.py` 中有类似断言（硬编码 `"估值表解析_output_2025-03-27.xlsx"`），P2 应将其升级为结构化文件名断言（验证文件名匹配 `估值表解析_output_<date>.xlsx` 模式且日期与输入一致）。
- **回退策略**：仅当通过 public pipeline 间接验证成本过高（如需要构造多组不同日期的 raw 样本文件才能覆盖多日期/无日期 edge case）时，才考虑直接测试私有函数 `_build_output_workbook_filename()`。此时需在测试文件中明确注释说明这是**有意的测试取舍**——优先保护行为契约而非封装边界，并注明 Python 惯例允许测试私有函数以保护关键契约。
- **预期行为**：
  1. 给定固定输入文件名列表，多次调用/运行返回相同文件名
  2. YYYY-MM-DD 格式正确提取（如 `"证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx"` → `"估值表解析_output_2025-03-27.xlsx"`）
  3. YYYYMMDD 格式正确提取（如 `"20250327_PRODUCT_002_证券投资基金估值表.xls"` → `"估值表解析_output_2025-03-27.xlsx"`）
  4. 多日期输入取最早日期
  5. 无日期输入回退至 `"估值表解析_output.xlsx"`
- **断言**（public pipeline 路径 — 优先）：
  1. 使用现有 raw 样本运行 pipeline：`outputs["output_workbook"].name` 模式匹配 `re.compile(r"估值表解析_output_\d{4}-\d{2}-\d{2}\.xlsx")`
  2. 文件名中的日期与输入样本中的日期一致（取最早日期）
- **断言**（直接测试路径 — 仅当 public path 成本过高时启用）：
  1. 单日期文件：`_build_output_workbook_filename(...)` 返回包含正确日期的文件名
  2. 多日期文件（如 `2025-03-25` + `2025-03-27`）：取 `2025-03-25`
  3. 混合格式（`YYYY-MM-DD` + `YYYYMMDD`）：取最早
  4. 无日期文件（如 `data.xlsx`）：回退至默认文件名
  5. 空输入列表：回退至默认文件名
- **风险**：低。文件名生成逻辑是确定性的纯函数，仅在管线测试中间接验证。P2 应优先加固 public pipeline 路径的断言。
- **建议实现位置**：`tests/test_workbook_consistency.py`（新建）

## Recommended implementation priority

以下为实习生对 5 个测试的推荐实现优先级，基于触发风险与实际保护价值的综合判断：

| 优先级 | 测试 | 推荐理由 |
|--------|------|----------|
| **P0（优先）** | Test 3: Row counts match CSV | 直接保护 workbook ↔ CSV 数据行数一致性，防止序列化路径意外丢行；实现简单 |
| **P0（优先）** | Test 4: Selected stable values match CSV | 唯一直接验证单元格级跨格式一致性的测试，覆盖空值等价和数值类型差异风险 |
| **P0（优先）** | Test 5: Date-derived filename stability | 保护文件名确定性契约，降低新增样本后 baseline 文件名不匹配的维护摩擦 |
| **P2（可选）** | Test 1: Sheet names match expected set | 触发风险极低：sheet 名称硬编码且自初始实现以来从未变更 |
| **P2（可选）** | Test 2: Headers match field constants | 触发风险极低：CSV 表头已有 smoke test 锁定，`*_FIELDS` 常量共享使用，workbook 表头漂移概率近乎为零 |

> **注意**：以上优先级为实习生建议，最终实现范围由 owner 确认 Decision Note 后决定。

## Tests explicitly not proposed

以下测试类型明确不提议在 P2 中实现：

- **`.xlsx` 字节级比对**：二进制 diff 不可读，openpyxl 版本敏感性高，无实际审阅价值
- **Workbook 样式/格式断言**（如字体、颜色、列宽、数字格式）：不属于数据契约，openpyxl 默认样式可能随版本变化
- **Baseline 刷新**：不修改 `data_samples/expected/` 下的任何文件
- **Runtime 行为变更**：不修改 `src/` 下的任何文件
- **新 adapter / 新路由 / 新 taxonomy**：属于 R2/R3/R4 范围
- **跨 Python 版本 workbook 一致性**：超出当前 scope

## Suggested files for P2

### Priority（P0 — 优先实现）

| 文件 | 变更类型 | 内容 |
|---|---|---|
| `tests/test_workbook_consistency.py` | **新建测试文件** | 集中容纳所有 workbook ↔ CSV 一致性回归测试 |
| `tests/test_workbook_consistency.py` | 新增测试函数 | `test_workbook_row_counts_match_csv`、`test_workbook_cell_values_match_csv`、`test_workbook_filename_stability` |
| `tests/test_workbook_consistency.py` | 新增辅助函数 | `_cell_values_equal(workbook_val, csv_val)` — 空值等价与数值容差比对 |

### Optional（P2 — 可选）

| 文件 | 变更类型 | 内容 |
|---|---|---|
| `tests/test_workbook_consistency.py` | 新增测试函数（可选） | `test_workbook_sheet_names_match_expected_set`、`test_workbook_headers_match_field_constants` |

**重要**：Workbook consistency regression 不应放入 `test_smoke.py`。Smoke test 的职责是快速验证管线基本可用性（输出存在、表头契约、基本结构），而 workbook ↔ CSV 一致性测试是 focused regression，应独立为 `tests/test_workbook_consistency.py`。这保持了两个测试文件的职责边界清晰。

P2 不新增测试数据文件，所有测试使用现有 `data_samples/raw/` 样本或构造最小 in-memory fixture。

## Validation commands for P2

P2 实现后的建议验证命令：

```bash
# 运行全部测试
python -m pytest

# 聚焦 workbook consistency 回归测试
python -m pytest tests/test_workbook_consistency.py -v

# 确保 acceptance baseline 仍然通过
python -m pytest tests/test_acceptance_baseline.py -v

# 确保 smoke test 不受影响
python -m pytest tests/test_smoke.py -v
```

## Open questions

1. **`_build_output_workbook_filename()` 测试路径选择**：Test 5 已修订为优先通过 public pipeline 间接验证。如果实施时发现 public path 覆盖多日期/无日期 edge case 成本过高，则回退到直接测试私有函数，此时需在测试文件中明确注释说明取舍理由。此决策留给 P2 实施阶段按实际成本判断。
2. **Test 4 的抽样策略**：已修订为 deterministic sampling（first / middle / last row + 已知空值行 + 已知数值行 + review edge case 行）。如果实施时发现抽样范围不足，owner 可决定追加更多行。
3. **P2 是否需要新增 pytest fixture？**如果多个测试需要相同的 workbook 实例，建议提取为 `@pytest.fixture` 避免重复生成。
4. **空值等价函数的放置位置**：建议放在 `tests/test_workbook_consistency.py` 模块级别，供同一文件内的多个测试复用。
