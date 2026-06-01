# OTC Derivative Review Rules

## Round 5A Principle

When a subject appears derivative-like but the valuation table does not expose enough contract detail, the item should enter review instead of being forced into ordinary positions.

## Candidate Rule Families

### Derivative subject without contract identity

- Trigger: subject name or standard subject suggests derivative exposure but no contract identifier is available
- Outcome: create derivative review item

### Margin without clear linked contract

- Trigger: margin-like balance exists and derivative context is plausible, but no stable contract join is available
- Outcome: keep as non-position accounting subject and open review

### Fair-value movement without underlying attribution

- Trigger: derivative-related fair-value movement exists but underlying asset is unknown
- Outcome: keep contract candidate incomplete and mark lookthrough pending

### Counterparty-dependent interpretation

- Trigger: valuation-table wording suggests swap, option, forward, or other OTC structure, but counterparty or settlement method is missing
- Outcome: require supplemental data before downstream modeling

## Pattern-Confirmation Gate Before Round 5D

The derivative subject patterns in `data/reference/otc_derivative_subject_patterns.csv` fall into two categories:

| Category | Pattern IDs | Confidence | Status |
|---|---|---|---|
| High-confidence anchor | DERIV-001 | high | Ready for reference use; subject-code-based match with clear chapter authority |
| Medium/low patterns requiring business confirmation | DERIV-002 — DERIV-007 | medium / low | **Not implicitly approved for runtime.** Each pattern was derived from keyword or section-context matching of the official reference documents. No business-side or product-domain review has been performed. |

### Confirmation gate

DERIV-002 through DERIV-007 **must receive explicit business-side confirmation** before being promoted to runtime use in Round 5D (OTC derivative minimum parsing and review queue). The confirmation must cover:

1. Whether the keyword pattern correctly identifies the intended derivative type in the repository's valuation-table population.
2. Whether the proposed `derivative_type` label matches domain practice.
3. Whether any pattern produces false positives that need exclusion rules.
4. Whether the `needs_review` flag should stay `yes` or can be lowered to `no` for specific patterns.

Until confirmed, these patterns remain design candidates only. A future implementer should **not** treat `confidence: medium` as implicitly approved for runtime.

The confirmation step is assigned to **business-side / domain-expert review** and is not expected to be resolved during Round 5A or Round 5B. The recommended trigger round for confirmation is Round 5C (OTC derivative model design finalization) or early Round 5D, before any runtime derivative identification code is written.

## Boundary

Round 5A defines these rules as design candidates only. It does not implement runtime review generation beyond the repository's current behavior.
