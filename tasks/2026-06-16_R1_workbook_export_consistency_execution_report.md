# R1 Workbook Export Consistency Audit Execution Report

## Status

done

## Tools used

- 工具：Claude Code（只读文件检查、glob 文件匹配、grep 内容搜索、文件写入）
- 选择理由：任务书允许实习生自主选择工具；Claude Code 支持高效并行文件读取、代码搜索和结构化报告生成。仓库内已有 `CLAUDE.md` 和 `AGENTS.md` 薄入口文件，Claude Code 可正确遵循项目边界。
- 人工核查记录：
  - 逐行核对 `exporters.py` 中所有 `*_FIELDS` 常量定义（`ROUTING_FIELDS` 10 字段、`SUBJECT_FIELDS` 35 字段、`POSITION_FIELDS` 31 字段、`REVIEW_FIELDS` 17 字段）
  - 手动追踪 `_build_output_workbook_filename()` 的完整逻辑链路（从 `run_pipeline()` 调用点到日期提取正则到回退常量）
  - 阅读 `test_acceptance_baseline.py` 中 `_read_workbook_rows()` 实现，确认 workbook baseline 比对方式为结构化数据比对
  - 确认所有审计结论均基于实际代码阅读，非 AI 推测
  - 确认整个过程中未使用 Edit/Write 修改 `src/`、`tests/`、`config/`、`data_samples/` 下任何文件

## Files changed

本次 PR 新增 4 个任务文件（均在 `tasks/` 目录下）：

| 文件 | 类型 | 说明 |
|---|---|---|
| `tasks/2026-06-16_R1_workbook_export_consistency_audit.md` | 新增 | R1-P1 只读审计报告 |
| `tasks/2026-06-16_R1_workbook_baseline_owner_decision_note.md` | 新增 | Owner decision note（5 项决策草案） |
| `tasks/2026-06-16_R1_workbook_export_consistency_p2_test_design.md` | 新增 | R1-P2 回归测试设计 |
| `tasks/2026-06-16_R1_workbook_export_consistency_execution_report.md` | 新增 | 本执行报告 |

## What changed

本轮只做只读审计和文档撰写，**未修改** `src/`、`config/`、`tests/`、`data_samples/`、`.github/workflows/`、AI entrypoints（`AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md`）和 `README.md`。

审计报告核心结论：
1. CSV 和 workbook 在 `exporters.py` 中共享同一组 `*_FIELDS` 常量，架构上已杜绝字段漂移
2. `data_samples/expected/估值表解析_output_2025-03-27.xlsx` 已作为 workbook-content baseline 存在，且被 `test_acceptance_baseline.py` 通过 sheet-content 结构化比对覆盖
3. 测试缺口主要集中在：无独立 `write_excel_workbook()` 单元测试、无跨格式（CSV ↔ workbook）一致性测试、无文件名确定性测试
4. 所有策略性结论（workbook 验收角色、baseline 策略、CSV 权威性、文件名契约）已整理为 decision note，5 项决策已由 owner 确认

## Validation results


### git diff --check

```
（无输出 — pass）
```

无空白字符问题。

### git diff --name-only

tasks/2026-06-16_R1_workbook_export_consistency_audit.md
tasks/2026-06-16_R1_workbook_baseline_owner_decision_note.md
tasks/2026-06-16_R1_workbook_export_consistency_p2_test_design.md
tasks/2026-06-16_R1_workbook_export_consistency_execution_report.md

### git status --short
PR diff 仅包含以下 4 个新任务文件，全部在 `tasks/` 目录下：

A  tasks/2026-06-16_R1_workbook_export_consistency_audit.md
A  tasks/2026-06-16_R1_workbook_baseline_owner_decision_note.md
A  tasks/2026-06-16_R1_workbook_export_consistency_execution_report.md
A  tasks/2026-06-16_R1_workbook_export_consistency_p2_test_design.md

无已修改文件、无已删除文件、无 `src/`、`config/`、`tests/`、`data_samples/`、`.github/workflows/` 变更。

### python -m pytest

```text
python -m pytest: not_run — docs / audit / decision-prep only; no runtime, tests, config, or baseline changes.
```

未运行 pytest 的理由：本轮 PR 为纯文档/审计/决策准备类型，未修改 parser runtime、测试、配置或 baseline。task 文件（Section 18）明确允许 docs/audit/decision-prep PR 不强制运行 pytest，但要求如实记录。

## Deviations from task package

| 项目 | 任务书要求 | 实际执行 | 说明 |
|---|---|---|---|
| Task package 文件 | 创建 `tasks/2026-06-xx_R1_workbook_export_consistency_task_package.md` | 未单独创建 | 本任务书（`d:\任务文件\3.0pricing_parser_R1_workbook_export_consistency_audit_decision_prep.md`）本身即为完整的 task package，已包含 scope、boundary、structure、acceptance criteria。再创建一份 task package 文件会重复任务书内容。本执行报告和审计报告已承担 task package 的记录功能。 |
| `docs/status.md` 更新 | 轻量更新（可选） | 未更新 | 任务书允许仅当需要记录 R1-P1 审计完成状态时轻量更新。当前 `docs/status.md` 已标注"R0 收尾，准备进入 R1"，R1-P1 审计报告和 decision note 本身即为 R1 阶段的记录。建议在 R1-P2 实现完成后一并更新 `docs/status.md`。 |
| `docs/roadmap.md` 更新 | 可选补充 | 未修改 | 审计未发现 R1 描述有明显需要补充的内容。 |

## Risks and follow-ups

- **日期派生文件名**：当前所有 raw 样本日期均为 `2025-03-27`，baseline 文件名固定。如果将来添加不同日期的样本，需同步更新 `data_samples/expected/` 中的 workbook baseline 文件名和测试中的硬编码断言。此风险已在 owner decision note（Decision 4）中提出。
- **Workbook sheet 名称硬编码**：`write_excel_workbook()` 中的 sheet 名称（`"routing_results"` 等）为内联字符串字面量，不与 CSV 文件名常量联动。虽然当前稳定，但如果在 P2 中将 sheet 名称提取为常量可进一步降低维护风险。
- **P2 实现已解除依赖**：5 项 owner decision 已全部确认（见上方），P2 可按 confirmed direction 直接实施。

## Owner decisions (confirmed)

Owner Decision Note（`tasks/2026-06-16_R1_workbook_baseline_owner_decision_note.md`）中 5 项决策已由 owner 确认：

1. **Decision 1**：✅ **confirmed** — 采用选项 B。Workbook 定位为 CSV 的 Excel 镜像 / 人工友好派生物，不作为独立权威产物。
2. **Decision 2**：✅ **confirmed** — 维持当前 sheet-content / structured read comparison 口径，不升级为二进制验收。
3. **Decision 3**：✅ **confirmed** — CSV 为语义权威。若 CSV 与 workbook 不一致，应视为 bug，但判断和修复应优先回到 CSV、字段常量和 `to_row()` 数据源。
4. **Decision 4**：✅ **confirmed** — 保持当前日期派生文件名规则，不在本轮修改 runtime 文件名行为。在 R1-P2 中纳入 regression test。
5. **Decision 5**：✅ **confirmed** — 授权进入 R1-P2: workbook ↔ CSV consistency regression implementation。R1-P2 只允许新增 focused tests，不改 runtime、不刷新 baseline、不处理 R2/R3/R4 内容。

## Recommended next PR

建议下一步根据 owner decision 进入 **R1-P2**：

```text
R1-P2：workbook ↔ CSV consistency regression implementation
```

R1-P2 才允许新增 focused tests，按实习生推荐优先级：

**P0（优先实现）**：
- workbook 行数与 CSV 输出一致（Test 3）
- 抽样稳定值跨格式一致（Test 4）
- 日期派生文件名确定性（Test 5）

**P2（可选）**：
- workbook sheet names 与预期集合一致（Test 1）
- workbook 表头匹配 `*_FIELDS` 常量（Test 2）

如果 R1-P1 审计发现需要 runtime / baseline 变更，必须先由 owner 明确批准，再设计 R1-P3。

## Intern learning notes

1. **只读审计优先**：在了解代码库之前先通读所有相关文件，形成全局视图后再写结论。任务书明确禁止"顺手修"，必须遵守。
2. **事实源边界**：`docs/status.md`（现在是什么）vs `docs/roadmap.md`（接下来怎么排）vs `tasks/*.md`（某一轮怎么做）的职责分离设计很有价值，写执行报告时应保持这个边界。
3. **字段常量的架构意义**：`exporters.py` 中共享 `*_FIELDS` 常量的设计看似简单，但它从根本上防止了 CSV 和 workbook 之间的字段漂移——这是"正确的设计让 bug 无法产生"的好例子。
4. **.xlsx 作为 baseline 的权衡**：二进制格式不适合 Git diff，但 `openpyxl` 结构化读取提供了折中方案——保持内容级验证的同时避免字节级噪声。
5. **Owner decision 的边界感**：实习生可以整理选项、分析利弊、提出推荐，但最终策略必须由 owner 确认。报告中明确区分"推荐"和"pending — 待 owner 确认"是正确的做法。
