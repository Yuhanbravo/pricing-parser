# ADR-0003: Separate valuation subjects, positions, review items, and exposures

## Status

Accepted

## Context

Valuation statement 中存在不同语义层级的数据。若强行把所有解析结果塞入单一 position table，会混淆 route decision、accounting subject、listed / standardized position、人审入口和未来 OTC / non-standard exposure valuation objects 的边界。

Owner 已确认：parser output objects 应按 semantic meaning 分离，而不是默认压平为一个持仓表。

## Decision

Parser 按 semantic meaning 分离 valuation-statement output objects。

Accepted object boundaries 如下：

- `routing_results`：文件识别、route decisions 和 identification results。
- `valuation_subjects`：accounting subjects 与 account-level valuation statement structure。
- `valuation_positions`：listed / exchange-traded / standardized security-like positions。
- `review_items`：human review entrypoints，用于 unresolved、ambiguous 或 intentionally non-promoted findings。
- `valuation_exposures`：未来 OTC / non-standard exposure valuation objects。

OTC / non-standard exposures 不应默认 promoted into `valuation_positions`。

未来 non-standard / OTC exposure object 名称为 `valuation_exposures`，不是 `valuation_derivatives`。原因是未来范围可能包括 total return swaps、OTC options、snowball-like structures、structured notes、financing-like exposures，以及其他经济上属于 exposure records、但不总能干净表达为 derivatives 的 non-standard valuation units。

Detailed `valuation_exposures` field groups、schema、sample governance 和 parsing implementation 明确 deferred 到未来 ADR / task。

本 ADR 只记录 owner decision，不引入 `valuation_exposures` runtime table、schema、exporter fields、tests 或 baselines。

## Consequences

- 未来 parser 或 export 设计应尊重 output object 的语义边界。
- 不应为了短期导出方便，把 OTC / non-standard exposure findings 默认塞入 `valuation_positions`。
- 引入 `valuation_exposures` 的详细 schema、fixtures、sample policy、parser implementation 或 baseline 变更前，需要单独 ADR / task 和正常 validation。
