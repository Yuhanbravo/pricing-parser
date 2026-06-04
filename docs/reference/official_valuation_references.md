# Official Valuation References

## Purpose

This document records the official reference set introduced in Round 5A and explains how each source is used inside this repository.

## Reference Set

### 中国基金估值标准 2018

- Primary role: valuation-guidance context and standard subject lookup support
- Useful evidence in current Round 5A work:
  - subject list including 1002, 1021, 1031, 1104, 1105, 1202, 1203, 2203, 2206, 2207, 2208, 2221, 3003, 4001
  - narrative treatment of bank deposits, settlement reserves, margin deposits, repo assets, clearing balances, and undistributed profit
  - valuation-language context for public-fair-value interpretation
- Current use boundary: reference only

### 证券投资基金会计核算操作实务手册-20240530

- Primary role: standard accounting subject structure and business-scene examples
- Useful evidence in current Round 5A work:
  - chapterized subject tables for股票、债券/资产支持证券、基金、衍生工具、买入返售、存款与短期借款等业务
  - explicit Chapter 5 derivative-business indexing
  - practical examples for 1102, 1103, 1105, 1203, 2221, 3003, 3102 and public-fair-value movement treatment
- Current use boundary: reference only

## Repository Boundary

Round 5A introduces these materials as reusable repository assets, not as executable parser configuration.

The intended layer order remains:

1. raw valuation-table subject
2. standard accounting subject layer
3. internal asset taxonomy layer
4. business-facing display layer

Round 5A does not change runtime exports, does not widen parser outputs, and does not reclassify ordinary positions using these sources directly.
