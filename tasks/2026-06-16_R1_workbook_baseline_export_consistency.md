# R1 Workbook Baseline与导出一致性报告

**Roadmap stage**：R1 — Workbook 基线与导出一致性

---

## 1. Workbook 定位

### 当前状态

`估值表解析_output_<date>.xlsx` 是 parser 运行后生成的 Excel 工作簿，与 CSV 产物共享同一组输入数据（`routes`、`subjects`、`positions`、`review_items`），通过 `openpyxl` 写入。

### 产物层级

```
一次 parser 运行产出：
├── routing_results.csv          ← 路由决策 CSV
├── valuation_subjects.csv       ← 科目 CSV
├── valuation_positions.csv      ← 持仓 CSV
├── review_items.csv             ← 人工复核 CSV
├── parse_summary.md             ← Markdown 运行摘要
└── 估值表解析_output_<date>.xlsx  ← Excel 工作簿（聚合上述 4 表）
```

### 定位判断

| 维度 | 说明 |
|---|---|
| 数据来源 | 与 CSV 完全同源（同一批 `RouteDecision` / `SubjectRecord` / `PositionRecord` / `ReviewItem` 列表） |
| 写入方式 | `exporters.py` 中 `write_excel_workbook()` 使用与 CSV 相同的 `*_FIELDS` 常量和 `to_row()` 方法 |
| 是否独立基线 | 当前是 CSV baseline 的 Excel 镜像，非独立验收产物 |
| 维护策略 | 随 CSV baseline 同步刷新，不作为单独验收契约 |

---

## 2. Workbook Sheet 目录

| Sheet 名称 | 字段数 | 数据行数 (当前 baseline) | 对应 CSV |
|---|---|---|---|
| `routing_results` | 10 | 11 | `routing_results.csv` |
| `valuation_subjects` | 35 | 1,022 | `valuation_subjects.csv` |
| `valuation_positions` | 31 | 182 | `valuation_positions.csv` |
| `review_items` | 17 | 238 | `review_items.csv` |

---

## 3. 字段命名规则

### 3.1 命名风格

- **全小写下划线**（snake_case）：所有字段名使用英文小写 + 下划线，如 `source_file`、`asset_type_internal`、`raw_row_index`。
- **中文字段值**：展示类字段使用中文值，如 `asset_type_display` 取值 `"A股股票"`、`asset_class_l1` 取值 `"权益类"`。
- **无前缀编号**：字段名不使用数字前缀或类型前缀，保持纯语义命名。

### 3.2 字段分组惯例

每个 sheet 的字段按以下逻辑分组排列：

1. **溯源字段**（trace）：`source_file`、`broker`、`sheet_name`、`valuation_date`、`product_id`、`association_code`、`custodian_id`、`custodian_name`、`adapter_key`、`route_source`
2. **业务主键**：`raw_row_index`、`subject_code`、`subject_name` / `instrument_name` 等
3. **层级/分类字段**：`parent_subject_code`、`subject_level`、`asset_type_internal`、`asset_type_display`、`asset_class_l1`、`asset_class_l2` 等
4. **数值字段**：`quantity`、`unit_cost`、`cost`、`market_price`、`market_value`、`pnl` 等
5. **复核/标记字段**：`review_flag`、`review_note`、`review_category`、`review_reason` 等
6. **辅助字段**：`raw_text`、`suspension_info` 等

### 3.3 字段定义权威来源

所有字段列表的唯一定义位于 `src/valuation_parser/exporters.py` 的模块级常量：

```python
ROUTING_FIELDS   = [...]  # routing_results sheet + CSV
SUBJECT_FIELDS   = [...]  # valuation_subjects sheet + CSV
POSITION_FIELDS  = [...]  # valuation_positions sheet + CSV
REVIEW_FIELDS    = [...]  # review_items sheet + CSV
```

CSV 和 Workbook **共用这些常量**，不存在独立定义。要修改字段，只需改这一处。

---

## 4. Parse Summary 内容结构

`parse_summary.md` 是 Markdown 格式的运行摘要，与 workbook 同时生成。其结构如下：

### 4.1 固定节段

| 节 | 内容 | 说明 |
|---|---|---|
| `# Parse Summary` | 运行统计数字 | 处理文件数、成功/失败路由数、subject/position/review 行数等 |
| `## Asset Type Coverage` | 资产类型分布表 | `asset_type_display` → count 的两列表格 |
| `## Unrouted File Details` | 未路由文件清单 | 列出所有 `route_status != success` 的文件 |
| `## Unrecognized Object Index` | 未识别对象索引 | 每条包含 `source_file`、`product_id`、`route_message` |
| `## Review Entry Index` | 复核入口索引 | 每条包含 `source_file`、`raw_row_index`、`subject_code`、`subject_name`、`entrypoint`（subject/position）、`reasons` |
| `## Review Queue By Source File` | 按文件汇总的复核队列 | 每个文件列出 review entry 数和 top 3 复核原因 |

### 4.2 关键设计决策

- **Review Entry Index** 合并了 subject 层 (`review_items`) 和 position 层 (`valuation_positions.review_note`) 的复核条目，去重 key 为 `(source_file, raw_row_index, subject_code, subject_name)`。
- **entrypoint 字段** 标明复核触发来源：`subject`（来自 `review_items`）、`position`（来自 `valuation_positions.review_note`）、`subject+position`（两者皆有）。
- **reasons 字段** 使用中文全角分号 `；` 作为分隔符，支持多个复核原因合并展示。

---
## 5. 字段对账：CSV ↔ Workbook 一致性检查

**检查范围**：`data_samples/expected/` 目录下的 4 对 CSV/Workbook 产物


### 5.1 字段数量

| 产物 | Workbook | CSV | 结果 |
|---|---|---|---|
| routing_results | 10 | 10 | ✅ PASS |
| valuation_subjects | 35 | 35 | ✅ PASS |
| valuation_positions | 31 | 31 | ✅ PASS |
| review_items | 17 | 17 | ✅ PASS |

### 5.2 字段名称与顺序

4 对产物的字段名称和列顺序完全一致，排查结论：均在 `src/valuation_parser/exporters.py` 中使用同一份 `*_FIELDS` 常量列表写入，因此不存在命名或顺序漂移。

| 产物 | 结果 |
|---|---|
| routing_results | ✅ PASS |
| valuation_subjects | ✅ PASS |
| valuation_positions | ✅ PASS |
| review_items | ✅ PASS |

### 5.3 数据行数

| 产物 | Workbook | CSV | 结果 |
|---|---|---|---|
| routing_results | 11 | 11 | ✅ PASS |
| valuation_subjects | 1022 | 1022 | ✅ PASS |
| valuation_positions | 182 | 182 | ✅ PASS |
| review_items | 238 | 238 | ✅ PASS |

### 5.4 空值策略

- Workbook 空值：单元格为 `None`（openpyxl 读取时返回）
- CSV 空值：空字符串 `""`（CSV 写入时 model 返回 `None`，DictWriter 转为空串）
- **两种表示等价，对应关系一致**：workbook `None` 数量 = CSV 空串数量，且匹配同一行同一列。

| 产物 | Workbook None 数 | CSV 空串数 | 不一致次数 | 结果 |
|---|---|---|---|---|
| routing_results | 13 | 13 | 0 | ✅ PASS |
| valuation_subjects | 5,555 | 5,555 | 0 | ✅ PASS |
| valuation_positions | 538 | 538 | 0 | ✅ PASS |
| review_items | 337 | 337 | 0 | ✅ PASS |

### 5.5 数据值抽样比对

对每对产物取前 3 行 + 中间 3 行 + 最后 3 行（共 9 行抽样），逐字段比较。

| 产物 | 抽样行 | 不一致次数 | 结果 |
|---|---|---|---|
| routing_results | 9/11 | 0 | ✅ PASS |
| valuation_subjects | 9/1022 | 16 | ⚠️ 仅格式差异 |
| valuation_positions | 9/182 | 18 | ⚠️ 仅格式差异 |
| review_items | 9/238 | 6 | ⚠️ 仅格式差异 |

**格式差异详情**：Workbook 中整数数值显示为 `0`、`16300`，CSV 中对应字段显示为 `0.0`、`16300.0`。

**根因分析**：
- Python `float` 类型值（如 `0.0`、`16300.0`）写入 CSV 时，`csv.DictWriter` 调用 `str()` 生成 `0.0`、`16300.0`。
- 同一 `float` 值写入 Excel 后，`openpyxl` 将其存储为 Excel 数字类型；Excel 对 `0.0` 的默认显示为 `0`（不显示无意义的小数部分）。使用 `data_only=True` 读回时，`openpyxl` 返回 `int` 类型的 `0` 而非 `float` 类型的 `0.0`。
- **这不影响数据语义**，仅反映 Excel 与 CSV 对数值的不同呈现层约定。

### 5.6 结论

- ✅ 字段名、顺序、数量、行数、空值策略：**4 对产物全部一致**。
- ⚠️ 数值格式：存在 `int` vs `float` 呈现差异，为 Excel 与 CSV 格式层的**已知天然差异**，不影响数据完整性和语义一致性，**无需修复**。
- 代码层面：`exporters.py` 中 CSV 和 Workbook 共用同一组 `*_FIELDS` 常量，架构上已确保不会出现字段漂移。


## 6. 需要 Owner 决策的事项

以下问题需要 owner 确认后才能在 R1 中关闭：

| # | 决策项 | 选项 | 影响 |
|---|---|---|---|
| 1 | Workbook 是否作为正式验收产物？ | A. 是，需独立维护 basline<br>B. 否，作为 CSV 的派生镜像 | 决定维护负担和 PR 审阅流程 |
| 2 | 下游消费方更依赖哪种格式？ | A. CSV<br>B. Workbook<br>C. 两者同等 | 决定 baseline 保护的优先级 |
| 3 | 是否接受日期派生文件名？ | A. 接受，每次随输入刷新<br>B. 不接受，改为固定名 | 影响 baseline 文件的 Git 历史稳定性 |
| 4 | 是否需要补充 workbook 专项 regression？ | A. 需要，在 tests/ 中补齐<br>B. 不需要，CSV regression 即覆盖 | 决定 R1 的完成标准 |



