# Task Package: Round 5A Official Reference Assetization

> This task package is the executable Round 5A slice for `pricing_parser / valuation_parser`. It narrows the upstream planning document to the minimum bounded scope needed for this round.

## Task Identification

- Name: Round 5A / Official Reference Assetization
- Phase: Round 5 reference and design preparation
- Submitted By: Drafter
- Date: 2026-05-28
- Upstream Planning Source: `任务书集合/pricing_parser第四轮审查结论摘要暨第五轮任务书.md`

## 1. Background

Round 4 has already closed the asset taxonomy layer and its accepted baseline. The current parser can parse valuation tables, route through mapping and adapters, export controlled outputs, and keep asset taxonomy fields stable in `subjects / positions / review / summary` scope.

What is still missing is an upstream reference layer for official valuation and accounting guidance. Round 5A does not integrate that layer into parser runtime. It only brings the public official reference materials into the repository as reusable assets, converts them into reviewable formats, extracts a first structured accounting-subject reference set, and records the design boundary between:

- raw valuation subjects
- standard accounting subjects
- internal asset taxonomy
- business-facing display labels

This round also records OTC derivative design inputs as reference assets only, so later rounds can work from a clear boundary instead of overloading ordinary security-position outputs.

## 2. Goal

本轮目标是把公开的官方估值与会计口径资料资产化，形成一套可读、可审、可引用的 reference assets，并为后续 Round 5B 标准会计科目接入设计、Round 5C/5D 场外衍生品支线设计提供结构化输入。

完成后应实现以下高层结果：

- 仓库内存在可追溯的官方 reference source 与 Markdown 转换件。
- 仓库内存在首版结构化标准会计科目抽取表与人工复核队列。
- 文档中明确 standard accounting subject layer 不直接替代 Round 4 asset taxonomy / `asset_type_display`。
- OTC derivative 相关内容被记录为未来独立子系统的参考资产，而不是普通 `valuation_positions.csv` 实现项。

## 3. Scope

本轮只允许做 reference/data/documentation 资产化，不改 parser runtime 行为。

### Allowed Changes

- 提交两份公开官方参考文件到仓库中的 reference source 目录。
- 将上述参考文件转换为适合 AI 阅读与人工审阅的 Markdown 版本。
- 新增 `source_manifest`，记录来源、版本、格式、转换方式、公开属性与使用边界。
- 新增首版结构化 CSV，用于抽取标准会计科目、记录标准化结果、记录映射 review queue、记录标准科目到 asset taxonomy 的设计草案。
- 新增 OTC derivative 相关的章节索引、字段字典、review rule 候选清单与设计说明文档。
- 新增或补充与本轮直接相关的简短文档说明，例如 `README.md`、`docs/HANDOFF.md`、`docs/status.md` 中的 reference-asset 说明。
- 新增本轮 execution report。
- 如确有必要，可新增一个最小可复用的 reference conversion script，但其职责只限 source-to-markdown 转换，不接入 parser runtime。

### Bounded Execution Focus

- 优先保证 reference assets 可追溯、可复核、可复用。
- 优先覆盖当前估值表样本中高频且后续价值高的会计科目与场外衍生品相关章节。
- 优先把字段分层和系统边界写清楚，而不是追求一次性完成完整官方文件全量抽取。

## 4. Explicit Non-goals

本轮明确不做以下事项：

- 不修改 `src/` 下 parser 核心逻辑。
- 不修改 adapters。
- 不新增 adapter。
- 不处理 `PRODUCT_022`。
- 不修改 routing。
- 不引入 generic fallback。
- 不刷新 `data_samples/expected/` baseline。
- 不修改 `valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv` 现有 runtime 输出字段。
- 不把官方参考文件直接作为 parser runtime 配置。
- 不用官方会计科目直接替换 `asset_type_internal`、`asset_type_display` 或 Round 4 taxonomy 口径。
- 不把 OTC derivatives 直接实现为普通 `valuation_positions.csv` 持仓行。
- 不承诺完整 OTC lookthrough。
- 不把估值方法口径直接落成自动估值判断逻辑。
- 不把 Round 5A 扩展成 Round 5B / 5C / 5D 的实现轮。

## 5. Target Files

### Primary Reference Assets

- `docs/reference/source/`
- `docs/reference/markdown/`
- `docs/reference/source_manifest.md`
- `docs/reference/official_valuation_references.md`
- `docs/reference/accounting_subjects_extraction_notes.md`
- `docs/reference/accounting_subjects_mapping_design.md`
- `docs/reference/official_reference_reusable_assets.md`

### OTC Derivative Design Assets

- `docs/derivatives/otc_derivative_model_design.md`
- `docs/derivatives/otc_derivative_reference_fields.md`
- `docs/derivatives/otc_derivative_review_rules.md`
- `docs/derivatives/otc_derivative_data_requirements.md`

### Structured Reference Data

- `data/reference/accounting_subjects_raw.csv`
- `data/reference/accounting_subjects_normalized.csv`
- `data/reference/accounting_subject_mapping_review_queue.csv`
- `data/reference/accounting_subject_to_asset_taxonomy_design.csv`
- `data/reference/otc_derivative_subject_patterns.csv`
- `data/reference/otc_derivative_field_dictionary.csv`
- `data/reference/otc_derivative_review_rules.csv`

### Optional Utility Script

- `scripts/reference/` 下与 docx-to-markdown 转换直接相关的最小脚本或说明

### Project Documentation

- `README.md`
- `docs/HANDOFF.md`
- `docs/status.md`

### Process Files

- `tasks/round5a_official_reference_assetization_task_package.md`
- `tasks/round5a_official_reference_assetization_execution_report.md`

## 6. Acceptance Criteria

本轮至少需要满足以下可验证标准：

1. `docs/reference/source/` 下已纳入两份官方 reference source 文件，且其来源与版本可在 manifest 中追溯。
2. `docs/reference/markdown/` 下已存在对应 Markdown 转换件，能够保留主要章节层级，并对明显 OCR 可疑内容做标注或在 extraction notes 中记录。
3. `docs/reference/source_manifest.md` 明确记录来源标题、版本、原始格式、提交格式、转换方式、转换日期、公开参考说明与使用边界。
4. `data/reference/accounting_subjects_raw.csv` 已抽取出一版原始标准会计科目候选记录。
5. `data/reference/accounting_subjects_normalized.csv` 已形成一版标准化会计科目结果。
6. `data/reference/accounting_subject_mapping_review_queue.csv` 已记录需要人工确认的映射候选，而不是强行完成全部归类。
7. `data/reference/accounting_subject_to_asset_taxonomy_design.csv` 已明确标准科目层与 asset taxonomy 层之间的设计关系。
8. OTC derivative 相关 reference CSV 和设计文档已说明未来输出对象、字段候选、review 规则候选与额外数据需求边界。
9. 文档中已明确保留字段分层原则：
   - `subject_code / subject_name`
   - `account_code_std / account_name_std`
   - `asset_type_internal`
   - `asset_type_display`
10. 文档中已明确说明官方口径是标准化底座，不直接替代 Round 4 展示分类。
11. 文档中已明确说明 OTC derivative 在后续轮次应作为独立子系统推进，而不是普通 `valuation_positions.csv` 扩展。
12. 本轮改动未进入 `src/` 主解析逻辑、adapter、routing、`PRODUCT_022`、generic fallback 或 expected baseline refresh。
13. `pytest -q` 通过；若 reference-only 变更未引发代码失败，也必须在 execution report 中记录验证结果。
14. 已生成 `tasks/round5a_official_reference_assetization_execution_report.md`，说明本轮做了什么、没做什么、如何验证、还有哪些待后续轮次处理。

## 7. Validation Requirements

本轮至少执行以下验证：

1. `git status --short`
2. `git diff --name-only`
3. `pytest -q`

如果新增了转换脚本，还应额外执行以下之一：

1. `python scripts/reference/<script_name>.py --help`
2. 与该脚本等价的最小 smoke test

验证结果必须写入 execution report，并区分：

- 通过的检查
- 环境阻塞导致未完成的检查
- 真正的失败项

## 8. Execution Report Requirements

执行完成后必须生成：`tasks/round5a_official_reference_assetization_execution_report.md`。

execution report 至少应包含以下章节：

1. `Scope Restatement`
   - 复述本轮只做 official reference assetization，不改 parser runtime。
2. `Files Changed`
   - 列出新增或修改文件及作用。
3. `Reference Assets Added`
   - 说明 source、markdown、manifest、structured CSV、design docs 的完成情况。
4. `Validation`
   - 列出命令、结果、失败原因和环境阻塞。
5. `Boundaries Kept`
   - 明确记录本轮没有改 parser、adapter、routing、baseline、PRODUCT_022。
6. `Open Review Items`
   - 记录仍需人工确认的标准科目映射、OCR 问题或 derivative 设计待确认点。
7. `Next Round Recommendations`
   - 分别给出 Round 5B 与 Round 5C/5D 的最小启动建议。
8. `Commit Summary`
   - 记录 commit hash 和 message；若未提交，明确写明未提交状态。

## Constraints

- 实施前必须先复述本轮目标、边界、明确不做事项和预计修改文件。
- 实施侧必须保持 bounded execution，只在授权目录和授权资产范围内施工。
- 发现范围外问题时，只记录到 execution report，不顺手扩写为本轮实现。
- 若更新 `docs/HANDOFF.md`，应遵守该文件作为 handoff 单一主文档的原则，并做 section-aware 增量更新。

## Supporting Context

- `任务书集合/pricing_parser第四轮审查结论摘要暨第五轮任务书.md`
- `tasks/round4_asset_taxonomy_task_package.md`
- `docs/HANDOFF.md`
- `docs/status.md`
- `README.md`

## Expected Output

- A bounded Round 5A reference-assetization change set.
- A structured execution report.
- No parser runtime behavior change.