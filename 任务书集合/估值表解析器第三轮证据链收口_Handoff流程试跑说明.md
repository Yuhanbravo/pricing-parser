# 估值表解析器第三轮证据链收口：Handoff 流程试跑说明

> 历史快照：本文是第三轮 handoff 流程试跑的过程性说明，保留用于复盘协作流程，不应替代当前项目状态文档或当前交付契约。

> 适用项目：`pricing_parser_v2 / valuation_parser`  
> 适用场景：实习生已完成第一轮项目骨架、第二轮外部契约修复，现在进入第三轮“证据链收口”。  
> 训练目标：让实习生完整使用 `chatgpt-handoff-pilot` 风格流程，完成一次从需求审合、任务包生成、分支施工、执行报告到 AI 复审的闭环。  
> 本轮原则：**feature branch 施工 + AI 主审 + 最终合并授权**。

---

## 1. 背景

估值表解析器项目已经完成两轮主要工作。

### 第一轮：项目骨架收口

第一轮主要完成了从 0 到 1 的解析器雏形：

- 建立 `cli / pipeline / routing / mapping_loader / product_identity / normalizers / exporters / adapters` 等模块
- 支持脱敏样本端到端跑通
- 建立基础 routing、identity、normalizer、adapter 和 smoke test
- 形成多 adapter 扩展骨架

但第一轮最大问题是：

> 能跑，但外部契约没有收口。

例如 trace 字段未真实导出、mapping 校验不严格、generic fallback 误记成功、docs/expected/output 口径分叉等。

### 第二轮：外部契约收口

第二轮主要针对第一轮审查问题进行修复，已经基本处理了最关键的 P0：

- `valuation_subjects / valuation_positions` 已真实导出 trace 字段
- `mapping_loader` 已在加载期拒绝未知 `adapter_key`
- 默认 strict routing 下，未命中 mapping 的文件不再被静默算成成功
- `review_flag / review_items / parse_summary` 的职责开始收紧
- smoke / exporter / mapping / routing 等测试开始锁定外部契约

第二轮复审结论是：

> 基本通过但仍需修正，建议再修一轮。

主要剩余问题已经不是核心功能问题，而是：

> docs / expected / outputs / tests / summary / tag 之间的证据链还没有完全统一。

---

## 2. 本轮定位

本轮命名为：

# 第三轮：证据链收口

英文可写作：

```text
Round 3: Evidence Chain Closure
```

本轮不是继续扩展解析能力，也不是重构项目架构，而是将当前项目收口成一个：

- 可验收
- 可复审
- 可接手
- 可打 tag
- 可作为后续并主线候选

的稳定节点。

---

## 3. 审阅与合并模式

## 3.1 原建议修正

原设想是“AI 主审，人只做最终授权或抽检”。  
现在修正为：

> **本地新建分支施工，AI 主审，人工最终审阅后再合并主线。**

这个调整更合理。

原因是：

1. 第三轮虽然任务简单，但仍然会修改文档、expected、测试和可能的输出基线。
2. 这些改动会影响后续是否打 tag、是否并主线，因此不适合直接在 `master/main` 上施工。
3. feature branch 能保留完整 diff，方便你审阅、回退和决定是否合并。
4. 这也能训练实习生更接近真实协作流程：**任务包 -> 分支施工 -> 执行报告 -> AI 复审 -> 人工合并授权**。

## 3.2 推荐责任划分

| 环节 | 推荐责任方 |
|---|---|
| 需求审合 | 实习生 + AI |
| task package 生成 | 实习生 + AI |
| 新建分支 | 实习生 |
| task package 执行 | 实习生 + Codex |
| execution report 生成 | Codex |
| 第三轮 AI 复审 | AI 主审 |
| 合并前人工审阅 | 实习生带教 |
| 是否合并主线 | 实习生带教最终授权 |
| 是否打 tag | 实习生带教最终授权 |

---

## 4. 分支策略

## 4.1 分支命名建议

推荐使用：

```text
review/round3-evidence-chain-closure
```

或更短：

```text
phase3/evidence-chain-closure
```

如果项目以 `master` 为主线，则从 `master` 新建：

```powershell
git checkout master
git status
git checkout -b review/round3-evidence-chain-closure
```

如果项目以 `main` 为主线，则从 `main` 新建：

```powershell
git checkout main
git status
git checkout -b review/round3-evidence-chain-closure
```

## 4.2 分支施工原则

- 第三轮所有改动都在该分支上完成
- 不直接改 `master/main`
- 不在该分支上混入无关功能
- 完成后输出 execution report 和 AI review report
- 你审阅通过后，再决定是否 merge

## 4.3 合并前建议检查

合并前至少执行：

```powershell
git status
git log --oneline --decorate --graph master..HEAD
git diff --stat master..HEAD
git diff --name-status master..HEAD
```

如果主线是 `main`，把 `master` 替换为 `main`。

---

## 5. 本轮目标

本轮只做“证据链收口”，目标包括：

1. 统一 README / HANDOFF / status 中的统计数字和项目状态
2. 补齐当前 strict-default 路径的 acceptance baseline
3. 让 expected output 能覆盖关键交付物
4. 补 `.xlsx` mapping 的自动化测试
5. 让 `parse_summary.md` 更清楚说明：
   - routing success
   - routing failure
   - fallback
   - review 入口
   - flagged subjects / positions / review items
6. 清理或标注历史产物，避免误导后续接手人
7. 检查并制定 tag 策略

---

## 6. 本轮明确不做

本轮禁止扩展为新的开发主题。

### 不做

- 不新增托管机构 adapter
- 不新增资产类型解析
- 不修改核心解析算法
- 不接入 Wind / Oracle / 生产系统
- 不接触真实敏感数据
- 不改脱敏逻辑
- 不做大规模重构
- 不引入新的复杂依赖
- 不把 bundle 文件作为源码仓库常规资产提交，除非有明确授权

### 可以做

- 修正文档数字和口径
- 补 expected baseline
- 补测试
- 修 summary 文案和统计
- 标记或清理历史产物
- 补充 tag 建议
- 更新 HANDOFF / status

---

## 7. 输入材料

执行本轮前，实习生需要准备以下材料：

```text
任务书集合/估值表解析器项目任务书.md
任务书集合/pricing_parser第一轮审查结论摘要.md
第二轮复审报告
README.md
docs/HANDOFF.md
docs/status.md
data_samples/expected/
tests/
```

如果仓库中已经拉入旧 bundle 基线，还应保留：

```text
oldbundle/master
```

用于对照新旧版本差异。

---

## 8. 推荐目录结构

本轮建议把流程文档统一放入：

```text
tasks/
```

推荐文件：

```text
tasks/
├─ 2026-xx-xx_evidence_chain_closure_need_review.md
├─ 2026-xx-xx_evidence_chain_closure_task_package.md
├─ 2026-xx-xx_evidence_chain_closure_execution_report.md
└─ 2026-xx-xx_evidence_chain_closure_ai_review_report.md
```

说明：

- `need_review.md`：需求审合摘要，可选但推荐
- `task_package.md`：正式施工任务包
- `execution_report.md`：执行报告
- `ai_review_report.md`：AI 复审报告

如果需要给你快速查看，可再增加：

```text
tasks/
└─ 2026-xx-xx_evidence_chain_closure_review_packet.md
```

---

## 9. 完整流程

## Step 0：主线确认与新建分支

先确认当前分支与工作区：

```powershell
git branch
git status
```

确保当前主线为 `master` 或 `main`，并且没有未提交改动。

从主线新建第三轮分支：

```powershell
git checkout master
git checkout -b review/round3-evidence-chain-closure
```

如果主线是 `main`：

```powershell
git checkout main
git checkout -b review/round3-evidence-chain-closure
```

执行后确认：

```powershell
git branch --show-current
```

应输出：

```text
review/round3-evidence-chain-closure
```

---

## Step 1：需求审合

### 目标

先审合需求，不直接改代码。

### 输入

- 第二轮复审报告
- 项目任务书
- 第一轮审查摘要
- README / HANDOFF / status

### 输出

生成：

```text
tasks/2026-xx-xx_evidence_chain_closure_need_review.md
```

### 内容要求

至少回答：

```text
1. 当前项目状态是什么？
2. 第三轮为什么只做证据链收口？
3. 本轮必须修哪些问题？
4. 哪些事情明确不做？
5. 预计涉及哪些文件？
6. 本轮完成后如何验收？
```

---

## Step 2：生成 task package

使用 `chatgpt-handoff-pilot` 风格生成正式任务包。

### 输出文件

```text
tasks/2026-xx-xx_evidence_chain_closure_task_package.md
```

### task package 必须包含

```text
# Task Package: Evidence Chain Closure

## 1. Background
说明第一轮、第二轮、第三轮的关系。

## 2. Goal
统一 docs / expected / outputs / tests / summary / tag 证据链。

## 3. Scope
列出本轮允许修改的范围。

## 4. Explicit Non-goals
列出本轮明确不做的事情。

## 5. Target Files
列出预计涉及文件。

## 6. Acceptance Criteria
列出可验证的完成标准。

## 7. Execution Report Requirements
规定执行报告必须包含什么。
```

### 建议验收标准

本轮 task package 至少应包含这些验收标准：

- README / HANDOFF / status 数字与当前 strict-default 实跑一致
- expected baseline 覆盖：
  - `routing_results.csv`
  - `valuation_subjects.csv`
  - `valuation_positions.csv`
  - `parse_summary.md`
  - workbook 结构说明
- `.xlsx` mapping 有自动化测试
- `parse_summary.md` 能说明未路由样本与 review 入口
- 历史产物不再与当前契约并列混淆
- tag 策略已给出建议
- 测试通过，或环境阻塞被明确记录

---

## Step 3：执行 task package

### 执行原则

- 严格按 task package 执行
- 不扩功能
- 不改核心算法
- 不顺手重构
- 不提交敏感数据
- 不把 unrelated cleanup 混入本轮

### 建议执行提示词

```text
请严格按 tasks/2026-xx-xx_evidence_chain_closure_task_package.md 执行。

先复述：
1. 本轮目标
2. 本轮边界
3. 明确不做事项
4. 预计修改文件

然后再进行 bounded execution。

完成后输出 execution report。
本轮不要扩展新 adapter，不要修改核心解析算法，不要引入生产数据。
```

---

## Step 4：生成 execution report

### 输出文件

```text
tasks/2026-xx-xx_evidence_chain_closure_execution_report.md
```

### execution report 必须包含

```text
# Execution Report

## 1. Scope Restatement
说明本轮只做证据链收口。

## 2. Files Changed
逐个列出文件和作用。

## 3. Changes Made
按 task package 的验收项逐条说明。

## 4. Validation
列出实际运行命令、结果、失败原因。

## 5. Boundaries Kept
说明没有做哪些事情。

## 6. Remaining Issues
列出仍未解决问题。

## 7. Tag Recommendation
说明是否建议打 tag，以及建议 tag 名称。

## 8. Commit Summary
列出本轮 commit hash 和 commit message。
```

---

## Step 5：分支内提交

本轮建议至少有一条清晰 commit。

示例：

```text
docs: Phase 3 - evidence - add closure task package and execution report
```

如果代码和文档都有修改，可以拆成：

```text
test(mapping): add xlsx mapping regression coverage
docs(expected): align evidence-chain baseline with strict routing
docs(handoff): refresh evidence closure status and tag recommendation
```

提交前检查：

```powershell
git status
git diff --stat
```

提交：

```powershell
git add .
git commit -m "docs(expected): align evidence-chain baseline with strict routing"
```

---

## Step 6：AI 复审

本轮建议由 AI 主审，不要求你人工逐项审阅每个细节。

### 复审输入

```text
tasks/2026-xx-xx_evidence_chain_closure_task_package.md
tasks/2026-xx-xx_evidence_chain_closure_execution_report.md
第二轮复审报告
README.md
docs/HANDOFF.md
docs/status.md
data_samples/expected/
tests/
```

### 输出文件

```text
tasks/2026-xx-xx_evidence_chain_closure_ai_review_report.md
```

### AI 复审重点

AI 需要判断：

1. task package 是否被严格执行
2. docs / expected / outputs / tests 是否说同一件事
3. 第二轮复审遗留 P0 是否清零
4. `.xlsx` mapping 是否已有自动化测试
5. `parse_summary.md` 是否说明未路由与 review 入口
6. 历史产物是否不再误导
7. 是否可以进入并主线前复审
8. 是否可以打 tag

### AI 复审提示词

```text
请在只读审阅模式下，对第三轮证据链收口结果进行复审。

审阅依据：
1. 第三轮 task package
2. 第三轮 execution report
3. 第二轮复审报告
4. 项目任务书
5. 当前 README / HANDOFF / status
6. 当前 expected output
7. 当前 tests
8. 当前 Git 历史与 tag 情况

重点判断：
- 第三轮 task package 是否被严格执行
- docs / expected / outputs / tests / summary 是否已经形成同一套证据链
- 第二轮复审遗留 P0 是否清零
- 是否仍存在阻碍并主线前复审的问题
- 是否建议打 tag
- 推荐 tag 名称是什么

本轮不要改代码，只输出结构化 AI Review Report。
```

---

## Step 7：人工合并前审阅

AI 复审通过后，不直接并入主线。  
由你进行合并前最终审阅。

### 你重点看

```text
1. AI review 是否给出“可进入并主线前复审”
2. git diff 是否只覆盖本轮授权范围
3. 是否存在 bundle / 临时输出 / 敏感文件误提交
4. 是否有清晰 execution report
5. 是否有明确 tag 建议
```

### 建议命令

假设主线是 `master`：

```powershell
git checkout review/round3-evidence-chain-closure
git log --oneline --decorate --graph master..HEAD
git diff --name-status master..HEAD
git diff --stat master..HEAD
```

确认后再合并：

```powershell
git checkout master
git merge --no-ff review/round3-evidence-chain-closure
```

如果主线是 `main`，将 `master` 替换为 `main`。

---

## Step 8：tag 决策

如果 AI 复审结论和你的最终审阅都认为可以进入下一阶段，则可以考虑打 tag。

推荐 tag：

```text
pricing-parser-review-r1-baseline
pricing-parser-review-r2-candidate
pricing-parser-evidence-chain-closed
```

或者更短：

```text
review-round1-baseline
review-round2-candidate
review-round3-evidence-closed
```

建议：

- `review-round1-baseline` 指向第一轮提交节点
- `review-round2-candidate` 指向第二轮复审候选节点
- `review-round3-evidence-closed` 指向第三轮证据链收口完成节点

---

## 10. 本轮产出物要求

本轮至少产出：

```text
1. 需求审合摘要
2. task package
3. execution report
4. AI review report
```

推荐额外产出：

```text
5. review packet
```

---

## 11. 本轮验收标准

本轮完成后，项目应满足：

| 维度 | 验收标准 |
|---|---|
| branch | 所有施工都在第三轮分支完成 |
| docs | README / HANDOFF / status 数字一致 |
| expected | expected baseline 覆盖关键输出 |
| outputs | 当前输出与 expected 不冲突 |
| tests | 包含 `.xlsx mapping` 自动化测试 |
| summary | 说明 routing failure / fallback / review 入口 |
| history | 历史产物不再误导当前契约 |
| tag | 有明确 tag 建议 |
| process | 有 task package / execution report / AI review report |
| merge | AI 复审通过后，由你最终决定是否合并主线 |

---

## 12. 实习生自查清单

提交前请自查：

```text
[ ] 是否从主线新建第三轮施工分支？
[ ] 是否确认当前分支不是 master/main？
[ ] 是否先完成需求审合？
[ ] 是否生成 task package？
[ ] 是否严格按 task package 执行？
[ ] 是否没有扩展新 adapter？
[ ] 是否没有修改核心解析算法？
[ ] 是否更新 README / HANDOFF / status？
[ ] 是否补齐 expected baseline？
[ ] 是否补了 .xlsx mapping 自动化测试？
[ ] 是否更新 parse_summary 口径？
[ ] 是否处理历史输出误导问题？
[ ] 是否生成 execution report？
[ ] 是否让 AI 做了只读复审？
[ ] 是否给出 tag 建议？
[ ] 是否没有直接合并 master/main？
```

---

## 13. 推荐 Git commit

本轮建议至少有一条清晰提交。

示例：

```text
docs: Phase 3 - evidence - add closure task package and execution report
```

如果代码和文档都有修改，可以拆成：

```text
test(mapping): add xlsx mapping regression coverage
docs(expected): align evidence-chain baseline with strict routing
docs(handoff): refresh evidence closure status and tag recommendation
```

不建议使用：

```text
update
fix
misc
continue
```

---

## 14. 最终判断口径

本轮结束后，请按以下标准判断项目状态：

### A：可进入并主线前复审

条件：

- 第二轮遗留 P0 清零
- docs / expected / outputs / tests 一致
- AI review 通过
- tag 策略明确
- 分支 diff 只包含授权范围

### B：仍需小修

条件：

- 主体已完成，但还有 1–2 个证据漂移
- 或测试仍缺关键路径
- 或 branch diff 中出现少量需清理文件

### C：需要重新组织任务

条件：

- task package 未被执行
- 或本轮又扩展了无关功能
- 或证据链仍然明显分叉
- 或直接在 master/main 上施工导致审阅困难

---

## 15. 一句话总结

本轮不是为了继续证明“解析器能跑”，而是为了证明：

> **这个节点可以被别人相信、复审、接手，并在 feature branch 上经过 AI 复审和人工授权后安全合并。**
