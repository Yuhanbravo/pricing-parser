# valuation-parser

估值表解析器项目脚手架，按“路由层 + 公共解析层 + 托管机构适配层”组织。当前已完成 Round 4 资产术语收敛：基于 `data_samples/raw/` 的全量 11 份受控样表重新生成并校验了受控输出与 `data_samples/expected/`，覆盖 mapping-driven routing、8 个已命中 adapter key、标准化 CSV/Markdown/Excel 导出、`3102*` 衍生工具科目 review 规则，以及统一的 taxonomy 展示口径；默认严格路由口径下仍保留 1 个未命中 mapping 的失败样本。

## 工作区边界

推荐使用同级目录多仓库结构：

```text
D:\intern_workspace\
├─ valuation-parser\
└─ ai_skill_hub\
```

- `valuation-parser` 是当前项目仓库，只负责项目代码、测试、配置和项目文档。
- `ai_skill_hub` 应作为独立参考仓库，通过 Git bundle 导入并单独维护。
- 不要把 `ai_skill_hub` 作为普通文件夹放进本仓库，也不要把 bundle 文件直接提交到本仓库。

## 环境约束

- 一个项目一个环境，不要长期在 `base` 环境开发。
- 本项目建议在独立 Python 环境中执行 `python -m pip install -e .[dev]`。
- 开始新一轮较大 AI 改动前，先确认环境正确，再做 Git checkpoint。

## 当前能力

- 从文件名、Sheet 名、表头预览中提取 `product_id` 与 `association_code`
- 读取 `.csv/.xlsx` 映射表，并兼容当前仓库中的紧凑版映射 CSV
- 支持 `.xls/.xlsx` 估值表输入
- 输出 `routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv`、`parse_summary.md`，以及按输入日期自动命名的 Excel 工作簿 `估值表解析_output_<date>.xlsx`
- `parse_summary.md` 当前会按 taxonomy 展示口径汇总已支持 / 未支持资产类型，并追加 `Asset Type Coverage` 统计表，便于快速判断样本覆盖面与剩余缺口
- `valuation_subjects.csv` 与 `valuation_positions.csv` 当前导出包含 trace 字段：`source_file`、`product_id`、`association_code`、`custodian_id`、`custodian_name`、`adapter_key`、`route_source`
- `valuation_subjects.csv`、`valuation_positions.csv` 与 `review_items.csv` 当前统一导出 taxonomy 字段：`asset_type_internal`、`asset_type_display`、`asset_class_l1`、`asset_class_l2`；subjects / review items 额外保留 `review_category`
- `routing_results.csv` 中的 `custodian_name_chinese` 会收敛为标准化名称，避免同一托管机构以简称和全称混用
- `valuation_positions.csv` 中的 `suspension_info` 会将 `【正常交易】` 等包裹格式收敛为纯文本 `正常交易`
- 当前注册并在受控路径中验证命中的 adapter key：`citics`、`cmsc`、`csc`、`greatwall`、`gtja`、`guosen`、`orient`、`xyzc`
- 最新受控全量运行结果：11 个文件、10 次成功路由、1 次路由失败、1022 条科目、182 条持仓、508 条 review-flagged subjects、238 条 review items、0 个 normalization issues；权威 strict-default baseline 维护在 `data_samples/expected/`
- 当前支持的 taxonomy 展示类型为：`A股股票`、`场内基金/ETF`、`存托凭证`、`港股`、`科创板股票`；收益互换、保证金、清算款、负债等非证券持仓仅保留在 subjects / review / summary 口径中，不进入 `valuation_positions.csv`
- 对于 `PRODUCT_022` 这类能提取身份但未命中有效 mapping 的文件，默认会保留 `failed` 路由结果；只有显式传入 `--allow-generic-fallback` 时才允许 `generic` 兜底解析
- 共享 review 逻辑已覆盖 `3102*` 衍生工具科目，命中后会进入 `review_items.csv`
- `valuation_positions.csv` 与 `valuation_subjects.csv` 中的 `review_flag` 使用 `1` 标记所有需要人工复核的记录，未命中时保持空白；`review_note` 与 `review_items.csv` 保留具体原因，`review_flag` 本身只承担“是否需要人工复核”的二值标记
- `data_samples/expected/` 当前已刷新并纳入 Round 4 acceptance baseline：`routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv`、`parse_summary.md`，以及 workbook-content baseline
- 测试已覆盖身份提取、映射加载、路由、adapter 样表、基于 `data_samples/raw/` 全量样表的 smoke，以及 review-item 回归

当前已验证的真实样表：

- `证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx` -> `greatwall`
- `20250327_PRODUCT_002_证券投资基金估值表.xls` 与 `20250327_PRODUCT_002_证券投资基金估值表.csv` -> `xyzc`
- `2025-03-27_PRODUCT_001估值表.xlsx` -> `guosen`
- `PRODUCT_008委托资产资产估值表20250327.xls` -> `cmsc`
- `估值表_PRODUCT_021_20250327.xls` -> `csc`
- `估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx` 默认未路由；仅在显式启用 `--allow-generic-fallback` 时走 `generic` fallback
- `PRODUCT_006_资产估值表_20250327.xls`、`PRODUCT_010_证券投资基金估值表_2025-03-27.xls`、`PRODUCT_012_估值表_20250327.xls` 已在批量管线测试中分别覆盖 `citics`、`orient`、`gtja`

Round 4 资产术语口径补充：

- ETF / 场内基金统一归为 `fund_exchange_traded` / `场内基金/ETF`，属于基金类，不按权益类落地。
- 收益互换统一归为 `derivative_swap` / `收益互换`，进入 review 口径，不进入 `valuation_positions.csv`。
- 现金及存款、保证金、证券清算款、应付款项、应交税费等科目保留在 subjects / summary 口径中，不作为证券持仓导出。
- `PRODUCT_022` 已明确不属于本轮处理范围，本轮不补 mapping、不新增 adapter，也不为消除单个 routing failure 改写 strict-default 契约。

## 项目结构

```text
pricing_parser/
├─ AGENTS.md
├─ README.md
├─ pyproject.toml
├─ .github/
│  └─ copilot-instructions.md
├─ config/
│  ├─ asset_taxonomy.yaml
│  ├─ adapters/
│  │  └─ *.yaml
│  └─ code_rules.yaml
├─ data_samples/
│  ├─ raw/
│  ├─ mapping/
│  └─ expected/
├─ docs/
├─ src/
│  └─ valuation_parser/
│     ├─ adapter_registry.py
│     ├─ cli.py
│     ├─ exporters.py
│     ├─ mapping_loader.py
│     ├─ models.py
│     ├─ normalizers.py
│     ├─ pipeline.py
│     ├─ product_identity.py
│     ├─ routing.py
│     ├─ taxonomy.py
│     └─ adapters/
├─ tasks/
│  └─ README.md
└─ tests/
```

## Git 工作流

开始开发前的最小流程：

```powershell
git status
git add .
git commit -m "chore: checkpoint before parser changes"
```

如果当前没有可提交内容，至少先执行 `git status`，确认工作区干净。

完成一个小阶段后，按项目约定提交清晰 commit，例如：

```text
feat(parser): add second custodian adapter
docs(status): refresh current parser boundaries and next steps
refactor(normalizer): centralize asset type inference
```

项目阶段性里程碑可以使用 `Phase 1 / 2 / 3`，但普通施工步骤不要写 Phase。

## PR 协作约定

PR 流程约定以本节为准；`AGENTS.md` 与 `.github/copilot-instructions.md` 只做薄引用，不另写第二套规则。

本地 / CI 默认验证命令：

- 涉及源码、配置、测试或 baseline 的改动：运行 `python -m pytest`。
- 仅文档改动：至少运行 `git diff --check`；源码测试可标记为 `not_run`，并说明原因是只改文档。

分支命名固定大类，topic 小类用短横线小写描述工作主题：

- `docs/<topic>`：文档、状态、handoff、README、任务说明。
- `feat/<topic>`：新增解析能力、adapter、导出能力、可见功能。
- `fix/<topic>`：行为修复、回归修复、数据口径修正。
- `review/<topic>`：review round、验收闭环、证据链整理。
- `backup/<topic>`：本地保护性备份分支，仅用于迁移或纠偏前 checkpoint。

历史分支形态继续兼容，例如 `feature/round4-asset-taxonomy`、`feature/round5a-official-reference-assetization`、`review/pr-3-round5a`、`review/round3-evidence-chain-closure`、`backup/local-before-pr3-gate-*`；新分支优先使用上面的固定大类，不要求重命名历史分支。

topic 小类可以后续扩展；当前建议使用类似 `docs/pr-workflow-minimal-convention`、`review/round5a-status-refresh` 的短主题。round / PR 类工作可以继续使用 `round5a-*` 或 `pr-3-*`，保持与历史审阅节奏兼容。

PR 描述至少说明：

- 改了什么、没改什么、验证结果。
- 如果改 parser 行为，说明相关测试新增或更新情况。
- 如果改 `data_samples/expected/`、baseline、样本策略或输出格式，说明原因和验证方式。
- 不提交临时 `output/`、raw 样本、缓存或本地运行产物。

## 安装

```bash
python -m pip install -e .[dev]
```

## 运行

本仓库后续默认不提交新的 raw `.xls/.xlsx/.csv` 样本。开发时请使用本地样本路径，下面命令中的输入路径应替换为你的本地文件或目录。

自动路由模式：

```bash
python -m valuation_parser.cli \
  --input D:/local_samples/raw \
  --mapping D:/local_samples/mapping/custodian_mapping.csv \
  --output-dir output
```

手动 override 模式：

```bash
python -m valuation_parser.cli \
  --input D:/local_samples/raw/sample.xls \
  --mapping D:/local_samples/mapping/custodian_mapping.csv \
  --adapter generic \
  --output-dir output
```

开发态显式启用 generic fallback：

```bash
python -m valuation_parser.cli \
  --input D:/local_samples/raw \
  --mapping D:/local_samples/mapping/custodian_mapping.csv \
  --output-dir output \
  --allow-generic-fallback
```

运行产物应写入 `output/`、`tmp/` 或其他已忽略目录，不要直接提交解析输出。

## 映射表说明

加载器支持两种格式：

1. 规范格式：`product_id, association_code, custodian_id, custodian_name, adapter_key, is_active, note`
2. 当前仓库样例的紧凑格式：按托管机构一行，产品和关联代码使用分号分隔；加载时会自动展开成规范格式

## 样本与数据策略

- 原始样本、临时输出、缓存文件默认不进仓库。
- 如果确实需要保留样本，请只保留极小、脱敏、明确用于测试的 fixture，并单独说明用途。
- `data_samples/` 应主要承担目录约定、README 说明和极少量受控 expected fixture 的角色，而不是存放日常开发 raw 数据。

## 状态文档

- 当前项目状态、边界和下一步建议统一记录在 `docs/status.md`。
- 每完成一个阶段，优先更新状态文档，再提交 `docs(status)` 或 `docs(handoff)` 类型的 commit。
- AI 协作入口保持薄层：`AGENTS.md` 面向 Codex/通用 agent，`.github/copilot-instructions.md` 面向 Copilot，`tasks/README.md` 说明任务包与 execution report 目录约定；不要把这些入口扩写成第二规则库。
- Round 4 相关 workflow / baseline 留痕集中在 `tasks/` 与 `skill_experiments/acceptance-baseline-refresh/`；其中实验 skill 仅为项目内试跑资产，不进入 `ai-skill-hub`。

## 下一步建议

1. 决定是否要为 `估值表解析_output_<date>.xlsx` 维护一份更完整的验收基线，并补入 `routing_results` 与 `parse_summary` 的对照面。
2. 明确 `PRODUCT_022` 这类未命中 mapping 的样本是补 mapping、补 adapter，还是长期保留为显式失败夹具。
3. 当新增资产类型或新的 review reason 进入共享规则时，再继续补充增量回归夹具；当前 `hk_equity`、`a_share`、`fund_or_etf` 的核心非衍生品 review path 已有专用覆盖。
4. 确认团队权威 PR 验证命令与分支命名约定，并放入现有薄入口 / canonical source 结构中，不新增第二套规则。
