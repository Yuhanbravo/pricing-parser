# Parse Summary

- Processed files: 11
- Successful routes: 10
- Manual overrides: 0
- Routing failures: 1
- Supported adapters in run: citics, cmsc, csc, greatwall, gtja, guosen, orient, xyzc
- Subject rows exported: 1022
- Position rows exported: 182
- Review flagged subjects: 238
- Review flagged positions: 0
- Review items exported: 238
- Normalization issues: 0
- Unrouted files: 估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx
- Generic fallback routes used: 0
- Fallback note: generic fallback runs only when --allow-generic-fallback is explicitly enabled.
- Review entrypoint: first inspect valuation_subjects.csv / valuation_positions.csv rows with review_flag=1, then use review_items.csv.review_reason and valuation_positions.csv.review_note for concrete reasons.
- Supported asset types: a_share, fund_or_etf, hk_equity
- Unsupported asset types: none

## Unrouted File Details
- 估值表日报-XXX022-PRODUCT_022-4-20250327.xlsx

## Review Queue By Source File
- 2025-03-27_PRODUCT_001估值表.xlsx: 35 review entries; top reasons: 叶子行存在市价但缺少数量 (21), 衍生工具科目，需单独建模或排除 (9), 估值增值汇总行，通常不作为持仓叶子 (5)
- 20250327_PRODUCT_002_证券投资基金估值表.csv: 37 review entries; top reasons: 衍生工具科目，需单独建模或排除 (33), 估值增值汇总行，通常不作为持仓叶子 (4)
- 20250327_PRODUCT_002_证券投资基金估值表.xls: 37 review entries; top reasons: 衍生工具科目，需单独建模或排除 (33), 估值增值汇总行，通常不作为持仓叶子 (4)
- PRODUCT_006_资产估值表_20250327.xls: 12 review entries; top reasons: 衍生工具科目，需单独建模或排除 (8), 叶子行存在市价但缺少数量 (4)
- PRODUCT_008委托资产资产估值表20250327.xls: 25 review entries; top reasons: 衍生工具科目，需单独建模或排除 (25)
- PRODUCT_010_证券投资基金估值表_2025-03-27.xls: 10 review entries; top reasons: 衍生工具科目，需单独建模或排除 (6), 估值增值汇总行，通常不作为持仓叶子 (4)
- PRODUCT_012_估值表_20250327.xls: 20 review entries; top reasons: 衍生工具科目，需单独建模或排除 (16), 估值增值汇总行，通常不作为持仓叶子 (4)
- XXX007_PRODUCT_007_估值表_20250327.xls: 11 review entries; top reasons: 衍生工具科目，需单独建模或排除 (7), 估值增值汇总行，通常不作为持仓叶子 (4)
- 估值表_PRODUCT_021_20250327.xls: 40 review entries; top reasons: 叶子行存在市价但缺少数量 (21), 衍生工具科目，需单独建模或排除 (15), 估值增值汇总行，通常不作为持仓叶子 (4)
- 证券投资基金估值表_PRODUCT_023_2025-03-27.xlsx: 11 review entries; top reasons: 衍生工具科目，需单独建模或排除 (10), 估值增值汇总行，通常不作为持仓叶子 (1)
