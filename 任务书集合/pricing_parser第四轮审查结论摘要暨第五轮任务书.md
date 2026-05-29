# pricing_parser 第四轮审查结论摘要暨第五轮任务书（含场外衍生品提前规划版）

## 文档定位

本文用于承接 `pricing-parser / valuation_parser` 项目 Round 4 合并后的下一阶段任务，作为实习生新分支开发、AI 审阅、人工验收和后续 handoff 的统一任务书。

- 上一轮：Round 4 资产术语收敛 / `asset taxonomy closure`
- 本轮主任务：Round 5A 官方估值与会计口径文件资产化
- 紧随其后的任务：Round 5B 标准会计科目映射层设计与接入准备
- 提前规划支线：Round 5C 场外衍生品识别与穿透模型设计
- 后续最小实现：Round 5D 场外衍生品最小解析与 review queue

本文是**任务书 / task package**，不是 execution report。施工完成后，应另行提交 execution report，并在 PR 中保留 review closeout message。

---

## 一、Round 4 审查结论摘要

### 1. Round 4 已完成事项

Round 4 已完成 asset taxonomy 闭环，主要包括：

- 新增 `config/asset_taxonomy.yaml`，作为资产展示分类的统一配置来源。
- 在 `valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv` 中增加 taxonomy 字段：
  - `asset_type_internal`
  - `asset_type_display`
  - `asset_class_l1`
  - `asset_class_l2`
- 在 subjects / review items 中保留 `review_category`。
- `parse_summary.md` 改为使用展示型 taxonomy label，并增加 `Asset Type Coverage` 统计。
- ETF / 场内基金统一按基金类展示，不按权益类处理。
- 收益互换、保证金、清算款、负债类科目不进入 `valuation_positions.csv`，仅保留在 subjects / review / summary 口径。
- `PRODUCT_022` 仍作为 strict-default 下的 intentional routing failure，不在 Round 4 中补 mapping 或新增 adapter。
- 新增项目内实验 skill：`skill_experiments/acceptance-baseline-refresh/`，用于受控 baseline refresh 流程试跑，不进入 `ai-skill-hub`。

### 2. Round 4 gate / review 收口结论

Round 4 PR 曾出现以下合并前问题：

- Windows 下 taxonomy 测试因临时 YAML 写入编码问题失败。
- `.bundle`、`.code-workspace`、`egg-info` 等非预期文件进入 PR diff。
- `525` vs `508` review-flagged subjects 存在文档口径漂移。
- 部分 task docs 中保留本地绝对路径。

最终修复后，Round 4 已完成：

- Windows 编码测试修复。
- 误提交 artifact 清理。
- `.gitignore` 补充。
- 文档 evidence-chain 口径统一到当前 accepted baseline。
- Round 4 边界保持：无新增 adapter、无 `PRODUCT_022` 处理、无 routing redesign、无核心计算重写。

本轮必须继承 Round 4 边界：**不要在 reference assetization 阶段修改 parser 输出契约，也不要刷新 expected baseline。**

---

## 二、第五轮总体路线

本阶段从“官方口径纳入项目”开始，但不应一次性完成所有代码接入。建议拆成四个连续小轮：

```text
Round 5A：官方估值与会计口径文件资产化
Round 5B：标准会计科目映射层设计与接入准备
Round 5C：场外衍生品识别与穿透模型设计
Round 5D：场外衍生品最小解析与 review queue
```

本任务书重点落地 **Round 5A**，同时提前写明 **Round 5B / 5C / 5D** 的设计方向和边界，避免后续误把官方会计口径直接替换掉现有 asset taxonomy，或误把场外衍生品强行塞入普通场内证券持仓表。

---

## 三、本轮任务名称

# Round 5A：官方估值与会计口径文件资产化

英文标题建议：

```text
Round 5A: add official valuation and accounting reference assets
```

PR 标题建议：

```text
Round 5A: assetize official valuation and accounting references
```

分支名建议：

```text
feature/round5a-official-reference-assets
```

---

## 四、任务背景

项目当前已具备：

- 估值表原始科目解析；
- mapping-driven routing；
- adapter 层样表解析；
- strict-default acceptance baseline；
- asset taxonomy 展示分类；
- review flag / review item 人工复核队列；
- 项目内 baseline refresh 实验 skill。

但当前项目仍缺少一层更上游的官方 / 行业口径支撑：

```text
原始估值表科目
  ↓
标准会计科目 / 官方估值口径
  ↓
内部资产分类 / 场外衍生品支线 / review 分类
  ↓
CSV / Excel / summary / 后续数据中心接口
```

因此本轮先把两个公开口径文件纳入项目 reference assets，并抽取标准会计科目结构，为下一轮 Round 5B 接入 parser 输出字段、Round 5C 场外衍生品穿透支线做准备。

---

## 五、参考文件与公开纳入口径

本轮参考文件：

1. 《中国基金估值标准2018》
2. 《证券投资基金会计核算操作实务手册-20240530》

当前业务判断：这两个文件已经确认可以纳入公开仓库，属于公开口径 / 公开经验资料。

本轮允许提交：

- 原始 OCR Word 文件；
- 转换后的 Markdown 文件；
- source manifest；
- 结构化抽取 CSV；
- 人工复核队列；
- 设计说明文档。

但必须清楚说明：

- 文件来源；
- 文件版本；
- 原始格式；
- OCR / Word / Markdown 转换过程；
- 本项目中的使用边界；
- 这些文件是 `reference source`，不是 parser runtime 配置。

---

## 六、关键设计决策：官方口径不直接替代现有展示分类

本轮需要明确一个核心设计边界：

> 官方估值 / 会计口径应作为“标准会计科目层”进入项目，而不是直接替代 Round 4 已完成的 asset taxonomy / 展示分类层。

### 1. 不采用的方案

```text
原始估值表科目
→ 官方会计科目直接替换 asset_type / asset_type_display
```

### 2. 采用的方案

```text
原始估值表科目
→ 标准会计科目层
→ 内部资产分类层
→ 对外展示口径层
```

### 3. 决策原因

1. 官方会计口径主要服务会计核算、估值处理、托管复核和审计追溯，强调科目标准化。
2. 现有 asset taxonomy 主要服务解析器输出、持仓边界、review 队列和业务展示，强调投资 / 风控可读性。
3. 官方会计科目与业务展示分类不是一一对应关系。例如：
   - `1102 交易性股票投资` 可能需要继续区分 A股、港股、科创板、存托凭证；
   - `1105 交易性基金投资` 在业务展示中可能需要归为 `场内基金/ETF`；
   - `1031 存出保证金`、证券清算款、应付款项等虽然属于会计科目，但不应进入 `valuation_positions.csv`；
   - 衍生工具 / 收益互换需要进入 review 或场外衍生品支线，但不应直接作为普通证券持仓导出。
4. 如果直接用官方会计科目替换展示分类，项目会变得“会计口径更标准”，但可能降低投资、风控和数据展示场景的可读性。
5. 保留展示层有利于后续接入 Excel 报表、数据中心、投资经理速查表和人工复核队列。

### 4. 字段分层原则

后续字段应保持四层关系：

```text
subject_code / subject_name
→ account_code_std / account_name_std
→ asset_type_internal
→ asset_type_display
```

| 层级 | 字段示例 | 作用 |
|---|---|---|
| 原始估值表科目 | `subject_code`, `subject_name` | 保留托管估值表原始追溯信息 |
| 标准会计科目 | `account_code_std`, `account_name_std`, `account_class_std` | 对齐官方 / 行业会计科目口径 |
| 内部资产分类 | `asset_type_internal`, `asset_class_l1`, `asset_class_l2` | 控制 parser 输出、是否进入持仓、是否进入 review |
| 对外展示口径 | `asset_type_display` | 面向投资、风控、业务人员展示 |

### 5. 决策树

```text
是否来自估值表原始科目？
  是 → 保留 subject_code / subject_name，不改写

是否能映射到官方标准会计科目？
  是 → 填充 account_code_std / account_name_std / account_class_std
  否 → 进入 account_mapping_review，不强行归类

是否需要进入普通证券持仓输出？
  是 → 根据 asset taxonomy 的 include_in_positions 判断
  否 → 保留在 subjects / summary / review，或分流到专门子系统

是否属于场外衍生品？
  是 → 不进入普通 valuation_positions.csv，进入 otc derivative 支线设计
  否 → 继续按普通 asset taxonomy / review 规则处理

是否需要业务友好展示？
  是 → 使用 asset_type_display
  否 → 保留标准会计科目字段即可
```

### 6. 一句话原则

> 官方口径是“科目标准化底座”，不是“业务展示分类替代品”。

---

## 七、场外衍生品提前规划决策

鉴于公司后续实际使用价值较高，本阶段需要提前规划场外衍生品支线。

### 1. 决策结论

科目映射之后，优先启动：

```text
Round 5C：场外衍生品识别与穿透模型设计
Round 5D：场外衍生品最小解析与 review queue
```

场外衍生品不应被视为普通 asset taxonomy 的一个小分类，而应作为独立的 `OTC derivatives sub-system` 设计。

### 2. 决策原因

场内证券持仓体系通常围绕：

```text
证券代码 / 证券名称 / 数量 / 成本 / 市价 / 市值 / 估值增值
```

场外衍生品体系更关心：

```text
合约编号 / 合约类型 / 交易对手方 / 标的资产 / 名义本金 / 方向 / 保证金 / 公允价值 / 浮动盈亏 / 敞口 / Delta / 到期日 / 估值方法
```

二者没有天然一一对应关系，因此不应把场外衍生品强行塞入普通 `valuation_positions.csv`。

### 3. 未来推荐输出结构

后续 Round 5C / 5D 可以设计三张独立输出：

```text
derivative_contracts.csv
derivative_underlying_exposures.csv
derivative_review_items.csv
```

#### `derivative_contracts.csv` 候选字段

```text
source_file
product_id
subject_code
subject_name
account_code_std
account_name_std
derivative_type
contract_name
contract_id
counterparty
trade_direction
notional_amount
market_value
cost
valuation_appreciation
margin_amount
settlement_amount
maturity_date
valuation_method_hint
review_flag
review_category
review_note
```

#### `derivative_underlying_exposures.csv` 候选字段

```text
source_file
product_id
contract_id
underlying_type
underlying_code
underlying_name
underlying_market
underlying_quantity
underlying_price
notional_exposure
delta_adjusted_exposure
long_short
exposure_source
lookthrough_confidence
review_flag
review_note
```

#### `derivative_review_items.csv` 候选字段

```text
source_file
product_id
contract_id
review_category
review_reason
required_supplemental_data
human_decision_needed
```

### 4. 估值表内识别 vs 补充数据穿透

估值表通常只能稳定提供：

```text
科目名称
科目代码
市值 / 估值增值
部分成本或保证金
部分合约名称
```

完整穿透往往需要额外数据源：

```text
券商收益互换台账
OTC 合约清单
交易确认书
收益互换估值明细
收益互换标的清单
保证金明细
对手方日报
```

因此后续目标必须拆成两级：

| 级别 | 目标 | 边界 |
|---|---|---|
| Level 1：估值表内识别 | 识别这是场外衍生品，形成合约候选记录和 review item | 不承诺完整穿透 |
| Level 2：补充数据穿透 | 接入券商 / 对手方明细后，穿透到底层标的和敞口 | 需要新增数据源与口径确认 |

### 5. 与现有 asset taxonomy 的关系

建议保持以下边界：

```text
收益互换 / 场外衍生品
→ asset_type_internal = derivative_swap / otc_derivative
→ include_in_positions = false
→ 进入 derivative_contracts / derivative_review_items
```

不要改成：

```text
收益互换 / 场外衍生品
→ valuation_positions.csv 普通持仓
```

---

## 八、Round 5A 本轮目标

建立官方口径资料资产层，输出以下内容：

1. 官方口径 source files；
2. Markdown 化 reference 文档；
3. 会计科目结构化抽取表；
4. 标准科目字段设计草案；
5. 原始估值表科目到标准会计科目的映射设计草案；
6. 标准科目到 asset taxonomy 的映射设计草案；
7. 场外衍生品相关章节索引和候选字段清单；
8. 人工复核队列；
9. 下一轮 Round 5B / 5C / 5D 建议。

---

## 九、建议新增目录与文件

### 1. Reference source

```text
docs/reference/source/
- 中国基金估值标准2018.docx
- 证券投资基金会计核算操作实务手册-20240530.docx
```

### 2. Markdown reference

```text
docs/reference/markdown/
- 中国基金估值标准2018.md
- 证券投资基金会计核算操作实务手册-20240530.md
```

### 3. Reference docs

```text
docs/reference/
- source_manifest.md
- official_valuation_references.md
- accounting_subjects_extraction_notes.md
- accounting_subjects_mapping_design.md
- official_reference_reusable_assets.md
```

### 4. 场外衍生品设计文档

```text
docs/derivatives/
- otc_derivative_model_design.md
- otc_derivative_reference_fields.md
- otc_derivative_review_rules.md
- otc_derivative_data_requirements.md
```

### 5. Structured reference data

```text
data/reference/
- accounting_subjects_raw.csv
- accounting_subjects_normalized.csv
- accounting_subject_mapping_review_queue.csv
- accounting_subject_to_asset_taxonomy_design.csv
- otc_derivative_subject_patterns.csv
- otc_derivative_field_dictionary.csv
- otc_derivative_review_rules.csv
```

### 6. Task artifacts

```text
tasks/
- round5a_official_reference_assetization_task_package.md
- round5a_official_reference_assetization_execution_report.md
```

### 7. 可选转换脚本

```text
scripts/reference/
- convert_docx_references_to_markdown.py
```

如果新增脚本，必须：

- 输入 `docs/reference/source/*.docx`；
- 输出 `docs/reference/markdown/*.md`；
- 不依赖本地绝对路径；
- 有最小 smoke test 或至少可手工运行说明。

---

## 十、source_manifest.md 要求

`source_manifest.md` 至少说明：

- `source_title`
- `source_version`
- `source_date`
- `original_format`
- `committed_format`
- `local_source_filename`
- `markdown_filename`
- `extraction_method`
- `extraction_date`
- `public_reference_note`
- `OCR_conversion_note`
- `markdown_conversion_note`
- `committed_full_text: yes`
- `usage_boundary`

`usage_boundary` 建议写明：

> 这些文件作为 pricing-parser 项目的公开 reference assets 使用，用于标准会计科目抽取、估值口径理解、场外衍生品识别与后续映射规则设计。这些文件不直接作为 parser runtime 配置，不直接改变现有解析输出契约，不替代人工业务判断。

---

## 十一、Markdown 转换要求

请将两个 docx 转换为 Markdown，目标是便于 AI 阅读、章节定位和人工审阅。

Markdown 转换要求：

1. 保留章节层级；
2. 尽量保留表格结构；
3. 删除明显 OCR 噪音，例如重复页眉、页脚、页码；
4. 不要改写原文含义；
5. 对 OCR 可疑内容加注 `<!-- OCR_REVIEW_NEEDED -->`；
6. 对表格严重变形的章节，在 extraction notes 中记录；
7. 如果转换脚本可复用，可以放在 `scripts/reference/` 下；
8. 如果转换过程是手工完成，请在 execution report 中说明。

---

## 十二、结构化字段建议

### 1. `data/reference/accounting_subjects_raw.csv`

```text
source_title
source_version
source_section
raw_account_code
raw_account_name
raw_account_class
raw_detail_subject
raw_description
raw_text_excerpt_short
extraction_note
needs_review
```

### 2. `data/reference/accounting_subjects_normalized.csv`

```text
account_code_std
account_name_std
account_class_std
account_class_l1
account_class_l2
standard_source
standard_version
source_section
description_short
is_active
normalization_note
review_status
```

### 3. `data/reference/accounting_subject_mapping_review_queue.csv`

```text
raw_subject_code_pattern
raw_subject_name_pattern
proposed_account_code_std
proposed_account_name_std
mapping_method
confidence
reason
needs_human_decision
review_note
```

### 4. `data/reference/accounting_subject_to_asset_taxonomy_design.csv`

```text
account_code_std
account_name_std
proposed_asset_type_internal
proposed_asset_type_display
proposed_asset_class_l1
proposed_asset_class_l2
include_in_positions
mapping_rule_id
mapping_basis
confidence
needs_review
review_note
```

### 5. `data/reference/otc_derivative_subject_patterns.csv`

```text
pattern_id
source_title
source_section
subject_code_pattern
subject_name_pattern
account_code_std
account_name_std
proposed_derivative_type
recognition_basis
confidence
needs_review
review_note
```

### 6. `data/reference/otc_derivative_field_dictionary.csv`

```text
field_name
field_display_name
field_layer
required_for_level1
required_for_level2
description
example_value
source_or_reason
needs_external_data
review_note
```

### 7. `data/reference/otc_derivative_review_rules.csv`

```text
rule_id
rule_name
trigger_condition
review_category
review_reason
required_supplemental_data
severity
human_decision_needed
notes
```

---

## 十三、本轮重点抽取对象

优先抽取证券投资基金估值表中常见科目相关内容，例如：

- 银行存款
- 结算备付金
- 存出保证金
- 交易性股票投资
- 交易性债券投资
- 交易性基金投资
- 交易性资产支持证券投资
- 其他交易性金融资产投资
- 买入返售金融资产
- 应收股利
- 应收利息 / 应计利息相关科目
- 证券清算款
- 应付赎回款
- 应付管理人报酬
- 应付托管费
- 应付销售服务费
- 应交税费
- 其他应付款
- 实收基金
- 未分配利润
- 损益类科目

同时请优先索引场外衍生品相关内容，例如：

- 衍生工具；
- 收益互换；
- 场外期权；
- 远期 / 掉期；
- 保证金；
- 公允价值变动；
- 交易对手方相关信息；
- 名义本金 / 标的 / 到期日 / 估值方法等字段需求。

不要追求一次性覆盖全部官方文件，优先覆盖当前估值表样本中出现过、且后续业务价值较高的科目和场景。

---

## 十四、除标准会计科目外的可复用官方口径资产

本轮除了抽取会计科目，还应建立官方文档中其他可复用内容的索引和候选清单。

### 1. 估值方法口径

例如：

- 活跃市场价格；
- 非活跃市场估值；
- 停牌证券估值；
- 第三方估值；
- 特殊资产估值；
- 公允价值判断。

本轮只需抽取章节索引和候选 review rule，不直接实现。

### 2. 特殊资产 / 特殊事项识别

例如：

- 停牌证券；
- 限售股 / 非流通股；
- 债券估值；
- 基金估值；
- 衍生工具 / 收益互换；
- 应收应付和费用计提。

### 3. 估值表质量校验规则

例如：

- 汇总项与明细项一致性；
- 数量 × 市价 ≈ 市值；
- 数量 × 单位成本 ≈ 成本；
- 市值 - 成本 ≈ 估值增值；
- 应收应付 / 费用科目存在性检查。

### 4. 分类解释与审计追溯字段

后续可以设计：

```text
classification_source
classification_rule_id
classification_basis
classification_confidence
requires_human_review
```

本轮只做设计草案，不接入 parser。

---

## 十五、本轮允许事项

允许：

- 提交两个官方口径 docx 文件；
- 提交转换后的 Markdown 文件；
- 新增 reference source manifest；
- 新增 reference extraction notes；
- 新增 `data/reference` 结构化 CSV；
- 新增人工复核队列；
- 新增官方口径到 asset taxonomy 的映射设计；
- 新增场外衍生品设计文档和 reference CSV；
- 新增转换脚本；
- 新增 Round 5A task package / execution report；
- 更新 README / HANDOFF / status 中关于 reference assets 的简短说明。

---

## 十六、本轮禁止事项

不要做以下事情：

- 不改 parser 核心逻辑；
- 不改 adapters；
- 不新增 adapter；
- 不处理 `PRODUCT_022`；
- 不改 routing；
- 不引入 generic fallback；
- 不刷新 `data_samples/expected/`；
- 不修改 `valuation_subjects.csv` / `valuation_positions.csv` / `review_items.csv` 输出字段；
- 不把官方 reference 文件直接作为 parser runtime 配置；
- 不修改 Round 4 asset taxonomy 口径；
- 不用官方会计科目直接覆盖 `asset_type_display`；
- 不把场外衍生品直接塞入普通 `valuation_positions.csv`；
- 不在本轮承诺完整场外衍生品底层穿透；
- 不把估值方法规则直接转成自动估值判断逻辑。

---

## 十七、验收标准

本轮 PR 通过标准：

1. source docx 文件已纳入 `docs/reference/source/`；
2. Markdown 转换文件已纳入 `docs/reference/markdown/`；
3. `source_manifest.md` 清楚说明来源、版本、转换过程和用途边界；
4. 至少抽取一版 `accounting_subjects_raw.csv`；
5. 至少抽取一版 `accounting_subjects_normalized.csv`；
6. 有 `accounting_subject_mapping_review_queue.csv`；
7. 有 `accounting_subject_to_asset_taxonomy_design.csv`，明确官方科目层和展示分类层的关系；
8. 有场外衍生品相关章节索引 / 字段字典 / review rule 候选清单；
9. 明确说明哪些科目映射需要人工确认；
10. 明确说明 Round 5B 需要新增哪些 runtime 字段；
11. 明确说明 Round 5C / 5D 的场外衍生品支线边界；
12. 不改 `src/` 主解析逻辑；
13. 不刷新 expected baseline；
14. `pytest -q` 保持通过；
15. 提供 execution report。

---

## 十八、建议验证

请至少执行：

```bash
git status --short
git diff --name-only
pytest -q
```

如果新增了转换脚本，请补充：

```bash
python scripts/reference/convert_docx_references_to_markdown.py --help
```

或提供等价 smoke test。

请在 execution report 中说明：

- 是否提交了原始 docx；
- 是否提交了 Markdown；
- Markdown 是否由脚本生成；
- OCR / Markdown 转换中发现了哪些问题；
- 抽取了哪些标准科目；
- 哪些映射需要人工确认；
- 哪些场外衍生品条目 / 字段 / 规则被识别为后续高优先级；
- 为什么本轮不改 parser；
- 为什么本轮不刷新 expected baseline；
- Round 5B 建议新增哪些字段；
- Round 5C / 5D 建议如何启动。

---

## 十九、PR 描述模板

```markdown
## Summary

This PR implements Round 5A official valuation and accounting reference assetization for the valuation parser project.

It adds public official reference documents, Markdown conversions, source manifests, structured accounting subject extraction tables, mapping review queues, and design documents for later standard accounting subject mapping and OTC derivative lookthrough modeling.

## Scope

- Add official reference source files and converted Markdown.
- Add structured accounting subject reference data.
- Add accounting subject to asset taxonomy design notes.
- Add OTC derivative model design notes and reference CSVs.
- Do not change parser runtime behavior.
- Do not refresh expected baselines.

## Non-goals

- No adapter changes.
- No PRODUCT_022 handling.
- No routing changes.
- No parser output field changes.
- No direct replacement of asset_type_display with official accounting subjects.
- No OTC derivative output implementation in this round.

## Validation

- [ ] git status --short checked
- [ ] git diff --name-only reviewed
- [ ] pytest -q passed
- [ ] Markdown conversion reviewed
- [ ] source_manifest completed
- [ ] execution report added
```

---

## 二十、给 Copilot / Codex 的审查提示词

```text
Please review this PR as Round 5A official reference assetization for the pricing-parser / valuation_parser project.

This PR should be reference/data/documentation focused. It should not change parser runtime behavior.

Review focus:

1. Confirm the PR adds official valuation/accounting reference assets, Markdown conversions, source manifest, structured accounting subject CSVs, and design notes.
2. Confirm source_manifest clearly documents source title, version, format, OCR/Markdown conversion, public reference status, and usage boundary.
3. Confirm official accounting subjects are modeled as a standard accounting subject layer, not as a direct replacement for Round 4 asset taxonomy or asset_type_display.
4. Confirm the PR preserves the decision tree:
   subject_code / subject_name
   → account_code_std / account_name_std
   → asset_type_internal
   → asset_type_display
5. Confirm OTC derivative content is treated as a future independent subsystem, not as ordinary valuation_positions.csv rows.
6. Confirm any OTC derivative design outputs remain design/reference assets only and do not change parser runtime behavior.
7. Confirm the PR does not change src/ parser logic, adapters, routing, PRODUCT_022 handling, generic fallback, or expected baselines.
8. Confirm pytest -q still passes.
9. Identify any source/doc formatting, OCR, Markdown, or structured CSV quality problems.
10. Categorize findings as P0 / P1 / P2 and include a final merge recommendation.

Non-goals:
- Do not request full parser integration in this PR.
- Do not request complete OTC derivative lookthrough implementation in this PR.
- Do not request valuation method automation in this PR.
```

---

## 二十一、后续路线建议

本阶段以 Round 5A（reference assetization）作为数据基础，后续三轮依次解决"标谁科目接入"、"场外衍生品模型设计"、"场外衍生品最小实现"三个递进问题。

**执行前提**：Round 5A 的所有 reference CSV 和设计文档必须先行合并，否则 Round 5B / 5C / 5D 缺少可引用的官方口径数据和场外衍生品章节索引，将被迫从头重新抽取，造成重复劳动和口径漂移。

**总体依赖关系**：

```text
Round 5A（参考文件资产化）
    │
    ├── Round 5B（标准科目映射层接入 parser）
    │       依赖：accounting_subjects_normalized.csv, accounting_subject_mapping_review_queue.csv
    │
    └── Round 5C（场外衍生品模型设计）
             │
             └── Round 5D（场外衍生品最小解析与 review queue）
                     依赖：otc_derivative_subject_patterns.csv, otc_derivative_field_dictionary.csv
             
Round 5C 和 Round 5D 不依赖 Round 5B 完成，可与 Round 5B 并行或交错执行。
```

---

### Round 5B：标准会计科目映射层接入 parser 输出

#### 5B.1 本轮定位

Round 5B 是 Round 5A 结构化抽取结果**首次进入 parser runtime 输出**的衔接轮。目标是在不改变现有输出契约的前提下，在 `valuation_subjects.csv` 中新增标准会计科目字段，完成"原始科目 → 标准会计科目"的第一层映射接入。

#### 5B.2 目标

1. 在 `valuation_subjects.csv` 中新增标准会计科目字段。
2. 基于 Round 5A 产出的 `accounting_subjects_normalized.csv` 实现 `subject_code / subject_name → account_code_std / account_name_std` 的静态映射。
3. 产出映射覆盖率统计和 mapping review queue 更新。

#### 5B.3 新增字段

在 `valuation_subjects.csv` 中新增以下字段：

```text
account_code_std         # 标准会计科目代码，如 "1102"
account_name_std         # 标准会计科目名称，如 "交易性股票投资"
account_class_std        # 标准会计科目分类，如 "股票投资"
account_source           # 映射来源，如 "中国基金估值标准2018" / "会计核算操作实务手册"
account_mapping_method   # 映射方式：exact_match / pattern_match / manual / unreviewed
account_mapping_confidence  # 置信度：high / medium / low / unreviewed
account_mapping_note     # 映射备注，记录例外情况或需要人工确认的内容
```

#### 5B.4 映射规则优先级

```text
1. subject_code 精确匹配 → 直接指派 account_code_std / account_name_std
2. subject_name 关键词匹配 → 根据 Round 5A mapping_review_queue 指派
3. 复合规则（code + name 联合）→ 适用于模糊科目
4. 无法匹配 → account_code_std = "UNMAPPED", account_mapping_method = "unmapped"
   进入 accounting_subject_mapping_review_queue 待人工确认
```

#### 5B.5 初期范围限制

- **只改 `valuation_subjects.csv`**，不改 `valuation_positions.csv` 和 `review_items.csv`。
- 不在本轮引入新 adapter、不改 routing、不改 core parser。
- 不在本轮将标准科目传播到 `asset_type_display`；展示层口径维持 Round 4 状态。
- 如果会计科目映射导致某科目的 `include_in_positions` 逻辑需要调整，记录为 Round 5B follow-up，不在本轮执行。

> **设计理由**：`valuation_subjects.csv` 是 parser 的第一层输出（科目级明细），在此新增标准科目字段对下游 `valuation_positions.csv`（持仓合并）、`review_items.csv`（复核标记）没有连锁影响，是风险最小的接入点。

#### 5B.6 输出产物

```text
src/valuation_parser/
  └── mapping/
      └── accounting_subject_mapping.py    # 新增：标准科目映射逻辑

data/reference/
  └── accounting_subject_mapping_review_queue.csv   # 更新：新增本轮新增的 unmapped 条目

tasks/
  └── round5b_accounting_subject_mapping_task_package.md       # 任务书
  └── round5b_accounting_subject_mapping_execution_report.md   # 执行报告
```

#### 5B.7 映射代码设计要求

1. 映射逻辑与业务展示分类（`asset_type_internal` / `asset_type_display`）解耦：`accounting_subject_mapping.py` 只做 `subject → account_code_std` 的映射，不涉及 `asset_type_display` 的改写。
2. 映射配置来源应为 Round 5A 产出的结构化 CSV（`accounting_subjects_normalized.csv`），而不是硬编码在 Python 字典中。
3. 支持 mapping review queue 的导出：每次运行后输出未覆盖科目清单，供人工复核。
4. 映射函数应保持纯函数（pure function）风格：输入 `subject_code, subject_name`，输出映射结果 + 置信度，不依赖全局状态。
5. 映射结果应可追溯：记录 `account_source`（来源文档）、`account_mapping_method`（映射方式），便于审计。

#### 5B.8 测试要求

- 至少覆盖当前 valuation_subjects.csv 中所有已知 subject_code 的映射。
- 对合并前已知无映射的科目（如衍生工具、收益互换类），验证其 `account_mapping_method = "unmapped"` 且进入 review queue。
- 不新增对环境（如 docx 文件存在性）的依赖。
- `pytest -q` 保持通过。

#### 5B.9 验收标准

1. `valuation_subjects.csv` 新增标准会计科目字段。
2. 每个 subject 均有 `account_mapping_method`（至少为 `unmapped`）。
3. 覆盖率统计可输出。
4. mapping review queue 可导出。
5. 不修改 `valuation_positions.csv` / `review_items.csv` 输出字段。
6. 不新增 adapter。
7. `pytest -q` 通过。
8. 提供 execution report。

#### 5B.10 禁止事项

- 不改 `asset_type_display` 口径。
- 不改 `include_in_positions` 逻辑。
- 不改 adapter / routing / parser core。
- 不刷新 expected baseline。
- 不引入场外衍生品解析逻辑。

---

### Round 5C：场外衍生品识别与穿透模型设计

#### 5C.1 本轮定位

Round 5C 是**纯设计轮**，不产生代码变更。目标是在 Round 5A 抽取的场外衍生品章节索引和候选字段基础上，完成场外衍生品独立子系统的完整数据模型设计、补充数据需求边界梳理和 review 规则设计。

#### 5C.2 目标

1. 完成 `derivative_contracts` 数据模型终稿设计。
2. 完成 `derivative_underlying_exposures` 数据模型终稿设计。
3. 完成 `derivative_review_items` 数据模型终稿设计。
4. 明确 Level 1（估值表内识别）vs Level 2（补充数据穿透）的分界线和数据需求清单。
5. 完成 OTC derivative review rules 设计。
6. 明确与现有 `valuation_subjects.csv` / `valuation_positions.csv` / `review_items.csv` 的分流边界。

#### 5C.3 设计输出

```text
docs/derivatives/
  ├── otc_derivative_model_design.md          # 总体数据模型设计文档
  ├── otc_derivative_reference_fields.md       # 候选字段完整字典
  ├── otc_derivative_review_rules.md           # review rule 设计
  └── otc_derivative_data_requirements.md      # 补充数据需求清单和 Level 1 / Level 2 分界

data/reference/
  ├── otc_derivative_subject_patterns.csv      # 更新：补充设计轮新增的 pattern
  ├── otc_derivative_field_dictionary.csv       # 更新：字段字典终稿
  └── otc_derivative_review_rules.csv           # 更新：review rule 终稿
```

#### 5C.4 数据模型设计要点

##### derivative_contracts

- 核心标识：`contract_id`（合约唯一标识，估值表无法提供时标记为 `UNKNOWN` 并进入 review）
- 合约分类：`derivative_type` 使用枚举，至少覆盖 `swap`、`otc_option`、`forward`、`futures`、`other`
- 多源字段分组：
  - **估值表可稳定提供**：`subject_code`, `subject_name`, `market_value`, `cost`, `valuation_appreciation`, `margin_amount`（部分）
  - **估值表可能提供**：`contract_name`, `counterparty`（部分）, `maturity_date`（部分）
  - **需补充数据源**：`notional_amount`, `trade_direction`, `settlement_amount`, `valuation_method_hint`, `underlying details`
- `valuation_method_hint` 应使用自由文本记录估值表或补充数据中描述的估值方法关键词，不承诺标准化。

##### derivative_underlying_exposures

- 每条合约可对应多条底层标的（如收益互换挂钩多个个股）。
- `exposure_source` 区分 `calculated_from_contract`（从合约信息推算）、`provided_by_counterparty`（对手方明细提供）、`estimated`（估算）。
- `lookthrough_confidence` 使用 `high / medium / low / unknown` 四级，`unknown` 必须进入 review。
- `delta_adjusted_exposure` 为可选字段，仅在 Level 2 有 Delta 值时填充。

##### derivative_review_items

- 继承现有 `review_items.csv` 的 `review_category` 分类体系，但增加 `derivative_specific` 类别。
- `required_supplemental_data` 字段记录需要人工或外部补充的数据类型。
- `human_decision_needed` 使用 `yes / no`，`yes` 表示必须人工确认才能推进后续处理。

#### 5C.5 Level 1 / Level 2 分界设计

| 维度 | Level 1：估值表内识别 | Level 2：补充数据穿透 |
|---|---|---|
| 数据源 | 估值表科目 | 券商收益互换台账 / OTC 合约清单 / 交易确认书 |
| 合约识别 | 科目名称 + subject code pattern | 合约 ID + 合同确认 |
| 承诺字段 | `subject_code`, `subject_name`, `market_value`, `cost`，部分 `margin` | 全部候选字段 |
| 底层标的 | 穿透为 UNKNOWN 或 limited | 完整标的 + 名义敞口 + Delta 调整敞口 |
| 对手方 | 部分可从科目名推断 | 明确记录 |
| 产出 | `derivative_contracts`（部分字段填充）+ review items | `derivative_contracts` + `derivative_underlying_exposures`（完整） |
| 触发条件 | 估值表 OTCDerivative adapter | 外部补充数据接入 |

#### 5C.6 与现有 asset taxonomy 的分流边界

重申 Round 5A 已确立的原则：

```text
收益互换 / 场外衍生品
→ asset_type_internal = derivative_swap / otc_derivative
→ include_in_positions = false
→ 不进 valuation_positions.csv
→ 进入 derivative_contracts + derivative_review_items
→ 估值表内识别为 Level 1，标注补充数据需求
```

设计文档必须明确：**场外衍生品数据模型是独立子系统，不是 valuation_positions.csv 的扩展**。

#### 5C.7 补充数据需求清单要求

`otc_derivative_data_requirements.md` 必须包含：

1. 每种衍生品类型所需的最低字段集（Level 1 minimum viable fields）。
2. 每种衍生品类型的完整字段集（Level 2 full fields）。
3. 外部数据源的候选渠道（如券商日报、柜台系统导出等）。
4. 数据口径确认建议（如估值表 vs 券商台账口径差异处理建议）。
5. 字段缺失时的默认行为和 review flag 规则。

#### 5C.8 验收标准

1. `docs/derivatives/` 下四个设计文档齐全。
2. `data/reference/` 下三个场外衍生品 CSV 达到终稿状态。
3. Level 1 / Level 2 分界清晰，字段归属明确。
4. 补充数据需求清单完整。
5. 不产生任何 `src/` 变更。
6. 不产生 `data_samples/expected/` 变更。
7. 不修改现有 parser 配置。
8. 提供 design review report（可作为 execution report 的一部分）。

#### 5C.9 禁止事项

- 不写 parser runtime 代码。
- 不修改现有 CSV 输出字段。
- 不刷新 expected baseline。
- 不新增 adapter。
- 不承诺 Level 2 数据源接入。

---

### Round 5D：场外衍生品最小解析与 review queue

#### 5D.1 本轮定位

Round 5D 是场外衍生品子系统的**最小可行实现轮**。基于 Round 5C 完成的数据模型设计，在 parser 中增加场外衍生品识别逻辑和分流输出。

**核心约束**：只做 Level 1（估值表内识别），不做 Level 2（补充数据穿透）。Level 2 列为后续轮次，不在本任务书中规划。

#### 5D.2 目标

1. 从估值表原始科目中识别场外衍生品候选记录。
2. 输出 `derivative_contracts.csv`（Level 1 字段子集）。
3. 输出 `derivative_review_items.csv`（标记缺失字段和 review 原因）。
4. `valuation_positions.csv` 中排除场外衍生品相关科目（继承 Round 4 的 `include_in_positions = false` 设定）。
5. 不输出 `derivative_underlying_exposures.csv`（Level 2，本轮不做）。

#### 5D.3 识别策略

基于 Round 5A 产出的 `otc_derivative_subject_patterns.csv` 和 Round 5C 设计的识别规则：

```text
1. subject_code 匹配预设 pattern（如 "12xx"、"13xx" 等衍生工具代码段）
2. subject_name 关键词匹配（如 "收益互换"、"场外期权"、"远期"、"掉期"、"衍生工具"）
3. asset_type_internal == "derivative_swap" / "otc_derivative"（Round 4 taxonomy 已有）
4. 匹配成功 → 分流到 derivative_contracts 输出管道
5. 匹配失败但疑似衍生品 → 进入 derivative_review_items
```

#### 5D.4 新增输出文件

```text
output_<timestamp>/
  ├── derivative_contracts.csv          # 新增：衍生品合约记录（Level 1 字段子集）
  ├── derivative_review_items.csv       # 新增：衍生品复核队列
  └── ...（现有 valuation_subjects.csv / valuation_positions.csv / review_items.csv 不变）
```

#### 5D.5 derivative_contracts.csv 初始字段（Level 1 子集）

```text
source_file
product_id
subject_code
subject_name
account_code_std           # Round 5B 已对接
account_name_std           # Round 5B 已对接
derivative_type            # 从 subject pattern 推断
contract_name              # 从估值表科目名或补充字段提取，不可得时留空
contract_id                # 不可得时填 UNKNOWN，进入 review
counterparty               # 从科目名推断，不可得时留空
trade_direction            # 从科目名或市值正负推断，不可得时进入 review
notional_amount            # Level 1 通常不可得，留空并进入 review
market_value               # 直接从原始数据传递
cost                       # 直接从原始数据传递
valuation_appreciation     # 直接从原始数据传递
margin_amount              # 部分估值表有保证金字段
settlement_amount          # Level 1 通常不可得
maturity_date              # Level 1 通常不可得
valuation_method_hint      # 从 subject name 或 account mapping 传递
review_flag                # 是否被 review 标记
review_category            # 衍生品 review 类别
review_note                # 缺失字段说明
```

**缺失字段处理原则**：`notional_amount`、`contract_id`、`counterparty`、`trade_direction`、`maturity_date` 在 Level 1 不可得时保留为空，同时在 `derivative_review_items.csv` 中记录缺失原因和所需的补充数据类型。不要在 Level 1 中编造或估算这些字段值。

#### 5D.6 代码结构建议

```text
src/valuation_parser/
  ├── ... 现有文件不变
  └── derivatives/
      ├── __init__.py
      ├── derivative_identifier.py      # 新增：场外衍生品识别逻辑
      ├── derivative_contract_builder.py # 新增：derivative_contracts.csv 构建
      └── derivative_review_builder.py   # 新增：derivative_review_items.csv 构建

config/
  └── derivative_patterns.yaml           # 新增：衍生品识别 pattern 配置（可选，也可沿用 otc_derivative_subject_patterns.csv）
```

#### 5D.7 与 parser 主流程的集成

```text
现有流程：
  raw subjects
    → routing → adapter → valuation_subjects.csv / positions / review_items

Round 5D 新增分流：
  raw subjects
    → routing → adapter
        → 非衍生品 → 现有管道（subjects / positions / review_items）
        → 衍生品   → derivative_identifier
            → derivative_contracts.csv + derivative_review_items.csv
```

- 识别/分流逻辑应在 adapter 层之后、最终输出之前插入。
- 不修改现有 adapter 的输出行为。
- `valuation_subjects.csv` 中仍保留衍生品科目（供审计追溯），但 `include_in_positions = false` 确保不进 `valuation_positions.csv`。

#### 5D.8 测试要求

- 至少覆盖已出现的收益互换 / 衍生工具 subject code pattern。
- 验证 `derivative_contracts.csv` 中合约记录与 `valuation_subjects.csv` 中衍生品科目一一对应。
- 验证缺失字段正确进入 `derivative_review_items.csv`。
- 验证 `valuation_positions.csv` 不包含衍生品科目。
- `pytest -q` 保持通过。

#### 5D.9 验收标准

1. `derivative_contracts.csv` 正确输出来源于估值表的衍生品合约记录。
2. `derivative_review_items.csv` 正确标记缺失字段和补充数据需求。
3. `valuation_positions.csv` 不包含场外衍生品科目。
4. 识别规则覆盖当前估值表样本中所有已知衍生品科目。
5. 不破坏现有 valuation_subjects.csv / valuation_positions.csv / review_items.csv 输出。
6. `pytest -q` 通过。
7. 提供 execution report 并明确记录 Level 1 与 Level 2 的边界。

#### 5D.10 禁止事项

- 不做 `derivative_underlying_exposures.csv` 输出（Level 2）。
- 不接入外部补充数据源。
- 不编造不可得的字段值。
- 不改 adapter。
- 不改 routing。
- 不刷新 expected baseline（因 `derivative_contracts.csv` / `derivative_review_items.csv` 是新增输出文件，不存在已有 baseline，不影响现有 baseline）。
- 不修改现有 `valuation_positions.csv` 的输出字段定义。

---

### 执行优先级建议

| 优先级 | 轮次 | 依赖 | 建议启动时机 |
|---|---|---|---|
| P0 | Round 5B | Round 5A 结构化数据 | Round 5A 合并后立即启动 |
| P1 | Round 5C | Round 5A 衍生品章节索引 | 可与 Round 5B 并行 |
| P2 | Round 5D | Round 5C 数据模型设计 | Round 5C 设计评审通过后启动 |

### Round 5B / 5C / 5D 之间的集成风险

1. **字段口径漂移**：Round 5B 的 `account_code_std` 字段如果在 Round 5C / 5D 完成后发现需要调整，会造成文档和代码的双向变更。建议 Round 5B 的 `account_code_std` 第一次发布时标记为 `alpha`，Round 5C 设计评审后确认终稿。

2. **衍生品识别与标准科目映射的重叠**：部分衍生品科目（如 `衍生工具`）既需要 Round 5B 的标准科目映射（`account_code_std = UNMAPPED`），也需要 Round 5D 的衍生品识别分流。两个管道不应相互阻塞：Round 5B 即使将衍生品科目映射为 `UNMAPPED`，也不影响 Round 5D 单独识别和分流。

3. **整体输出契约稳定性**：在 Round 5D 完成前，`valuation_subjects.csv` 和 `valuation_positions.csv` 的输出字段不应再发生非兼容变更。如果 Round 5B 之后发现需要调整输出契约建议推迟到 Round 5D 之后的集中清理轮。

---

## 二十二、一句话任务边界

本轮不是“用官方会计科目重写 parser”，也不是“直接完成场外衍生品穿透”。

本轮是：

> 把官方估值与会计口径转化为可读、可审、可引用的 reference assets，并提前建立标准科目层与场外衍生品支线的设计边界。
