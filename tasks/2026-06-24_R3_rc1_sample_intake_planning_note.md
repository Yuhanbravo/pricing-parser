# R3 RC1 Sample Intake — Planning Note

## Objective

Plan how, and in what order, to introduce 8 sanitized RC1 workbooks from the `Pricing_sheet` handoff into `pricing-parser`'s sample coverage. This is a planning-only task — no parser runtime changes, no expected output generation, no baseline refresh.

---

## 1. Materials Reviewed

All files live under `data_samples/local_rc1/pricing-parser-rc1-intake-001/` (gitignored, local-only). This directory cannot be verified by CI or contributors without the owner-provided handoff package.

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

The table below distinguishes **parser adapter keys** (runtime contract, as registered in the parser) from **RC1 / Pricing_sheet keys** (source aliases, retained as audit metadata).

| sample_id | scenario | parser_adapter_key | source_adapter_key (RC1) | actual ext | workbook |
|---|---|---|---|---|---|
| RC1_001 | `normal_day` | — | UNKNOWN | `.xlsx` | `2025-03-27_PRODUCT_001估值表__1.xlsx` |
| RC1_024 | `month_end` | orient | orient | `.xlsx` | `PRODUCT_011_估值表_20260430.xlsx` |
| RC1_025 | `month_end` | xyzc | xingye | `.xls` | `20250630_PRODUCT_005_证券投资基金估值表.xls` |
| RC1_026 | `month_end` | guosen | guoxin | `.xls` | `20251031_PRODUCT_002_证券投资基金估值表.xls` |
| RC1_028 | `quarter_end` | xyzc | xingye | `.xls` | `PRODUCT_009_资产估值表_20260331.xls` |
| RC1_030 | `quarter_end` | citics | citic | `.xlsx` | `2025-02-28_PRODUCT_001估值表.xlsx` |
| RC1_032 | `special_day` | gtja | gt_haitong | `.xls` | `PRODUCT_014_估值表_20250910.xls` |
| RC1_034 | `special_day` | citics | citic | `.xls` | `PRODUCT_006_资产估值表_20260211.xls` |

All 8 files confirmed present in the workbooks directory.

### Adapter-Key Loading Rule

The current parser canonical mapping path reads `adapter_key` and validates it against registered parser adapter keys. Therefore:

- **`parser_adapter_key`** (the runtime-loaded column) must continue to hold parser-native keys: `citics`, `guosen`, `xyzc`, `gtja`, `orient`.
- **RC1 / Pricing_sheet keys** (`citic`, `guoxin`, `xingye`, `gt_haitong`) must be stored as source aliases / audit metadata (e.g., `source_adapter_key`, `rc1_adapter_key`, `pricing_sheet_key`).
- If a future change wants the loaded `adapter_key` column to hold RC1 / Pricing_sheet keys while adding a new `parser_adapter_key` for runtime use, that requires a dedicated loader support implementation and test PR — it is out of scope for this planning PR.

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

### By Parser Adapter Key

| parser_adapter_key | count | source_alias (RC1) | status |
|---|---|---|---|
| `orient` | 1 | `orient` | ✅ exact match |
| `citics` | 2 | `citic` | ⚠️ naming variant |
| `guosen` | 1 | `guoxin` | ⚠️ naming variant |
| `xyzc` | 2 | `xingye` | ⚠️ naming variant |
| `gtja` | 1 | `gt_haitong` | ⚠️ naming variant |
| — (UNKNOWN) | 1 | `UNKNOWN` | ❌ gap case only |

---

## 4. Key Findings

### 4.1 Adapter-key Naming Gap

RC1 and pricing-parser use different naming conventions for the same custodians. All 5 variant pairs refer to the **same custodian** — no new adapter logic is needed, only name alignment:

| RC1 key (source alias) | Parser key (runtime) | Custodian |
|---|---|---|
| `citic` | `citics` | 中信证券 |
| `guoxin` | `guosen` | 国信证券 |
| `xingye` | `xyzc` | 兴业证券 |
| `gt_haitong` | `gtja` | 国泰海通 |
| `orient` | `orient` | 东方证券 (exact match) |

The runtime-loaded `adapter_key` column must continue to hold the parser-native keys above. RC1 / Pricing_sheet keys are source aliases. See Section 2 "Adapter-Key Loading Rule" for the full rationale and implementation boundary.

### 4.2 Extension Metadata Inconsistency

Two samples have a mismatch between the manifest `extension` field and the actual workbook filename extension:

| sample | manifest says | actual file | parser rule |
|---|---|---|---|
| RC1_026 | `.xlsx` | `.xls` | Use actual filename extension |
| RC1_030 | `.xls` | `.xlsx` | Use actual filename extension |

Per the task package: this is known, not a blocker. Manifest `extension` is retained as source metadata only; parser keys off the actual file extension.

### 4.3 All Non-UNKNOWN Products Are Mapped

Every non-UNKNOWN sample's `product_stub` and `custodian_id` exist in `产品与托管机构映射表.csv`. No mapping gaps for the 7 usable samples.

### 4.4 Workbook Filename ≠ product_stub

RC1_025, RC1_026, RC1_028, and RC1_030 show workbook filenames that differ from their manifest `product_stub`. This is expected in sanitized handoff packages — always treat the manifest as authoritative for product identity.

---

## 5. First-Intake Candidate Recommendations (R3-B)

Owner decision: first intake uses 3 samples in layered roles — one baseline candidate plus two dry-run / gap-analysis candidates. This exposes alias and `.xls` risks without making issue attribution too hard.

| role | sample | adapter path | scenario | ext | reason |
|---|---|---|---|---|---|
| **Baseline candidate** | **RC1_024** | `orient` (exact match) | `month_end` | `.xlsx` | Lowest risk. Only sample where RC1 key exactly matches a parser adapter. Zero config needed — can run parser immediately. |
| **Dry-run candidate** | **RC1_030** | `citic` → `citics` | `quarter_end` | `.xlsx` | Validates citic→citics alias resolution. Covers a new scenario for the citics adapter. |
| **Dry-run candidate** | **RC1_026** | `guoxin` → `guosen` | `month_end` | `.xls` | Validates guoxin→guosen alias resolution. Tests the parser's xlrd-based `.xls` path. |

Only **RC1_024** is a first-round baseline candidate. RC1_030 and RC1_026 are dry-run / gap-analysis candidates first; they do not enter the expected baseline until their outputs are reviewed.

Expected output generation for any sample requires owner approval in a dedicated implementation PR. Parser output must not be treated as truth automatically — the first RC1 expected baseline must be owner-reviewed to establish the acceptance pattern for later samples.

---

## 6. Deferred Samples

The following samples are deferred from the first intake round:

| sample | reason |
|---|---|
| RC1_025 | Deferred. Introduce after RC1_030 and RC1_026 dry runs establish stable alias patterns. |
| RC1_028 | Deferred. Introduce after RC1_025. |
| RC1_032 | Deferred. `special_day` + `gt_haitong`→`gtja` alias. Most complex scenario — run last. |
| RC1_034 | Deferred. `special_day` + `citic`→`citics` alias. Introduce after initial dry runs. |
| RC1_001 | Permanent gap-analysis reference. `adapter_key = UNKNOWN`. Not a baseline candidate. Must not trigger creation of an UNKNOWN adapter. |

`special_day` samples are deferred until initial intake exposes stable review queue patterns. R2 (review item regression expansion) remains deferred until RC1 dry runs reveal actual review item / review queue needs.

---

## 7. Risks

| risk | severity | mitigation |
|---|---|---|
| Naming alignment done wrong (wrong custodian mapped) | **High** | Owner/domain review required before any alias, custodian registry, or mapping-layer change. No automatic adapter-key aliasing in this planning PR. Wrong mapping would cause parser to use the wrong adapter. |
| `.xls` files expose parser bugs not seen in `.xlsx` | Low-Medium | Introduce `.xls` samples incrementally (dry-run first), not all at once |
| `special_day` data triggers unexpected review items | Medium | `special_day` samples deferred; review output before promoting to baseline |
| RC1_001 accidentally treated as a supported adapter case | Low | Explicitly labeled as gap case; do not create adapter for UNKNOWN |

---

## 8. Safety Verification

| check | status |
|---|---|
| `data_samples/local_rc1/` is gitignored | ✅ |
| No workbook files in `git status` | ✅ |
| All custodian IDs are `CUSTODIAN_XXX` (sanitized) | ✅ |
| All product IDs are `PRODUCT_XXX` (sanitized) | ✅ |
| No raw workbooks present | ✅ |
| No source paths or real identities leaked | ✅ |

---

## 9. Non-goals (This Round)

- Do **not** run the parser against any RC1 workbook.
- Do **not** generate expected output.
- Do **not** refresh `data_samples/expected/`.
- Do **not** modify adapters, routing, mapping, or taxonomy.
- Do **not** commit local RC1 handoff files, full manifests, workbooks, generated outputs, source paths, sensitive mapping, or residual sensitive metadata.
- Do **not** treat UNKNOWN as a supported adapter.

Sanitized aggregate planning metadata in this note (sample IDs, scenarios, extensions, sanitized product/custodian IDs, adapter keys, source aliases, coverage dimensions, planning-tier recommendations) is intentionally committed for owner review.

### Sanitized Workbook Commit Policy

RC1 sanitized workbooks are **local-only for now** and must remain gitignored. Do not commit workbooks or local RC1 handoff files unless the owner explicitly approves a future exception. Even sanitized workbooks may contain structure, metadata, or residual business-sensitive patterns.

---

## 10. R3-A: Custodian / Product-Custodian SSOT Alignment

Per owner decision, a dedicated phase is inserted before RC1 implementation:

**R3-A objective:** align pricing-parser's custodian / adapter naming with the Pricing_sheet SSOT before consuming RC1 samples, so that RC1 intake does not operate against dual SSOTs.

**R3-A scope:**
- Fix the `product_id → custodian_id → parser_adapter_key` mapping chain.
- Establish the canonical custodian registry and alias table.
- Produce the local SSOT seed (see Section 12).

**Boundary:** R3-A is still planning / alignment — it does not rename parser adapters or modify loader / runtime behavior.

**R3-B** (RC1 first-intake dry run and baseline proposal) follows after R3-A is confirmed.

---

## 11. Owner Direction: Pricing_sheet SSOT Alignment

**Owner direction:** Pricing-parser custodian naming and custodian registry should gradually align with the Pricing_sheet SSOT.

**Current PR scope:** Planning only. No adapter rename, no loader change, no runtime behavior change.

**Implementation boundary:** Pricing_sheet / RC1 keys are source aliases for now. Current parser adapter keys remain parser-native until a dedicated migration PR is approved. Directly aligning to the upstream SSOT is the correct direction, but adapter keys are a runtime contract and must not be implicitly changed in a planning PR.

---

## 12. Owner-Provided SSOT Seed Plan

Owner will provide a sanitized product-custodian mapping seed as the local SSOT input for R3-A.

**Allowed fields:**

| field | description |
|---|---|
| `product_id` | Sanitized product identifier |
| `custodian_id` | Sanitized custodian identifier |
| `custodian_short_name` | Short display name |
| `pricing_sheet_key` / `source_alias` | Key used in Pricing_sheet / RC1 |
| `parser_adapter_key` | Key used by parser runtime |
| `source_aliases` | Additional historical or variant keys |
| `is_cleared_product` | Whether the product has been cleared |
| `notes` | Free-text planning notes |

**Forbidden content — must not be submitted or introduced:**

- Real product names
- Product registration codes
- Real product codes
- Source paths
- Original SSOT Excel files
- Sensitive mapping exports
- Un-sanitized workbooks

The seed is **local-only / gitignored** in its first phase and must not be committed to Git directly.

---

## 13. Owner Decisions Recorded

| # | decision | rationale |
|---|---|---|
| D1 | PR #12 remains R3 planning only | Must not perform parser execution, expected output generation, baseline refresh, runtime changes, or adapter changes |
| D2 | Sanitized aggregate planning metadata may be committed | Enough sanitized structure for owner review; excludes local handoff files, full manifests, workbooks, generated outputs, source paths, sensitive mapping, real product/custodian identity, residual sensitive metadata |
| D3 | RC1 sanitized workbooks are local-only, must remain gitignored | Even sanitized workbooks may contain structure, metadata, or residual business-sensitive patterns; any future exception requires a separate owner-approved decision |
| D4 | Long-term direction: align custodian naming with Pricing_sheet SSOT | Maintaining separate naming systems creates SSOT drift; this PR records the direction but does not rename adapters or modify loader/runtime |
| D5 | Runtime-loaded `adapter_key` must remain parser-native for now; RC1 keys are source aliases | Current mapping loader validates against registered parser adapter keys; putting RC1 keys into that column would break validation or routing |
| D6 | Owner will provide sanitized product-custodian SSOT seed for R3-A | The stable chain needed is `product_id → custodian_id → parser_adapter_key` |
| D7 | R3-B first intake: 3 samples in layered roles (RC1_024 baseline candidate; RC1_030 + RC1_026 dry-run candidates) | One sample too narrow; all 8 at once makes issue attribution too hard |
| D8 | Expected output generation not authorized in this PR | Must be done in a dedicated implementation PR after owner approves the selected sample and review process |
| D9 | First RC1 expected baseline must be owner-reviewed | Parser output must not be treated as truth automatically; first baseline establishes acceptance pattern |
| D10 | RC1_001 remains permanent gap-analysis reference | UNKNOWN adapter key; must not enter baseline or trigger creation of an UNKNOWN adapter |
| D11 | R2 remains deferred | Review item regression should start after RC1 intake exposes actual review queue patterns |

---

## 14. Validation Commands

Windows (PowerShell):
```powershell
git status --short
git diff --check
git diff --name-only
dir data_samples\local_rc1\pricing-parser-rc1-intake-001\workbooks
```

POSIX (Git Bash / Linux):
```bash
git status --short
git diff --check
git diff --name-only
ls data_samples/local_rc1/pricing-parser-rc1-intake-001/workbooks/
```
