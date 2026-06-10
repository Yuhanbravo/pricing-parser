# Intern Project Takeover Notes

## Scope

本次覆盖的文件：

- `pricing-parser` 项目以下入口文件：
  - `README.md`
  - `docs/HANDOFF.md`
  - `docs/status.md`
  - `AGENTS.md`
  - `.github/copilot-instructions.md`
  - `tasks/README.md`
  - `pyproject.toml`
- 以及`ai-skill-hub` 中的
  - `skills/project-takeover/SKILL.md`
  - `README.md`

本次不覆盖：

- `src/valuation_parser/` 内部模块实现细节
- `tests/` 具体测试用例
- `config/` 具体配置内容
- `data_samples/` 样本文件内容
- `MIGRATION_PLAN.md` 迁移计划细节


## Local Workspace Setup
本地目录结构：
- `D:\dev\pricing_parser\pricing-parser`
- `D:\dev\pricing_parser\ai-skill-hub`

VS Code workspace使用情况，以及固定路径配置检查：

- 使用 VS Codet workspace 同时打开两个仓库，且workspace 文件未提交到仓库
- 固定路径检查结果：在一些md文件中写了 D:\intern_workspace 等硬编码路径，与当前本地目录 pricing_parser 不一致，这些是文档示例路径，不影响运行，也不影响本地路径配置。此外还搜索到一些二进制文件（.xlsx / .xls），可能是误报，此部分文件属于测试样本数据，不是代码或配置，也不影响运行。


## Project Understanding

**项目描述：**`pricing-parser` 是一个 Python 估值表解析工具。它解决的核心问题是：不同托管机构（中信、招商、国泰海通 等）出具的证券投资基金估值表格式各不相同，手动整理费时易错。这个工具通过"先识别产品身份和托管机构，再交给对应的 adapter 解析"的方式，把异构的 `.xls`/`.xlsx`/`.csv` 估值表自动转为标准化的 CSV 和 Excel 输出。

**主要输入：** 估值表文件（`.xls` / `.xlsx` / `.csv`）+ 产品-托管机构映射表（CSV）+ 配置文件（taxonomy YAML、adapter YAML、code rules YAML）

**主要输出：** `routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv`、`parse_summary.md`、以及按输入日期自动命名的 Excel 工作簿 `估值表解析_output_<date>.xlsx`

**当前不应随便修改的边界：** 
- 核心解析链路（`src` 下的 parser runtime、路由逻辑、adapter 逻辑）是项目的行为主体，未经 task package 授权不应改动。
- `tests` 是可执行的行为契约，`config` 中的 taxonomy 和 adapter 规则定义了分类与解析口径，这两类文件同样不能随意修改。
- `expected` 是受控 acceptance baseline，只在全量 rerun 验证后才能刷新，平时不能动。
- 此外，`AGENTS.md` 和 `copilot-instructions.md` 必须保持 thin adapter，不能膨胀成第二套规则库。



## Main Entry Points
本次阅读的入口文件作用说明：

- `pricing-parser` 仓库:
    - `README.md`：项目总入口。
    - `docs/HANDOFF.md`：项目交接和当前状态。
    - `docs/status.md`:当前阶段快照
    - `AGENTS.md`：AI agent 项目入口说明。
    - `.github/copilot-instructions.md`：Copilot 项目说明。
    - `tasks/README.md`：任务材料组织规则。
    - `pyproject.toml`：包元数据、依赖声明、以及pytest 配置

- `ai-skill-hub` 仓库
    - `skills/project-takeover/SKILL.md`：项目接手 skill 的规范定义
    - `README.md`：仓库总入口


## Skill Reference

- skill-hub 是参考仓库，不是本项目代码；

- project-takeover用途：
这是一个项目接管型 skill，用来为陌生仓库生成最小可用的 takeover packet，帮助新维护者或 AI agent快速进入项目。核心思路是把项目接手分为四个阶段：scan（扫描）→ understand（理解）→ structure（整理）→ output（输出）

- 本次任务采用的接手思路具体包括：
  - scan：阅读全部指定入口文件；检查固定路径配置以及执行基础验证 pytest
  - understand：根据阅读结果理解项目结构，主要解决的问题和当前状态，以及ai使用的范围和边界；区分已确认事实、我的理解和待确认问题
  - structure：按接手材料模板整理成本文档，整合离散信息
  - output：生成本文档草稿并提交Pull Request

- 判断 vs 修改：
project-takeover skill 的前三个阶段（scan、understand、structure）都是纯判断，不应修改任何代码，最终 output 阶段也只产出接手文档本身。
本次任务所有对项目代码、配置、测试的观察都只是判断，记录在本文档中，不做任何代码修改


## AI Entry Files Understanding

AI 入口文件的简要说明：

| 文件 | 给谁看 | 作用 | 不能替代 |
|---|---|---|---|
| `AGENTS.md` | AI agent | 让 AI agent 进入项目时知道先读哪些文件、有哪些硬性工作边界 | 不能替代 README.md 中的详细说明、docs/status.md 中的状态快照、tests/ 中的行为契约。它只是一个"指路牌"，不是规则全集。
| `.github/copilot-instructions.md` | GitHub Copilot / Copilot Chat | Copilot 生成代码建议时，需要遵守的一些规则和边界 | 它是 AGENTS.md 的下游适配器，不是独立的规则文件。
| `tasks/README.md` | AI agent / 任务协作者 | 规定 task package 和 execution report 的文件命名格式和最小字段，让 AI-assisted 工作可追溯、可 review | 不存放project facts和code behaviour


## Current Boundaries
我理解的当前边界：
- 不修改 parser runtime；
- 不修改 routing / adapter；
- 不修改 `src/`、`tests/`、`config/`；
- 不刷新 `data_samples/expected/`；
- 不提交 `output/`；
- 不提交 .code-workspace；
- 不提交 API key 或敏感数据；
- 不提交新 raw 样本：.xls / .xlsx / .csv 默认不进仓库；
- 不提交 ai-skill-hub 内容：独立同级仓库，不属于本项目；
- 不提交 workspace 文件、缓存、egg-info；
- PRODUCT_022 故意保持路由失败：不为其补 mapping 或 adapter；
- AI 入口文件保持 thin：不膨胀成第二套规则库。


## Validation
实际运行过的命令和结果：

命令：
- `git status`
- `git branch --show-current`:
- `python -c "import sys; print(sys.executable)"`
- `python -m pytest -q`

- `git pull`
- `git checkout -b docs/intern-project-takeover`:

结果：
- On branch master
Your branch is up to date with 'origin/master'.
- master
- C:\Users\Evelyn\miniforge3\envs\pricing-parser-py312\python.exe
- 52 passed in 12.49s

- Already up to date.
- Switched to a new branch 'docs/intern-project-takeover'


## Questions / Pending Items
列出 3–5 个仍需主管或 reviewer 判断的问题。

- 固定路径配置检查：在一些md文件中写了 D:\intern_workspace 等硬编码路径，与当前本地目录 pricing_parser 不一致，这些是文档示例路径，不影响运行，也不影响本地路径配置。此外还搜索到一些二进制文件（.xlsx / .xls），可能是误报，此部分文件属于测试样本数据，不是代码或配置，也不影响运行。

- 命名差异：仓库目录名为 pricing-parser，但 pyproject.toml 中包名为 valuation-parser。这是一个历史命名差异，还是有意区分"仓库名"与"包名"？是否需要统一？