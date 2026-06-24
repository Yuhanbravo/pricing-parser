# R3 RC1 Sample Intake — Planning Note

## Objective

Plan how, and in what order, to introduce 8 sanitized RC1 workbooks from the `Pricing_sheet` handoff
into `pricing-parser`'s sample coverage. This is a planning-only task — no parser runtime changes,
no expected output generation, no baseline refresh.

---

## 1. Materials Reviewed

All files live under `data_samples/local_rc1/pricing-parser-rc1-intake-001/` (gitignored).

| File | Purpose |
|---|---|
| `README.md` | Handoff scope and safety boundary |
| `selected_sample_manifest.csv` | 8-row sample index (id, scenario, adapter_key, extension, etc.) |
| `source_rc1_manifest_excerpt.csv` | RC1 source manifest excerpt with extra metadata |
| `LOCAL_SELECTION.md` | Why these 8 were chosen from the full RC1 library |
| `sample_coverage_summary.md` | Dimension-level coverage counts |
| `evidence_index_excerpt.csv` | RC1 provenance: which source group each sample came from |
| `workbooks/` | 8 sanitized workbooks (5 `.xls` + 3 `.xlsx`) |

---

## 2. Sample Inventory

| sample_id | scenario | adapter_key (RC1) | actual ext | workbook |
|---|---|---|---|---|
| RC1_001 | `normal_day` | UNKNOWN | `.xlsx` | `2025-03-27_PRODUCT_001估值表__1.xlsx` |
| RC1_024 | `month_end` | orient | `.xlsx` | `PRODUCT_011_估值表_20260430.xlsx` |
| RC1_025 | `month_end` | xingye | `.xls` | `20250630_PRODUCT_005_证券投资基金估值表.xls` |
| RC1_026 | `month_end` | guoxin | `.xls` | `20251031_PRODUCT_002_证券投资基金估值表.xls` |
| RC1_028 | `quarter_end` | xingye | `.xls` | `PRODUCT_009_资产估值表_20260331.xls` |
| RC1_030 | `quarter_end` | citic | `.xlsx` | `2025-02-28_PRODUCT_001估值表.xlsx` |
| RC1_032 | `special_day` | gt_haitong | `.xls` | `PRODUCT_014_估值表_20250910.xls` |
| RC1_034 | `special_day` | citic | `.xls` | `PRODUCT_006_资产估值表_20260211.xls` |

All 8 files confirmed present in the workbooks directory.

---

## 3. Coverage Summary

### By Scenario

| scenario | count | samples |
|---|---|---|
| `normal_day` | 1 | RC1_001 |
| `month_end` | 3 | RC1_024, RC1_025, RC1_026 |
| `quarter_end` | 2 | RC1_028, RC1_030 |
| `special_day` | 2 | RC1_032, RC1_034 |

### By Extension (actual file)

| extension | count |
|---|---|
| `.xls` | 5 |
| `.xlsx` | 3 |

### By Adapter Key

| RC1 adapter_key | count | parser adapter | status |
|---|---|---|---|
| `orient` | 1 | `orient` | ✅ exact match |
| `citic` | 2 | `citics` | ⚠️ naming variant |
| `guoxin` | 1 | `guosen` | ⚠️ naming variant |
| `xingye` | 2 | `xyzc` | ⚠️ naming variant |
| `gt_haitong` | 1 | `gtja` | ⚠️ naming variant |
| `UNKNOWN` | 1 | — | ❌ gap case only |

---

## 4. Key Findings

### 4.1 Adapter-key Naming Gap

RC1 and pricing-parser use different naming conventions for the same custodians.
All 5 variant pairs refer to the **same custodian** — no new adapter logic is needed,
only name alignment:

| RC1 key | Parser key | Custodian |
|---|---|---|
| `citic` | `citics` | 中信证券 |
| `guoxin` | `guosen` | 国信证券 |
| `xingye` | `xyzc` | 兴业证券 |
| `gt_haitong` | `gtja` | 国泰海通 |
| `orient` | `orient` | 东方证券 (exact match) |

### 4.2 Extension Metadata Inconsistency

Two samples have a mismatch between the manifest `extension` field and the actual
workbook filename extension:

| sample | manifest says | actual file | parser rule |
|---|---|---|---|
| RC1_026 | `.xlsx` | `.xls` | Use actual filename extension |
| RC1_030 | `.xls` | `.xlsx` | Use actual filename extension |

Per the task package: this is known, not a blocker. Manifest `extension` is retained
as source metadata only; parser keys off the actual file extension.

### 4.3 All Non-UNKNOWN Products Are Mapped

Every non-UNKNOWN sample's `product_stub` and `custodian_id` exist in
`产品与托管机构映射表.csv`. No mapping gaps for the 7 usable samples.

### 4.4 Workbook Filename ≠ product_stub

RC1_025, RC1_026, RC1_028, and RC1_030 show workbook filenames that differ from
their manifest `product_stub`. This is expected in sanitized handoff packages —
always treat the manifest as authoritative for product identity.

---

## 5. First-Intake Candidate Recommendations

Recommended order for introducing RC1 samples into parser testing.
Start simple, build up.

### Tier 1 — Start Here

| priority | sample | reason |
|---|---|---|
| **1** | **RC1_024** | Only sample where adapter_key exactly matches a parser adapter (`orient`). Month-end `.xlsx`. Zero config needed — can run parser immediately. |

### Tier 2 — After Naming Alignment

These require owner to confirm the adapter-key mapping first, but no new adapter code:

| priority | sample | reason |
|---|---|---|
| **2** | **RC1_030** | `citic`→`citics`. Quarter-end `.xlsx`. Covers a new scenario for the citics adapter. |
| **3** | **RC1_026** | `guoxin`→`guosen`. Month-end `.xls`. Tests the `.xls` / excel-com engine path. |
| **4** | **RC1_025** | `xingye`→`xyzc`. Month-end `.xls`. First RC1 coverage for the xyzc adapter. |

### Tier 3 — Higher Complexity

These introduce `special_day` scenarios, which may surface unexpected review patterns:

| priority | sample | reason |
|---|---|---|
| **5** | **RC1_034** | `citic`→`citics`. Special day (subscription/redemption). `.xls`. |
| **6** | **RC1_028** | `xingye`→`xyzc`. Quarter-end `.xls`. Good follow-up after RC1_025. |
| **7** | **RC1_032** | `gt_haitong`→`gtja`. Special day (large redemption). `.xls`. Most complex scenario — run last. |

### Gap Case — Do Not Promote

| sample | reason |
|---|---|
| **RC1_001** | `adapter_key = UNKNOWN`. No mapping, no adapter. Retain as a gap-analysis reference only. Not a baseline candidate. |

---

## 6. Risks

| risk | severity | mitigation |
|---|---|---|
| Naming alignment done wrong (wrong custodian mapped) | Medium | Owner confirms each RC1 key → parser key mapping before implementation |
| `.xls` files expose parser bugs not seen in `.xlsx` | Low-Medium | Introduce `.xls` samples incrementally (Tier 2), not all at once |
| `special_day` data triggers unexpected review items | Medium | Tier 3 samples deferred; review output before promoting to baseline |
| RC1_001 accidentally treated as a supported adapter case | Low | Explicitly labeled as gap case; do not create adapter for UNKNOWN |

---

## 7. Safety Verification

| check | status |
|---|---|
| `data_samples/local_rc1/` is gitignored | ✅ |
| No workbook files in `git status` | ✅ |
| All custodian IDs are `CUSTODIAN_XXX` (sanitized) | ✅ |
| All product IDs are `PRODUCT_XXX` (sanitized) | ✅ |
| No raw workbooks present | ✅ |
| No source paths or real identities leaked | ✅ |

---

## 8. Non-goals (This Round)

- Do **not** run the parser against any RC1 workbook.
- Do **not** generate expected output.
- Do **not** refresh `data_samples/expected/`.
- Do **not** modify adapters, routing, mapping, or taxonomy.
- Do **not** commit workbooks or RC1 metadata to Git.
- Do **not** treat UNKNOWN as a supported adapter.

---

## 9. Owner Decisions Required

| # | decision | suggested default |
|---|---|---|
| D1 | Proceed with first-intake sample (RC1_024)? | Yes — zero config, exact adapter match |
| D2 | Confirm adapter-key name mappings (citic→citics, guoxin→guosen, xingye→xyzc, gt_haitong→gtja)? | Confirm each pair; add alias in mapping layer |
| D3 | How to implement name alignment? | Recommended: add `parser_adapter_key` column to mapping table, keep RC1 `adapter_key` as audit trail |
| D4 | Allow expected output generation for intake samples? | Only after owner reviews parser output |
| D5 | Allow committing sanitized workbooks to Git, or local only? | Owner decision |
| D6 | Treat RC1_001 (UNKNOWN) as permanent gap case? | Yes — retain as reference, do not enter baseline |

---

## 10. Validation Commands

```powershell
git status --short
git diff --check
git diff --name-only
dir data_samples\local_rc1\pricing-parser-rc1-intake-001\workbooks
```
