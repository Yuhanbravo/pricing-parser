# pricing-parser 路线图（Roadmap）

## 1. 文档目的

`docs/roadmap.md` 是后续多轮功能开发的路线图入口，用于帮助 owner、reviewer、intern 和 AI agent 对齐：

- 多轮开发的优先级排序；
- 每个阶段的边界、进入条件和完成条件；
- 需要人工 owner decision 的位置；
- 可交给实习生执行的任务边界；
- PR 描述中如何挂接 roadmap 阶段、change type、validation command 与 baseline impact。

本文档是人机共读文档（Human-AI shared），不是 AI-only entrypoint。AI 入口文件只应薄引用项目事实源，不应复制本路线图内容。

## 2. 事实源边界

本仓库的事实源按职责分层：

- `README.md`：稳定项目说明、工作区边界、安装运行方式、样本策略、PR 协作约定和文档入口。
- `docs/status.md`：当前状态 SSOT，记录最新支持范围、已知缺口、当前 snapshot 和推荐下一步。
- `docs/roadmap.md`：多轮规划与阶段排序，说明未来工作如何拆分、哪些点需要 owner decision。
- `tasks/README.md`：任务包与 execution report 的规范入口。
- `tasks/*.md`：历史 audit trail，用于追溯具体任务执行过程，不反向覆盖 `docs/status.md` 或本文档。
- AI 入口文件：`AGENTS.md`、`.github/copilot-instructions.md`、`CLAUDE.md` 等保持薄入口，只做指针引用，不复制状态、路线图或长期规则。

## 3. 路线图原则

后续开发默认遵循以下原则：

- **strict-default**：默认路由保持严格；未命中 mapping 的文件不应静默走 generic fallback。
- **baseline-first**：影响导出、解析结果、review item 或 workbook 的改动，应先明确 baseline 保护方式，再改行为。
- **review item controlled surface**：`review_items` 是人工复核入口，新增 review reason 或 review_category 时应控制影响面，并补充 regression。
- **generic fallback explicit-only**：`generic` 仅在显式 override 或显式启用 fallback 时使用，不作为默认自动兜底。
- **small PR / clear diff**：每个 PR 尽量只覆盖一个 roadmap 阶段或一个清晰 change type，避免把 parser 行为、baseline 和文档治理混在一起。
- **status and roadmap separated**：`docs/status.md` 记录“现在是什么”，`docs/roadmap.md` 记录“接下来怎么排”。
- **owner decision before business semantics**：涉及业务分类、产品覆盖、默认策略或下游消费契约的变更，需要 owner 先确认。

## 4. 阶段总览

| 阶段 | 主题 |
| -- | -- |
| R0 | 文档治理与 AI 协作入口稳定 |
| R1 | Workbook 基线与导出一致性 |
| R2 | Review item 回归覆盖扩展 |
| R3 | 路由与产品覆盖决策 |
| R4 | 持仓 taxonomy 与业务分类扩展 |
| R5 | 运营可用性与下游消费 |

## 5. R0 — 文档治理与 AI 协作入口稳定

### 目标

稳定文档事实源、AI entrypoint、任务包与 PR 描述边界，避免同一项目事实在多个文件中漂移。

### 典型工作

- 精简或校准 `README.md`、`docs/status.md`、`tasks/README.md` 的职责说明。
- 确认 AI entrypoints 只保留薄引用，不扩写成规则中心。
- 为后续任务包建立统一 execution report 结构。
- 在不改变 parser runtime 的前提下补齐文档入口链接。

### 进入条件

- 当前 parser 行为不需要立即修复高优先级 bug。
- owner 同意先冻结功能改动，优先清理协作结构。

### 完成条件

- 文档入口职责清晰，`docs/status.md` 与 `docs/roadmap.md` 没有互相复制大量内容。
- AI entrypoints 不包含当前状态 snapshot 或长期 roadmap 正文。
- docs-only PR 可以通过 `git diff --check` 和必要的状态检查。

### 需要 owner 判断的事项

- 哪些文档是 owner-facing，哪些是 AI-facing。
- 是否需要保留历史治理报告，或迁移为 `tasks/*.md` audit trail。

### 是否适合实习生执行

适合。实习生可执行链接补齐、重复内容清理、execution report 整理；不应自行决定事实源重构或删除历史材料。

## 6. R1 — Workbook 基线与导出一致性

### 目标

稳定 workbook export 的基线（baseline）与导出一致性，确保后续 parser 变更可以通过清晰 diff 审阅。

### 典型工作

- 明确 `估值表解析_output_<date>.xlsx` 是否需要独立 acceptance baseline。
- 梳理 workbook sheet、字段顺序、命名规则和 summary 内容。
- 为 CSV 与 workbook 中相同语义字段建立一致性检查。
- 更新或新增 export regression，避免格式漂移。

### 进入条件

- R0 的文档边界已基本稳定。
- owner 确认 workbook 是否作为正式验收产物。

### 完成条件

- workbook baseline 策略明确：维护、忽略或按需生成。
- 关键导出字段的顺序、命名和空值策略有 regression 保护。
- PR 中能明确说明 baseline impact。

### 需要 owner 判断的事项

- workbook 是否必须与 CSV baseline 同步维护。
- 下游消费方更依赖 workbook、CSV，还是两者都依赖。
- 是否接受日期派生文件名带来的 baseline 维护成本。

### 是否适合实习生执行

部分适合。实习生可做字段对账、生成 diff 报告、补充简单 regression；baseline 策略和导出契约需 owner 决定。

## 7. R2 — Review item 回归覆盖扩展

### 目标

扩展 `review_items` 相关 regression，使人工复核入口的变化可控、可解释、可回归。

### 典型工作

- 为新的 `review_note`、`review_category` 或 review reason 增加 focused tests。
- 检查 `valuation_subjects`、`valuation_positions` 与 `review_items` 的 trace fields 是否一致。
- 覆盖不同 `subject_name` / `instrument_name` 组合下的 dedup 和 grouping 行为。
- 为新增资产类型或特殊科目建立最小 fixture。

### 进入条件

- R1 已明确 baseline 或导出一致性策略，避免 review item 改动无法审阅。
- owner 确认新的 review reason 是否属于人工复核范围。

### 完成条件

- 关键 review item 生成路径具备 regression coverage。
- review queue 的新增、减少或字段变更能在 PR 中解释。
- 不把 review item 规则散落到文档中；可执行契约仍在 `tests/` 和 parser 逻辑中。

### 需要 owner 判断的事项

- 哪些异常应进入 `review_items`，哪些应直接失败或保持空值。
- review queue 的字段是否满足实际人工复核流程。

### 是否适合实习生执行

适合但需边界清晰。实习生可根据已确认规则补测试和 fixture；不应自行定义新的业务 review semantics。

## 8. R3 — 路由与产品覆盖决策

### 目标

处理未覆盖产品、mapping gap、adapter 覆盖与 strict-default 行为之间的关系。

### 典型工作

- 分析未命中 mapping 的样本是否应补 mapping、补 dedicated adapter，或保持失败 fixture。
- 为新 custodian adapter 增加最小路由和解析覆盖。
- 明确 manual adapter override 与 `--allow-generic-fallback` 的使用边界。
- 维护 routing results 的 trace fields 和失败原因可读性。

### 进入条件

- R1/R2 已提供足够 baseline 与 review item 保护。
- owner 已对目标产品或 custodian 覆盖优先级排序。

### 完成条件

- 新增或调整的路由路径有 regression coverage。
- 默认模式仍保持 strict-default；generic fallback 不被隐式启用。
- PR 明确说明新增覆盖、未覆盖范围和 baseline impact。

### 需要 owner 判断的事项

- 未覆盖产品是业务上必须支持，还是保留为失败样本。
- 新产品应通过 mapping 解决、adapter 解决，还是暂缓。

### 是否适合实习生执行

部分适合。实习生可整理 mapping audit、失败样本清单和测试草案；adapter 行为和默认路由策略需 owner 或核心开发者确认。

## 9. R4 — 持仓 taxonomy 与业务分类扩展

### 目标

扩展持仓 taxonomy 与业务分类表达，提升 downstream reconciliation 和人工审阅可读性。

### 典型工作

- 在 `config/asset_taxonomy.yaml` 中扩展已确认的资产分类。
- 调整 parser taxonomy 显示字段和内部字段映射。
- 为新 `asset_type_internal`、`asset_type_display`、`asset_class_l1`、`asset_class_l2` 增加 regression。
- 校验 subjects、positions、review items 与 parse summary 中 taxonomy 口径一致。

### 进入条件

- owner 明确新增分类的业务语义和展示口径。
- R2 已能保护 review item 影响面。

### 完成条件

- 新 taxonomy 类型在配置、解析、导出和测试中一致。
- 旧 baseline 的变化可解释，且没有无保护的大范围 diff。
- 文档只记录原则和入口，不把 taxonomy 规则复制到 roadmap。

### 需要 owner 判断的事项

- 新分类是否为正式业务分类，还是临时 review marker。
- 中英文展示名、层级归属和下游字段是否稳定。

### 是否适合实习生执行

部分适合。实习生可按已确认 taxonomy 规则补配置和测试；分类定义、层级命名和业务口径必须由 owner 决定。

## 10. R5 — 运营可用性与下游消费

### 目标

提升 CLI、输出目录、错误报告和下游消费契约的运营可用性，同时避免过早产品化。

### 典型工作

- 改善 CLI 参数说明、错误信息和运行摘要。
- 明确 `output/`、`tmp/`、baseline 与本地产物的边界。
- 为下游消费方整理字段契约和变更说明。
- 设计轻量 validation checklist，便于非核心开发者执行。

### 进入条件

- 核心导出、review item、routing 和 taxonomy 基线已较稳定。
- owner 明确实际下游消费方式和最低可用要求。

### 完成条件

- 常见运行失败能被用户定位，不需要阅读 parser 内部实现。
- 下游消费字段变更有清晰说明和 validation command。
- 未引入 Web UI / GUI 或重型运营平台假设。

### 需要 owner 判断的事项

- 哪些输出是正式交付物，哪些只是 debug artifact。
- 是否需要面向运营用户的额外说明文档。

### 是否适合实习生执行

适合。实习生可整理 CLI 示例、错误信息截图、字段清单和运行 checklist；不应自行定义新的交付 SLA 或对接系统。

## 11. 暂缓方向

以下方向暂缓，除非 owner 单独批准并重新定义 scope：

- Web UI / GUI。
- full accounting engine。
- 自动业务判断或自动替代人工复核。
- 默认 generic fallback。
- 投资组合归因 / 多因子分析。
- 直接对接券商、托管、PB 或运营系统。
- 无 baseline 保护的大型重构。

## 12. PR 挂接规则

未来 PR 描述建议包含以下字段，便于 reviewer 快速判断影响面：

```md
Roadmap stage: R0 / R1 / R2 / R3 / R4 / R5
Change type: docs / tests / parser / config / baseline / tooling
Owner decision required: yes / no
Validation command: <command>
Baseline impact: none / expected update / needs review
```

填写要求：

- `Roadmap stage`：说明该 PR 主要对应哪个阶段；跨阶段 PR 需要解释原因。
- `Change type`：说明改动类型，避免 docs-only PR 混入 runtime 行为。
- `Owner decision required`：涉及业务语义、默认策略、baseline 策略时通常为 `yes`。
- `Validation command`：列出实际运行的命令，例如 `git diff --check` 或 `python -m pytest`。
- `Baseline impact`：说明是否影响 `data_samples/expected/`、workbook baseline 或输出字段。

## 13. 推荐推进顺序

推荐按以下顺序推进，除非出现高优先级 bug 或 owner 重新排序：

1. 先完成 R0，保持文档治理和 AI 协作入口稳定。
2. 再推进 R1，确认 workbook baseline 与导出一致性策略。
3. 随后推进 R2，为 review item 影响面建立更充分 regression。
4. 在 baseline 和 review surface 可控后推进 R3，处理路由与产品覆盖决策。
5. 之后推进 R4，扩展 taxonomy 与业务分类。
6. 最后推进 R5，改善运营可用性和下游消费体验。
