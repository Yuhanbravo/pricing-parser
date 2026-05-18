# 第二轮复审结论摘要

> 历史快照：本文记录第二轮复审时的仓库状态与遗留问题，保留用于回看修复过程，不代表当前代码、基线或交付物的最新事实。当前权威口径以 `README.md`、`docs/HANDOFF.md`、`docs/status.md`、`data_samples/expected/` 与最新 strict-default 输出为准。

- 总评：`基本通过但仍需修正`
- 推荐结论：`需再修一轮`
- 风险等级：`中`

# 1. 第二轮提交总体判断

这轮提交的主线是明确的契约收口，核心起点就是 `d4d41fc`，后续 11 个 commit 基本都在围绕第一轮提出的导出 trace、mapping 严格校验、strict routing、review 契约、summary 口径和文档同步继续补洞。  
从代码和最小复跑结果看，第一轮最硬的 3 个 P0 已基本打掉：`valuation_subjects/positions` 现在真的导出 trace 字段，`mapping_loader` 会在加载期拒绝未知 `adapter_key`，默认路径下 `PRODUCT_022` 也不再被静默提升为成功路由。  
最大改进是“外部契约终于开始落到真实输出上”，不再只是模型层有字段、文档层有说法。  
最大遗留问题是“证据链还没完全收口”：`README/HANDOFF/status` 的运行数字与当前实跑/expected 仍有漂移，`data_samples/expected/` 反而删掉了旧 workbook baseline，只剩 `parse_summary.md`，而仓库里还保留着旧的 `output_phase1/*` 和过期 governance report。  
因此它已经从“第一轮的明显不达标”提升到了“主问题修得差不多”，但还没到我会直接判定“可进入并主线前复审”的程度。  
以下判断以 `HEAD` 为主，忽略当前工作区把任务书与 commit convention 文档移入 `任务书集合/` 的未提交整理。

# 2. 新旧版本差异概览

- `oldbundle/master..HEAD` 共新增 `12` 个 commit，主线清晰。
- 主要新增 commit：
  - `d4d41fc`：trace 字段导出、`adapter_key` 注册校验、generic fallback 改显式、smoke/expected/doc 首轮收口。
  - `6730a61`：README/HANDOFF/status 改成 strict routing 叙事。
  - `025af9c`、`4df3c9a`、`6c290a7`：`review_flag` 改为二值 `1`，并把 review reason 收到 `review_note` / `review_items`。
  - `9fe06ee`、`4a37706`：workbook 命名从历史 `phase3_outputs.xlsx` 收口到按日期命名。
  - `3de6799`：`routing_results.csv` 输出标准化 `custodian_name_chinese`。
  - `f28260c`、`57df62a`、`8be1abd`：`parse_summary.md` 增加资产类型和 flagged subjects 统计，并清理旧 expected workbook。
  - `8b393b2`：`正常交易` 文本标准化。
- 改动最集中的模块是 `src/valuation_parser/exporters.py`、`pipeline.py`、`mapping_loader.py`、`adapters/base.py`、`routing.py`、`tests/test_smoke.py`，以及 `README.md`、`docs/HANDOFF.md`、`docs/status.md`。
- 这轮主要属于：`契约收口`、`输出修复`、`review 收紧`、`docs 对齐`、`测试增强`；不是扩新功能为主。

# 3. 第一轮审查问题完成度对照表

| 第一轮问题 | 上轮级别 | 本轮状态 | 证据 | 判断 |
| --- | --- | --- | --- | --- |
| trace 字段缺失 | P0 | 已修 | `src/valuation_parser/exporters.py:23-84` 已加入 `source_file/product_id/association_code/custodian_id/custodian_name/adapter_key/route_source`；`tests/test_smoke.py:6-14,54-63` 锁表头；最小复跑输出表头与之吻合 | 这是本轮最实的修复，已经从“模型有、导出无”变成“导出与 smoke 都锁住” |
| `adapter_key` 未校验 | P0 | 已修 | `src/valuation_parser/mapping_loader.py:196-205` 新增 `SUPPORTED_ADAPTERS` 校验；`tests/test_mapping_loader.py:25-34` 直接断言未知 key 抛错；我手工构造 `.xlsx` mapping 也能正常加载合法 key | 已从运行期问题前移到加载期失败，符合任务书 `6.2` |
| fallback 误记成功 | P0 | 已修 | `src/valuation_parser/pipeline.py:42-47,104-115` 只有显式 `allow_generic_fallback=True` 才启用 fallback；`src/valuation_parser/cli.py:26-30` 暴露显式开关；`tests/test_smoke.py:151-177` 同时锁 strict default 和 opt-in fallback；最小复跑默认 10 成功 1 失败，开启后才变 11 成功 | 路由边界明显收紧，第一轮最危险的口径偏差已消除 |
| docs / outputs 分叉 | P1 | 部分修 | `README.md:30-39`、`docs/HANDOFF.md:15-19`、`docs/status.md:16-18` 叙事已收紧；但 `README.md:36`、`docs/HANDOFF.md:33`、`docs/status.md:13` 仍写 `242 review items`，而 `data_samples/expected/parse_summary.md:12` 与实跑结果都是 `238`；仓库还保留旧 `output_phase1/*` 与过期 `docs/documentation_governance_report.md:20-33` | 主文档方向对了，但“仓库里所有证据都在说同一件事”这件事还没做到 |
| `review_flag` 职责不清 | P1 | 部分修 | `src/valuation_parser/normalizers.py:42-53`、`src/valuation_parser/adapters/base.py:45-107,215-229` 已把 `review_flag` 收成二值标记，`review_note`/`review_items` 承担原因；`tests/test_review_items.py:37-50` 验证衍生品场景；但当前全量复跑 summary 仍是 `238 flagged subjects / 0 flagged positions / 238 review items` | 关系比上轮清楚很多，但“positions 级 review 入口”在当前主样本集上仍缺少有力运行证据 |
| 契约测试不足 | P1 | 部分修 | `tests/test_smoke.py` 现在直接断言 trace 表头、strict routing、fallback 开关；`tests/test_exporters.py:7-71` 新增 summary 契约；但 `data_samples/expected/` 只剩 `parse_summary.md`，仓库内没有当前 CSV/workbook 的完整 acceptance baseline，也没有仓库内自动化的 `.xlsx` mapping 测试 | 已不再是“完全没锁”，但还没到“完整验收基线已固化” |

# 4. 对任务书的对齐度（第二轮后）

- 已真正满足的要求：
  - `product_id -> custodian_id -> adapter_key` 可追踪，且 subjects/positions/routing 三类导出都能看到主链 trace，符合任务书 `5.2`、`6.6`。
  - `mapping_loader` 对 `adapter_key` 做注册表校验，符合任务书 `6.2`。
  - 路由优先级重新回到“显式 mapping 为主、generic 仅显式启用”，符合任务书 `6.3`。
  - `.xlsx` mapping 路径代码可跑，我做了手工 smoke，能成功读入 1 条 canonical mapping。
- 仍然只做到“内部结构/局部证据有了”的地方：
  - `parse_summary.md` 目前还是聚合计数为主，没有把“哪些记录未识别/哪些需要人工复核”明确展开到 summary 本体，和任务书 `目标 H` 仍有距离。
  - `review_flag` / `review_items` / `parse_summary` 的职责边界已能解释清楚，但仓库当前主样本的运行证据仍主要落在 `review_items` 和 flagged subjects，不够像最终验收口径。
  - expected 基线没有完整覆盖 `routing_results.csv`、CSV 契约和 workbook 导出。
- 已从“可跑”升级到“可验收一部分”的地方：
  - strict default routing、trace 导出、mapping 注册校验、workbook 命名，这四项现在都不只是代码里有，而是文档、smoke、最小复跑都能对应上。

# 5. 运行与测试复核

- 实际运行通过：
  - `D:\miniforge3\envs\prod-core-py312\python.exe -m valuation_parser.cli --help`
  - 直接调用 `run_pipeline('data_samples/raw', '产品与托管机构映射表.csv', ...)`，默认得到 `10 successful routes / 1 routing failure / 1022 subjects / 182 positions / 238 review items`
  - 同一管线在 `allow_generic_fallback=True` 下得到 `11 successful routes / 0 routing failures / 1113 subjects / 202 positions / 247 review items`
  - 手工 `.xlsx` mapping smoke：成功读入 1 条 canonical mapping 记录
- 实际失败：
  - 默认 `python` 无项目依赖，也没有 `pytest`
  - `dev-core-py312` 在导入 `openpyxl` 时发生环境级崩溃
  - `prod-core-py312` 下运行 `pytest` 时，`tmp_path` 统一卡在 `C:\Users\Public\Documents\Wondershare\CreatorTemp\pytest-of-imado` 的 `PermissionError [WinError 5]`
- 测试结论：
  - 在这次运行里，`pytest` 结果是 `5 passed, 9 errors`；9 个错误都发生在 `tmp_path` fixture setup，不是仓库断言失败。
  - 因此我认可“本轮关键修复已有较强静态和最小复跑证据”，但还不能说“自动化验收已经完整、稳定、可复现”。

# 6. Git 历史与 tag 审查

- 第二轮 commit 质量总体是中上：12 条提交能看出从“第一轮问题”到“第二轮修复”的映射关系，主线不乱。
- 过宽提交仍然存在：
  - `d4d41fc` 一条里混了 exporter、mapping、pipeline、tests、expected、bundle、任务文档，粒度偏大。
  - `6730a61` 没有按轻量 convention 使用 `type(scope): action`，而且 message 说“Generate output_phase6 baseline”，但仓库并没有对应的受控 baseline 提交。
- 按 `任务书集合/单项目 Commit Convention（轻量版）:27-58,202-237`，本轮历史是“基本合格但不够整齐”，不是高质量示范。
- 当前 tag 情况：
  - `git tag --list` 为空
  - `HEAD` 没有命中任何 tag
- 是否建议补 tag：
  - `建议等修完最后一轮证据链问题后再补`
- 推荐 tag 方案：
  - `review-round1-baseline` 指向 `oldbundle/master` / `bf02bae`
  - `review-round2-candidate` 指向“清完 docs/expected/output 漂移后的下一提交”
  - 如果后续需要更产品化命名，再加一层 `v0.1-round1`、`v0.2-round2-candidate`；当前我更推荐 review-oriented tag，而不是先上 semver

# 7. 当前遗留问题（按优先级排序）

## P0（还必须修）

- 外部证据链还没完全收口。`README.md:36`、`docs/HANDOFF.md:33`、`docs/status.md:13` 仍写 `242 review items`，但当前 expected 与实跑都是 `238`；同时 `data_samples/expected/` 只剩 `parse_summary.md`，仓库又还保留旧 `output_phase1/*` 和过期 `docs/documentation_governance_report.md`。这会直接影响“并主线前复审”对当前契约的判断。

## P1（建议尽快修）

- `parse_summary.md` 仍以计数为主，没有把未识别文件/需复核对象在 summary 本体中说清楚，和任务书对 summary 的外部可读性要求还有差距。
- `review_flag` 契约比第一轮清楚很多，但在当前主样本全量运行中仍表现为 `238 flagged subjects / 0 flagged positions / 238 review items`，说明“position 级人工复核入口”还缺少强证据。
- 自动化验证还没完全落地为可复现验收。仓库内没有当前 CSV/workbook 的完整 acceptance baseline，`.xlsx` mapping 也只有代码路径和本轮手工 smoke，没有仓库内自动化回归。

## P2（优化项）

- `docs/documentation_governance_report.*` 已经明显过期，容易误导接手人。
- 第二轮 Git 历史已有清晰主线，但还缺一个轻量 milestone tag，后续回看 review 节点成本偏高。
- `pricing_parser.bundle` 出现在第二轮主修复提交里，会增加历史噪音，不利于把代码修复与协作工件分开阅读。

# 8. 是否建议进入下一阶段

- 是否建议继续由实习生推进：`建议继续`
- 是否建议先再修一轮：`建议`
- 是否已经可以进入“并主线前复审”：`不建议现在进入`
- 推荐下一轮任务包应聚焦什么：`只做证据链收口包`，聚焦 `docs/expected/output` 同步、summary 口径补齐、acceptance baseline 固化、补 tag

# 9. 最小后续建议

1. 先把 `README/HANDOFF/status` 的统计数字统一到当前真实结果，至少修正 `242 -> 238 review items` 这一处显性漂移。  
2. 为当前 strict-default 路径补一份权威 acceptance baseline，至少覆盖 `routing_results.csv`、`valuation_subjects.csv`、`valuation_positions.csv` 和 workbook 结构。  
3. 明确 `output_phase1/*` 与 `docs/documentation_governance_report.*` 的地位：要么删掉，要么显式标注为历史材料，避免和当前契约并列。  
4. 给 `.xlsx` mapping 加一个仓库内自动化测试，不再只依赖手工 smoke。  
5. 再补一次 summary 契约：至少把未路由样本和 review 入口说明写清楚，而不只报总数。  
6. 收完上面几项后再打 tag；优先补 `review-round1-baseline` 和 `review-round2-candidate`。
