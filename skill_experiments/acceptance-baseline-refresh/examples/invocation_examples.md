# Invocation Examples

## Round 4 Example

请使用 `acceptance-baseline-refresh` 草案流程，对 Round 4 asset taxonomy 改动后的 expected baseline 进行：

1. 受控重跑
2. 与 `data_samples/expected/` 对比
3. 将差异分类为“预期契约更新 / 潜在回归 / 待确认”
4. 仅刷新被判定为预期契约更新的 baseline
5. 输出 baseline refresh 报告，并同步 README / HANDOFF / status

## Negative Example

如果当前 smoke 仍失败，或者 task package 尚未明确授权输出字段变化，则不要进入 baseline refresh；应先完成实现与最小验证，再回到本流程。