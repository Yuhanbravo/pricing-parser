# 审查结论摘要

- 总评：`基本通过但需修正`
- 推荐结论：`需先修正后再继续`
- 风险等级：`中`

# 1. 项目总体判断

这个仓库已经不是“脚本 demo 态”，而是一个有清晰分层、可实际跑通样本、并且具备多 adapter 扩展骨架的解析器雏形。主入口、路由层、映射加载、身份提取、标准化、导出层都已独立存在，结构上基本符合任务书要求。最明显的优点是：真实样本集可以端到端跑通，且多家托管机构适配没有退化成按产品堆 if-else。最明显的问题不是“跑不起来”，而是“交付口径开始分叉”：当前代码、测试、expected、README/HANDOFF 对外输出契约并不完全对齐任务书。尤其 `valuation_subjects` / `valuation_positions` 的 trace 字段在模型层存在、但在导出层被裁掉，这会直接影响验收与并主线。整体上它符合“估值表解析器”的目标定位，但当前更像“内部受控样本验证版”，还不到可以无条件并入主线的状态。

# 2. 需求对齐检查表

| 项目 | 状态 | 说明 |
| --- | --- | --- |
| 读取估值表 | 已完成 | `.xls/.xlsx` 已在本轮实跑样本中验证，`data_samples/raw/` 全量 11 个文件可跑通。 |
| 读取映射表 | 部分完成 | `.csv` 已实跑；`.xlsx` 代码路径存在，但本轮没有用真实 `.xlsx` mapping 样本复验。 |
| 产品身份提取 | 已完成 | 文件名、sheet 名、header preview 三路提取均已实现，并有对应测试。 |
| 自动路由 | 部分完成 | mapping-driven routing 主链路可用，但存在未命中 mapping 时被 `generic` fallback 提升为成功路由的偏离。 |
| 手动 adapter override | 已完成 | CLI 参数存在，且本轮实跑 `--adapter generic` 得到 `manual_override` 路由结果。 |
| 科目结构识别 | 已完成 | 科目行提取、层级标注、父子关系与叶子判断均已实现。 |
| 持仓叶子识别 | 已完成 | 多个 adapter 样本都能抽出 position 叶子。 |
| 证券代码标准化 | 已完成 | `SH/SZ/HK` 规则与 ETF/fund 基础判断已实现，并有测试覆盖。 |
| 输出 subjects | 部分完成 | 文件能输出，但当前导出字段缺少任务书要求的 `source_file/product_id/association_code/custodian_id/adapter_key/route_source` 等 trace。 |
| 输出 positions | 部分完成 | 文件能输出，但同样缺少关键 trace 字段，且 `review_flag` 使用面偏弱。 |
| 输出 routing_results | 已完成 | 当前输出包含 `route_source / route_status / route_message`，这一点是达标的。 |
| 输出 summary | 部分完成 | 基本统计项存在，但未展开“哪些未识别/哪些需人工复核”的明细口径，且 fallback 路由也被计入成功。 |
| smoke test | 已完成 | 仓库内有 smoke test；本轮还做了真实 CLI/pipeline 最小运行验证。 |

# 3. 架构审查

当前分层总体是合理的：`cli -> pipeline -> routing/mapping/identity -> adapter -> exporter` 的主链路清楚，`routing.py`、`mapping_loader.py`、`product_identity.py`、`normalizers.py` 也都独立存在。adapter 设计方向是对的，主要按托管机构分层，并通过 YAML 配置复用共享 tabular parser，没有退化成按产品写分支脚本。最大的架构问题不在“内部耦合”，而在“外部契约断层”：`models.py` 里的 `SubjectRecord` / `PositionRecord` 已经带有完整 trace 元数据，但 `exporters.py` 把这些字段裁掉了，导致内部信息比外部交付更完整。routing 本身是独立的，但 `pipeline.py` 又在路由失败后加入了 `generic` layout fallback，把“未命中 mapping”改写成“成功解析”，这削弱了 routing 层的边界清晰度。

# 4. 运行与测试审查

- 通过：`D:\miniforge3\envs\dev-core-py312\python.exe -m valuation_parser.cli --help`，CLI 参数与任务书/README 基本一致。
- 通过：单样本实跑 `证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx`，成功生成 `routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv`、`review_items.csv`、`parse_summary.md`、`phase3_outputs.xlsx`。
- 通过：全量实跑 `data_samples/raw/`，得到 11 文件、11 成功路由、1113 条 subjects、202 条 positions、253 条 review items，与 README / HANDOFF 口径数值一致。
- 通过：`pytest -q tests/test_routing.py tests/test_product_identity.py tests/test_code_normalizer.py tests/test_adapter_sample.py tests/test_phase5_adapters.py tests/test_review_items.py -p no:cacheprovider`，结果 `21 passed in 0.45s`。
- 受当前沙箱环境限制未能正常结束：`tests/test_smoke.py` 与 `tests/test_mapping_loader.py` 依赖 `tmp_path`，默认临时目录落在 `C:\Users\liuyuhan\AppData\Local\Temp\pytest-of-liuyuhan`，本轮命中 `WinError 5` 权限拒绝；这是当前运行环境限制，不足以单独判定项目代码失败。
- 当前测试足以证明“核心骨架可跑”，但还不足以支撑“按任务书验收”，因为没有测试锁定任务书要求的输出字段契约，也没有测试约束 mapping 中 `adapter_key` 必须在注册表中存在。
- 本轮未改源码；最小验证只写入了已忽略目录 `output/review_run_single`、`output/review_run_full`、`output/review_run_override`。

# 5. 输出与口径审查

`routing_results.csv` 是目前最接近任务书定义的输出，字段齐全，`route_source / route_status / route_message` 也都真实记录了。问题主要集中在 `valuation_subjects.csv` 和 `valuation_positions.csv`：当前实际生成的表头以 `broker,sheet_name,...` 开头，缺少任务书要求的来源文件、产品身份、custodian、adapter、route trace 等核心字段。更关键的是，仓库里已跟踪的 `output_phase1/valuation_subjects.csv` 仍保留这些 trace 字段，而当前代码新跑出来的输出却没有，说明仓库内“历史产物”和“当前导出实现”已经分叉。`data_samples/expected/估值表解析_expected_output_2025-12-01.xlsx` 也只覆盖 `valuation_subjects / valuation_positions / review_items`，没有把 `routing_results` 和 `parse_summary` 纳入 expected 范围，因此它更像 parser 视角的样表基线，不是完整交付契约。`review_flag` 目前更多只是 normalization 标志；我实跑全量样本时 `valuation_positions.csv` 里 202 条持仓的 `review_flag` 全为空，但 `review_items.csv` 有 253 条，这说明“人工复核口径”实际主要落在 `review_items`，`review_flag` 并没有承担主审查入口。

# 6. Git 与提交规范审查

Git 历史整体比一般实习生项目要好，9 条提交能看出从初始化、routing、首个 adapter、Phase 4、Phase 5 到文档收口的阶段性推进，也没有出现大量 `update / misc / fix bug` 这类低信息量 subject。大多数提交使用了 `feat/docs/chore` 等约定类型，方向上符合轻量结构化规范。问题在于部分提交过宽：`36f9a57 feat(valuation-parser): complete Phase 4 with enhanced review and routing logic` 一次混入配置、adapter、pipeline、测试、文档和样本文件调整，已经超出了“一个主要动作”的理想粒度；`bf02bae docs: refresh all documentation after Phase 5` 也偏宽泛。结论是：commit message 质量总体合格，但粒度控制仍可再收敛，尤其阶段性大提交仍有“多种改动压成一条”的倾向。

# 7. 问题清单（按优先级排序）

## P0（必须先修）

- 标题：`valuation_subjects` / `valuation_positions` 导出字段不满足任务书 trace 要求。位置：`src/valuation_parser/exporters.py:23`、`src/valuation_parser/exporters.py:48`、`src/valuation_parser/exporters.py:156`、`src/valuation_parser/models.py:55`、`src/valuation_parser/models.py:91`、`tests/test_smoke.py:42`。问题说明：模型层明明保留了 `source_file/product_id/association_code/custodian_id/custodian_name/adapter_key/route_source`，但 exporter 只导出精简列，并通过 `extrasaction="ignore"` 直接丢弃额外字段；本轮真实运行结果也证实当前 CSV 缺这些列。为什么重要：这直接不满足任务书的输出定义和原始痕迹保留要求，会阻碍验收、回查和后续落库接入。
- 标题：mapping loader 没有校验 `adapter_key` 是否存在于注册表。位置：`src/valuation_parser/mapping_loader.py:39`、`src/valuation_parser/mapping_loader.py:53`、`src/valuation_parser/mapping_loader.py:195`。问题说明：当前 `_validate_records()` 只检查空值和重复，不检查 `adapter_key` 是否已注册；我用内联验证构造 `adapter_key='not_registered'` 的 `MappingRecord`，校验直接通过。为什么重要：这违背任务书对 mapping loader 的要求，也会让 mapping 错误从“加载期可控失败”拖到“运行期 KeyError”才暴露。
- 标题：未命中 mapping 的文件会被 `generic` fallback 记为成功路由。位置：`src/valuation_parser/pipeline.py:39`、`src/valuation_parser/pipeline.py:80`、`tests/test_smoke.py:112`。问题说明：`route_identity()` 已经返回失败时，`pipeline.py` 会根据表头布局把它改写成 `layout_fallback(generic)` 成功；本轮全量实跑里 `PRODUCT_022` 就是这种情况，因此 summary 显示 `Routing failures: 0`。为什么重要：这会高估 mapping 覆盖率，削弱“显式 mapping 才是路由主依据”的任务书边界，对后续生产接入是高风险信号。

## P1（建议尽快修）

- 标题：README / HANDOFF / status 与仓库内实际产物存在口径分叉。位置：`README.md:30`、`README.md:32`、`docs/status.md:11`、`docs/HANDOFF.md:10`、`output_phase1/`。问题说明：文档反复写“最新验证产物在 `output_phase5/`”，但仓库里实际跟踪的是 `output_phase1/`；而且 `output_phase1` 的 CSV 表头和当前 exporter 新生成结果也不一致。为什么重要：这会削弱 handoff 可信度，别人接手时很难判断哪个输出才是当前真实契约。
- 标题：`review_flag` 没有承担实际人工复核入口。位置：`src/valuation_parser/adapters/base.py:49`、`src/valuation_parser/adapters/base.py:71`、`src/valuation_parser/normalizers.py:40`。问题说明：当前 position 级 `review_flag` 只在 normalization / asset_type 推断失败时触发，而大量真正需要复核的情况被单独写进 `review_items.csv`；本轮全量运行出现“253 条 review_items、0 条 review_flag”的割裂。为什么重要：任务书明确关心 `review_flag` 的实际用途；现在这个字段对外看起来存在，但并不是主复核机制。
- 标题：测试覆盖锁定了“当前样例口径”，没有锁定“任务书契约”。位置：`tests/test_smoke.py:42`、`tests/test_smoke.py:65`、`data_samples/expected/估值表解析_expected_output_2025-12-01.xlsx`。问题说明：现有 smoke / expected 主要断言的是 `broker,...` 这一套精简导出口径，并把 `layout_fallback(generic)` 当作正向覆盖点，但没有约束任务书要求的 trace 字段和严格 mapping 校验。为什么重要：这意味着项目即使继续“全部测试通过”，也可能继续偏离验收口径。

## P2（优化项）

- 标题：工作簿产物名仍是历史性的 `phase3_outputs.xlsx`。位置：`src/valuation_parser/pipeline.py:55`、`README.md:30`、`docs/status.md:32`。问题说明：代码和文档都把这个问题当作“兼容性保留”，但它仍然把当前 Phase 5 交付和旧 phase 标签耦合在一起。为什么重要：不是功能阻塞，但会持续制造沟通噪音和误判。
- 标题：expected output 只覆盖 parser 结果，不覆盖完整交付物。位置：`data_samples/expected/估值表解析_expected_output_2025-12-01.xlsx`。问题说明：该 expected workbook 没有 `routing_results` 和 `parse_summary` 对照面。为什么重要：它能帮助收敛表结构，但还不足以承担完整验收基线。
- 标题：Phase 4 提交粒度偏大。位置：Git 提交 `36f9a57`。问题说明：一次提交混入 parser、adapter、config、tests、docs 和样本文件调整。为什么重要：后续定位回归来源、做 selective cherry-pick 或 handoff 回看时会变重。

# 8. 是否建议进入下一阶段

- 是否建议继续由实习生推进：`建议继续，但不建议直接并主线后再推进。`
- 是否建议先做一轮修复再推进：`建议，且这轮修复应是明确的“契约收口包”。`
- 是否建议你本人接手重整：`暂不建议。当前骨架没坏到需要推倒重来，更适合让实习生补齐 contract / validation / docs 三件事；如果下一轮仍无法收口，再考虑接手重整。`
- 推荐下一轮任务包应聚焦：`1）导出字段与任务书对齐；2）mapping 校验严格化；3）generic fallback 的治理；4）expected / smoke / docs 统一到同一份外部契约。`

# 9. 最小修正建议

1. 先把 `valuation_subjects` 和 `valuation_positions` 的导出字段补回任务书要求的 trace 列，再重生 expected 和示例输出。
2. 在 `load_mapping()` 阶段增加 `adapter_key in registry` 校验，禁止把 mapping 错误拖到运行期。
3. 把 `layout_fallback(generic)` 改成显式可配置的开发态行为，默认不要计入“成功自动路由”。
4. 新增一组“契约测试”，直接断言 subjects/positions/routing/summary 的必需字段和 summary 口径。
5. 统一 `review_flag` 与 `review_items` 的职责，要么让 `review_flag` 真正映射主要复核场景，要么在 README/summary 中明确它只是 normalization flag。
6. 清理文档与产物证据链：要么补齐 `output_phase5` 的可复验证据，要么把 README/HANDOFF 改成只引用当前仓库真实存在、且与现代码一致的输出。