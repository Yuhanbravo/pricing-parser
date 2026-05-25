# pricing_parser 第三轮审查结论摘要暨第四轮任务书

> 项目：`pricing-parser / valuation_parser`  
> 上一轮：Round 3 证据链收口  
> 本轮：Round 4 资产术语收敛  
> 建议分支：`feature/round4-asset-taxonomy`  
> 任务类型：上一轮 PR 审查闭环摘要 + 下一轮功能口径收敛任务书 + AI 工作流训练 + 项目内实验 skill 试作  
> 本轮主目标：建立轻量、可配置、可测试的资产分类术语层，使 `subjects / positions / review_items / parse_summary / expected baseline` 的资产术语口径一致。  
> 本轮训练目标：练习使用 `workflow-bootstrap` 的多角色 AI 开发流程，并将实习生草案 `acceptance-baseline-refresh` 改造成项目内实验 skill，但暂不进入 `ai-skill-hub`。

---

## 与第三轮 Handoff 流程试跑说明的关系

`估值表解析器第三轮证据链收口_Handoff流程试跑说明.md` 是 Round 3 过程性文档，用于记录第三轮如何通过 handoff/PR/AI review 完成证据链收口。

本文是 Round 3 完成后的正式承接文件，用于记录第三轮审查闭环结论，并定义 Round 4 资产术语收敛任务。

因此，Round 4 施工应以本文为准。

## 0. 文件命名与管理口径

本项目后续任务书建议采用以下命名习惯：

```text
<项目名>第N轮审查结论摘要暨第N+1轮任务书.md
```

原因：

1. 上一轮审查结论是下一轮任务输入。
2. 下一轮任务不应脱离上一轮实际审查结果重新发散。
3. 便于后续从 `任务书集合/` 中连续追踪：
   - 本轮为什么做
   - 上轮留下了什么问题
   - 哪些问题已经人工裁决
   - 下一轮明确不做什么

本文件即采用该口径：

```text
pricing_parser第三轮审查结论摘要暨第四轮任务书.md
```

---

## 1. 第三轮审查与合并摘要

## 1.1 第三轮任务定位

第三轮为：

```text
Round 3：证据链收口
```

主要目标不是新增解析能力，而是将第二轮后的项目状态收口成一个可审、可验、可接手、可合并的稳定节点。

核心关注：

- README / HANDOFF / status 口径一致
- expected baseline 完整
- strict-default routing 证据清楚
- `.xlsx mapping` 自动化测试补齐
- parse_summary 说明更清晰
- 历史 output / 过期治理材料不再误导当前契约
- PR 审查流程走通

---

## 1.2 第三轮审查方式

第三轮主要通过 PR 审查完成。

原始 PR：

```text
https://github.com/ryr20262026/pricing-parser/pull/1
```

辅助 review / fork mirror PR：

```text
https://github.com/Yuhanbravo/pricing-parser/pull/1
```

审查过程大致包括：

1. 实习生在 `review/round3-evidence-chain-closure` 分支完成第三轮改动。
2. 发起 PR，合入 `master`。
3. 先通过 Copilot / Codex 进行 AI review。
4. 对 review 意见进行一轮或多轮修复。
5. 由 AI 最终复核确认无 P0/P1 阻碍项。
6. 合并 PR 到主线。
7. 当前项目进入 Round 4 能力增强规划阶段。

---

## 1.3 第三轮完成判断

第三轮可以视为已经完成阶段目标。

完成点：

- `data_samples/expected/` 已作为当前 strict-default acceptance baseline。
- README / HANDOFF / status 已围绕当前基线收口。
- `review_flag / review_note / review_items` 职责已有较清楚说明。
- `PRODUCT_022` 作为未路由样本被显式呈现，不再被 generic fallback 静默算作成功。
- `.xlsx mapping` 相关路径已纳入自动化测试。
- PR 流程已完成：分支开发、AI review、修复、合并主线。

第三轮的主要价值不只是代码改动，而是让实习生完成了一次接近真实团队协作的：

```text
feature branch -> PR -> AI review -> 修复 -> 复核 -> merge
```

---

## 1.4 第三轮之后的遗留事项

第三轮之后仍有几个后续方向，但不再属于证据链收口问题。

### 已人工裁决事项：PRODUCT_022

原 Round 4A 设想为：

```text
PRODUCT_022 路由决策
```

现在已人工裁决：

> `PRODUCT_022` 是已经终止的老产品，暂不进入下一轮处理；后续将采用其他同托管方产品替代。

因此：

- 不为 `PRODUCT_022` 补 mapping
- 不为 `PRODUCT_022` 新增 adapter
- 不为了消除一个 routing failure 而破坏当前受控样本口径
- 本轮只需在文档中说明其不进入 Round 4 施工范围

### 后续开发方向

第三轮之后，开发方向从“证据链治理”切换到“真实能力增强”。

本轮选择：

```text
Round 4：资产术语收敛
```

后续可以顺延：

```text
Round 5：新增 adapter / 样本覆盖
Round 6：最小 API / 数据中心接入接口
```

---

## 2. Round 4 编号调整说明

原规划中 Round 4 拆为：

- Round 4A：`PRODUCT_022` 路由决策
- Round 4B：资产术语收敛
- Round 4C：新增 adapter / 样本覆盖
- Round 4D：最小 API / 数据中心接入接口

由于 Round 4A 已人工裁决跳过，为避免实习生误以为还有待施工的 4A，本任务书将原 “Round 4B：资产术语收敛” 调整为：

# **Round 4：资产术语收敛**

本轮中如需提及 `PRODUCT_022`，只作为背景说明，不进入开发范围。

---

## 3. Round 4 背景与定位

估值表解析器已经完成：

1. **第一轮：项目骨架收口**  
   建立了解析器基础结构，包括 `routing / mapping / identity / adapter / exporter / tests` 等模块，并能对脱敏估值表样本端到端跑通。

2. **第二轮：外部契约收口**  
   修复了 trace 字段导出、`adapter_key` 校验、strict routing、review 口径等核心问题。

3. **第三轮：证据链收口**  
   完成 README / HANDOFF / status / expected / outputs / tests / parse_summary 的证据链整理，并通过 PR 审阅后合并主线。

当前项目进入下一阶段：**从“证据链治理”切换到“真实能力增强”**。

本轮聚焦：

> **资产分类术语收敛（Asset Taxonomy Closure）**

同时，本轮作为实习生 AI 开发流程训练任务，需要同步完成：

- 使用 `workflow-bootstrap` 进行多角色 AI 开发流程试跑
- 将 `acceptance-baseline-refresh` 草案转化为项目内实验 skill
- 用该实验 skill 辅助本轮 expected baseline 刷新与差异判断

---

## 4. 总体目标

本轮有三个并行但分层的目标。

## 4.1 主任务：资产术语收敛

建立一套轻量、稳定、可配置、可展示的资产分类术语层。

目标是让以下输出中的资产术语口径一致：

- `valuation_subjects.csv`
- `valuation_positions.csv`
- `review_items.csv`
- `parse_summary.md`
- Excel workbook 输出
- `data_samples/expected/` acceptance baseline

本轮不是重写解析器，而是在现有解析结果之上增加一层**术语映射与展示口径**。

## 4.2 流程训练：workflow-bootstrap 多角色流程

本轮需要使用 `workflow-bootstrap` 的角色链组织开发流程：

```text
Drafter -> Reviewer -> Implementer -> Reporter -> Final Reviewer
```

其中：

- Drafter：收敛需求、边界、任务包
- Reviewer：在施工前审查任务包边界
- Implementer：按任务包 bounded execution
- Reporter：生成 execution report
- Final Reviewer：只读复审边界、验证、证据链

`workflow-bootstrap` 只定义工作流壳层，不替代 `chatgpt-handoff-pilot` 的 task package / bounded execution / execution report 协议。

## 4.3 实验 skill：acceptance-baseline-refresh

实习生已提出 `acceptance-baseline-refresh` 草案，其定位是用于“受控样本基线刷新”的工作流草案。

本轮要求将该草案整理成**项目内实验 skill**，用于练习 skill 构建与真实项目试跑。

注意：

- 本轮**不把该 skill PR 到你的 `ai-skill-hub`**
- 本轮**不将其视为正式 canonical skill**
- 本轮只在 `pricing-parser` 项目内试作、试跑、留痕
- 后续是否进入 `ai-skill-hub`，由你另行评估

---

## 5. workflow-bootstrap 获取与使用方式

本轮要求显式使用 `ai-skill-hub` 中的 `workflow-bootstrap` skill 进行多角色 AI 开发流程试跑。

## 5.1 仓库地址

`ai-skill-hub` 仓库地址：

```text
https://github.com/Yuhanbravo/ai-skill-hub
```

`workflow-bootstrap` canonical 路径：

```text
skills/workflow-bootstrap/
```

该 skill 的默认角色链为：

```text
Drafter -> Reviewer -> Implementer -> Reporter -> Final Reviewer
```

本轮只使用该 skill 进行工作流壳层与角色分工，不让它替代 `chatgpt-handoff-pilot` 的 task package / execution report 协议。

## 5.2 推荐本地目录结构

建议将 `ai-skill-hub` 和当前项目放在同一个工作区下，但保持为两个独立 Git 仓库：

```text
..\
├─ ai-skill-hub\
└─ pricing-parser\          (当前项目)
```

不要把 `ai-skill-hub` 直接复制进 `pricing-parser` 仓库提交。

## 5.3 首次拉取 ai-skill-hub

```powershell
cd ..\
git clone https://github.com/Yuhanbravo/ai-skill-hub.git
```

如果已经有本地仓库，则更新：

```powershell
cd ..\ai-skill-hub
git pull
```

## 5.4 加入 VS Code 工作空间

建议在 VS Code 中同时打开：

```text
..\pricing-parser    (当前项目)
..\ai-skill-hub      (skill 仓库)
```

这样可以一边开发 `pricing-parser`，一边查阅 `workflow-bootstrap` 的完整 skill 说明。

## 5.5 同步 workflow-bootstrap 到项目

如果本轮希望 Codex 在 `pricing-parser` 项目中直接发现并使用该 skill，建议从 `ai-skill-hub` 同步：

```powershell
cd ..\ai-skill-hub

pwsh -File .\tools\sync_skills_to_nongit_project.ps1 `
  -ProjectPath ..\pricing-parser `
  -SkillName workflow-bootstrap `
  -Targets codex
```

执行后，`pricing-parser` 中应出现：

```text
pricing-parser/
└─ .codex/
   └─ skills/
      └─ workflow-bootstrap/
```

## 5.6 本轮使用边界

`workflow-bootstrap` 只负责：

- 定义多角色工作流壳层
- 明确 Drafter / Reviewer / Implementer / Reporter / Final Reviewer 分工
- 将本轮任务组织成可审、可执行、可报告的流程

它不负责：

- 直接替代 task package
- 直接替代 execution report
- 自动批准合并
- 自动进入 `ai-skill-hub`
- 扩展本轮任务范围

---

## 6. 本轮分支与 PR 要求

## 6.1 新建分支

必须从当前主线新建分支，不允许直接在 `master/main` 上施工。

如果主线是 `master`：

```powershell
git checkout master
git pull
git checkout -b feature/round4-asset-taxonomy
```

如果主线是 `main`：

```powershell
git checkout main
git pull
git checkout -b feature/round4-asset-taxonomy
```

## 6.2 PR 要求

本轮完成后提交 PR，PR 标题建议：

```text
Round 4: add asset taxonomy terminology layer
```

PR 描述必须包含：

```text
## Previous Review Context
## Scope
## Non-goals
## Workflow-bootstrap role chain used
## Asset taxonomy changes
## Acceptance baseline refresh
## Experimental skill notes
## Tests run
## Known limitations
```

其中 `Previous Review Context` 应简要说明：

- 第三轮通过 PR 完成证据链收口
- PR 地址：`https://github.com/ryr20262026/pricing-parser/pull/1`
- 本轮不处理 `PRODUCT_022`
- 本轮从证据链治理转入术语收敛

---

## 7. 主任务需求：资产术语收敛

## 7.1 核心设计原则

本轮不得直接替换或删除现有 `asset_type` 字段。

建议保留旧字段，并新增稳定分类字段：

```text
asset_type
asset_type_internal
asset_type_display
asset_class_l1
asset_class_l2
```

含义：

| 字段 | 用途 |
|---|---|
| `asset_type` | 兼容旧字段，暂不改变既有语义 |
| `asset_type_internal` | 程序稳定分类，英文、可用于下游系统 |
| `asset_type_display` | 中文展示分类，用于 summary / Excel / review |
| `asset_class_l1` | 大类，例如 权益类、基金类、现金类 |
| `asset_class_l2` | 细类，例如 A股、港股、场内基金 |

---

## 7.2 建议分类表

本轮至少覆盖当前样本中已出现的主要类型。

| asset_type_internal | asset_type_display | asset_class_l1 | asset_class_l2 | 是否进入 positions |
|---|---|---|---|---|
| `equity_a_share` | A股股票 | 权益类 | A股 | 是 |
| `equity_hk` | 港股 | 权益类 | 港股 | 是 |
| `equity_star` | 科创板股票 | 权益类 | 科创板 | 是 |
| `cdr` | 存托凭证 | 权益类 | 存托凭证 | 是 |
| `fund_exchange_traded` | 场内基金/ETF | 基金类 | 场内基金 | 是 |
| `cash_deposit` | 现金及存款 | 现金类 | 银行存款 | 否 |
| `margin_deposit` | 保证金 | 保证金类 | 存出保证金 | 否 |
| `clearing_balance` | 证券清算款 | 清算款类 | 证券清算款 | 否 |
| `derivative_swap` | 收益互换 | 衍生品类 | 收益互换 | 否，进入 review |
| `payable` | 应付款项 | 负债类 | 应付款项 | 否 |
| `tax_payable` | 应交税费 | 负债类 | 税费 | 否 |
| `unknown` | 未识别 | 未识别 | 未识别 | 否 |

---

## 7.3 关键业务口径

### 7.3.1 ETF 归基金类

本轮将 ETF / 场内基金归入：

```text
asset_type_internal = fund_exchange_traded
asset_type_display = 场内基金/ETF
asset_class_l1 = 基金类
asset_class_l2 = 场内基金
```

不要因为 ETF 追踪股票指数，就在本轮把它归入权益类。  
权益风险敞口是另一个风险口径，不是估值表资产分类口径。

### 7.3.2 收益互换只进入 review，不进入 positions

收益互换建议分类：

```text
asset_type_internal = derivative_swap
asset_type_display = 收益互换
asset_class_l1 = 衍生品类
asset_class_l2 = 收益互换
review_flag = 1
review_category = derivative_review
```

但本轮不把收益互换强行纳入 `valuation_positions.csv`。

### 7.3.3 现金、保证金、清算款不进入 positions

这些科目保留在 `valuation_subjects.csv`，可在 summary 中统计，但不作为证券持仓进入 `valuation_positions.csv`。

### 7.3.4 A 股有限细分

本轮只做有限细分：

- A股股票
- 科创板股票
- 存托凭证

不新增创业板、北交所、行业、ST 等更细标签。

---

## 8. 配置文件要求

新增配置文件：

```text
config/asset_taxonomy.yaml
```

推荐结构：

```yaml
version: 1

asset_types:
  equity_a_share:
    display_name: A股股票
    asset_class_l1: 权益类
    asset_class_l2: A股
    include_in_positions: true
    default_review_flag: 0

  equity_hk:
    display_name: 港股
    asset_class_l1: 权益类
    asset_class_l2: 港股
    include_in_positions: true
    default_review_flag: 0

  fund_exchange_traded:
    display_name: 场内基金/ETF
    asset_class_l1: 基金类
    asset_class_l2: 场内基金
    include_in_positions: true
    default_review_flag: 0

  derivative_swap:
    display_name: 收益互换
    asset_class_l1: 衍生品类
    asset_class_l2: 收益互换
    include_in_positions: false
    default_review_flag: 1
    default_review_category: derivative_review

  unknown:
    display_name: 未识别
    asset_class_l1: 未识别
    asset_class_l2: 未识别
    include_in_positions: false
    default_review_flag: 1
    default_review_category: unknown_subject
```

约束：

- 配置只负责术语映射和展示口径
- 不把完整解析规则塞入 taxonomy 配置
- 科目识别仍由 adapter / parser 负责
- taxonomy 层不得反向改变 routing 或持仓识别逻辑

---

## 9. 输出字段要求

## 9.1 `valuation_positions.csv`

新增字段：

```text
asset_type_internal
asset_type_display
asset_class_l1
asset_class_l2
```

对于正常证券持仓，上述字段应尽量非空。

## 9.2 `valuation_subjects.csv`

新增字段：

```text
asset_type_internal
asset_type_display
asset_class_l1
asset_class_l2
review_category
```

允许部分非资产类汇总行为空或 `unknown`，但主要资产/负债/复核项应有分类。

## 9.3 `review_items.csv`

新增字段：

```text
asset_type_internal
asset_type_display
asset_class_l1
asset_class_l2
review_category
review_note
```

review 分类和资产分类必须分开，不能把“是否需要复核”塞进 asset type。

## 9.4 `parse_summary.md`

新增或调整资产分类统计，使用统一的 `asset_type_display` 展示。

示例：

```markdown
## Asset Type Coverage

| asset_type_display | count |
|---|---:|
| A股股票 | 38 |
| 港股 | 12 |
| 场内基金/ETF | 5 |
| 收益互换 | 3 |
```

## 9.5 Excel workbook

如果当前已有 Excel workbook 输出，可以增加或调整 summary sheet 中的字段：

- `asset_type_display`
- `asset_class_l1`
- `review_category`

本轮不做复杂样式改造。

---

## 10. review 字段独立要求

不得将 review 逻辑混入 asset taxonomy。

建议使用：

```text
review_flag
review_note
review_category
```

示例：

| 场景 | asset_type_internal | review_flag | review_category |
|---|---|---|
| 正常 A股 | `equity_a_share` | 0 | 空 |
| 正常 ETF | `fund_exchange_traded` | 0 | 空 |
| 收益互换 | `derivative_swap` | 1 | `derivative_review` |
| 未识别科目 | `unknown` | 1 | `unknown_subject` |
| routing 失败 | 空 | 1 | `routing_failure` |

---

## 11. 明确不做事项

本轮不得扩展为新的开发主题。

不做：

- 不新增 adapter
- 不处理 `PRODUCT_022`
- 不新增新产品样本
- 不改变 routing 逻辑
- 不改变核心持仓识别规则
- 不改金额、成本、市值、盈亏计算
- 不改变当前 strict-default 行为
- 不做生产数据库字段设计
- 不做复杂行业分类、策略分类、交易所全量映射
- 不把 review 逻辑和 asset taxonomy 混在一起
- 不把实验 skill 提交到你的 `ai-skill-hub`

---

## 12. workflow-bootstrap 多角色流程要求

本轮必须使用 `workflow-bootstrap` 的多角色链路组织工作。

角色链：

```text
Drafter -> Reviewer -> Implementer -> Reporter -> Final Reviewer
```

## 12.1 Drafter

输出：

```text
tasks/round4_asset_taxonomy_task_package.md
```

内容至少包括：

- 背景
- 目标
- 范围
- 明确不做
- 目标文件
- 验收标准
- 测试要求
- execution report 要求

## 12.2 Reviewer

在执行前审查 task package。

输出：

```text
tasks/round4_asset_taxonomy_pre_implementation_review.md
```

至少判断：

- 是否混入无关功能
- 是否会改变核心解析逻辑
- 是否正确处理 `PRODUCT_022` 不纳入本轮
- 是否正确保留旧 `asset_type`
- 是否把 taxonomy 与 review 逻辑分开

## 12.3 Implementer

严格按 task package 执行。

要求：

- 在 feature branch 上施工
- 不直接改主线
- 不扩展 adapter
- 不处理 `PRODUCT_022`
- 不新增生产接入能力

## 12.4 Reporter

输出：

```text
tasks/round4_asset_taxonomy_execution_report.md
```

至少包含：

- 修改文件清单
- 每个文件作用
- 完成了哪些验收项
- 运行了哪些测试
- expected baseline 是否刷新
- 是否触发 experimental skill
- 剩余问题

## 12.5 Final Reviewer

输出：

```text
tasks/round4_asset_taxonomy_final_review.md
```

至少判断：

- task package 是否被严格执行
- taxonomy 字段是否真实进入输出
- summary 是否统一展示
- tests / expected 是否同步
- 是否存在范围外改动
- 是否建议提交 PR

---

## 13. 项目内实验 skill：acceptance-baseline-refresh

## 13.1 任务定位

实习生已提出 `acceptance-baseline-refresh` 草案。  
该草案用于受控样本基线刷新，核心流程是：

```text
重跑 -> 比对 -> 判定 -> 刷新 -> 同步说明
```

本轮要求将其整理为项目内实验 skill。

## 13.2 存放位置

建议放在项目内：

```text
skill_experiments/acceptance-baseline-refresh/
```

推荐结构：

```text
skill_experiments/
└─ acceptance-baseline-refresh/
   ├─ README.md
   ├─ SKILL.md
   ├─ DEV_NOTES.md
   └─ examples/
      └─ invocation_examples.md
```

说明：

- 这是项目内实验目录
- 不是正式 canonical skill
- 不放入 `ai-skill-hub`
- 不进入 `.codex/skills/` 作为正式运行时 skill，除非另有授权
- 可以在本项目中以文档方式试用

## 13.3 skill 内容要求

`SKILL.md` 至少应包含：

- 何时使用
- 输入
- 输出
- 执行步骤
- 约束
- 验收口径
- 与 `chatgpt-handoff-pilot` / `workflow-bootstrap` 的边界

`README.md` 至少说明：

- 该实验 skill 解决什么问题
- 本轮在 `pricing-parser` 中如何试跑
- 当前局限
- 为什么暂不进入 `ai-skill-hub`

`DEV_NOTES.md` 至少记录：

- 草案来源
- 本轮试跑反馈
- 哪些地方有效
- 哪些地方不成熟
- 后续若要进入 `ai-skill-hub` 需要补什么

`examples/invocation_examples.md` 至少给出一个本项目示例：

```text
请使用 acceptance-baseline-refresh 草案流程，对 Round 4 asset taxonomy 改动后的 expected baseline 进行重跑、diff、差异分类和刷新建议。
```

## 13.4 实验 skill 的本轮试跑要求

在本轮实现 asset taxonomy 后，需要用该实验 skill 的流程完成一次 baseline refresh 说明。

输出建议：

```text
tasks/round4_acceptance_baseline_refresh_report.md
```

内容至少包含：

- 本轮重跑入口
- 当前 baseline 位置
- 新输出位置
- diff 摘要
- 哪些变化是预期契约更新
- 哪些变化是非预期回归
- 哪些变化仍待确认
- 是否刷新 expected baseline
- 是否同步 README / HANDOFF / status

---

## 14. 测试要求

至少补充或更新以下测试：

```text
tests/test_asset_taxonomy.py
tests/test_exporters.py
tests/test_review_items.py
tests/test_smoke.py
```

测试覆盖：

- taxonomy 配置加载
- 已知 asset type 映射
- unknown fallback
- positions 输出新增字段
- subjects 输出新增字段
- review_items 输出新增字段
- parse_summary 使用统一展示口径
- expected baseline 与当前输出一致

如果已有同类测试，可在原测试中扩展，不强制新增文件。

---

## 15. expected baseline 要求

如果输出字段发生变化，应刷新：

```text
data_samples/expected/
```

至少包括：

- `valuation_subjects.csv`
- `valuation_positions.csv`
- `review_items.csv`
- `parse_summary.md`
- workbook baseline 或 workbook 结构说明

刷新 baseline 前必须先用实验 skill 流程做 diff 判定，不允许因为有 diff 就直接覆盖 baseline。

---

## 16. 文档更新要求

至少更新：

```text
README.md
docs/HANDOFF.md
docs/status.md
```

内容包括：

- Round 4 当前状态
- 新增 asset taxonomy 字段说明
- ETF / 收益互换 / 现金保证金等关键口径
- `PRODUCT_022` 本轮不处理的原因
- 实验 skill 只是项目内试跑，不进入 `ai-skill-hub`
- 本轮测试与 expected baseline 状态

---

## 17. 提交规范

建议至少拆成以下 commit：

```text
docs(round4): define asset taxonomy task package
feat(taxonomy): add configurable asset taxonomy mapping
test(taxonomy): cover taxonomy exports and summary fields
docs(skill): add project-local acceptance baseline refresh experiment
docs(status): refresh round4 taxonomy closure status
```

不要使用：

```text
update
fix
misc
continue
```

---

## 18. PR 审阅重点

本轮完成后提交 PR。PR 审阅重点：

- 是否保留旧 `asset_type`
- 是否新增 taxonomy 字段且进入实际输出
- ETF 是否归基金类
- 收益互换是否归衍生品类并进入 review
- 现金/保证金/清算款是否未进入 positions
- taxonomy 是否配置化
- review 字段是否和 taxonomy 分开
- expected baseline 是否按流程刷新
- 实验 skill 是否只留在项目内
- workflow-bootstrap 五角色流程是否有完整留痕
- 是否未处理 `PRODUCT_022`
- 是否没有新增 adapter 或核心算法改动

---

## 19. 本轮验收标准

本轮完成后应满足：

| 维度 | 验收标准 |
|---|---|
| 分支 | 所有改动在 `feature/round4-asset-taxonomy` 分支完成 |
| workflow-bootstrap | 已从 `ai-skill-hub` 查阅或同步 `workflow-bootstrap` |
| taxonomy | 存在 `config/asset_taxonomy.yaml` |
| outputs | subjects / positions / review_items 包含新增术语字段 |
| summary | parse_summary 使用统一展示口径 |
| expected | expected baseline 已按流程刷新 |
| tests | taxonomy / exporter / review / smoke 测试通过 |
| workflow | 产生 task package / pre-review / execution report / final review |
| skill | 项目内实验 skill 目录完整 |
| baseline refresh | 产生 baseline refresh report |
| docs | README / HANDOFF / status 已同步 |
| boundary | 未新增 adapter，未处理 PRODUCT_022，未进入 ai-skill-hub |

---

## 20. 最终交付物清单

本轮 PR 至少应包含：

```text
config/asset_taxonomy.yaml
src/... taxonomy loader/helper 相关修改
outputs/exporter 相关修改
tests/...
data_samples/expected/...
README.md
docs/HANDOFF.md
docs/status.md
tasks/round4_asset_taxonomy_task_package.md
tasks/round4_asset_taxonomy_pre_implementation_review.md
tasks/round4_asset_taxonomy_execution_report.md
tasks/round4_asset_taxonomy_final_review.md
tasks/round4_acceptance_baseline_refresh_report.md
skill_experiments/acceptance-baseline-refresh/
```

如实际文件名不同，应在 execution report 中说明。

---

## 21. 一句话总结

本轮不是为了增加更多解析能力，而是为了让现有估值表解析输出拥有一套**稳定、可配置、可展示、可测试的资产分类术语层**，同时让实习生练习从 `workflow-bootstrap` 多角色流程到项目内实验 skill 的完整 AI 工程化闭环。
