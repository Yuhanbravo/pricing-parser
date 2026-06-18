# R1 Workbook Export Consistency Audit

## Status

done

## Scope

对 `src/valuation_parser/exporters.py` 中 workbook export 与 CSV export 的关系进行只读审计，覆盖字段常量、CSV 导出函数、workbook 导出函数、sheet 与 CSV 映射关系、空值处理、workbook 文件名生成逻辑、现有测试覆盖和 baseline 覆盖情况。

## Tools used

- 工具：Claude Code（只读文件检查、glob 文件匹配、grep 内容搜索）
- 选择理由：任务书允许实习生自主选择工具；Claude Code 可高效并行读取文件和正则搜索代码库
- 人工核查记录：
  - 手动逐行核对 `exporters.py` 中所有 `*_FIELDS` 常量定义
  - 将字段数量与现有 R1 准备材料交叉比对
  - 手动追踪 `_build_output_workbook_filename()` 日期提取逻辑
  - 手动审查 `test_acceptance_baseline.py` 中 `_read_workbook_rows()` 确认 workbook-content baseline 覆盖
  - 确认整个审计过程中未修改任何源码文件
  - 确认所有结论基于实际代码阅读而非 AI 推测

## Files inspected

| 文件 | 审计目的 |
|---|---|
| `src/valuation_parser/exporters.py` | 主审计目标：字段常量、CSV 导出、workbook 导出 |
| `src/valuation_parser/pipeline.py` | Workbook 文件名生成逻辑、输出字典结构 |
| `tests/test_acceptance_baseline.py` | Workbook-content baseline 测试覆盖检查 |
| `tests/test_smoke.py` | Header 契约、文件名、输出存在性检查 |
| `tests/test_exporters.py` | Summary 和 taxonomy 列的单测 |
| `tests/test_review_items.py` | Review item 生成逻辑（间接影响导出） |
| `data_samples/expected/` | 现有 baseline 文件（CSV、summary、workbook） |
| `data_samples/expected/README.md` | Baseline 目录说明文档 |
| `tasks/2026-06-16_R1_workbook_baseline_export_consistency.md` | 已有 R1 准备材料（已完成字段对账） |
| `docs/roadmap.md` | R1 阶段定义与完成标准 |
| `docs/status.md` | 当前项目状态与推荐下一步 |

## Current export pipeline summary

- CLI / 管线入口：`run_pipeline()` 位于 `src/valuation_parser/pipeline.py`
- CSV 导出入口：`write_routing_results()`、`write_subjects()`、`write_positions()`、`write_review_items()` 位于 `src/valuation_parser/exporters.py`
- Workbook 导出入口：`write_excel_workbook()` 位于 `src/valuation_parser/exporters.py`
- 输出目录行为：所有产物写入用户指定的 `output_dir`；每次写入前执行 `path.parent.mkdir(parents=True, exist_ok=True)`
- Workbook 文件名逻辑：`pipeline.py` 中 `_build_output_workbook_filename()` 从输入文件名中提取日期（支持 YYYY-MM-DD 和 YYYYMMDD 两种格式），取最早日期；若未提取到任何日期，回退至常量 `DEFAULT_WORKBOOK_FILENAME` = `估值表解析_output.xlsx`

## Field constants mapping

| 常量 | 字段数 | CSV 使用 | Workbook 使用 | 目标输出 |
|---|---|---|---|---|
| `ROUTING_FIELDS` | 10 | 是 | 是 | `routing_results`（CSV + sheet） |
| `SUBJECT_FIELDS` | 35 | 是 | 是 | `valuation_subjects`（CSV + sheet） |
| `POSITION_FIELDS` | 31 | 是 | 是 | `valuation_positions`（CSV + sheet） |
| `REVIEW_FIELDS` | 17 | 是 | 是 | `review_items`（CSV + sheet） |

**关键发现**：四组字段常量均在 `exporters.py` 模块级别唯一定义一次，CSV 导出路径（`_write_csv`）和 workbook 导出路径（`_write_sheet`）共享同一组常量。不存在 workbook 独立维护一套字段定义的情况。该架构从根源上防止了 CSV 与 workbook 之间的字段漂移。

各模型（`RouteDecision`、`SubjectRecord`、`PositionRecord`、`ReviewItem`）的 `to_row()` 方法返回 `dict[str, object | None]`。`_write_csv`（通过 `csv.DictWriter`）和 `_write_sheet`（通过 `worksheet.append`）消费相同的行字典、对照相同的字段常量。

## Sheet-to-CSV mapping

| Workbook sheet | 对应 CSV | 字段来源 | 备注 |
|---|---|---|---|
| `routing_results` | `routing_results.csv` | `ROUTING_FIELDS` | 相同 `to_row()` 调用，相同字段顺序 |
| `valuation_subjects` | `valuation_subjects.csv` | `SUBJECT_FIELDS` | 相同 `to_row()` 调用，相同字段顺序 |
| `valuation_positions` | `valuation_positions.csv` | `POSITION_FIELDS` | 相同 `to_row()` 调用，相同字段顺序 |
| `review_items` | `review_items.csv` | `REVIEW_FIELDS` | 相同 `to_row()` 调用，相同字段顺序 |

Workbook 仅包含上述四个 sheet，没有额外的 sheet。`parse_summary.md` 是独立的 Markdown 文件，不包含在 workbook 中。

## Consistency dimensions

### Sheet names

Sheet 名称与对应 CSV 文件名完全一致：`routing_results`、`valuation_subjects`、`valuation_positions`、`review_items`。Sheet 名称在 `write_excel_workbook()` 中以内联字符串字面量硬编码（非从常量派生）。风险：如果 `pipeline.py` 中 CSV 文件名发生变更，而 `write_excel_workbook()` 中的 sheet 名称字面量未同步更新，可能导致命名不一致。但目前两者均稳定，且在同一模块中近距定义。**审计结论**：实际风险低——sheet 名称自初始实现以来保持稳定，且已由 `test_acceptance_baseline.py` 间接验证。

### Header / column names

CSV 和 workbook 使用完全相同的 `*_FIELDS` 常量作为表头。列名采用 snake_case 英文标识符，无中文字段名。已有 R1 准备材料的字段对账确认：4 对产物在字段数量、名称、顺序上全部一致。

### Column order

CSV 列顺序 = workbook 列顺序 = `*_FIELDS` 列表顺序。`_write_csv` 使用 `csv.DictWriter(fieldnames=fieldnames)` 对表头和数据行均保持列表顺序。`_write_sheet` 先 `worksheet.append(fieldnames)` 写入表头，再按 `fieldnames` 顺序逐行写入。两条路径均为顺序保持路径，不存在重排序。

### Row counts

Workbook 和 CSV 接收来自 `run_pipeline()` 的同一批数据列表（`routes`、`subjects`、`positions`、`review_items`）。因消费相同的内存数据，行数天然一致。已有 R1 准备材料确认：4 对产物行数完全一致。

### Empty / null value handling

CSV 路径：`row.get(field)` 对缺失键返回 `None`；`csv.DictWriter` 将 `None` 转为空字符串 `""`。Workbook 路径：`row.get(field)` 对缺失键返回 `None`；`openpyxl` 将 `None` 写为空单元格。两者存在表示差异（CSV 使用 `""`，workbook 使用 `None` / 空单元格），但语义等价——均表示"无值"，底层数据完全一致。测试影响：CSV 与 workbook 之间的直接文本比对会将此标记为差异；需要进行内容级比对（将 `None` ↔ `""` 视为等价）。当前 baseline 测试 `test_acceptance_baseline.py` 分别进行 workbook-to-workbook 和 CSV-to-CSV 比对（非跨格式比对），因此该表示差异不会导致测试失败。

### Date-derived workbook filename

文件名生成逻辑：`_build_output_workbook_filename()` 从所有输入文件名中提取日期，排序后取最早日期。日期提取模式（按优先级）：(1) `YYYY-MM-DD`（带连字符，如 `2025-03-27`）；(2) `YYYYMMDD`（8 位连续数字，如 `20250327`）。多日期行为：取 `extracted_dates[0]`（排序后最早日期）。无日期行为：回退至 `DEFAULT_WORKBOOK_FILENAME` = `估值表解析_output.xlsx`。当前 baseline 文件名：`估值表解析_output_2025-03-27.xlsx`——这是在 `data_samples/expected/` 中固定的文件名。**关键观察**：当前 baseline 文件名固定为 `2025-03-27`，因为所有 raw 样本均携带该日期。如果将来添加不同日期的样本，生成的文件名将随之变化。

### Selected stable values

已有 R1 准备材料（`tasks/2026-06-16_R1_workbook_baseline_export_consistency.md`）已完成字段数量对账（4/4 通过）、字段名称与顺序对账（4/4 通过）、行数对账（4/4 通过）、空值对账（4/4 通过，None 数量 = 空串数量，位置一致）、抽样值比对（每对产物各 9 行，仅存在微小格式差异——Excel 中 int 与 float 的呈现差异）。

## Existing test coverage

- 测试文件数：`tests/` 下共 11 个测试文件
- 已有覆盖：
  - **`test_acceptance_baseline.py::test_strict_default_run_matches_acceptance_baseline`**：完整验收基线测试，包含 workbook sheet-content 比对。该测试通过 `_read_workbook_rows()` 使用 `openpyxl`（`read_only=True, data_only=True`）加载期望和实际的 workbook，将所有 sheet 提取为 `dict[str, list[list[object | None]]]` 进行比对。**这是一个 workbook-content baseline 测试。**
  - **`test_smoke.py`**：多个测试验证 workbook 文件存在性（`outputs["output_workbook"].exists()`）和文件名正确性（`outputs["output_workbook"].name == "估值表解析_output_2025-03-27.xlsx"`）
  - **`test_smoke.py::test_pipeline_locks_export_header_contracts_for_current_baseline`**：验证 CSV 表头与期望字符串一致
  - **`test_exporters.py`**：测试 `write_summary` 内容和 taxonomy 列。**未**单独测试 `write_excel_workbook()`
- 未覆盖：
  - 没有针对 `write_excel_workbook()` 的独立单元测试——仅通过完整管线间接测试
  - 没有跨格式一致性测试（同一行/列的 CSV 单元格值与对应 workbook 单元格值比对）
  - 没有专门测试 workbook sheet 名称是否为精确集合 `{routing_results, valuation_subjects, valuation_positions, review_items}`
  - 没有专门测试 workbook 表头是否匹配 `*_FIELDS` 常量（仅有 CSV 表头被 smoke test 锁定）
  - 没有针对同输入多次运行的文件名确定性的测试
  - 没有针对多日期输入文件名行为的测试

## Existing baseline coverage

`data_samples/expected/` 下包含以下文件：`routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv`、`parse_summary.md`、`估值表解析_output_2025-03-27.xlsx`、`README.md`（baseline 说明文档，非测试产物）。

- 是否存在 workbook-content baseline：**是**。`估值表解析_output_2025-03-27.xlsx` 即为 workbook-content baseline。
- 是否被测试使用：**是**。`test_acceptance_baseline.py` 通过 `_read_workbook_rows()` 加载并比对。
- 是否文本可读：**否**。`.xlsx` 是二进制格式（ZIP 压缩 XML），无法进行有意义的文本 diff。测试通过 `openpyxl` 程序化读取并比对待结构数据（sheet → 行 → 单元格）。
- 实际 baseline 策略：Workbook baseline 已作为 **sheet-content baseline**（而非字节级二进制 baseline）维护。测试将期望和实际 workbook 读入内存作为结构化数据比对——这是内容级比对，而非二进制 diff。

## Findings

| # | 发现 | 严重程度 | 证据 | 建议 |
|---|---|---|---|---|
| 1 | CSV 和 workbook 共享同一组 `*_FIELDS` 常量——不存在字段定义重复 | 信息 | `exporters.py` 第 11–114 行：常量同时被 `_write_csv()` 和 `_write_sheet()` 使用 | 无需处理；架构设计合理 |
| 2 | Workbook-content baseline 已存在且被测试覆盖 | 信息 | `test_acceptance_baseline.py` 第 38–40 行：`_read_workbook_rows()` 比对；`data_samples/expected/估值表解析_output_2025-03-27.xlsx` 存在 | 当前覆盖充分；P2 应增加聚焦的跨格式一致性测试 |
| 3 | 无针对 `write_excel_workbook()` 的独立单元测试 | 低 | `test_exporters.py` 测试了 CSV writer 和 `write_summary`，但未测试 `write_excel_workbook` | P2 中增加聚焦单元测试（非本轮 PR） |
| 4 | Workbook sheet 名称以内联字符串字面量硬编码，未从常量或 CSV 文件名派生 | 低 | `exporters.py` 第 363–366 行：`"routing_results"`、`"valuation_subjects"` 等为字符串字面量 | 风险低；sheet 名称稳定。如果将来 sheet 名称变更，可考虑提取为常量 |
| 5 | 日期派生文件名在新增不同日期样本时可能导致 baseline 文件名不匹配 | 中 | `pipeline.py` 第 85–89 行：文件名取最早提取日期；接收测试硬编码 `2025-03-27` | 文件名对固定输入集是确定性的，非 bug。但意味着每次输入日期变更时需更新 baseline 文件名。P2 应锁定文件名确定性 |
| 6 | 空值表示在 CSV（`""`）和 workbook（`None`）之间存在差异，但数据语义等价 | 信息 | `exporters.py` 第 384 行：`row.get(field)` 对缺失键返回 `None`；CSV `DictWriter` 转为 `""`，openpyxl 写入 `None` | 非 bug。P2 跨格式一致性测试需处理此等价关系 |
| 7 | 已有 R1 准备材料已全面覆盖字段对账工作 | 信息 | `tasks/2026-06-16_R1_workbook_baseline_export_consistency.md` 第 3–5 节 | 本次审计独立确认了这些结论。准备材料的结论与源码检查结果一致 |
| 8 | Workbook 生成不包含 `parse_summary.md` 内容 | 信息 | `exporters.py` 第 352–369 行：仅 4 个数据 sheet；summary 为独立 Markdown 文件 | 设计如此。Summary 为文本性质，非表格数据。无需处理 |

## P2 test design candidates

详见独立文件：`tasks/2026-06-16_R1_workbook_export_consistency_p2_test_design.md`

P2 建议测试摘要：
1. Workbook sheet 名称与预期集合一致
2. Workbook 表头与 `*_FIELDS` 常量一致
3. Workbook 行数与 CSV 输出行数一致
4. 抽样稳定值与 CSV 对应值一致
5. 日期派生文件名对相同输入具有确定性

## Open questions for owner

所有待决策事项详见 `tasks/2026-06-16_R1_workbook_baseline_owner_decision_note.md`。摘要：

1. **Workbook 验收角色**：Workbook 是正式交付物（A）、CSV 镜像（B）、还是人工查看辅助物（C）？
2. **独立 workbook baseline**：是否需要在当前 sheet-content 比对之外维护独立的 workbook baseline？
3. **CSV 与 workbook 权威性**：如果 CSV 和 workbook 内容不一致，哪个输出应视为权威？
4. **文件名稳定性**：日期派生文件名 `估值表解析_output_<date>.xlsx` 是否属于稳定契约？
5. **输出契约范围**：哪些输出是正式交付物，哪些是调试产物？
