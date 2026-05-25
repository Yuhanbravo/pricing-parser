# Need Review: Evidence Chain Closure

> Historical snapshot: this need-review note records the pre-closure assessment as of 2026-04-27. It may intentionally describe drift that has since been resolved; use the current project docs and baselines for live status.

## 1. 当前项目状态是什么？

项目已经从“能跑但契约外漏”的第一轮状态，推进到“核心外部契约基本修正完成，但证据链仍未完全统一”的第二轮后状态。

- 第一轮暴露的核心 P0 已在第二轮大体修正：`valuation_subjects.csv` / `valuation_positions.csv` 已真实导出 trace 字段，`mapping_loader` 已拒绝未知 `adapter_key`，strict-default 路径下未命中 mapping 的文件不再被静默计入成功路由。
- 当前代码、输出和测试已经证明解析器主链可用：支持 11 份受控样本的 routing、subjects、positions、review_items 和 summary 导出。
- 当前项目仍不能直接判定为“可进入并主线前复审”，原因不是核心解析链路失效，而是 docs / expected / outputs / tests / summary / tag 之间仍有证据漂移。
- 最直接的漂移已经可见：当前 [output/parse_summary.md](../output/parse_summary.md) 和 [data_samples/expected/parse_summary.md](../data_samples/expected/parse_summary.md) 都是 `238 review items`，但 [README.md](../README.md)、[docs/HANDOFF.md](../docs/HANDOFF.md) 和 [docs/status.md](../docs/status.md) 仍写 `242 review items`。
- 仓库里还同时保留旧阶段产物和过期治理报告，接手人难以一眼判断“当前契约”究竟以哪一组文档和输出为准。

结论：项目当前适合进入第三轮，但第三轮的定位必须是“证据链收口”，而不是继续扩展解析能力。

## 2. 第三轮为什么只做证据链收口？

第三轮只做证据链收口，是因为本项目的主要风险已经从“功能缺失”转移到“交付口径不统一”。

- 项目任务书要求的主干能力已经具备，第二轮也已修掉最关键的结构性偏差。
- 目前剩余问题集中在验收层和交接层：文档数字漂移、expected baseline 不完整、summary 说明不够外显、历史产物与当前产物并列造成误导、tag 策略缺失。
- 如果现在继续扩展 adapter、资产类型或核心算法，只会把审阅范围重新放大，让第三轮无法成为稳定的验收节点。
- 结合 [估值表解析器项目任务书.md](../估值表解析器项目任务书.md)、第一轮与第二轮审查摘要，最合理的下一步不是继续“做更多”，而是把现有结论统一成一套可信、可复审、可接手的证据链。

结论：第三轮的目标应是把现有结果收口成一个可供 AI 复审和人工合并决策使用的稳定候选节点。

## 3. 本轮必须修哪些问题？

本轮必须修的问题应严格围绕第二轮遗留证据漂移展开。

### P0：必须修

1. 统一 `README / HANDOFF / status / parse_summary / expected` 的统计数字和项目状态描述，至少先消除 `242 -> 238 review items` 这一类显性漂移。
2. 为当前 strict-default 路径补齐 acceptance baseline，不能只剩一份 `parse_summary.md`，至少要覆盖：
   - `routing_results.csv`
   - `valuation_subjects.csv`
   - `valuation_positions.csv`
   - `parse_summary.md`
   - workbook 结构说明
3. 把历史产物和当前契约关系说明清楚，避免 `output_phase1/*`、旧 baseline、过期治理报告与当前输出并列造成误判。

### P1：应在本轮一起收口

1. 补 `.xlsx` mapping` 的仓库内自动化测试，不再只依赖第二轮手工 smoke 结论。
2. 调整 `parse_summary.md` 的说明口径，使其不只报总数，还能说明：
   - routing success
   - routing failure
   - generic fallback 的启用条件
   - review 入口
   - flagged subjects / positions / review items 的关系
3. 在 handoff/status 级文档中明确 tag 建议与打 tag 的条件。

### P2：如不超边界可同步处理

1. 对过期的治理报告或旧输出目录做历史标注。
2. 让 review reader 能一眼区分“当前权威证据”和“历史参考材料”。

## 4. 哪些事情明确不做？

本轮明确不做以下事项：

- 不新增托管机构 adapter。
- 不新增资产类型解析规则。
- 不修改核心解析算法、路由主逻辑或脱敏逻辑。
- 不引入 Wind、Oracle、生产系统或任何真实敏感数据。
- 不做大规模重构。
- 不引入新的复杂依赖。
- 不把 bundle 文件作为本轮常规源码资产提交。
- 不顺手做与证据链收口无直接关系的 cleanup。

结论：本轮是验收与交接层的 bounded execution，不是功能开发轮。

## 5. 预计涉及哪些文件？

根据当前遗留问题，本轮预计涉及文件应集中在 docs、expected、tests 和少量 summary/export 面。

### 核心文档与状态面

- [README.md](../README.md)
- [docs/HANDOFF.md](../docs/HANDOFF.md)
- [docs/status.md](../docs/status.md)

### expected 与输出基线面

- [data_samples/expected/parse_summary.md](../data_samples/expected/parse_summary.md)
- `data_samples/expected/` 下新增或整理的 CSV / workbook 结构基线
- 可能需要补充对历史输出目录的标注文档

### 测试与契约面

- `tests/` 下与 mapping、summary、exporter、smoke baseline 相关的测试文件
- 特别是 `.xlsx` mapping 自动化回归测试文件

### 如 summary 口径需要代码配合

- `src/valuation_parser/exporters.py`
- `src/valuation_parser/pipeline.py`

说明：若 summary 口径已可通过现有导出结果和测试收口，则应避免扩大到更多源码模块。

### 本轮流程文档

- [tasks/2026-04-27_evidence_chain_closure_need_review.md](2026-04-27_evidence_chain_closure_need_review.md)
- 后续将继续生成对应的 task package、execution report 和 AI review report

## 6. 本轮完成后如何验收？

本轮完成后的验收应以“证据链是否已经说同一件事”为核心，而不是只看解析器能否运行。

### 最低验收标准

1. `README / HANDOFF / status` 的数字与当前 strict-default 实跑结果一致。
2. `data_samples/expected/` 能覆盖本轮关键交付物，而不是只剩单一 summary 文件。
3. `.xlsx` mapping 已有仓库内自动化测试。
4. `parse_summary.md` 已明确说明未路由样本、fallback 条件和 review 入口。
5. 历史产物不会再与当前契约并列混淆。
6. tag 策略已经形成书面建议。
7. 测试通过；若受环境阻塞未全部通过，阻塞原因必须被明确记录到执行报告。

### 完成判断

- 若上述条件全部满足，可进入“并主线前复审”候选状态。
- 若仍存在 1 到 2 个轻微漂移，则应判定为“仍需小修”，而不是直接宣布收口完成。
- 若本轮执行过程中扩展了新功能或无法证明 docs / expected / outputs / tests 的一致性，则视为偏离第三轮目标。

## Assumptions

- “第二轮复审报告”在当前仓库内以 [任务书集合/pricing_parser第二轮审查结论摘要.md](../任务书集合/pricing_parser第二轮审查结论摘要.md) 作为可执行输入来源。
- 本文仅作为 Step 1 的需求审合摘要，不替代后续正式 task package。