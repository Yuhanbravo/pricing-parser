# ADR-0002: Use ADRs as owner decision records

## Status

Accepted

## Context

本仓库已有 [`README.md`](../../README.md)、[`docs/status.md`](../status.md)、[`docs/roadmap.md`](../roadmap.md)、[`docs/HANDOFF.md`](../HANDOFF.md)、[`MIGRATION_PLAN.md`](../../MIGRATION_PLAN.md) 和 [`tasks/`](../../tasks/) 等 planning、handoff 与 audit trail 文档。缺少 ADR layer 时，开发者、实习生、reviewer 和 AI agent 难以区分 owner accepted decision、roadmap planning、historical execution record 和未来需要 owner decision 的事项。

## Decision

引入 `docs/adr/` 作为 formal owner decision layer。

ADR 用于记录重要 owner decisions，以及 rejected、deferred、superseded alternatives。ADR 可以链接既有文档以提供上下文，但不复制 current status snapshot 或 roadmap phase text。

只有 `Accepted` ADR 是 implementation guidance。

`Proposed` ADR 是 discussion draft，不能作为 runtime behavior、output contract、baseline 或 sample policy 变更的权威依据。

Runtime changes、baseline changes 和 sample-policy changes 仍然必须经过正常 task package、PR review 和 validation。ADR 不能替代实现任务、测试、基线审查或样本治理流程。

## Consequences

- 涉及 product boundary、architecture、output contract、sample / fixture governance 或 owner-approved semantics 的事项，应优先判断是否需要 ADR。
- ADR 文档应保持轻量，只记录决策、背景、影响和必要链接。
- 状态快照继续归 [`docs/status.md`](../status.md) 管理，路线图继续归 [`docs/roadmap.md`](../roadmap.md) 管理，任务执行留痕继续归 [`tasks/`](../../tasks/) 管理。
