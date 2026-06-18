# R1-P2 Workbook Export Consistency Regression Test Design

## Purpose

本文档基于 R1-P1 审计报告（`tasks/2026-06-16_R1_workbook_export_consistency_audit.md`）中的发现，设计 R1-P2 阶段的 workbook ↔ CSV 一致性回归测试。本文档仅做测试设计，不实现测试代码。所有测试实现应在 owner 确认 Decision Note 后进行。

## Preconditions

- Owner decision on workbook acceptance role：**pending**（推荐选项 B：Workbook 是 CSV 镜像）
- Owner decision on baseline strategy：**pending**（推荐维持当前 content-level sheet baseline）
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
- **建议实现位置**：`tests/test_exporters.py` 新增 `test_write_excel_workbook_creates_expected_sheets`

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
- **建议实现位置**：`tests/test_exporters.py` 新增 `test_write_excel_workbook_headers_match_field_constants`

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
- **建议实现位置**：`tests/test_exporters.py` 新增 `test_workbook_row_counts_match_csv`（或 `tests/test_smoke.py`）

### Test 4: Selected stable values match CSV outputs

- **目标**：抽样验证 workbook 中特定单元格的值与对应 CSV 文件中同位置的值一致
- **预期行为**：对同一行同一列，workbook 单元格值与 CSV 单元格值语义等价
- **输入**：使用全量 raw 集运行 `run_pipeline()`
- **断言**：
  1. 对每个 sheet，取首行、中间行、末行（共 3 行），逐列比对 workbook 单元格与 CSV 单元格
  2. 字符串值：精确匹配
  3. 数值：转为 `float` 后比对（容差 `1e-9`）——处理 int/float 呈现差异
  4. 空值：`None`（workbook）与 `""`（CSV）视为等价
- **风险**：中。需要处理空值等价（`None` ↔ `""`）和数值类型差异（`int` vs `float`）。建议实现为专用比对函数 `_cell_values_equal(workbook_val, csv_val)`。
- **建议实现位置**：`tests/test_exporters.py` 新增 `test_workbook_cell_values_match_csv`

### Test 5: Date-derived filename stability

- **目标**：验证 `_build_output_workbook_filename()` 对相同输入返回相同文件名
- **预期行为**：
  1. 给定固定输入文件名列表，多次调用返回相同文件名
  2. YYYY-MM-DD 格式正确提取（如 `"证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx"` → `"估值表解析_output_2025-03-27.xlsx"`）
  3. YYYYMMDD 格式正确提取（如 `"20250327_PRODUCT_002_证券投资基金估值表.xls"` → `"估值表解析_output_2025-03-27.xlsx"`）
  4. 多日期输入取最早日期
  5. 无日期输入回退至 `"估值表解析_output.xlsx"`
- **输入**：构造虚拟文件名列表（不实际创建文件），调用 `_build_output_workbook_filename()`
- **断言**：
  1. 单日期文件：文件名包含正确日期
  2. 多日期文件（如 `2025-03-25` + `2025-03-27`）：取 `2025-03-25`
  3. 混合格式（`YYYY-MM-DD` + `YYYYMMDD`）：取最早
  4. 无日期文件（如 `data.xlsx`）：回退至默认文件名
  5. 空输入列表：回退至默认文件名
- **风险**：低。`_build_output_workbook_filename()` 当前未被独立测试，仅在管线测试中间接验证。此测试应导入该函数直接测试。
- **注意**：`_build_output_workbook_filename()` 当前是 `pipeline.py` 的模块级私有函数（前缀 `_`）。P2 实现时需确认是否直接测试私有函数，或通过 `run_pipeline()` 间接验证文件名。建议直接测试——Python 惯例允许测试私有函数以保护关键契约。
- **建议实现位置**：`tests/test_smoke.py` 或新文件 `tests/test_workbook_filename.py`

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
| `tests/test_exporters.py` | 新增测试函数 | `test_workbook_row_counts_match_csv`、`test_workbook_cell_values_match_csv` |
| `tests/test_exporters.py` | 新增辅助函数 | `_cell_values_equal(workbook_val, csv_val)` — 空值等价与数值容差比对 |
| `tests/test_smoke.py` 或新文件 | 新增测试函数 | `test_workbook_filename_determinism`（测试 `_build_output_workbook_filename`） |

### Optional（P2 — 可选）

| 文件 | 变更类型 | 内容 |
|---|---|---|
| `tests/test_exporters.py` | 新增测试函数（可选） | `test_write_excel_workbook_creates_expected_sheets`、`test_write_excel_workbook_headers_match_field_constants` |

P2 不新增测试数据文件，所有测试使用现有 `data_samples/raw/` 样本或构造最小 in-memory fixture。

## Validation commands for P2

P2 实现后的建议验证命令：

```bash
# 运行全部测试
python -m pytest

# 聚焦 exporter 和 workbook 相关测试
python -m pytest tests/test_exporters.py tests/test_smoke.py -v

# 确保 acceptance baseline 仍然通过
python -m pytest tests/test_acceptance_baseline.py -v
```

## Open questions

1. **`_build_output_workbook_filename()` 是否应提升为公共函数？**当前为模块级私有函数（`_` 前缀）。如果 P2 需要直接测试，建议保留私有前缀但允许测试访问（Python 惯例允许）。owner 可决定是否将其重命名为公共函数。
2. **Test 4 的抽样策略**：当前建议每 sheet 取 3 行（首、中、末）。owner 可决定是否需要更大的抽样范围或全量比对。
3. **P2 是否需要新增 pytest fixture？**如果多个测试需要相同的 workbook 实例，建议提取为 `@pytest.fixture` 避免重复生成。
4. **空值等价函数的放置位置**：建议放在 `tests/test_exporters.py` 模块级别，供多个测试复用。
