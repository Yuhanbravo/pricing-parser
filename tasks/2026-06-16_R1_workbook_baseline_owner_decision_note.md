# R1 Workbook Baseline Owner Decision Note

## Purpose

本文档基于 R1-P1 只读审计结果，整理 workbook 验收角色、baseline 策略、CSV vs workbook 权威性、文件名稳定性和 P2 回归方向的 owner decision 选项。5 项决策已由 owner 确认（详见各 Decision 的 `confirmed` 标记）。

## Facts from audit

以下事实来自 `tasks/2026-06-16_R1_workbook_export_consistency_audit.md` 的审计结论：

1. **字段定义共享**：CSV 和 workbook 在 `exporters.py` 中共享同一组 `ROUTING_FIELDS`、`SUBJECT_FIELDS`、`POSITION_FIELDS`、`REVIEW_FIELDS` 常量，不存在独立字段定义。
2. **数据同源**：Workbook 和 CSV 消费来自 `run_pipeline()` 的同一批 `routes`、`subjects`、`positions`、`review_items` 内存数据。
3. **Baseline 现状**：`data_samples/expected/估值表解析_output_2025-03-27.xlsx` 已作为 workbook-content baseline 存在，且 `test_acceptance_baseline.py` 通过 `_read_workbook_rows()` 进行 sheet-content 级比对——当前并非字节级二进制 baseline。
4. **空值表示差异**：CSV 空值表示为 `""`，workbook 空值表示为 `None`/空单元格。语义等价，但跨格式直接比对时需处理此差异。
5. **文件名日期派生**：Workbook 文件名 `估值表解析_output_<date>.xlsx` 从输入文件名中提取日期生成，取最早日期。对相同输入确定，但随输入日期变化。
6. **测试缺口**：无独立 `write_excel_workbook()` 单元测试，无跨格式（CSV ↔ workbook）一致性测试，无文件名确定性测试。

## Decision 1: Workbook acceptance role

问题：Workbook 是正式验收产物，还是 CSV 的便捷镜像？

### 候选选项

| 选项 | 含义 | 后果 |
|---|---|---|
| A | Workbook 是正式交付物 | 需要更强 workbook-specific regression 或独立 baseline |
| B | Workbook 是 CSV 镜像 | 不单独维护 workbook baseline，用一致性测试保护 |
| C | Workbook 是人工查看辅助物 | 只做基本生成测试，不承诺强字段契约 |

### 推荐选项：B — Workbook 是 CSV 镜像

### 推荐理由

1. 代码架构层面，workbook 和 CSV 共享同一组 `*_FIELDS` 常量和 `to_row()` 方法，workbook 本质上是 CSV 数据的 Excel 格式镜像，而非独立输出。
2. 当前 `data_samples/expected/` 中 workbook baseline 已是 sheet-content 形式，但所有语义验证本质上依赖 CSV baseline。
3. 选择 B 的维护成本最低：CSV baseline 变化时 workbook 随动更新，不需要独立维护两套验收标准。
4. 避免 `.xlsx` 二进制 diff 带来的非语义噪声（如 openpyxl 内部样式/元数据差异）。
5. 如果下游消费方后续要求 workbook 作为正式交付物，可从 B 升级到 A——但反过来（从 A 退到 B）更困难。

### Owner decision (Decision 1)

- **confirmed** — 采用选项 B。Workbook 定位为 CSV 的 Excel 镜像 / 人工友好派生物，不作为独立权威产物。

## Decision 2: Independent workbook baseline

问题：是否维护 `估值表解析_output_<date>.xlsx` 的独立 expected baseline？

### 候选选项

| 选项 | 含义 |
|---|---|
| 不维护独立二进制 workbook baseline | 当前 sheet-content baseline 通过 `openpyxl` 读取后比对结构化数据 |
| 维护 content-level extracted baseline | 将 workbook 内容提取为文本格式（如 JSON/csv snapshot）作为 baseline |
| 维护完整 workbook 二进制 baseline | 直接 `.xlsx` 字节比对 |
| 其他 | — |

### 推荐选项：维持当前 content-level sheet baseline，不升级为二进制 baseline

### 推荐理由

1. `.xlsx` 是 ZIP 压缩 XML 格式，二进制 diff 不可读。任何 openpyxl 版本升级或内部元数据变化都可能产生非语义 diff。
2. 当前 `test_acceptance_baseline.py` 中的 `_read_workbook_rows()` 方案已将 workbook 内容提取为结构化数据（`dict[str, list[list[object | None]]]`），能有效捕获语义变化。
3. 无需额外文本提取步骤——当前方案的比对逻辑简洁、可读、可调试。
4. 如果将来需要更轻量的 baseline 文本化，可考虑将 workbook 每 sheet 导出为 CSV 片段作为 extracted baseline——但这在当前阶段并非必要，因为 CSV baseline 本身已在 `data_samples/expected/` 中维护。

### Owner decision (Decision 2)

- **confirmed** — 维持当前 sheet-content / structured read comparison 口径，不升级为二进制验收。不采用 .xlsx 字节级 binary baseline。

## Decision 3: CSV vs workbook authority

问题：如果 CSV 和 workbook 内容不一致，哪个输出应视为权威？

### 候选选项

| 选项 | 含义 |
|---|---|
| CSV 为权威 | 不一致时以 CSV 为准；workbook 视为派生格式 |
| Workbook 为权威 | 不一致时以 workbook 为准；CSV 视为导出副产品 |
| 二者同为正式交付物 | 不一致即为 bug，需修复 |
| 分 sheet / 字段判断 | 不同输出类型有不同权威来源 |

### 推荐选项：CSV 为权威

### 推荐理由

1. CSV 是 parser 的直接文本输出，通过 `csv.DictWriter` 写入，无中间格式转换。Workbook 经过 `openpyxl` 的 Excel 序列化层，引入了额外的格式层（如 int/float 呈现差异）。
2. CSV 可文本 diff，适合 Git 代码审查。Workbook 是二进制格式，无法直接 diff。
3. 当前测试架构以 CSV baseline 为核心：`test_acceptance_baseline.py` 逐文件比对 CSV 文本内容，workbook 则通过结构化数据比对。CSV 是更"直接"的真值源。
4. 在代码层面，如果 `*_FIELDS` 常量或 `to_row()` 方法出错，CSV 和 workbook 会同时出错——因为共享同一数据源。真正的"不一致"更可能来自 openpyxl 序列化层的漂移，而非数据层漂移。

### Owner decision (Decision 3)

- **confirmed** — CSV 为语义权威。若 CSV 与 workbook 不一致，应视为 bug，但判断和修复应优先回到 CSV、字段常量和 `to_row()` 数据源。

## Decision 4: Filename stability

问题：日期派生文件名 `估值表解析_output_<date>.xlsx` 是否属于稳定契约？

### 审计事实

- 日期来自输入文件名中的日期字符串（YYYY-MM-DD 或 YYYYMMDD 格式）
- 多文件时取最早日期
- 无日期时回退至 `估值表解析_output.xlsx`
- 当前所有 raw 样本日期均为 `2025-03-27`，因此当前文件名固定
- 如果新增不同日期的样本，文件名会自动变化

### 候选选项

| 选项 | 含义 |
|---|---|
| 接受日期派生文件名 | 文件名随输入日期变化，baseline 文件名需同步更新 |
| 改为固定文件名 | 移除日期后缀，使用固定名如 `估值表解析_output.xlsx` |
| 保持当前行为但纳入测试契约 | 将文件名确定性纳入 regression，确保同输入同文件名 |

### 推荐选项：保持当前行为但纳入测试契约（选项 C）

### 推荐理由

1. 日期派生文件名对下游消费有实际价值——可以从文件名快速识别估值日期。
2. 当前逻辑是确定性的：相同输入集产生相同文件名。不需要改为固定名。
3. 当前测试（`test_smoke.py`）已硬编码验证 `"估值表解析_output_2025-03-27.xlsx"`，但未测试文件名生成逻辑本身。P2 应单独测试 `_build_output_workbook_filename()` 的确定性。
4. 如果将来输入样本日期发生变化，baseline 文件名需随之更新——这是接受的维护成本，应在 `docs/status.md` 中注明。

### Owner decision (Decision 4)

- **confirmed** — 保持当前日期派生文件名规则，不在本轮修改 runtime 文件名行为。在 R1-P2 中纳入 regression test。

## Decision 5: P2 regression direction

问题：R1-P2 应优先实现哪些 regression tests？

### 推荐方案

基于审计发现的缺口，按优先级建议以下 P2 测试：

| 优先级 | 测试 | 理由 |
|---|---|---|
| P0 | Test 3: Workbook 行数与 CSV 输出行数一致 | 直接保护 workbook ↔ CSV 数据行数一致性，防止序列化路径意外丢行；实现简单 |
| P0 | Test 4: 抽样稳定值与 CSV 对应值一致 | 唯一直接验证单元格级跨格式一致性的测试，覆盖空值等价和数值类型差异风险 |
| P0 | Test 5: 日期派生文件名对相同输入具有确定性 | 保护文件名确定性契约，降低新增样本后 baseline 文件名不匹配的维护摩擦 |
| P2 | Test 1: Workbook sheet names 与预期集合一致 | 触发风险极低：sheet 名称硬编码且自初始实现以来从未变更 |
| P2 | Test 2: Workbook 表头与 `*_FIELDS` 常量一致 | 触发风险极低：`*_FIELDS` 常量共享使用，CSV 表头已有 smoke test 锁定，workbook 表头漂移概率近乎为零 |

### 明确不提议的测试

- `.xlsx` 字节级比对：二进制 diff 不可读，openpyxl 版本敏感性高
- Workbook 样式/格式断言：不属于数据契约
- Baseline 刷新：P1 阶段不做 baseline 变更
- Runtime 行为变更：P1/P2 仅做只读审计和测试设计，P2 实现测试不改变 parser

### Owner decision (Decision 5)

- **confirmed** — 授权进入 R1-P2: workbook ↔ CSV consistency regression implementation。R1-P2 只允许新增 focused tests，不改 runtime、不刷新 baseline、不处理 R2/R3/R4 内容。

## Items not decided in this PR

以下事项不在本轮 PR 范围内，也不应被理解为已确认：

- `PRODUCT_022` 的处理策略
- 是否新增 adapter
- 是否调整 taxonomy
- 是否改变 review item 生成规则
- 是否进入 R2 / R3 / R4
- DeepSeek Review workflow 是否调整
- `data_samples/expected/` 是否需要新增 baseline 文件
