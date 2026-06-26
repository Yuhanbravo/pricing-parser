# R3-A SSOT 对账报告

> 日期：2026-06-25
> 阶段：R3-A1 — SSOT Reconciliation Planning
> 对账范围：owner-provided local SSOT seed ↔ pricing-parser 当前 mapping ↔ RC1 manifest

---

## 1. 材料来源

### 1.1 SSOT Seed（本地，gitignored）

路径：`data_samples/local_rc1/pricing-parser-r3a0-custodian-ssot-seed-001/`

| 文件 | 用途 |
|---|---|
| `custodian_registry_seed.local.csv` | 托管人注册表（13 行） |
| `product_custodian_map_seed.local.csv` | 产品-托管映射表（43 行） |
| `ssot_seed_schema.md` | 字段说明 |
| `ssot_seed_safety_note.md` | 安全边界 |

### 1.2 Parser 当前 Mapping

路径：`产品与托管机构映射表.csv`（仓库根目录，compact 格式）

通过 `mapping_loader.py` 加载，使用 `NAME_TO_ADAPTER_KEY` 推导 `adapter_key`：

| 托管人简称 | adapter_key |
|---|---|
| 兴业证券 | `xyzc` |
| 招商证券 | `cmsc` |
| 中信证券 | `citics` |
| 东方证券 | `orient` |
| 中信建投 | `csc` |
| 国泰海通 | `gtja` |
| 国信证券 | `guosen` |
| 长城证券 | `greatwall` |

Parser 已注册 adapter（`adapter_registry.py` `SUPPORTED_ADAPTERS`）：`citics`、`cmsc`、`csc`、`generic`、`greatwall`、`gtja`、`guosen`、`orient`、`xyzc`（共 9 个，含 `generic`）。

配置文件（`config/adapters/`）均有对应 yaml：`citics.yaml`、`cmsc.yaml`、`csc.yaml`、`generic.yaml`、`greatwall.yaml`、`gtja.yaml`、`guosen.yaml`、`orient.yaml`、`xyzc.yaml`。

### 1.3 RC1 Manifest

路径：`data_samples/local_rc1/pricing-parser-rc1-intake-001/selected_sample_manifest.csv`（8 个样本）

---

## 2. 基础校验（必答项）

### 2.1 `custodian_registry_seed.local.csv` 是否可读、行数是否为 13？

✅ **通过**。文件可读，数据行 13 行（含表头共 14 行），与任务书 3.2A 验收摘要一致。

### 2.2 `product_custodian_map_seed.local.csv` 是否可读、行数是否为 43？

✅ **通过**。文件可读，数据行 43 行（含表头共 44 行），与任务书 3.2A 验收摘要一致。

其中：
- 运行中产品（`is_cleared_product=no`）：38 个
- 清盘产品（`is_cleared_product=yes`）：5 个（`PRODUCT_041`、`PRODUCT_042`、`PRODUCT_043`、`PRODUCT_044`、`PRODUCT_045`）

### 2.3 `custodian_id` 外键校验

✅ **通过**。`product_custodian_map_seed.local.csv` 中所有 43 行的 `custodian_id` 均在 `custodian_registry_seed.local.csv` 中存在对应记录，无孤立外键。

---

## 3. SSOT Seed 托管人概览

| custodian_id | 托管人简称 | pricing_sheet_key | parser_adapter_key | has_parser_adapter |
|---|---|---|---|---|
| CUSTODIAN_001 | 兴业证券 | xingye | xyzc | yes |
| CUSTODIAN_002 | 中信建投 | — | — | no |
| CUSTODIAN_003 | 中信证券 | citic | citics | yes |
| CUSTODIAN_004 | 东方证券 | orient | orient | yes |
| CUSTODIAN_005 | 中泰证券 | — | — | no |
| CUSTODIAN_006 | 国泰海通 | gt_haitong | gtja | yes |
| CUSTODIAN_007 | 国信证券 | guoxin | guosen | yes |
| CUSTODIAN_008 | 华泰证券 | — | — | no |
| CUSTODIAN_009 | 广发证券 | — | — | no |
| CUSTODIAN_010 | 招商证券 | — | — | no |
| CUSTODIAN_011 | 浙商证券 | — | — | no |
| CUSTODIAN_012 | 长城证券 | — | — | no |
| CUSTODIAN_013 | 长江证券 | — | — | no |

**SSOT seed 中有 parser_adapter_key 的托管人**：5 个（CUSTODIAN_001/003/004/006/007），对应 adapter key：`xyzc`、`citics`、`orient`、`gtja`、`guosen`。

---

## 4. Parser 当前 Mapping vs SSOT Seed 对比

### 4.1 `custodian_id` 编号一致性

⚠️ **发现严重不一致**：parser mapping 与 SSOT seed 使用了**不同的 `custodian_id` 编号体系**。

| custodian_id | Parser Mapping 真实托管人 | SSOT Seed 托管人 | 是否一致 |
|---|---|---|---|
| CUSTODIAN_001 | 兴业证券 → `xyzc` | 兴业证券 → `xyzc` | ✅ 一致 |
| CUSTODIAN_002 | 招商证券 → `cmsc` | **中信建投** → 无 adapter | ❌ 不一致 |
| CUSTODIAN_003 | 中信证券 → `citics` | 中信证券 → `citics` | ✅ 一致 |
| CUSTODIAN_004 | 东方证券 → `orient` | 东方证券 → `orient` | ✅ 一致 |
| CUSTODIAN_005 | 中信建投 → `csc` | **中泰证券** → 无 adapter | ❌ 不一致 |
| CUSTODIAN_006 | 国泰海通 → `gtja` | 国泰海通 → `gtja` | ✅ 一致 |
| CUSTODIAN_007 | 国信证券 → `guosen` | 国信证券 → `guosen` | ✅ 一致 |
| CUSTODIAN_008 | 长城证券 → `greatwall` | **华泰证券** → 无 adapter | ❌ 不一致 |

**分析**：Parser mapping 的 `custodian_id` 是早期内部编号（CUSTODIAN_001–008），而 SSOT seed 是 owner 侧权威编号（CUSTODIAN_001–013）。两者在 CUSTODIAN_001/003/004/006/007 上碰巧一致（因为它们都是最早有 adapter 的托管人），但 CUSTODIAN_002/005/008 完全不同。

### 4.2 Parser 有 Adapter 但 SSOT Seed 标注为 "无" 的托管人

SSOT seed 中以下托管人标注 `has_parser_adapter=no`，但 parser 实际**已实现对应 adapter**：

| 托管人 | SSOT custodian_id | Parser 是否有 adapter | Adapter Key |
|---|---|---|---|
| 中信建投 | CUSTODIAN_002 | ✅ 有 | `csc`（`config/adapters/csc.yaml`） |
| 长城证券 | CUSTODIAN_012 | ✅ 有 | `greatwall`（`config/adapters/greatwall.yaml`） |
| 招商证券 | CUSTODIAN_010 | ✅ 有 | `cmsc`（`config/adapters/cmsc.yaml`） |

**结论**：SSOT seed 的 `has_parser_adapter` 和 `parser_adapter_key` 字段需要更新，以反映 parser 当前实际能力。这三个托管人的 adapter 已经在 parser 中实现并经过测试验证（`docs/status.md` 确认 `cmsc`、`csc`、`greatwall` 在最近一次运行中命中）。

### 4.3 SSOT Seed 有但 Parser Mapping 未覆盖的托管人

| custodian_id | 托管人简称 | 涉及产品数 | Parser 是否有 adapter |
|---|---|---|---|
| CUSTODIAN_005 | 中泰证券 | 2（PRODUCT_031, PRODUCT_039） | ❌ 无 |
| CUSTODIAN_008 | 华泰证券 | 2（PRODUCT_024, PRODUCT_033） | ❌ 无 |
| CUSTODIAN_009 | 广发证券 | 1（PRODUCT_044） | ❌ 无 |
| CUSTODIAN_011 | 浙商证券 | 1（PRODUCT_045） | ❌ 无 |
| CUSTODIAN_013 | 长江证券 | 2（PRODUCT_032, PRODUCT_036） | ❌ 无 |

这 5 个托管人目前 parser 既无 mapping 也无 adapter。涉及 8 个产品（含 2 个清盘产品）。

---

## 5. RC1 首批 3 个样本链路校验

### 5.1 RC1_024

| 链路节点 | 来源 | 值 |
|---|---|---|
| sample_id | RC1 manifest | `RC1_024` |
| product_id | RC1 manifest → SSOT seed | `PRODUCT_011` |
| custodian_id | RC1 manifest → SSOT seed | `CUSTODIAN_004` |
| 托管人 | SSOT seed | 东方证券 |
| source_adapter_key (RC1) | RC1 manifest | `orient` |
| parser_adapter_key | SSOT seed / parser mapping | `orient` |
| 实际 workbook | local_rc1 | `.xlsx`（OOXML） |

✅ **链路闭合**。`orient` 精确匹配，无需 alias 转换。这是风险最低的 baseline candidate。

### 5.2 RC1_030

| 链路节点 | 来源 | 值 |
|---|---|---|
| sample_id | RC1 manifest | `RC1_030` |
| product_id | RC1 manifest → SSOT seed | `PRODUCT_009` |
| custodian_id | RC1 manifest → SSOT seed | `CUSTODIAN_003` |
| 托管人 | SSOT seed | 中信证券 |
| source_adapter_key (RC1) | RC1 manifest | `citic` |
| parser_adapter_key | SSOT seed / parser mapping | `citics` |
| alias 关系 | SSOT seed | `citic → citics` |
| 实际 workbook | local_rc1 | `.xlsx`（OOXML） |

✅ **链路闭合**。通过 alias `citic → citics` 可正确路由。需在 parser intake 时做 alias 转换。

### 5.3 RC1_026

| 链路节点 | 来源 | 值 |
|---|---|---|
| sample_id | RC1 manifest | `RC1_026` |
| product_id | RC1 manifest → SSOT seed | `PRODUCT_001` |
| custodian_id | RC1 manifest → SSOT seed | `CUSTODIAN_007` |
| 托管人 | SSOT seed | 国信证券 |
| source_adapter_key (RC1) | RC1 manifest | `guoxin` |
| parser_adapter_key | SSOT seed / parser mapping | `guosen` |
| alias 关系 | SSOT seed | `guoxin → guosen` |
| 实际 workbook | local_rc1 | `.xls`（Excel COM / xlrd） |

✅ **链路闭合**。通过 alias `guoxin → guosen` 可正确路由。需在 parser intake 时做 alias 转换。注意：RC1 manifest 标注 `extension=.xlsx`，但实际 workbook 文件名为 `.xls`，应以实际文件格式为准；parser 已支持 `.xls` 预览和解析。

---

## 6. Alias Mapping 一致性

任务书定义的 alias 关系与 SSOT seed 对比：

| pricing_sheet_key | parser_adapter_key | SSOT seed 确认 | 状态 |
|---|---|---|---|
| `citic` | `citics` | ✅ CUSTODIAN_003 | 一致 |
| `guoxin` | `guosen` | ✅ CUSTODIAN_007 | 一致 |
| `xingye` | `xyzc` | ✅ CUSTODIAN_001 | 一致 |
| `gt_haitong` | `gtja` | ✅ CUSTODIAN_006 | 一致 |
| `orient` | `orient` | ✅ CUSTODIAN_004 | 一致（无需转换） |

✅ **全部 5 组 alias 关系一致**，无缺失、无冲突。

---

## 7.4 3个 Product Map 在 Parser Mapping 中的覆盖情况

### 7.1 已在 Parser Mapping 中出现

Parser mapping（compact 格式）包含以下 product：

| custodian_id (parser) | 托管人 | adapter_key | 覆盖的 product_id |
|---|---|---|---|
| CUSTODIAN_001 | 兴业证券 | `xyzc` | PRODUCT_002, PRODUCT_003, PRODUCT_004, PRODUCT_005 |
| CUSTODIAN_002 | 招商证券 | `cmsc` | PRODUCT_008, PRODUCT_013 |
| CUSTODIAN_003 | 中信证券 | `citics` | PRODUCT_006, PRODUCT_009, PRODUCT_018, PRODUCT_020 |
| CUSTODIAN_004 | 东方证券 | `orient` | PRODUCT_010, PRODUCT_011, PRODUCT_015, PRODUCT_017, PRODUCT_019 |
| CUSTODIAN_005 | 中信建投 | `csc` | PRODUCT_021 |
| CUSTODIAN_006 | 国泰海通 | `gtja` | PRODUCT_012, PRODUCT_014 |
| CUSTODIAN_007 | 国信证券 | `guosen` | PRODUCT_001 |
| CUSTODIAN_008 | 长城证券 | `greatwall` | PRODUCT_023 |

**合计**：Parser mapping 覆盖 **20 个 product**（8 个托管人）。

### 7.2 在 SSOT Seed 中但不在 Parser Mapping 中

以下 product 在 SSOT seed 中存在，但 parser mapping 未覆盖：

| product_id | custodian_id (SSOT) | 托管人 | parser_adapter_key | 备注 |
|---|---|---|---|---|
| PRODUCT_007 | CUSTODIAN_006 | 国泰海通 | gtja | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_024 | CUSTODIAN_008 | 华泰证券 | — | 无 adapter |
| PRODUCT_025 | CUSTODIAN_006 | 国泰海通 | gtja | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_026 | CUSTODIAN_012 | 长城证券 | — | parser 有 greatwall adapter，但 mapping 未包含 |
| PRODUCT_027 | CUSTODIAN_006 | 国泰海通 | gtja | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_028 | CUSTODIAN_003 | 中信证券 | citics | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_029 | CUSTODIAN_010 | 招商证券 | — | parser 有 cmsc adapter，但 mapping 未包含 |
| PRODUCT_030 | CUSTODIAN_012 | 长城证券 | — | parser 有 greatwall adapter，但 mapping 未包含 |
| PRODUCT_031 | CUSTODIAN_005 | 中泰证券 | — | 无 adapter |
| PRODUCT_032 | CUSTODIAN_013 | 长江证券 | — | 无 adapter |
| PRODUCT_033 | CUSTODIAN_008 | 华泰证券 | — | 无 adapter |
| PRODUCT_034 | CUSTODIAN_010 | 招商证券 | — | parser 有 cmsc adapter，但 mapping 未包含 |
| PRODUCT_035 | CUSTODIAN_007 | 国信证券 | guosen | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_036 | CUSTODIAN_013 | 长江证券 | — | 无 adapter |
| PRODUCT_037 | CUSTODIAN_003 | 中信证券 | citics | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_038 | CUSTODIAN_004 | 东方证券 | orient | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_039 | CUSTODIAN_005 | 中泰证券 | — | 无 adapter |
| PRODUCT_040 | CUSTODIAN_003 | 中信证券 | citics | parser 有 adapter 但 mapping 未包含此 product |
| PRODUCT_041 | CUSTODIAN_004 | 东方证券 | orient | 清盘产品 |
| PRODUCT_042 | CUSTODIAN_003 | 中信证券 | citics | 清盘产品 |
| PRODUCT_043 | CUSTODIAN_006 | 国泰海通 | gtja | 清盘产品 |
| PRODUCT_044 | CUSTODIAN_009 | 广发证券 | — | 清盘产品，无 adapter |
| PRODUCT_045 | CUSTODIAN_011 | 浙商证券 | — | 清盘产品，无 adapter |

**合计**：23 个 product 在 SSOT seed 中但不在 parser mapping 中。

其中：
- **12 个运行中产品**，对应 parser 已有 adapter 但 mapping 未覆盖（PRODUCT_007/025/026/027/028/029/030/034/035/037/038/040）
- **6 个运行中产品**，对应 parser 无 adapter（PRODUCT_024/031/032/033/036/039）
- **3 个清盘产品**，对应 parser 有 adapter（PRODUCT_041/042/043）
- **2 个清盘产品**，对应 parser 无 adapter（PRODUCT_044/045）

---

## 8. 关键发现汇总

### 8.1 阻断性问题

| # | 发现 | 严重程度 | 影响范围 |
|---|---|---|---|
| 1 | **`custodian_id` 编号体系不一致**：parser mapping 与 SSOT seed 对 CUSTODIAN_002/005/008 分配了不同托管人 | 🔴 高 | 在合并两套 mapping 前必须统一编号体系，否则产品-托管关联会错乱 |

### 8.2 需要注意的问题

| # | 发现 | 严重程度 | 影响范围 |
|---|---|---|---|
| 2 | **SSOT seed `has_parser_adapter` 字段过期**：中信建投（CUSTODIAN_002）、长城证券（CUSTODIAN_012）、招商证券（CUSTODIAN_010）在 SSOT 中标注为无 adapter，但 parser 已实现 `csc`、`greatwall`、`cmsc` | 🟡 中 | SSOT seed 需更新 |
| 3 | **Parser mapping 覆盖不完整**：parser 有 8 个 adapter 但 mapping 仅覆盖 20 个 product，SSOT seed 中有 12 个运行中产品 parser 有对应 adapter 但 mapping 中未登记 | 🟡 中 | 需扩充 mapping |

### 8.3 RC1 首批 3 个样本状态

| # | 发现 | 严重程度 |
|---|---|---|
| 4 | ✅ **RC1_024/030/026 链路全部闭合**，不受 custodian_id 不一致影响（这三个托管人的 custodian_id 在两套体系中恰好一致） | 🟢 无阻断 |

### 8.4 Alias 一致性

| # | 发现 | 严重程度 |
|---|---|---|
| 5 | ✅ **5 组 alias 关系完全一致**，无需修正 | 🟢 无阻断 |

---

## 9. Mismatch / Missing 清单

### 9.1 Mismatch（不一致）

| 类型 | 描述 |
|---|---|
| custodian_id 编号 | Parser CUSTODIAN_002=招商证券，SSOT CUSTODIAN_002=中信建投 |
| custodian_id 编号 | Parser CUSTODIAN_005=中信建投，SSOT CUSTODIAN_005=中泰证券 |
| custodian_id 编号 | Parser CUSTODIAN_008=长城证券，SSOT CUSTODIAN_008=华泰证券 |
| has_parser_adapter | SSOT 标注中信建投/长城证券/招商证券为 no，实际 parser 已实现 |

### 9.2 Missing（缺失）

| 类型 | 描述 |
|---|---|
| Parser mapping 缺失 | 12 个运行中产品（有 adapter 但 mapping 未登记） |
| Parser mapping 缺失 | 6 个运行中产品（无 adapter） |
| Parser adapter 缺失 | 中泰证券、华泰证券、广发证券、浙商证券、长江证券（5 个托管人） |

---

## 10. R3-A2 触发建议

### 10.1 是否需要 R3-A2 implementation？

**需要，但应分两阶段进行。**

**R3-A2a（推荐立即执行）**：
- 更新 SSOT seed 中 `has_parser_adapter` 和 `parser_adapter_key` 字段（中信建投→`csc`、长城证券→`greatwall`、招商证券→`cmsc`）
- 此为 SSOT seed 元数据修正，不涉及 parser 代码变更

**R3-A2b（需 owner 决策后执行）**：
- 统一 `custodian_id` 编号体系（以 SSOT seed 为准，还是以 parser mapping 为准？）
- 扩充 parser mapping 覆盖 12 个"有 adapter 但 mapping 未登记"的运行中产品
- 引入 alias-aware mapping loader（使 parser 能自动将 RC1 source key 映射到 parser adapter key）
- 是否将 5 个无 adapter 的托管人纳入 scope

### 10.2 Owner 决策点

| # | 决策问题 | 上下文 |
|---|---|---|
| D1 | `custodian_id` 编号以哪套为准？建议以 SSOT seed 为准，同步更新 parser mapping 和 `产品与托管机构映射表.csv` | 当前两套体系不一致 |
| D2 | 是否在 R3-A 阶段扩充 parser mapping 覆盖已实现 adapter 的全部运行中产品？ | 12 个产品已可被 parser 处理，仅缺少 mapping 条目 |
| D3 | R3-B dry run 前是否需要完成 alias-aware loader？还是暂时手动指定 alias？ | RC1_030/026 需 `citic→citics`、`guoxin→guosen` 转换 |
| D4 | 5 个无 adapter 的托管人（中泰/华泰/广发/浙商/长江）是否纳入当前 scope？ | 这些托管人不在 RC1 首批样本中 |

---

## 11. 对 R3-B1 Dry Run 的影响评估

✅ **RC1_024 / RC1_030 / RC1_026 的 `product_id → custodian_id → parser_adapter_key` 链路均闭合，R3-B1 可以进入 dry run。**

需要注意的实操问题：
- RC1_030 需要 `citic → citics` alias 转换
- RC1_026 需要 `guoxin → guosen` alias 转换，且 workbook 为 `.xls` 格式
- 当前 parser routing 依赖 `产品与托管机构映射表.csv` 中的 `adapter_key` 字段，不直接支持 source alias 自动转换

---

## 12. 结论

| 检查项 | 结果 |
|---|---|
| SSOT seed 可读性 | ✅ 通过 |
| 行数校验（13 + 43） | ✅ 通过 |
| 外键完整性 | ✅ 通过 |
| 3 个 RC1 样本链路闭合 | ✅ 全部闭合 |
| Alias 关系一致性 | ✅ 5 组全部一致 |
| Parser mapping ↔ SSOT 整体一致性 | ❌ custodian_id 编号不一致 |
| SSOT has_parser_adapter 字段时效性 | ⚠️ 3 处过期 |

**总体评估**：SSOT seed 的 `product_id → custodian_id → parser_adapter_key` 链路在核心路径上（RC1 首批 3 个样本）是闭合的。parser mapping 与 SSOT seed 之间存在 custodian_id 编号体系不一致的问题，但不影响 R3-B1 首批 dry run。建议先完成 R3-A2a（SSOT seed 元数据修正），然后在 owner 决策后再执行 R3-A2b（mapping 体系统一）。

**R3-B1 可以进入，不需要等待 R3-A2b 完成。**
