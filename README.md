# valuation-parser

估值表解析器项目脚手架，按“路由层 + 公共解析层 + 托管机构适配层”组织。解析器从估值表文件中提取身份信息、路由到对应托管机构适配器、解析科目与持仓，并输出标准化 CSV / Markdown / Excel 产物。

> 当前运行统计、已验证的适配器列表、taxonomy 类型和支持范围见 **[docs/status.md](docs/status.md)** 的 Current Snapshot 与 Supported Scope。

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

解析器从估值表文件中提取身份信息、路由到对应托管机构适配器、解析科目与持仓，并输出标准化 CSV / Markdown / Excel 产物。核心能力：

- 基于 mapping-driven routing 自动识别托管机构并选择适配器
- 共享解析与导出管线，统一输出 `routing_results`、`valuation_subjects`、`valuation_positions`、`review_items`、`parse_summary` 以及 Excel 工作簿
- 统一 taxonomy 展示口径与 review 标记规则
- 严格默认路由：未命中 mapping 的文件保留 `failed` 状态，不走隐式兜底

> 详细的适配器列表、taxonomy 类型、最新运行统计和验收基线见 **[docs/status.md](docs/status.md)** 的 Current Snapshot 与 Supported Scope。

> 已验证的样表与适配器映射关系见 **[docs/status.md](docs/status.md)** 的 Current Snapshot。

> Round 4 资产术语口径已在 `config/asset_taxonomy.yaml`、`src/valuation_parser/taxonomy.py` 和 `tests/` 中落地；当前 taxonomy 展示类型和支持范围见 **[docs/status.md](docs/status.md)** 的 Supported Scope。

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

## 文档分类与事实源

本仓库文档按受众与权威性分为以下层级：

- **AI-only wrapper**（薄入口，只做指针引用）：`AGENTS.md`、`.github/copilot-instructions.md`、`CLAUDE.md`
- **Human-AI shared**（稳定说明与工作约定）：`README.md`（本文档）
- **Current-state SSOT**（可变项目状态的唯一事实源）：`docs/status.md`
- **Task records**（任务包与执行报告，审计留痕，不是规则中心）：`tasks/`

关键边界：

- `docs/status.md` 是项目当前状态、支持范围、已知缺口和下一步建议的**唯一事实源**；其他文档只引用、不复制可变状态。
- `tasks/` 中的执行报告是历史审计记录，不能反向覆盖当前状态文档中的结论。
- AI 入口文件（`AGENTS.md`、`.github/copilot-instructions.md`、`CLAUDE.md`）保持薄层，不扩展为第二规则库。
- `ai-skill-hub` 是 sibling reference repository，不提交进本仓库。

## 状态文档

- 当前项目状态、边界和下一步建议统一记录在 `docs/status.md`。
- 每完成一个阶段，优先更新状态文档，再提交 `docs(status)` 或 `docs(handoff)` 类型的 commit。
- AI 协作入口保持薄层：`AGENTS.md` 面向 Codex/通用 agent，`.github/copilot-instructions.md` 面向 Copilot，`tasks/README.md` 说明任务包与 execution report 目录约定；不要把这些入口扩写成第二规则库。
- Round 4 相关 workflow / baseline 留痕集中在 `tasks/` 与 `skill_experiments/acceptance-baseline-refresh/`；其中实验 skill 仅为项目内试跑资产，不进入 `ai-skill-hub`。

## 下一步建议

> 详细的下一步建议见 **[docs/status.md](docs/status.md)** 的 Recommended Next Steps。
