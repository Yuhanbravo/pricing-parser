# 单项目 Commit Convention（轻量版）
## —— 适配当前 Python / migration 项目的定制示例版

## 0. 目的

本规范用于统一单个 Python 项目中的 commit message 写法，尤其适用于以下类型的长期维护项目：

- 迁移 / 重构类项目
- 数据处理 / ETL / 解析类项目
- 带 `HANDOFF.md`、`status.md`、`migration plan` 的项目
- 有 AI 参与开发、需要后续重新接管的项目
- 强调“边界不动、主流程不动、渐进式收敛”的项目

本规范的目标不是把提交写得更正式，而是让提交历史具备这些价值：

- 快速看懂“本次改动做了什么”
- 区分功能、修复、重构、文档、测试等不同类型改动
- 为 handoff / status / AI takeover 提供清晰时间线
- 与项目文档形成分工，而不是互相替代

本项目采用：

> 轻量结构化、默认单行、必要时带 scope 或 phase 的 commit 规范

---

## 1. 基本格式

推荐使用以下三种格式之一：

```text
<type>: <action>
<type>(<scope>): <action>
<type>: Phase <n>[.<m>] - <scope> - <action>

合法示例：

feat: add configurable analysis entry
fix(export): preserve original sheet order
refactor(loader): extract shared normalization helper
docs(handoff): refresh current boundaries and next steps
test(smoke): cover pipeline entry with sample config
docs: Phase 2 - migration - define runtime boundaries
2. type（改动类型）

表示本次提交的主要性质。

推荐使用以下集合：

type	说明
feat	新功能、新入口、新能力
fix	bug 修复、错误路径修正、兼容性修补
refactor	结构整理、实现收敛，不改变外部行为
docs	文档、handoff、status、说明更新
test	测试、smoke、回归保护
chore	杂项维护、配置、小型清理

默认仅使用以上六类。
只有当项目中已经形成稳定新模式时，才考虑扩展。

3. 适配当前 Python / migration 项目的常用 scope

scope 不强制，但在以下项目里通常很有价值：

模块边界相对清晰
提交主要落在一个模块或一层
需要后续按模块回看历史
3.1 通用 Python 工程 scope
loader
parser
export
config
api
service
adapter
pipeline
ui
cli
runtime
schema
validation
3.2 migration / 渐进重构类常用 scope
migration
boundary
legacy
wrapper
normalization
integration
compat
handoff
status
smoke
3.3 适合你当前项目风格的例子
refactor(loader): extract shared normalization helper
fix(export): keep workbook sheet order stable
feat(api): add configurable analysis entry
refactor(adapter): isolate legacy conversion path
docs(handoff): refresh blockers after dry-run validation
test(smoke): add minimal configurable entry coverage
docs(status): record phase-2 delivery snapshot

如果一次改动范围较散，或 scope 会让 subject 变得别扭，可以不写 scope。

4. action（动作描述）

action 应简短说明“本次做了什么”。

推荐写法：

动词 + 结果 / 对象

例如：

add configurable analysis entry
extract shared normalization helper
preserve original sheet order
refresh handoff after parser integration
define migration boundaries
stabilize legacy adapter invocation

不推荐写法：

update
misc
fix bug
do changes
continue work

这些词信息量过低，无法支撑后续回看、交接和 AI 理解。

5. Phase 的使用原则

Phase 是可选项，只在项目确实存在阶段叙事时使用。

5.1 适用场景
项目本身有明确阶段，如 Phase 1 / Phase 2 / Phase 3
当前提交对应某阶段的边界定义、阶段收口或里程碑
你希望 Git log 能直接映射项目演进时间线

格式：

<type>: Phase <n>[.<m>] - <scope> - <action>

例如：

docs: Phase 1 - migration - define project boundaries
refactor: Phase 2 - loader - extract shared parsing helper
test: Phase 2.1 - export - add workbook smoke coverage
docs: Phase 3 - handoff - update blockers and next steps
5.2 不适用场景

不要把下面这些写成 Phase：

一次普通小修
当天做的一次检查
AI 执行过程中的步骤，如 scan / audit / report / fix
一次性的试验调整
5.3 当前这类项目的判断口径

对于你常见的 Python / migration 项目：

项目阶段 可以写 Phase
施工步骤 不要写 Phase

例如：

Phase 2 - migration - stabilize runtime boundary 可以
Phase audit - parser - inspect sections 不可以

这个判断口径与现有 skill-hub 规范一致：Phase 代表系统/项目演进阶段，而不是一次执行动作。

6. 对 migration 项目的特别约束

这部分是定制版里最重要的地方。

6.1 新增能力用 feat

当外部使用方式、功能能力、入口能力发生新增时，用 feat。

例如：

feat(api): add configurable analysis entry
feat(cli): add batch export command
feat(parser): support section-level filtering output
6.2 不改变行为的收敛，用 refactor

当你只是：

抽 helper
收敛重复实现
薄包装转调
调整目录或模块组织
不改变外部输出和调用契约

应写成 refactor，不要误写成 feat。

例如：

refactor(loader): extract shared normalization helper
refactor(wrapper): preserve old entrypoints while routing to shared impl
refactor(adapter): isolate legacy bridge without changing run contract
6.3 契约修正或口径修正，用 fix

当你修的是：

错误路径
输出结构偏差
配置兼容性问题
结果口径 bug
Excel / 文档 / sheet / schema 的错误行为

用 fix。

例如：

fix(export): preserve original sheet order
fix(config): fallback to default runtime settings on invalid file
fix(parser): handle empty section titles
fix(adapter): avoid incorrect legacy path resolution
6.4 状态文档更新，用 docs

当改动主要是：

HANDOFF.md
status.md
migration_status.md
next_steps.md
README.md

统一用 docs。

例如：

docs(handoff): refresh current blockers and next steps
docs(status): record dry-run validation result
docs(migration): update phase-2 execution status
docs: clarify runtime boundary and legacy ownership
7. 与 HANDOFF / STATUS / MIGRATION 文档的分工

建议沿用下面这套分工：

层	作用
commit	记录“发生了什么”
HANDOFF.md	记录“当前状态、边界、阻塞、下一步”
status / migration 文档	记录“阶段快照、专项说明、执行计划”

因此：

commit 不承担完整上下文说明
复杂背景不要全部塞进 subject
阶段结论、当前状态、边界说明，优先沉淀到 handoff / status 文档
commit 负责提供简洁、可检索的时间线

这也和你现有规范的三层分工一致：commit 是 timeline，HANDOFF 是 state，STATUS 是 snapshot。

8. 是否需要 commit body

默认策略：

优先使用单行 subject
不强制使用多行 body
8.1 推荐使用 body 的场景

对于你当前项目，下面几种情况很适合加 body：

这次改动有明显边界约束
做的是“低风险收敛”，需要说明没做什么
迁移任务涉及兼容旧入口
单行 subject 不能完整表达约束
8.2 推荐格式
refactor(loader): extract shared normalization helper

- preserve original public entrypoints
- keep output schema unchanged
- reduce duplicated normalization logic across two scripts
8.3 body 使用规则
第一行只写 subject
第二行必须留空
后续 body 用自然语言段落或 - 列表均可
body 应补充背景、边界和不变项
不要写空泛占位词，如 misc、stuff、update

这也和你现有规范对 body 的口径一致。

9. 当前项目最常见的高质量提交示例
9.1 数据加载 / 解析类
feat(parser): add contract section filtering entry
fix(loader): handle empty workbook path
refactor(normalization): centralize return-series cleanup logic
test(smoke): add minimal parser flow validation
9.2 migration / adapter / legacy 收敛类
docs: Phase 1 - migration - define boundary and ownership
refactor(wrapper): preserve old entrypoints while routing to shared helper
refactor(adapter): isolate legacy conversion path
fix(compat): keep legacy output schema unchanged
docs(handoff): refresh current migration blockers
9.3 Excel / export / 报表类
fix(export): preserve original sheet naming
fix(export): keep workbook sheet order stable
refactor(export): split chart insertion helper without changing output layout
test(smoke): validate workbook generation with sample input
9.4 配置 / runtime / CLI 类
feat(config): add runtime settings loader
fix(runtime): fallback to default settings on invalid config
chore(cli): align local path defaults
docs(status): record runtime config delivery status
9.5 handoff / 状态维护类
docs(handoff): update current boundaries and next steps
docs(status): record phase-2 snapshot after smoke pass
docs: clarify migration scope and non-goals
10. 常见错误与修正
错误 1
update parser

问题：

没有合法 type
描述过于空泛

改成：

feat(parser): add section filtering entry

或：

fix(parser): handle empty section titles
错误 2
refactor stuff

问题：

没有 scope
没说明改了什么

改成：

refactor(loader): extract shared normalization helper
错误 3
docs: Phase migration - update handoff

问题：

Phase 后缺少数值阶段

改成：

docs: Phase 2 - migration - refresh handoff after boundary review

如果这不是阶段型提交，也可以直接写：

docs(handoff): refresh migration blockers and next steps
错误 4
feat(export): refactor output logic

问题：

refactor 类动作被误写成 feat

改成：

refactor(export): extract workbook helper without changing output layout
错误 5
fix: bug fix

问题：

没有定位信息
完全不可检索

改成：

fix(config): fallback to default runtime settings on invalid file
11. 推荐实践
推荐 1：一条 commit 只表达一个主要动作

不要把多个无关事项压成一个 subject。

不推荐：

feat: add parser and update handoff and fix export

推荐拆开：

feat(parser): add section filtering entry
fix(export): preserve original sheet order
docs(handoff): refresh usage after parser integration
推荐 2：迁移项目里，优先写清“是否改变行为”

你当前很多项目都强调运行契约稳定，所以 subject 最好能让人一眼看出：

是新增能力
还是行为不变的收敛
还是修正错误

例如：

refactor(wrapper): preserve old entrypoints while routing to shared impl

这类写法很适合你当前工作流。

推荐 3：文档提交尽量写清对象

对于 handoff / status 类文档，建议直接写对象，而不是泛泛写 update docs。

例如：

docs(handoff): refresh blockers after dry-run validation
docs(status): record migration phase snapshot
docs(migration): update execution plan and non-goals
推荐 4：不要过度设计 scope

如果模块边界还在变化，就先用少量稳定 scope：

loader
parser
export
config
adapter
pipeline
handoff
status
migration
smoke

等项目稳定了再细化。

12. 最小执行标准

对于当前这类 Python / migration 项目，建议至少满足以下标准：

使用 feat/fix/refactor/docs/test/chore 之一开头
subject 能看出主要动作和主要对象
不使用 update / misc / stuff / fix bug
复杂改动时使用标准 body 格式
只有项目确实存在阶段叙事时才使用 Phase
migration 收敛类改动优先明确“是否改变外部行为”

这已经足以形成高质量、低负担、便于 AI 理解的提交历史。

13. 建议的落地方式
第一阶段

先只放文档，不上 hook。

第二阶段

连续使用一段时间后，观察以下内容是否已经稳定：

type 使用是否稳定
常用 scope 是否稳定
phase 命名是否稳定
是否经常出现低质量 subject
第三阶段

只有在项目真的长期维护、多人协作或频繁 handoff 时，再考虑增加极简 commit-msg 校验。

原则：

先形成稳定实践，再决定是否工具化固化

14. 总结

本规范的核心不是“把 commit 写得更正式”，而是：

让 Git 历史成为可读的项目演进日志，而不是随手记录

理想状态下：

Git log：能快速看懂项目一路做了什么
HANDOFF：能快速理解当前状态、边界和阻塞
STATUS / MIGRATION：能定位某阶段的专项信息

对于当前这类 Python / migration 项目，只要做到：

轻量结构化 + 行为口径明确 + 持续一致

就已经足够有价值。