# valuation-parser

估值表解析器项目脚手架，按“路由层 + 公共解析层 + 托管机构适配层”组织。当前已完成 Phase 5 的受控交付：全量 11 份受控原始样本可端到端跑通，覆盖 mapping-driven routing、9 个 adapter key、标准化 CSV/Markdown/Excel 导出，以及 `3102*` 衍生工具科目 review 规则。

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
- 输出 `routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv`、`parse_summary.md`，以及 Excel 工作簿 `phase3_outputs.xlsx`（当前仍保留该历史文件名）
- 当前注册并在受控路径中验证过的 adapter key：`citics`、`cmsc`、`csc`、`generic`、`greatwall`、`gtja`、`guosen`、`orient`、`xyzc`
- 最新 `output_phase5/` 全量运行结果：11 个文件、11 次成功路由、0 次路由失败、1113 条科目、202 条持仓、253 条 review items、0 个 normalization issues
- 共享 review 逻辑已覆盖 `3102*` 衍生工具科目，命中后会进入 `review_items.csv`
- 测试已覆盖身份提取、映射加载、路由、adapter 样表、Phase 5 全量 smoke 和 review-item 回归

当前已验证的真实样表：

- `证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx` -> `greatwall`
- `20250327_PRODUCT_002_证券投资基金估值表.xls` 与 `20250327_PRODUCT_002_证券投资基金估值表.csv` -> `xyzc`
- `2025-03-27_PRODUCT_001估值表.xlsx` -> `guosen`
- `PRODUCT_008委托资产资产估值表20250327.xls` -> `cmsc`
- `估值表_PRODUCT_021_20250327.xls` -> `csc`
- `估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx` -> `generic` fallback
- `PRODUCT_006_资产估值表_20250327.xls`、`PRODUCT_010_证券投资基金估值表_2025-03-27.xls`、`PRODUCT_012_估值表_20250327.xls` 已在批量管线测试中分别覆盖 `citics`、`orient`、`gtja`

## 项目结构

```text
pricing_parser/
├─ README.md
├─ pyproject.toml
├─ config/
│  ├─ adapters/
│  │  ├─ generic.yaml
│  │  ├─ greatwall.yaml
│  │  ├─ xyzc.yaml
│  │  └─ guosen.yaml
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
│     └─ adapters/
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

## 下一步建议

1. 制定 `phase3_outputs.xlsx` 的兼容迁移方案，再决定是否切换到中性命名的工作簿文件名。
2. 继续补充更多资产类型与 review reason 的回归夹具，避免共享规则只在当前样本集上成立。
3. 用 `data_samples/expected/` 中的样例继续收敛 `valuation_subjects.csv`、`valuation_positions.csv` 和 `review_items.csv` 的字段口径。
