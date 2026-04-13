# Git 与 Bundle 开发协作规范（实习生版）

> 适用范围：独立于具体项目之外的开发规范。  
> 目标：让实习生能在本地用 Git 管理项目开发，并能通过 `bundle` 形式接收和使用 `ai_skill_hub`。

---

## 1. 核心原则

### 1.1 一个项目一个仓库一个工作区

推荐按以下方式组织：

```text
workspace/
├─ valuation-parser/   # 当前项目仓库
└─ ai_skill_hub/       # 通过 bundle 导入的 skill hub 本地仓库
```

不要把多个不相关项目混在一个仓库里。  
不要把 `ai_skill_hub` 直接塞进项目仓库内部作为普通文件夹提交。

### 1.2 环境跟着项目走

- 一个项目一个环境
- 一个仓库一个工作区
- 不要长期在 base 环境里开发

### 1.3 AI 改代码前先做 Git checkpoint

每次开始一轮较大改动前，先提交一个 checkpoint，便于回滚和对比。

---

## 2. 工作区建议结构

推荐使用同级目录多仓库结构：

```text
D:\intern_workspace\
├─ valuation-parser\
└─ ai_skill_hub\
```

说明：

- `valuation-parser`：实习生负责开发的项目仓库
- `ai_skill_hub`：你下发给实习生的 skill hub 本地参考仓库

这样做的好处：

- 项目与 skill-hub 权限边界清晰
- VS Code 打开 workspace 更方便
- Git 历史互不污染
- 后续替换 bundle 或更新项目时不容易误操作

---

## 3. valuation-parser 项目初始化

## 3.1 新建目录

```powershell
mkdir D:\intern_workspace\valuation-parser
cd D:\intern_workspace\valuation-parser
```

## 3.2 初始化 Git 仓库

```powershell
git init
git add .
git commit -m "chore: initialize valuation parser repository"
```

如果项目文件还没放进去，可以在项目脚手架准备好之后再执行 `git add .`。

## 3.3 推荐首批文件

```text
valuation-parser/
├─ README.md
├─ .gitignore
├─ pyproject.toml
├─ src/
├─ tests/
├─ config/
├─ data_samples/
└─ docs/
```

---

## 4. `.gitignore` 最小建议

建议至少包含：

```gitignore
.venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.vscode/.ropeproject/
output/
tmp/
*.log
*.xlsx
*.xls
*.parquet
*.csv
!data_samples/README.md
```

说明：

- 原始样本、临时输出、缓存文件默认不要进仓库
- 如果需要提交极小的脱敏 demo 样本，应单独放到明确目录，并控制体积和数量

---

## 5. 日常 Git 最小流程

## 5.1 开始开发前

```powershell
git status
git add .
git commit -m "chore: checkpoint before parser changes"
```

如果当前没有可提交内容，可以只执行 `git status`，确认工作区干净。

## 5.2 开发中

常用命令：

```powershell
git status
git diff
git add <file>
git restore <file>
```

## 5.3 完成一个小阶段后

```powershell
git add .
git commit -m "feat(parser): add broker-a leaf position extraction"
```

## 5.4 查看历史

```powershell
git log --oneline --decorate --graph -20
```

---

## 6. 推荐分支策略

实习生阶段建议尽量简单：

### 方案 A：只有主分支

适合单人、本地开发为主：

```text
main
```

### 方案 B：主分支 + 功能分支

适合阶段性功能开发更清晰：

```text
main
feature/broker-a-parser
feature/code-normalizer
feature/tests
```

只本地使用分支，不要求提交到github库。

创建分支：

```powershell
git checkout -b feature/broker-a-parser
```

---

## 7. Commit message 规范

本规范参考你提供的 `单项目 Commit Convention（轻量版）.md`，保留“轻量结构化”的核心思路：

### 7.1 基本格式

```text
<type>: <action>
<type>(<scope>): <action>
<type>: Phase <n>[.<m>] - <scope> - <action>
```

推荐示例：

```text
feat(parser): add broker-a subject row detection
fix(export): preserve original sheet order
refactor(normalizer): extract shared code cleanup helper
docs(handoff): refresh current parser boundaries and next steps
test(smoke): add sanitized sample workbook coverage
docs: Phase 2 - migration - define adapter boundaries
```

### 7.2 推荐 type

| type | 用途 |
| --- | --- |
| `docs` | 文档、README、任务书、说明 |
| `feat` | 新功能、新解析能力、新 adapter |
| `fix` | bug 修复、规则修正 |
| `refactor` | 重构，不改变外部行为 |
| `test` | 测试、smoke、回归保护 |
| `chore` | 杂项维护、初始化、清理 |

默认只使用这六类；如果项目里还没有稳定新模式，不建议随意扩展 type。

### 7.3 scope 使用建议

scope 不强制，但在这些场景下很有价值：

- 模块边界相对清晰
- 提交主要集中在一个模块或一层
- 后续需要按模块回看历史

针对 `valuation-parser`，建议优先使用这些 scope：

- `parser`
- `broker-a`
- `broker-b`
- `normalizer`
- `export`
- `config`
- `adapter`
- `cli`
- `smoke`
- `tests`
- `handoff`
- `status`
- `docs`
- `repo`

如果一次改动范围较散，或者 scope 会让 subject 变得别扭，可以不写 scope。

### 7.4 action 写法

action 应尽量写成“动词 + 结果 / 对象”，让人一眼看懂本次改动做了什么。

推荐写法：

- `add broker-a subject row detection`
- `preserve original sheet order`
- `extract shared normalization helper`
- `refresh handoff after parser integration`

不推荐写法：

- `update`
- `misc`
- `fix bug`
- `do changes`
- `continue work`

### 7.5 Phase 使用原则

Phase 是可选项，只在项目确实存在阶段叙事时使用。

适用场景：

- 项目本身有明确阶段，例如 Phase 1 / Phase 2 / Phase 3
- 当前提交对应某阶段的边界定义、阶段收口或里程碑
- 你希望 Git log 能直接映射项目演进时间线

不适用场景：

- 一次普通小修
- 当天做的一次检查
- AI 执行过程中的步骤，例如 scan / audit / report / fix
- 一次性的试验调整

判断口径：

- 项目阶段可以写 Phase
- 施工步骤不要写 Phase

例如：

```text
docs: Phase 1 - migration - define parser ownership boundary
test: Phase 2.1 - export - add workbook smoke coverage
```

不要写成：

```text
docs: Phase audit - parser - inspect sections
```

### 7.6 什么时候用 feat / refactor / fix / docs

推荐按“是否改变外部行为”来判断：

- `feat`：新增功能、入口、解析能力
- `refactor`：收敛实现、抽 helper、调整结构，但不改变外部行为
- `fix`：修规则、修输出口径、修兼容性或错误路径
- `docs`：更新 README、handoff、status、任务书等文档

示例：

```text
feat(parser): add broker-a subject row detection
refactor(adapter): isolate broker-specific extraction flow
fix(export): preserve original sheet order
docs(status): record dry-run validation result
```

### 7.7 什么时候使用 body

默认单行 subject 即可。  
以下情况建议补 body：

- 改动较复杂
- 涉及多个模块
- 有行为边界需要说明
- 做的是低风险收敛，需要说明没做什么
- 需要标出未做事项

推荐格式：

```text
refactor(normalizer): extract shared code cleanup helper

- preserve existing parser output schema
- keep broker-specific rules inside adapter layer
- reduce duplicated cleanup logic across exporters
```

body 使用规则：

- 第一行只写 subject
- 第二行留空
- 后续 body 用自然语言段落或 `-` 列表均可
- body 主要补充背景、边界和不变项

### 7.8 常见高质量示例

```text
chore: initialize valuation parser repository
feat(parser): add broker-a subject row detection
fix(broker-a): skip summary rows in leaf extraction
refactor(normalizer): centralize hk code padding cleanup
test(smoke): add sanitized workbook parser coverage
docs(handoff): refresh current parser boundaries and next steps
docs: Phase 2 - migration - define adapter boundaries
```

避免使用这些无信息量写法：

- `refactor stuff`
- `fix: bug fix`
- `update`
- `misc`
- `fix stuff`
- `change code`

---

## 8. `ai_skill_hub` 的 bundle 导入方式

你会直接收到最新的 `ai-skill-hub` bundle。  
建议将其放在本地的 `ai_skill_hub` 文件夹中，作为独立仓库使用。

## 8.1 初次导入

假设你收到的 bundle 文件路径为：

```text
D:\transfer\ai-skill-hub-latest.bundle
```

请在工作区根目录执行：

```powershell
cd D:\intern_workspace
git clone D:\transfer\ai-skill-hub-latest.bundle ai_skill_hub
```

导入完成后目录将变成：

```text
D:\intern_workspace\ai_skill_hub
```

## 8.2 进入仓库检查

```powershell
cd D:\intern_workspace\ai_skill_hub
git status
git log --oneline -5
```

如果仓库里带有 hook 安装脚本，再执行一次：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\install_git_hooks.ps1
```

## 8.3 使用原则

- `ai_skill_hub` 默认视为**参考仓库 / 工具仓库**
- 不要把它作为 `valuation-parser` 的子目录提交进去
- 不要在没有明确要求的情况下直接改它
- 项目实际运行时，以项目目录下的 `.codex/skills/` 为准

---

## 9. `ai_skill_hub` 的更新方式

如果后续收到新的 bundle，优先使用**重新克隆到新目录**或**备份后重建**的简单方式。

### 方案 A：重新克隆到新目录

```powershell
cd D:\intern_workspace
git clone D:\transfer\ai-skill-hub-latest-2.bundle ai_skill_hub_new
```

确认无误后，再手工替换旧目录。

### 方案 B：删除旧目录后重建

仅在你确认旧目录没有本地改动时使用。

```powershell
cd D:\intern_workspace
rmdir /s /q ai_skill_hub
git clone D:\transfer\ai-skill-hub-latest.bundle ai_skill_hub
```

### 不建议的做法

- 不要把 bundle 文件直接解压当普通文件夹用
- 不要把 `ai_skill_hub` 直接复制进项目仓库
- 不要让项目仓库和 hub 仓库共用 `.git` 目录

---

## 10. 项目与 skill 的关系

### 10.1 `ai_skill_hub` 是源头参考

它主要用来：

- 看有哪些 skill
- 看 README / SKILL / 模板
- 必要时下发 skill 到项目

### 10.2 `valuation-parser` 是实际开发仓库

它主要用来：

- 写代码
- 跑测试
- 提交 commit
- 交付项目成果

### 10.3 项目实际使用的 skill 位置

如果需要把 skill 下发到项目，目标位置通常是：

```text
valuation-parser/.codex/skills/
```

也就是说：

- `ai_skill_hub`：源头 / 参考 / 发布物导入点
- `valuation-parser/.codex/skills/`：项目运行时使用位置

---

## 11. 推荐日常节奏

### 每次开始工作前

1. 打开 `valuation-parser`
2. 看 `git status`
3. 确认环境正确
4. 如需用 AI 大改，先做 checkpoint commit

### 每完成一个小功能后

1. 跑最小测试
2. 看 `git diff`
3. 提交一次清晰 commit
4. 更新 README 或进度文档

### 每次接触新 skill 前

1. 先去 `ai_skill_hub` 看说明
2. 再看项目里的 `.codex/skills/`
3. 先用已有 skill，不先改 skill

---

## 12. 常见错误

### 错误 1：不建 Git 仓库，直接写代码

后果：没有 checkpoint，AI 改坏后很难恢复。

### 错误 2：把 `ai_skill_hub` 放进项目仓库提交

后果：仓库膨胀、历史混乱、边界不清。

### 错误 3：commit message 过于随意

例如：

```text
update
refactor stuff
fix: bug fix
```

后果：后续几乎无法看懂演进历史。

### 错误 4：bundle 当普通压缩包处理

后果：失去 Git 历史和仓库能力。

### 错误 5：一个工作区里混多个目标但没有边界

后果：项目、skill、工具链上下文串味。

---

## 13. 最小操作清单

## 13.1 初始化项目仓库

```powershell
mkdir D:\intern_workspace\valuation-parser
cd D:\intern_workspace\valuation-parser
git init
git add .
git commit -m "chore: initialize valuation parser repository"
```

## 13.2 导入 `ai_skill_hub` bundle

```powershell
cd D:\intern_workspace
git clone D:\transfer\ai-skill-hub-latest.bundle ai_skill_hub
```

## 13.3 日常 checkpoint

```powershell
cd D:\intern_workspace\valuation-parser
git status
git add .
git commit -m "chore: checkpoint before parser refactor"
```

## 13.4 功能完成后提交

```powershell
git add .
git commit -m "feat(parser): add broker-a position extraction"
```

---

## 14. 一句话总结

- **项目代码放项目仓库**
- **skill hub 用独立仓库接收 bundle**
- **AI 改代码前先做 checkpoint**
- **commit message 用轻量结构化格式**
- **不要把项目、skill、bundle 混成一个仓库**
