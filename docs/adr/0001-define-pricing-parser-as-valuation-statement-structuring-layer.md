# ADR-0001: Define pricing-parser as a valuation-statement structuring layer

## Status

Accepted

## Context

`pricing-parser` 需要明确自身在整体数据链路中的边界。仓库已经包含 parser runtime、mapping-driven routing、shared parsing/export logic、custodian adapters、tests 和文档协作约定，但仍需要用 owner decision record 明确：本仓库负责 valuation statement structuring，而不是下游分析、计算或查询服务。

## Decision

`pricing-parser` 是 valuation-statement structuring layer。

它负责从 custodians、brokers、outsourcing service providers，以及未来 OTC / non-standard valuation sources 收到的 valuation statement files 中识别、解析、清洗、标准化并导出结构化数据。

该 parser layer 应产出 stable、auditable、regression-testable、archive-ready 的 structured outputs，用于数据归档和 downstream consumption。

该 parser layer 不实现 downstream analysis 或 calculation logic。明确 non-goals 包括：

- portfolio analytics；
- performance attribution；
- return calculation；
- risk indicator calculation；
- valuation verification；
- market-data enrichment；
- investment decision analysis；
- reporting dashboards；
- data-center query services。

这些能力属于 downstream analysis、archive、reporting 或 data-center layers，不属于本 parser layer。

Parser 工作应优先保证：

- stable output contracts；
- traceability；
- regression coverage；
- archive-ready structure；
- clear review entrypoints。

## Consequences

- 新功能设计应先判断是否属于 valuation-statement structuring layer。
- 涉及 analytics、risk、return、market-data enrichment、dashboard 或 query service 的需求，应被归入下游层，而不是加入 parser runtime。
- Parser 变更应围绕可追溯、可回归、可归档的 structured outputs 进行设计和验证。
