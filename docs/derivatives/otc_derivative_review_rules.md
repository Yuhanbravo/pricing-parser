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

## Boundary

Round 5A defines these rules as design candidates only. It does not implement runtime review generation beyond the repository's current behavior.
